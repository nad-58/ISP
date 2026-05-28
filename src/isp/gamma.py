"""Gamma correction utilities."""

from __future__ import annotations

import numpy as np


def apply_gamma(rgb: np.ndarray, gamma: float = 2.2, max_value: float = 65535.0) -> np.ndarray:
    """Apply gamma encoding to a linear RGB image."""
    if gamma <= 0:
        raise ValueError("gamma must be positive")
    linear = np.clip(rgb.astype(np.float32) / max_value, 0.0, 1.0)
    encoded = np.power(linear, 1.0 / gamma)
    return encoded * max_value


def to_uint8(rgb: np.ndarray, max_value: float = 65535.0) -> np.ndarray:
    """Convert an RGB image to 8-bit display range."""
    return np.clip(rgb / max_value * 255.0, 0, 255).astype(np.uint8)
