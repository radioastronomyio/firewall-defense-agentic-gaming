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
| 3.3: Enemy System | 3.3.1-3.3.5 | 🔄 In Progress | Fixed-slot arrays, movement, spawn, compaction |
| 3.4: Collision Resolution | 3.4.1-3.4.4 | ⬜ Pending | Vectorized detection, damage, core breach |
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

### Task 3.2: Wall Mechanics 🔄

| Sub-Task | Issue | Status | Description |
|----------|-------|--------|-------------|
| 3.2.1 | #8 | ✅ Complete | Wall placement with validity checks |
| 3.2.2 | #9 | ✅ Complete | Cooldown system (GCD + cell cooldowns) |
| 3.2.3 | #10 | ✅ Complete | Wall arming (pending → armed transition) |
| 3.2.4 | #11 | ✅ Complete | Unit tests for wall lifecycle |

### Task 3.3: Enemy System 🔄

| Sub-Task | Issue | Status | Description |
|----------|-------|--------|-------------|
| 3.3.1 | #12 | ✅ Complete | Fixed-slot enemy arrays |
| 3.3.2 | #13 | ⬜ Pending | Drop movement (half-cell fixed-point) |
| 3.3.3 | #14 | ⬜ Pending | Spawn logic |
| 3.3.4 | #15 | ⬜ Pending | Array compaction |
| 3.3.5 | #16 | ⬜ Pending | Unit tests for enemy lifecycle |

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
| Enemy state | `src/core/enemies.py` | EnemyState dataclass and factory |
| Constant tests | `src/tests/unit/test_constants.py` | 41 tests validating constants |
| Grid tests | `src/tests/unit/test_grid.py` | 27 tests validating grid state |
| Wall tests | `tests/unit/test_walls.py` | 43 tests validating wall lifecycle |

---

## 7. Success Criteria

| Metric | Target | Current |
|--------|--------|---------|
| Headless SPS | > 10,000 | ⬜ Not measured |
| Determinism | seed + actions = trajectory | ⬜ Not tested |
| All M03 tests | Pass | 🔄 ~118 passing |
