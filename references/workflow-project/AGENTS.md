# Shared Electrochemical Workflow Rules

- Prefer `.mpr` files for electrochemical measurements.
- Always inspect the live shared Google Sheet before selecting samples or labels:
  https://docs.google.com/spreadsheets/d/1ycoCdaol3zYWx8PDTvrI30eZV0nuC7ooFpEvz9qOlds/edit
- Use `wepy` for loading and analyzing measurements.
- Use `we.load_folders`, `we.load_files`, and `we.read_file_safe` for batch workflows.
- Select sample folders using the sample `Type` from the live sheet: `AEM` samples
  are under `AEM-WE`; known non-AEM samples are under the year folder; if `Type`
  is blank, search both locations.
- Use `wepy.iv_curve.IV_curves_data` for IV/SV extraction.
- Use the default `we.get_colors()` scale; do not override its colormap unless requested.
- Skip empty, header-only, unreadable, and zero-byte files safely with a warning.
- Use the Google Sheet `Sample Name` in labels; if blank or unavailable, use only the sample number.
- Run generated graph scripts and inspect their output before reporting completion.
- Keep raw data on the shared measurement location. Never commit raw measurements, secrets, API keys, credentials, or personal notebooks.
