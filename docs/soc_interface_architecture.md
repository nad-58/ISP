# SoC Interface Architecture

This note summarises the system-level view of an educational Image Signal Processor (ISP) integrated into a camera System-on-Chip.

The purpose is to explain the main hardware and firmware interfaces around an ISP pipeline. It is not a vendor-specific hardware specification and does not contain confidential register-map details.

## System view

A typical ISP subsystem contains three cooperating parts:

- **Pixel-processing core**: a high-throughput hardware pipeline that performs pixel-rate operations such as noise reduction, lens shading correction, colour correction, tone mapping, gamma correction, and output formatting.
- **Firmware and control API**: a software control layer responsible for exposure, white balance, focus control, mode switching, and safe pipeline configuration.
- **Calibration and tuning data**: offline-generated parameters such as colour matrices, lens shading maps, gamma curves, and noise profiles.

The central design idea is to keep high-bandwidth image processing inside the pixel pipeline while using firmware for slower control-loop decisions.

## Control interface

The ISP is normally configured through a low-bandwidth control interface. In many SoC designs, this is a memory-mapped register space reached through a peripheral bus.

Typical control operations include:

- enabling or disabling modules
- selecting sensor input timing mode
- configuring image width and height
- loading lookup tables
- updating crop or output-window settings
- reading status flags and statistics-ready indicators

For stable operation, multi-register changes should be applied at a frame-safe boundary. A common approach is:

1. request pipeline stop
2. wait until the hardware reports idle or frame-safe status
3. update sensor configuration
4. update ISP configuration
5. request pipeline start
6. wait until the hardware reports active status

## High-bandwidth memory interface

Some ISP blocks require external frame memory. Examples include temporal noise reduction, wide-dynamic-range frame combination, digital image stabilization, and output frame buffering.

A high-bandwidth memory interface is used for:

- reading previous frames
- writing current processed frames
- maintaining circular output buffers
- supporting video encoder or display handoff

Memory bandwidth depends on image resolution, frame rate, bit depth, number of buffers, and whether intermediate processing uses increased internal precision.

## Lookup tables and local memory

ISP modules often use small local memories or lookup tables to avoid expensive per-pixel computation. Typical examples include:

- gamma curves
- tone-mapping curves
- lens shading meshes
- sharpening response curves
- noise profile tables
- defect-pixel maps

In this educational Python repository, these concepts are represented using NumPy arrays rather than hardware SRAM.

## Statistics for 3A algorithms

An ISP commonly generates statistics for firmware control loops:

- **AE**: exposure-related luminance histograms
- **AWB**: colour-ratio statistics for white balance
- **AF**: sharpness or contrast metrics for focus control

These statistics are usually calculated over image zones so that firmware can weight the centre, ignore saturated areas, or select a region of interest.

## Interrupts and events

Hardware events notify the host or microcontroller when a relevant boundary has been reached. Examples include:

- frame start
- frame end
- statistics ready
- output buffer complete
- error or overflow status

In this Python implementation, these hardware events are not modelled directly. They are documented to explain how a real-time ISP subsystem interacts with firmware and the wider SoC.
