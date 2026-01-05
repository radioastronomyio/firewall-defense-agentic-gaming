# Grid Defense RL Product

## Vision

A watchable RL training pipeline where viewers can see an agent learn, fail, and adapt through curriculum learning—with saliency visualization showing *what* the agent attends to at each moment.

## Target Audience

| Audience | Use Case |
|----------|----------|
| ML Learners | Watch RL training with xAI visualization |
| RL Practitioners | Study curriculum learning and saliency methods |
| Content Creators | Fork for educational YT/streaming content |
| Maintainer | Portfolio piece at AI + gaming intersection |

## Content Format

- **Length:** 15-minute episodes
- **Platform:** YouTube
- **Style:** Educational, "watch and learn"
- **Hook:** Agent breaks when new enemy appears → retrains → adapts

## Deliverables

| Phase | Deliverable |
|-------|-------------|
| Prototype | Working `GridDefenseEnv`, >10k SPS, random agent passes |
| Phase 1 | PPO trained on Drop, baseline metrics |
| Phase 2 | Curriculum with Drifter, failure + adaptation recording |
| Phase 3 | Full enemy roster (Seeker, Flood) |
| Phase 4 | Saliency visualization, video production |

## Success Metrics

| Metric | Target |
|--------|--------|
| Headless SPS | > 10,000 |
| Gymnasium compliance | Passes `check_env()` |
| Determinism | Same seed + actions = same trajectory |
| Episode length | ~15 minutes of interesting content per enemy introduction |

## Non-Goals

- Production game (this is educational content, not a shipped product)
- Real cybersecurity simulation (firewall framing is thematic)
- Mobile deployment (desktop/cluster only)
- Real-time multiplayer (single-agent RL)
