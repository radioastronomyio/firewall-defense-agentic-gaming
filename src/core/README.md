<!--
---
title: "Core Simulation"
description: "Headless NumPy-based game logic"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: core-engine
  - tech: [python, numpy]
  - stage: prototype
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Core Simulation

Headless game logic using NumPy arrays. Pure math, no rendering, no Gymnasium dependencies. Target: >10k steps/second.

---

## 1. Contents

```
core/
├── __init__.py        # Package exports
├── config.py          # Grid size, speeds, cooldowns, MAX_ENEMIES
├── grid_state.py      # State arrays, reset, step helpers
├── enemies.py         # Drop behavior, vectorized, fixed-point
├── walls.py           # Placement, cooldown, arming, collision
└── README.md          # This file
```

---

## 2. Files

| File | Description | Status |
|------|-------------|--------|
| config.py | Constants and configuration | 📋 Planned |
| grid_state.py | State management | 📋 Planned |
| enemies.py | Enemy movement and spawning | 📋 Planned |
| walls.py | Wall placement and collision | 📋 Planned |

---

## 3. Design Principles

### Coordinate Convention

Arrays use `(H, W)` shape = `(9, 13)` and index as `[y, x]`:

```python
grid = np.zeros((9, 13), dtype=np.int8)  # (H, W)
grid[y, x] = WALL  # row y, column x
```

### Fixed-Point Positions

Enemy positions use half-cell integers (no floats):

```python
enemy_y_half: np.ndarray  # dtype=np.int16
cell_y = enemy_y_half // 2
```

### Vectorized Operations

No OOP enemies. All updates are array operations:

```python
enemy_y_half[enemy_alive] += speed_half
```

---

## 4. Related

| Document | Relationship |
|----------|--------------|
| [src/](../README.md) | Parent directory |
| [Grid Defense Spec](../../scratch/grid-defense-spec-v2.md) | Specification |
