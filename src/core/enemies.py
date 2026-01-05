#!/usr/bin/env python3
"""
Script Name  : enemies.py
Description  : Enemy state management and initialization
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
EnemyState dataclass and factory function for managing enemy state arrays.
All enemy arrays use fixed-size (MAX_ENEMIES,) = (20,) shape with zero-padding
for inactive slots. This module provides the single source of truth for enemy
state initialization.

State Arrays (Section 10.2)
---------------------------
- enemy_y_half: Half-cell y position (vertical position in half-cells)
- enemy_x: Cell x position (horizontal position, integer)
- enemy_alive: Active mask (True if enemy is alive, False if slot empty)
- enemy_type: Type ID (0 = Drop, future types 1+)
- enemy_spawn_tick: Tick when spawned (for stable ordering)

All arrays are always shape (20,) - no dynamic resizing. Inactive slots are
zero-padded with enemy_alive=False.

Usage
-----
    from src.core.enemies import EnemyState, create_enemy_state

    # Create fresh enemy state for new episode
    state = create_enemy_state()

    # Access arrays using slot index
    state.enemy_y_half[0] = 0  # Spawn enemy at top
    state.enemy_x[0] = 6
    state.enemy_alive[0] = True
    state.enemy_type[0] = 0  # Drop enemy
"""

# =============================================================================
# Imports
# =============================================================================

from dataclasses import dataclass

import numpy as np

from src.core.constants import (
    ENEMY_ALIVE_DTYPE,
    ENEMY_POS_DTYPE,
    ENEMY_SPEED_HALF,
    ENEMY_TICK_DTYPE,
    ENEMY_TYPE_DROP,
    ENEMY_TYPE_DTYPE,
    MAX_ENEMIES,
    WIDTH,
)

# =============================================================================
# EnemyState Dataclass
# =============================================================================


@dataclass
class EnemyState:
    """
    Container for all enemy state arrays.

    All enemy arrays have shape (MAX_ENEMIES,) = (20,) and use fixed-size
    arrays with zero-padding for inactive slots. No dynamic resizing - arrays
    are always full size, with enemy_alive mask indicating active slots.

    Note
    ----
    This dataclass is designed for initialization. During simulation,
    arrays are mutated in-place for performance. The factory function
    create_enemy_state() should be called at episode reset to get
    fresh, independent state.

    Attributes
    ----------
    enemy_y_half : np.ndarray
        Half-cell y positions with shape (20,), dtype int16.
        Vertical position in half-cells (0-16 for grid height 9).
        Cell lookup: cell_y = enemy_y_half // 2.
    enemy_x : np.ndarray
        Cell x positions with shape (20,), dtype int16.
        Horizontal position in cells (0-12 for grid width 13).
    enemy_alive : np.ndarray
        Active mask with shape (20,), dtype bool_.
        True if enemy slot is active, False if slot is empty.
    enemy_type : np.ndarray
        Type IDs with shape (20,), dtype uint8.
        0 = Drop (prototype), future types 1+.
    enemy_spawn_tick : np.ndarray
        Spawn tick with shape (20,), dtype uint32.
        Tick when enemy was spawned (for stable ordering).
    """

    # Enemy arrays with shape (20,)
    enemy_y_half: np.ndarray
    enemy_x: np.ndarray
    enemy_alive: np.ndarray
    enemy_type: np.ndarray
    enemy_spawn_tick: np.ndarray


# =============================================================================
# Factory Function
# =============================================================================


def create_enemy_state() -> EnemyState:
    """
    Create a fresh EnemyState with all arrays initialized to zero.

    This is the canonical way to create enemy state for a new episode.
    Each call returns independent arrays with no shared references.

    Returns
    -------
    EnemyState
        Fresh enemy state with:
        - enemy_y_half: all zeros (no enemies)
        - enemy_x: all zeros (no enemies)
        - enemy_alive: all False (all slots empty)
        - enemy_type: all zeros (no type assigned)
        - enemy_spawn_tick: all zeros (no spawn time)

    Notes
    -----
    All arrays are created with np.zeros() to ensure deterministic
    initialization. The factory function guarantees that each call
    returns completely independent state—modifying one instance does
    not affect any other instance.

    Arrays are always shape (MAX_ENEMIES,) = (20,). Inactive slots are
    zero-padded with enemy_alive=False. This fixed-size design eliminates
    variable-length observation noise and enables vectorized operations.

    Examples
    --------
    >>> state1 = create_enemy_state()
    >>> state2 = create_enemy_state()
    >>> state1.enemy_alive[0] = True
    >>> state1.enemy_y_half[0] = 0
    >>> state1.enemy_x[0] = 6
    >>> state1.enemy_type[0] = 0  # Drop
    >>> state2.enemy_alive[0]  # Still False, independent arrays
    False
    """
    # Initialize all enemy arrays to zero with correct shapes and dtypes
    enemy_y_half = np.zeros(MAX_ENEMIES, dtype=ENEMY_POS_DTYPE)
    enemy_x = np.zeros(MAX_ENEMIES, dtype=ENEMY_POS_DTYPE)
    enemy_alive = np.zeros(MAX_ENEMIES, dtype=ENEMY_ALIVE_DTYPE)
    enemy_type = np.zeros(MAX_ENEMIES, dtype=ENEMY_TYPE_DTYPE)
    enemy_spawn_tick = np.zeros(MAX_ENEMIES, dtype=ENEMY_TICK_DTYPE)

    return EnemyState(
        enemy_y_half=enemy_y_half,
        enemy_x=enemy_x,
        enemy_alive=enemy_alive,
        enemy_type=enemy_type,
        enemy_spawn_tick=enemy_spawn_tick,
    )


