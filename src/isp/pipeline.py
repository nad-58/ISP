"""Educational ISP pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .autogain import percentile_autogain
from .black_level import correct_black_level
from .color_correction import apply_color_matrix
from .defect_pixel import correct_defect_pixels
from .demosaic import demosaic_bilinear
from .gamma import apply_gamma, to_uint8
from .green_equalization import equalize_green_channels
from .lens_shading import apply_mesh_lens_shading
from .sharpening import enhance_detail
from .tone_mapping import reinhard_tone_map
from .white_balance import apply_rgb_gains, gray_world_gains


@dataclass
class ISPConfig:
    """Configuration for the simplified ISP pipeline."""

    bayer_pattern: str = "RGGB"
    black_offsets: tuple[float, float, float, float] = (64.0, 64.0, 64.0, 64.0)
    white_balance_gains: tuple[float, float, float] | None = None
    color_matrix: np.ndarray = field(default_factory=lambda: np.eye(3, dtype=np.float32))
    gamma: float = 2.2
    max_value: float = 65535.0
    enable_defect_correction: bool = True
    enable_green_equalization: bool = False
    enable_autogain: bool = False
    enable_sharpening: bool = True
    lens_shading_mesh: np.ndarray | None = None


class ISPPipeline:
    """Small educational ISP pipeline for raw Bayer images."""

    def __init__(self, config: ISPConfig | None = None) -> None:
        self.config = config or ISPConfig()

    def run(self, bayer: np.ndarray) -> np.ndarray:
        """Process a Bayer image and return an 8-bit RGB image."""
        cfg = self.config
        raw = correct_black_level(
            bayer,
            offsets=cfg.black_offsets,
            pattern=cfg.bayer_pattern,
        )

        if cfg.enable_defect_correction:
            raw = correct_defect_pixels(raw)

        if cfg.enable_green_equalization:
            raw = equalize_green_channels(raw, pattern=cfg.bayer_pattern)

        if cfg.lens_shading_mesh is not None:
            raw = apply_mesh_lens_shading(raw, cfg.lens_shading_mesh, pattern=cfg.bayer_pattern)

        if cfg.enable_autogain:
            raw, _ = percentile_autogain(raw, target=cfg.max_value, max_gain=4.0)

        rgb = demosaic_bilinear(raw, pattern=cfg.bayer_pattern)
        gains = cfg.white_balance_gains or gray_world_gains(rgb)
        rgb = apply_rgb_gains(rgb, gains)
        rgb = apply_color_matrix(rgb, cfg.color_matrix)
        rgb = reinhard_tone_map(rgb)

        if cfg.enable_sharpening:
            rgb = enhance_detail(rgb, strength=0.25)

        rgb = apply_gamma(rgb, gamma=cfg.gamma, max_value=cfg.max_value)
        return to_uint8(rgb, max_value=cfg.max_value)
