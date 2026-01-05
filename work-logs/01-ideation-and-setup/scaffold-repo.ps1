<#
.SYNOPSIS
    Scaffolds the firewall-defense-agentic-gaming repository structure.

.DESCRIPTION
    Creates the directory structure for the Grid Defense RL project.
    Idempotent - safe to run multiple times.

.NOTES
    Author: VintageDon
    Created: 2026-01-04
    Project: firewall-defense-agentic-gaming
    Repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
#>

param(
    [string]$RepoRoot = (Get-Location).Path
)

# Ensure we're in the right place
if (-not (Test-Path (Join-Path $RepoRoot "README.md"))) {
    Write-Error "Run this script from the repository root or specify -RepoRoot"
    exit 1
}

Write-Host "Scaffolding repository structure..." -ForegroundColor Cyan

# Define directory structure
$directories = @(
    # Source code
    "src",
    "src/core",
    "src/env",
    "src/tests",
    
    # Development support
    "notebooks",
    "configs",
    "scripts",
    
    # Output (gitignored)
    "renders",
    
    # Existing directories (ensure they exist)
    "docs",
    "docs/documentation-standards",
    "assets",
    "scratch",
    "staging",
    "shared",
    "work-logs",
    "work-logs/01-ideation-and-setup",
    "work-logs/02-github-project-frameout",
    ".ai-sandbox",
    ".internal-files",
    ".kilocode",
    ".kilocode/rules",
    ".kilocode/rules/memory-bank",
    ".kilocode/workflows",
    ".vscode"
)

# Create directories
foreach ($dir in $directories) {
    $path = Join-Path $RepoRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  Exists:  $dir" -ForegroundColor DarkGray
    }
}

# Create .gitkeep files for empty directories that should be tracked
$gitkeepDirs = @(
    "src/core",
    "src/env",
    "src/tests",
    "notebooks",
    "configs",
    "scripts",
    "staging",
    ".ai-sandbox"
)

foreach ($dir in $gitkeepDirs) {
    $gitkeep = Join-Path $RepoRoot $dir ".gitkeep"
    if (-not (Test-Path $gitkeep)) {
        New-Item -ItemType File -Path $gitkeep -Force | Out-Null
        Write-Host "  Created: $dir/.gitkeep" -ForegroundColor Green
    }
}

# Add renders to .gitignore if not already there
$gitignore = Join-Path $RepoRoot ".gitignore"
$rendersPattern = "renders/"

if (Test-Path $gitignore) {
    $content = Get-Content $gitignore -Raw
    if ($content -notmatch [regex]::Escape($rendersPattern)) {
        Add-Content $gitignore "`n# Rendered output (video frames, etc.)`n$rendersPattern"
        Write-Host "  Added renders/ to .gitignore" -ForegroundColor Green
    }
} else {
    # Create .gitignore from example if it exists
    $example = Join-Path $RepoRoot ".gitignore.example"
    if (Test-Path $example) {
        Copy-Item $example $gitignore
        Add-Content $gitignore "`n# Rendered output (video frames, etc.)`n$rendersPattern"
        Write-Host "  Created .gitignore from example" -ForegroundColor Green
    }
}

Write-Host "`nRepository structure scaffolded successfully." -ForegroundColor Cyan
Write-Host "Next: Run interior README generation." -ForegroundColor Yellow
