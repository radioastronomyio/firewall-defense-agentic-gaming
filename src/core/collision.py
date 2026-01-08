#!/usr/bin/env python3
"""
Script Name  : collision.py
Description  : Vectorized collision detection for enemies and walls
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-08
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Vectorized collision detection for identifying which alive enemies occupy cells
with armed walls. This module implements the first step of collision resolution:
detecting collisions only. Damage application, wall destruction, and enemy death
marking are handled by subsequent functions in the collision module.

The detection uses advanced NumPy indexing to check all enemy positions against
the wall_armed grid in a single vectorized operation. No Python loops over
enemy slots are used, ensuring performance for training at >10k SPS.

Position System (Section 4)
---------------------------
- enemy_y_half: Half-cell y position (0-16 for grid height 9)
- enemy_x: Cell x position (0-12 for grid width 13)
- Cell lookup: cell_y = enemy_y_half // 2 (integer division)
- Example: y_half=1 maps to cell 0 (mid-cell), y_half=2 maps to cell 1

Collision Rules (Section 6.2)
------------------------------
- Only armed walls (wall_armed=True) trigger collisions
- Pending walls (wall_armed=False, wall_pending=True) do NOT trigger collisions
- Dead enemies (enemy_alive=False) cannot collide
- Multiple enemies on same armed wall cell all detected as colliding

Note
----
This module only detects collisions. Damage stacking, wall destruction, and
enemy death marking are handled by separate functions in the collision module
(Tasks 3.4.2-3.4.3).

Usage
-----
    from src.core.grid import create_grid_state
    from src.core.enemies import create_enemy_state
    from src.core.collision import detect_collisions

    grid_state = create_grid_state()
    enemy_state = create_enemy_state()

    # Place and arm a wall
    grid_state.grid[4, 6] = 1
    grid_state.wall_armed[4, 6] = True

    # Spawn enemy at (4, 6)
    enemy_state.enemy_alive[0] = True
    enemy_state.enemy_y_half[0] = 8  # cell 4
    enemy_state.enemy_x[0] = 6

    # Detect collisions
    collisions = detect_collisions(grid_state, enemy_state)
    # collisions[0] is True (enemy 0 on armed wall)
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.enemies import EnemyState
from src.core.grid import GridState

# =============================================================================
# Collision Detection
# =============================================================================


def detect_collisions(grid_state: GridState, enemy_state: EnemyState) -> np.ndarray:
    """
    Detect which alive enemies occupy cells with armed walls.

    This function performs vectorized collision detection by checking all enemy
    positions against the wall_armed grid in a single operation. Only alive
    enemies on cells with wall_armed=True are marked as colliding.

    The detection uses advanced NumPy indexing:
    1. Convert enemy_y_half to cell coordinates: cell_y = enemy_y_half // 2
    2. Look up wall_armed[cell_y, enemy_x] for all enemies
    3. Combine with enemy_alive mask (dead enemies cannot collide)
    4. Return boolean array with shape (MAX_ENEMIES,)

    Technical Details
    -----------------
    - Vectorized operation: No Python loops over enemy slots
    - Advanced indexing: grid_state.wall_armed[cell_y, enemy_x] checks all
      positions in single operation
    - Half-cell conversion: cell_y = enemy_y_half // 2 maps half-cell
      positions to integer cell coordinates
    - Masking: enemy_alive ensures dead slots return False
    - Return shape: Always (MAX_ENEMIES,) = (20,), dtype bool

    Parameters
    ----------
    grid_state : GridState
        Current grid state containing wall_armed array with shape (9, 13).
        Only cells with wall_armed=True trigger collisions.
    enemy_state : EnemyState
        Current enemy state containing positions and alive mask.
        enemy_y_half: Half-cell y positions (int16, shape 20)
        enemy_x: Cell x positions (int16, shape 20)
        enemy_alive: Active mask (bool, shape 20)

    Returns
    -------
    np.ndarray
        Boolean array with shape (MAX_ENEMIES,) = (20,).
        True at index i means enemy i is alive AND occupies a cell where
        wall_armed is True. False for dead enemies and enemies not on
        armed walls.

    Notes
    -----
    - Pending walls (wall_armed=False, wall_pending=True) do NOT trigger
      collisions. This is the anti-triviality rule from Section 5.4.
    - Multiple enemies on same armed wall cell all return True (damage
      stacking is handled by separate function in Task 3.4.2).
    - Dead enemies always return False regardless of position.
    - No bounds checking is performed—enemy positions are assumed to be
      within grid bounds (enemies are spawned within bounds and move
      downward only).

    Examples
    --------
    >>> from src.core.grid import create_grid_state
    >>> from src.core.enemies import create_enemy_state
    >>> from src.core.collision import detect_collisions
    >>> grid = create_grid_state()
    >>> enemies = create_enemy_state()
    >>> # Place and arm a wall at (4, 6)
    >>> grid.grid[4, 6] = 1
    >>> grid.wall_armed[4, 6] = True
    >>> # Spawn enemy at (4, 6)
    >>> enemies.enemy_alive[0] = True
    >>> enemies.enemy_y_half[0] = 8  # cell 4
    >>> enemies.enemy_x[0] = 6
    >>> collisions = detect_collisions(grid, enemies)
    >>> collisions[0]
    True
    >>> # Enemy on empty cell
    >>> enemies.enemy_alive[1] = True
    >>> enemies.enemy_y_half[1] = 4  # cell 2
    >>> enemies.enemy_x[1] = 3
    >>> collisions = detect_collisions(grid, enemies)
    >>> collisions[1]
    False
    >>> # Dead enemy (cannot collide)
    >>> enemies.enemy_alive[2] = False
    >>> enemies.enemy_y_half[2] = 8
    >>> enemies.enemy_x[2] = 6
    >>> collisions = detect_collisions(grid, enemies)
    >>> collisions[2]
    False
    >>> # Enemy on pending (unarmed) wall
    >>> grid.grid[5, 7] = 1
    >>> grid.wall_pending[5, 7] = True
    >>> grid.wall_armed[5, 7] = False
    >>> enemies.enemy_alive[3] = True
    >>> enemies.enemy_y_half[3] = 10  # cell 5
    >>> enemies.enemy_x[3] = 7
    >>> collisions = detect_collisions(grid, enemies)
    >>> collisions[3]
    False
    """
    # Convert half-cell y positions to cell coordinates
    # enemy_y_half stores vertical position in half-cells (0-16)
    # Cell lookup: cell_y = y_half // 2 (integer division)
    # Example: y_half=1 maps to cell 0, y_half=2 maps to cell 1
    cell_y = enemy_state.enemy_y_half // 2

    # Look up wall_armed at each enemy's cell position
    # Advanced indexing: grid_state.wall_armed[cell_y, enemy_x] returns
    # an array with shape (MAX_ENEMIES,) where each element is True if
    # that enemy's cell has an armed wall
    on_armed_wall = grid_state.wall_armed[cell_y, enemy_state.enemy_x]

    # Combine with enemy_alive mask: only alive enemies can collide
    # Logical AND: enemy must be alive AND on armed wall
    collisions = on_armed_wall & enemy_state.enemy_alive

    return collisions
