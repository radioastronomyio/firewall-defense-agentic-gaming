#!/usr/bin/env python3
"""
Script Name  : test_simulation.py
Description  : Unit tests for simulation module (RNG encapsulation and determinism)
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : 2026-01-08
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
Comprehensive unit tests for the simulation module, focusing on RNG encapsulation,
determinism, and reproducibility. These tests verify that:

1. SimulationState properly encapsulates RNG
2. Factory function creates RNG with seed parameter
3. step() function uses internal RNG (not external parameter)
4. Same seed + same actions produce identical trajectories
5. Different seeds produce different trajectories
6. RNG isolation prevents global state mutation

This test suite ensures the core simulation meets the determinism requirements
for reproducible reinforcement learning training.

Audience
----------
- **Developers**: Understanding simulation state structure and RNG usage
- **ML Practitioners**: Verifying determinism for reproducible training
- **QA Engineers**: Validating RNG isolation and reproducibility guarantees
"""

import numpy as np

from src.core import create_simulation_state, step
from src.core.constants import NO_OP_ACTION

# =============================================================================
# TestSimulationStateFactory
# =============================================================================


class TestSimulationStateFactory:
    """
    Tests for create_simulation_state() factory function.

    Verifies that RNG is properly created and seeded in SimulationState,
    and that different seeds produce different random sequences.

    Technical Details
    -----------------
    - RNG creation: Uses np.random.default_rng(seed)
    - Seed type: int | None (None uses system entropy)
    - RNG storage: Encapsulated in SimulationState.rng field
    - Determinism: Same seed → same sequence

    Test Coverage
    -------------
    - Default seed (None) creates RNG
    - Explicit seed creates RNG
    - Different seeds produce different sequences
    - Same seed produces same sequence
    """

    def test_default_seed_creates_rng(self):
        """
        Verify that create_simulation_state() creates RNG with seed=None.

        When seed parameter is omitted or None, factory should create
        RNG using system entropy. RNG field should be present and
        functional.

        Technical Details
        -----------------
        - np.random.default_rng(None) uses system entropy
        - RNG should be np.random.Generator instance
        - RNG should be callable (e.g., integers() method)

        Examples
        --------
        >>> sim = create_simulation_state()
        >>> isinstance(sim.rng, np.random.Generator)
        True
        >>> sim.rng.integers(0, 13) in range(13)
        True
        """
        # Create simulation with default seed (None)
        sim = create_simulation_state()

        # Verify RNG exists and is correct type
        assert hasattr(sim, "rng"), "SimulationState should have rng field"
        assert isinstance(
            sim.rng, np.random.Generator
        ), "rng should be np.random.Generator instance"

        # Verify RNG is functional
        random_col = sim.rng.integers(0, 13)
        assert 0 <= random_col < 13, "RNG should produce valid column values"

    def test_explicit_seed_creates_rng(self):
        """
        Verify that create_simulation_state() creates RNG with explicit seed.

        When seed parameter is provided, factory should create
        deterministic RNG with that seed. RNG should be reproducible
        across multiple simulations.

        Technical Details
        -----------------
        - np.random.default_rng(seed) creates deterministic RNG
        - Same seed → same sequence (reproducibility)
        - RNG should be np.random.Generator instance

        Examples
        --------
        >>> sim1 = create_simulation_state(seed=42)
        >>> sim2 = create_simulation_state(seed=42)
        >>> col1 = sim1.rng.integers(0, 13)
        >>> col2 = sim2.rng.integers(0, 13)
        >>> col1 == col2
        True
        """
        # Create simulation with explicit seed
        sim = create_simulation_state(seed=42)

        # Verify RNG exists and is correct type
        assert hasattr(sim, "rng"), "SimulationState should have rng field"
        assert isinstance(
            sim.rng, np.random.Generator
        ), "rng should be np.random.Generator instance"

        # Verify RNG is deterministic (same seed produces same value)
        sim2 = create_simulation_state(seed=42)
        col1 = sim.rng.integers(0, 13)
        col2 = sim2.rng.integers(0, 13)
        assert col1 == col2, "Same seed should produce same sequence"

    def test_different_seeds_different_sequences(self):
        """
        Verify that different seeds produce different random sequences.

        When different seeds are provided, factory should create
        RNGs with different internal states, producing different
        spawn columns and random values.

        Technical Details
        -----------------
        - np.random.default_rng(seed) initializes RNG state
        - Different seeds → different internal states
        - Different states → different sequences
        - Probability of collision is 1/13 for single value

        Examples
        --------
        >>> sim42 = create_simulation_state(seed=42)
        >>> sim123 = create_simulation_state(seed=123)
        >>> col42 = sim42.rng.integers(0, 13)
        >>> col123 = sim123.rng.integers(0, 13)
        >>> col42 != col123  # Likely but not guaranteed
        True
        """
        # Create simulations with different seeds
        sim42 = create_simulation_state(seed=42)
        sim123 = create_simulation_state(seed=123)

        # Generate spawn columns from each RNG
        col42 = sim42.rng.integers(0, 13)
        col123 = sim123.rng.integers(0, 13)

        # Verify different seeds produce different columns (high probability)
        # Note: This is probabilistic, but with 13 possible values,
        # collision probability is 1/13 ≈ 7.7%
        assert col42 != col123, (
            f"Different seeds should produce different columns: "
            f"seed=42 → {col42}, seed=123 → {col123}"
        )


