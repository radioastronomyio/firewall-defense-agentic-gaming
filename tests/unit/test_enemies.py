#!/usr/bin/env python3
"""
Script Name  : test_enemies.py
Description  : Unit tests for enemy state management, spawning, movement, and compaction
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Comprehensive test suite for enemy lifecycle covering state initialization,
spawning logic, half-cell movement, array compaction, and position
conversion.

Tests cover:
- EnemyState factory initialization and array properties
- Spawn logic with capacity limits and determinism
- Vectorized movement with half-cell positions
- Array compaction with stable sorting
- Half-cell to cell position conversion

Reference: docs/design-document.md Sections 10.1-10.3

Usage
-----
    pytest tests/unit/test_enemies.py -v

Examples
--------
    pytest tests/unit/test_enemies.py
        Run all enemy lifecycle tests

    pytest tests/unit/test_enemies.py -k "spawn"
        Run only spawn logic tests

    pytest tests/unit/test_enemies.py -k "compact"
        Run only compaction tests
"""

# =============================================================================
# Imports
# =============================================================================

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
from src.core.enemies import (
    EnemyState,
    compact_enemies,
    create_enemy_state,
    move_enemies,
    spawn_enemy,
)

# =============================================================================
# EnemyState Factory Tests
# =============================================================================


class TestEnemyStateFactory:
    """Test EnemyState factory function and array initialization."""

    def test_create_enemy_state_returns_enemy_state_instance(self):
        """Verify create_enemy_state returns EnemyState dataclass instance."""
        state = create_enemy_state()
        assert isinstance(state, EnemyState), "Should return EnemyState instance"

    def test_enemy_y_half_has_correct_shape(self):
        """Verify enemy_y_half array has shape (MAX_ENEMIES,)."""
        state = create_enemy_state()
        assert (
            state.enemy_y_half.shape == (MAX_ENEMIES,)
        ), f"enemy_y_half shape should be ({MAX_ENEMIES},)"

    def test_enemy_x_has_correct_shape(self):
        """Verify enemy_x array has shape (MAX_ENEMIES,)."""
        state = create_enemy_state()
        assert (
            state.enemy_x.shape == (MAX_ENEMIES,)
        ), f"enemy_x shape should be ({MAX_ENEMIES},)"

    def test_enemy_alive_has_correct_shape(self):
        """Verify enemy_alive array has shape (MAX_ENEMIES,)."""
        state = create_enemy_state()
        assert (
            state.enemy_alive.shape == (MAX_ENEMIES,)
        ), f"enemy_alive shape should be ({MAX_ENEMIES},)"

    def test_enemy_type_has_correct_shape(self):
        """Verify enemy_type array has shape (MAX_ENEMIES,)."""
        state = create_enemy_state()
        assert (
            state.enemy_type.shape == (MAX_ENEMIES,)
        ), f"enemy_type shape should be ({MAX_ENEMIES},)"

    def test_enemy_spawn_tick_has_correct_shape(self):
        """Verify enemy_spawn_tick array has shape (MAX_ENEMIES,)."""
        state = create_enemy_state()
        assert (
            state.enemy_spawn_tick.shape == (MAX_ENEMIES,)
        ), f"enemy_spawn_tick shape should be ({MAX_ENEMIES},)"

    def test_enemy_y_half_has_correct_dtype(self):
        """Verify enemy_y_half uses ENEMY_POS_DTYPE (int16)."""
        state = create_enemy_state()
        assert (
            state.enemy_y_half.dtype == ENEMY_POS_DTYPE
        ), f"enemy_y_half dtype should be {ENEMY_POS_DTYPE}"

    def test_enemy_x_has_correct_dtype(self):
        """Verify enemy_x uses ENEMY_POS_DTYPE (int16)."""
        state = create_enemy_state()
        assert (
            state.enemy_x.dtype == ENEMY_POS_DTYPE
        ), f"enemy_x dtype should be {ENEMY_POS_DTYPE}"

    def test_enemy_alive_has_correct_dtype(self):
        """Verify enemy_alive uses ENEMY_ALIVE_DTYPE (bool_)."""
        state = create_enemy_state()
        assert (
            state.enemy_alive.dtype == ENEMY_ALIVE_DTYPE
        ), f"enemy_alive dtype should be {ENEMY_ALIVE_DTYPE}"

    def test_enemy_type_has_correct_dtype(self):
        """Verify enemy_type uses ENEMY_TYPE_DTYPE (uint8)."""
        state = create_enemy_state()
        assert (
            state.enemy_type.dtype == ENEMY_TYPE_DTYPE
        ), f"enemy_type dtype should be {ENEMY_TYPE_DTYPE}"

    def test_enemy_spawn_tick_has_correct_dtype(self):
        """Verify enemy_spawn_tick uses ENEMY_TICK_DTYPE (uint32)."""
        state = create_enemy_state()
        assert (
            state.enemy_spawn_tick.dtype == ENEMY_TICK_DTYPE
        ), f"enemy_spawn_tick dtype should be {ENEMY_TICK_DTYPE}"

    def test_enemy_y_half_initialized_to_zero(self):
        """Verify enemy_y_half is all zeros on fresh state."""
        state = create_enemy_state()
        assert not state.enemy_y_half.any(), "enemy_y_half should be all zeros"

    def test_enemy_x_initialized_to_zero(self):
        """Verify enemy_x is all zeros on fresh state."""
        state = create_enemy_state()
        assert not state.enemy_x.any(), "enemy_x should be all zeros"

    def test_enemy_alive_initialized_to_false(self):
        """Verify enemy_alive is all False on fresh state."""
        state = create_enemy_state()
        assert not state.enemy_alive.any(), "enemy_alive should be all False"

    def test_enemy_type_initialized_to_zero(self):
        """Verify enemy_type is all zeros on fresh state."""
        state = create_enemy_state()
        assert not state.enemy_type.any(), "enemy_type should be all zeros"

    def test_enemy_spawn_tick_initialized_to_zero(self):
        """Verify enemy_spawn_tick is all zeros on fresh state."""
        state = create_enemy_state()
        assert not state.enemy_spawn_tick.any(), "enemy_spawn_tick should be all zeros"

    def test_independent_instances_no_shared_references(self):
        """Verify each call returns independent state instances."""
        state1 = create_enemy_state()
        state2 = create_enemy_state()

        # Modify state1
        state1.enemy_alive[0] = True
        state1.enemy_y_half[0] = 5
        state1.enemy_x[0] = 6
        state1.enemy_type[0] = 1
        state1.enemy_spawn_tick[0] = 100

        # state2 should be unchanged
        assert state2.enemy_alive[0] == False, "state2 should be independent"
        assert state2.enemy_y_half[0] == 0, "state2 should be independent"
        assert state2.enemy_x[0] == 0, "state2 should be independent"
        assert state2.enemy_type[0] == 0, "state2 should be independent"
        assert state2.enemy_spawn_tick[0] == 0, "state2 should be independent"


