#!/usr/bin/env python3
"""
Script Name  : cooldowns.py
Description  : Global and cell cooldown management
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Cooldown management for global action cooldown and per-cell cooldowns.
This module enforces the commitment constraints that force the agent to
make geometric decisions rather than toggle-juggling.

Cooldown System (Section 5.1-5.2)
----------------------------------
- Global Cooldown (GCD): 10 frames after any action before next action allowed
- Cell Cooldown: 150 frames (~5 seconds at 30 ticks/s) after wall placement
  before the cell can be used again

The cooldown system prevents the agent from:
- Rapidly toggling walls on/off (GCD)
- Reusing the same cell immediately (cell CD)
- Reactively placing walls on top of enemies (combined with arming delay)

Note
----
This module does NOT perform validity checks. The place_wall() function
checks cooldowns before placement. This module applies cooldowns after
a successful wall placement and decrements them each tick.

Usage
-----
    from src.core.grid import create_grid_state
    from src.core.walls import place_wall
    from src.core.cooldowns import apply_cooldowns, tick_cooldowns

    # After successful wall placement
    state = create_grid_state()
    if place_wall(state, y=4, x=6):
        apply_cooldowns(state, y=4, x=6)

    # Each tick in step loop
    tick_cooldowns(state)
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.constants import CELL_CD_FRAMES, COOLDOWN_DTYPE, GCD_FRAMES
from src.core.grid import GridState

# =============================================================================
# Cooldown Application
# =============================================================================


def apply_cooldowns(state: GridState, y: int, x: int) -> None:
    """
    Apply global and cell cooldowns after a successful wall placement.

    This function should be called immediately after place_wall() returns
    True to enforce the cooldown constraints that commit the agent to
    geometric decisions.

    Cooldown Values
    ---------------
    - Global Cooldown (GCD): Set to GCD_FRAMES (10 frames)
    - Cell Cooldown: Set to CELL_CD_FRAMES (150 frames) at the placed cell

    The GCD blocks all actions for 10 frames, forcing the agent to wait
    before making another decision. The cell CD blocks reuse of the same
    cell for 150 frames, preventing rapid wall toggling.

    Parameters
    ----------
    state : GridState
        Current grid state to modify. Mutated in-place.
    y : int
        Row index of the wall placement (0 to HEIGHT-1). Uses [y, x] indexing.
    x : int
        Column index of the wall placement (0 to WIDTH-1). Uses [y, x] indexing.

    Returns
    -------
    None
        This function mutates state in-place and returns nothing.

    Notes
    -----
    - This function assumes the wall placement was valid (bounds, GCD=0, cell_cd=0)
    - No validation is performed—caller should ensure placement was successful
    - Cooldowns are set to their maximum values, not incremented
    - The step loop decrements cooldowns each tick via tick_cooldowns()

    Examples
    --------
    >>> from src.core.grid import create_grid_state
    >>> from src.core.walls import place_wall
    >>> from src.core.cooldowns import apply_cooldowns
    >>> state = create_grid_state()
    >>> if place_wall(state, 4, 6):
    ...     apply_cooldowns(state, 4, 6)
    >>> state.gcd
    10
    >>> state.cell_cd[4, 6]
    150
    >>> state.cell_cd[0, 0]  # Other cells unchanged
    0
    """
    # Set global cooldown to maximum value
    state.gcd = np.uint16(GCD_FRAMES)

    # Set cell cooldown at the placed cell to maximum value
    state.cell_cd[y, x] = np.uint16(CELL_CD_FRAMES)


# =============================================================================
# Cooldown Tick
# =============================================================================


def tick_cooldowns(state: GridState) -> None:
    """
    Decrement all active cooldowns by one frame.

    This function should be called once per tick in the step loop to
    progress cooldowns toward zero. Cooldowns stop at 0 and do not
    underflow into negative values.

    Decrement Logic
    ---------------
    - Global Cooldown (GCD): Decremented by 1 if > 0, else stays 0
    - Cell Cooldowns: All cells with value > 0 decremented by 1 (vectorized)

    The vectorized decrement for cell_cd uses NumPy's maximum() function
    to ensure no underflow: cell_cd = np.maximum(cell_cd - 1, 0)

    Parameters
    ----------
    state : GridState
        Current grid state to modify. Mutated in-place.

    Returns
    -------
    None
        This function mutates state in-place and returns nothing.

    Notes
    -----
    - Vectorized operation: no Python loops over cells
    - GCD is a scalar np.uint16, cell_cd is a 2D array
    - Cooldowns stop at 0 (no negative values)
    - This function should be called every tick in the step loop
    - Order in step loop: after action application, before collision

    Examples
    --------
    >>> from src.core.grid import create_grid_state
    >>> from src.core.cooldowns import apply_cooldowns, tick_cooldowns
    >>> state = create_grid_state()
    >>> apply_cooldowns(state, 4, 6)
    >>> state.gcd
    10
    >>> state.cell_cd[4, 6]
    150
    >>> tick_cooldowns(state)
    >>> state.gcd
    9
    >>> state.cell_cd[4, 6]
    149
    >>> # After 10 ticks, GCD reaches 0
    >>> for _ in range(9):
    ...     tick_cooldowns(state)
    >>> state.gcd
    0
    >>> state.cell_cd[4, 6]  # Cell CD still active (140 frames remaining)
    140
    """
    # Decrement global cooldown if > 0 (scalar operation)
    if state.gcd > 0:
        state.gcd = state.gcd - np.uint16(1)

    # Decrement all cell cooldowns > 0 by 1 (vectorized, no Python loops)
    # Use np.where to prevent uint16 underflow (0 - 1 would wrap to 65535)
    state.cell_cd = np.where(
        state.cell_cd > 0, state.cell_cd - np.uint16(1), np.uint16(0)
    ).astype(COOLDOWN_DTYPE)
