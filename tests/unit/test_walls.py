#!/usr/bin/env python3
"""
Script Name  : test_walls.py
Description  : Unit tests for wall placement, arming, and cooldown lifecycle
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Comprehensive test suite for wall lifecycle covering placement validity,
cooldown blocking, arming delay, and state mutations.

Tests cover:
- Placement validity (bounds, occupancy, cooldowns)
- State mutations on valid placement
- Cooldown blocking (GCD and cell_cd)
- Arming lifecycle (pending → armed transition)
- Cooldown application and decrement

Reference: docs/design-document.md Sections 5.1-5.4, 6

Usage
-----
    pytest tests/unit/test_walls.py -v

Examples
--------
    pytest tests/unit/test_walls.py
        Run all wall lifecycle tests

    pytest tests/unit/test_walls.py -k "placement"
        Run only placement validity tests

    pytest tests/unit/test_walls.py -k "arming"
        Run only arming lifecycle tests
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.constants import (
    CELL_CD_FRAMES,
    DEFAULT_WALL_HP,
    GCD_FRAMES,
    HEIGHT,
    WALL,
    WIDTH,
)
from src.core.cooldowns import apply_cooldowns, tick_cooldowns
from src.core.grid import create_grid_state
from src.core.walls import arm_pending_walls, place_wall

# =============================================================================
# Placement Validity Tests
# =============================================================================


class TestPlacementValidity:
    """Test wall placement validity checks."""

    def test_place_wall_accepts_valid_placement(self):
        """Verify place_wall returns True for valid placement."""
        state = create_grid_state()
        success = place_wall(state, y=4, x=6)
        assert success is True, "Valid placement should return True"

    def test_place_wall_rejects_negative_y_coordinate(self):
        """Verify place_wall rejects negative y coordinate."""
        state = create_grid_state()
        success = place_wall(state, y=-1, x=6)
        assert success is False, "Negative y coordinate should be rejected"

    def test_place_wall_rejects_y_equal_to_height(self):
        """Verify place_wall rejects y coordinate equal to HEIGHT."""
        state = create_grid_state()
        success = place_wall(state, y=HEIGHT, x=6)
        assert success is False, f"y={HEIGHT} should be rejected (out of bounds)"

    def test_place_wall_rejects_y_greater_than_height(self):
        """Verify place_wall rejects y coordinate greater than HEIGHT."""
        state = create_grid_state()
        success = place_wall(state, y=HEIGHT + 1, x=6)
        assert success is False, f"y={HEIGHT+1} should be rejected (out of bounds)"

    def test_place_wall_rejects_negative_x_coordinate(self):
        """Verify place_wall rejects negative x coordinate."""
        state = create_grid_state()
        success = place_wall(state, y=4, x=-1)
        assert success is False, "Negative x coordinate should be rejected"

    def test_place_wall_rejects_x_equal_to_width(self):
        """Verify place_wall rejects x coordinate equal to WIDTH."""
        state = create_grid_state()
        success = place_wall(state, y=4, x=WIDTH)
        assert success is False, f"x={WIDTH} should be rejected (out of bounds)"

    def test_place_wall_rejects_x_greater_than_width(self):
        """Verify place_wall rejects x coordinate greater than WIDTH."""
        state = create_grid_state()
        success = place_wall(state, y=4, x=WIDTH + 1)
        assert success is False, f"x={WIDTH+1} should be rejected (out of bounds)"

    def test_place_wall_rejects_occupied_cell(self):
        """Verify place_wall rejects placement on cell already containing WALL."""
        state = create_grid_state()
        # Place first wall
        place_wall(state, y=4, x=6)
        # Try to place second wall at same location
        success = place_wall(state, y=4, x=6)
        assert success is False, "Occupied cell should be rejected"

    def test_place_wall_accepts_all_valid_bounds(self):
        """Verify place_wall accepts all valid coordinate combinations."""
        state = create_grid_state()
        # Test corners and edges
        assert place_wall(state, 0, 0) is True, "Top-left corner should be valid"
        assert place_wall(state, 0, WIDTH - 1) is True, "Top-right corner should be valid"
        assert place_wall(state, HEIGHT - 1, 0) is True, "Bottom-left corner should be valid"
        assert place_wall(state, HEIGHT - 1, WIDTH - 1) is True, "Bottom-right corner should be valid"


class TestPlacementStateMutation:
    """Test state mutations on valid wall placement."""

    def test_place_wall_sets_grid_to_wall(self):
        """Verify place_wall sets grid[y, x] to WALL."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)
        assert state.grid[4, 6] == WALL, f"grid[4,6] should be {WALL}"

    def test_place_wall_sets_wall_hp_to_default(self):
        """Verify place_wall sets wall_hp[y, x] to DEFAULT_WALL_HP."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)
        assert (
            state.wall_hp[4, 6] == DEFAULT_WALL_HP
        ), f"wall_hp[4,6] should be {DEFAULT_WALL_HP}"

    def test_place_wall_sets_wall_pending_to_true(self):
        """Verify place_wall sets wall_pending[y, x] to True."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)
        assert state.wall_pending[4, 6] == True, "wall_pending[4,6] should be True"

    def test_place_wall_sets_wall_armed_to_false(self):
        """Verify place_wall sets wall_armed[y, x] to False."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)
        assert state.wall_armed[4, 6] == False, "wall_armed[4,6] should be False"

    def test_place_wall_only_mutates_target_cell(self):
        """Verify place_wall only mutates the target cell, not others."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)

        # Target cell should be modified
        assert state.grid[4, 6] == WALL
        assert state.wall_hp[4, 6] == DEFAULT_WALL_HP
        assert state.wall_pending[4, 6] == True
        assert state.wall_armed[4, 6] == False

        # Other cells should remain unchanged
        assert state.grid[3, 6] == 0, "Adjacent cell should remain empty"
        assert state.grid[5, 6] == 0, "Adjacent cell should remain empty"
        assert state.grid[4, 5] == 0, "Adjacent cell should remain empty"
        assert state.grid[4, 7] == 0, "Adjacent cell should remain empty"


