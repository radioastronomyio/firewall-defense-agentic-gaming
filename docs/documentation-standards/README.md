<!--
---
title: "Documentation Standards"
description: "Templates and guidelines for Grid Defense RL project documentation"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: documentation
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Documentation Standards

Templates for RAG-optimized documentation customized for the Grid Defense RL project.

---

## 1. Contents

```
documentation-standards/
├── primary-readme-template.md      # Repository root README
├── interior-readme-template.md     # Directory README
├── general-kb-template.md          # Standalone documents
├── worklog-readme-template.md      # Work-log milestone directories
├── code-commenting-dual-audience.md # Code comment methodology
├── tagging-strategy.md             # Controlled vocabulary for this project
├── script-header-python.md         # Python script header
├── script-header-shell.md          # Bash script header
├── script-header-powershell.md     # PowerShell script header
└── README.md                       # This file
```

---

## 2. Templates

### Document Templates

| Template | Use For |
|----------|---------|
| [primary-readme-template.md](primary-readme-template.md) | Repository root README.md |
| [interior-readme-template.md](interior-readme-template.md) | Any directory that needs a README |
| [general-kb-template.md](general-kb-template.md) | Standalone documents (guides, specs, reports) |
| [worklog-readme-template.md](worklog-readme-template.md) | Milestone directories in `work-logs/` |

### Script Header Templates

| Template | Use For |
|----------|---------|
| [script-header-python.md](script-header-python.md) | All `.py` files |
| [script-header-shell.md](script-header-shell.md) | All `.sh` files |
| [script-header-powershell.md](script-header-powershell.md) | All `.ps1` files |

### Guidelines

| Document | Use For |
|----------|---------|
| [tagging-strategy.md](tagging-strategy.md) | Controlled vocabulary (domain, type, stage tags) |
| [code-commenting-dual-audience.md](code-commenting-dual-audience.md) | Writing comments for humans and AI agents |

---

## 3. Project-Specific Tags

Quick reference from [tagging-strategy.md](tagging-strategy.md):

| Category | Values |
|----------|--------|
| `domain` | core-engine, gymnasium-env, training, saliency, rendering, infrastructure, documentation, research |
| `stage` | prototype, phase-1, phase-2, phase-3, phase-4 |
| `tech` | python, numpy, gymnasium, stable-baselines3, pytorch, arcade, opengl |

---

## 4. Template Selection

### Documents

```
Is it the repository root README?
├─ Yes → primary-readme-template.md
└─ No: Is it a directory README?
        ├─ Yes: Is it a work-logs milestone?
        │       ├─ Yes → worklog-readme-template.md
        │       └─ No  → interior-readme-template.md
        └─ No: Is it a standalone document?
                └─ Yes → general-kb-template.md
```

### Scripts

```
What language?
├─ Python (.py)     → script-header-python.md
├─ Bash (.sh)       → script-header-shell.md
└─ PowerShell (.ps1)→ script-header-powershell.md
```

---

## 5. Related

| Document | Relationship |
|----------|--------------|
| [docs/](../README.md) | Parent directory |
| [Grid Defense Spec](../../scratch/grid-defense-spec-v2.md) | Project specification |
