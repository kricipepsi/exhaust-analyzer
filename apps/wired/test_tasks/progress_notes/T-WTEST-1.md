# T-WTEST-1 — progress note

## Plan
Scope confirmation: I am taking `T-WTEST-1` only. This is run-only: I will touch only `apps/wired/test_tasks/progress_notes/T-WTEST-1.md`, `apps/wired/test_tasks/reports/WTEST1_BASELINE_2026-06-30.md`, and `apps/wired/test_tasks/TEST_PROGRESS.md`; I will run `/agent_workspace/.venv-wired/bin/python --version` plus eight independent `pytest -q` runs from `labs/{gaslab,obdlab,dtclab,comlab,dnalab,vinlab,symptomlab}` and `apps/wired`; I will not edit lab, COMLab, wired source, tests, or run graphify. AGENTS risk is only accidental cache/source changes, so the gate will confirm report-only `.md` changes and no source/test diffs.

## Interpreter

```text
/agent_workspace/.venv-wired/bin/python --version
Python 3.14.6
```

## Pytest baseline

Verdict: **GREEN**. Total passed: **1991**. Total skipped: **16**. Failures/errors: **0**.

| Target | Passed | Failed | Skipped | XFailed | Errors | Exit |
|---|---:|---:|---:|---:|---:|---:|
| `labs/gaslab` | 208 | 0 | 2 | 0 | 0 | 0 |
| `labs/obdlab` | 388 | 0 | 2 | 0 | 0 | 0 |
| `labs/dtclab` | 590 | 0 | 0 | 0 | 0 | 0 |
| `labs/comlab` | 510 | 0 | 4 | 0 | 0 | 0 |
| `labs/dnalab` | 27 | 0 | 0 | 0 | 0 | 0 |
| `labs/vinlab` | 194 | 0 | 8 | 0 | 0 | 0 |
| `labs/symptomlab` | 63 | 0 | 0 | 0 | 0 | 0 |
| `apps/wired` | 11 | 0 | 0 | 0 | 0 | 0 |

### Skipped-test reasons

#### `labs/gaslab`

```text
SKIPPED [1] tests/generative/test_fuzz.py:8: Fuzz generator not implemented in shared engine
SKIPPED [1] tests/test_cases.py:11: gaslab_cases.csv not yet derived
208 passed, 2 skipped, 4 deselected in 8.36s
```

#### `labs/obdlab`

```text
SKIPPED [1] tests/generative/test_noise.py:8: blocked: T-TST-8 obdlab harness
SKIPPED [1] tests/generative/test_overlap.py:8: blocked: T-TST-8 obdlab harness
388 passed, 2 skipped in 0.54s
```

#### `labs/comlab`

```text
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:17: phase 3: implement Pydantic validation
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:24: phase 3: implement DTC regex validator
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:32: phase 3: implement fallback tree
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:42: phase 3: implement legacy graceful degradation
510 passed, 4 skipped in 7.53s
```

#### `labs/vinlab`

```text
SKIPPED [1] tests/unit/test_contract_conformance.py:203: No sample VINs available
SKIPPED [1] tests/unit/test_csv_suite.py:22: CSV not found: /cases/csv/cases_petrol_master_v6.csv
SKIPPED [1] tests/unit/test_csv_suite.py:63: CSV not found: /cases/csv/cases_petrol_master_v6.csv
SKIPPED [1] tests/unit/test_csv_suite.py:160: CSV not found: /cases/csv/cases_petrol_master_v6.csv
SKIPPED [1] tests/unit/test_csv_suite.py:274: CSV not found: /cases/csv/cases_petrol_master_v6.csv
SKIPPED [1] tests/unit/test_decoder.py:411: No sample VINs available
SKIPPED [1] tests/unit/test_decoder.py:432: No sample VINs available
SKIPPED [1] tests/unit/test_patch_regression.py:66: OPSI CSV not present in this env
194 passed, 8 skipped in 0.71s
```

### Command tails

#### `labs/gaslab`

Command: `cd /agent_workspace/labs/gaslab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
.....ss................................................................. [ 34%]
........................................................................ [ 68%]
..................................................................       [100%]
208 passed, 2 skipped, 4 deselected in 8.05s
```

