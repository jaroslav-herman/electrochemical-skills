# Electrochemical Skills

Private, version-controlled team skills for electrochemical data analysis.

## Included plugin

- `electrochemical-analysis`: reusable workflows for EC-Lab IV/SV curve comparisons and performance evolution.

The Codex marketplace catalog is at `.agents/plugins/marketplace.json`. The Claude Code catalog is at `.claude-plugin/marketplace.json`. The grouped plugin includes both `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` manifests.

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

## Team installation

Requirements: Windows, Git, `uv`, Python 3.14 or newer, and access to the shared
`\\ELECTROLYZER` measurement location. GitHub access to both
`jaroslav-herman/electrochemical-skills` and `jaroslav-herman/wepy` is required.

Run the installer from PowerShell:

```powershell
irm https://raw.githubusercontent.com/jaroslav-herman/electrochemical-skills/main/install.ps1 | iex
```

The installer creates a local workflow project, installs the pinned `wepy` release,
and registers the skill marketplace for Claude Code and Codex. After an approved
update, run the updater from the local skills checkout:

```powershell
.\update.ps1
```

The installer and updater are deliberately version-pinned. They do not add raw
measurement data to GitHub. A full Claude Code/Codex restart is required after a
plugin update.

Manual fallback commands, after cloning this repository, are:

```powershell
claude plugin marketplace add .
claude plugin install electrochemical-analysis@electrochemical-skills --scope user
codex plugin marketplace add .
codex plugin add electrochemical-analysis@electrochemical-skills
```

Private GitHub repositories require the colleague to have repository access and
working Git credentials. Use `gh auth login` or the organization's approved Git
credential helper before running the installer.

## Version compatibility

| Skills store | `wepy` |
| --- | --- |
| 0.2.3 | 0.1.3 |

The `0.2.3` skills-store version is the first release using the bootstrap workflow
described here.
