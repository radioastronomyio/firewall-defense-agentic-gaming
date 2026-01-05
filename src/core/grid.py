#!/usr/bin/env python3
"""
Script Name  : grid.py
Description  : Grid state management and initialization
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
GridState dataclass and factory function for managing the core simulation state.
All grid arrays use (HEIGHT, WIDTH) = (9, 13) shape with [y, x] indexing.
This module provides the single source of truth for grid state initialization.

State Arrays (Section 10.1)
---------------------------
- grid: Cell contents (0=empty, 1=wall)
- wall_hp: Wall hit points (0 if no wall)
- wall_armed: Boolean, true if wall can kill enemies
- wall_pending: Boolean, true if wall placed this tick (arming delay)
- cell_cd: Cell cooldowns (frames until cell can be used again)
- gcd: Global cooldown (frames until next action allowed)

Usage
-----
    from src.core.grid import GridState, create_grid_state

    # Create fresh grid state for new episode
    state = create_grid_state()

    # Access arrays using [y, x] indexing
    state.grid[4, 6] = 1  # Place wall at row 4, column 6
"""

# =============================================================================
# Imports
# =============================================================================

from dataclasses import dataclass

import numpy as np

from src.core.constants import (
    COOLDOWN_DTYPE,
    GRID_DTYPE,
    GRID_SHAPE,
    WALL_HP_DTYPE,
    WALL_STATE_DTYPE,
)

# =============================================================================
# GridState Dataclass
# =============================================================================


@dataclass
class GridState:
    """
    Immutable container for all grid state arrays.

    All grid arrays have shape (HEIGHT, WIDTH) = (9, 13) and use [y, x] indexing.
    The gcd field is a scalar, not an array.

    Note
    ----
    This dataclass is designed for initialization. During simulation,
    arrays are mutated in-place for performance. The factory function
    create_grid_state() should be called at episode reset to get
    fresh, independent state.

    Attributes
    ----------
    grid : np.ndarray
        Cell contents array with shape (9, 13), dtype int8.
        0 = empty, 1 = wall.
    wall_hp : np.ndarray
        Wall hit points array with shape (9, 13), dtype uint8.
        0 if no wall present, >0 for active walls.
    wall_armed : np.ndarray
        Boolean array with shape (9, 13), dtype bool_.
        True if wall can kill enemies on collision.
    wall_pending : np.ndarray
        Boolean array with shape (9, 13), dtype bool_.
        True if wall was placed this tick (arming delay).
    cell_cd : np.ndarray
        Cell cooldown array with shape (9, 13), dtype uint16.
        Frames until cell can be used again after wall placement.
    gcd : np.uint16
        Global cooldown (scalar), frames until next action allowed.
    """

    # Grid arrays with shape (9, 13)
    grid: np.ndarray
    wall_hp: np.ndarray
    wall_armed: np.ndarray
    wall_pending: np.ndarray
    cell_cd: np.ndarray

    # Global cooldown (scalar)
    gcd: np.uint16


# =============================================================================
# Factory Function
# =============================================================================


def create_grid_state() -> GridState:
    """
    Create a fresh GridState with all arrays initialized to zero.

    This is the canonical way to create grid state for a new episode.
    Each call returns independent arrays with no shared references.

    Returns
    -------
    GridState
        Fresh grid state with:
        - grid: all zeros (all cells empty)
        - wall_hp: all zeros (no walls)
        - wall_armed: all False (no armed walls)
        - wall_pending: all False (no pending walls)
        - cell_cd: all zeros (no cooldowns active)
        - gcd: 0 (no global cooldown)

    Notes
    -----
    All arrays are created with np.zeros() to ensure deterministic
    initialization. The factory function guarantees that each call
    returns completely independent state—modifying one instance does
    not affect any other instance.

    Examples
    --------
    >>> state1 = create_grid_state()
    >>> state2 = create_grid_state()
    >>> state1.grid[4, 6] = 1
    >>> state2.grid[4, 6]  # Still 0, independent arrays
    0
    """
    # Initialize all grid arrays to zero with correct shapes and dtypes
    grid = np.zeros(GRID_SHAPE, dtype=GRID_DTYPE)
    wall_hp = np.zeros(GRID_SHAPE, dtype=WALL_HP_DTYPE)
    wall_armed = np.zeros(GRID_SHAPE, dtype=WALL_STATE_DTYPE)
    wall_pending = np.zeros(GRID_SHAPE, dtype=WALL_STATE_DTYPE)
    cell_cd = np.zeros(GRID_SHAPE, dtype=COOLDOWN_DTYPE)

    # Global cooldown starts at 0 (no cooldown)
    gcd = np.uint16(0)

    return GridState(
        grid=grid,
        wall_hp=wall_hp,
        wall_armed=wall_armed,
        wall_pending=wall_pending,
        cell_cd=cell_cd,
        gcd=gcd,
    )
