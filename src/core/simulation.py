#!/usr/bin/env python3
"""
Script Name  : simulation.py
Description  : Deterministic simulation step loop
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-08
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Deterministic simulation step loop that orchestrates all core engine operations
in a fixed order per design document Section 9. This module provides the main
step() function that executes one simulation tick, processing actions, moving
enemies, resolving collisions, spawning new enemies, and computing rewards.

The step ordering is critical for determinism: same seed + same actions must
produce identical trajectories. This is enforced by a strict 12-step sequence
that never varies, ensuring reproducibility for training and testing.

Step Ordering (Section 9)
-------------------------
1. tick_cooldowns() - Decrement GCD and cell cooldowns
2. arm_pending_walls() - Pending → armed transition
3. Apply action - Place wall if action != NO_OP and GCD was 0
4. move_enemies() - All alive enemies advance
5. detect_collisions() + resolve_collisions() - Wall damage, enemy death
6. detect_core_breach() - Check termination condition
7. Spawn enemy - If tick % spawn_interval == 0
8. compact_enemies() - Remove dead, maintain order
9. Compute reward - Enemy kills + survival + breach penalty
10. Increment tick, check termination flags
11. (Observation building deferred to Task 4.2)
12. Return (reward, terminated, truncated)

Note
----
This module implements the core simulation loop but does NOT include:
- Observation building (deferred to Gymnasium wrapper in Task 4.2)
- Action mask generation (deferred to Gymnasium wrapper in Task 4.2)
- Rendering (deferred to observer layer in Phase 4)

Usage
-----
    from src.core import create_simulation_state

    # Create seeded simulation for determinism
    sim_state = create_simulation_state(seed=42)

    # Execute one tick with action 0 (NO-OP)
    reward, terminated, truncated = step(sim_state, action=0)
"""

# =============================================================================
# Imports
# =============================================================================

from dataclasses import dataclass

import numpy as np

from src.core.collision import detect_collisions, detect_core_breach, resolve_collisions
from src.core.constants import (
    DEFAULT_SPAWN_INTERVAL,
    MAX_EPISODE_TICKS,
    NO_OP_ACTION,
    REWARD_CORE_BREACH,
    REWARD_ENEMY_KILLED,
    REWARD_TICK_SURVIVED,
    WIDTH,
)
from src.core.cooldowns import apply_cooldowns, tick_cooldowns
from src.core.enemies import (
    EnemyState,
    compact_enemies,
    create_enemy_state,
    move_enemies,
    spawn_enemy,
)
from src.core.grid import GridState, create_grid_state
from src.core.walls import arm_pending_walls, place_wall

# =============================================================================
# Simulation State
# =============================================================================


@dataclass
class SimulationState:
    """
    Complete simulation state containing grid, enemies, and metadata.

    This dataclass aggregates all state required for a single simulation episode.
    It combines grid state, enemy state, and simulation metadata into a single
    object that can be passed to the step() function for each tick.

    Technical Details
    -----------------
    - Immutable by default: dataclass fields are not frozen, but should be
      treated as read-only outside of step() function
    - Grid state: Contains all wall arrays, cooldowns, and cell contents
    - Enemy state: Contains fixed-slot enemy arrays with positions and status
    - tick: Current simulation tick (0-indexed, increments each step)
    - spawn_interval: Ticks between enemy spawns (default 30 ≈ 1 second)
    - rng: Seeded random number generator for deterministic randomness

    Parameters
    ----------
    grid_state : GridState
        Grid state containing wall arrays, cooldowns, and cell contents.
        Mutated in-place during simulation step.
    enemy_state : EnemyState
        Enemy state containing fixed-slot enemy arrays with positions and status.
        Mutated in-place during simulation step.
    tick : int
        Current simulation tick (0 to MAX_EPISODE_TICKS-1). Increments each
        step call. Used for spawn timing and episode termination.
    spawn_interval : int
        Number of ticks between enemy spawns. Enemies spawn when
        tick % spawn_interval == 0. Default is 30 ticks (~1 second at 30 tps).
    rng : np.random.Generator
        Seeded random number generator for enemy spawn column selection and
        any other randomization. Must be seeded at episode start for
        determinism. Uses np.random.default_rng(seed) for modern NumPy RNG.

    Notes
    -----
    - This dataclass is the primary state object passed to step()
    - All mutations happen in-place (no copying for performance)
    - Factory function create_simulation_state() initializes all fields
    - tick is incremented at end of step() (not beginning)
    - RNG is encapsulated in SimulationState for reproducibility

    Examples
    --------
    >>> from src.core import create_simulation_state
    >>> sim = create_simulation_state(spawn_interval=30)
    >>> sim.tick
    0
    >>> sim.spawn_interval
    30
    >>> sim.grid_state.grid.shape
    (9, 13)
    >>> sim.enemy_state.enemy_y_half.shape
    (20,)
    >>> sim.rng.integers(0, 13)  # Random spawn column
    7
    """

    grid_state: GridState
    enemy_state: EnemyState
    tick: int
    spawn_interval: int
    rng: np.random.Generator


