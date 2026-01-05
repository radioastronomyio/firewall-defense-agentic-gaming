<!--
---
title: "Tagging Strategy Guide"
description: "Controlled vocabulary for Grid Defense RL project documentation"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
tags:
  - type: guide
  - domain: documentation
related_documents:
  - "[Interior README Template](interior-readme-template.md)"
  - "[General KB Template](general-kb-template.md)"
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Tagging Strategy Guide

## 1. Purpose

Controlled tag vocabulary for the Grid Defense RL project. Consistent tagging enables navigation and RAG retrieval across documentation.

---

## 2. Domain Tags

Project-specific content categories:

| Tag | Description |
|-----|-------------|
| `core-engine` | Headless simulation logic (grid, enemies, walls, collisions) |
| `gymnasium-env` | Gymnasium wrapper, observation/action spaces, step loop |
| `training` | PPO training, hyperparameters, curriculum, checkpoints |
| `saliency` | xAI visualization, perturbation methods, attention mapping |
| `rendering` | Python Arcade visualization, shaders, video output |
| `infrastructure` | Hardware, deployment, cluster integration |
| `documentation` | Templates, standards, guides |
| `research` | GDR outputs, multi-model synthesis, design rationale |

---

## 3. Type Tags

| Tag | Use For |
|-----|---------|
| `directory-readme` | README for a directory (interior READMEs) |
| `project-root` | Repository root README |
| `guide` | Step-by-step procedures |
| `reference` | Lookup information (schema, API, constants) |
| `specification` | Formal requirements or contracts |
| `worklog` | Phase milestone documentation |
| `report` | Analysis, findings, summaries |
| `one-pager` | Compact handoff documents for cross-model context |

---

## 4. Tech Tags

Technologies used in this project:

| Tag | Description |
|-----|-------------|
| `python` | Primary language |
| `numpy` | Core simulation arrays |
| `gymnasium` | RL environment interface |
| `stable-baselines3` | PPO implementation |
| `pytorch` | Neural network backend |
| `arcade` | 2D rendering (future) |
| `opengl` | Shader pipeline (future) |

---

## 5. Training Stage Tags

For documents related to specific curriculum phases:

| Tag | Description |
|-----|-------------|
| `prototype` | Initial validation (Drop enemy, random agent) |
| `phase-1` | Drop training, PPO baseline |
| `phase-2` | Drifter introduction, curriculum expansion |
| `phase-3` | Seeker/Flood, full enemy roster |
| `phase-4` | Saliency integration, video production |

---

## 6. Status Tags

| Tag | Description |
|-----|-------------|
| `draft` | In development, not complete |
| `active` | Current, maintained |
| `deprecated` | Superseded, avoid for new work |
| `archived` | Historical reference only |

---

## 7. Audience Tags

| Tag | Description |
|-----|-------------|
| `all` | General audience |
| `contributors` | Active developers |
| `ml-practitioners` | Users with RL/ML background |
| `viewers` | YouTube audience (educational content consumers) |

---

## 8. Implementation

### In YAML Frontmatter

```yaml
<!--
---
title: "Document Title"
description: "What this document covers"
tags:
  - type: specification
  - domain: gymnasium-env
  - tech: [python, numpy, gymnasium]
  - stage: prototype
  - status: active
  - audience: contributors
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->
```

### Conventions

- Lowercase, hyphenated values (`core-engine` not `CoreEngine`)
- One value per line for readability
- Array syntax `[a, b, c]` for multi-value fields like `tech`
- Always include `repository` field in frontmatter

---

## 9. References

| Resource | Description |
|----------|-------------|
| [Interior README Template](interior-readme-template.md) | Directory README format |
| [General KB Template](general-kb-template.md) | Standalone document format |
| [Grid Defense Spec v2](../../scratch/grid-defense-spec-v2.md) | Current project specification |
