<!--
---
title: "Scripts"
description: "Training entrypoints and utility scripts"
author: "VintageDon"
date: "2026-01-04"
version: "1.1"
status: "Active"
tags:
  - type: directory-readme
  - domain: training
  - tech: [python, powershell, stable-baselines3]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Scripts

Command-line scripts for training, evaluation, and utilities. These are entrypoints, not library code.

---

## 1. Contents

```
scripts/
├── Initialize-GitHubProject.ps1   # GitHub project setup (labels, milestones, issues)
├── Initialize-RepoStructure.ps1   # Repository scaffolding
└── README.md                      # This file
```

---

## 2. Setup Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| Initialize-RepoStructure.ps1 | Create directory structure | ✅ Complete |
| Initialize-GitHubProject.ps1 | Create GitHub labels, milestones, tasks, sub-tasks | ✅ Complete |

### Initialize-GitHubProject.ps1

Creates the full GitHub Project structure:

- Labels for categorization (Task, Sub-Task, domain labels)
- Milestones M01-M06
- Tasks with sub-task linkages (progress bars)
- Sub-tasks as assignable work units

**Prerequisites:** `gh` CLI authenticated, `gh-sub-issue` extension installed.

```powershell
# Run from repository root
.\scripts\Initialize-GitHubProject.ps1

# Preview without creating
.\scripts\Initialize-GitHubProject.ps1 -WhatIf
```

---

## 3. Planned Scripts

| Script | Purpose | Stage |
|--------|---------|-------|
| train.py | PPO training entrypoint | phase-1 |
| evaluate.py | Policy evaluation and metrics | phase-1 |
| benchmark.py | SPS benchmark runner | prototype |
| record.py | Episode recording (seed + actions) | phase-1 |

---

## 4. Usage Pattern

Training scripts will consume configs from `configs/`:

```bash
# Train with default config
python scripts/train.py --config configs/ppo_baseline.yaml

# Evaluate checkpoint
python scripts/evaluate.py --checkpoint checkpoints/model.zip --episodes 100

# Run benchmark
python scripts/benchmark.py --steps 100000
```

---

## 5. Hardware Targeting

Training scripts detect available hardware:

| Hardware | Behavior |
|----------|----------|
| radio-gpu01 (A4000) | Full training, GPU acceleration |
| Desktop (RTX 3080) | Development, visualization |
| CPU-only | Reduced batch size, slower |

---

## 6. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [configs/](../configs/README.md) | Configuration files |
| [renders/](../renders/README.md) | Output directory for recordings |
