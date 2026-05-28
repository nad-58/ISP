"""Lens-shading correction utilities."""

from __future__ import annotations

import cv2
import numpy as np

from .bayer import channel_masks


def apply_mesh_lens_shading(
    raw: np.ndarray,
    mesh_rgb: np.ndarray,
    pattern: str = "RGGB",
    mode: str = "divide",
    eps: float = 1e-6,
) -> np.ndarray:
    """Apply a low-resolution RGB lens-shading mesh to a Bayer image."""
    image = raw.astype(np.float32, copy=False)
    mesh = np.asarray(mesh_rgb, dtype=np.float32)
    if mesh.ndim != 3 or mesh.shape[2] != 3:
        raise ValueError("mesh_rgb must have shape HxWx3")

    full = cv2.resize(mesh, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_CUBIC)
    masks = channel_masks(image.shape, pattern)
    gain = np.ones_like(image, dtype=np.float32)
    gain[masks["R"]] = full[..., 0][masks["R"]]
    gain[masks["G"]] = full[..., 1][masks["G"]]
    gain[masks["B"]] = full[..., 2][masks["B"]]

    if mode == "divide":
        return image / np.maximum(gain, eps)
    if mode == "multiply":
        return image * gain
    raise ValueError("mode must be 'divide' or 'multiply'")


def radial_lens_shading_map(
    shape: tuple[int, int],
    strength: float = 0.25,
    center: tuple[float, float] | None = None,
) -> np.ndarray:
    """Generate a simple synthetic radial shading map for demonstrations."""
    height, width = shape
    yy, xx = np.indices((height, width), dtype=np.float32)
    if center is None:
        center = ((width - 1) / 2.0, (height - 1) / 2.0)
    cx, cy = center
    radius = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    radius /= max(float(radius.max()), 1e-6)
    return 1.0 - strength * radius**2
