"""Chroma noise reduction in a YCbCr-like colour space."""

from __future__ import annotations

import cv2
import numpy as np


_RGB_TO_YCBCR = np.array(
    [
        [0.2990, 0.5870, 0.1140],
        [-0.1687, -0.3313, 0.5000],
        [0.5000, -0.4187, -0.0813],
    ],
    dtype=np.float32,
)
_YCBCR_TO_RGB = np.linalg.inv(_RGB_TO_YCBCR)


def reduce_chroma_noise(rgb: np.ndarray, kernel_size: int = 9, strength: float = 0.6) -> np.ndarray:
    """Blur chroma channels while preserving luma."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("rgb must have shape HxWx3")
    if kernel_size % 2 == 0:
        kernel_size += 1
    image = np.clip(rgb.astype(np.float32), 0.0, 1.0)
    ycc = np.tensordot(image, _RGB_TO_YCBCR.T, axes=1)
    ycc[..., 1:] += 0.5

    blurred_cb = cv2.GaussianBlur(ycc[..., 1], (kernel_size, kernel_size), 0)
    blurred_cr = cv2.GaussianBlur(ycc[..., 2], (kernel_size, kernel_size), 0)
    ycc[..., 1] = (1.0 - strength) * ycc[..., 1] + strength * blurred_cb
    ycc[..., 2] = (1.0 - strength) * ycc[..., 2] + strength * blurred_cr

    ycc[..., 1:] -= 0.5
    out = np.tensordot(ycc, _YCBCR_TO_RGB.T, axes=1)
    return np.clip(out, 0.0, 1.0)
