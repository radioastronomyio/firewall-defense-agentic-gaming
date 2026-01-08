#!/usr/bin/env python3
"""
Script Name  : test_collision.py
Description  : Unit tests for vectorized collision detection
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-08
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Comprehensive test suite for vectorized collision detection covering
basic scenarios, multiple enemies, half-cell position edge cases,
and return array properties.

Tests cover:
- Basic collision detection (no enemies, no walls, single enemy)
- Multiple enemy scenarios (some on walls, some not, same cell)
- Half-cell position edge cases (y_half=0, 1, 2, 17)
- Return array properties (shape, dtype, dead slots)

Reference: docs/design-document.md Sections 6.2, 10.1-10.2

Usage
-----
    pytest tests/unit/test_collision.py -v

Examples
--------
    pytest tests/unit/test_collision.py
        Run all collision detection tests

    pytest tests/unit/test_collision.py -k "basic"
        Run only basic collision scenarios

    pytest tests/unit/test_collision.py -k "half_cell"
        Run only half-cell edge case tests
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.collision import detect_collisions, detect_core_breach, resolve_collisions
from src.core.constants import EMPTY, MAX_ENEMIES
from src.core.enemies import create_enemy_state
from src.core.grid import create_grid_state

# =============================================================================
# Basic Collision Detection Tests
# =============================================================================


class TestDetectCollisionsBasic:
    """Test basic collision detection scenarios."""

    def test_no_enemies_alive_returns_all_false(self):
        """Verify detect_collisions returns all False when no enemies alive."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True

        # No enemies alive
        collisions = detect_collisions(grid, enemies)

        assert collisions.shape == (MAX_ENEMIES,), f"Shape should be ({MAX_ENEMIES},)"
        assert not collisions.any(), "All collisions should be False when no enemies alive"

    def test_no_armed_walls_returns_all_false(self):
        """Verify detect_collisions returns all False when no armed walls."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Spawn enemy
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        # No armed walls (grid is empty)
        collisions = detect_collisions(grid, enemies)

        assert not collisions.any(), "All collisions should be False when no armed walls"

    def test_single_enemy_on_armed_wall_returns_true(self):
        """Verify detect_collisions returns True for enemy on armed wall."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True

        # Spawn enemy at wall position
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "Enemy on armed wall should collide"
        assert not collisions[1:].any(), "Other slots should be False"

    def test_single_enemy_on_empty_cell_returns_false(self):
        """Verify detect_collisions returns False for enemy on empty cell."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Spawn enemy at empty cell
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == False, "Enemy on empty cell should not collide"

    def test_single_enemy_on_pending_wall_returns_false(self):
        """Verify detect_collisions returns False for enemy on pending (unarmed) wall."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place pending wall (not armed)
        grid.grid[4, 6] = 1
        grid.wall_pending[4, 6] = True
        grid.wall_armed[4, 6] = False

        # Spawn enemy at pending wall position
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == False, "Enemy on pending wall should not collide"


# =============================================================================
# Multiple Enemy Collision Tests
# =============================================================================


