# Electrochemical Skills

Private, version-controlled team skills for electrochemical data analysis.

## Included plugin

- `electrochemical-analysis`: reusable workflows for EC-Lab IV/SV curve comparisons and performance evolution.

The Codex marketplace catalog is at `.agents/plugins/marketplace.json`. The Claude Code catalog is at `.claude-plugin/marketplace.json`.

## House rules

- Edit skills in this repository and push the changes. Never edit installed copies.
- To add a skill, drop its folder under the plugin's `skills/` directory, add its path to the Claude catalog, and bump the version in the Codex `plugin.json`.
- A full restart is required after any plugin update.
- Never commit secrets, API keys, credentials, or private measurement data unless explicitly approved.
- Keep each skill's `SKILL.md` frontmatter `name` identical to its containing folder name and include a useful `description`.

## Development

Validate the Codex plugin before committing:

```powershell
python C:\Users\Herman\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py plugins\electrochemical-analysis
```

The repository is intended to be private when published to GitHub. Team members should install from the private repository and update from the repository rather than modifying local installed copies.
