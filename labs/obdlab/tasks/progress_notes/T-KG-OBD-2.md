# T-KG-OBD-2 - Graphify ingest production OBDLab code map

## Plan

Scope: production package `labs/obdlab/obdlab/` only, resolved from the lab
directory as `obdlab/`. Tests, research, wiki, `graph/*`, canonical `graphify-out/`,
and root-level graph directories were excluded.

This was a dedicated KG-lane exception after `T-KG-OBD-2-PREP` completed. The stale
`blocked` ledger row was treated as unblocked for this task only because its blocker was
already `done`.

Build path:

1. Verified freeze gates in `tasks/PROGRESS.md`: `T-OBDV2-8`, `T-OBDV2-FIX-1` through
   `T-OBDV2-FIX-7`, `T-OBDV2-ARCH-1`, `T-OBDV2-ARCH-2`, and `T-KG-OBD-2-PREP` are all
   `done`.
2. Snapshotted protected paths before generation:
   `graph/v1_baseline`, `graph/v2_current`, `graph/v2_wiki`, and existing
   `graphify-out`.
3. Used the venv-local graphify package, `graphifyy` `0.8.35`, via
   `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe`.
4. Ran AST-only extraction over 16 production Python files under `obdlab/`.
5. Built the graph in default undirected mode (`directed: false`) inside
   `graph/_tmp_v2_code_build/graphify-out/`.
6. Moved only final artifacts into `graph/v2_code/`:
   `graph.json`, `GRAPH_REPORT.md`, and `graph.html`.
7. Removed only the task-created `graph/_tmp_v2_code_build/` directory.

Generated graph:

| Metric | Count |
|---|---:|
| Source Python files | 16 |
| Nodes | 188 |
| Links | 492 |
| Communities | 11 |
| Hyperedges | 0 |
| Input tokens | 0 |
| Output tokens | 0 |

Required symbol spot-checks in `graph/v2_code/graph.json`:

| Symbol | Present |
|---|---:|
| `o2_normalizer` | yes |
| `translate` | yes |
| `OBDLivePayload` | yes |
| `O2FailureMode` | yes |
| `TrimAnalyticsGate` | yes |

## VERIFICATION GATE

Commands run from `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab`:

```powershell
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m graphify --help
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -c "import importlib.metadata; print(importlib.metadata.version('graphifyy'))"
git status --porcelain -- graph/v1_baseline graph/v2_current graph/v2_wiki graphify-out
git status --porcelain -- '4DLab/4DLabV2/labs/obdlab/obdlab'
```

Results:

- Graphify executable: PASS, venv-local package is `graphifyy` `0.8.35`.
- Output artifacts: PASS, `graph/v2_code/graph.json`, `GRAPH_REPORT.md`, and
  `graph.html` exist.
- Graph content: PASS, `188 nodes / 492 links`, `directed: false`, and links > 0.
- Required symbol spot-checks: PASS, 5/5 symbols present.
- AST-only scope: PASS, 16 `.py` files from production `obdlab/`; no tests, research,
  wiki, graph directories, or semantic extraction.
- Protected graph collateral: PASS, `graph/v1_baseline`, `graph/v2_current`, and
  `graph/v2_wiki` are clean; existing untracked `graphify-out/` remains pre-existing.
- Source collateral: PASS, no changed files under production `obdlab/`.
- Temp cleanup: PASS, `graph/_tmp_v2_code_build/` removed.

## CODE REVIEW

PASS. This task adds only the requested code-map deliverable and task bookkeeping:

- `graph/v2_code/graph.json`
- `graph/v2_code/GRAPH_REPORT.md`
- `graph/v2_code/graph.html`
- `tasks/progress_notes/T-KG-OBD-2.md`
- `tasks/PROGRESS.md`

No source code, tests, research files, wiki graph, baseline graph, current graph, or
pre-existing `graphify-out/` directory was modified. The graph was built as an AST-only,
undirected code-navigation artifact for production OBDLab source.