# =============================================================================
# Cooldown Blocking Tests
# =============================================================================


class TestGCDBlocking:
    """Test global cooldown (GCD) blocking of wall placement."""

    def test_place_wall_rejects_when_gcd_positive(self):
        """Verify place_wall returns False when state.gcd > 0."""
        state = create_grid_state()
        state.gcd = np.uint16(5)
        success = place_wall(state, y=4, x=6)
        assert success is False, "Placement should be rejected when GCD > 0"

    def test_place_wall_rejects_when_gcd_at_max(self):
        """Verify place_wall returns False when state.gcd equals GCD_FRAMES."""
        state = create_grid_state()
        state.gcd = np.uint16(GCD_FRAMES)
        success = place_wall(state, y=4, x=6)
        assert success is False, f"Placement should be rejected when GCD={GCD_FRAMES}"

    def test_place_wall_accepts_when_gcd_zero(self):
        """Verify place_wall accepts placement when state.gcd == 0."""
        state = create_grid_state()
        state.gcd = np.uint16(0)
        success = place_wall(state, y=4, x=6)
        assert success is True, "Placement should succeed when GCD == 0"

    def test_gcd_blocking_prevents_state_mutation(self):
        """Verify GCD blocking prevents any state mutation."""
        state = create_grid_state()
        state.gcd = np.uint16(5)

        # Attempt placement (should fail)
        place_wall(state, y=4, x=6)

        # State should be unchanged
        assert state.grid[4, 6] == 0, "Grid should remain empty"
        assert state.wall_hp[4, 6] == 0, "Wall HP should remain 0"
        assert state.wall_pending[4, 6] == False, "Wall pending should remain False"
        assert state.wall_armed[4, 6] == False, "Wall armed should remain False"


