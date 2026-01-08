<!--
---
title: "Phase 03: Core Engine Prototype"
description: "Headless NumPy simulation with grid arrays, walls, Drop enemy, collision, and deterministic step loop"
author: "VintageDon"
date: "2026-01-04"
version: "0.1"
status: "In Progress"
tags:
  - type: worklog
  - domain: core-engine
  - stage: prototype
related_documents:
  - "[Previous Phase](../02-github-project-frameout/README.md)"
  - "[Next Phase](../04-gymnasium-integration/README.md)"
  - "[Design Document](../../docs/design-document.md)"
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Phase 03: Core Engine Prototype

## Summary

| Attribute | Value |
|-----------|-------|
| Status | 🔄 In Progress |
| Sessions | Ongoing |
| Target | Headless NumPy core running >10k SPS |

Objective: Build the complete headless simulation — grid arrays, wall mechanics, Drop enemy, collision resolution, and deterministic step loop.

---

## 1. Task Overview

| Task | Sub-Tasks | Status | Description |
|------|-----------|--------|-------------|
| 3.1: Grid State Management | 3.1.1-3.1.3 | ✅ Complete | Core arrays, GridState dataclass, factory function |
| 3.2: Wall Mechanics | 3.2.1-3.2.4 | ✅ Complete | Placement, cooldowns, arming, tests |
| 3.3: Enemy System | 3.3.1-3.3.5 | ✅ Complete | Fixed-slot arrays, movement, spawn, compaction |
| 3.4: Collision Resolution | 3.4.1-3.4.4 | 🔄 In Progress | Vectorized detection, damage, core breach |
| 3.5: Step Loop | 3.5.1-3.5.3 | ⬜ Pending | Deterministic ordering, RNG, integration test |

---

## 2. Completed Sub-Tasks

### Task 3.1: Grid State Management ✅

| Sub-Task | Branch | Description | Artifacts |
|----------|--------|-------------|-----------|
| 3.1.1 | `feature/4-define-constants-and-array-dtypes` | Constants and dtype specifications | `src/core/constants.py`, `test_constants.py` |
| 3.1.2 | `feature/5-initialize-grid-arrays` | GridState dataclass and factory | `src/core/grid.py` |
| 3.1.3 | `feature/5-initialize-grid-arrays` | Unit tests for grid state | `src/tests/unit/test_grid.py` |

**Key decisions:**
- `[y, x]` indexing convention matches NumPy/image idiom
- GridState is mutable dataclass (arrays mutated in-place for performance)
- Factory function ensures independent instances per episode

---

## 3. Active Work

### Task 3.2: Wall Mechanics ✅

| Sub-Task | Issue | Status | Description |
|----------|-------|--------|-------------|
| 3.2.1 | #8 | ✅ Complete | Wall placement with validity checks |
| 3.2.2 | #9 | ✅ Complete | Cooldown system (GCD + cell cooldowns) |
| 3.2.3 | #10 | ✅ Complete | Wall arming (pending → armed transition) |
| 3.2.4 | #11 | ✅ Complete | Unit tests for wall lifecycle |

### Task 3.3: Enemy System ✅

| Sub-Task | Issue | Status | Description |
|----------|-------|--------|-------------|
| 3.3.1 | #12 | ✅ Complete | Fixed-slot enemy arrays |
| 3.3.2 | #13 | ✅ Complete | Drop movement (half-cell fixed-point) |
| 3.3.3 | #15 | ✅ Complete | Spawn logic |
| 3.3.4 | #16 | ✅ Complete | Array compaction |
| 3.3.5 | #17 | ✅ Complete | Unit tests for enemy lifecycle |

### Task 3.4: Collision Resolution 🔄

| Sub-Task | Issue | Status | Description |
|----------|-------|--------|-------------|
| 3.4.1 | #19 | ✅ Complete | Vectorized collision detection |
| 3.4.2 | #20 | ✅ Complete | Damage stacking and wall destruction |
| 3.4.3 | #21 | ✅ Complete | Core breach detection |
| 3.4.4 | #22 | ⬜ Pending | Unit tests for collision scenarios |

---

## 4. Session Log

### Session 1 — 2026-01-04

**Focus:** Task 3.1 (Grid State Management)