class TestDetectCollisionsMultiple:
    """Test multiple enemy collision scenarios."""

    def test_multiple_enemies_some_on_armed_walls(self):
        """Verify detect_collisions correctly identifies multiple collisions."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed walls at (4, 6) and (5, 7)
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.grid[5, 7] = 1
        grid.wall_armed[5, 7] = True

        # Spawn 3 enemies
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6  # On armed wall

        enemies.enemy_alive[1] = True
        enemies.enemy_y_half[1] = 10  # cell 5
        enemies.enemy_x[1] = 7  # On armed wall

        enemies.enemy_alive[2] = True
        enemies.enemy_y_half[2] = 4  # cell 2
        enemies.enemy_x[2] = 3  # On empty cell

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "Enemy 0 on armed wall should collide"
        assert collisions[1] == True, "Enemy 1 on armed wall should collide"
        assert collisions[2] == False, "Enemy 2 on empty cell should not collide"

    def test_multiple_enemies_on_same_armed_wall_cell(self):
        """Verify detect_collisions returns True for all enemies on same armed wall."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True

        # Spawn 3 enemies at same cell
        for i in range(3):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6  # Same column

        collisions = detect_collisions(grid, enemies)

        # All three should collide
        assert collisions[0] == True, "Enemy 0 should collide"
        assert collisions[1] == True, "Enemy 1 should collide"
        assert collisions[2] == True, "Enemy 2 should collide"

    def test_mix_of_alive_and_dead_enemies(self):
        """Verify detect_collisions only marks alive enemies as colliding."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True

        # Mix of alive and dead enemies at wall position
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8
        enemies.enemy_x[0] = 6

        enemies.enemy_alive[1] = False  # Dead
        enemies.enemy_y_half[1] = 8
        enemies.enemy_x[1] = 6

        enemies.enemy_alive[2] = True
        enemies.enemy_y_half[2] = 8
        enemies.enemy_x[2] = 6

        enemies.enemy_alive[3] = False  # Dead
        enemies.enemy_y_half[3] = 8
        enemies.enemy_x[3] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "Alive enemy 0 should collide"
        assert collisions[1] == False, "Dead enemy 1 should not collide"
        assert collisions[2] == True, "Alive enemy 2 should collide"
        assert collisions[3] == False, "Dead enemy 3 should not collide"

    def test_multiple_armed_walls_multiple_enemies(self):
        """Verify detect_collisions handles multiple armed walls and enemies."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place 3 armed walls
        for i, (y, x) in enumerate([(2, 3), (4, 6), (6, 9)]):
            grid.grid[y, x] = 1
            grid.wall_armed[y, x] = True

        # Spawn 5 enemies at various positions
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 4  # cell 2
        enemies.enemy_x[0] = 3  # On armed wall

        enemies.enemy_alive[1] = True
        enemies.enemy_y_half[1] = 8  # cell 4
        enemies.enemy_x[1] = 6  # On armed wall

        enemies.enemy_alive[2] = True
        enemies.enemy_y_half[2] = 12  # cell 6
        enemies.enemy_x[2] = 9  # On armed wall

        enemies.enemy_alive[3] = True
        enemies.enemy_y_half[3] = 6  # cell 3
        enemies.enemy_x[3] = 5  # Empty cell

        enemies.enemy_alive[4] = True
        enemies.enemy_y_half[4] = 10  # cell 5
        enemies.enemy_x[4] = 8  # Empty cell

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "Enemy 0 on armed wall should collide"
        assert collisions[1] == True, "Enemy 1 on armed wall should collide"
        assert collisions[2] == True, "Enemy 2 on armed wall should collide"
        assert collisions[3] == False, "Enemy 3 on empty cell should not collide"
        assert collisions[4] == False, "Enemy 4 on empty cell should not collide"


# =============================================================================
# Half-Cell Position Tests
# =============================================================================