class TestCellCooldownBlocking:
    """Test cell cooldown (cell_cd) blocking of wall placement."""

    def test_place_wall_rejects_when_cell_cd_positive(self):
        """Verify place_wall returns False when cell_cd[y, x] > 0."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(50)
        success = place_wall(state, y=4, x=6)
        assert success is False, "Placement should be rejected when cell_cd > 0"

    def test_place_wall_rejects_when_cell_cd_at_max(self):
        """Verify place_wall returns False when cell_cd equals CELL_CD_FRAMES."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(CELL_CD_FRAMES)
        success = place_wall(state, y=4, x=6)
        assert (
            success is False
        ), f"Placement should be rejected when cell_cd={CELL_CD_FRAMES}"

    def test_place_wall_accepts_when_cell_cd_zero(self):
        """Verify place_wall accepts placement when cell_cd[y, x] == 0."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(0)
        success = place_wall(state, y=4, x=6)
        assert success is True, "Placement should succeed when cell_cd == 0"

    def test_cell_cd_blocking_prevents_state_mutation(self):
        """Verify cell_cd blocking prevents any state mutation."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(50)

        # Attempt placement (should fail)
        place_wall(state, y=4, x=6)

        # State should be unchanged
        assert state.grid[4, 6] == 0, "Grid should remain empty"
        assert state.wall_hp[4, 6] == 0, "Wall HP should remain 0"
        assert state.wall_pending[4, 6] == False, "Wall pending should remain False"
        assert state.wall_armed[4, 6] == False, "Wall armed should remain False"

    def test_cell_cd_blocking_only_affects_target_cell(self):
        """Verify cell_cd blocking only affects the target cell."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(50)  # Block cell (4, 6)

        # Placement at (4, 6) should fail
        assert place_wall(state, y=4, x=6) is False

        # Placement at adjacent cell should succeed
        assert place_wall(state, y=4, x=7) is True


# =============================================================================
# Arming Lifecycle Tests
# =============================================================================


class TestArmingDelay:
    """Test 1-tick arming delay (anti-triviality rule)."""

    def test_freshly_placed_wall_is_pending_not_armed(self):
        """Verify freshly placed wall has wall_pending=True, wall_armed=False."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)

        assert (
            state.wall_pending[4, 6] == True
        ), "Freshly placed wall should be pending"
        assert (
            state.wall_armed[4, 6] == False
        ), "Freshly placed wall should not be armed"

    def test_anti_triviality_wall_not_armed_immediately(self):
        """Verify anti-triviality: wall_armed=False immediately after place_wall."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)

        # Wall should not be armed immediately
        assert state.wall_armed[4, 6] == False, "Wall should not be armed on same tick"


class TestArmPendingWalls:
    """Test arm_pending_walls() function."""

    def test_arm_pending_walls_transitions_pending_to_armed(self):
        """Verify arm_pending_walls transitions pending walls to armed."""
        state = create_grid_state()
        place_wall(state, y=4, x=6)

        # Before arming
        assert state.wall_pending[4, 6] == True
        assert state.wall_armed[4, 6] == False

        # Arm pending walls
        arm_pending_walls(state)

        # After arming
        assert not state.wall_pending[4, 6], "Wall should no longer be pending"
        assert state.wall_armed[4, 6] == True, "Wall should be armed"

    def test_arm_pending_walls_handles_multiple_walls(self):
        """Verify arm_pending_walls arms multiple pending walls in single call."""
        state = create_grid_state()

        # Place multiple walls
        place_wall(state, y=3, x=5)
        apply_cooldowns(state, 3, 5)
        state.gcd = np.uint16(0)
        place_wall(state, y=5, x=7)
        apply_cooldowns(state, 5, 7)
        state.gcd = np.uint16(0)
        place_wall(state, y=7, x=9)

        # Verify all are pending
        assert state.wall_pending[3, 5] == True
        assert state.wall_pending[5, 7] == True
        assert state.wall_pending[7, 9] == True

        # Arm all pending walls
        arm_pending_walls(state)

        # Verify all are armed
        assert state.wall_armed[3, 5].item() == True
        assert state.wall_armed[5, 7].item() == True
        assert state.wall_armed[7, 9].item() == True

        # Verify pending flags cleared
        assert not state.wall_pending[3, 5], "Wall at (3,5) should no longer be pending"
        assert not state.wall_pending[5, 7], "Wall at (5,7) should no longer be pending"
        assert not state.wall_pending[7, 9], "Wall at (7,9) should no longer be pending"

    def test_arm_pending_walls_no_op_when_no_pending_walls(self):
        """Verify arm_pending_walls is safe when no walls are pending."""
        state = create_grid_state()

        # Should not raise any errors
        arm_pending_walls(state)

        # State should remain unchanged
        assert not state.wall_pending.any(), "No walls should be pending"
        assert not state.wall_armed.any(), "No walls should be armed"

    def test_arm_pending_walls_preserves_already_armed_walls(self):
        """Verify arm_pending_walls preserves already armed walls."""
        state = create_grid_state()

        # Place and arm first wall
        place_wall(state, y=2, x=3)
        arm_pending_walls(state)

        # Place second wall
        state.gcd = np.uint16(0)
        place_wall(state, y=4, x=5)

        # Arm both (first wall already armed)
        arm_pending_walls(state)

        # Both should be armed
        assert state.wall_armed[2, 3].item() == True, "Previously armed wall should remain armed"
        assert state.wall_armed[4, 5].item() == True, "Newly pending wall should become armed"

    def test_arm_pending_walls_vectorized_operation(self):
        """Verify arm_pending_walls uses vectorized operation."""
        state = create_grid_state()

        # Place walls at multiple positions
        positions = [(1, 1), (2, 2), (3, 3), (4, 4)]
        for y, x in positions:
            place_wall(state, y, x)
            apply_cooldowns(state, y, x)
            state.gcd = np.uint16(0)

        # Verify all are pending
        for y, x in positions:
            assert state.wall_pending[y, x] == True
            assert state.wall_armed[y, x] == False

        # Arm all at once (vectorized)
        arm_pending_walls(state)

        # Verify all are armed
        for y, x in positions:
            assert not state.wall_pending[y, x], f"Wall at ({y},{x}) should no longer be pending"
            assert state.wall_armed[y, x] == True, f"Wall at ({y},{x}) should be armed"


# =============================================================================
# Cooldown Application Tests
# =============================================================================


class TestApplyCooldowns:
    """Test apply_cooldowns() function."""

    def test_apply_cooldowns_sets_gcd_to_max(self):
        """Verify apply_cooldowns sets state.gcd to GCD_FRAMES."""
        state = create_grid_state()
        apply_cooldowns(state, y=4, x=6)
        assert state.gcd == GCD_FRAMES, f"GCD should be {GCD_FRAMES}"

    def test_apply_cooldowns_sets_cell_cd_to_max(self):
        """Verify apply_cooldowns sets cell_cd[y, x] to CELL_CD_FRAMES."""
        state = create_grid_state()
        apply_cooldowns(state, y=4, x=6)
        assert (
            state.cell_cd[4, 6] == CELL_CD_FRAMES
        ), f"cell_cd[4,6] should be {CELL_CD_FRAMES}"

    def test_apply_cooldowns_only_affects_target_cell(self):
        """Verify apply_cooldowns only affects the target cell."""
        state = create_grid_state()
        apply_cooldowns(state, y=4, x=6)

        # Target cell should have cooldown
        assert state.cell_cd[4, 6] == CELL_CD_FRAMES

        # Other cells should remain at 0
        assert state.cell_cd[3, 6] == 0, "Adjacent cell should have no cooldown"
        assert state.cell_cd[5, 6] == 0, "Adjacent cell should have no cooldown"
        assert state.cell_cd[4, 5] == 0, "Adjacent cell should have no cooldown"
        assert state.cell_cd[4, 7] == 0, "Adjacent cell should have no cooldown"


class TestTickCooldowns:
    """Test tick_cooldowns() function."""

    def test_tick_cooldowns_decrements_gcd(self):
        """Verify tick_cooldowns decrements GCD by 1."""
        state = create_grid_state()
        state.gcd = np.uint16(5)
        tick_cooldowns(state)
        assert state.gcd == 4, "GCD should decrement from 5 to 4"

    def test_tick_cooldowns_decrements_cell_cd(self):
        """Verify tick_cooldowns decrements all active cell cooldowns."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(50)
        state.cell_cd[5, 7] = np.uint16(30)
        tick_cooldowns(state)
        assert state.cell_cd[4, 6] == 49, "cell_cd[4,6] should decrement from 50 to 49"
        assert state.cell_cd[5, 7] == 29, "cell_cd[5,7] should decrement from 30 to 29"

    def test_tick_cooldowns_stops_gcd_at_zero(self):
        """Verify tick_cooldowns stops GCD at 0 (no underflow)."""
        state = create_grid_state()
        state.gcd = np.uint16(1)
        tick_cooldowns(state)
        assert state.gcd == 0, "GCD should stop at 0"

        # Tick again - should remain at 0
        tick_cooldowns(state)
        assert state.gcd == 0, "GCD should not underflow below 0"

    def test_tick_cooldowns_stops_cell_cd_at_zero(self):
        """Verify tick_cooldowns stops cell_cd at 0 (no underflow)."""
        state = create_grid_state()
        state.cell_cd[4, 6] = np.uint16(1)
        tick_cooldowns(state)
        assert state.cell_cd[4, 6] == 0, "cell_cd[4,6] should stop at 0"

        # Tick again - should remain at 0
        tick_cooldowns(state)
        assert state.cell_cd[4, 6] == 0, "cell_cd[4,6] should not underflow below 0"

    def test_tick_cooldowns_vectorized_decrement(self):
        """Verify tick_cooldowns decrements all active cell cooldowns vectorized."""
        state = create_grid_state()

        # Set cooldowns at multiple cells
        state.cell_cd[1, 1] = np.uint16(10)
        state.cell_cd[2, 2] = np.uint16(20)
        state.cell_cd[3, 3] = np.uint16(30)

        tick_cooldowns(state)

        # All should decrement by 1
        assert state.cell_cd[1, 1] == 9
        assert state.cell_cd[2, 2] == 19
        assert state.cell_cd[3, 3] == 29

    def test_tick_cooldowns_handles_zero_cooldowns(self):
        """Verify tick_cooldowns handles cells with zero cooldown correctly."""
        state = create_grid_state()

        # Mix of active and zero cooldowns
        state.cell_cd[4, 6] = np.uint16(10)
        state.cell_cd[5, 7] = np.uint16(0)
        state.cell_cd[6, 8] = np.uint16(5)

        tick_cooldowns(state)

        # Active cooldowns decrement
        assert state.cell_cd[4, 6] == 9
        assert state.cell_cd[6, 8] == 4

        # Zero cooldowns remain at 0 (no underflow)
        assert state.cell_cd[5, 7] == 0


