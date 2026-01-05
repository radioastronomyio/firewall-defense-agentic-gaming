<!--
---
title: "Renders"
description: "Video output and visualization artifacts (gitignored)"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Active"
tags:
  - type: directory-readme
  - domain: rendering
  - tech: [arcade, opengl]
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Renders

Output directory for rendered videos, frames, and visualization artifacts. **This directory is gitignored** — contents are not committed.

---

## 1. Contents

```
renders/
├── .gitkeep          # Ensures directory exists
└── README.md         # This file (committed)
```

---

## 2. Expected Output Types

| Type | Extension | Description |
|------|-----------|-------------|
| Video | .mp4 | Rendered episodes with saliency overlay |
| Frames | .png | Individual frames for debugging |
| Logs | .jsonl | Episode metadata and action logs |

---

## 3. Workflow

1. Train on `radio-gpu01` (headless)
2. Save episode logs (seed + action sequence)
3. Transfer logs to desktop
4. Render with Python Arcade + saliency overlay
5. Output to `renders/`

---

## 4. Storage

This directory is gitignored because:
- Video files are large (hundreds of MB)
- Frames accumulate quickly during development
- Final videos go to external storage / YT upload

---

## 5. Related

| Document | Relationship |
|----------|--------------|
| [Repository Root](../README.md) | Parent |
| [scripts/](../scripts/README.md) | Recording scripts |
| [Grid Defense Spec §11](../scratch/grid-defense-spec-v2.md) | Saliency visualization |
