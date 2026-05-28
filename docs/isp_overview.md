# ISP Overview

An Image Signal Processor (ISP) converts raw image sensor measurements into images that can be displayed, stored, streamed, or passed to downstream computer vision algorithms.

Most camera sensors measure light through a colour filter array, commonly a Bayer pattern. The raw sensor image is not directly suitable for viewing because each pixel contains only one colour component and also includes sensor offsets, noise, optical non-uniformity, colour response differences, and limited dynamic range.

A simplified ISP pipeline usually includes:

1. **Input handling**: read raw Bayer data and identify the Bayer pattern.
2. **Black-level correction**: subtract the sensor baseline offset.
3. **Defect-pixel correction**: replace hot or dead pixels using neighbouring values.
4. **Noise reduction**: reduce spatial and temporal noise while preserving edges.
5. **White balance**: correct colour cast caused by illumination.
6. **Lens shading correction**: compensate for vignetting and colour shading.
7. **Tone mapping**: compress high dynamic range into display range.
8. **Demosaicing**: convert Bayer samples into full RGB pixels.
9. **Colour correction**: transform camera RGB into a target colour space.
10. **Gamma correction**: encode image values for display.
11. **Sharpening**: improve perceived edge detail.
12. **Output conversion**: convert RGB to output formats such as YUV.

This repository implements a clean educational subset of these stages in Python.

## Important note

The implementation is intentionally generic. It does not reproduce any proprietary hardware pipeline, confidential register map, calibration tool, or vendor-specific algorithm.
