# Python Script Header Template

> Template Version: 1.0  
> Applies To: All `.py` files  
> Repository: https://github.com/radioastronomyio/firewall-defense-agentic-gaming  
> Last Updated: 2026-01-04

---

## Template

```python
#!/usr/bin/env python3
"""
Script Name  : script_name.py
Description  : [One-line description of what the script does]
Repository   : firewall-defense-agentic-gaming
Author       : VintageDon (https://github.com/vintagedon)
Created      : YYYY-MM-DD
Link         : https://github.com/radioastronomyio/firewall-defense-agentic-gaming

Description
-----------
[2-4 sentences explaining the script's purpose, what it operates on,
and what outputs it produces. Include any important behavioral notes.]

Usage
-----
    python script_name.py [options]

Examples
--------
    python script_name.py
        [Description of what this invocation does]

    python script_name.py --verbose
        [Description of what this invocation does]
"""

# =============================================================================
# Imports
# =============================================================================

from pathlib import Path

import numpy as np

# =============================================================================
# Configuration
# =============================================================================

# Grid dimensions (H, W) - index as [y, x]
GRID_HEIGHT = 9
GRID_WIDTH = 13

# =============================================================================
# Functions
# =============================================================================


def main() -> None:
    """Entry point for script execution."""
    pass


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    main()
```

---

## Field Descriptions

| Field | Required | Description |
|-------|----------|-------------|
| Script Name | Yes | Filename for reference (snake_case) |
| Description | Yes | Single line, verb-led description |
| Repository | Yes | `firewall-defense-agentic-gaming` |
| Author | Yes | Name with GitHub profile link |
| Created | Yes | Creation date (YYYY-MM-DD) |
| Link | Yes | `https://github.com/radioastronomyio/firewall-defense-agentic-gaming` |
| Description section | Yes | Expanded multi-line explanation |
| Usage section | Yes | Command syntax |
| Examples section | Yes | At least one usage example |

---

## Section Comments

Use banner comments to separate logical sections:

```python
# =============================================================================
# Section Name
# =============================================================================
```

Standard sections (in order):

1. **Imports** — Standard library, third-party, local imports (in that order)
2. **Configuration** — Constants, paths, settings
3. **Functions** — Function and class definitions
4. **Entry Point** — `if __name__ == "__main__":` block

---

## Docstring Style

Use NumPy-style docstrings for functions:

```python
def validate_action(
    action: int,
    action_mask: np.ndarray
) -> bool:
    """
    Validate an action against the current action mask.

    Parameters
    ----------
    action : int
        Action index (0 = NO-OP, 1-117 = place wall at cell).
    action_mask : np.ndarray
        Boolean array of shape (118,) indicating valid actions.

    Returns
    -------
    bool
        True if action is valid, False otherwise.

    Raises
    ------
    ValueError
        If action is out of range [0, 117].
    """
    pass
```

---

## Project-Specific Conventions

### Coordinate Convention

Always use `[y, x]` indexing for grid arrays:

```python
# Correct
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)
grid[y, x] = WALL

# Wrong (will cause bugs)
grid[x, y] = WALL
```

### Fixed-Point Positions

Use half-cell integers for enemy positions:

```python
# Position in half-cells (not floats)
enemy_y_half: np.ndarray  # dtype=np.int16
cell_y = enemy_y_half // 2
```

### Type Hints

Always include type hints for function parameters and returns:

```python
def step(self, action: int) -> tuple[np.ndarray, float, bool, bool, dict]:
    ...
```

---

## Notes

- Use `#!/usr/bin/env python3` for portability
- Module docstring goes immediately after shebang
- Keep Description line under 80 characters
- Use present tense, active voice ("Validates..." not "This script validates...")
- Use `pathlib.Path` instead of string paths
- Follow PEP 8 style guide
- Use NumPy dtypes explicitly (`np.int8`, `np.float32`)