# =============================================================================
# Spawn Logic
# =============================================================================


def spawn_enemy(
    state: EnemyState, current_tick: int, rng: np.random.Generator
) -> bool:
    """
    Spawn a Drop enemy at the top of the grid in a random column.

    Finds the first dead slot (enemy_alive[i] == False) and initializes
    it with a new Drop enemy. Returns False if all 20 slots are alive.

    This function only spawns a single enemy. Spawn interval/timing logic
    is handled by the step loop (see simulation.py, task 3.5.1).

    Parameters
    ----------
    state : EnemyState
        Enemy state to mutate in-place. Arrays are modified directly.
    current_tick : int
        Current simulation tick for spawn_tick tracking. Used for
        stable ordering during compaction (task 3.3.4).
    rng : np.random.Generator
        Seeded random number generator for reproducibility. Do NOT
        use np.random global state.

    Returns
    -------
    bool
        True if enemy spawned successfully, False if all slots are alive.

    Notes
    -----
    Slot finding uses np.argmax(~state.enemy_alive) which returns the
    first index where enemy_alive is False. This is equivalent to a
    linear scan but vectorized. If all slots are alive, argmax returns
    0, so we verify the slot is actually dead before spawning.

    The spawned enemy is initialized with:
    - enemy_y_half = 0 (top of grid, half-cell position)
    - enemy_x = random column 0-12 (using rng.integers)
    - enemy_alive = True
    - enemy_type = ENEMY_TYPE_DROP (0)
    - enemy_spawn_tick = current_tick

    Examples
    --------
    >>> state = create_enemy_state()
    >>> rng = np.random.default_rng(42)
    >>> spawn_enemy(state, 0, rng)
    True
    >>> state.enemy_alive[0]
    True
    >>> state.enemy_y_half[0]
    0
    >>> state.enemy_x[0]  # Random column from seed 42
    6
    >>> # All slots full, spawn fails
    >>> for i in range(20):
    ...     spawn_enemy(state, i, rng)
    True
    >>> spawn_enemy(state, 20, rng)
    False
    """
    # Find first dead slot using vectorized operation
    # ~state.enemy_alive gives True for dead slots
    # argmax returns first True index
    dead_slots = ~state.enemy_alive
    slot = np.argmax(dead_slots)

    # Verify slot is actually dead (argmax returns 0 if all False)
    if not dead_slots[slot]:
        return False

    # Initialize enemy in the found slot
    state.enemy_y_half[slot] = 0  # Top of grid
    state.enemy_x[slot] = rng.integers(0, WIDTH)  # Random column 0-12
    state.enemy_alive[slot] = True
    state.enemy_type[slot] = ENEMY_TYPE_DROP
    state.enemy_spawn_tick[slot] = current_tick

    return True


# =============================================================================
# Enemy Movement
# =============================================================================


def move_enemies(state: EnemyState) -> None:
    """
    Move all alive enemies downward by ENEMY_SPEED_HALF half-cells.

    This function implements Drop enemy movement using a half-cell fixed-point
    position system. Enemies move downward at a constant speed of 1 half-cell
    per tick (0.5 cells per tick). Only alive enemies are moved; dead slots
    remain unchanged.

    The movement is vectorized for performance—no Python loops are used.
    A masked assignment updates only the positions of alive enemies.

    Technical Details
    -----------------
    - Position system: enemy_y_half stores vertical position in half-cells
    - Cell lookup: cell_y = enemy_y_half // 2 (integer division)
    - Movement: state.enemy_y_half[state.enemy_alive] += ENEMY_SPEED_HALF
    - ENEMY_SPEED_HALF = 1 (from constants.py)
    - In-place mutation: state.enemy_y_half is modified directly

    No bounds checking is performed here—core breach detection is handled
    separately in the collision module (task 3.4.3).

    Parameters
    ----------
    state : EnemyState
        Enemy state arrays. enemy_y_half is mutated in-place.

    Returns
    -------
    None
        Mutates state in-place (specifically state.enemy_y_half).

    Examples
    --------
    >>> state = create_enemy_state()
    >>> state.enemy_alive[0] = True
    >>> state.enemy_y_half[0] = 0  # Spawn at top
    >>> state.enemy_x[0] = 6
    >>> move_enemies(state)
    >>> state.enemy_y_half[0]
    1  # Moved down by 1 half-cell
    >>> state.enemy_y_half[0] // 2  # Cell lookup
    0  # Still in row 0 (cell boundary at y_half=1)

    Notes
    -----
    This function is called once per tick during the simulation step loop.
    The movement is deterministic—given the same initial state, the same
    movement will always occur. This is critical for reproducible training.

    The half-cell system eliminates float boundary bugs. Enemies at y_half=1
    are visually in the middle of row 0, but cell lookup returns row 0.
    When y_half reaches 2, cell lookup returns row 1.
    """
    # Vectorized movement: increment y_half for all alive enemies
    state.enemy_y_half[state.enemy_alive] += ENEMY_SPEED_HALF
