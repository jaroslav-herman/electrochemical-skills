---
name: electrochemical-iv-comparison
description: Generate and verify reproducible comparisons of EC-Lab IV/SV curves across electrochemical samples.
---

# Electrochemical IV Comparison

Use this skill for requests to compare polarization/IV/SV curves or performance evolution across samples, days, procedures, cycles, or selected cell voltages.

## Workflow

1. Identify the data root, sample IDs, day, procedure, technique, and requested curve/cycle. If the user does not specify cell voltages for performance evolution, use the established defaults `1.6`, `1.8`, and `2.0 V`.
2. Prefer `.mpr` files. Discover sample folders with `wepy.basics.load_folders()` and measurement files with `wepy.basics.load_files(..., extension=".mpr", natural_sort=True)`.
3. Read files with `wepy.basics.read_file_safe()`. Empty, header-only, unreadable, or zero-byte exports must be skipped with a warning; do not abort a multi-sample comparison because of one invalid file.
4. Use `wepy.iv_curve.IV_curves_data(data)` for SV/IV extraction. It returns `(voltages, currents)` lists. Select the requested curve by its position or explicit cycle number; do not unpack it as a list of `(voltage, current)` pairs.
5. For performance at a target cell voltage, use the current value nearest that voltage on each extracted IV curve. Treat natural file order and curve order as the measurement sequence unless reliable timestamps are explicitly requested.
6. Use the default color scale exactly as `we.get_colors(number_of_samples)`. Do not override `colormap` unless the user asks for a different palette.
7. Label samples with names from the shared Google Sheet sample table. If the matching `Sample Name` is blank or unavailable, use only the sample number. For reproducible local scripts, record the retrieved names in a clearly marked mapping and state that they came from the shared table.
8. Generate a standalone Python script in the research workspace, save outputs under `results/`, execute the script, and visually inspect the generated PNG(s). A graph request is not complete until the output files exist and the script has run successfully.

## Selection rules

- For a request such as "the second IV on Day 5", select cycle/curve 2 from the Day 5 SV `.mpr` file, normally using the second item returned by `IV_curves_data()` when the cycles are ordered 1, 2, 3.
- If multiple candidate files exist, inspect filenames and data availability. Prefer the first valid naturally sorted file for a single requested curve; skip empty candidates with `read_file_safe()`.
- If a requested sample folder or curve is missing, report it clearly and continue only when the requested comparison remains scientifically interpretable.
- Keep the x-axis label as "Measurement sequence" when no trustworthy elapsed-time field is being used.

## Plot output

- For a direct SV/IV comparison, create one graph containing one selected curve per sample.
- For performance evolution at multiple voltages, create one separate graph per voltage, with all requested samples compared on each graph.
- Use publication-style axis labels, legends containing sample number and nonblank sample name, tight layout, and 300 dpi PNG output.

## Self-Improvement

At the end of every run, before ending:

1. Did any step fail or need a workaround?
2. Did the user correct or reject anything meaningful?
3. Did you discover something a future run might need?
   Only propose a change if it meaningfully improves the skill.
