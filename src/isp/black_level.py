"""Black-level correction for Bayer images."""

from __future__ import annotations

import numpy as np


def correct_black_level(
    bayer: np.ndarray,
    offsets: tuple[float, float, float, float] = (64.0, 64.0, 64.0, 64.0),
    pattern: str = "RGGB",
    clip_min: float = 0.0,
) -> np.ndarray:
    """Subtract per-channel black-level offsets from a Bayer image.

    The offsets are ordered according to the 2x2 Bayer tile positions:
    top-left, top-right, bottom-left, bottom-right.
    For an RGGB pattern this corresponds to R, Gr, Gb, B.
    """
    if bayer.ndim != 2:
        raise ValueError("bayer must be a 2D array")
    if len(offsets) != 4:
        raise ValueError("offsets must contain four values")

    output = bayer.astype(np.float32, copy=True)
    output[0::2, 0::2] -= offsets[0]
    output[0::2, 1::2] -= offsets[1]
    output[1::2, 0::2] -= offsets[2]
    output[1::2, 1::2] -= offsets[3]
    return np.maximum(output, clip_min)
