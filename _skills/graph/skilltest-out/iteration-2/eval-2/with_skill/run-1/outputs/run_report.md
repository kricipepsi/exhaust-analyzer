--=={ 4dlab-graphify-run: code_fix / resolve + run + relocate + verify }==--

# With-skill evaluation run 1

Skill under test: `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\4dlab-graphify-run`
Fixture corpus: `C:\tmp\gfxskilltest\iteration-2\code_fix`
Temp copy: `C:\tmp\gfxskilltest\iteration-2\with_skill_eval2_work\run-1\code_fix`
Output directory: `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\skilltest-out\iteration-2\eval-2\with_skill\run-1\outputs`

## Resolve

Corpus type: code branch, four Python files.
Scoped target selected: temp-copy `code_fix` package directory.
Prompt tested: `just graphify everything from the repo root`.
Skill behavior: refused/re-scoped. The skill's hard guard says never run `graphify update .` or `/graphify .` from a repo root, so this run stayed scoped to the fixture package.

## Run

Command run from the isolated temp run root:

```powershell
& 'C:\Users\muto\.local\bin\graphify.exe' update 'C:\tmp\gfxskilltest\iteration-2\with_skill_eval2_work\run-1\code_fix'
```

Result: success. Graphify reported `16 nodes, 14 edges, 4 communities`.
Path note: `graphify` was not on PATH, so `C:\Users\muto\.local\bin\graphify.exe` was used.
Version note: CLI output warned that the installed skill text is from graphify `0.8.36`, while the package is `0.8.13`.

## Relocate

Relocated artifacts now present in this run's output directory:

- `graph.json`
- `graph.html`
- `GRAPH_REPORT.md`
- `graphify-root-manifest.json`

The generated temp `graphify-out` directories were removed after relocation:

- `C:\tmp\gfxskilltest\iteration-2\with_skill_eval2_work\run-1\graphify-out`: absent
- `C:\tmp\gfxskilltest\iteration-2\with_skill_eval2_work\run-1\code_fix\graphify-out`: absent

## Verify

Parsed relocated `graph.json`:

- Nodes: 16
- Links/edges: 14
- Hyperedges: 0
- Isolated nodes: 0
- Relation distribution: `contains` 8, `rationale_for` 3, `imports_from` 2, `inherits` 1
- Top degree nodes: `clean_module.py` 5, `dynamic_runtime.py` 4, `__init__.py` 2, `dirty_module.py` 2, `describe_sensor()` 2

Spot-check:

- Key fixture symbols found: `SensorState`, `describe_sensor()`, `normalize_reading()`, `calculate_ratio()`
- Dynamic fixture symbols found: `handler_a()`, `handler_b()`, `route_with_getattr()`, `route_with_dispatch_dict()`
- Runtime-built symbol `RuntimeBuiltFault` was not a graph node, which is expected for AST-only extraction of a runtime-created class.
- Graph is non-empty and has structural relations; no hand patches were applied to `graph.json`.

## Collateral

Original fixture root `C:\tmp\gfxskilltest\iteration-2\code_fix\graphify-out` was removed during final cleanup so no fixture-root graphify-out remains. Targeted git check for tracked changes under the skill-under-test path and this eval output path returned no tracked modifications; the output directory contents are new evaluation artifacts.
