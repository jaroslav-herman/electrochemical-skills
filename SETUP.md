# Team setup requirements

## Accounts and software

Each colleague needs:

- GitHub access to `jaroslav-herman/electrochemical-skills`.
- GitHub access to `jaroslav-herman/wepy`.
- Windows 10 or newer.
- Git.
- `uv`.
- Python 3.14 or newer.
- Claude Code and/or Codex, depending on which agent they use.

Authenticate Git before installing private repositories:

```powershell
gh auth login
```

If the organization uses another approved credential helper, configure that
instead. Do not put tokens in scripts, `pyproject.toml`, or committed files.

## Measurement data

The workflow reads EC-Lab files from the shared network location, normally under
`\\ELECTROLYZER\PEM-WE_measurements\2026`. GitHub stores only code, instructions,
and sanitized examples; it never stores `.mpr` files or generated research data.

The colleague must be connected to the laboratory network and have read access
to the relevant measurement folders. The live sample metadata is read from the
shared Google Sheet documented in the skill.

## Version policy

The initial installer checks out the skills-store release tag and installs the
`wepy` tag declared by the workflow template. The explicit updater moves the
skills checkout to the maintainer-approved `main` branch and refreshes the
locked Python environment. Changes should be tested and committed before being
made available on `main`.