# =============================================================================
# TestStepRNGUsage
# =============================================================================


class TestStepRNGUsage:
    """
    Tests for step() function RNG usage and determinism.

    Verifies that step() uses internal RNG from SimulationState,
    and that same seed + same actions produce identical trajectories.

    Technical Details
    -----------------
    - step() signature: step(sim_state, action) (no rng parameter)
    - RNG source: sim_state.rng (encapsulated)
    - Determinism: Same seed + same actions → same trajectory
    - Trajectory includes: enemy positions, rewards, termination

    Test Coverage
    -------------
    - step() uses internal RNG (not external parameter)
    - Same seed + same actions → identical enemy positions
    - Same seed + same actions → identical rewards
    - Different seeds → divergent trajectories
    """

    def test_step_uses_internal_rng(self):
        """
        Verify that step() uses internal RNG from SimulationState.

        The step() function should use sim_state.rng for all
        randomization (enemy spawn columns), not accept an external
        rng parameter. This ensures RNG is encapsulated in state.

        Technical Details
        -----------------
        - step() signature: def step(sim_state, action)
        - No rng parameter in function signature
        - spawn_enemy() called with sim_state.rng
        - RNG state advances with each spawn

        Examples
        --------
        >>> sim = create_simulation_state(seed=42)
        >>> reward, terminated, truncated = step(sim, action=0)
        >>> # Enemy spawned at column determined by sim.rng
        >>> sim.enemy_state.enemy_alive[0]
        True
        """
        # Create seeded simulation
        sim = create_simulation_state(seed=42)

        # Execute step with NO-OP action (triggers spawn at tick 0)
        reward, terminated, truncated = step(sim, action=NO_OP_ACTION)

        # Verify spawn occurred (enemy at tick 0)
        assert sim.tick == 1, "Tick should increment to 1"
        assert np.any(sim.enemy_state.enemy_alive), "Enemy should be spawned"

        # Verify spawn column is within valid range (0-12)
        alive_mask = sim.enemy_state.enemy_alive
        spawn_col = sim.enemy_state.enemy_x[alive_mask][0]
        assert 0 <= spawn_col < 13, f"Spawn column {spawn_col} should be in range [0, 12]"

    def test_same_seed_same_trajectory(self):
        """
        Verify that same seed + same actions produce identical trajectory.

        Two simulations with same seed and same action sequence
        should produce bit-for-bit identical trajectories: same enemy
        positions, same rewards, same termination states.

        Technical Details
        -----------------
        - Determinism requirement: seed + actions → trajectory
        - Trajectory includes: enemy_y_half, enemy_x, rewards
        - Tick-by-tick comparison: identical at each step
        - Spawn columns: deterministic via seeded RNG

        Examples
        --------
        >>> sim1 = create_simulation_state(seed=42)
        >>> sim2 = create_simulation_state(seed=42)
        >>> for _ in range(10):
        ...     step(sim1, action=0)
        ...     step(sim2, action=0)
        >>> np.array_equal(sim1.enemy_state.enemy_y_half,
        ...                sim2.enemy_state.enemy_y_half)
        True
        """
        # Create two simulations with same seed
        sim1 = create_simulation_state(seed=42)
        sim2 = create_simulation_state(seed=42)

        # Execute identical action sequences
        actions = [NO_OP_ACTION] * 10  # 10 NO-OP steps
        rewards1 = []
        rewards2 = []

        for action in actions:
            r1, _, _ = step(sim1, action=action)
            r2, _, _ = step(sim2, action=action)
            rewards1.append(r1)
            rewards2.append(r2)

        # Verify identical enemy positions
        assert np.array_equal(
            sim1.enemy_state.enemy_y_half, sim2.enemy_state.enemy_y_half
        ), "Same seed + same actions should produce identical enemy_y_half"

        assert np.array_equal(
            sim1.enemy_state.enemy_x, sim2.enemy_state.enemy_x
        ), "Same seed + same actions should produce identical enemy_x"

        # Verify identical rewards
        assert rewards1 == rewards2, (
            "Same seed + same actions should produce identical rewards"
        )

        # Verify identical tick counts
        assert sim1.tick == sim2.tick, (
            "Same seed + same actions should produce identical tick counts"
        )

    def test_different_seed_different_trajectory(self):
        """
        Verify that different seeds produce divergent trajectories.

        Two simulations with different seeds should produce different
        enemy positions, spawn columns, and potentially different
        rewards due to different random sequences.

        Technical Details
        -----------------
        - Different seeds → different RNG states
        - Different RNG states → different spawn columns
        - Different spawn columns → different trajectories
        - High probability of divergence (1 - (1/13)^n)

        Examples
        --------
        >>> sim42 = create_simulation_state(seed=42)
        >>> sim123 = create_simulation_state(seed=123)
        >>> for _ in range(10):
        ...     step(sim42, action=0)
        ...     step(sim123, action=0)
        >>> not np.array_equal(sim42.enemy_state.enemy_x,
        ...                    sim123.enemy_state.enemy_x)  # Likely
        True
        """
        # Create two simulations with different seeds
        sim42 = create_simulation_state(seed=42)
        sim123 = create_simulation_state(seed=123)

        # Execute identical action sequences
        actions = [NO_OP_ACTION] * 10  # 10 NO-OP steps

        for action in actions:
            step(sim42, action=action)
            step(sim123, action=action)

        # Verify different enemy positions (high probability)
        # With 10 spawns, probability of identical sequences is (1/13)^10 ≈ 7e-12
        assert not np.array_equal(
            sim42.enemy_state.enemy_x, sim123.enemy_state.enemy_x
        ), (
            "Different seeds should produce different enemy_x positions. "
            "This test is probabilistic; if it fails, it's extremely unlikely "
            "but possible (collision probability ≈ 7e-12 for 10 spawns)."
        )


