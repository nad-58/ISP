"""Defect-pixel correction for raw Bayer images."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


_SALT_KERNEL = np.array(
    [
        [-1, 0, -2, 0, -1],
        [0, 0, 0, 0, 0],
        [-2, 0, 12, 0, -2],
        [0, 0, 0, 0, 0],
        [-1, 0, -2, 0, -1],
    ],
    dtype=np.float32,
) / 16.0

_NEIGHBOUR_AVERAGE_KERNEL = np.array(
    [
        [1, 0, 2, 0, 1],
        [0, 0, 0, 0, 0],
        [2, 0, 0, 0, 2],
        [0, 0, 0, 0, 0],
        [1, 0, 2, 0, 1],
    ],
    dtype=np.float32,
) / 12.0

_NORMALISATION_KERNEL = np.array(
    [
        [1, 0, 2, 0, 1],
        [0, 0, 0, 0, 0],
        [2, 0, 4, 0, 2],
        [0, 0, 0, 0, 0],
        [1, 0, 2, 0, 1],
    ],
    dtype=np.float32,
) / 16.0


def correct_defect_pixels(
    raw: np.ndarray,
    threshold: float = 1.0,
    eps: float = 1e-6,
) -> np.ndarray:
    """Replace isolated hot or dead pixels using same-colour neighbours."""
    image = raw.astype(np.float32, copy=False)
    response = ndimage.convolve(image, _SALT_KERNEL, mode="reflect")
    local_level = ndimage.convolve(image, _NORMALISATION_KERNEL, mode="reflect")
    score = response / np.maximum(local_level, eps)
    mask = np.abs(score) > threshold
    replacement = ndimage.convolve(image, _NEIGHBOUR_AVERAGE_KERNEL, mode="reflect")
    return np.where(mask, replacement, image)