# =============================================================================
# Factory Function
# =============================================================================


def create_simulation_state(
    spawn_interval: int = DEFAULT_SPAWN_INTERVAL,
    seed: int | None = None,
) -> SimulationState:
    """
    Create a new simulation state with initialized grid and enemies.

    This factory function initializes all simulation components to their
    starting values: empty grid, no enemies, tick at 0, and specified
    spawn interval. This is the standard way to create a fresh simulation
    for each episode.

    Technical Details
    -----------------
    - Grid initialization: create_grid_state() returns empty grid with
      all arrays zeroed (no walls, no cooldowns)
    - Enemy initialization: create_enemy_state() returns empty enemy state
      with all slots dead and positions zeroed
    - Tick initialization: Starts at 0, increments each step
    - Spawn interval: Configurable for curriculum learning (e.g., faster
      spawns in advanced episodes)
    - RNG initialization: np.random.default_rng(seed) creates seeded
      generator for deterministic randomness

    Parameters
    ----------
    spawn_interval : int, optional
        Number of ticks between enemy spawns. Default is DEFAULT_SPAWN_INTERVAL
        (30 ticks ≈ 1 second at 30 tps). Enemies spawn when
        tick % spawn_interval == 0. Must be positive integer.
    seed : int or None, optional
        Random seed for reproducibility. If None, uses system entropy
        (non-deterministic). If int, creates deterministic RNG for
        reproducible episodes. Default is None.

    Returns
    -------
    SimulationState
        New simulation state with initialized grid, enemies, and metadata.
        All arrays are fresh copies (no shared references with previous states).
        RNG is seeded with provided seed (or None for non-deterministic).

    Notes
    -----
    - This function is called by Gymnasium wrapper's reset() method
    - Spawn interval can be varied for curriculum learning
    - No enemies are present at initialization (first spawn at tick=0)
    - Grid is completely empty (no walls, no cooldowns)
    - RNG is encapsulated in SimulationState for reproducibility
    - Same seed + same actions = identical trajectory (determinism)

    Examples
    --------
    >>> from src.core import create_simulation_state
    >>> sim = create_simulation_state()
    >>> sim.tick
    0
    >>> sim.spawn_interval
    30
    >>> np.sum(sim.enemy_state.enemy_alive)
    0
    >>> np.sum(sim.grid_state.grid)
    0
    >>> # Custom spawn interval for harder episodes
    >>> sim_fast = create_simulation_state(spawn_interval=15)
    >>> sim_fast.spawn_interval
    15
    >>> # Seeded simulation for reproducibility
    >>> sim_seeded = create_simulation_state(seed=42)
    >>> col1 = sim_seeded.rng.integers(0, 13)
    >>> sim_seeded2 = create_simulation_state(seed=42)
    >>> col2 = sim_seeded2.rng.integers(0, 13)
    >>> col1 == col2  # Same seed produces same sequence
    True
    """
    grid_state = create_grid_state()
    enemy_state = create_enemy_state()
    rng = np.random.default_rng(seed)

    return SimulationState(
        grid_state=grid_state,
        enemy_state=enemy_state,
        tick=0,
        spawn_interval=spawn_interval,
        rng=rng,
    )


# =============================================================================
# Step Function
# =============================================================================