| Activity | Result |
|----------|--------|
| 3.1.1: Constants module | `constants.py` with all grid dimensions, cell states, cooldowns, dtypes |
| 3.1.2: GridState dataclass | `grid.py` with dataclass and `create_grid_state()` factory |
| 3.1.3: Grid unit tests | `test_grid.py` with 27 tests covering shapes, dtypes, indexing, independence |

**Artifacts produced:**
- `src/core/constants.py`
- `src/core/grid.py`
- `src/tests/unit/test_constants.py`
- `src/tests/unit/test_grid.py`

---

### Session 2 — 2026-01-05

**Focus:** Task 3.2.1–3.2.3 (Wall mechanics implementation)

| Activity | Result |
|----------|--------|
| 3.2.1: Wall placement | `place_wall()` with bounds, GCD, cell_cd, occupancy checks |
| 3.2.2: Cooldown system | `apply_cooldowns()` and `tick_cooldowns()` — vectorized, no Python loops |
| 3.2.3: Wall arming | `arm_pending_walls()` — vectorized pending → armed transition |
| Code review | All three passed — docstrings comprehensive, dual-audience standard met |

**Artifacts produced:**
- `src/core/walls.py` — `place_wall()`, `arm_pending_walls()`
- `src/core/cooldowns.py` — `apply_cooldowns()`, `tick_cooldowns()`
- `src/core/__init__.py` — updated exports for all new functions

---

### Session 3 — 2026-01-05

**Focus:** Task 3.2.4 (Wall lifecycle unit tests)

| Activity | Result |
|----------|--------|
| 3.2.4: Wall lifecycle tests | 9 test classes, ~50 tests covering full wall lifecycle |
| Task 3.2 complete | All wall mechanics implemented and tested |

**Test coverage:**
- `TestPlacementValidity` — bounds, occupancy checks
- `TestPlacementStateMutation` — grid, HP, pending, armed state
- `TestGCDBlocking` — GCD prevents placement when > 0
- `TestCellCooldownBlocking` — cell_cd prevents placement when > 0
- `TestArmingDelay` — anti-triviality rule verification
- `TestArmPendingWalls` — vectorized pending → armed transition
- `TestApplyCooldowns` — GCD and cell_cd application
- `TestTickCooldowns` — vectorized decrement, no underflow
- `TestCooldownLifecycle` — full GCD/cell_cd expiration cycles

**Artifacts produced:**
- `tests/unit/test_walls.py` — comprehensive wall lifecycle test suite

---

### Session 4 — 2026-01-05

**Focus:** Task 3.3.1 (Fixed-slot enemy arrays)

| Activity | Result |
|----------|--------|
| 3.3.1: Enemy arrays | `EnemyState` dataclass with 5 fixed-size arrays |
| Factory function | `create_enemy_state()` matching grid.py pattern |
| Export updates | `__init__.py` updated with enemy exports |

**Key implementation details:**
- Fixed 20 slots — no dynamic resizing, stable observation structure
- Half-cell positions via `enemy_y_half` (int16), cell lookup: `y_half // 2`
- `enemy_spawn_tick` enables stable sorting for observation consistency
- Zero-padded inactive slots with `enemy_alive=False` mask

**Artifacts produced:**
- `src/core/enemies.py` — `EnemyState` dataclass and `create_enemy_state()` factory
- `src/core/__init__.py` — updated exports

---

### Session 5 — 2026-01-05

**Focus:** Task 3.3.2 (Drop movement)

| Activity | Result |
|----------|--------|
| 3.3.2: Drop movement | `move_enemies()` — vectorized half-cell increment |
| Export updates | `__init__.py` updated with `move_enemies` export |

**Key implementation details:**
- Single vectorized operation: `state.enemy_y_half[state.enemy_alive] += ENEMY_SPEED_HALF`
- In-place mutation for performance (no array copying)
- No bounds checking here — core breach detection handled in collision module (3.4.3)
- Cell lookup via integer division: `cell_y = enemy_y_half // 2`

**Artifacts produced:**
- `src/core/enemies.py` — added `move_enemies()` function
- `src/core/__init__.py` — updated exports

---

### Session 6 — 2026-01-05

**Focus:** Task 3.3.3 (Spawn logic)

