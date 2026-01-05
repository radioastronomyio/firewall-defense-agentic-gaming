# PowerShell Script Header Template

> Template Version: 1.0  
> Applies To: All `.ps1` files  
> Repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming  
> Last Updated: 2026-01-04

---

## Template

```powershell
<#
.SYNOPSIS
    [One-line description of what the script does]

.DESCRIPTION
    [2-4 sentences explaining the script's purpose, what it operates on,
    and what outputs it produces. Include any important behavioral notes.]

.NOTES
    Repository  : firewall-defense-agentic-gaming
    Author      : VintageDon (https://github.com/vintagedon)
    Created     : YYYY-MM-DD

.EXAMPLE
    .\script-name.ps1

    [Description of what this invocation does]

.EXAMPLE
    .\script-name.ps1 -Parameter Value

    [Description of what this invocation does]

.LINK
    https://github.com/radioastronomyio/firewall-defense-agentic-gaming
#>

# =============================================================================
# Configuration
# =============================================================================

$RepoRoot = Split-Path -Parent $PSScriptRoot

# =============================================================================
# Functions
# =============================================================================

# [Function definitions if needed]

# =============================================================================
# Execution
# =============================================================================

# [Main script logic]
```

---

## Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| `.SYNOPSIS` | Yes | Single line, verb-led description |
| `.DESCRIPTION` | Yes | Expanded explanation of purpose and behavior |
| `.NOTES` | Yes | Repository: `firewall-defense-agentic-gaming`, Author, Created |
| `.EXAMPLE` | Yes | At least one usage example with description |
| `.LINK` | Yes | `https://github.com/radioastronomyio/firewall-defense-agentic-gaming` |
| `.PARAMETER` | If applicable | Document any script parameters |

---

## Section Comments

Use banner comments to separate logical sections:

```powershell
# =============================================================================
# Section Name
# =============================================================================
```

Standard sections (in order):

1. **Configuration** — Variables, paths, settings
2. **Functions** — Helper function definitions (if any)
3. **Execution** — Main script logic

---

## Example: Repository Scaffolding Script

```powershell
<#
.SYNOPSIS
    Scaffolds the firewall-defense-agentic-gaming repository structure.

.DESCRIPTION
    Creates the directory structure for the Grid Defense RL project.
    Idempotent - safe to run multiple times.

.NOTES
    Repository  : firewall-defense-agentic-gaming
    Author      : VintageDon (https://github.com/vintagedon)
    Created     : 2026-01-04

.EXAMPLE
    .\scaffold-repo.ps1

    Creates all project directories in the repository root.

.EXAMPLE
    .\scaffold-repo.ps1 -RepoRoot "D:\projects\grid-defense"

    Creates directories in the specified location.

.LINK
    https://github.com/radioastronomyio/firewall-defense-agentic-gaming
#>

param(
    [string]$RepoRoot = (Get-Location).Path
)

# =============================================================================
# Configuration
# =============================================================================

$Directories = @(
    "src/core",
    "src/env",
    "src/tests"
)

# =============================================================================
# Execution
# =============================================================================

foreach ($dir in $Directories) {
    $path = Join-Path $RepoRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created: $dir" -ForegroundColor Green
    }
}
```

---

## Notes

- PowerShell comment-based help enables `Get-Help script-name.ps1`
- Keep `.SYNOPSIS` under 80 characters
- Use present tense, active voice ("Scaffolds..." not "This script scaffolds...")
- Include `-WhatIf` support for destructive operations when practical
