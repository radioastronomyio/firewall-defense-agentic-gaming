<!--
---
title: "Test Suite"
description: "pytest tests, benchmarks, and determinism checks"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: gymnasium-env
  - tech: [python, pytest]
  - stage: prototype
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Test Suite

pytest-based test suite covering core simulation, environment wrapper, and performance validation.

---

## 1. Contents

```
tests/
├── __init__.py           # Package marker
├── test_grid_state.py    # Grid state management tests
├── test_enemies.py       # Enemy movement and spawning tests
├── test_walls.py         # Wall placement and collision tests
├── test_env.py           # Environment integration tests
└── README.md             # This file
```

---

## 2. Files

| File | Description | Status |
|------|-------------|--------|
| test_grid_state.py | Grid array operations | 📋 Planned |
| test_enemies.py | Enemy vectorized operations | 📋 Planned |
| test_walls.py | Wall mechanics | 📋 Planned |
| test_env.py | Gymnasium compliance, SPS benchmark, determinism | 📋 Planned |

---

## 3. Success Criteria

From spec §12.3:

| Metric | Target |
|--------|--------|
| Headless SPS | > 10,000 |
| Gymnasium compliance | Passes `check_env()` |
| Determinism | Same seed + actions = same trajectory |
| Random agent | 1000 episodes, no crash |

---

## 4. Running Tests

```bash
# Run all tests
pytest src/tests/

# Run with coverage
pytest src/tests/ --cov=src/core --cov=src/env

# Run benchmark only
pytest src/tests/test_env.py -k benchmark -v
```

---

## 5. Related

| Document | Relationship |
|----------|--------------|
| [src/](../README.md) | Parent directory |
| [Grid Defense Spec §12](../../scratch/grid-defense-spec-v2.md) | Success criteria |
