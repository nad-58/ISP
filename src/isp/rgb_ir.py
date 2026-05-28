"""Basic RGB-IR raw-pattern processing utilities."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def separate_rgb_ir_bgir(
    raw: np.ndarray,
    correction_matrix: np.ndarray | None = None,
    highlight_level: float = 0.95,
) -> tuple[np.ndarray, np.ndarray]:
    """Convert a simple BGIR-style 2x2 pattern into corrected Bayer plus IR."""
    image = raw.astype(np.float32, copy=True)
    b = image[0::2, 0::2]
    ir = image[0::2, 1::2]
    g = image[1::2, 0::2]
    r = image[1::2, 1::2]

    if correction_matrix is not None:
        mat = np.asarray(correction_matrix, dtype=np.float32)
        if mat.shape != (3, 4):
            raise ValueError("correction_matrix must have shape 3x4")
        highlight_mask = np.ones_like(ir)
        highlight_mask[(r > highlight_level) & (g > highlight_level) & (b > highlight_level)] = 0.1
        highlight_mask = ndimage.gaussian_filter(highlight_mask, sigma=1.0)
        stack = np.stack([r, g, b, ir * highlight_mask], axis=-1)
        corrected = np.tensordot(stack, mat.T, axes=1)
        r, g, b = corrected[..., 0], corrected[..., 1], corrected[..., 2]

    corrected_raw = np.empty_like(image)
    corrected_raw[0::2, 0::2] = b
    corrected_raw[0::2, 1::2] = g
    corrected_raw[1::2, 0::2] = g
    corrected_raw[1::2, 1::2] = r
    return corrected_raw, ir
