# Grid Defense RL Tech Stack

## Core Technologies

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| Language | Python | 3.11+ | Primary language |
| Simulation | NumPy | Latest | Headless core arrays |
| RL Interface | Gymnasium | 0.29+ | Environment API |
| RL Algorithm | Stable-Baselines3 | 2.x | PPO implementation |
| Action Masking | SB3-Contrib | Latest | MaskablePPO |
| Deep Learning | PyTorch | 2.x | Neural network backend |
| Testing | pytest | Latest | Test framework |

## Future Technologies (Phase 4+)

| Component | Technology | Purpose |
|-----------|------------|---------|
| Visualization | Python Arcade | 2D rendering |
| Shaders | OpenGL/GLSL | Bloom, CRT effects |
| Video | FFmpeg | Frame assembly |

## Development Tools

| Tool | Purpose |
|------|---------|
| VS Code | Primary IDE |
| Ruff | Linting + formatting |
| mypy | Type checking |
| pre-commit | Git hooks |

## Hardware

| Machine | Specs | Use |
|---------|-------|-----|
| radio-gpu01 | A4000 16GB, 12 vCPU, 48GB RAM | Training |
| Desktop | RTX 3080, i9, 64GB RAM | Development, rendering |
| radio-fs02 | NFS/SMB storage | Checkpoint transfer |

## Key Constraints

### Performance

- Target: >10k steps/second headless
- Observation: 667 features (MLP, not CNN)
- Action space: 118 discrete (NO-OP + 117 cells)

### Determinism

- Fixed-point positions (half-cell integers)
- Explicit step ordering
- Seeded RNG for reproducibility

### Conventions

- Arrays: `(H, W)` = `(9, 13)`, indexed `[y, x]`
- Positions: `enemy_y_half` (int16), cell = `y_half // 2`
- Dtypes: explicit (`np.int8`, `np.float32`)

## Dependencies (Prototype)

```
numpy>=1.24
gymnasium>=0.29
stable-baselines3>=2.0
sb3-contrib>=2.0
torch>=2.0
pytest>=7.0
```
