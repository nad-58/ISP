"""White-balance utilities."""

from __future__ import annotations

import numpy as np


def apply_rgb_gains(rgb: np.ndarray, gains: tuple[float, float, float]) -> np.ndarray:
    """Apply per-channel RGB gains."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("rgb must have shape HxWx3")
    gain_array = np.asarray(gains, dtype=np.float32).reshape(1, 1, 3)
    return rgb.astype(np.float32) * gain_array


def gray_world_gains(rgb: np.ndarray, eps: float = 1e-6) -> tuple[float, float, float]:
    """Estimate white-balance gains using the gray-world assumption."""
    if rgb.ndim != 3 or rgb.shape[2] != 3:
        raise ValueError("rgb must have shape HxWx3")
    means = rgb.reshape(-1, 3).mean(axis=0).astype(np.float32)
    target = float(means.mean())
    gains = target / np.maximum(means, eps)
    return tuple(float(x) for x in gains)
