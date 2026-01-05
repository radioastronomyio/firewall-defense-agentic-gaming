<#
.SYNOPSIS
    Creates GitHub Project structure with milestones, labels, tasks, and sub-tasks.

.DESCRIPTION
    Populates the GitHub repository with the complete project management structure
    for Grid Defense RL. Creates labels for categorization, milestones for phase
    containers, parent tasks with progress tracking, and linked sub-tasks as
    assignable work units.

    Requires: gh CLI authenticated, gh-sub-issue extension installed.

.NOTES
    Repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
    Author:     VintageDon
    Created:    2026-01-04
    Version:    1.0
    Phase:      M02 - GitHub Project Frameout

.EXAMPLE
    .\Initialize-GitHubProject.ps1

    Creates all labels, milestones, tasks, and sub-tasks in the repository.

.EXAMPLE
    .\Initialize-GitHubProject.ps1 -WhatIf

    Shows what would be created without making changes.

.LINK
    https://github.com/radioastronomyio/firewall-defense-agentic-gaming
#>

[CmdletBinding(SupportsShouldProcess)]
param()

$ErrorActionPreference = 'Stop'

# =============================================================================
# Configuration
# =============================================================================

$Repo = "radioastronomyio/firewall-defense-agentic-gaming"

# Labels: name, color (hex without #), description
$Labels = @(
    @{ name = "Task"; color = "1d76db"; description = "Parent issue with sub-tasks" }
    @{ name = "Sub-Task"; color = "5319e7"; description = "Assignable work unit" }
    @{ name = "core-engine"; color = "d93f0b"; description = "NumPy simulation core" }
    @{ name = "gymnasium"; color = "0e8a16"; description = "Environment wrapper" }
    @{ name = "training"; color = "fbca04"; description = "PPO/RL training" }
    @{ name = "visualization"; color = "e99695"; description = "Rendering and saliency" }
    @{ name = "documentation"; color = "c5def5"; description = "Docs, READMEs, specs" }
    @{ name = "testing"; color = "bfd4f2"; description = "Unit and integration tests" }
)

# Milestones: title, description, due_on (ISO 8601, can be null for placeholders)
# AI NOTE: due_on must be ISO 8601 format or null. GitHub API rejects invalid dates.
$Milestones = @(
    @{
        title       = "M01: Ideation and Setup"
        description = "Project inception, multi-model research synthesis, repository scaffolding. COMPLETE."
        due_on      = $null
    }
    @{
        title       = "M02: GitHub Project Frameout"
        description = "Project board populated, work units defined and assignable. COMPLETE."
        due_on      = $null
    }
    @{
        title       = "M03: Core Engine Prototype"
        description = "Headless NumPy core: grid arrays, walls, Drop enemy, collision, deterministic step loop."
        due_on      = $null
    }
    @{
        title       = "M04: Gymnasium Integration"
        description = "Environment wrapper, observation space, action masking, random agent validation, >10k SPS."
        due_on      = $null
    }
    @{
        title       = "M05: PPO Training Baseline"
        description = "Placeholder - Train MaskablePPO on Drop, validate performance and determinism."
        due_on      = $null
    }
    @{
        title       = "M06: Visualization Layer"
        description = "Placeholder - Python Arcade observer, replay from seed+log, saliency overlay."
        due_on      = $null
    }
)

# =============================================================================
# Task and Sub-Task Definitions
# =============================================================================

# Structure: Each task has a number, title, milestone, labels, body, and sub-tasks array.
# Sub-tasks have number, title, labels, and body.
#
# AI NOTE: Task numbers follow {Milestone}.{Task} convention (e.g., 3.1).
# Sub-task numbers follow {Milestone}.{Task}.{SubTask} convention (e.g., 3.1.1).
# This enables Kanban readability - at a glance you know the phase and grouping.