class TestDetectCollisionsHalfCell:
    """Test half-cell position edge cases."""

    def test_enemy_at_y_half_zero_on_armed_wall(self):
        """Verify y_half=0 (cell 0) on armed wall collides."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall at top row
        grid.grid[0, 6] = 1
        grid.wall_armed[0, 6] = True

        # Spawn enemy at y_half=0 (cell 0)
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 0
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "y_half=0 on armed wall should collide"

    def test_enemy_at_y_half_one_on_armed_wall(self):
        """Verify y_half=1 (still cell 0) on armed wall collides."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall at top row
        grid.grid[0, 6] = 1
        grid.wall_armed[0, 6] = True

        # Spawn enemy at y_half=1 (mid-cell, still cell 0)
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 1
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "y_half=1 on armed wall should collide"

    def test_enemy_at_y_half_two_on_armed_wall(self):
        """Verify y_half=2 (cell 1) on armed wall collides."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall at row 1
        grid.grid[1, 6] = 1
        grid.wall_armed[1, 6] = True

        # Spawn enemy at y_half=2 (cell 1)
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 2
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "y_half=2 on armed wall should collide"

    def test_enemy_at_y_half_seventeen_on_armed_wall(self):
        """Verify y_half=17 (cell 8, bottom row) on armed wall collides."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall at bottom row
        grid.grid[8, 6] = 1
        grid.wall_armed[8, 6] = True

        # Spawn enemy at y_half=17 (cell 8)
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 17
        enemies.enemy_x[0] = 6

        collisions = detect_collisions(grid, enemies)

        assert collisions[0] == True, "y_half=17 on armed wall should collide"

    def test_half_cell_boundary_crossing(self):
        """Verify collision detection works across cell boundaries."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall at row 1
        grid.grid[1, 6] = 1
        grid.wall_armed[1, 6] = True

        # Test multiple y_half values that map to cell 1
        y_half_values = [2, 3]  # Both map to cell 1

        for i, y_half in enumerate(y_half_values):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = y_half
            enemies.enemy_x[i] = 6

        collisions = detect_collisions(grid, enemies)

        # Both should collide
        assert collisions[0] == True, "y_half=2 should collide"
        assert collisions[1] == True, "y_half=3 should collide"

    def test_half_cell_conversion_correctness(self):
        """Verify cell lookup uses integer division correctly."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed walls at rows 0, 1, 2
        for y in [0, 1, 2]:
            grid.grid[y, 6] = 1
            grid.wall_armed[y, 6] = True

        # Test y_half values and expected cells
        test_cases = [
            (0, 0),  # y_half=0 -> cell 0
            (1, 0),  # y_half=1 -> cell 0
            (2, 1),  # y_half=2 -> cell 1
            (3, 1),  # y_half=3 -> cell 1
            (4, 2),  # y_half=4 -> cell 2
            (5, 2),  # y_half=5 -> cell 2
        ]

        for i, (y_half, expected_cell) in enumerate(test_cases):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = y_half
            enemies.enemy_x[i] = 6

        collisions = detect_collisions(grid, enemies)

        # All should collide (all on armed walls)
        for i in range(len(test_cases)):
            assert collisions[i] == True, f"y_half={test_cases[i][0]} should collide at cell {expected_cell}"


# =============================================================================
# Return Array Properties Tests
# =============================================================================


