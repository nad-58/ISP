"""Zone statistics for AE, AWB, and AF style control loops."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def zone_grid(image: np.ndarray, rows: int, cols: int) -> list[np.ndarray]:
    """Split an image into approximately equal zones."""
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")
    y_edges = np.linspace(0, image.shape[0], rows + 1, dtype=int)
    x_edges = np.linspace(0, image.shape[1], cols + 1, dtype=int)
    return [image[y_edges[r]:y_edges[r + 1], x_edges[c]:x_edges[c + 1]] for r in range(rows) for c in range(cols)]


def ae_histogram(image: np.ndarray, bins: int = 256) -> np.ndarray:
    """Compute a normalized luminance histogram."""
    arr = np.clip(image.astype(np.float32), 0.0, 1.0)
    hist, _ = np.histogram(arr, bins=bins, range=(0.0, 1.0))
    total = max(int(hist.sum()), 1)
    return hist.astype(np.float32) / total


def awb_gray_world_rgb(rgb: np.ndarray, eps: float = 1e-6) -> dict[str, float]:
    """Return simple colour-ratio statistics for AWB demonstrations."""
    mean = rgb.reshape(-1, 3).astype(np.float32).mean(axis=0)
    r, g, b = mean
    return {
        "r_over_g": float(r / max(g, eps)),
        "b_over_g": float(b / max(g, eps)),
        "g_over_r": float(g / max(r, eps)),
        "g_over_b": float(g / max(b, eps)),
    }


def af_sharpness_metric(gray: np.ndarray) -> float:
    """Return a simple focus metric based on high-frequency energy."""
    image = gray.astype(np.float32)
    lap = ndimage.laplace(image, mode="reflect")
    return float(np.mean(lap * lap))
