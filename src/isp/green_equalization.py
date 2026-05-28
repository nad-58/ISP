"""Green-channel equalisation for Bayer images."""

from __future__ import annotations

import numpy as np
from scipy import ndimage

from .bayer import channel_masks


def equalize_green_channels(
    raw: np.ndarray,
    pattern: str = "RGGB",
    strength: float = 0.5,
    threshold: float = 0.02,
) -> np.ndarray:
    """Reduce imbalance between the two green Bayer sample positions."""
    if not 0 <= strength <= 1:
        raise ValueError("strength must be between 0 and 1")

    image = raw.astype(np.float32, copy=True)
    masks = channel_masks(image.shape, pattern)
    green = np.where(masks["G"], image, 0.0)

    kernel = np.array(
        [
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
        ],
        dtype=np.float32,
    )
    local_sum = ndimage.convolve(green, kernel, mode="reflect")
    local_count = ndimage.convolve(masks["G"].astype(np.float32), kernel, mode="reflect")
    local_green = local_sum / np.maximum(local_count, 1.0)

    scale = max(float(np.percentile(image, 99.0)), 1e-6)
    edge_safe = np.abs(image - local_green) / scale < threshold
    update_mask = masks["G"] & edge_safe
    image[update_mask] = (1.0 - strength) * image[update_mask] + strength * local_green[update_mask]
    return image
