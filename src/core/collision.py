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
Vectorized collision detection and resolution for enemies and walls. This module
implements the complete collision pipeline:
1. detect_collisions() - Identify which enemies occupy cells with armed walls
2. resolve_collisions() - Apply damage, destroy walls, mark enemies dead
3. detect_core_breach() - Check if any alive enemy reached the bottom row

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
This module implements the complete collision pipeline including wall-enemy
collisions and core breach detection (enemies reaching bottom row).

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

from src.core.constants import CORE_Y_HALF, EMPTY
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


# =============================================================================
# Collision Resolution
# =============================================================================


def resolve_collisions(
    grid_state: GridState,
    enemy_state: EnemyState,
    collisions: np.ndarray,
) -> tuple[int, int]:
    """
    Resolve collision damage, wall destruction, and enemy death.

    This function applies damage from colliding enemies to walls, destroys
    walls when HP reaches zero, and marks colliding enemies as dead. Damage
    stacks cumulatively when multiple enemies collide with the same wall cell.

    The resolution uses vectorized NumPy operations to count damage per cell
    and apply wall destruction in a single pass, ensuring performance for
    training at >10k SPS.

    Damage Stacking Logic
    ---------------------
    - Multiple enemies on same cell deal cumulative damage
    - Vectorized counting: np.add.at() counts enemies per (cell_y, x) pair
    - Cell lookup: cell_y = enemy_y_half // 2
    - Example: 3 enemies on same wall cell = 3 damage to that wall

    Wall Destruction
    ----------------
    - wall_hp[y, x] -= damage_count (applied cumulatively)
    - When wall_hp[y, x] <= 0:
        - grid[y, x] = EMPTY
        - wall_hp[y, x] = 0
        - wall_armed[y, x] = False
        - wall_pending[y, x] = False
    - Only walls with HP <= 0 are destroyed

    Enemy Death
    -----------
    - All enemies marked True in collisions array: enemy_alive[collisions] = False
    - This is a vectorized boolean assignment

    Technical Details
    -----------------
    - Vectorized damage counting: np.add.at() accumulates damage per cell
    - Vectorized wall destruction: boolean indexing finds walls to destroy
    - Vectorized enemy death: boolean indexing marks colliding enemies dead
    - In-place mutation: All state arrays modified directly
    - No Python loops over enemies or cells

    Parameters
    ----------
    grid_state : GridState
        Current grid state containing wall arrays. Mutated in-place.
        grid: Cell contents (0=empty, 1=wall)
        wall_hp: Wall health points (uint8)
        wall_armed: Armed status (bool)
        wall_pending: Pending status (bool)
    enemy_state : EnemyState
        Current enemy state containing positions and alive mask. Mutated in-place.
        enemy_y_half: Half-cell y positions (int16, shape 20)
        enemy_x: Cell x positions (int16, shape 20)
        enemy_alive: Active mask (bool, shape 20)
    collisions : np.ndarray
        Boolean array with shape (MAX_ENEMIES,) = (20,). True at index i
        means enemy i collides with an armed wall. Output from detect_collisions().

    Returns
    -------
    tuple[int, int]
        (enemies_killed, walls_destroyed) for reward calculation.
        - enemies_killed: Number of enemies marked dead (sum of collisions)
        - walls_destroyed: Number of walls destroyed (HP <= 0 after damage)

    Notes
    -----
    - Damage is applied cumulatively: 3 enemies on same wall = 3 damage
    - Walls with HP > 0 after damage remain intact
    - Dead enemies cannot collide (enforced by detect_collisions())
    - Only armed walls can be damaged (enforced by detect_collisions())
    - Core breach detection is handled separately (Task 3.4.3)

    Examples
    --------
    >>> from src.core.grid import create_grid_state
    >>> from src.core.enemies import create_enemy_state
    >>> from src.core.collision import detect_collisions, resolve_collisions
    >>> grid = create_grid_state()
    >>> enemies = create_enemy_state()
    >>> # Place and arm a wall at (4, 6)
    >>> grid.grid[4, 6] = 1
    >>> grid.wall_armed[4, 6] = True
    >>> grid.wall_hp[4, 6] = 2
    >>> # Spawn 3 enemies at (4, 6)
    >>> enemies.enemy_alive[0:3] = True
    >>> enemies.enemy_y_half[0:3] = 8  # cell 4
    >>> enemies.enemy_x[0:3] = 6
    >>> # Detect and resolve collisions
    >>> collisions = detect_collisions(grid, enemies)
    >>> enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)
    >>> enemies_killed
    3
    >>> walls_destroyed
    1
    >>> grid.wall_hp[4, 6]  # Wall destroyed, HP clamped to 0
    0
    >>> grid.grid[4, 6]  # Wall removed
    0
    >>> grid.wall_armed[4, 6]
    False
    >>> # Another wall with higher HP
    >>> grid2 = create_grid_state()
    >>> enemies2 = create_enemy_state()
    >>> grid2.grid[3, 5] = 1
    >>> grid2.wall_armed[3, 5] = True
    >>> grid2.wall_hp[3, 5] = 3  # HP=3, can survive 2 hits
    >>> enemies2.enemy_alive[0:2] = True  # 2 enemies
    >>> enemies2.enemy_y_half[0:2] = 6  # cell 3
    >>> enemies2.enemy_x[0:2] = 5
    >>> collisions2 = detect_collisions(grid2, enemies2)
    >>> enemies_killed, walls_destroyed = resolve_collisions(grid2, enemies2, collisions2)
    >>> enemies_killed
    2
    >>> walls_destroyed  # Wall survives with HP=1
    0
    >>> grid2.wall_hp[3, 5]  # 3 - 2 = 1
    1
    >>> # No collisions = no changes
    >>> grid3 = create_grid_state()
    >>> enemies3 = create_enemy_state()
    >>> collisions3 = detect_collisions(grid3, enemies3)
    >>> enemies_killed, walls_destroyed = resolve_collisions(grid3, enemies3, collisions3)
    >>> enemies_killed, walls_destroyed
    (0, 0)
    """
    # Mark all colliding enemies as dead (vectorized boolean assignment)
    # This is a simple in-place operation: set enemy_alive to False where
    # collisions is True
    enemy_state.enemy_alive[collisions] = False

    # Count enemies killed (sum of collisions boolean array)
    # This is the number of enemies marked dead above
    enemies_killed = int(np.sum(collisions))

    # If no enemies collided, no damage to apply
    if enemies_killed == 0:
        return 0, 0

    # Convert half-cell y positions to cell coordinates
    # enemy_y_half stores vertical position in half-cells (0-16)
    # Cell lookup: cell_y = y_half // 2 (integer division)
    cell_y = enemy_state.enemy_y_half // 2

    # Get positions of colliding enemies only
    # We only need to count damage for enemies that actually collided
    colliding_cell_y = cell_y[collisions]
    colliding_x = enemy_state.enemy_x[collisions]

    # Count damage per cell using np.add.at()
    # This accumulates damage for each (cell_y, x) coordinate pair
    # Initialize damage array with zeros (same shape as grid)
    damage = np.zeros((9, 13), dtype=np.int8)

    # Accumulate damage: for each colliding enemy, add 1 to damage[cell_y, x]
    # np.add.at handles duplicate indices correctly (cumulative addition)
    np.add.at(damage, (colliding_cell_y, colliding_x), 1)

    # Find walls destroyed: damage >= current HP (and wall exists)
    # AI NOTE: wall_hp is uint8, so direct subtraction would underflow.
    # We compare damage to HP first to identify destroyed walls, then
    # use signed arithmetic for the actual HP update.
    destroyed = (damage > 0) & (damage >= grid_state.wall_hp)

    # Apply damage using signed arithmetic to avoid uint8 underflow
    # Cast to int16, subtract, clamp to 0 minimum, cast back to uint8
    new_hp = grid_state.wall_hp.astype(np.int16) - damage
    new_hp = np.maximum(new_hp, 0)
    grid_state.wall_hp = new_hp.astype(np.uint8)

    # Count walls destroyed
    walls_destroyed = int(np.sum(destroyed))

    # Clear destroyed walls (vectorized assignment)
    # Set grid to EMPTY for all destroyed walls
    grid_state.grid[destroyed] = EMPTY

    # Reset wall_hp to 0 for destroyed walls
    grid_state.wall_hp[destroyed] = 0

    # Clear armed status for destroyed walls
    grid_state.wall_armed[destroyed] = False

    # Clear pending status for destroyed walls
    grid_state.wall_pending[destroyed] = False

    return enemies_killed, walls_destroyed