#### `labs/obdlab`

Command: `cd /agent_workspace/labs/obdlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...ss................................................................... [ 18%]
........................................................................ [ 36%]
........................................................................ [ 55%]
........................................................................ [ 73%]
........................................................................ [ 92%]
..............................                                           [100%]
388 passed, 2 skipped in 0.48s
```

#### `labs/dtclab`

Command: `cd /agent_workspace/labs/dtclab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
........................................................................ [ 12%]
........................................................................ [ 24%]
........................................................................ [ 36%]
........................................................................ [ 48%]
........................................................................ [ 61%]
........................................................................ [ 73%]
........................................................................ [ 85%]
........................................................................ [ 97%]
..............                                                           [100%]
590 passed in 3.47s
```

#### `labs/comlab`

Command: `cd /agent_workspace/labs/comlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
........................................................................ [ 14%]
........................................................................ [ 28%]
........................................................................ [ 42%]
........................................................................ [ 56%]
.............................................ssss....................... [ 70%]
........................................................................ [ 84%]
........................................................................ [ 98%]
..........                                                               [100%]
=========================== short test summary info ============================
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:17: phase 3: implement Pydantic validation
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:24: phase 3: implement DTC regex validator
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:32: phase 3: implement fallback tree
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:42: phase 3: implement legacy graceful degradation
510 passed, 4 skipped in 7.81s
```

#### `labs/dnalab`

Command: `cd /agent_workspace/labs/dnalab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...........................                                              [100%]
27 passed in 0.12s
```

#### `labs/vinlab`

Command: `cd /agent_workspace/labs/vinlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
.........................sssss.......................................... [ 35%]
.....................................................ss................. [ 71%]
................s.........................................               [100%]
194 passed, 8 skipped in 0.77s
```

#### `labs/symptomlab`

Command: `cd /agent_workspace/labs/symptomlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...............................................................          [100%]
63 passed in 0.09s
```

#### `apps/wired`

Command: `cd /agent_workspace/apps/wired && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...........                                                              [100%]
11 passed in 1.79s
```

### OTel span test confirmation

```text
cd /agent_workspace && /agent_workspace/.venv-wired/bin/python -m pytest -q apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled
.                                                                        [100%]
pytest: 1 passed in 0.56s
```

## VERIFICATION GATE — T-WTEST-1

```text
VERIFICATION GATE — T-WTEST-1
1. Compile : PASS  (N/A: run-only task; no Python source touched)
2. Lint    : PASS  (N/A: run-only task; no Python source touched; task excludes ruff)
3. Types   : PASS  (N/A: run-only task; no Python source touched; task excludes pyright)
4. Tests   : PASS  (8 package pytest runs -> 1991 passed, 16 skipped, 0 failed/errors; OTel span test direct run -> 1 passed)
5. Contract: PASS  (report `apps/wired/test_tasks/reports/WTEST1_BASELINE_2026-06-30.md`; all 8 targets recorded with counts + exit code; GREEN iff all exits 0)
6. Orphan  : N-A   (no field/fault/consumer mapping added)
Result: CLEAN
```

## CODE REVIEW — T-WTEST-1

```text
CODE REVIEW — T-WTEST-1
Scope         : PASS  (changed only the baseline report, this progress note, and TEST_PROGRESS.md for T-WTEST-1/T-WTEST-2/T-WTEST-3 ledger promotion)
Composition   : PASS  (no lab edits by this task, no second-lab imports, no deferred path, no graphify)
Consumers     : PASS  (N/A: no mapped fields; named consumer is architect go/no-go via the baseline report)
Literals      : PASS  (N/A: no boundary literals added)
Docstrings    : PASS  (N/A: no public functions added)
Craft (WARN)  : depth=N/A run-only; deletion=no dead code added; seam=no mapping logic touched; interface=public pytest package suites plus direct public OTel test confirmation
Result: CLEAN
```

## Workspace note

`git status --short -- apps/wired/wired apps/wired/tests` showed pre-existing untracked oil-case fixture/test files outside this task. This task did not edit source or tests; only the three paths named in Scope were created/updated here.