def step(
    sim_state: SimulationState,
    action: int,
) -> tuple[float, bool, bool]:
    """
    Execute one simulation tick with deterministic step ordering.

    This function implements the complete 12-step simulation loop per design
    document Section 9. The ordering is strictly enforced to ensure
    determinism: same seed + same actions = identical trajectory.

    The step function processes actions, moves enemies, resolves collisions,
    spawns new enemies, computes rewards, and checks termination conditions.
    All operations are vectorized for performance (>10k SPS target).

    Step Ordering (Section 9)
    -------------------------
    1. tick_cooldowns() - Decrement GCD and cell cooldowns
    2. arm_pending_walls() - Pending → armed transition
    3. Apply action - Place wall if action != NO_OP and GCD was 0
    4. move_enemies() - All alive enemies advance
    5. detect_collisions() + resolve_collisions() - Wall damage, enemy death
    6. detect_core_breach() - Check termination condition
    7. Spawn enemy - If tick % spawn_interval == 0
    8. compact_enemies() - Remove dead, maintain order
    9. Compute reward - Enemy kills + survival + breach penalty
    10. Increment tick, check terminated/truncated
    11. (Observation building deferred to Task 4.2)
    12. Return (reward, terminated, truncated)

    Technical Details
    -----------------
    - In-place mutation: All state arrays modified directly (no copying)
    - Vectorized operations: No Python loops over enemies or cells
    - Deterministic ordering: Fixed 12-step sequence, no conditional branching
    - Action validation: NO-OP (0) always valid, placement requires GCD=0
    - Cooldown tracking: GCD checked before action, applied after placement
    - Reward structure: Binary rewards (no shaping) per Section 8
    - Termination conditions: Core breach (terminated) or max ticks (truncated)
    - RNG encapsulation: Uses sim_state.rng (seeded at creation)

    Parameters
    ----------
    sim_state : SimulationState
        Current simulation state containing grid, enemies, metadata, and RNG.
        Mutated in-place during step execution.
    action : int
        Action to execute this tick. Action 0 = NO-OP (always valid).
        Actions 1-117 = Place wall at cell (x, y) where y, x = divmod(action-1, 13).
        Placement only succeeds if GCD was 0 before this tick.

    Returns
    -------
    tuple[float, bool, bool]
        (reward, terminated, truncated) tuple.
        - reward: Float reward for this tick. REWARD_ENEMY_KILLED * enemies_killed
          + REWARD_TICK_SURVIVED (+ REWARD_CORE_BREACH if breached).
        - terminated: True if core breached (game over), False otherwise.
        - truncated: True if tick >= MAX_EPISODE_TICKS (time limit), False otherwise.

    Notes
    -----
    - Observation building is deferred to Gymnasium wrapper (Task 4.2)
    - Action mask generation is deferred to Gymnasium wrapper (Task 4.2)
    - Core breach immediately terminates episode with negative reward
    - Truncation occurs at MAX_EPISODE_TICKS (1000 ticks)
    - Spawn timing: tick % spawn_interval == 0 (spawn at tick 0, 30, 60, ...)
    - Enemy spawn column is random but deterministic via sim_state.rng
    - Dead enemies are compacted to maintain contiguous alive block
    - Wall placement fails silently if GCD > 0 or cell invalid
    - RNG is encapsulated in SimulationState for reproducibility

    Examples
    --------
    >>> from src.core import create_simulation_state
    >>> # Create seeded simulation for reproducibility
    >>> sim = create_simulation_state(seed=42)
    >>> # Execute NO-OP action
    >>> reward, terminated, truncated = step(sim, action=0)
    >>> reward  # Survival reward + first enemy spawn
    0.0
    >>> terminated
    False
    >>> truncated
    False
    >>> sim.tick
    1
    >>> # Place wall at cell (4, 6) = action 4*13 + 6 + 1 = 59
    >>> sim.grid_state.gcd = 0  # Reset GCD to allow placement
    >>> reward, terminated, truncated = step(sim, action=59)
    >>> sim.grid_state.grid[4, 6]  # Wall placed
    1
    >>> sim.grid_state.gcd  # GCD applied after placement
    10
    >>> # Core breach scenario
    >>> sim2 = create_simulation_state(seed=42)
    >>> sim2.enemy_state.enemy_alive[0] = True
    >>> sim2.enemy_state.enemy_y_half[0] = 16  # At breach threshold
    >>> reward, terminated, truncated = step(sim2, action=0)
    >>> terminated
    True
    >>> reward
    -1.0
    >>> # Episode truncation
    >>> sim3 = create_simulation_state(seed=42)
    >>> sim3.tick = MAX_EPISODE_TICKS
    >>> reward, terminated, truncated = step(sim3, action=0)
    >>> truncated
    True
    """
    # =============================================================================
    # Step 1: Decrement cooldowns
    # =============================================================================
    # Decrement GCD and all cell cooldowns by 1 frame
    # This happens BEFORE action check, so GCD decrements from previous action
    tick_cooldowns(sim_state.grid_state)

    # =============================================================================
    # Step 2: Arm pending walls
    # =============================================================================
    # Transition walls from pending state to armed state
    # This implements the 1-tick arming delay (anti-triviality rule)
    # Newly placed walls remain pending during the same tick they're placed
    # Only walls from the previous tick are armed
    arm_pending_walls(sim_state.grid_state)

    # =============================================================================
    # Step 3: Apply action (if valid)
    # =============================================================================
    # Check if action is NO-OP or if GCD was 0 before this tick
    # Note: GCD was decremented in Step 1, so we check if it's now 0
    # This means a 10-frame GCD blocks actions for 10 ticks after placement
    if action != NO_OP_ACTION and sim_state.grid_state.gcd == 0:
        # Convert action to (y, x) coordinates
        # Action mapping: y, x = divmod(action - 1, WIDTH)
        # Action 0 is NO-OP, actions 1-117 map to cells
        y, x = divmod(action - 1, WIDTH)

        # Attempt to place wall at specified cell
        # place_wall() handles validity checks (cell empty, no cooldown, etc.)
        # Returns True if placement succeeded, False otherwise
        placement_success = place_wall(sim_state.grid_state, y, x)

        # If placement succeeded, apply cooldowns
        # apply_cooldowns() sets GCD and cell cooldown for the placed wall
        if placement_success:
            apply_cooldowns(sim_state.grid_state, y, x)

    # =============================================================================
    # Step 4: Move enemies
    # =============================================================================
    # Advance all alive enemies downward by ENEMY_SPEED_HALF (1 half-cell)
    # This is a vectorized operation: enemy_y_half[alive] += 1
    move_enemies(sim_state.enemy_state)

    # =============================================================================
    # Step 5: Detect and resolve collisions
    # =============================================================================
    # Detect which enemies occupy cells with armed walls
    # Only armed walls trigger collisions (pending walls do not)
    collisions = detect_collisions(sim_state.grid_state, sim_state.enemy_state)

    # Resolve collisions: apply damage, destroy walls, mark enemies dead
    # Returns (enemies_killed, walls_destroyed) for reward calculation
    enemies_killed, _ = resolve_collisions(
        sim_state.grid_state, sim_state.enemy_state, collisions
    )

    # =============================================================================
    # Step 6: Check core breach
    # =============================================================================
    # Check if any alive enemy has reached or exceeded CORE_Y_HALF (16)
    # This is a game-ending condition: a single breach terminates the episode
    breached = detect_core_breach(sim_state.enemy_state)

    # =============================================================================
    # Step 7: Spawn enemy (if due)
    # =============================================================================
    # Spawn enemy if current tick is divisible by spawn_interval
    # Spawn timing: tick % spawn_interval == 0 (e.g., every 30 ticks)
    # First spawn happens at tick 0 (immediately after reset)
    if sim_state.spawn_interval > 0 and sim_state.tick % sim_state.spawn_interval == 0:
        spawn_enemy(sim_state.enemy_state, sim_state.tick, sim_state.rng)

    # =============================================================================
    # Step 8: Compact enemies
    # =============================================================================
    # Remove dead enemies, shift alive enemies to maintain contiguous block
    # Preserves spawn order for stable observation structure
    # Zero-pads trailing slots after compaction
    compact_enemies(sim_state.enemy_state)

    # =============================================================================
    # Step 9: Compute reward
    # =============================================================================
    # Binary reward structure per Section 8 (no shaping)
    # Reward = (enemies_killed * REWARD_ENEMY_KILLED) + REWARD_TICK_SURVIVED
    # If breached, add REWARD_CORE_BREACH (negative penalty)
    reward = (enemies_killed * REWARD_ENEMY_KILLED) + REWARD_TICK_SURVIVED

    if breached:
        reward += REWARD_CORE_BREACH

    # =============================================================================
    # Step 10: Increment tick, check termination flags
    # =============================================================================
    # Increment tick counter for next step
    sim_state.tick += 1

    # Check termination conditions
    # terminated: Core breach occurred (game over)
    # truncated: Reached maximum episode length (time limit)
    terminated = breached
    truncated = sim_state.tick >= MAX_EPISODE_TICKS

    # =============================================================================
    # Step 11: (Observation building deferred to Task 4.2)
    # =============================================================================
    # Observation space definition and building will be implemented in
    # Gymnasium wrapper (src/env/grid_defense_env.py) during Task 4.2

    # =============================================================================
    # Step 12: Return results
    # =============================================================================
    return reward, terminated, truncated