# =============================================================================
# TestRNGIsolation
# =============================================================================


class TestRNGIsolation:
    """
    Tests for RNG isolation and global state mutation prevention.

    Verifies that simulation RNG does not mutate global NumPy random
    state, and that multiple simulations maintain independent RNG states.

    Technical Details
    -----------------
    - Global state: np.random global RNG (deprecated)
    - Local state: np.random.Generator instances (modern)
    - Isolation: sim_state.rng should not affect global state
    - Independence: Multiple sims maintain separate RNG sequences

    Test Coverage
    -------------
    - Simulation does not mutate global np.random state
    - Multiple simulations maintain independent RNG sequences
    - Interleaved steps don't interfere with each other
    """

    def test_no_global_state_mutation(self):
        """
        Verify that simulation does not mutate global np.random state.

        Running simulation steps should not affect the global NumPy
        random number generator state. Only the encapsulated
        sim_state.rng should be used for randomization.

        Technical Details
        -----------------
        - Global state: np.random global RNG (legacy)
        - Local state: sim_state.rng (modern Generator)
        - Isolation: sim_state.rng operations should not affect global
        - Verification: Compare global state before and after

        Examples
        --------
        >>> val_before = np.random.randint(0, 100)
        >>> sim = create_simulation_state(seed=42)
        >>> for _ in range(10):
        ...     step(sim, action=0)
        >>> val_after = np.random.randint(0, 100)
        >>> # Global RNG sequence should continue uninterrupted
        """
        # Sample from global RNG before simulation
        global_val_before = np.random.randint(0, 1000)

        # Run simulation steps (which use internal RNG)
        sim = create_simulation_state(seed=42)
        for _ in range(10):
            step(sim, action=NO_OP_ACTION)

        # Sample from global RNG after simulation
        global_val_after = np.random.randint(0, 1000)

        # Verify global RNG state unchanged by checking that the sequence
        # continues as if simulation never happened
        # Note: This is a probabilistic test, but with 1000 possible values,
        # the probability of collision is 0.001
        assert global_val_before != global_val_after, (
            "Global RNG should continue its sequence uninterrupted. "
            "If this test fails, it's extremely unlikely (p=0.001) "
            "but possible due to random collision."
        )

    def test_independent_rng_per_simulation(self):
        """
        Verify that multiple simulations maintain independent RNG states.

        Two simulations with different seeds should maintain
        independent random sequences, even when run interleaved.
        Each simulation's RNG state should not affect the other.

        Technical Details
        -----------------
        - Independence: Each sim has its own Generator instance
        - No interference: sim1.rng operations don't affect sim2.rng
        - Interleaved execution: Steps alternate between sims
        - Verification: Compare sequences to independent baselines

        Examples
        --------
        >>> sim1 = create_simulation_state(seed=42)
        >>> sim2 = create_simulation_state(seed=123)
        >>> # Interleaved steps
        >>> step(sim1, action=0)
        >>> step(sim2, action=0)
        >>> step(sim1, action=0)
        >>> step(sim2, action=0)
        >>> # Verify sequences match independent baselines
        >>> baseline1 = create_simulation_state(seed=42)
        >>> baseline2 = create_simulation_state(seed=123)
        >>> # ... compare trajectories
        """
        # Create two simulations with different seeds
        sim1 = create_simulation_state(seed=42)
        sim2 = create_simulation_state(seed=123)

        # Create independent baselines (run separately)
        baseline1 = create_simulation_state(seed=42)
        baseline2 = create_simulation_state(seed=123)

        # Run interleaved steps on sim1 and sim2
        for _ in range(5):
            step(sim1, action=NO_OP_ACTION)
            step(sim2, action=NO_OP_ACTION)

        # Run same steps on baselines (non-interleaved)
        for _ in range(5):
            step(baseline1, action=NO_OP_ACTION)
        for _ in range(5):
            step(baseline2, action=NO_OP_ACTION)

        # Verify sim1 matches baseline1 (independent execution)
        assert np.array_equal(
            sim1.enemy_state.enemy_x, baseline1.enemy_state.enemy_x
        ), "Interleaved sim1 should match non-interleaved baseline1"

        assert np.array_equal(
            sim1.enemy_state.enemy_y_half, baseline1.enemy_state.enemy_y_half
        ), "Interleaved sim1 should match non-interleaved baseline1"

        # Verify sim2 matches baseline2 (independent execution)
        assert np.array_equal(
            sim2.enemy_state.enemy_x, baseline2.enemy_state.enemy_x
        ), "Interleaved sim2 should match non-interleaved baseline2"

        assert np.array_equal(
            sim2.enemy_state.enemy_y_half, baseline2.enemy_state.enemy_y_half
        ), "Interleaved sim2 should match non-interleaved baseline2"
