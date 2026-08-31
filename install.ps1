$ErrorActionPreference = 'Stop'

$SkillsRepository = 'https://github.com/jaroslav-herman/electrochemical-skills.git'
$WepyRepository = 'https://github.com/jaroslav-herman/wepy.git'
$SkillsVersion = '0.2.0'
$SkillsTag = 'v0.2.0'
$WepyVersion = 'v0.1.3'
$LocalRoot = Join-Path $env:LOCALAPPDATA 'electrochemical-workflow'
$SkillsRoot = Join-Path $LocalRoot 'electrochemical-skills'
$WorkflowRoot = Join-Path $LocalRoot 'workflow-project'

function Require-Command([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command '$Name' was not found. Install it and rerun this script."
    }
}

Require-Command 'git'
Require-Command 'uv'
Require-Command 'python'

$pythonVersion = & python --version 2>&1
if ($pythonVersion -notmatch 'Python 3\.1[4-9]') {
    throw "Python 3.14 or newer is required; detected: $pythonVersion"
}

if (Test-Path (Join-Path $SkillsRoot '.git')) {
    git -C $SkillsRoot fetch --tags origin
    git -C $SkillsRoot checkout $SkillsTag
} else {
    New-Item -ItemType Directory -Force -Path (Split-Path $SkillsRoot) | Out-Null
    git clone --branch $SkillsTag $SkillsRepository $SkillsRoot
}

if (-not (Test-Path (Join-Path $WorkflowRoot 'pyproject.toml'))) {
    New-Item -ItemType Directory -Force -Path $WorkflowRoot | Out-Null
    Copy-Item (Join-Path $SkillsRoot 'references\workflow-project\pyproject.toml') (Join-Path $WorkflowRoot 'pyproject.toml')
    Copy-Item (Join-Path $SkillsRoot 'references\workflow-project\README.md') (Join-Path $WorkflowRoot 'README.md')
    Copy-Item (Join-Path $SkillsRoot 'references\workflow-project\AGENTS.md') (Join-Path $WorkflowRoot 'AGENTS.md')
}

Push-Location $WorkflowRoot
try {
    uv sync --python 3.14
    uv run python -c "import wepy; print('wepy ' + wepy.__version__)"
} finally {
    Pop-Location
}

if (Get-Command claude -ErrorAction SilentlyContinue) {
    $marketplaces = (& claude plugin marketplace list --json 2>$null | Out-String)
    if ($marketplaces -notmatch 'electrochemical-skills') {
        & claude plugin marketplace add $SkillsRoot
    } else {
        & claude plugin marketplace update electrochemical-skills
    }
    & claude plugin install 'electrochemical-analysis@electrochemical-skills' --scope user
} else {
    Write-Warning 'Claude Code CLI was not found; add and install the marketplace later with claude plugin marketplace add and claude plugin install.'
}

if (Get-Command codex -ErrorAction SilentlyContinue) {
    & codex plugin marketplace add $SkillsRoot 2>$null
    & codex plugin add 'electrochemical-analysis@electrochemical-skills'
} else {
    Write-Warning 'Codex CLI was not found; install/register the marketplace later from the cloned skills checkout.'
}

Write-Host "Installed electrochemical workflow $SkillsVersion with wepy $WepyVersion in $WorkflowRoot"
Write-Host 'Restart Claude Code/Codex before using updated skills.'
