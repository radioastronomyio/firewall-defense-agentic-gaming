<!--
---
title: "[Document Title]"
description: "What this document covers"
author: "VintageDon"
date: "YYYY-MM-DD"
version: "1.0"
status: "Draft|Active|Archived"
tags:
  - type: [guide/reference/specification/report/one-pager]
  - domain: [core-engine/gymnasium-env/training/saliency/rendering/infrastructure/documentation/research]
  - tech: [python/numpy/gymnasium/stable-baselines3/pytorch/arcade]
  - stage: [prototype/phase-1/phase-2/phase-3/phase-4]
  - audience: [all/contributors/ml-practitioners/viewers]
related_documents:
  - "[Related Doc](path/to/doc.md)"
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# [Document Title]

[1-2 sentences: What this document provides and why it exists.]

---

## 1. Purpose

[What problem this document solves or what need it addresses. 2-3 sentences max.]

---

## 2. Scope

What's covered:

- [Item 1]
- [Item 2]
- [Item 3]

---

## 3. Audience

[Who should read this and what background is assumed. 1-2 sentences.]

---

## 4. [Content Section Title]

[Your actual content goes here. This is the meat of the document.]

[Add as many content sections as needed: 5, 6, 7, ...]

---

## N. References

| Resource | Description |
|----------|-------------|
| [Grid Defense Spec](../../scratch/grid-defense-spec-v2.md) | Project specification |
| [Link](url) | What it provides |

---

## N+1. Document Info

| | |
|---|---|
| Author | VintageDon |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |
| Version | 1.0 |

---

<!--
TEMPLATE USAGE NOTES (remove when using):

1. FRONTMATTER: Always include. Tags enable RAG retrieval.
   - repository field is REQUIRED
   - Use controlled vocabulary from tagging-strategy.md

2. SEMANTIC NUMBERING: 
   - Sections 1-3 (Purpose/Scope/Audience) are the wrapper
   - Section 4+ is your content
   - If you omit wrapper sections, preserve numbering gaps
   - References and Doc Info are always last (use N, N+1)

3. DOMAIN TAGS (pick one):
   - core-engine: Headless simulation (grid, enemies, walls)
   - gymnasium-env: RL wrapper, obs/action spaces
   - training: PPO, hyperparams, curriculum
   - saliency: xAI visualization
   - rendering: Python Arcade, video output
   - infrastructure: Hardware, deployment
   - documentation: Standards, templates
   - research: GDR outputs, design rationale

4. STAGE TAGS (pick one if applicable):
   - prototype: Initial validation
   - phase-1: Drop training
   - phase-2: Drifter curriculum
   - phase-3: Full enemy roster
   - phase-4: Saliency + video

5. KEEP IT LEAN: Wrapper is thin. Content is the point.
-->
