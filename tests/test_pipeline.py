from __future__ import annotations

import numpy as np

from isp import ISPPipeline, ISPConfig


def test_pipeline_returns_uint8_rgb_image() -> None:
    height, width = 32, 48
    bayer = np.full((height, width), 2048, dtype=np.uint16)
    pipeline = ISPPipeline(ISPConfig())

    result = pipeline.run(bayer)

    assert result.shape == (height, width, 3)
    assert result.dtype == np.uint8
