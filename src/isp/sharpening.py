"""Image-detail enhancement utilities."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def enhance_detail(rgb: np.ndarray, strength: float = 0.75) -> np.ndarray:
    """Enhance detail using a difference-of-blurs filter."""
    image = rgb.astype(np.float32)
    small_kernel = np.outer([1, 2, 1], [1, 2, 1]).astype(np.float32) / 16.0
    large_kernel = np.outer([1, 4, 6, 4, 1], [1, 4, 6, 4, 1]).astype(np.float32) / 256.0

    small = np.empty_like(image)
    large = np.empty_like(image)
    for channel in range(image.shape[2]):
        small[..., channel] = ndimage.convolve(image[..., channel], small_kernel, mode="reflect")
        large[..., channel] = ndimage.convolve(image[..., channel], large_kernel, mode="reflect")
    return image + strength * (small - large)
