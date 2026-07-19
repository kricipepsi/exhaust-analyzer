# Baseline Evaluation Report: without_skill run-2

## Scope

- Skill loading: no 4dlab graph skill was read or loaded for this run.
- Fixture corpus: `C:\tmp\gfxskilltest\iteration-2\code_fix`
- Temp execution copy: `C:\Users\muto\AppData\Local\Temp\graphify-baseline-eval2-20260609-170723-563\run-2`
- Output directory: `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\skilltest-out\iteration-2\eval-2\without_skill\run-2\outputs`
- Existing fixture `graphify-out` and `__pycache__` were not copied into the temp execution directory.

## Repo-root request handling

Request tested: "just graphify everything from the repo root"

Decision: re-scoped.

Reason: in this evaluation, accepting the unbounded wording could graphify production repository files or update an existing canonical graph. I treated "repo root" as the isolated temp copy of the small fixture root and ran graphify there only.

## Command

```powershell
& 'C:\Users\muto\.local\bin\graphify.exe' update .
```

Working directory:

```text
C:\Users\muto\AppData\Local\Temp\graphify-baseline-eval2-20260609-170723-563\run-2
```

Exit code: 0

Observed output:

```text
Re-extracting code files in . (no LLM needed)...
[graphify watch] Rebuilt: 16 nodes, 14 edges, 4 communities
[graphify watch] graph.json, graph.html and GRAPH_REPORT.md updated in graphify-out
Code graph updated. For doc/paper/image changes run /graphify --update in your AI assistant.
Tip: set GEMINI_API_KEY or GOOGLE_API_KEY to use Gemini for semantic extraction.
warning: skill is from graphify 0.8.36, package is 0.8.13. Run 'graphify install' to update.
```

## Produced artifacts

Copied from the temp run into:

```text
C:\Users\muto\claude\4DApp\4DLab\4DLabV2\_skills\graph\skilltest-out\iteration-2\eval-2\without_skill\run-2\outputs\graphify-out
```

Artifacts present:

- `.graphify_labels.json`
- `.graphify_root`
- `graph.json`
- `graph.html`
- `GRAPH_REPORT.md`
- `manifest.json`
- `cache\`

## Verification

Result: pass for baseline graph generation.

- `graph.json` parsed successfully.
- Node count: 16.
- Link count: 14. The JSON uses `links`; the CLI reports these as edges.
- Hyperedge count: 0.
- Source files represented: `__init__.py`, `clean_module.py`, `dirty_module.py`, `dynamic_runtime.py`.
- Expected symbol labels represented: `SensorState`, `normalize_reading()`, `describe_sensor()`, `calculate_ratio()`, `handler_a()`, `handler_b()`, `route_with_getattr()`, `route_with_dispatch_dict()`.
- Expected file import links represented from `__init__.py` to `clean_module.py` and `dirty_module.py`.

Limitations observed:

- The AST-only update produced a structural graph; it did not flag the seeded style/runtime violations as policy findings.
- `RuntimeBuiltFault` was not represented as a symbol node in the graph, consistent with the AST-only extractor focusing on files, classes, functions, imports, docstrings, and rationale comments.
