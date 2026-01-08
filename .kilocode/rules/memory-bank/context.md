# Grid Defense RL Context

## Project Origin

This project emerged from exploring the intersection of gaming, RL, and xAI for YouTube educational content. Initial research via Gemini Deep Research (GDR) explored a "packet filter defense" concept, which evolved into a grid-based tower defense where the cybersecurity framing is thematic wrapper, not the point.

## Multi-Model Synthesis

The specification was developed through multi-model collaboration:

| Model | Contribution |
|-------|--------------|
| **GDR Round 1** | Initial research: 13×9 grid (PPO horizon math), hybrid cooldown model, vector perturbation saliency |
| **GPT-5.2 Review 1** | Architecture validation: added NO-OP action, 1-tick wall arming rule |
| **GPT-5.2 Review 2** | Implementation fixes: `[y,x]` indexing, fixed-point positions, fixed enemy slots |
| **Claude** | Orchestration, spec synthesis, prompt engineering |

## Key Documents

| Document | Location | Purpose |
|----------|----------|---------|
| Design Document | `docs/design-document.md` | Authoritative technical specification |
| Spec v2 | `scratch/grid-defense-spec-v2.md` | Internal working spec |
| One-pager | `scratch/grid-defense-one-pager.md` | Compact handoff format |
| GDR Round 1 | `.internal-files/Grid Defense RL Environment Design.md` | Initial research |
| GDR Round 2 | `.internal-files/Grid Defense RL Implementation Refinement.md` | Refinement pass |

## Content Philosophy

The educational hook is **"watch an agent break, then adapt"**:

1. Train agent on Drop enemy (down-only movement)
2. Introduce Drifter (down + lateral)
3. Watch agent fail spectacularly
4. Saliency shows agent "looking in wrong place"
5. Retrain on mixed enemies
6. Saliency shifts—agent now tracks lateral movement

This creates natural episode arcs for 15-minute YouTube content.

## Current Status

**Phase:** M03 — Core Engine Prototype (nearing completion)

**Active work:** Task 3.5 (Step Loop), sub-tasks 3.5.2-3.5.3 remaining

**Completed:**
- M01: Ideation and Setup — GDR research, GPT-5.2 review, spec consolidation, repo scaffolding
- M02: GitHub Project Frameout — Labels, milestones, tasks, sub-tasks defined
- Task 3.1: Grid State Management — GridState dataclass, factory, unit tests
- Task 3.2: Wall Mechanics — Placement, cooldowns, arming, full test coverage
- Task 3.3: Enemy System — Fixed-slot arrays, movement, spawn, compaction, full test coverage
- Task 3.4: Collision Resolution — `detect_collisions()`, `resolve_collisions()`, `detect_core_breach()`, full test coverage
- Task 3.5.1: Deterministic step ordering — `SimulationState`, `create_simulation_state()`, `step()` with 12-step tick loop

**Remaining M03:**
- Task 3.5.2: Seed-based RNG for reproducibility
- Task 3.5.3: Integration test for determinism

**Next:** After M03 complete, M04 (Gymnasium Integration) sub-tasks will be defined based on learnings.

## Work Tracking

- GitHub Project: https://github.com/radioastronomyio/firewall-defense-agentic-gaming/issues
- Work logs: `work-logs/` directory with per-phase documentation
- Rolling horizon: M03 fully decomposed (19 sub-tasks), M04 tasks only, M05+ placeholders