class TestDetectCollisionsReturnShape:
    """Validate return array properties."""

    def test_return_shape_is_always_max_enemies(self):
        """Verify return shape is always (MAX_ENEMIES,) regardless of alive count."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Test with 0 alive enemies
        collisions = detect_collisions(grid, enemies)
        assert collisions.shape == (MAX_ENEMIES,), f"Shape should be ({MAX_ENEMIES},)"

        # Test with 1 alive enemy
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8
        enemies.enemy_x[0] = 6
        collisions = detect_collisions(grid, enemies)
        assert collisions.shape == (MAX_ENEMIES,), f"Shape should be ({MAX_ENEMIES},)"

        # Test with 10 alive enemies (keep positions within grid bounds)
        for i in range(10):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = i   # Use i instead of i*2 to stay within bounds
            enemies.enemy_x[i] = i % 13
        collisions = detect_collisions(grid, enemies)
        assert collisions.shape == (MAX_ENEMIES,), f"Shape should be ({MAX_ENEMIES},)"

    def test_return_dtype_is_bool(self):
        """Verify return array dtype is bool."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        collisions = detect_collisions(grid, enemies)

        assert collisions.dtype == np.bool_, f"Return dtype should be bool_, got {collisions.dtype}"

    def test_dead_enemy_slots_always_false(self):
        """Verify dead enemy slots always return False regardless of position."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True

        # Set all enemies to wall position, but only mark some as alive
        for i in range(10):
            enemies.enemy_y_half[i] = 8
            enemies.enemy_x[i] = 6

        enemies.enemy_alive[0] = True
        enemies.enemy_alive[2] = True
        enemies.enemy_alive[4] = True
        enemies.enemy_alive[6] = True
        enemies.enemy_alive[8] = True
        # Slots 1, 3, 5, 7, 9 are dead

        collisions = detect_collisions(grid, enemies)

        # Alive slots should be True
        assert collisions[0] == True, "Alive slot 0 should collide"
        assert collisions[2] == True, "Alive slot 2 should collide"
        assert collisions[4] == True, "Alive slot 4 should collide"
        assert collisions[6] == True, "Alive slot 6 should collide"
        assert collisions[8] == True, "Alive slot 8 should collide"

        # Dead slots should be False
        assert collisions[1] == False, "Dead slot 1 should not collide"
        assert collisions[3] == False, "Dead slot 3 should not collide"
        assert collisions[5] == False, "Dead slot 5 should not collide"
        assert collisions[7] == False, "Dead slot 7 should not collide"
        assert collisions[9] == False, "Dead slot 9 should not collide"

    def test_all_slots_false_when_no_collisions(self):
        """Verify all slots are False when no collisions occur."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Spawn multiple enemies on empty cells
        for i in range(5):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = i * 2
            enemies.enemy_x[i] = i

        collisions = detect_collisions(grid, enemies)

        assert not collisions.any(), "All slots should be False when no collisions"

    def test_all_slots_true_when_all_on_armed_walls(self):
        """Verify all alive slots are True when all on armed walls."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place armed walls for each enemy
        for i in range(5):
            y = i * 2
            x = i
            grid.grid[y, x] = 1
            grid.wall_armed[y, x] = True

            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = y * 2  # cell y
            enemies.enemy_x[i] = x

        collisions = detect_collisions(grid, enemies)

        # First 5 should be True
        for i in range(5):
            assert collisions[i] == True, f"Enemy {i} on armed wall should collide"

        # Rest should be False (dead)
        for i in range(5, MAX_ENEMIES):
            assert collisions[i] == False, f"Dead slot {i} should not collide"


# =============================================================================
# Collision Resolution Tests - Single Hit
# =============================================================================


class TestResolveCollisionsSingleHit:
    """Test single enemy collision scenarios."""

    def test_single_enemy_on_wall_kills_enemy_damages_wall(self):
        """Verify single enemy colliding with wall: enemy dies, wall takes 1 damage."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=3
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 3

        # Spawn enemy at wall position
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 1, "Should kill 1 enemy"
        assert walls_destroyed == 0, "Should not destroy wall (HP=3, damage=1)"
        assert enemies.enemy_alive[0] == False, "Enemy should be dead"
        assert grid.wall_hp[4, 6] == 2, "Wall HP should decrement from 3 to 2"

    def test_enemy_on_empty_cell_no_collision(self):
        """Verify enemy on empty cell: no state change."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Spawn enemy at empty cell
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 0, "Should kill 0 enemies"
        assert walls_destroyed == 0, "Should destroy 0 walls"
        assert enemies.enemy_alive[0] == True, "Enemy should still be alive"
        assert grid.wall_hp[4, 6] == 0, "Wall HP should remain 0 (no wall)"

    def test_wall_hp_decrements_correctly(self):
        """Verify wall HP decrements correctly (HP=3 -> HP=2 after 1 hit)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=3
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 3

        # Spawn enemy at wall position
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8  # cell 4
        enemies.enemy_x[0] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        resolve_collisions(grid, enemies, collisions)

        assert grid.wall_hp[4, 6] == 2, "Wall HP should decrement from 3 to 2"


# =============================================================================
# Collision Resolution Tests - Multi-Hit (Damage Stacking)
# =============================================================================


