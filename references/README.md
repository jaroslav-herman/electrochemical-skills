# Reference workflows

This directory contains sanitized workflow guidance and examples for colleagues.
It intentionally excludes raw measurement data, credentials, private exports, and
personal notebooks.

The canonical workflow is the `electrochemical-iv-comparison` skill. The
`workflow-project/compare_performance_evolution.py` file is a sanitized starter
template; update its sample IDs from the live Google Sheet before running it.
Example scripts should use `.mpr` files, `wepy`, safe file reading, and the
default `we.get_colors()` scale.
