"""Bayer-pattern utilities for educational ISP processing."""

from __future__ import annotations

import numpy as np


_PATTERN_TILES: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {
    "RGGB": (("R", "Gr"), ("Gb", "B")),
    "GRBG": (("Gr", "R"), ("B", "Gb")),
    "GBRG": (("Gb", "B"), ("R", "Gr")),
    "BGGR": (("B", "Gb"), ("Gr", "R")),
}


def normalize_pattern(pattern: str) -> str:
    """Return a validated uppercase Bayer pattern name."""
    pattern = str(pattern).upper()
    if pattern not in _PATTERN_TILES:
        raise ValueError(f"Unsupported Bayer pattern: {pattern}")
    return pattern


def channel_masks(shape: tuple[int, int], pattern: str = "RGGB") -> dict[str, np.ndarray]:
    """Create Boolean masks for the Bayer colour samples."""
    pattern = normalize_pattern(pattern)
    masks = {
        "R": np.zeros(shape, dtype=bool),
        "Gr": np.zeros(shape, dtype=bool),
        "Gb": np.zeros(shape, dtype=bool),
        "B": np.zeros(shape, dtype=bool),
    }
    tile = _PATTERN_TILES[pattern]
    for row in range(2):
        for col in range(2):
            masks[tile[row][col]][row::2, col::2] = True
    masks["G"] = masks["Gr"] | masks["Gb"]
    return masks


def channel_image(values: np.ndarray, pattern: str = "RGGB") -> np.ndarray:
    """Map four Bayer-tile values into a full-resolution Bayer array."""
    if len(values) != 4:
        raise ValueError("values must contain four entries")
    values = np.asarray(values)
    out = np.zeros(values.shape[-2:] if values.ndim > 1 else (2, 2), dtype=np.float32)
    out[0::2, 0::2] = values[0]
    out[0::2, 1::2] = values[1]
    out[1::2, 0::2] = values[2]
    out[1::2, 1::2] = values[3]
    return out
