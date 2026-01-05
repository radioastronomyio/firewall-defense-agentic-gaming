#!/usr/bin/env python3
"""
Script Name  : __init__.py
Description  : Core engine package - headless NumPy simulation
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-04
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Package marker for the core engine. Contains the headless NumPy simulation
that runs at >10k steps per second. No rendering, no Gymnasium dependencies.

Modules:
    constants   - Game constants and dtype specifications
    grid        - Grid state initialization and management
    walls       - Wall placement and validity checks
    enemies     - Enemy spawning, movement, and compaction (planned)
    collision   - Vectorized collision detection (planned)
    simulation  - Deterministic step loop (planned)
"""

# =============================================================================
# Public API
# =============================================================================

from src.core.constants import (
    CELL_CD_FRAMES,
    COOLDOWN_DTYPE,
    DEFAULT_SPAWN_INTERVAL,
    DEFAULT_WALL_HP,
    EMPTY,
    ENEMY_SPEED_HALF,
    ENEMY_TYPE_DROP,
    GCD_FRAMES,
    GRID_DTYPE,
    GRID_SHAPE,
    HEIGHT,
    MAX_ENEMIES,
    MAX_EPISODE_TICKS,
    NUM_ACTIONS,
    OBSERVATION_SIZE,
    REWARD_CORE_BREACH,
    REWARD_ENEMY_KILLED,
    REWARD_TICK_SURVIVED,
    TOTAL_CELLS,
    WALL,
    WALL_HP_DTYPE,
    WALL_STATE_DTYPE,
    WIDTH,
)
from src.core.cooldowns import apply_cooldowns, tick_cooldowns
from src.core.grid import GridState, create_grid_state
from src.core.walls import place_wall

__all__ = [
    # Cooldowns
    "apply_cooldowns",
    "tick_cooldowns",
    # Constants
    "CELL_CD_FRAMES",
    "COOLDOWN_DTYPE",
    "DEFAULT_WALL_HP",
    "DEFAULT_SPAWN_INTERVAL",
    "EMPTY",
    "ENEMY_SPEED_HALF",
    "ENEMY_TYPE_DROP",
    "GCD_FRAMES",
    "GRID_DTYPE",
    "GRID_SHAPE",
    "HEIGHT",
    "MAX_ENEMIES",
    "MAX_EPISODE_TICKS",
    "NUM_ACTIONS",
    "OBSERVATION_SIZE",
    "REWARD_CORE_BREACH",
    "REWARD_ENEMY_KILLED",
    "REWARD_TICK_SURVIVED",
    "TOTAL_CELLS",
    "WALL",
    "WALL_HP_DTYPE",
    "WALL_STATE_DTYPE",
    "WIDTH",
    # Grid
    "GridState",
    "create_grid_state",
    # Walls
    "place_wall",
]