$Tasks = @(
    # -------------------------------------------------------------------------
    # M01: Ideation and Setup (backfill - already complete)
    # -------------------------------------------------------------------------
    @{
        number    = "1.1"
        title     = "Task 1.1: Ideation and Setup"
        milestone = "M01: Ideation and Setup"
        labels    = @("Task", "documentation")
        body      = @"
## Objective
Establish project concept through multi-model research, produce consolidated specification, scaffold repository.

## Status
✅ **COMPLETE**

## Deliverables
- [x] GDR Round 1 & 2 research
- [x] GPT-5.2 architecture review
- [x] Spec v2 consolidated
- [x] Design document (public)
- [x] Repository scaffolded
- [x] Memory bank populated
- [x] Infographics generated

## Artifacts
- ``docs/design-document.md`` - Authoritative technical specification
- ``scratch/grid-defense-spec-v2.md`` - Internal working spec
- ``.kilocode/rules/memory-bank/*.md`` - AI context files
"@
        subtasks  = @()  # No sub-tasks for backfilled complete work
    }

    # -------------------------------------------------------------------------
    # M02: GitHub Project Frameout (this work)
    # -------------------------------------------------------------------------
    @{
        number    = "2.1"
        title     = "Task 2.1: GitHub Project Frameout"
        milestone = "M02: GitHub Project Frameout"
        labels    = @("Task", "documentation")
        body      = @"
## Objective
Transform project scope into actionable GitHub Project with milestones, tasks, and sub-tasks.

## Status
✅ **COMPLETE** (upon script execution)

## Deliverables
- [x] Labels created
- [x] Milestones M01-M06 created
- [x] M03 tasks and sub-tasks defined
- [x] M04 tasks defined (sub-tasks deferred)
- [x] M05-M06 placeholders created

## Artifacts
- ``scripts/Initialize-GitHubProject.ps1`` - This setup script
- ``work-logs/02-github-project-frameout/README.md`` - Phase worklog
"@
        subtasks  = @()  # No sub-tasks for procedural overhead
    }

    # -------------------------------------------------------------------------
    # M03: Core Engine Prototype
    # -------------------------------------------------------------------------
    @{
        number    = "3.1"
        title     = "Task 3.1: Grid State Management"
        milestone = "M03: Core Engine Prototype"
        labels    = @("Task", "core-engine")
        body      = @"
## Objective
Implement core grid arrays with correct indexing convention and data types.

## Reference
- Design doc Section 3 (Grid Specification)
- Design doc Section 10 (Data Layout)

## Sub-Tasks
- [ ] 3.1.1: Define constants and array dtypes
- [ ] 3.1.2: Initialize grid arrays
- [ ] 3.1.3: Unit tests for array shapes and indexing
"@
        subtasks  = @(
            @{
                number = "3.1.1"
                title  = "Sub-Task 3.1.1: Define constants and array dtypes"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Create constants module with grid dimensions, cell states, and dtype specifications.

## Deliverables
- ``src/core/constants.py`` with:
  - Grid dimensions: WIDTH=13, HEIGHT=9
  - Cell states: EMPTY=0, WALL=1
  - Position constants: CORE_Y_HALF=16, MAX_ENEMIES=20
  - Dtype specifications matching design doc Section 10.1

## Acceptance Criteria
- All constants match design document exactly
- Docstrings explain each constant's purpose
- No magic numbers in subsequent code
"@
            }
            @{
                number = "3.1.2"
                title  = "Sub-Task 3.1.2: Initialize grid arrays"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement grid state initialization with correct shapes and dtypes.

## Deliverables
- ``src/core/grid.py`` with GridState class or initialization function
- Arrays: grid, wall_hp, wall_armed, wall_pending, cell_cd, gcd
- All arrays use ``[y, x]`` indexing convention (H, W) = (9, 13)

## Acceptance Criteria
- ``grid.shape == (9, 13)``
- All dtypes match design doc Section 10.1
- Reset function returns fresh state
"@
            }
            @{
                number = "3.1.3"
                title  = "Sub-Task 3.1.3: Unit tests for array shapes and indexing"
                labels = @("Sub-Task", "core-engine", "testing")
                body   = @"
## Objective
Verify grid arrays have correct shapes, dtypes, and indexing behavior.

## Deliverables
- ``tests/unit/test_grid.py`` with tests for:
  - Array shapes match (9, 13)
  - Dtypes match specification
  - ``[y, x]`` indexing works correctly (row, column)
  - Reset produces clean state

## Acceptance Criteria
- All tests pass
- Coverage of edge cases (corners, boundaries)
"@
            }
        )
    }
    @{
        number    = "3.2"
        title     = "Task 3.2: Wall Mechanics"
        milestone = "M03: Core Engine Prototype"
        labels    = @("Task", "core-engine")
        body      = @"
## Objective
Implement wall placement, cooldown system, and arming logic.

## Reference
- Design doc Section 5 (Action Model)
- Design doc Section 10.1 (State Arrays)

## Sub-Tasks
- [ ] 3.2.1: Wall placement with validity checks
- [ ] 3.2.2: Cooldown system (GCD + cell cooldowns)
- [ ] 3.2.3: Wall arming (pending → armed transition)
- [ ] 3.2.4: Unit tests for wall lifecycle
"@
        subtasks  = @(
            @{
                number = "3.2.1"
                title  = "Sub-Task 3.2.1: Wall placement with validity checks"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement wall placement logic with validity checking.

## Deliverables
- ``src/core/walls.py`` with placement function
- Validity checks: GCD=0, cell_cd[y,x]=0, grid[y,x]!=WALL
- Returns success/failure boolean

## Acceptance Criteria
- Cannot place wall when GCD > 0
- Cannot place wall on cooldown cell
- Cannot stack walls on existing wall
- Successful placement sets wall_pending[y,x] = True
"@
            }
            @{
                number = "3.2.2"
                title  = "Sub-Task 3.2.2: Cooldown system (GCD + cell cooldowns)"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement global cooldown and per-cell cooldown mechanics.

## Deliverables
- GCD: 10 frames after any action
- Cell CD: ~150 frames after wall placed on cell
- Decrement function called each tick
- Cooldown values from design doc Section 5.1

## Acceptance Criteria
- GCD blocks all actions when > 0
- Cell CD blocks specific cell when > 0
- Both decrement correctly each tick
- Zero is "ready" state
"@
            }
            @{
                number = "3.2.3"
                title  = "Sub-Task 3.2.3: Wall arming (pending → armed transition)"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement 1-tick wall arming delay (anti-triviality rule).

## Deliverables
- Walls placed this tick: wall_pending = True, wall_armed = False
- Next tick: wall_pending → wall_armed transition
- Only armed walls cause collision damage

## Reference
Design doc Section 5.3: "Walls arm 1 tick after placement. Enemy on cell at placement time is not killed."

## Acceptance Criteria
- Freshly placed wall does not kill enemy on same tick
- Wall becomes armed exactly 1 tick later
- Armed walls participate in collision
"@
            }
            @{
                number = "3.2.4"
                title  = "Sub-Task 3.2.4: Unit tests for wall lifecycle"
                labels = @("Sub-Task", "core-engine", "testing")
                body   = @"
## Objective
Test complete wall lifecycle: placement → arming → collision → destruction.

## Deliverables
- ``tests/unit/test_walls.py`` with tests for:
  - Valid/invalid placement scenarios
  - GCD blocking
  - Cell cooldown blocking
  - Arming delay (1 tick)
  - HP tracking

## Acceptance Criteria
- All validity edge cases covered
- Arming timing verified
- Anti-triviality rule tested explicitly
"@
            }
        )
    }
    @{
        number    = "3.3"
        title     = "Task 3.3: Enemy System"
        milestone = "M03: Core Engine Prototype"
        labels    = @("Task", "core-engine")
        body      = @"
## Objective
Implement Drop enemy with fixed-slot arrays and half-cell movement.

## Reference
- Design doc Section 6 (Enemy Specification)
- Design doc Section 4 (Position System)
- Design doc Section 10.2 (Enemy Arrays)

## Sub-Tasks
- [ ] 3.3.1: Fixed-slot enemy arrays
- [ ] 3.3.2: Drop movement (half-cell fixed-point)
- [ ] 3.3.3: Spawn logic
- [ ] 3.3.4: Array compaction
- [ ] 3.3.5: Unit tests for enemy lifecycle
"@
        subtasks  = @(
            @{
                number = "3.3.1"
                title  = "Sub-Task 3.3.1: Fixed-slot enemy arrays"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement 20 fixed enemy slots with zero-padding and spawn-order sorting.

## Deliverables
- ``src/core/enemies.py`` with enemy array structure
- Arrays: enemy_y_half, enemy_x, enemy_alive, enemy_type, enemy_spawn_tick
- All shape (20,) with dtypes from design doc Section 10.2

## Reference
Design doc Section 7.2: "20 enemy slots, zero-padded, sorted by spawn order (oldest first)."

## Acceptance Criteria
- Exactly 20 slots, no dynamic resizing
- Dead slots zero-padded
- Spawn order maintained (oldest first)
"@
            }
            @{
                number = "3.3.2"
                title  = "Sub-Task 3.3.2: Drop movement (half-cell fixed-point)"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement Drop enemy movement using half-cell integer positions.

## Deliverables
- Movement: ``enemy_y_half[alive] += 1`` per tick
- Cell lookup: ``cell_y = enemy_y_half // 2``
- Speed: 0.5 cells/tick = 1 half-cell/tick

## Reference
Design doc Section 4: Fixed-point positions eliminate float boundary bugs.

## Acceptance Criteria
- No float arithmetic anywhere
- Cell lookup is integer division
- Movement is vectorized over alive enemies
"@
            }
            @{
                number = "3.3.3"
                title  = "Sub-Task 3.3.3: Spawn logic"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement enemy spawning at row 0 with configurable timing.

## Deliverables
- Spawn at y_half=0, random column (0-12)
- Configurable spawn interval (default: every 30 ticks)
- Find first dead slot, populate with new enemy
- Track spawn_tick for ordering

## Acceptance Criteria
- Enemies spawn at top row
- Random column distribution
- Respects MAX_ENEMIES limit
- Spawn order tracked correctly
"@
            }
            @{
                number = "3.3.4"
                title  = "Sub-Task 3.3.4: Array compaction"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Compact enemy arrays after deaths to maintain spawn-order sorting.

## Deliverables
- Remove dead enemies from arrays
- Shift alive enemies to maintain contiguous block
- Preserve spawn order (oldest first)
- Zero-pad empty trailing slots

## Acceptance Criteria
- No gaps in alive enemy block
- Spawn order preserved after compaction
- Trailing slots properly zeroed
"@
            }
            @{
                number = "3.3.5"
                title  = "Sub-Task 3.3.5: Unit tests for enemy lifecycle"
                labels = @("Sub-Task", "core-engine", "testing")
                body   = @"
## Objective
Test enemy spawn, movement, and array management.

## Deliverables
- ``tests/unit/test_enemies.py`` with tests for:
  - Spawn at correct position
  - Movement increments correctly
  - Array compaction preserves order
  - MAX_ENEMIES respected
  - Half-cell to cell conversion

## Acceptance Criteria
- Full lifecycle coverage
- Edge cases: full array, rapid spawning, mass death
"@
            }
        )
    }
    @{
        number    = "3.4"
        title     = "Task 3.4: Collision Resolution"
        milestone = "M03: Core Engine Prototype"
        labels    = @("Task", "core-engine")
        body      = @"
## Objective
Implement vectorized collision detection and resolution.

## Reference
- Design doc Section 6.2 (Collision Resolution)
- Design doc Section 10.3 (Vectorized Operations)

## Sub-Tasks
- [ ] 3.4.1: Vectorized collision detection
- [ ] 3.4.2: Damage stacking and wall destruction
- [ ] 3.4.3: Core breach detection
- [ ] 3.4.4: Unit tests for collision scenarios
"@
        subtasks  = @(
            @{
                number = "3.4.1"
                title  = "Sub-Task 3.4.1: Vectorized collision detection"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Detect enemy-wall collisions using vectorized NumPy operations.

## Deliverables
- Check all alive enemies against grid in single operation
- Only armed walls cause collision
- Return mask of colliding enemies

## Reference
Design doc Section 10.3 code example for vectorized collision.

## Acceptance Criteria
- No Python loops over enemies
- Only wall_armed cells trigger collision
- Correct cell lookup from half-cell positions
"@
            }
            @{
                number = "3.4.2"
                title  = "Sub-Task 3.4.2: Damage stacking and wall destruction"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Handle multiple enemies hitting same wall and wall HP depletion.

## Deliverables
- Multiple enemies on same cell: damage stacks
- wall_hp[y,x] -= count of enemies on cell
- Wall destroyed when HP <= 0
- Reset grid[y,x] = EMPTY, wall_armed = False

## Acceptance Criteria
- 3 enemies on 1-HP wall destroys wall
- Wall state fully cleaned on destruction
- Enemy deaths processed correctly
"@
            }
            @{
                number = "3.4.3"
                title  = "Sub-Task 3.4.3: Core breach detection"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Detect when any enemy reaches the core (row 8).

## Deliverables
- Check: ``enemy_y_half[alive] >= CORE_Y_HALF`` (16)
- Return breach flag for episode termination
- Track which enemy breached (for debugging/viz)

## Acceptance Criteria
- Breach detected at y_half >= 16
- Single breach ends episode
- Breach info available for reward calculation
"@
            }
            @{
                number = "3.4.4"
                title  = "Sub-Task 3.4.4: Unit tests for collision scenarios"
                labels = @("Sub-Task", "core-engine", "testing")
                body   = @"
## Objective
Test collision detection and resolution edge cases.

## Deliverables
- ``tests/unit/test_collision.py`` with tests for:
  - Single enemy hits wall
  - Multiple enemies hit same wall
  - Wall destruction from stacked damage
  - Core breach detection
  - Unarmed wall no collision

## Acceptance Criteria
- Anti-triviality rule verified (unarmed wall)
- Damage stacking verified
- Core breach boundary tested
"@
            }
        )
    }
    @{
        number    = "3.5"
        title     = "Task 3.5: Step Loop"
        milestone = "M03: Core Engine Prototype"
        labels    = @("Task", "core-engine")
        body      = @"
## Objective
Implement deterministic step ordering per design doc Section 9.

## Reference
- Design doc Section 9 (Step Ordering)

## Sub-Tasks
- [ ] 3.5.1: Implement deterministic step ordering
- [ ] 3.5.2: Seed-based RNG for reproducibility
- [ ] 3.5.3: Integration test for determinism
"@
        subtasks  = @(
            @{
                number = "3.5.1"
                title  = "Sub-Task 3.5.1: Implement deterministic step ordering"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement the 12-step tick ordering from design doc.

## Deliverables
- ``src/core/simulation.py`` with step() function
- Order: decrement CDs → apply action → arm walls → move enemies → resolve collisions → check breach → spawn → compact → compute reward → check done → build obs → return

## Reference
Design doc Section 9 specifies exact ordering.

## Acceptance Criteria
- All 12 steps in correct order
- Each step isolated and testable
- Clear separation of concerns
"@
            }
            @{
                number = "3.5.2"
                title  = "Sub-Task 3.5.2: Seed-based RNG for reproducibility"
                labels = @("Sub-Task", "core-engine")
                body   = @"
## Objective
Implement seeded random number generation for deterministic replay.

## Deliverables
- np.random.Generator instance per simulation
- Seed passed at reset()
- All randomness (spawn column, etc.) uses seeded RNG

## Acceptance Criteria
- Same seed = same random sequence
- No use of global np.random state
- Seed stored for replay capability
"@
            }
            @{
                number = "3.5.3"
                title  = "Sub-Task 3.5.3: Integration test for determinism"
                labels = @("Sub-Task", "core-engine", "testing")
                body   = @"
## Objective
Verify same seed + same actions = identical trajectory.

## Deliverables
- ``tests/integration/test_determinism.py``
- Run episode with fixed seed and action sequence
- Run again with same seed and actions
- Assert all state arrays match at every step

## Acceptance Criteria
- Bit-for-bit reproducibility
- Works across multiple episodes
- Documents replay capability
"@
            }
        )
    }

    # -------------------------------------------------------------------------
    # M04: Gymnasium Integration (tasks only, sub-tasks deferred)
    # -------------------------------------------------------------------------
    @{
        number    = "4.1"
        title     = "Task 4.1: Gymnasium Wrapper"
        milestone = "M04: Gymnasium Integration"
        labels    = @("Task", "gymnasium")
        body      = @"
## Objective
Wrap core simulation in Gymnasium-compliant environment.

## Reference
- Design doc Section 2.1 (Decoupled Simulation Pattern)
- Gymnasium API documentation

## Scope
- GridDefenseEnv class inheriting gymnasium.Env
- step(), reset(), render() methods
- Proper episode lifecycle

## Sub-Tasks
To be defined at M03 completion.
"@
        subtasks  = @()
    }
    @{
        number    = "4.2"
        title     = "Task 4.2: Observation Space"
        milestone = "M04: Gymnasium Integration"
        labels    = @("Task", "gymnasium")
        body      = @"
## Objective
Implement 667-feature observation vector with normalization.

## Reference
- Design doc Section 7 (Observation Space)

## Scope
- Feature vector construction from grid state
- Normalization to [0, 1] range
- gymnasium.spaces.Box definition
- Action mask in observation

## Sub-Tasks
To be defined at M03 completion.
"@
        subtasks  = @()
    }
    @{
        number    = "4.3"
        title     = "Task 4.3: Action System"
        milestone = "M04: Gymnasium Integration"
        labels    = @("Task", "gymnasium")
        body      = @"
## Objective
Implement NO-OP + 117 placement actions with masking.

## Reference
- Design doc Section 5 (Action Model)

## Scope
- Action space: Discrete(118)
- Action 0 = NO-OP (always valid)
- Actions 1-117 = cell placement
- Action mask in info dict for MaskablePPO

## Sub-Tasks
To be defined at M03 completion.
"@
        subtasks  = @()
    }
    @{
        number    = "4.4"
        title     = "Task 4.4: Validation"
        milestone = "M04: Gymnasium Integration"
        labels    = @("Task", "gymnasium", "testing")
        body      = @"
## Objective
Validate environment meets all requirements.

## Reference
- Design doc Section 12.3 (Success Criteria)

## Scope
- gymnasium.utils.env_checker.check_env() passes
- Random agent runs 1000 episodes without crash
- Headless SPS > 10,000
- Determinism verified

## Sub-Tasks
To be defined at M03 completion.
"@
        subtasks  = @()
    }
)

# =============================================================================
# Functions
# =============================================================================

function New-GitHubLabel {
    param(
        [string]$Name,
        [string]$Color,
        [string]$Description
    )
    
    if ($PSCmdlet.ShouldProcess($Name, "Create label")) {
        # Check if label exists
        $existing = gh label list --repo $Repo --json name | ConvertFrom-Json | Where-Object { $_.name -eq $Name }
        
        if ($existing) {
            Write-Host "  Label exists: $Name" -ForegroundColor Yellow
        }
        else {
            gh label create $Name --repo $Repo --color $Color --description $Description
            Write-Host "  Created label: $Name" -ForegroundColor Green
        }
    }
}

function New-GitHubMilestone {
    param(
        [string]$Title,
        [string]$Description,
        [string]$DueOn
    )
    
    if ($PSCmdlet.ShouldProcess($Title, "Create milestone")) {
        # Check if milestone exists
        $existing = gh api "repos/$Repo/milestones" --jq ".[] | select(.title == `"$Title`")" 2>$null
        
        if ($existing) {
            Write-Host "  Milestone exists: $Title" -ForegroundColor Yellow
        }
        else {
            $body = @{
                title       = $Title
                description = $Description
            }
            
            if ($DueOn) {
                $body.due_on = $DueOn
            }
            
            $json = $body | ConvertTo-Json -Compress
            $json | gh api "repos/$Repo/milestones" --method POST --input - | Out-Null
            Write-Host "  Created milestone: $Title" -ForegroundColor Green
        }
    }
}

function New-GitHubIssue {
    param(
        [string]$Title,
        [string]$Body,
        [string]$Milestone,
        [string[]]$Labels
    )
    
    if ($PSCmdlet.ShouldProcess($Title, "Create issue")) {
        # Build label arguments
        $labelArgs = @()
        foreach ($label in $Labels) {
            $labelArgs += "--label"
            $labelArgs += $label
        }
        
        $issueUrl = gh issue create --repo $Repo --title $Title --body $Body --milestone $Milestone @labelArgs
        
        # Extract issue number from URL
        $issueNumber = ($issueUrl -split '/')[-1]
        Write-Host "  Created issue #$issueNumber : $Title" -ForegroundColor Green
        
        return [int]$issueNumber
    }
    
    return 0
}

function Add-SubIssueLink {
    param(
        [int]$ParentNumber,
        [int]$ChildNumber
    )
    
    if ($PSCmdlet.ShouldProcess("#$ChildNumber -> #$ParentNumber", "Link sub-issue")) {
        gh sub-issue add $ParentNumber $ChildNumber --repo $Repo 2>$null
        Write-Host "    Linked #$ChildNumber to parent #$ParentNumber" -ForegroundColor Cyan
    }
}

# =============================================================================
# Execution
# =============================================================================

Write-Host "`n=== Grid Defense RL - GitHub Project Setup ===" -ForegroundColor Cyan
Write-Host "Repository: $Repo`n"

# --- Labels ---
Write-Host "Creating labels..." -ForegroundColor White
foreach ($label in $Labels) {
    New-GitHubLabel -Name $label.name -Color $label.color -Description $label.description
}

# --- Milestones ---
Write-Host "`nCreating milestones..." -ForegroundColor White
foreach ($milestone in $Milestones) {
    New-GitHubMilestone -Title $milestone.title -Description $milestone.description -DueOn $milestone.due_on
}

# --- Tasks and Sub-Tasks ---
Write-Host "`nCreating tasks and sub-tasks..." -ForegroundColor White

# AI NOTE: We need to create all issues first, then link sub-issues in a second pass.
# This is because gh sub-issue add requires both issues to exist.
$issueMap = @{}  # Maps task/subtask number to GitHub issue number

foreach ($task in $Tasks) {
    # Create parent task
    $taskNumber = New-GitHubIssue -Title $task.title -Body $task.body -Milestone $task.milestone -Labels $task.labels
    $issueMap[$task.number] = $taskNumber
    
    # Create sub-tasks
    foreach ($subtask in $task.subtasks) {
        $subtaskNumber = New-GitHubIssue -Title $subtask.title -Body $subtask.body -Milestone $task.milestone -Labels $subtask.labels
        $issueMap[$subtask.number] = $subtaskNumber
    }
}

# --- Link Sub-Issues ---
Write-Host "`nLinking sub-issues to parents..." -ForegroundColor White

foreach ($task in $Tasks) {
    if ($task.subtasks.Count -gt 0) {
        $parentIssue = $issueMap[$task.number]
        
        foreach ($subtask in $task.subtasks) {
            $childIssue = $issueMap[$subtask.number]
            Add-SubIssueLink -ParentNumber $parentIssue -ChildNumber $childIssue
        }
    }
}

# --- Summary ---
Write-Host "`n=== Setup Complete ===" -ForegroundColor Cyan
Write-Host "Labels created:     $($Labels.Count)"
Write-Host "Milestones created: $($Milestones.Count)"

$taskCount = ($Tasks | Where-Object { $_.subtasks.Count -eq 0 -or $_.labels -contains "Task" }).Count
$subtaskCount = ($Tasks | ForEach-Object { $_.subtasks.Count } | Measure-Object -Sum).Sum

Write-Host "Tasks created:      $taskCount"
Write-Host "Sub-tasks created:  $subtaskCount"
Write-Host "`nView project: https://github.com/$Repo/issues" -ForegroundColor Green
