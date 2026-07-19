--=={ 4dlab-code-ingest: code_fix / audit }==--

## Step 0 — Target resolved
Package: C:\tmp\gfxskilltest\code_fix\
Type: .py package (3 files: __init__.py, dirty_module.py, clean_module.py)
Scope: production package only (no tests/, no research/)

## Step 1 — probe: SKIPPED
graphify CLI not available in this environment. Per skill rules: E/R/D rules
removed from audit scope since probe answers could not be verified.
- enum member sub-node: UNKNOWN (E skipped)
- # WHY: rationale node: UNKNOWN (R skipped)
- docstring/formula rationale node: UNKNOWN (D skipped)

## Step 2 — audit results

### Rule I — Explicit named imports
| file:line | rule | found | fix |
|-----------|------|-------|-----|
| dirty_module.py:2 | I | `from math import *` | Replace with explicit imports: `from math import <names used>` |

Count: 1 violation. clean_module.py uses explicit imports ✓. __init__.py uses explicit imports ✓.

### Rule A — Public surface via __all__
| file:line | rule | found | fix |
|-----------|------|-------|-----|
| __init__.py | A | No `__all__` defined | Add `__all__ = ["calculate_ratio", "SensorState", "describe_sensor", "normalize_reading"]` |

Count: 1 violation. clean_module.py has `__all__` ✓.

### Rule T — Type hints on public signatures
| file:line | rule | found | fix |
|-----------|------|-------|-----|
| dirty_module.py:4 | T | `def calculate_ratio(a, b):` — no param types, no return type | Add type hints: `def calculate_ratio(a: float, b: float) -> float:` |

Count: 1 violation. clean_module.py signatures are fully annotated ✓.

### Rule C — Static call sites
No violations found. No `getattr()`, `importlib`, `__import__`, or dispatch dict patterns detected.

### Rule S — Statically named symbols
No violations found. No `type()`, `exec()`, `eval()`, or runtime symbol construction detected.

### Rules E/R/D — skipped (probe unavailable)

## Audit summary
| Rule | Violations |
|------|-----------|
| I (star imports) | 1 |
| A (missing __all__) | 1 |
| T (missing type hints) | 1 |
| C (dynamic dispatch) | 0 |
| S (runtime symbols) | 0 |
| E (explicit enums) | skipped |
| R (rationale tags) | skipped |
| D (formula docstrings) | skipped |

Total: 3 machine-checkable violations found. Zero false positives on clean_module.py.
