=====
TASK 3.3.1
=====

===
PROMPT
===

I'll update both files, then output the KC prompt.Documentation updated. Here's the KC prompt for 3.3.1:

---

## Task: Sub-Task 3.3.1 — Fixed-slot enemy arrays #13

**Branch:** `feature/task-3_3_1-fixed-slot-enemy-arrays`

**Mode:** Code

### Objective

Create `src/core/enemies.py` with fixed-slot enemy arrays following the data layout in design-document.md Section 10.2. Arrays are always shape `(MAX_ENEMIES,)` with zero-padding for inactive slots. Include `EnemyState` dataclass and factory function following the pattern established in `grid.py`.

### Scope

**Modify:**
- `src/core/enemies.py` (create)
- `src/core/constants.py` (add MAX_ENEMIES, enemy dtypes)
- `src/core/__init__.py` (add exports)

**Reference:**
- `docs/design-document.md` — Section 6, 7.2, 10.2
- `src/core/grid.py` — pattern for dataclass + factory
- `src/core/constants.py` — existing dtype patterns
- `.kilocode/rules/memory-bank/` — project context

### Deliverables & Validation

1. **Constants in `src/core/constants.py`**
   - [ ] `MAX_ENEMIES = 20` defined
   - [ ] `ENEMY_POS_DTYPE = np.int16` defined
   - [ ] `ENEMY_TYPE_DTYPE = np.uint8` defined
   - [ ] `ENEMY_TICK_DTYPE = np.uint32` defined
   - [ ] All new constants exported in module `__all__`

2. **`EnemyState` dataclass in `src/core/enemies.py`**
   - [ ] `enemy_y_half: np.ndarray` — shape (20,), dtype int16, half-cell y position
   - [ ] `enemy_x: np.ndarray` — shape (20,), dtype int16, cell x position
   - [ ] `enemy_alive: np.ndarray` — shape (20,), dtype bool, active mask
   - [ ] `enemy_type: np.ndarray` — shape (20,), dtype uint8, type ID (0 = Drop)
   - [ ] `enemy_spawn_tick: np.ndarray` — shape (20,), dtype uint32, tick when spawned
   - [ ] Dataclass is mutable (no `frozen=True`)
   - [ ] Dual-audience docstring following project commenting standard

3. **`create_enemy_state()` factory function**
   - [ ] Returns fresh `EnemyState` with all arrays zero-initialized
   - [ ] Each call returns independent instance (no shared arrays)
   - [ ] Docstring with usage example

4. **Exports in `src/core/__init__.py`**
   - [ ] `EnemyState` imported and in `__all__`
   - [ ] `create_enemy_state` imported and in `__all__`

5. **All tests pass**
   - [ ] `pytest tests/` passes with no failures
   - [ ] Existing grid/wall tests unaffected

### Constraints

- Arrays are always full size (20 slots) — no dynamic resizing
- Zero-padding for inactive slots (alive=False)
- No OOP enemies — all operations will be array-based
- Follow `[y, x]` indexing convention (enemy_y_half is vertical position)
- Match existing code style in `src/core/`

---

**Environment:**
- Terminal mode (inline PS disabled)
- venv active
- Context: `.kilocode/rules/memory-bank/`

===
KC Results
===