class TestCooldownLifecycle:
    """Test complete cooldown lifecycle from application to expiration."""

    def test_gcd_full_lifecycle(self):
        """Verify GCD complete lifecycle: set → decrement → expire."""
        state = create_grid_state()

        # Apply cooldown
        apply_cooldowns(state, y=4, x=6)
        assert state.gcd == GCD_FRAMES

        # Decrement to zero
        for _ in range(GCD_FRAMES):
            tick_cooldowns(state)

        assert state.gcd == 0, "GCD should reach 0 after GCD_FRAMES ticks"

    def test_cell_cd_full_lifecycle(self):
        """Verify cell_cd complete lifecycle: set → decrement → expire."""
        state = create_grid_state()

        # Apply cooldown
        apply_cooldowns(state, y=4, x=6)
        assert state.cell_cd[4, 6] == CELL_CD_FRAMES

        # Decrement to zero
        for _ in range(CELL_CD_FRAMES):
            tick_cooldowns(state)

        assert (
            state.cell_cd[4, 6] == 0
        ), "cell_cd[4,6] should reach 0 after CELL_CD_FRAMES ticks"

    def test_gcd_blocks_placement_until_expired(self):
        """Verify GCD blocks placement until it expires."""
        state = create_grid_state()

        # Apply cooldown
        apply_cooldowns(state, y=4, x=6)

        # Should be blocked while GCD > 0
        assert place_wall(state, y=5, x=7) is False, "Should be blocked while GCD > 0"

        # Decrement GCD to zero
        for _ in range(GCD_FRAMES):
            tick_cooldowns(state)

        # Should succeed after GCD expires
        assert place_wall(state, y=5, x=7) is True, "Should succeed after GCD expires"

    def test_cell_cd_blocks_placement_until_expired(self):
        """Verify cell_cd blocks placement at specific cell until it expires."""
        state = create_grid_state()

        # Place wall and apply cooldown
        place_wall(state, y=4, x=6)
        apply_cooldowns(state, y=4, x=6)
        state.gcd = np.uint16(0)  # Reset GCD to test cell_cd only

        # Should be blocked at same cell while cell_cd > 0
        assert (
            place_wall(state, y=4, x=6) is False
        ), "Should be blocked at same cell while cell_cd > 0"

        # Remove the wall (simulate destruction) to test cell_cd expiration
        state.grid[4, 6] = 0
        state.wall_hp[4, 6] = 0
        state.wall_armed[4, 6] = False
        state.wall_pending[4, 6] = False

        # Decrement cell_cd to zero
        for _ in range(CELL_CD_FRAMES):
            tick_cooldowns(state)

        # Should succeed at same cell after cell_cd expires (cell is now empty)
        assert (
            place_wall(state, y=4, x=6) is True
        ), "Should succeed at same cell after cell_cd expires"
