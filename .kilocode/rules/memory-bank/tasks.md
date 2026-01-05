# Grid Defense RL Tasks

## Current Phase: Prototype

### Completed

- [x] GDR Round 1 — Initial research
- [x] GDR Round 2 — Implementation refinement
- [x] Multi-model synthesis — GPT-5.2 architecture review
- [x] Spec v2 — Consolidated specification
- [x] Repository scaffolding — Directory structure, templates
- [x] Memory bank — KiloCode context populated
- [x] Work-log 01 — Ideation and setup documentation

### In Progress

- [ ] Prototype implementation
  - [ ] `src/core/config.py` — Constants
  - [ ] `src/core/grid_state.py` — State arrays
  - [ ] `src/core/enemies.py` — Drop enemy
  - [ ] `src/core/walls.py` — Wall mechanics
  - [ ] `src/env/grid_defense_env.py` — Gymnasium wrapper
  - [ ] `src/tests/test_env.py` — SPS benchmark, determinism

### Prototype Success Criteria

| Metric | Target | Status |
|--------|--------|--------|
| Headless SPS | > 10,000 | ⬜ Not started |
| Gymnasium compliance | `check_env()` passes | ⬜ Not started |
| Determinism | seed + actions = trajectory | ⬜ Not started |
| Random agent | 1000 episodes, no crash | ⬜ Not started |

## Phase 1: Drop Training

- [ ] PPO baseline configuration
- [ ] Training script
- [ ] Evaluation metrics
- [ ] Episode recording (seed + actions)

## Phase 2: Curriculum

- [ ] Drifter enemy implementation
- [ ] Curriculum schedule
- [ ] Failure recording (trained Drop agent vs Drifter)
- [ ] Mixed training

## Phase 3: Full Roster

- [ ] Seeker enemy (Dijkstra pathfinding)
- [ ] Flood enemy (Boids behavior)
- [ ] Full curriculum

## Phase 4: Visualization

- [ ] Python Arcade observer
- [ ] Saliency computation
- [ ] Saliency overlay rendering
- [ ] Video production pipeline

## Backlog

- [ ] KISS variants (Sprinter, Tank, Splitter, Weaver, Jumper)
- [ ] Reward shaping (if training flatlines)
- [ ] LSTM policy exploration
- [ ] Frame stacking experiments
