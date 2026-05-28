"""Colour correction matrix utilities."""

from __future__ import annotations

import numpy as np


def apply_color_matrix(rgb: np.ndarray, matrix: np.ndarray | None = None) -> np.ndarray:
    """Apply a 3x3 colour correction matrix to an RGB image."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("rgb must have shape HxWx3")
    if matrix is None:
        matrix = np.eye(3, dtype=np.float32)
    matrix = np.asarray(matrix, dtype=np.float32)
    if matrix.shape != (3, 3):
        raise ValueError("matrix must have shape 3x3")
    return np.tensordot(rgb.astype(np.float32), matrix.T, axes=1)
