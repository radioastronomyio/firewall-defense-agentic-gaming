<!--
---
title: "Test Suite"
description: "pytest tests, benchmarks, and determinism checks"
author: "VintageDon"
date: "2026-01-04"
version: "1.1"
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
├── README.md             # This file
├── unit/                 # Unit tests (isolated component tests)
│   ├── __init__.py
│   ├── test_constants.py # Constants module validation
│   ├── test_grid.py      # Grid state management (planned)
│   ├── test_walls.py     # Wall mechanics (planned)
│   ├── test_enemies.py   # Enemy system (planned)
│   └── test_collision.py # Collision resolution (planned)
└── integration/          # Integration tests (cross-component)
    ├── __init__.py
    └── test_determinism.py # Seed reproducibility (planned)
```

---

## 2. Test Status

### Unit Tests

| File | Description | Status |
|------|-------------|--------|
| test_constants.py | Constants match design doc | ✅ Complete (41 tests) |
| test_grid.py | Grid array shapes, dtypes, indexing | 📋 Planned (3.1.3) |
| test_walls.py | Wall placement, cooldowns, arming | 📋 Planned (3.2.4) |
| test_enemies.py | Spawn, movement, compaction | 📋 Planned (3.3.5) |
| test_collision.py | Collision detection, damage stacking | 📋 Planned (3.4.4) |

### Integration Tests

| File | Description | Status |
|------|-------------|--------|
| test_determinism.py | Same seed + actions = same trajectory | 📋 Planned (3.5.3) |
| test_env.py | Gymnasium compliance, SPS benchmark | 📋 Planned (M04) |

---

## 3. Success Criteria

From design doc §12.3:

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

# Run unit tests only
pytest src/tests/unit/

# Run integration tests only
pytest src/tests/integration/

# Run with coverage
pytest src/tests/ --cov=src/core --cov=src/env

# Run specific test file
pytest src/tests/unit/test_constants.py -v
```

---

## 5. Related

| Document | Relationship |
|----------|--------------|
| [src/](../README.md) | Parent directory |
| [Design Document §12](../../docs/design-document.md) | Success criteria |
