"""Small numerical walkthrough of the educational ISP pipeline."""
from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from isp.black_level import correct_black_level  # noqa: E402
from isp.demosaic import demosaic_bilinear  # noqa: E402
from isp.gamma import apply_gamma, to_uint8  # noqa: E402
from isp.tone_mapping import reinhard_tone_map  # noqa: E402


def main() -> None:
    bayer = np.array(
        [
            [100, 140, 180, 220],
            [120, 160, 200, 240],
            [140, 180, 220, 260],
            [160, 200, 240, 280],
        ],
        dtype=np.uint16,
    )
    corrected = correct_black_level(bayer, offsets=(64, 64, 64, 64), pattern="RGGB")
    rgb = demosaic_bilinear(corrected, pattern="RGGB")
    mapped = reinhard_tone_map(rgb)
    encoded = apply_gamma(mapped, gamma=2.2, max_value=1.0)
    output = to_uint8(encoded, max_value=1.0)

    print("Input Bayer matrix:\n", bayer)
    print("\nAfter black-level correction:\n", corrected)
    print("\nDemosaiced RGB shape:", rgb.shape)
    print("Tone-mapped range:", float(mapped.min()), "to", float(mapped.max()))
    print("8-bit output:\n", output)


if __name__ == "__main__":
    main()
