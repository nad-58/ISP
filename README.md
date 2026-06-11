# ISP: Image Signal Processor

Educational Python implementation of an Image Signal Processor (ISP) pipeline.

This repository explains how raw Bayer sensor data can be transformed into display-ready RGB images using a simplified, public-safe ISP pipeline. It demonstrates the major processing stages used in camera systems without exposing proprietary vendor code, confidential documentation, company-specific implementation details, or private MATLAB source code.

## Implemented pipeline

The current Python pipeline includes:

1. Raw Bayer input handling
2. Black-level correction
3. Defect-pixel correction
4. Green-channel equalisation
5. White balance and digital gain
6. Lens shading correction
7. Optional percentile autogain
8. Bayer demosaicing
9. 3x3 colour correction
10. Reinhard tone mapping
11. Detail enhancement
12. Gamma correction
13. 8-bit RGB output conversion

The modules are intentionally simplified and educational. They are not intended to reproduce a proprietary ISP implementation.

## Repository structure

```text
ISP/
├── src/isp/                    # Reusable ISP stages and pipeline
├── examples/
│   ├── run_pipeline.py         # Synthetic image-to-RGB demonstration
│   └── numerical_walkthrough.py # Small inspectable Bayer-matrix example
├── tests/
│   ├── test_pipeline.py        # End-to-end pipeline smoke test
│   └── test_isp_stages.py      # Stage validation and boundary tests
├── .github/workflows/
│   └── python-checks.yml       # Compile, test, examples, and pip-audit
├── pyproject.toml              # Package and development metadata
└── requirements.txt
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Run the examples

Run the full synthetic-image pipeline:

```bash
MPLBACKEND=Agg python examples/run_pipeline.py
```

The generated image is saved to:

```text
outputs/synthetic_isp_output.png
```

Run the numerical walkthrough:

```bash
python examples/numerical_walkthrough.py
```

The walkthrough prints:

- the input 4x4 Bayer matrix;
- black-level corrected values;
- the demosaiced RGB shape;
- the tone-mapped range;
- the final 8-bit RGB matrix.

## Run validation locally

```bash
python -m compileall -q src examples tests
python -m pytest tests -q
pip-audit
```

Automated GitHub Actions performs the same compile, test, example, and dependency-audit checks on every push and pull request.

## Test coverage

The current tests check:

- end-to-end RGB output shape and `uint8` type;
- safe float conversion during black-level subtraction;
- clipping of negative corrected values;
- rejection of invalid Bayer patterns;
- demosaicing output shape and finite values;
- finite tone-mapping and gamma results;
- final 8-bit output range.

## Public-safe scope

This repository contains only generic educational material. Do not commit:

- unreviewed MATLAB source code;
- proprietary documentation;
- company or customer identifiers;
- internal project names;
- confidential comments, paths, or register maps;
- private calibration data or sensor tuning files.

Any external or legacy logic should first be converted into clean Python, reviewed, and stripped of confidential identifiers before being added.

## Roadmap

- Add RGB-to-YUV and output-format examples
- Add image-quality metrics and stage-by-stage visual comparisons
- Add configurable YAML pipeline examples
- Expand tests for defect correction, lens shading, autogain, sharpening, and colour correction
- Add benchmark timing for larger synthetic frames

## License

MIT License. See `LICENSE`.
