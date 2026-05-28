from __future__ import annotations

import numpy as np

from isp.autogain import percentile_autogain
from isp.defect_pixel import correct_defect_pixels
from isp.green_equalization import equalize_green_channels
from isp.lens_shading import apply_mesh_lens_shading
from isp.pipeline import ISPConfig, ISPPipeline
from isp.statistics import ae_histogram, af_sharpness_metric, awb_gray_world_rgb


def test_pipeline_runs_on_synthetic_bayer() -> None:
    raw = np.full((32, 48), 2048, dtype=np.uint16)
    raw[10, 10] = 65535
    rgb = ISPPipeline(ISPConfig()).run(raw)
    assert rgb.shape == (32, 48, 3)
    assert rgb.dtype == np.uint8


def test_defect_pixel_correction_reduces_spike() -> None:
    raw = np.ones((16, 16), dtype=np.float32)
    raw[8, 8] = 100.0
    corrected = correct_defect_pixels(raw, threshold=0.5)
    assert corrected[8, 8] < 100.0


def test_green_equalization_preserves_shape() -> None:
    raw = np.random.default_rng(0).random((16, 16)).astype(np.float32)
    out = equalize_green_channels(raw, pattern="RGGB")
    assert out.shape == raw.shape


def test_mesh_lens_shading_preserves_shape() -> None:
    raw = np.ones((16, 16), dtype=np.float32)
    mesh = np.ones((4, 4, 3), dtype=np.float32)
    out = apply_mesh_lens_shading(raw, mesh)
    assert out.shape == raw.shape


def test_statistics_helpers() -> None:
    gray = np.random.default_rng(1).random((32, 32)).astype(np.float32)
    rgb = np.dstack([gray, gray, gray])
    hist = ae_histogram(gray)
    assert np.isclose(hist.sum(), 1.0)
    assert awb_gray_world_rgb(rgb)["r_over_g"] > 0
    assert af_sharpness_metric(gray) >= 0


def test_percentile_autogain() -> None:
    image = np.full((8, 8), 0.25, dtype=np.float32)
    out, gain = percentile_autogain(image, target=1.0)
    assert gain > 1.0
    assert out.mean() > image.mean()