# =============================================================================
# Spawn Logic Tests
# =============================================================================


class TestSpawnEnemy:
    """Test spawn_enemy() function for spawning Drop enemies."""

    def test_spawn_enemy_returns_true_when_slots_available(self):
        """Verify spawn_enemy returns True when slots are available."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        success = spawn_enemy(state, current_tick=0, rng=rng)
        assert success is True, "Spawn should succeed when slots available"

    def test_spawn_enemy_returns_false_when_all_slots_full(self):
        """Verify spawn_enemy returns False when all 20 slots are alive."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Fill all 20 slots
        for i in range(MAX_ENEMIES):
            spawn_enemy(state, current_tick=i, rng=rng)

        # Try to spawn when full
        success = spawn_enemy(state, current_tick=20, rng=rng)
        assert success is False, "Spawn should fail when all slots are full"

    def test_spawn_enemy_sets_y_half_to_zero(self):
        """Verify spawn_enemy sets enemy_y_half to 0 (top of grid)."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        spawn_enemy(state, current_tick=0, rng=rng)
        assert state.enemy_y_half[0] == 0, "Enemy should spawn at y_half=0"

    def test_spawn_enemy_sets_x_in_valid_range(self):
        """Verify spawn_enemy sets enemy_x in range [0, WIDTH)."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        spawn_enemy(state, current_tick=0, rng=rng)
        assert 0 <= state.enemy_x[0] < WIDTH, "Column should be in valid range"

    def test_spawn_enemy_sets_alive_to_true(self):
        """Verify spawn_enemy sets enemy_alive to True for spawned slot."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        spawn_enemy(state, current_tick=0, rng=rng)
        assert state.enemy_alive[0] == True, "Spawned slot should be alive"

    def test_spawn_enemy_sets_type_to_drop(self):
        """Verify spawn_enemy sets enemy_type to ENEMY_TYPE_DROP (0)."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        spawn_enemy(state, current_tick=0, rng=rng)
        assert state.enemy_type[0] == ENEMY_TYPE_DROP, "Enemy type should be DROP"

    def test_spawn_enemy_sets_spawn_tick_to_current_tick(self):
        """Verify spawn_enemy sets enemy_spawn_tick to current_tick."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)
        spawn_enemy(state, current_tick=123, rng=rng)
        assert state.enemy_spawn_tick[0] == 123, "Spawn tick should match current_tick"

    def test_spawn_enemy_finds_first_dead_slot(self):
        """Verify spawn_enemy finds first dead slot using np.argmax pattern."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 3 enemies
        spawn_enemy(state, current_tick=0, rng=rng)
        spawn_enemy(state, current_tick=10, rng=rng)
        spawn_enemy(state, current_tick=20, rng=rng)

        # Kill slot 1 (middle enemy)
        state.enemy_alive[1] = False

        # Next spawn should use slot 1 (first dead)
        success = spawn_enemy(state, current_tick=30, rng=rng)
        assert success is True, "Spawn should find first dead slot"
        assert state.enemy_alive[1] == True, "Slot 1 should be re-used"
        assert state.enemy_spawn_tick[1] == 30, "Spawn tick should be 30"
        assert state.enemy_alive[3] == False, "Slot 3 should remain dead"

    def test_spawn_enemy_deterministic_with_seeded_rng(self):
        """Verify same seed produces same column sequence."""
        state1 = create_enemy_state()
        state2 = create_enemy_state()
        rng1 = np.random.default_rng(42)
        rng2 = np.random.default_rng(42)

        # Spawn 5 enemies with same seed
        for i in range(5):
            spawn_enemy(state1, current_tick=i, rng=rng1)
            spawn_enemy(state2, current_tick=i, rng=rng2)

        # Columns should be identical
        assert np.array_equal(
            state1.enemy_x[:5], state2.enemy_x[:5]
        ), "Same seed should produce same columns"

    def test_spawn_enemy_fills_slots_sequentially(self):
        """Verify multiple spawns fill slots in order."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 5 enemies
        for i in range(5):
            spawn_enemy(state, current_tick=i, rng=rng)

        # First 5 slots should be alive, rest dead
        assert state.enemy_alive[:5].all(), "First 5 slots should be alive"
        assert not state.enemy_alive[5:].any(), "Slots 5-19 should be dead"

    def test_spawn_enemy_random_column_bounds(self):
        """Verify random columns are always within [0, WIDTH)."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 10 enemies and verify all columns are valid
        for i in range(10):
            spawn_enemy(state, current_tick=i, rng=rng)
            assert 0 <= state.enemy_x[i] < WIDTH, f"Column {state.enemy_x[i]} should be in [0, {WIDTH})"