| Activity | Result |
|----------|--------|
| 3.3.3: Spawn logic | `spawn_enemy()` — spawns Drop at y_half=0, random column |
| Export updates | `__init__.py` updated with `spawn_enemy` export |
| KC issue | KC accidentally deleted `move_enemies()` — restored manually |

**Key implementation details:**
- Finds first dead slot using `np.argmax(~state.enemy_alive)` (vectorized)
- Returns `False` if all 20 slots alive (at capacity)
- Uses seeded `np.random.Generator` for deterministic column selection
- Sets: `enemy_y_half=0`, `enemy_x=rng.integers(0, WIDTH)`, `enemy_alive=True`, `enemy_type=ENEMY_TYPE_DROP`, `enemy_spawn_tick=current_tick`
- Spawn interval/timing not implemented here — belongs in step loop (3.5.1)

**Artifacts produced:**
- `src/core/enemies.py` — added `spawn_enemy()` function
- `src/core/__init__.py` — updated exports

---

### Session 7 — 2026-01-05

**Focus:** Task 3.3.4 (Array compaction)

| Activity | Result |
|----------|--------|
| 3.3.4: Array compaction | `compact_enemies()` — vectorized stable sort with zero-padding |
| Export updates | `__init__.py` updated with `compact_enemies` export |

**Key implementation details:**
- Sort key: alive enemies use `spawn_tick`, dead enemies use `MAX_UINT32` to sort last
- `np.argsort` with `kind='stable'` preserves relative order for same-tick spawns
- Advanced indexing applies sort to all 5 arrays simultaneously
- Zero-pads trailing slots after alive count
- Returns alive count for caller convenience

**Artifacts produced:**
- `src/core/enemies.py` — added `compact_enemies()` function
- `src/core/__init__.py` — updated exports

---

### Session 8 — 2026-01-05

**Focus:** Task 3.3.5 (Enemy lifecycle unit tests)

| Activity | Result |
|----------|--------|
| 3.3.5: Enemy lifecycle tests | 49 tests covering full enemy lifecycle |
| Task 3.3 complete | All enemy system functions implemented and tested |

**Test coverage:**
- `TestEnemyStateFactory` — shapes, dtypes, zero initialization, independence
- `TestSpawnEnemy` — slot finding, state mutations, capacity limits, determinism
- `TestMoveEnemies` — vectorized increment, alive-only movement, accumulation
- `TestCompactEnemies` — stable sort by spawn_tick, zero-padding, alive count
- `TestHalfCellConversion` — cell lookup formula, boundary crossing

**Artifacts produced:**
- `tests/unit/test_enemies.py` — comprehensive enemy lifecycle test suite

---

### Session 9 — 2026-01-08

**Focus:** Task 3.4.1 (Vectorized collision detection)

| Activity | Result |
|----------|--------|
| 3.4.1: Collision detection | `detect_collisions()` — vectorized enemy/wall collision check |
| Export updates | `__init__.py` updated with `detect_collisions` export |
| Unit tests | 20 tests covering all collision scenarios |

**Key implementation details:**
- Advanced NumPy indexing: `wall_armed[cell_y, enemy_x]` checks all 20 positions in single operation
- Half-cell conversion: `cell_y = enemy_y_half // 2` for cell lookup
- Combined with `enemy_alive` mask — dead enemies cannot collide
- Only `wall_armed=True` triggers collision (pending walls do not)
- Returns boolean array shape `(MAX_ENEMIES,)` = `(20,)`

**Test coverage:**
- `TestDetectCollisionsBasic` — no enemies, no walls, single enemy, pending wall handling
- `TestDetectCollisionsMultiple` — multiple enemies, same cell, alive/dead mix
- `TestDetectCollisionsHalfCell` — y_half=0, 1, 2, 17 edge cases, boundary crossing
- `TestDetectCollisionsReturnShape` — shape validation, dtype, dead slots

**Artifacts produced:**
- `src/core/collision.py` — `detect_collisions()` function
- `tests/unit/test_collision.py` — 20 collision detection tests
- `src/core/__init__.py` — updated exports

---

### Session 10 — 2026-01-08

**Focus:** Task 3.4.2 (Damage stacking and wall destruction)

