$ErrorActionPreference = 'Stop'

$LocalRoot = Join-Path $env:LOCALAPPDATA 'electrochemical-workflow'
$SkillsRoot = Join-Path $LocalRoot 'electrochemical-skills'
$WorkflowRoot = Join-Path $LocalRoot 'workflow-project'
$CodexSkillRoot = Join-Path $env:USERPROFILE '.codex\skills\electrochemical-iv-comparison'

if (-not (Test-Path (Join-Path $SkillsRoot '.git'))) {
    throw "Skills checkout not found at $SkillsRoot. Run install.ps1 first."
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required.' }
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { throw 'uv is required.' }

git -C $SkillsRoot fetch --tags origin
git -C $SkillsRoot checkout main
git -C $SkillsRoot pull --ff-only origin main

foreach ($referenceFile in @('AGENTS.md', 'compare_performance_evolution.py', 'verify_install.py', '.env.example')) {
    $destination = Join-Path $WorkflowRoot $referenceFile
    if (-not (Test-Path $destination)) {
        Copy-Item (Join-Path $SkillsRoot ('references\workflow-project\' + $referenceFile)) $destination
    }
}

Push-Location $WorkflowRoot
try {
    uv lock --upgrade-package eisyfit-wepy
    uv sync --python 3.14
    uv run python verify_install.py
} finally {
    Pop-Location
}

if (Get-Command claude -ErrorAction SilentlyContinue) {
    & claude plugin marketplace update electrochemical-skills
    & claude plugin install 'electrochemical-analysis@electrochemical-skills' --scope user
}
if (Get-Command codex -ErrorAction SilentlyContinue) {
    & codex plugin marketplace add $SkillsRoot 2>$null
    & codex plugin marketplace upgrade electrochemical-skills 2>$null
    & codex plugin add 'electrochemical-analysis@electrochemical-skills'
}

New-Item -ItemType Directory -Force -Path (Split-Path $CodexSkillRoot) | Out-Null
if (Test-Path $CodexSkillRoot) { Remove-Item -LiteralPath $CodexSkillRoot -Recurse -Force }
Copy-Item (Join-Path $SkillsRoot 'plugins\electrochemical-analysis\skills\electrochemical-iv-comparison') $CodexSkillRoot -Recurse -Force
Write-Host "Refreshed direct Codex skill fallback at $CodexSkillRoot"

Write-Host 'Updated the pinned workflow dependencies and plugins.'
Write-Host 'Run the validation checks before using the workflow, then restart Claude Code/Codex.'
