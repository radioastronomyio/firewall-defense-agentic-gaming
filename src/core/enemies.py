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
    ENEMY_TICK_DTYPE,
    ENEMY_TYPE_DTYPE,
    MAX_ENEMIES,
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
