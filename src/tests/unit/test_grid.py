#!/usr/bin/env python3
"""
Script Name  : test_grid.py
Description  : Unit tests for grid state initialization and management
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-05
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Validates GridState dataclass and create_grid_state() factory function.
Tests array shapes, dtypes, initialization values, and instance independence.

Reference: docs/design-document.md Section 10.1 (State Arrays)

Usage
-----
    pytest src/tests/unit/test_grid.py -v

Examples
--------
    pytest src/tests/unit/test_grid.py
        Run all grid state validation tests

    pytest src/tests/unit/test_grid.py -k "factory"
        Run only factory function tests
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.constants import (
    COOLDOWN_DTYPE,
    GRID_DTYPE,
    GRID_SHAPE,
    WALL_HP_DTYPE,
    WALL_STATE_DTYPE,
)
from src.core.grid import GridState, create_grid_state

# =============================================================================
# GridState Dataclass Tests
# =============================================================================


class TestGridStateAttributes:
    """Test GridState dataclass attribute types and structure."""

    def test_grid_state_has_all_required_attributes(self):
        """Verify GridState has all required state array attributes."""
        state = create_grid_state()

        # Check all grid array attributes exist
        assert hasattr(state, "grid"), "GridState should have 'grid' attribute"
        assert hasattr(state, "wall_hp"), "GridState should have 'wall_hp' attribute"
        assert hasattr(
            state, "wall_armed"
        ), "GridState should have 'wall_armed' attribute"
        assert hasattr(
            state, "wall_pending"
        ), "GridState should have 'wall_pending' attribute"
        assert hasattr(state, "cell_cd"), "GridState should have 'cell_cd' attribute"
        assert hasattr(state, "gcd"), "GridState should have 'gcd' attribute"

    def test_grid_arrays_are_ndarrays(self):
        """Verify all grid arrays are numpy arrays."""
        state = create_grid_state()

        assert isinstance(
            state.grid, np.ndarray
        ), "grid should be a numpy ndarray"
        assert isinstance(
            state.wall_hp, np.ndarray
        ), "wall_hp should be a numpy ndarray"
        assert isinstance(
            state.wall_armed, np.ndarray
        ), "wall_armed should be a numpy ndarray"
        assert isinstance(
            state.wall_pending, np.ndarray
        ), "wall_pending should be a numpy ndarray"
        assert isinstance(
            state.cell_cd, np.ndarray
        ), "cell_cd should be a numpy ndarray"


class TestGridArrayShapes:
    """Test grid array shapes match GRID_SHAPE constant."""

    def test_grid_array_shape(self):
        """Verify grid array has shape (9, 13)."""
        state = create_grid_state()
        assert (
            state.grid.shape == GRID_SHAPE
        ), f"grid shape should be {GRID_SHAPE}, got {state.grid.shape}"

    def test_wall_hp_array_shape(self):
        """Verify wall_hp array has shape (9, 13)."""
        state = create_grid_state()
        assert (
            state.wall_hp.shape == GRID_SHAPE
        ), f"wall_hp shape should be {GRID_SHAPE}, got {state.wall_hp.shape}"

    def test_wall_armed_array_shape(self):
        """Verify wall_armed array has shape (9, 13)."""
        state = create_grid_state()
        assert (
            state.wall_armed.shape == GRID_SHAPE
        ), f"wall_armed shape should be {GRID_SHAPE}, got {state.wall_armed.shape}"

    def test_wall_pending_array_shape(self):
        """Verify wall_pending array has shape (9, 13)."""
        state = create_grid_state()
        assert (
            state.wall_pending.shape == GRID_SHAPE
        ), f"wall_pending shape should be {GRID_SHAPE}, got {state.wall_pending.shape}"

    def test_cell_cd_array_shape(self):
        """Verify cell_cd array has shape (9, 13)."""
        state = create_grid_state()
        assert (
            state.cell_cd.shape == GRID_SHAPE
        ), f"cell_cd shape should be {GRID_SHAPE}, got {state.cell_cd.shape}"


class TestGridArrayDtypes:
    """Test grid array dtypes match constants specification."""

    def test_grid_dtype(self):
        """Verify grid array dtype is int8."""
        state = create_grid_state()
        assert (
            state.grid.dtype == GRID_DTYPE
        ), f"grid dtype should be {GRID_DTYPE}, got {state.grid.dtype}"

    def test_wall_hp_dtype(self):
        """Verify wall_hp array dtype is uint8."""
        state = create_grid_state()
        assert (
            state.wall_hp.dtype == WALL_HP_DTYPE
        ), f"wall_hp dtype should be {WALL_HP_DTYPE}, got {state.wall_hp.dtype}"

    def test_wall_armed_dtype(self):
        """Verify wall_armed array dtype is bool_."""
        state = create_grid_state()
        assert (
            state.wall_armed.dtype == WALL_STATE_DTYPE
        ), f"wall_armed dtype should be {WALL_STATE_DTYPE}, got {state.wall_armed.dtype}"

    def test_wall_pending_dtype(self):
        """Verify wall_pending array dtype is bool_."""
        state = create_grid_state()
        assert (
            state.wall_pending.dtype == WALL_STATE_DTYPE
        ), f"wall_pending dtype should be {WALL_STATE_DTYPE}, got {state.wall_pending.dtype}"

    def test_cell_cd_dtype(self):
        """Verify cell_cd array dtype is uint16."""
        state = create_grid_state()
        assert (
            state.cell_cd.dtype == COOLDOWN_DTYPE
        ), f"cell_cd dtype should be {COOLDOWN_DTYPE}, got {state.cell_cd.dtype}"

    def test_gcd_dtype(self):
        """Verify gcd is scalar uint16."""
        state = create_grid_state()
        # np.uint16 is a dtype, not a class, so check dtype attribute
        assert isinstance(
            state.gcd, (np.integer, int)
        ), f"gcd should be a numpy integer, got {type(state.gcd)}"
        assert (
            state.gcd.dtype == np.uint16
        ), f"gcd dtype should be uint16, got {state.gcd.dtype}"


class TestGridArrayIndexing:
    """Test grid arrays use [y, x] indexing convention."""

    def test_grid_array_yx_indexing(self):
        """Verify grid array supports [y, x] indexing."""
        state = create_grid_state()

        # Test [y, x] indexing works
        state.grid[4, 6] = 1  # Row 4, column 6
        assert state.grid[4, 6] == 1, "[y, x] indexing should work on grid array"

        # Reset for next test
        state.grid[4, 6] = 0

    def test_all_arrays_support_yx_indexing(self):
        """Verify all grid arrays support [y, x] indexing."""
        state = create_grid_state()

        # Test each array with [y, x] indexing
        y, x = 3, 7

        state.grid[y, x] = 1
        state.wall_hp[y, x] = 5
        state.wall_armed[y, x] = True
        state.wall_pending[y, x] = True
        state.cell_cd[y, x] = 10

        assert state.grid[y, x] == 1
        assert state.wall_hp[y, x] == 5
        assert state.wall_armed[y, x] == True
        assert state.wall_pending[y, x] == True
        assert state.cell_cd[y, x] == 10


# =============================================================================
# Factory Function Tests
# =============================================================================


class TestFactoryInitialization:
    """Test create_grid_state() returns properly initialized state."""

    def test_factory_returns_grid_state_instance(self):
        """Verify factory returns GridState instance."""
        state = create_grid_state()
        assert isinstance(
            state, GridState
        ), "create_grid_state() should return GridState instance"

    def test_factory_initializes_arrays_to_zero(self):
        """Verify factory initializes all grid arrays to zero."""
        state = create_grid_state()

        assert np.all(
            state.grid == 0
        ), "grid array should be all zeros after initialization"
        assert np.all(
            state.wall_hp == 0
        ), "wall_hp array should be all zeros after initialization"
        assert np.all(
            state.wall_armed == False
        ), "wall_armed array should be all False after initialization"
        assert np.all(
            state.wall_pending == False
        ), "wall_pending array should be all False after initialization"
        assert np.all(
            state.cell_cd == 0
        ), "cell_cd array should be all zeros after initialization"

    def test_factory_initializes_gcd_to_zero(self):
        """Verify factory initializes gcd to 0."""
        state = create_grid_state()
        assert state.gcd == 0, f"gcd should be 0 after initialization, got {state.gcd}"

    def test_factory_requires_no_arguments(self):
        """Verify factory function requires no arguments."""
        # Should not raise TypeError for missing arguments
        state = create_grid_state()
        assert state is not None, "create_grid_state() should work with no arguments"


class TestFactoryIndependence:
    """Test factory returns independent instances (no shared references)."""

    def test_factory_returns_independent_grid_arrays(self):
        """Verify multiple factory calls return independent grid arrays."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        # Modify state1
        state1.grid[4, 6] = 1

        # state2 should be unaffected
        assert (
            state2.grid[4, 6] == 0
        ), "state2.grid should be unaffected by state1.grid modification"

    def test_factory_returns_independent_wall_hp_arrays(self):
        """Verify wall_hp arrays are independent across instances."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        state1.wall_hp[3, 7] = 10

        assert (
            state2.wall_hp[3, 7] == 0
        ), "state2.wall_hp should be unaffected by state1.wall_hp modification"

    def test_factory_returns_independent_wall_armed_arrays(self):
        """Verify wall_armed arrays are independent across instances."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        state1.wall_armed[2, 5] = True

        assert (
            state2.wall_armed[2, 5] == False
        ), "state2.wall_armed should be unaffected by state1.wall_armed modification"

    def test_factory_returns_independent_wall_pending_arrays(self):
        """Verify wall_pending arrays are independent across instances."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        state1.wall_pending[1, 3] = True

        assert (
            state2.wall_pending[1, 3] == False
        ), "state2.wall_pending should be unaffected by state1.wall_pending modification"

    def test_factory_returns_independent_cell_cd_arrays(self):
        """Verify cell_cd arrays are independent across instances."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        state1.cell_cd[5, 8] = 50

        assert (
            state2.cell_cd[5, 8] == 0
        ), "state2.cell_cd should be unaffected by state1.cell_cd modification"

    def test_factory_returns_independent_gcd_values(self):
        """Verify gcd values are independent across instances."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        state1.gcd = np.uint16(5)

        assert (
            state2.gcd == 0
        ), "state2.gcd should be unaffected by state1.gcd modification"

    def test_multiple_factory_calls_all_independent(self):
        """Verify three or more factory calls are all independent."""
        state1 = create_grid_state()
        state2 = create_grid_state()
        state3 = create_grid_state()

        # Modify all three differently
        state1.grid[0, 0] = 1
        state2.grid[0, 0] = 2
        state3.grid[0, 0] = 3

        # Each should retain its own value
        assert state1.grid[0, 0] == 1, "state1 should retain its value"
        assert state2.grid[0, 0] == 2, "state2 should retain its value"
        assert state3.grid[0, 0] == 3, "state3 should retain its value"


class TestFactoryDeterminism:
    """Test factory produces deterministic results."""

    def test_factory_proces_same_initial_state(self):
        """Verify factory always produces same initial state."""
        state1 = create_grid_state()
        state2 = create_grid_state()

        # All arrays should be identical
        assert np.array_equal(
            state1.grid, state2.grid
        ), "grid arrays should be identical"
        assert np.array_equal(
            state1.wall_hp, state2.wall_hp
        ), "wall_hp arrays should be identical"
        assert np.array_equal(
            state1.wall_armed, state2.wall_armed
        ), "wall_armed arrays should be identical"
        assert np.array_equal(
            state1.wall_pending, state2.wall_pending
        ), "wall_pending arrays should be identical"
        assert np.array_equal(
            state1.cell_cd, state2.cell_cd
        ), "cell_cd arrays should be identical"
        assert state1.gcd == state2.gcd, "gcd values should be identical"
