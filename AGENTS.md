# Shared Electrochemical Workflow Rules

- Prefer `.mpr` files for electrochemical measurements. Use other formats only when explicitly requested or when no suitable `.mpr` files exist.
- Before selecting samples or labels, inspect the live shared Google Sheet: https://docs.google.com/spreadsheets/d/1ycoCdaol3zYWx8PDTvrI30eZV0nuC7ooFpEvz9qOlds/edit
- Use its `Type` column for folder selection: `AEM` samples are under the
  year's `AEM-WE` subfolder; other known types are under the year folder; if
  `Type` is blank, search both locations.
- Use `wepy` for measurement loading and analysis. Use `we.load_folders`, `we.load_files`, and `we.read_file_safe` for batch workflows.
- Use `wepy.iv_curve.IV_curves_data` for IV/SV extraction and the default `we.get_colors()` scale for comparisons.
- Empty, header-only, unreadable, and zero-byte files must be skipped safely with a warning.
- For plot labels, use the Google Sheet `Sample Name`; if it is blank or unavailable, use only the sample number.
- Run every generated graph script and inspect the resulting graph files before reporting completion.
- Keep research data on the shared measurement location. Never commit raw measurements, secrets, API keys, credentials, or personal notebooks.
