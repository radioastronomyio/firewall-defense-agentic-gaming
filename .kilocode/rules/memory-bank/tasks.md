# Grid Defense RL — Tasks

Project board: https://github.com/radioastronomyio/firewall-defense-agentic-gaming/issues

Rolling horizon approach: M03 fully decomposed, M04 tasks only, M05+ placeholders.

---

## M01: Ideation and Setup ✅

Project inception, multi-model research synthesis, repository scaffolding.

| Task | Status | Description |
|------|--------|-------------|
| 1.1: Ideation and Setup | ✅ Complete | GDR research, GPT-5.2 review, spec v2, repo scaffolding, memory bank |

---

## M02: GitHub Project Frameout ✅

Project board populated, work units defined and assignable.

| Task | Status | Description |
|------|--------|-------------|
| 2.1: GitHub Project Frameout | ✅ Complete | Labels, milestones, tasks, sub-tasks created via script |

---

## M03: Core Engine Prototype 🔄

Headless NumPy core: grid arrays, walls, Drop enemy, collision, deterministic step loop.

### Task 3.1: Grid State Management

Implement core grid arrays with correct indexing convention and data types.

| Sub-Task | Status | Description |
|----------|--------|-------------|
| 3.1.1: Define constants and array dtypes | ✅ Complete | Create `src/core/constants.py` with grid dimensions, cell states, position constants, cooldown values, and numpy dtype specifications. Single source of truth — no magic numbers elsewhere. |
| 3.1.2: Initialize grid arrays | ✅ Complete | Implement `src/core/grid.py` with GridState initialization. Arrays: grid, wall_hp, wall_armed, wall_pending, cell_cd, gcd. All use `[y, x]` indexing, shapes (9, 13). |
| 3.1.3: Unit tests for array shapes and indexing | ✅ Complete | `tests/unit/test_grid.py` verifying shapes, dtypes, `[y, x]` indexing, reset behavior. |

### Task 3.2: Wall Mechanics

Implement wall placement, cooldown system, and arming logic.

| Sub-Task | Status | Description |
|----------|--------|-------------|
| 3.2.1: Wall placement with validity checks | ✅ Complete | `src/core/walls.py` placement function. Validity: GCD=0, cell_cd[y,x]=0, grid[y,x]!=WALL. Returns success/failure. |
| 3.2.2: Cooldown system (GCD + cell cooldowns) | ✅ Complete | GCD: 10 frames after any action. Cell CD: ~150 frames after wall placed. Decrement each tick. |
| 3.2.3: Wall arming (pending → armed transition) | ✅ Complete | 1-tick arming delay (anti-triviality rule). Freshly placed wall does not kill enemy same tick. |
| 3.2.4: Unit tests for wall lifecycle | ✅ Complete | `tests/unit/test_walls.py` covering placement, GCD blocking, cell CD blocking, arming delay, HP tracking. |

### Task 3.3: Enemy System

Implement Drop enemy with fixed-slot arrays and half-cell movement.

| Sub-Task | Status | Description |
|----------|--------|-------------|
| 3.3.1: Fixed-slot enemy arrays | ✅ Complete | `src/core/enemies.py` with 20 fixed slots. Arrays: enemy_y_half, enemy_x, enemy_alive, enemy_type, enemy_spawn_tick. Zero-padded, spawn-order sorted. |
| 3.3.2: Drop movement (half-cell fixed-point) | ✅ Complete | Movement: `enemy_y_half[alive] += 1` per tick. Cell lookup: `cell_y = enemy_y_half // 2`. No floats. |
| 3.3.3: Spawn logic | ✅ Complete | Spawn at y_half=0, random column (0-12). Uses seeded RNG. Find first dead slot via `np.argmax`. |
| 3.3.4: Array compaction | ✅ Complete | Remove dead enemies, shift alive to maintain contiguous block, preserve spawn order, zero-pad trailing. |
| 3.3.5: Unit tests for enemy lifecycle | ✅ Complete | `tests/unit/test_enemies.py` covering spawn, movement, compaction, MAX_ENEMIES limit, half-cell conversion. |

### Task 3.4: Collision Resolution

Implement vectorized collision detection and resolution.

| Sub-Task | Status | Description |
|----------|--------|-------------|
| 3.4.1: Vectorized collision detection | ✅ Complete | Check all alive enemies against grid in single operation. Only armed walls trigger collision. No Python loops. |
| 3.4.2: Damage stacking and wall destruction | ✅ Complete | `resolve_collisions()` — np.add.at() for damage counting, signed arithmetic for uint8 safety, returns (killed, destroyed). |
| 3.4.3: Core breach detection | ✅ Complete | Check `enemy_y_half[alive] >= 16`. Single breach ends episode. |
| 3.4.4: Unit tests for collision scenarios | ✅ Complete | `tests/unit/test_collision.py` covering single hit, multi-hit, damage stacking, core breach, unarmed wall no-collision. |

### Task 3.5: Step Loop

Implement deterministic step ordering per design doc Section 9.

| Sub-Task | Status | Description |
|----------|--------|-------------|
| 3.5.1: Implement deterministic step ordering | ✅ Complete | `src/core/simulation.py` with 12-step tick order: decrement CDs → apply action → arm walls → move → collide → breach check → spawn → compact → reward → done → obs → return. |
| 3.5.2: Seed-based RNG for reproducibility | ✅ Complete | np.random.Generator per simulation. Seed at reset(). All randomness uses seeded RNG, no global state. |
| 3.5.3: Integration test for determinism | ⬜ Pending | `tests/integration/test_determinism.py` verifying same seed + same actions = identical trajectory, bit-for-bit. |

---

## M04: Gymnasium Integration ⬜

Environment wrapper, observation space, action masking, random agent validation, >10k SPS.

Sub-tasks to be defined at M03 completion.

| Task | Status | Description |
|------|--------|-------------|
| 4.1: Gymnasium Wrapper | ⬜ Pending | GridDefenseEnv class inheriting gymnasium.Env. step(), reset(), render() methods. |
| 4.2: Observation Space | ⬜ Pending | 667-feature vector with normalization. gymnasium.spaces.Box definition. |
| 4.3: Action System | ⬜ Pending | Discrete(118): NO-OP + 117 placement. Action mask in info dict for MaskablePPO. |
| 4.4: Validation | ⬜ Pending | check_env() passes, random agent 1000 episodes, headless SPS > 10,000, determinism verified. |

---

## M05: PPO Training Baseline ⬜

Placeholder — Train MaskablePPO on Drop, validate performance and determinism.

---

## M06: Visualization Layer ⬜

Placeholder — Python Arcade observer, replay from seed+log, saliency overlay.

---

## Success Criteria (M03-M04)

| Metric | Target | Status |
|--------|--------|--------|
| Headless SPS | > 10,000 | ⬜ |
| Gymnasium compliance | `check_env()` passes | ⬜ |
| Determinism | seed + actions = trajectory | ⬜ |
| Random agent | 1000 episodes, no crash | ⬜ |