| Activity | Result |
|----------|--------|
| 3.4.2: Collision resolution | `resolve_collisions()` — damage stacking, wall destruction, enemy death |
| Export updates | `__init__.py` updated with `resolve_collisions` export |
| Bug fix | Fixed uint8 underflow bug in KC output — wall_hp subtraction now uses signed arithmetic |

**Key implementation details:**
- `np.add.at()` for vectorized damage counting per cell
- Handles multiple enemies on same cell (damage stacks cumulatively)
- Signed arithmetic to avoid uint8 underflow: cast to int16, subtract, clamp to 0, cast back
- Destruction check: `(damage > 0) & (damage >= wall_hp)` before HP update
- Clears all wall state on destruction: grid, wall_hp, wall_armed, wall_pending
- Marks colliding enemies dead: `enemy_alive[collisions] = False`
- Returns `(enemies_killed, walls_destroyed)` tuple for reward calculation

**Bug caught during review:**
- KC's initial implementation used `grid_state.wall_hp -= damage` which causes uint8 underflow
- Example: HP=1, damage=3 → wraps to 254 instead of -2
- Fixed by comparing damage to HP first, then using signed arithmetic with clamping

**Artifacts produced:**
- `src/core/collision.py` — added `resolve_collisions()` function
- `src/core/__init__.py` — updated exports

---

### Session 11 — 2026-01-08

**Focus:** Task 3.4.3 (Core breach detection)

| Activity | Result |
|----------|--------|
| 3.4.3: Core breach detection | `detect_core_breach()` — vectorized check for enemies reaching bottom |
| Export updates | `__init__.py` updated with `detect_core_breach` export |

**Key implementation details:**
- Vectorized single-liner: `bool(np.any(enemy_state.enemy_y_half[enemy_state.enemy_alive] >= CORE_Y_HALF))`
- Breach threshold: `CORE_Y_HALF = 16` (row 8, bottom of grid)
- Only checks alive enemies via boolean indexing
- Returns `True` if any alive enemy has `y_half >= 16`, `False` otherwise
- No bounds checking — enemies constrained by movement logic

**Artifacts produced:**
- `src/core/collision.py` — added `detect_core_breach()` function
- `src/core/__init__.py` — updated exports

---

## 5. Key Technical Decisions

| Decision | Rationale | Reference |
|----------|-----------|-----------|
| Half-cell integer positions | Eliminates float boundary bugs | Design doc Section 4 |
| Fixed 20 enemy slots | Stable observation structure | Design doc Section 7.2 |
| 1-tick arming delay | Anti-triviality rule — prediction over reaction | Design doc Section 5.3 |
| GCD 10 frames / Cell CD 150 frames | Prevents toggle-juggling, commits to geometry | Design doc Section 5.1 |

---

## 6. Artifacts Index

| Artifact | Location | Description |
|----------|----------|-------------|
| Constants | `src/core/constants.py` | All game constants, single source of truth |
| Grid state | `src/core/grid.py` | GridState dataclass and factory |
| Wall placement | `src/core/walls.py` | `place_wall()`, `arm_pending_walls()` |
| Cooldown system | `src/core/cooldowns.py` | `apply_cooldowns()`, `tick_cooldowns()` |
| Core package | `src/core/__init__.py` | Public API exports |
| Enemy state | `src/core/enemies.py` | EnemyState dataclass, factory, movement, spawn |
| Collision | `src/core/collision.py` | `detect_collisions()`, `resolve_collisions()`, `detect_core_breach()` |
| Constant tests | `src/tests/unit/test_constants.py` | 41 tests validating constants |
| Grid tests | `src/tests/unit/test_grid.py` | 27 tests validating grid state |
| Wall tests | `tests/unit/test_walls.py` | 43 tests validating wall lifecycle |
| Enemy tests | `tests/unit/test_enemies.py` | 49 tests validating enemy lifecycle |
| Collision tests | `tests/unit/test_collision.py` | 20 tests validating collision detection |

---

## 7. Success Criteria

| Metric | Target | Current |
|--------|--------|---------|
| Headless SPS | > 10,000 | ⬜ Not measured |
| Determinism | seed + actions = trajectory | ⬜ Not tested |
| All M03 tests | Pass | 🔄 ~180 passing |
| uint8 safety | No underflow | ✅ Verified in 3.4.2 |