# =============================================================================
# Core Breach Detection
# =============================================================================


def detect_core_breach(enemy_state: EnemyState) -> bool:
    """
    Check if any alive enemy has breached the core (reached bottom).

    A core breach occurs when any alive enemy reaches or exceeds the
    CORE_Y_HALF threshold (16 half-cells, corresponding to row 8 at the
    bottom of the grid). This is a game-ending condition—a single breach
    terminates the episode with a negative reward.

    The detection is vectorized for performance, checking all alive enemies
    in a single NumPy operation without Python loops.

    Technical Details
    -----------------
    - Breach threshold: CORE_Y_HALF = 16 (from constants.py)
    - Grid height: 9 rows = 18 half-cells (0-17)
    - Core row: Row 8 (bottom row) starts at y_half = 16
    - Vectorized check: enemy_state.enemy_y_half[enemy_state.enemy_alive] >= CORE_Y_HALF
    - Aggregation: np.any() returns True if any alive enemy meets condition
    - No bounds checking: Enemy movement is constrained to grid bounds
    - In-place read: enemy_state is not modified (read-only operation)

    Position System Context
    -----------------------
    - enemy_y_half stores vertical position in half-cells (0-16 for grid height 9)
    - Cell lookup: cell_y = enemy_y_half // 2
    - Example: y_half=15 maps to cell 7, y_half=16 maps to cell 8 (core row)
    - Breach occurs when enemy reaches y_half >= 16 (row 8 or beyond)

    Parameters
    ----------
    enemy_state : EnemyState
        Current enemy state containing positions and alive mask.
        enemy_y_half: Half-cell y positions (int16, shape 20)
        enemy_alive: Active mask (bool, shape 20)

    Returns
    -------
    bool
        True if any alive enemy has enemy_y_half >= CORE_Y_HALF (16),
        False otherwise. A single breach ends the episode.

    Notes
    -----
    - Only alive enemies are checked (dead slots ignored via boolean indexing)
    - The check is inclusive: y_half == 16 counts as a breach
    - This function is called once per tick during the simulation step loop
    - Core breach is checked after collision resolution (Task 3.5.1)
    - A single breach immediately terminates the episode with reward -1.0

    Examples
    --------
    >>> from src.core.enemies import create_enemy_state
    >>> from src.core.collision import detect_core_breach
    >>> enemies = create_enemy_state()
    >>> # Enemy not breached yet
    >>> enemies.enemy_alive[0] = True
    >>> enemies.enemy_y_half[0] = 15  # Row 7, one row above core
    >>> detect_core_breach(enemies)
    False
    >>> # Enemy at breach threshold
    >>> enemies.enemy_y_half[0] = 16  # Row 8, core row
    >>> detect_core_breach(enemies)
    True
    >>> # Enemy past breach
    >>> enemies.enemy_y_half[0] = 17  # Beyond core
    >>> detect_core_breach(enemies)
    True
    >>> # Dead enemy (cannot breach)
    >>> enemies.enemy_alive[0] = False
    >>> enemies.enemy_y_half[0] = 16
    >>> detect_core_breach(enemies)
    False
    >>> # Multiple enemies, one breached
    >>> enemies.enemy_alive[0:2] = True
    >>> enemies.enemy_y_half[0] = 10  # Safe
    >>> enemies.enemy_y_half[1] = 16  # Breached
    >>> detect_core_breach(enemies)
    True
    """
    # Check if any alive enemy has reached or exceeded CORE_Y_HALF
    # Boolean indexing: enemy_state.enemy_alive selects only alive enemies
    # Comparison: >= CORE_Y_HALF checks breach condition
    # Aggregation: np.any() returns True if any alive enemy meets condition
    return bool(np.any(enemy_state.enemy_y_half[enemy_state.enemy_alive] >= CORE_Y_HALF))
