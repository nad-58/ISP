from __future__ import annotations

import numpy as np
import pytest

from isp.black_level import correct_black_level
from isp.demosaic import demosaic_bilinear
from isp.gamma import apply_gamma, to_uint8
from isp.tone_mapping import reinhard_tone_map


def test_black_level_uses_float_and_clips_negative_values() -> None:
    raw = np.array([[10, 20], [30, 40]], dtype=np.uint8)
    corrected = correct_black_level(raw, offsets=(16, 16, 16, 16), pattern="RGGB")
    assert corrected.dtype == np.float32
    assert np.all(corrected >= 0)


def test_demosaic_validates_pattern() -> None:
    raw = np.full((4, 4), 1000, dtype=np.float32)
    with pytest.raises(ValueError):
        demosaic_bilinear(raw, pattern="INVALID")


def test_demosaic_returns_rgb_shape() -> None:
    raw = np.arange(64, dtype=np.float32).reshape(8, 8)
    rgb = demosaic_bilinear(raw, pattern="RGGB")
    assert rgb.shape == (8, 8, 3)
    assert np.isfinite(rgb).all()


def test_tone_mapping_and_gamma_remain_finite() -> None:
    rgb = np.array([[[0.0, 1.0, 1000.0]]], dtype=np.float32)
    mapped = reinhard_tone_map(rgb)
    gamma = apply_gamma(mapped, gamma=2.2, max_value=1.0)
    output = to_uint8(gamma, max_value=1.0)
    assert np.isfinite(mapped).all()
    assert np.isfinite(gamma).all()
    assert output.dtype == np.uint8
    assert output.min() >= 0 and output.max() <= 255
