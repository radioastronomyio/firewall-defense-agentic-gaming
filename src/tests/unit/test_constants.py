#!/usr/bin/env python3
"""
Script Name  : test_constants.py
Description  : Unit tests validating constants match design document
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-04
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Validates all constant values in src.core.constants match the design document
specifications. Ensures dtype definitions are valid numpy dtype objects.
Tests are organized by constant category matching the module structure.

Reference: docs/design-document.md Sections 3, 4, 5, 7, 10, 14

Usage
-----
    pytest src/tests/unit/test_constants.py -v

Examples
--------
    pytest src/tests/unit/test_constants.py
        Run all 41 constant validation tests

    pytest src/tests/unit/test_constants.py -k "dtype"
        Run only dtype specification tests
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

from src.core.constants import (
    # Cooldown Constants
    CELL_CD_FRAMES,
    COOLDOWN_DTYPE,
    # Position System
    CORE_Y_HALF,
    # Episode Constants
    DEFAULT_SPAWN_INTERVAL,
    # Wall Constants
    DEFAULT_WALL_HP,
    # Cell States
    EMPTY,
    ENEMY_ALIVE_DTYPE,
    ENEMY_POS_DTYPE,
    # Movement Constants
    ENEMY_SPEED_HALF,
    ENEMY_TICK_DTYPE,
    ENEMY_TYPE_DRIFTER,
    # Enemy Type Constants
    ENEMY_TYPE_DROP,
    ENEMY_TYPE_DTYPE,
    ENEMY_TYPE_FLOOD,
    ENEMY_TYPE_SEEKER,
    GCD_FRAMES,
    # Dtype Specifications
    GRID_DTYPE,
    GRID_SHAPE,
    HEIGHT,
    MAX_COOLDOWN,
    MAX_ENEMIES,
    MAX_ENEMY_TYPE,
    MAX_EPISODE_TICKS,
    MAX_WALL_HP,
    # Validation Constants
    MIN_WALL_HP,
    NO_OP_ACTION,
    # Action Constants
    NUM_ACTIONS,
    OBS_ACTION_MASK_SIZE,
    OBS_CELL_CD_SIZE,
    OBS_ENEMY_ALIVE_SIZE,
    OBS_ENEMY_POS_SIZE,
    OBS_ENEMY_TYPE_SIZE,
    OBS_GCD_SIZE,
    # Observation Constants
    OBS_GRID_STATE_SIZE,
    OBS_WALL_ARMED_SIZE,
    OBS_WALL_HP_SIZE,
    OBSERVATION_SIZE,
    # Reward Constants
    REWARD_CORE_BREACH,
    REWARD_ENEMY_KILLED,
    REWARD_TICK_SURVIVED,
    TOTAL_CELLS,
    WALL,
    WALL_HP_DTYPE,
    WALL_STATE_DTYPE,
    # Grid Constants
    WIDTH,
)

# =============================================================================
# Grid Constants Tests (Section 3)
# =============================================================================


class TestGridConstants:
    """Test grid dimension and shape constants."""

    def test_grid_dimensions(self):
        """Verify grid dimensions match 13×9 specification."""
        assert WIDTH == 13, "Grid width should be 13 columns"
        assert HEIGHT == 9, "Grid height should be 9 rows"

    def test_total_cells(self):
        """Verify total cells equals width × height."""
        assert TOTAL_CELLS == 117, "Total cells should be 13 × 9 = 117"

    def test_grid_shape(self):
        """Verify grid shape tuple is (HEIGHT, WIDTH) for [y, x] indexing."""
        assert GRID_SHAPE == (9, 13), "Grid shape should be (HEIGHT, WIDTH) = (9, 13)"


# =============================================================================
# Cell States Tests (Section 3)
# =============================================================================


class TestCellStates:
    """Test cell state constants."""

    def test_cell_state_values(self):
        """Verify cell state values are correct."""
        assert EMPTY == 0, "EMPTY should be 0"
        assert WALL == 1, "WALL should be 1"


# =============================================================================
# Position System Tests (Section 4)
# =============================================================================


class TestPositionSystem:
    """Test position system constants."""

    def test_core_y_half(self):
        """Verify core breach threshold."""
        assert CORE_Y_HALF == 16, "Core Y half should be 16 (row 8 reached)"

    def test_max_enemies(self):
        """Verify fixed enemy slot count."""
        assert MAX_ENEMIES == 20, "Max enemies should be 20 fixed slots"


# =============================================================================
# Movement Constants Tests (Section 4)
# =============================================================================


class TestMovementConstants:
    """Test movement constants."""

    def test_enemy_speed_half(self):
        """Verify enemy speed in half-cells per tick."""
        assert ENEMY_SPEED_HALF == 1, "Enemy speed should be 1 half-cell per tick"


# =============================================================================
# Cooldown Constants Tests (Section 5)
# =============================================================================


class TestCooldownConstants:
    """Test cooldown constants."""

    def test_gcd_frames(self):
        """Verify global cooldown duration."""
        assert GCD_FRAMES == 10, "GCD should be 10 frames"

    def test_cell_cd_frames(self):
        """Verify cell cooldown duration."""
        assert CELL_CD_FRAMES == 150, "Cell CD should be 150 frames"


# =============================================================================
# Episode Constants Tests (Section 14)
# =============================================================================


class TestEpisodeConstants:
    """Test episode constants."""

    def test_default_spawn_interval(self):
        """Verify default spawn interval."""
        assert DEFAULT_SPAWN_INTERVAL == 30, "Default spawn interval should be 30 ticks"

    def test_max_episode_ticks(self):
        """Verify maximum episode length."""
        assert MAX_EPISODE_TICKS == 1000, "Max episode ticks should be 1000"


# =============================================================================
# Action Constants Tests (Section 5)
# =============================================================================


class TestActionConstants:
    """Test action constants."""

    def test_num_actions(self):
        """Verify total action count (NO-OP + 117 cells)."""
        assert NUM_ACTIONS == 118, "Num actions should be 118 (1 NO-OP + 117 cells)"

    def test_no_op_action(self):
        """Verify NO-OP action index."""
        assert NO_OP_ACTION == 0, "NO-OP action should be index 0"


# =============================================================================
# Wall Constants Tests (Section 6)
# =============================================================================


class TestWallConstants:
    """Test wall constants."""

    def test_default_wall_hp(self):
        """Verify default wall HP."""
        assert DEFAULT_WALL_HP == 1, "Default wall HP should be 1"


# =============================================================================
# Enemy Type Constants Tests (Section 6)
# =============================================================================


class TestEnemyTypeConstants:
    """Test enemy type constants."""

    def test_enemy_type_drop(self):
        """Verify Drop enemy type ID."""
        assert ENEMY_TYPE_DROP == 0, "Drop enemy type should be 0"

    def test_future_enemy_types(self):
        """Verify future enemy type IDs are sequential."""
        assert ENEMY_TYPE_DRIFTER == 1, "Drifter enemy type should be 1"
        assert ENEMY_TYPE_SEEKER == 2, "Seeker enemy type should be 2"
        assert ENEMY_TYPE_FLOOD == 3, "Flood enemy type should be 3"


# =============================================================================
# Reward Constants Tests (Section 8)
# =============================================================================


class TestRewardConstants:
    """Test reward constants."""

    def test_reward_core_breach(self):
        """Verify core breach reward."""
        assert REWARD_CORE_BREACH == -1.0, "Core breach reward should be -1.0"

    def test_reward_enemy_killed(self):
        """Verify enemy kill reward."""
        assert REWARD_ENEMY_KILLED == 1.0, "Enemy killed reward should be 1.0"

    def test_reward_tick_survived(self):
        """Verify per-tick survival reward."""
        assert REWARD_TICK_SURVIVED == 0.0, "Tick survived reward should be 0.0"


# =============================================================================
# Dtype Specifications Tests (Section 10)
# =============================================================================


class TestDtypeSpecifications:
    """Test dtype specifications."""

    def test_grid_dtype(self):
        """Verify grid dtype is valid numpy int8."""
        assert isinstance(GRID_DTYPE, np.dtype), "GRID_DTYPE should be a numpy dtype"
        assert GRID_DTYPE == np.dtype(np.int8), "GRID_DTYPE should be int8"

    def test_wall_hp_dtype(self):
        """Verify wall HP dtype is valid numpy uint8."""
        assert isinstance(WALL_HP_DTYPE, np.dtype), "WALL_HP_DTYPE should be a numpy dtype"
        assert WALL_HP_DTYPE == np.dtype(np.uint8), "WALL_HP_DTYPE should be uint8"

    def test_wall_state_dtype(self):
        """Verify wall state dtype is valid numpy bool."""
        assert isinstance(WALL_STATE_DTYPE, np.dtype), "WALL_STATE_DTYPE should be a numpy dtype"
        assert WALL_STATE_DTYPE == np.dtype(np.bool_), "WALL_STATE_DTYPE should be bool_"

    def test_cooldown_dtype(self):
        """Verify cooldown dtype is valid numpy uint16."""
        assert isinstance(COOLDOWN_DTYPE, np.dtype), "COOLDOWN_DTYPE should be a numpy dtype"
        assert COOLDOWN_DTYPE == np.dtype(np.uint16), "COOLDOWN_DTYPE should be uint16"

    def test_enemy_pos_dtype(self):
        """Verify enemy position dtype is valid numpy int16."""
        assert isinstance(ENEMY_POS_DTYPE, np.dtype), "ENEMY_POS_DTYPE should be a numpy dtype"
        assert ENEMY_POS_DTYPE == np.dtype(np.int16), "ENEMY_POS_DTYPE should be int16"

    def test_enemy_alive_dtype(self):
        """Verify enemy alive dtype is valid numpy bool."""
        assert isinstance(ENEMY_ALIVE_DTYPE, np.dtype), "ENEMY_ALIVE_DTYPE should be a numpy dtype"
        assert ENEMY_ALIVE_DTYPE == np.dtype(np.bool_), "ENEMY_ALIVE_DTYPE should be bool_"

    def test_enemy_type_dtype(self):
        """Verify enemy type dtype is valid numpy uint8."""
        assert isinstance(ENEMY_TYPE_DTYPE, np.dtype), "ENEMY_TYPE_DTYPE should be a numpy dtype"
        assert ENEMY_TYPE_DTYPE == np.dtype(np.uint8), "ENEMY_TYPE_DTYPE should be uint8"

    def test_enemy_tick_dtype(self):
        """Verify enemy spawn tick dtype is valid numpy uint32."""
        assert isinstance(ENEMY_TICK_DTYPE, np.dtype), "ENEMY_TICK_DTYPE should be a numpy dtype"
        assert ENEMY_TICK_DTYPE == np.dtype(np.uint32), "ENEMY_TICK_DTYPE should be uint32"


# =============================================================================
# Observation Constants Tests (Section 7)
# =============================================================================


class TestObservationConstants:
    """Test observation feature counts."""

    def test_obs_grid_state_size(self):
        """Verify grid state observation size."""
        assert OBS_GRID_STATE_SIZE == 117, "Grid state size should be 117 cells"

    def test_obs_wall_hp_size(self):
        """Verify wall HP observation size."""
        assert OBS_WALL_HP_SIZE == 117, "Wall HP size should be 117 cells"

    def test_obs_wall_armed_size(self):
        """Verify wall armed observation size."""
        assert OBS_WALL_ARMED_SIZE == 117, "Wall armed size should be 117 cells"

    def test_obs_cell_cd_size(self):
        """Verify cell cooldown observation size."""
        assert OBS_CELL_CD_SIZE == 117, "Cell CD size should be 117 cells"

    def test_obs_gcd_size(self):
        """Verify GCD observation size."""
        assert OBS_GCD_SIZE == 1, "GCD size should be 1"

    def test_obs_action_mask_size(self):
        """Verify action mask observation size."""
        assert OBS_ACTION_MASK_SIZE == 118, "Action mask size should be 118 actions"

    def test_obs_enemy_pos_size(self):
        """Verify enemy position observation size."""
        assert OBS_ENEMY_POS_SIZE == 40, "Enemy pos size should be 20 × 2 = 40"

    def test_obs_enemy_alive_size(self):
        """Verify enemy alive observation size."""
        assert OBS_ENEMY_ALIVE_SIZE == 20, "Enemy alive size should be 20"

    def test_obs_enemy_type_size(self):
        """Verify enemy type observation size."""
        assert OBS_ENEMY_TYPE_SIZE == 20, "Enemy type size should be 20"

    def test_observation_size(self):
        """Verify total observation size is 667."""
        assert OBSERVATION_SIZE == 667, (
            f"Observation size should be 667, got {OBSERVATION_SIZE}"
        )


# =============================================================================
# Validation Constants Tests
# =============================================================================


class TestValidationConstants:
    """Test validation constants."""

    def test_min_wall_hp(self):
        """Verify minimum wall HP."""
        assert MIN_WALL_HP == 0, "Minimum wall HP should be 0"

    def test_max_wall_hp(self):
        """Verify maximum wall HP (uint8 max)."""
        assert MAX_WALL_HP == 255, "Max wall HP should be 255 (uint8 max)"

    def test_max_cooldown(self):
        """Verify maximum cooldown (uint16 max)."""
        assert MAX_COOLDOWN == 65535, "Max cooldown should be 65535 (uint16 max)"

    def test_max_enemy_type(self):
        """Verify maximum enemy type (uint8 max)."""
        assert MAX_ENEMY_TYPE == 255, "Max enemy type should be 255 (uint8 max)"