class TestResolveCollisionsMultiHit:
    """Test damage stacking with multiple enemies on same wall."""

    def test_two_enemies_same_cell_wall_takes_two_damage(self):
        """Verify 2 enemies same cell: wall takes 2 damage, both enemies die."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=3
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 3

        # Spawn 2 enemies at same wall position
        for i in range(2):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 2, "Should kill 2 enemies"
        assert walls_destroyed == 0, "Should not destroy wall (HP=3, damage=2)"
        assert enemies.enemy_alive[0] == False, "Enemy 0 should be dead"
        assert enemies.enemy_alive[1] == False, "Enemy 1 should be dead"
        assert grid.wall_hp[4, 6] == 1, "Wall HP should decrement from 3 to 1"

    def test_three_enemies_same_cell_wall_takes_three_damage(self):
        """Verify 3 enemies same cell: wall takes 3 damage, all enemies die."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=3
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 3

        # Spawn 3 enemies at same wall position
        for i in range(3):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 3, "Should kill 3 enemies"
        assert walls_destroyed == 1, "Should destroy wall (HP=3, damage=3)"
        assert all(enemies.enemy_alive[0:3] == False), "All 3 enemies should be dead"
        assert grid.wall_hp[4, 6] == 0, "Wall HP should be 0 (destroyed)"
        assert grid.grid[4, 6] == EMPTY, "Grid cell should be EMPTY"
        assert grid.wall_armed[4, 6] == False, "Wall armed should be False"

    def test_multiple_enemies_different_walls_independent_damage(self):
        """Verify multiple enemies on different walls: each wall damaged independently."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm 2 walls with HP=2
        for i, (y, x) in enumerate([(3, 4), (5, 7)]):
            grid.grid[y, x] = 1
            grid.wall_armed[y, x] = True
            grid.wall_hp[y, x] = 2

        # Spawn 2 enemies, each on different wall
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 6  # cell 3
        enemies.enemy_x[0] = 4

        enemies.enemy_alive[1] = True
        enemies.enemy_y_half[1] = 10  # cell 5
        enemies.enemy_x[1] = 7

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 2, "Should kill 2 enemies"
        assert walls_destroyed == 0, "Should not destroy walls (HP=2, damage=1 each)"
        assert grid.wall_hp[3, 4] == 1, "Wall at (3,4) HP should decrement from 2 to 1"
        assert grid.wall_hp[5, 7] == 1, "Wall at (5,7) HP should decrement from 2 to 1"


# =============================================================================
# Collision Resolution Tests - Wall Destruction
# =============================================================================


class TestResolveCollisionsWallDestruction:
    """Test wall destruction scenarios."""

    def test_wall_destroyed_when_damage_equals_hp(self):
        """Verify wall destroyed when damage >= HP (HP=2, 2 enemies -> destroyed)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=2
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 2

        # Spawn 2 enemies at wall position
        for i in range(2):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 2, "Should kill 2 enemies"
        assert walls_destroyed == 1, "Should destroy 1 wall"
        assert grid.wall_hp[4, 6] == 0, "Wall HP should be 0"
        assert grid.grid[4, 6] == EMPTY, "Grid cell should be EMPTY"
        assert grid.wall_armed[4, 6] == False, "Wall armed should be False"
        assert grid.wall_pending[4, 6] == False, "Wall pending should be False"

    def test_wall_survives_when_damage_less_than_hp(self):
        """Verify wall survives when damage < HP (HP=3, 2 enemies -> HP=1)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=3
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 3

        # Spawn 2 enemies at wall position
        for i in range(2):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 2, "Should kill 2 enemies"
        assert walls_destroyed == 0, "Should not destroy wall (HP=3, damage=2)"
        assert grid.wall_hp[4, 6] == 1, "Wall HP should be 1"
        assert grid.grid[4, 6] == 1, "Grid cell should still be WALL"
        assert grid.wall_armed[4, 6] == True, "Wall armed should still be True"

    def test_destruction_clears_all_wall_state(self):
        """Verify destruction clears all wall state: grid=EMPTY, wall_hp=0, armed=False, pending=False."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=2
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_pending[4, 6] = True  # Also test pending flag
        grid.wall_hp[4, 6] = 2

        # Spawn 2 enemies at wall position
        for i in range(2):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        resolve_collisions(grid, enemies, collisions)

        assert grid.grid[4, 6] == EMPTY, "Grid cell should be EMPTY"
        assert grid.wall_hp[4, 6] == 0, "Wall HP should be 0"
        assert grid.wall_armed[4, 6] == False, "Wall armed should be False"
        assert grid.wall_pending[4, 6] == False, "Wall pending should be False"

    def test_uint8_safety_no_underflow_when_damage_exceeds_hp(self):
        """Verify uint8 safety: no underflow when damage > HP (HP=1, 3 enemies -> HP clamps to 0)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall with HP=1
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 1

        # Spawn 3 enemies at wall position (damage=3, HP=1)
        for i in range(3):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 8  # cell 4
            enemies.enemy_x[i] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 3, "Should kill 3 enemies"
        assert walls_destroyed == 1, "Should destroy 1 wall"
        assert grid.wall_hp[4, 6] == 0, "Wall HP should clamp to 0 (no underflow)"
        assert grid.grid[4, 6] == EMPTY, "Grid cell should be EMPTY"


# =============================================================================
# Collision Resolution Tests - Return Values
# =============================================================================


class TestResolveCollisionsReturnValues:
    """Test return values from resolve_collisions()."""

    def test_return_tuple_shape(self):
        """Verify return tuple shape: (enemies_killed, walls_destroyed)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm wall
        grid.grid[4, 6] = 1
        grid.wall_armed[4, 6] = True
        grid.wall_hp[4, 6] = 2

        # Spawn enemy
        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 8
        enemies.enemy_x[0] = 6

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        result = resolve_collisions(grid, enemies, collisions)

        assert isinstance(result, tuple), "Return value should be tuple"
        assert len(result) == 2, "Return tuple should have 2 elements"
        assert isinstance(result[0], int), "First element should be int"
        assert isinstance(result[1], int), "Second element should be int"

    def test_return_values_match_actual_mutations(self):
        """Verify return values match actual state mutations."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm 2 walls with different HP
        grid.grid[3, 4] = 1
        grid.wall_armed[3, 4] = True
        grid.wall_hp[3, 4] = 3  # Survives 2 hits

        grid.grid[5, 7] = 1
        grid.wall_armed[5, 7] = True
        grid.wall_hp[5, 7] = 2  # Destroyed by 2 hits

        # Spawn 4 enemies: 2 on each wall
        for i in range(2):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 6  # cell 3
            enemies.enemy_x[i] = 4

        for i in range(2, 4):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = 10  # cell 5
            enemies.enemy_x[i] = 7

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        # Verify return values
        assert enemies_killed == 4, "Return value should indicate 4 enemies killed"

        # Verify actual mutations match return values
        actual_enemies_killed = int(np.sum(~enemies.enemy_alive[0:4]))
        actual_walls_destroyed = int(
            (grid.grid[3, 4] == EMPTY) + (grid.grid[5, 7] == EMPTY)
        )
        assert enemies_killed == actual_enemies_killed, "Return value should match actual enemies killed"
        assert walls_destroyed == actual_walls_destroyed, "Return value should match actual walls destroyed"

    def test_no_collisions_returns_zero_zero(self):
        """Verify no collisions returns (0, 0)."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Spawn enemies on empty cells
        for i in range(3):
            enemies.enemy_alive[i] = True
            enemies.enemy_y_half[i] = i * 2
            enemies.enemy_x[i] = i

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 0, "Should kill 0 enemies"
        assert walls_destroyed == 0, "Should destroy 0 walls"
        assert (enemies_killed, walls_destroyed) == (0, 0), "Return should be (0, 0)"

    def test_multiple_walls_destroyed_returns_correct_count(self):
        """Verify multiple walls destroyed returns correct count."""
        grid = create_grid_state()
        enemies = create_enemy_state()

        # Place and arm 3 walls with HP=2
        for i, (y, x) in enumerate([(2, 3), (4, 6), (6, 9)]):
            grid.grid[y, x] = 1
            grid.wall_armed[y, x] = True
            grid.wall_hp[y, x] = 2

        # Spawn 2 enemies on each wall (6 total)
        for i, (y, x) in enumerate([(2, 3), (4, 6), (6, 9)]):
            enemies.enemy_alive[i * 2] = True
            enemies.enemy_y_half[i * 2] = y * 2
            enemies.enemy_x[i * 2] = x

            enemies.enemy_alive[i * 2 + 1] = True
            enemies.enemy_y_half[i * 2 + 1] = y * 2
            enemies.enemy_x[i * 2 + 1] = x

        # Detect and resolve collisions
        collisions = detect_collisions(grid, enemies)
        enemies_killed, walls_destroyed = resolve_collisions(grid, enemies, collisions)

        assert enemies_killed == 6, "Should kill 6 enemies"
        assert walls_destroyed == 3, "Should destroy 3 walls"
        assert grid.grid[2, 3] == EMPTY, "Wall at (2,3) should be destroyed"
        assert grid.grid[4, 6] == EMPTY, "Wall at (4,6) should be destroyed"
        assert grid.grid[6, 9] == EMPTY, "Wall at (6,9) should be destroyed"


