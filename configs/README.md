<!--
---
title: "Configuration Files"
description: "Hyperparameters and experiment configurations"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: training
  - tech: [yaml]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Configuration Files

YAML configuration files for training hyperparameters, experiment settings, and environment variants.

---

## 1. Contents

```
configs/
├── .gitkeep          # Placeholder
└── README.md         # This file
```

---

## 2. Planned Configurations

| Config | Purpose | Stage |
|--------|---------|-------|
| env_default.yaml | Default environment parameters | prototype |
| ppo_baseline.yaml | PPO hyperparameters for Drop training | phase-1 |
| curriculum.yaml | Enemy introduction schedule | phase-2+ |

---

## 3. Configuration Schema

Environment configs:

```yaml
grid:
  width: 13
  height: 9

cooldowns:
  gcd: 10
  cell: 150

enemies:
  max_count: 20
  spawn_interval: 30
```

Training configs:

```yaml
algorithm: PPO
policy: MlpPolicy
learning_rate: 3e-4
n_steps: 2048
batch_size: 64
n_epochs: 10
gamma: 0.99
gae_lambda: 0.95
```

---

## 4. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [scripts/](../scripts/README.md) | Training scripts that consume these configs |
| [Grid Defense Spec](../scratch/grid-defense-spec-v2.md) | Default values |
