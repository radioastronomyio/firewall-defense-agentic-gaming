#!/usr/bin/env python3
"""
Script Name  : walls.py
Description  : Wall placement and validity checks
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Wall placement logic with comprehensive validity checks. This module
implements the anti-triviality rule (1-tick arming delay) and enforces
cooldown constraints that force the agent to commit to geometric decisions.

Placement Rules (Section 5.3-5.4)
---------------------------------
- Bounds check: y and x must be within grid dimensions
- Global cooldown: GCD must be 0 (action allowed)
- Cell cooldown: cell_cd[y, x] must be 0 (cell not in cooldown)
- Occupancy check: grid[y, x] must not already contain a wall
- On valid placement: wall is placed with pending status (not armed)
- Invalid placements return False without mutating state

Arming Delay (Anti-Triviality)
-------------------------------
Freshly placed walls are marked as pending (wall_pending=True, wall_armed=False)
and cannot kill enemies until the next tick. This prevents the agent from
reactively placing walls on top of enemies and forces prediction.

Note
----
This module does NOT set GCD or cell_cd values. Cooldown application is
handled by the step loop in the simulation module (Task 3.2.2).

Usage
-----
    from src.core.grid import create_grid_state
    from src.core.walls import place_wall

    state = create_grid_state()
    success = place_wall(state, y=4, x=6)

    if success:
        # Wall placed at (4, 6), pending arming
        assert state.grid[4, 6] == 1
        assert state.wall_pending[4, 6] == True
        assert state.wall_armed[4, 6] == False
    else:
        # Placement failed, state unchanged
"""

# =============================================================================
# Imports
# =============================================================================

from src.core.constants import DEFAULT_WALL_HP, HEIGHT, WALL, WIDTH
from src.core.grid import GridState

# =============================================================================
# Wall Placement
# =============================================================================


def place_wall(state: GridState, y: int, x: int) -> bool:
    """
    Place a wall at the specified cell coordinates with validity checks.

    This function validates all placement constraints before mutating state.
    Invalid placements return False immediately without any state changes.

    Validity Checks
    ---------------
    1. Bounds: 0 <= y < HEIGHT and 0 <= x < WIDTH
    2. Global cooldown: state.gcd == 0
    3. Cell cooldown: state.cell_cd[y, x] == 0
    4. Occupancy: state.grid[y, x] != WALL

    State Mutation (on valid placement)
    ------------------------------------
    - state.grid[y, x] = WALL
    - state.wall_hp[y, x] = DEFAULT_WALL_HP
    - state.wall_pending[y, x] = True
    - state.wall_armed[y, x] = False

    Parameters
    ----------
    state : GridState
        Current grid state to modify. Mutated in-place on valid placement.
    y : int
        Row index (0 to HEIGHT-1). Uses [y, x] indexing convention.
    x : int
        Column index (0 to WIDTH-1). Uses [y, x] indexing convention.

    Returns
    -------
    bool
        True if wall was placed successfully, False if placement invalid.

    Notes
    -----
    - No state mutation occurs on invalid placement
    - GCD and cell_cd values are NOT set by this function (see Task 3.2.2)
    - The arming delay (pending → armed transition) is handled by the step loop

    Examples
    --------
    >>> from src.core.grid import create_grid_state
    >>> state = create_grid_state()
    >>> place_wall(state, 4, 6)
    True
    >>> state.grid[4, 6]
    1
    >>> place_wall(state, 4, 6)  # Cell already occupied
    False
    >>> state.gcd = 5  # Set global cooldown
    >>> place_wall(state, 5, 7)  # GCD blocks placement
    False
    """
    # Bounds check: y and x must be within grid dimensions
    if y < 0 or y >= HEIGHT or x < 0 or x >= WIDTH:
        return False

    # Global cooldown check: action only allowed when GCD is 0
    if state.gcd != 0:
        return False

    # Cell cooldown check: cell must not be in cooldown
    if state.cell_cd[y, x] != 0:
        return False

    # Occupancy check: cell must not already contain a wall
    if state.grid[y, x] == WALL:
        return False

    # All checks passed - place wall with pending status (arming delay)
    state.grid[y, x] = WALL
    state.wall_hp[y, x] = DEFAULT_WALL_HP
    state.wall_pending[y, x] = True
    state.wall_armed[y, x] = False

    return True
