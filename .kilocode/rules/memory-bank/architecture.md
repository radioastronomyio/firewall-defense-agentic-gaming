# Grid Defense RL Architecture

## Decoupled Simulation Pattern

Three layers that never overlap:

| Layer | Role | Runtime |
|-------|------|---------|
| **Ground Truth** | Headless NumPy core (`src/core/`). Pure math, no pixels. | Training (>10k SPS) |
| **Interface** | Gymnasium wrapper (`src/env/`). State → normalized observation. | Training |
| **Observer** | Offline renderer (future). Reconstructs from seed + action log. | Video only |

## Directory Structure

```
firewall-defense-agentic-gaming/
├── src/
│   ├── core/             # Headless simulation (grid, enemies, walls)
│   ├── env/              # Gymnasium wrapper
│   └── tests/            # Test suite
├── notebooks/            # Experimentation
├── configs/              # Hyperparameters (YAML)
├── scripts/              # Training entrypoints
├── renders/              # Video output (gitignored)
├── docs/                 # Documentation
│   └── documentation-standards/
├── scratch/              # Working documents
├── work-logs/            # Phase documentation
└── .kilocode/            # Agent context
```

## Data Flow

```
Training:
  core/ → env/ → SB3 PPO → checkpoints/

Visualization (future):
  checkpoints/ + episode_log → observer/ → renders/
```

## Key Design Decisions

1. **NumPy-only core** — No PyTorch in simulation. Keeps training fast.
2. **Fixed-point positions** — Half-cell integers, not floats. Eliminates boundary bugs.
3. **`[y, x]` indexing** — Arrays are `(H, W)` = `(9, 13)`. Idiomatic NumPy.
4. **20 fixed enemy slots** — No variable-length arrays. Zero-padded, spawn-order sorted.
5. **Action masking** — Invalid actions masked via `info["action_mask"]`.
6. **1-tick wall arming** — Anti-triviality rule. Forces prediction over reaction.

## Hardware Workflow

| Phase | Hardware | Rationale |
|-------|----------|-----------|
| Training | radio-gpu01 (A4000, 12 vCPU) | GPU for gradients, CPU for rollouts |
| Rendering | Win11 desktop (RTX 3080) | Rasterization + saliency inference |
| Transfer | SMB via radio-fs02 | Compact logs (seed + actions), not video |
