<!--
---
title: "Phase 02: GitHub Project Frameout"
description: "GitHub project structure creation with milestones, tasks, and sub-tasks"
author: "VintageDon"
date: "2026-01-04"
version: "1.0"
status: "Complete"
tags:
  - type: worklog
  - domain: documentation
  - stage: prototype
related_documents:
  - "[Previous Phase](../01-ideation-and-setup/README.md)"
  - "[Next Phase](../03-core-engine-prototype/README.md)"
repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming
---
-->

# Phase 02: GitHub Project Frameout

## Summary

| Attribute | Value |
|-----------|-------|
| Status | ✅ Complete |
| Sessions | 1 |
| Artifacts | 1 script, 2 README updates |

Objective: Transform project scope into actionable GitHub Project with milestones, tasks, and sub-tasks.

Outcome: PowerShell script creates complete project structure. Rolling horizon approach adopted — M03 fully decomposed, M04 tasks only, M05+ placeholders.

---

## 1. Contents

```
02-github-project-frameout/
└── README.md             # This file
```

Script located at: `scripts/Initialize-GitHubProject.ps1`

---

## 2. Work Completed

| Task | Description | Result |
|------|-------------|--------|
| Scope discussion | Milestone granularity, rolling horizon approach | M03-M04 framed, M05+ deferred |
| Script creation | PowerShell script per methodology | `scripts/Initialize-GitHubProject.ps1` |
| Documentation | Updated scripts README | Reflects new script |

---

## 3. Artifacts Produced

| Artifact | Location | Description |
|----------|----------|-------------|
| Setup script | `scripts/Initialize-GitHubProject.ps1` | Creates labels, milestones, tasks, sub-tasks |
| Scripts README | `scripts/README.md` | Updated with setup scripts section |

---

## 4. Project Structure Created

### Milestones

| # | Name | Status |
|---|------|--------|
| M01 | Ideation and Setup | Backfill (complete) |
| M02 | GitHub Project Frameout | Backfill (complete) |
| M03 | Core Engine Prototype | Tasks + sub-tasks defined |
| M04 | Gymnasium Integration | Tasks only (sub-tasks at M03 end) |
| M05 | PPO Training Baseline | Placeholder |
| M06 | Visualization Layer | Placeholder |

### M03 Tasks and Sub-Tasks

| Task | Sub-Tasks |
|------|-----------|
| 3.1: Grid State Management | 3.1.1-3.1.3 (3 sub-tasks) |
| 3.2: Wall Mechanics | 3.2.1-3.2.4 (4 sub-tasks) |
| 3.3: Enemy System | 3.3.1-3.3.5 (5 sub-tasks) |
| 3.4: Collision Resolution | 3.4.1-3.4.4 (4 sub-tasks) |
| 3.5: Step Loop | 3.5.1-3.5.3 (3 sub-tasks) |

**Total:** 5 tasks, 19 sub-tasks for M03

### M04 Tasks (Sub-Tasks Deferred)

| Task | Scope |
|------|-------|
| 4.1: Gymnasium Wrapper | GridDefenseEnv class |
| 4.2: Observation Space | 667-feature vector |
| 4.3: Action System | NO-OP + 117 placement |
| 4.4: Validation | check_env, random agent, SPS |

---

## 5. Key Decisions

| Decision | Rationale |
|----------|-----------|
| Rolling horizon | Avoid over-planning; M03 learnings inform M04 sub-tasks |
| M01/M02 no sub-tasks | Procedural overhead, follows documented methodology |
| Direct commits for M01/M02 | No branches/PRs needed for setup phases |
| 19 sub-tasks for M03 | Session-sized units, independently assignable |

---

## 6. Labels Created

| Label | Color | Purpose |
|-------|-------|---------|
| Task | Blue | Parent issues |
| Sub-Task | Purple | Assignable work units |
| core-engine | Red | NumPy simulation |
| gymnasium | Green | Environment wrapper |
| training | Yellow | PPO/RL training |
| visualization | Pink | Rendering/saliency |
| documentation | Light blue | Docs and READMEs |
| testing | Light blue | Unit/integration tests |

---

## 7. Next Phase

Handoff: GitHub Project populated. M03 sub-tasks are ready for assignment.

Next Steps:

1. Run `scripts/Initialize-GitHubProject.ps1` to create GitHub structure
2. Begin M03 development with Task 3.1: Grid State Management
3. At M03 completion, define M04 sub-tasks based on learnings
