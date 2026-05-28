"""Simple tone mapping utilities."""

from __future__ import annotations

import numpy as np


def reinhard_tone_map(rgb: np.ndarray, white_point: float | None = None) -> np.ndarray:
    """Apply a simple global Reinhard tone-mapping curve.

    This is an educational approximation of dynamic range compression, not a
    hardware-specific local tone-mapping implementation.
    """
    image = np.maximum(rgb.astype(np.float32), 0.0)
    if white_point is None:
        white_point = float(np.percentile(image, 99.5))
    white_point = max(white_point, 1e-6)
    normalized = image / white_point
    mapped = normalized / (1.0 + normalized)
    return mapped * white_point
