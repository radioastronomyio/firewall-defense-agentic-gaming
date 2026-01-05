<!--
---
title: "Notebooks"
description: "Jupyter notebooks for experimentation and analysis"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: research
  - tech: [python, jupyter]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Notebooks

Jupyter notebooks for experimentation, prototyping, and analysis. Not production code.

---

## 1. Contents

```
notebooks/
├── .gitkeep          # Placeholder
└── README.md         # This file
```

---

## 2. Planned Notebooks

| Notebook | Purpose | Stage |
|----------|---------|-------|
| env_exploration.ipynb | Interactive environment testing | prototype |
| saliency_dev.ipynb | Perturbation saliency development | phase-4 |
| training_analysis.ipynb | Training curve visualization | phase-1+ |

---

## 3. Conventions

- Notebooks are for exploration, not production
- Clear outputs before committing (reduce repo size)
- Document findings in proper docs, not notebook markdown
- Use `%load_ext autoreload` for development

---

## 4. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [configs/](../configs/README.md) | Hyperparameters used in experiments |
