## Task: Sub-Task 3.2.3 — Wall arming (pending → armed transition) #10

Branch: `feature/task-3_2_3-wall-arming`
Mode: Code

### Objective

Implement the 1-tick wall arming delay (anti-triviality rule). Walls placed this tick have `wall_pending=True, wall_armed=False`. On the next tick, pending walls transition to armed. Only armed walls cause collision damage.

### Scope

**Modify:**
- `src/core/walls.py` — Add `arm_pending_walls()` function
- `src/core/__init__.py` — Export `arm_pending_walls`

**Reference:**
- `.kilocode/rules/memory-bank/tasks.md` — Task definition
- `docs/design-document.md` — Section 5.3 (Anti-Triviality Rule), Section 9 (Step Ordering, step 3)
- `src/core/walls.py` — Existing `place_wall()` sets pending=True, armed=False
- `src/core/cooldowns.py` — Pattern reference for vectorized tick operations

### Deliverables & Validation

1. **`arm_pending_walls(state: GridState) -> None` function in `walls.py`**
   - [ ] Vectorized operation: `wall_armed |= wall_pending` (or equivalent)
   - [ ] Clears pending after arming: `wall_pending[:] = False`
   - [ ] No Python loops over cells
   - [ ] Docstring follows project convention (see `place_wall()`, `tick_cooldowns()`)

2. **Export in `__init__.py`**
   - [ ] `arm_pending_walls` imported from `src.core.walls`
   - [ ] Added to `__all__` list

3. **Basic validation**
   - [ ] Manual test in Python REPL or scratch script confirms:
     - Fresh state: `wall_pending` and `wall_armed` both False everywhere
     - After `place_wall(state, 4, 6)`: `wall_pending[4,6]=True`, `wall_armed[4,6]=False`
     - After `arm_pending_walls(state)`: `wall_pending[4,6]=False`, `wall_armed[4,6]=True`

### Constraints

- Function is called once per tick in step loop (step 3 in Section 9)
- Must handle case where no walls are pending (no-op, no errors)
- Do NOT modify `place_wall()` — it already sets correct initial state
- Unit tests deferred to Sub-Task 3.2.4

---

**Environment:**
- Terminal mode (inline PS disabled)
- venv active
- Context: `.kilocode/rules/memory-bank/`
