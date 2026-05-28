# ISP: Image Signal Processor

Educational Python implementation of an Image Signal Processor (ISP) pipeline.

This repository explains how raw Bayer sensor data can be transformed into display-ready RGB or YUV images using a simplified ISP pipeline. The goal is educational: to demonstrate the main processing stages used in real camera systems without exposing proprietary vendor code, confidential documentation, company-specific implementation details, or private MATLAB source code.

## Why this project?

An Image Signal Processor is the part of a camera system that converts raw sensor measurements into usable images. A typical ISP performs corrections and transformations such as black-level correction, defect-pixel correction, white balance, lens shading correction, demosaicing, colour correction, tone mapping, gamma correction, sharpening, and RGB/YUV output conversion.

This project provides a clean Python reference implementation to help engineers, students, and researchers understand the core concepts behind ISP pipelines.

## Pipeline overview

The initial educational pipeline is structured around the following stages:

1. Raw Bayer input handling
2. Black-level correction
3. Defect-pixel correction
4. Green-channel equalisation
5. Spatial noise reduction
6. White balance and digital gain
7. Lens shading correction
8. Tone mapping
9. Demosaicing from Bayer to RGB
10. 3x3 colour correction matrix
11. Gamma correction
12. Sharpening
13. RGB to YUV conversion
14. Dithering and output quantisation
15. Cropping and output formatting

The modules are intentionally simplified. They are not intended to reproduce any proprietary ISP vendor implementation.

## Repository status

This repository is being built in stages:

- Stage 1: public educational structure and documentation
- Stage 2: clean Python ISP building blocks
- Stage 3: example pipeline and demo image processing
- Stage 4: tests and validation examples
- Stage 5: optional conversion of separately reviewed MATLAB logic into sanitized Python only

No MATLAB source code or confidential documentation should be committed to this repository.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

## Example usage

```bash
python examples/run_pipeline.py
```

The example uses a synthetic Bayer image so that the repository can run without private datasets.

## Confidentiality policy

This repository must contain only generic educational material. Do not commit:

- MATLAB source code before conversion and sanitization
- proprietary documentation
- company names or customer names
- internal project names
- confidential comments, file paths, or register maps
- private calibration data or sensor tuning files

Any external or legacy code should first be converted into clean Python, reviewed, and stripped of confidential identifiers before being added.

## License

MIT License. See `LICENSE`.