# =============================================================================
# Core Breach Detection Tests
# =============================================================================


class TestDetectCoreBreach:
    """Test core breach detection scenarios."""

    def test_y_half_fifteen_no_breach(self):
        """Verify y_half=15 (row 7): no breach."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 15  # Row 7, one above core

        breach = detect_core_breach(enemies)

        assert breach == False, "y_half=15 should not breach"

    def test_y_half_sixteen_breach_detected(self):
        """Verify y_half=16 (row 8, threshold): breach detected."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 16  # Row 8, core row

        breach = detect_core_breach(enemies)

        assert breach == True, "y_half=16 should breach"

    def test_y_half_seventeen_beyond_threshold(self):
        """Verify y_half=17 (beyond threshold): breach detected."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 17  # Beyond core

        breach = detect_core_breach(enemies)

        assert breach == True, "y_half=17 should breach"

    def test_dead_enemy_at_threshold_no_breach(self):
        """Verify dead enemy at threshold: no breach (dead enemies ignored)."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = False  # Dead
        enemies.enemy_y_half[0] = 16  # At threshold

        breach = detect_core_breach(enemies)

        assert breach == False, "Dead enemy should not trigger breach"

    def test_multiple_enemies_only_one_breached(self):
        """Verify multiple enemies, only one breached: breach detected."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 10  # Safe

        enemies.enemy_alive[1] = True
        enemies.enemy_y_half[1] = 16  # Breached

        enemies.enemy_alive[2] = True
        enemies.enemy_y_half[2] = 12  # Safe

        breach = detect_core_breach(enemies)

        assert breach == True, "One breached enemy should trigger breach"

    def test_no_alive_enemies_no_breach(self):
        """Verify no alive enemies: no breach."""
        enemies = create_enemy_state()

        # All enemies dead
        for i in range(5):
            enemies.enemy_alive[i] = False
            enemies.enemy_y_half[i] = 16  # Even at threshold

        breach = detect_core_breach(enemies)

        assert breach == False, "No alive enemies should not breach"

    def test_return_type_is_bool(self):
        """Verify return type is bool."""
        enemies = create_enemy_state()

        enemies.enemy_alive[0] = True
        enemies.enemy_y_half[0] = 16

        breach = detect_core_breach(enemies)

        assert isinstance(breach, bool), "Return type should be bool"
        assert breach == True, "Should return True for breach"
