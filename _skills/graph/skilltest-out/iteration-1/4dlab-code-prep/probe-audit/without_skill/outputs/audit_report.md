# Audit Report: code_fix Package

**Package path:** `C:\tmp\gfxskilltest\code_fix\`
**Files audited:** `__init__.py`, `dirty_module.py`, `clean_module.py`
**Audit date:** 2026-06-09

---

## Summary of Findings

| # | Rule | Severity | File | Line(s) | Description |
|---|------|----------|------|---------|-------------|
| 1 | I (Star import) | HIGH | `dirty_module.py` | 2 | `from math import *` obscures which symbols originate from `math`. A tree-sitter AST parser cannot resolve re-exports through star imports without evaluating the source module, breaking cross-file symbol resolution. |
| 2 | A (Missing `__all__`) | HIGH | `__init__.py` | (entire file) | `__init__.py` imports `calculate_ratio`, `SensorState`, and `describe_sensor` but defines no `__all__`. Without `__all__`, graphify's public-API detection must fall back to `dir()` or all non-underscore names, yielding a noisier, less accurate surface. |
| 3 | T (Missing type hints) | MEDIUM | `dirty_module.py` | 4 | `calculate_ratio(a, b)` has no parameter type hints and no return type annotation. Graphify relies on type annotations to label edges (e.g., `int -> float`) and to disambiguate overloaded signatures. Missing hints produce generic `Any` edges that degrade query precision. |

---

## Findings by Rule

### Rule I -- Star Imports

**Finding 1: `from math import *` in `dirty_module.py:2`**

```
from math import *  # seeded violation: rule I (star import)
```

**Impact on code-map quality:**
- The symbol table of `dirty_module.py` is implicitly extended with every public name in `math` (approximately 50 symbols: `sin`, `cos`, `sqrt`, `pi`, `e`, `floor`, `ceil`, etc.).
- A static analyzer cannot determine which of those symbols are actually *used* vs. merely imported, inflating the module's effective interface.
- If another module does `from dirty_module import *`, the contamination propagates transitively.

**Recommended fix:** Replace with explicit imports:
```
from math import <only the names actually needed>
```

---

### Rule A -- Missing `__all__` in `__init__.py`

**Finding 2: No `__all__` defined in `__init__.py`**

```python
# Deliberately missing __all__ (seeded violation: rule A)
from .dirty_module import calculate_ratio
from .clean_module import SensorState, describe_sensor
```

**Impact on code-map quality:**
- The package's public API surface is undefined. A graph builder must either:
  - Treat every non-underscore name in `__init__.py` as public (including re-exported symbols, which is noisy).
  - Walk into submodules, losing the distinction between "intended public API" and "internal implementation detail."
- `calculate_ratio` from `dirty_module` and `SensorState`/`describe_sensor` from `clean_module` are re-exported, but a consumer reading only the graph cannot tell which are canonical entry points.
- `normalize_reading` is declared in `clean_module`'s own `__all__` but is NOT re-exported by the package's `__init__.py`. Without package-level `__all__`, this is not visible in the graph, but the lack of `__all__` makes the situation ambiguous rather than explicit.

**Recommended fix:** Add an explicit `__all__`:
```python
__all__ = ["calculate_ratio", "SensorState", "describe_sensor"]
```

---

### Rule T -- Public Functions Without Type Hints

**Finding 3: `calculate_ratio` lacks type annotations in `dirty_module.py:4`**

```python
def calculate_ratio(a, b):  # seeded violation: rule T (no type hints on public def)
    return a / b if b else 0.0
```

**Impact on code-map quality:**
- Both parameters (`a`, `b`) and the return type are unannotated. The graph edge for this function will be typed as `(Any, Any) -> Any`, providing no signal for type-based queries (e.g., "find all functions that consume a `float` and produce a `float`").
- The docstring is also missing, removing another potential source of semantic metadata.

**Recommended fix:**
```python
def calculate_ratio(a: float, b: float) -> float:
    """Return a / b, or 0.0 if b is zero."""
    return a / b if b else 0.0
```

---

## Rules With No Findings

### Rule D -- Dynamic Dispatch Hiding Call Sites

No dynamic dispatch patterns found in any file. Specifically, none of the following were detected:
- `getattr(obj, name)(...)` or `getattr(obj, name)()` patterns
- Decorator-based dispatch tables (`@register`, singletons with decorator registries)
- `eval()` or `exec()` calls
- Callable stored as dict values looked up at runtime
- `functools.singledispatch` or similar runtime-overload mechanisms

### Rule R -- Runtime Symbol Construction

No runtime symbol construction found in any file. Specifically, none of the following were detected:
- `setattr(module, name, value)` or `setattr(cls, name, value)`
- `globals()[name] = value` or `locals()[name] = value`
- `type(name, bases, namespace)` dynamic class creation
- `__import__(string_name)` or `importlib.import_module(string_name)` with computed names
- `exec()` or `compile()` building code objects at runtime

---

## File-by-File Summary

### `__init__.py` -- 1 finding
- Missing `__all__` (HIGH)

### `dirty_module.py` -- 2 findings
- Star import from `math` (HIGH)
- `calculate_ratio` missing type hints (MEDIUM)

### `clean_module.py` -- 0 findings
- Has `__all__` with explicit exports ✓
- All public functions have type hints ✓
- No star imports ✓
- No dynamic dispatch or runtime symbol construction ✓

---

## Overall Package Grade

| Metric | Score |
|--------|-------|
| Star imports | FAIL -- 1 instance |
| `__all__` hygiene | FAIL -- `__init__.py` missing |
| Type hint coverage | PARTIAL -- 1 of 3 public functions untyped |
| Dynamic dispatch | PASS -- none detected |
| Runtime symbol construction | PASS -- none detected |

The `clean_module.py` file serves as a model reference. The two violations in `dirty_module.py` and `__init__.py` would cause graphify to produce incomplete edges and an inaccurate public-API boundary for this package.
