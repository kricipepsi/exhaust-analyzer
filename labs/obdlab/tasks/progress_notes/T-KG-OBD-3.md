# T-KG-OBD-3 - Graphify ingest OBDLab test map

## Plan

Scope: test tree `labs/obdlab/tests/` only, resolved from the lab directory as
`tests/`. Production `obdlab/`, research, wiki, existing graph directories, and
canonical `graphify-out/` were excluded.

This was a dedicated KG-lane exception. The stale `blocked` ledger row was
treated as unblocked for this task only because its named blockers were already
done in the test-rollout ledger: `T-TST-6` and `T-TST-8`.

Build path:

1. Verified `T-TST-6` and `T-TST-8` are `done` in
   `planning/test_rollout/TEST_ROLLOUT_PROGRESS.md`.
2. Verified graphify package version `graphifyy` `0.8.35`, matching the prior
   OBDLab KG tasks.
3. Built an AST-only graph from `tests/` with `GRAPHIFY_OUT` pointed at
   `graph/_tmp_v2_tests_build/graphify-out`.
4. Moved only final artifacts into `graph/v2_tests/`:
   `graph.json`, `GRAPH_REPORT.md`, and `graph.html`.
5. Removed only the task-created `graph/_tmp_v2_tests_build/` directory.

Generated graph:

| Metric | Count |
|---|---:|
| Source test files | 41 |
| Nodes | 878 |
| Links | 1196 |
| Communities | 61 |
| Hyperedges | 0 |
| Directed | false |

Spot checks:

| Check | Result |
|---|---|
| `SensorSignalTranslator.translate` query | PASS - returns pid-logset, regression, and translator import tests |
| `o2_normalizer` present | PASS |
| `obdlab_cases.csv`/case projection nodes present | PASS |
| generative harness nodes present | PASS |
| source scope | PASS - 41 unique `source_file` values, 0 out-of-scope paths |

## VERIFICATION GATE

Commands run from `C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab`:

```powershell
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m graphify --help
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -c "import importlib.metadata; print(importlib.metadata.version('graphifyy'))"
$env:GRAPHIFY_OUT = "C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\obdlab\graph\_tmp_v2_tests_build\graphify-out"
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m graphify update tests
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m graphify query "SensorSignalTranslator translate" --context call --graph graph\v2_tests\graph.json
git status --porcelain -- '4DLabV2/labs/obdlab/graph/v1_baseline' '4DLabV2/labs/obdlab/graph/v2_current' '4DLabV2/labs/obdlab/graph/v2_wiki' '4DLabV2/labs/obdlab/graph/v2_code' '4DLabV2/labs/obdlab/graphify-out' '4DLabV2/labs/obdlab/obdlab' '4DLabV2/labs/obdlab/tests/graphify-out'
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m ruff check .
$env:PYTHONPATH = "C:\Users\muto\claude\4DApp\4DLab\4DLabV2;C:\Users\muto\claude\4DApp\4DLab\4DLabV2\harness"
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\pyright.exe
C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe -m pytest -q
```

Results:

- Graphify executable: PASS, venv-local package is `graphifyy` `0.8.35`.
- Output artifacts: PASS, `graph/v2_tests/graph.json`, `GRAPH_REPORT.md`, and
  `graph.html` exist.
- Graph content: PASS, `878 nodes / 1196 links`, `directed: false`, and
  `61 communities`.
- Required query: PASS, `SensorSignalTranslator translate` returns
  `pid_logset/test_pid_logset_wiring_gate.py`,
  `regression/test_obdlab_regression.py`, and
  `unit/test_sensor_signal_translator.py`.
- AST-only scope: PASS, 41 test-side source files; no production `obdlab/`,
  research, wiki, graph directories, or semantic extraction.
- Protected graph collateral: PASS, `graph/v1_baseline`, `graph/v2_current`,
  `graph/v2_wiki`, and `graph/v2_code` remain clean; existing untracked
  `graphify-out/` remains pre-existing.
- Source collateral: PASS, no changed files under production `obdlab/`.
- Temp cleanup: PASS, `graph/_tmp_v2_tests_build/` removed; no
  `tests/graphify-out/` created.
- Ruff: PASS, `All checks passed!`.
- Pyright: PASS with shared harness path on `PYTHONPATH`, `0 errors, 0 warnings`.
- Regression suite: PASS, `388 passed, 2 skipped`.

## CODE REVIEW

PASS. This task adds only the requested test-map deliverable and task
bookkeeping:

- `graph/v2_tests/graph.json`
- `graph/v2_tests/GRAPH_REPORT.md`
- `graph/v2_tests/graph.html`
- `tasks/progress_notes/T-KG-OBD-3.md`
- `tasks/PROGRESS.md`

No source code, tests, research files, wiki graph, baseline graph, current
graph, code graph, or pre-existing `graphify-out/` directory was modified. The
graph was built as an AST-only, undirected coverage/traceability artifact for
OBDLab tests.
