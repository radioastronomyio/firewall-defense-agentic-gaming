#!/usr/bin/env python3
"""
Script Name  : constants.py
Description  : Game constants and numpy dtype specifications
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-04
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Single source of truth for all game constants used throughout the core engine.
No magic numbers should exist elsewhere in the codebase. All values are derived
from the design document (docs/design-document.md) Sections 3, 4, 5, 7, 10, 14.

This module defines grid dimensions, cell states, position system constants,
cooldown values, action space parameters, reward values, and numpy dtype
specifications for all state arrays.

Usage
-----
    from src.core.constants import WIDTH, HEIGHT, GRID_DTYPE
    from src.core.constants import EMPTY, WALL, MAX_ENEMIES

Examples
--------
    from src.core.constants import GRID_SHAPE, GRID_DTYPE
    grid = np.zeros(GRID_SHAPE, dtype=GRID_DTYPE)
"""

# =============================================================================
# Imports
# =============================================================================

import numpy as np

# =============================================================================
# Grid Constants (Section 3)
# =============================================================================

# Grid dimensions: 13 columns × 9 rows
# Rationale: Odd width allows centered core, height keeps reward horizon tight
WIDTH: int = 13
HEIGHT: int = 9
TOTAL_CELLS: int = WIDTH * HEIGHT  # 117 cells

# Grid shape for NumPy arrays (H, W) - indexed as [y, x]
# AI NOTE: All grid arrays use (HEIGHT, WIDTH) shape and [y, x] indexing.
# This matches NumPy/image convention (row, column). Transposing to (W, H)
# or using [x, y] indexing will cause silent bugs in collision detection,
# observation building, and action mapping. See design doc Section 3.3.
GRID_SHAPE: tuple[int, int] = (HEIGHT, WIDTH)

# =============================================================================
# Cell States (Section 3)
# =============================================================================

# Cell content values for grid array
EMPTY: int = 0
WALL: int = 1

# =============================================================================
# Position System (Section 4)
# =============================================================================

# Half-cell position system eliminates float boundary bugs
# Grid height in half-cells: 9 cells × 2 = 18 half-cells
CORE_Y_HALF: int = 16  # Core breach threshold (row 8 reached)

# Fixed enemy slots for stable observation structure
MAX_ENEMIES: int = 20

# =============================================================================
# Movement Constants (Section 4)
# =============================================================================

# Enemy speed in half-cells per tick
# 1 half-cell/tick = 0.5 cells/tick
ENEMY_SPEED_HALF: int = 1

# =============================================================================
# Cooldown Constants (Section 5)
# =============================================================================

# Global Cooldown: frames after any action before next action allowed
# Prevents toggle-juggling, forces commitment to decisions
GCD_FRAMES: int = 10

# Cell Cooldown: frames after wall placement before cell can be used again
# ~150 frames ≈ 5 seconds at 30 ticks/s - commits agent to geometric decisions
CELL_CD_FRAMES: int = 150

# =============================================================================
# Episode Constants (Section 14)
# =============================================================================

# Default spawn interval in ticks
# ~30 ticks ≈ 1 second at 30 ticks/s
DEFAULT_SPAWN_INTERVAL: int = 30

# Maximum episode length in ticks
# Episode ends on core breach or reaching this limit
MAX_EPISODE_TICKS: int = 1000

# =============================================================================
# Action Constants (Section 5)
# =============================================================================

# Action space: Discrete(118)
# Action 0 = NO-OP (always valid)
# Actions 1-117 = Place wall at cell (x, y)
# Mapping: y, x = divmod(action - 1, WIDTH)
NUM_ACTIONS: int = TOTAL_CELLS + 1  # 117 cells + 1 NO-OP = 118
NO_OP_ACTION: int = 0

# =============================================================================
# Wall Constants (Section 6)
# =============================================================================

# Default wall HP - may need tuning for Tank enemies
DEFAULT_WALL_HP: int = 1

# =============================================================================
# Enemy Type Constants (Section 6)
# =============================================================================

# Enemy type IDs for enemy_type array
# Only Drop is implemented in prototype
ENEMY_TYPE_DROP: int = 0

# Future enemy types (not in prototype)
ENEMY_TYPE_DRIFTER: int = 1
ENEMY_TYPE_SEEKER: int = 2
ENEMY_TYPE_FLOOD: int = 3

# =============================================================================
# Reward Constants (Section 8)
# =============================================================================

# Prototype reward structure (binary, no shaping)
REWARD_CORE_BREACH: float = -1.0
REWARD_ENEMY_KILLED: float = 1.0
REWARD_TICK_SURVIVED: float = 0.0

# =============================================================================
# Dtype Specifications (Section 10)
# =============================================================================

# State array dtypes (Section 10.1)
GRID_DTYPE = np.dtype(np.int8)  # Cell contents: 0=empty, 1=wall
WALL_HP_DTYPE = np.dtype(np.uint8)  # Wall HP, 0 if no wall
WALL_STATE_DTYPE = np.dtype(np.bool_)  # Wall armed/pending status
COOLDOWN_DTYPE = np.dtype(np.uint16)  # Cell cooldowns and GCD

# Enemy array dtypes (Section 10.2)
ENEMY_POS_DTYPE = np.dtype(np.int16)  # y_half and x positions
ENEMY_ALIVE_DTYPE = np.dtype(np.bool_)  # Active mask
ENEMY_TYPE_DTYPE = np.dtype(np.uint8)  # Type ID (0=Drop, 1+=future)
ENEMY_TICK_DTYPE = np.dtype(np.uint32)  # Spawn tick for ordering

# =============================================================================
# Observation Constants (Section 7)
# =============================================================================

# Observation vector feature counts
# Total: 117×4 + 1 + 118 + 20×4 = 667 features
OBS_GRID_STATE_SIZE: int = TOTAL_CELLS  # 117
OBS_WALL_HP_SIZE: int = TOTAL_CELLS  # 117
OBS_WALL_ARMED_SIZE: int = TOTAL_CELLS  # 117
OBS_CELL_CD_SIZE: int = TOTAL_CELLS  # 117
OBS_GCD_SIZE: int = 1  # 1
OBS_ACTION_MASK_SIZE: int = NUM_ACTIONS  # 118
OBS_ENEMY_POS_SIZE: int = MAX_ENEMIES * 2  # 20×2 = 40
OBS_ENEMY_ALIVE_SIZE: int = MAX_ENEMIES  # 20
OBS_ENEMY_TYPE_SIZE: int = MAX_ENEMIES  # 20

OBSERVATION_SIZE: int = (
    OBS_GRID_STATE_SIZE
    + OBS_WALL_HP_SIZE
    + OBS_WALL_ARMED_SIZE
    + OBS_CELL_CD_SIZE
    + OBS_GCD_SIZE
    + OBS_ACTION_MASK_SIZE
    + OBS_ENEMY_POS_SIZE
    + OBS_ENEMY_ALIVE_SIZE
    + OBS_ENEMY_TYPE_SIZE
)  # 667

# =============================================================================
# Validation Constants
# =============================================================================

# Minimum wall HP (walls die at HP <= 0)
MIN_WALL_HP: int = 0

# Maximum values for validation
MAX_WALL_HP: int = 255  # uint8 max
MAX_COOLDOWN: int = 65535  # uint16 max
MAX_ENEMY_TYPE: int = 255  # uint8 max