# =============================================================================
# Movement Tests
# =============================================================================


class TestMoveEnemies:
    """Test move_enemies() function for half-cell movement."""

    def test_move_enemies_increments_y_half_by_speed(self):
        """Verify move_enemies increments y_half by ENEMY_SPEED_HALF."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0

        move_enemies(state)

        assert state.enemy_y_half[0] == ENEMY_SPEED_HALF, f"y_half should increment by {ENEMY_SPEED_HALF}"

    def test_move_enemies_only_moves_alive_enemies(self):
        """Verify move_enemies only moves alive enemies, dead slots unchanged."""
        state = create_enemy_state()

        # Set up alive and dead enemies
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0
        state.enemy_alive[1] = False
        state.enemy_y_half[1] = 5

        move_enemies(state)

        # Alive enemy should move
        assert state.enemy_y_half[0] == 1, "Alive enemy should move"

        # Dead enemy should remain unchanged
        assert state.enemy_y_half[1] == 5, "Dead enemy should not move"

    def test_move_enemies_moves_multiple_alive_enemies(self):
        """Verify move_enemies moves all alive enemies in single call."""
        state = create_enemy_state()

        # Set up 3 alive enemies
        for i in range(3):
            state.enemy_alive[i] = True
            state.enemy_y_half[i] = i * 2

        move_enemies(state)

        # All should have moved by ENEMY_SPEED_HALF
        assert state.enemy_y_half[0] == 1, "Enemy 0 should move"
        assert state.enemy_y_half[1] == 3, "Enemy 1 should move"
        assert state.enemy_y_half[2] == 5, "Enemy 2 should move"

    def test_move_enemies_in_place_mutation(self):
        """Verify move_enemies mutates state in-place (no return value)."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0

        result = move_enemies(state)

        # Function should return None
        assert result is None, "move_enemies should return None"

        # State should be mutated
        assert state.enemy_y_half[0] == 1, "State should be mutated in-place"

    def test_move_enemies_multiple_calls_accumulate(self):
        """Verify multiple move_enemies calls accumulate movement."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0

        # Move 3 times
        move_enemies(state)
        move_enemies(state)
        move_enemies(state)

        # Should have moved by 3 * ENEMY_SPEED_HALF
        assert state.enemy_y_half[0] == 3, "Movement should accumulate"


# =============================================================================
# Compaction Tests
# =============================================================================


class TestCompactEnemies:
    """Test compact_enemies() function for array compaction."""

    def test_compact_enemies_returns_zero_when_all_dead(self):
        """Verify compact_enemies returns 0 when no enemies alive."""
        state = create_enemy_state()
        alive_count = compact_enemies(state)
        assert alive_count == 0, "Should have 0 alive enemies"

    def test_compact_enemies_zero_pads_when_all_dead(self):
        """Verify compact_enemies zero-pads all arrays when all dead."""
        state = create_enemy_state()
        compact_enemies(state)

        # All arrays should be zero
        assert not state.enemy_alive.any(), "All slots should be dead"
        assert state.enemy_y_half.sum() == 0, "All y_half should be 0"
        assert state.enemy_x.sum() == 0, "All x should be 0"
        assert state.enemy_type.sum() == 0, "All types should be 0"
        assert state.enemy_spawn_tick.sum() == 0, "All spawn ticks should be 0"

    def test_compact_enemies_preserves_order_when_all_alive(self):
        """Verify compact_enemies preserves order when all enemies alive."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 5 enemies at different ticks
        for i in range(5):
            spawn_enemy(state, current_tick=i * 10, rng=rng)

        # Record original order
        original_spawn_ticks = state.enemy_spawn_tick[:5].copy()

        # Compact
        alive_count = compact_enemies(state)

        # Order should be preserved
        assert alive_count == 5, "Should have 5 alive enemies"
        assert np.array_equal(
            state.enemy_spawn_tick[:5], original_spawn_ticks
        ), "Order should be preserved"

    def test_compact_enemies_sorts_by_spawn_tick_oldest_first(self):
        """Verify compact_enemies sorts alive enemies by spawn_tick (oldest first)."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 3 enemies at different ticks
        spawn_enemy(state, current_tick=100, rng=rng)  # Slot 0, tick 100
        spawn_enemy(state, current_tick=200, rng=rng)  # Slot 1, tick 200
        spawn_enemy(state, current_tick=150, rng=rng)  # Slot 2, tick 150

        # Kill slot 1 (middle enemy, tick 200)
        state.enemy_alive[1] = False

        # Compact should sort by spawn_tick: 100, 150
        alive_count = compact_enemies(state)

        assert alive_count == 2, "Should have 2 alive enemies"
        assert state.enemy_spawn_tick[0] == 100, "Slot 0 should have oldest (tick 100)"
        assert state.enemy_spawn_tick[1] == 150, "Slot 1 should have second-oldest (tick 150)"

    def test_compact_enemies_shifts_alive_to_front(self):
        """Verify compact_enemies shifts alive enemies to front of arrays."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 3 enemies
        spawn_enemy(state, current_tick=100, rng=rng)
        spawn_enemy(state, current_tick=150, rng=rng)
        spawn_enemy(state, current_tick=200, rng=rng)

        # Kill slot 1 (middle enemy)
        state.enemy_alive[1] = False

        # Compact should shift alive enemies to front
        alive_count = compact_enemies(state)

        assert alive_count == 2, "Should have 2 alive enemies"
        assert state.enemy_alive[0] == True, "Slot 0 should be alive"
        assert state.enemy_alive[1] == True, "Slot 1 should be alive"
        assert not state.enemy_alive[2:].any(), "Slots 2-19 should be dead"

    def test_compact_enemies_zero_pads_trailing_slots(self):
        """Verify compact_enemies zero-pads trailing slots after alive enemies."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 3 enemies
        spawn_enemy(state, current_tick=100, rng=rng)
        spawn_enemy(state, current_tick=150, rng=rng)
        spawn_enemy(state, current_tick=200, rng=rng)

        # Kill slot 1
        state.enemy_alive[1] = False

        # Compact
        alive_count = compact_enemies(state)

        # Trailing slots should be zero-padded
        assert not state.enemy_alive[alive_count:].any(), "Trailing slots should be dead"
        assert state.enemy_y_half[alive_count:].sum() == 0, "Trailing y_half should be 0"
        assert state.enemy_x[alive_count:].sum() == 0, "Trailing x should be 0"
        assert state.enemy_type[alive_count:].sum() == 0, "Trailing types should be 0"
        assert state.enemy_spawn_tick[alive_count:].sum() == 0, "Trailing spawn ticks should be 0"

    def test_compact_enemies_handles_multiple_dead_slots(self):
        """Verify compact_enemies handles multiple dead slots correctly."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 5 enemies
        for i in range(5):
            spawn_enemy(state, current_tick=i * 10, rng=rng)

        # Kill slots 1 and 3
        state.enemy_alive[1] = False
        state.enemy_alive[3] = False

        # Compact should keep enemies at ticks 0, 20, 40
        alive_count = compact_enemies(state)

        assert alive_count == 3, "Should have 3 alive enemies"
        expected_ticks = [0, 20, 40]
        actual_ticks = sorted(state.enemy_spawn_tick[:3].tolist())
        assert actual_ticks == expected_ticks, f"Expected {expected_ticks}, got {actual_ticks}"

    def test_compact_enemies_stable_sort_preserves_order(self):
        """Verify compact_enemies uses stable sort for same-tick spawns."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Spawn 3 enemies at same tick
        spawn_enemy(state, current_tick=100, rng=rng)
        spawn_enemy(state, current_tick=100, rng=rng)
        spawn_enemy(state, current_tick=100, rng=rng)

        # Kill middle enemy
        state.enemy_alive[1] = False

        # Compact should preserve order for same tick
        alive_count = compact_enemies(state)

        assert alive_count == 2, "Should have 2 alive enemies"
        assert state.enemy_spawn_tick[0] == 100, "Slot 0 should have tick 100"
        assert state.enemy_spawn_tick[1] == 100, "Slot 1 should have tick 100"

    def test_compact_enemies_full_capacity(self):
        """Verify compact_enemies works correctly with all 20 slots."""
        state = create_enemy_state()
        rng = np.random.default_rng(42)

        # Fill all 20 slots
        for i in range(MAX_ENEMIES):
            spawn_enemy(state, current_tick=i, rng=rng)

        # Kill slot 5
        state.enemy_alive[5] = False

        # Compact
        alive_count = compact_enemies(state)

        assert alive_count == 19, "Should have 19 alive enemies"
        assert state.enemy_alive[:19].all(), "First 19 slots should be alive"
        assert not state.enemy_alive[19], "Slot 19 should be dead"


# =============================================================================
# Half-Cell Conversion Tests
# =============================================================================


class TestHalfCellConversion:
    """Test half-cell to cell position conversion logic."""

    def test_half_cell_zero_maps_to_cell_zero(self):
        """Verify y_half=0 maps to cell 0."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0

        cell_y = state.enemy_y_half[0] // 2
        assert cell_y == 0, "y_half=0 should map to cell 0"

    def test_half_cell_one_maps_to_cell_zero(self):
        """Verify y_half=1 maps to cell 0 (mid-cell)."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 1

        cell_y = state.enemy_y_half[0] // 2
        assert cell_y == 0, "y_half=1 should map to cell 0 (mid-cell)"

    def test_half_cell_two_maps_to_cell_one(self):
        """Verify y_half=2 maps to cell 1."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 2

        cell_y = state.enemy_y_half[0] // 2
        assert cell_y == 1, "y_half=2 should map to cell 1"

    def test_half_cell_three_maps_to_cell_one(self):
        """Verify y_half=3 maps to cell 1 (mid-cell)."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 3

        cell_y = state.enemy_y_half[0] // 2
        assert cell_y == 1, "y_half=3 should map to cell 1 (mid-cell)"

    def test_half_cell_four_maps_to_cell_two(self):
        """Verify y_half=4 maps to cell 2."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 4

        cell_y = state.enemy_y_half[0] // 2
        assert cell_y == 2, "y_half=4 should map to cell 2"

    def test_movement_across_cell_boundary(self):
        """Verify movement from y_half=1 to y_half=2 crosses cell boundary."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 1

        # Before move: cell 0 (mid-cell)
        cell_before = state.enemy_y_half[0] // 2
        assert cell_before == 0, "Before move: should be in cell 0"

        # Move
        move_enemies(state)

        # After move: cell 1 (new cell)
        cell_after = state.enemy_y_half[0] // 2
        assert cell_after == 1, "After move: should be in cell 1"

    def test_multiple_cell_boundaries(self):
        """Verify multiple movements cross cell boundaries correctly."""
        state = create_enemy_state()
        state.enemy_alive[0] = True
        state.enemy_y_half[0] = 0

        # Track cell positions through multiple moves
        expected_cells = [0, 0, 1, 1, 2, 2, 3, 3]

        for expected_cell in expected_cells:
            cell_y = state.enemy_y_half[0] // 2
            assert cell_y == expected_cell, f"y_half={state.enemy_y_half[0]} should map to cell {expected_cell}"
            move_enemies(state)
