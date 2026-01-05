<!--
---
title: "Source Code"
description: "Core simulation, Gymnasium environment, and test suite"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: core-engine
  - tech: [python, numpy, gymnasium]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Source Code

Python source code for the Grid Defense RL environment. Organized into core simulation logic, Gymnasium wrapper, and test suite.

---

## 1. Contents

```
src/
├── core/           # Headless simulation (grid, enemies, walls)
│   └── README.md
├── env/            # Gymnasium environment wrapper
│   └── README.md
├── tests/          # Test suite
│   └── README.md
└── README.md       # This file
```

---

## 2. Subdirectories

| Directory | Description |
|-----------|-------------|
| [core/](core/README.md) | NumPy-based headless simulation. No rendering, no dependencies beyond numpy. |
| [env/](env/README.md) | Gymnasium wrapper. Translates core state to observations. |
| [tests/](tests/README.md) | Test suite including SPS benchmark and determinism checks. |

---

## 3. Architecture

The source follows a decoupled simulation pattern:

```
core/ (Ground Truth)     → Pure NumPy, stateless functions
    ↓
env/  (Interface)        → Gymnasium wrapper, observation builder
    ↓
tests/ (Validation)      → pytest, benchmark, determinism
```

Training happens against `env/`. Visualization (future) reconstructs from seed + action log, never imports from `core/` directly.

---

## 4. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [Grid Defense Spec](../scratch/grid-defense-spec-v2.md) | Specification |
