"""Automatic gain utilities."""

from __future__ import annotations

import numpy as np


def percentile_autogain(
    image: np.ndarray,
    percentile: float = 99.95,
    target: float = 1.0,
    max_gain: float = 4.0,
) -> tuple[np.ndarray, float]:
    """Scale an image so a high percentile reaches the target level."""
    arr = image.astype(np.float32)
    level = float(np.percentile(arr, percentile))
    if level <= 0:
        return arr, 1.0
    gain = min(target / level, max_gain)
    return arr * gain, float(gain)
