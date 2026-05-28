"""Simple Bayer demosaicing utilities."""

from __future__ import annotations

import cv2
import numpy as np

_BAYER_TO_CV2 = {
    "RGGB": cv2.COLOR_BayerRG2RGB,
    "BGGR": cv2.COLOR_BayerBG2RGB,
    "GRBG": cv2.COLOR_BayerGR2RGB,
    "GBRG": cv2.COLOR_BayerGB2RGB,
}


def demosaic_bilinear(bayer: np.ndarray, pattern: str = "RGGB") -> np.ndarray:
    """Convert a Bayer image to RGB using OpenCV bilinear demosaicing."""
    pattern = pattern.upper()
    if pattern not in _BAYER_TO_CV2:
        raise ValueError(f"Unsupported Bayer pattern: {pattern}")
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2D array")

    image = np.asarray(bayer)
    if image.dtype != np.uint16:
        image = np.clip(image, 0, 65535).astype(np.uint16)
    return cv2.cvtColor(image, _BAYER_TO_CV2[pattern]).astype(np.float32)
