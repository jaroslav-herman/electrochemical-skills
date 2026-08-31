$ErrorActionPreference = 'Stop'

$LocalRoot = Join-Path $env:LOCALAPPDATA 'electrochemical-workflow'
$SkillsRoot = Join-Path $LocalRoot 'electrochemical-skills'
$WorkflowRoot = Join-Path $LocalRoot 'workflow-project'

if (-not (Test-Path (Join-Path $SkillsRoot '.git'))) {
    throw "Skills checkout not found at $SkillsRoot. Run install.ps1 first."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required.' }
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'uv is required.' }

git -C $SkillsRoot fetch --tags origin
git -C $SkillsRoot checkout main
git -C $SkillsRoot pull --ff-only origin main

Push-Location $WorkflowRoot
try {
    uv lock --upgrade-package eisyfit-wepy
    uv sync --python 3.14
    uv run python -c "import wepy; print('wepy ' + wepy.__version__)"
} finally {
    Pop-Location
}

if (Get-Command claude -ErrorAction SilentlyContinue) {
    & claude plugin marketplace update electrochemical-skills
    & claude plugin install 'electrochemical-analysis@electrochemical-skills' --scope user
}
if (Get-Command codex -ErrorAction SilentlyContinue) {
    & codex plugin marketplace add $SkillsRoot 2>$null
    & codex plugin add 'electrochemical-analysis@electrochemical-skills'
}

Write-Host 'Updated the pinned workflow dependencies and plugins.'
Write-Host 'Run the validation checks before using the workflow, then restart Claude Code/Codex.'
