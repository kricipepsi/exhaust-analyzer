--=={ 4dlab-code-ingest: code_fix / probe+audit+report }==--

# With-skill evaluation run 2

Skill under test: `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\4dlab-code-prep`
Fixture package: `C:\tmp\gfxskilltest\iteration-2\code_fix`
Temp fixture copy audited: `C:\tmp\gfxskilltest\iteration-2\with_skill_work\run-2\fixture`
Temp probe directory: `C:\tmp\gfxskilltest\iteration-2\with_skill_work\run-2\probe`

No fixture source files or skill files were edited.

## Graphify version

`graphifyy` version: `0.8.36`
Python executable: `C:\Program Files\Python312\python.exe`

## Probe results

The probe was run as a code-only graphify extraction against the throwaway sample directory:

`python -m graphify extract C:\tmp\gfxskilltest\iteration-2\with_skill_work\run-2\probe --out C:\tmp\gfxskilltest\iteration-2\with_skill_work\run-2\probe --no-cluster`

Probe output: 6 nodes, 6 edges.

| Probe question | Answer | Evidence |
|---|---:|---|
| Enum member `STABILIZED_IDLE` present as its own node? | no | `graph.json` contains `RpmStateBucket`, `StrEnum`, and rationale nodes, but no `STABILIZED_IDLE` label. |
| `file_type: "rationale"` node for the `# WHY:` comment? | yes | Node label `# WHY: guard MAP=0 before division`, `file_type: rationale`, `source_location: L10`. |
| `rationale` node carrying the docstring/formula? | yes | Node label `VE = (maf * R * T) / (map_kpa * Vd * rpm).`, `file_type: rationale`, `source_location: L9`. |

Rules in scope after probe: I, A, T, C, S, R, D.
Rule E is out of scope for this graphify build because enum members were not emitted as separate nodes.

## Existing graph context

The fixture already included `graphify-out/graph.json`. A read-only query showed `dynamic_runtime.py` contains `handler_a()`, `handler_b()`, `route_with_getattr()`, and `route_with_dispatch_dict()`, with only file containment/import edges. `RuntimeBuiltFault` had no matching graph node, confirming the runtime-built symbol risk for rule S.

## Audit summary

| Rule | Count | Consumer protected |
|---|---:|---|
| A - Public surface via `__all__` | 1 | god-node ranking and entry-point nodes |
| I - Explicit named imports | 1 | import/call edge set |
| T - Type hints on public signatures | 1 | type-reference edges |
| C - Static call sites | 2 | call graph |
| S - Statically named symbols | 1 | node set and spot-check queries |
| R - Rationale tags | 1 | rationale nodes for non-obvious guards/equations |
| D - Formula docstrings | 1 | rationale nodes for formulas/validation methods |
| E - Explicit enums | skipped | skipped because probe returned no enum-member nodes |

## Audit hits

| file:line | rule | found | fix |
|---|---|---|---|
| `__init__.py:1` | A | Package initializer has no `__all__`. | Add an explicit reviewed `__all__` for the public package surface. |
| `dirty_module.py:1` | I | `from math import *` star import. | Replace with explicit named imports for the math symbols actually used, or remove the import if unused. |
| `dirty_module.py:4` | T | Public function `calculate_ratio(a, b)` has unannotated params `a`, `b`, and no return annotation. | Add concrete parameter and return annotations, for example numeric types that match intended inputs. |
| `dirty_module.py:4` | D | Formula-like ratio function has no docstring naming parameters or formula semantics. | Add a short formula/validation docstring that describes `a`, `b`, and zero-denominator behavior. |
| `dirty_module.py:5` | R | Division guard `if b else 0.0` has no `# WHY:` or `# NOTE:` rationale comment. | Add a rationale tag explaining the zero-denominator guard if this behavior is intentional. |
| `dynamic_runtime.py:13` | C | `getattr(obj, name)` hides the eventual call target from static analysis. | Advisory: prefer an explicit dispatch table or surface accepted names so graphify can recover call edges. |
| `dynamic_runtime.py:19` | C | `handlers[key](value)` performs callable dispatch through a dictionary. | Advisory: keep if intentional, but document accepted keys or use explicit wrapper calls when graph call edges matter. |
| `dynamic_runtime.py:22` | S | `RuntimeBuiltFault = type("RuntimeBuiltFault", (), {"code": "P9999"})` builds a queryable symbol at runtime. | Define a normal class if `RuntimeBuiltFault` is expected to appear as a stable graph node. |

## Report checklist

Non-greppable readiness checks for the coder:

- One responsibility per module. Consumer: cleaner Leiden/community clustering and fewer mixed-purpose communities.
- Folders should mirror architecture. Consumer: file/module nodes become useful navigation anchors.
- Descriptive stable names. Consumer: node labels are literal source names, so renames churn graph queries and saved references.
- Dynamic dispatch is advisory, not automatically wrong. Consumer: call graph completeness; keep legitimate indirection but make hidden targets reviewable.

Post-prep verification:

- Run graphify against a fresh temp copy of the package, not the fixture source or canonical graph directories.
- Compare node and edge counts before/after.
- Spot-check key symbols: `calculate_ratio()`, `route_with_getattr()`, `route_with_dispatch_dict()`, and `RuntimeBuiltFault`.
- Confirm the expected rationale nodes appear for any added `# WHY:`/`# NOTE:` comments and formula docstrings.
