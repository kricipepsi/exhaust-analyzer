# Baseline Audit Report - Run 2

Fixture: `C:\tmp\gfxskilltest\iteration-2\code_fix`

Scope: audited without reading or loading any 4dlab graph skill. Fixture source was not edited. Graphify was run only against a temp copy:
`C:\tmp\gfxskilltest\iteration-2\baseline-run-2-48400934653642238f086a83b33c309c`

## Verdict

The package is parseable and can be ingested into a basic AST-backed source graph, but it is not ready for high-fidelity static knowledge graph ingestion. Several constructs obscure public API boundaries, import provenance, call targets, type signatures, and runtime-created symbols.

## Probe Summary

- `python -m compileall -q` passed during syntax probing.
- `graphify` executable was not on PATH in PowerShell; `python -m graphify` was available.
- `python -m graphify update <temp-copy>` completed successfully.
- Graphify output: 16 nodes, 19 links, 4 communities.
- Generated `graph.json` SHA-256: `F3852FD7563918B5D0005B31643331D0CDE0E50BDC271F27024CF8F2AF02325C`.
- `python -m graphify explain RuntimeBuiltFault` returned: `No node matching 'RuntimeBuiltFault' found.`

## Findings

### High - Runtime-built symbol is invisible to the generated graph

`dynamic_runtime.py:22` creates `RuntimeBuiltFault` with `type("RuntimeBuiltFault", (), {"code": "P9999"})`.

This is a real runtime symbol, but it is not represented as a graph node in the generated graph. `python -m graphify explain RuntimeBuiltFault --graph <temp graph>` returned no matching node. A static source-code knowledge graph would miss the class-like symbol and its `code` attribute unless it has special handling for runtime construction.

### High - `getattr` dispatch hides call targets

`dynamic_runtime.py:13` assigns `handler = getattr(obj, name)`, and `dynamic_runtime.py:14` calls `handler(value)`.

The generated graph contains `route_with_getattr()` but only links it back to `dynamic_runtime.py` with `contains`. `python -m graphify explain route_with_getattr` reported degree 1 and no target function edges. The possible call target depends on runtime object state and string input, so static ingestion cannot confidently connect this route to concrete handlers.

### Medium - Dispatch dictionary call loses handler relationships

`dynamic_runtime.py:18` builds `handlers = {"a": handler_a, "b": handler_b}`, and `dynamic_runtime.py:19` calls `handlers[key](value)`.

The graph contains `handler_a()`, `handler_b()`, and `route_with_dispatch_dict()`, but `python -m graphify explain route_with_dispatch_dict` reported only the module `contains` edge. It did not emit references or call edges from the dispatching function to `handler_a()` or `handler_b()`. Static ingestion should either model this pattern explicitly or flag it as a dynamic call site.

### Medium - Package public API boundary is ambiguous

`__init__.py:1` documents that `__all__` is deliberately missing. `__init__.py:2` and `__init__.py:3` import public names into the package namespace.

An import probe showed that `from code_fix import *` exposes `SensorState`, `calculate_ratio`, `clean_module`, `describe_sensor`, `dirty_module`, and `normalize_reading`. Because there is no package-level `__all__`, the public API includes imported module bindings as well as intended functions/classes. This makes exported-symbol modeling ambiguous for graph ingestion.

### Medium - Star import obscures import provenance

`dirty_module.py:1` uses `from math import *`.

The generated graph did not include a `math` node or import edge for this star import. Star imports make name provenance broad and implicit, so a static graph cannot precisely know which imported names are available without module-specific expansion.

### Medium - Public function lacks type annotations

`dirty_module.py:4` defines `calculate_ratio(a, b)` without parameter or return annotations.

The graph captures `calculate_ratio()` as a node and package import target, but it has no type information for `a`, `b`, or the return value. That weakens typed relationship extraction and downstream reasoning over numeric behavior.

## Readiness Notes

Clean areas: `clean_module.py` has a module-level `__all__`, typed public functions, docstrings, and an enum relationship that graphify captured as `SensorState -> StrEnum`.

Blocking areas for static graph fidelity: runtime symbol creation, dynamic dispatch, missing package exports, star imports, and untyped public API. The package can be ingested, but the resulting graph should be treated as incomplete unless these patterns are fixed or explicitly modeled by the extractor.
