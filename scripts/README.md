<!--
---
title: "Scripts"
description: "Training entrypoints and utility scripts"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: training
  - tech: [python, stable-baselines3]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Scripts

Command-line scripts for training, evaluation, and utilities. These are entrypoints, not library code.

---

## 1. Contents

```
scripts/
├── .gitkeep          # Placeholder
└── README.md         # This file
```

---

## 2. Planned Scripts

| Script | Purpose | Stage |
|--------|---------|-------|
| train.py | PPO training entrypoint | phase-1 |
| evaluate.py | Policy evaluation and metrics | phase-1 |
| benchmark.py | SPS benchmark runner | prototype |
| record.py | Episode recording (seed + actions) | phase-1 |

---

## 3. Usage Pattern

Scripts consume configs from `configs/`:

```bash
# Train with default config
python scripts/train.py --config configs/ppo_baseline.yaml

# Evaluate checkpoint
python scripts/evaluate.py --checkpoint checkpoints/model.zip --episodes 100

# Run benchmark
python scripts/benchmark.py --steps 100000
```

---

## 4. Hardware Targeting

Training scripts detect available hardware:

| Hardware | Behavior |
|----------|----------|
| radio-gpu01 (A4000) | Full training, GPU acceleration |
| Desktop (RTX 3080) | Development, visualization |
| CPU-only | Reduced batch size, slower |

---

## 5. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [configs/](../configs/README.md) | Configuration files |
| [renders/](../renders/README.md) | Output directory for recordings |
