"""Run the educational ISP pipeline on a synthetic Bayer image."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from isp import ISPPipeline, ISPConfig  # noqa: E402


def make_synthetic_bayer(height: int = 256, width: int = 384) -> np.ndarray:
    """Create a simple synthetic RGGB Bayer image."""
    y = np.linspace(0, 1, height, dtype=np.float32)[:, None]
    x = np.linspace(0, 1, width, dtype=np.float32)[None, :]
    base = 1024 + 48000 * (0.65 * x + 0.35 * y)

    bayer = np.zeros((height, width), dtype=np.float32)
    bayer[0::2, 0::2] = base[0::2, 0::2] * 1.15  # R
    bayer[0::2, 1::2] = base[0::2, 1::2] * 1.00  # Gr
    bayer[1::2, 0::2] = base[1::2, 0::2] * 0.98  # Gb
    bayer[1::2, 1::2] = base[1::2, 1::2] * 0.80  # B
    return np.clip(bayer, 0, 65535).astype(np.uint16)


def main() -> None:
    bayer = make_synthetic_bayer()
    pipeline = ISPPipeline(ISPConfig())
    rgb = pipeline.run(bayer)

    output_dir = ROOT / "outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "synthetic_isp_output.png"
    plt.imsave(output_path, rgb)
    print(f"Saved {output_path}")


if __name__ == "__main__":
    main()
