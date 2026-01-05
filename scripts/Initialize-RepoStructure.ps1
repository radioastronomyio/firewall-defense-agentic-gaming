<#
.SYNOPSIS
    Scaffolds the firewall-defense-agentic-gaming repository structure.

.DESCRIPTION
    Creates all directories and placeholder READMEs for the Grid Defense RL project.
    Idempotent - safe to run multiple times.

.NOTES
    Repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
    Author:     VintageDon
    Created:    2026-01-04
    Version:    1.0
#>

[CmdletBinding()]
param(
    [Parameter()]
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = 'Stop'

# Directory structure definition
$directories = @(
    # Source code
    'src',
    'src/core',
    'src/env',
    'src/viz',
    
    # Tests
    'tests',
    'tests/unit',
    'tests/integration',
    
    # Experimentation
    'notebooks',
    
    # Configuration
    'configs',
    'configs/training',
    'configs/experiments',
    
    # Scripts and entrypoints
    'scripts',
    
    # Outputs (gitignored)
    'renders',
    'checkpoints',
    'logs'
)

# Create directories
foreach ($dir in $directories) {
    $path = Join-Path $RepoRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "Exists:  $dir" -ForegroundColor Yellow
    }
}

# Add to .gitignore if not present
$gitignorePath = Join-Path $RepoRoot '.gitignore'
$gitignoreAdditions = @(
    '',
    '# Training outputs',
    'renders/',
    'checkpoints/',
    'logs/',
    '*.ckpt',
    '*.pt',
    '*.pth',
    '',
    '# Notebook checkpoints',
    '.ipynb_checkpoints/'
)

if (Test-Path $gitignorePath) {
    $existing = Get-Content $gitignorePath -Raw
    if ($existing -notmatch 'checkpoints/') {
        Add-Content -Path $gitignorePath -Value ($gitignoreAdditions -join "`n")
        Write-Host "Updated .gitignore with training outputs" -ForegroundColor Green
    }
}

Write-Host "`nRepository structure initialized." -ForegroundColor Cyan
