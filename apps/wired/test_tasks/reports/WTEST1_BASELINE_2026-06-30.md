# WTEST1 baseline — 2026-06-30

## Verdict

- Verdict: **GREEN**
- Total passed: **1991**
- Interpreter: `/agent_workspace/.venv-wired/bin/python` -> `Python 3.14.6`
- Scope: seven labs plus `apps/wired`, each run independently from its own package directory.
- OTel check: `apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled` ran directly and passed (`1 passed`, skip=0).

## Per-target counts

| Target | Passed | Failed | Skipped | XFailed | Errors | Exit | Duration |
|---|---:|---:|---:|---:|---:|---:|---:|
| `labs/gaslab` | 208 | 0 | 2 | 0 | 0 | 0 | 8.42s |
| `labs/obdlab` | 388 | 0 | 2 | 0 | 0 | 0 | 1.06s |
| `labs/dtclab` | 590 | 0 | 0 | 0 | 0 | 0 | 4.12s |
| `labs/comlab` | 510 | 0 | 4 | 0 | 0 | 0 | 8.45s |
| `labs/dnalab` | 27 | 0 | 0 | 0 | 0 | 0 | 0.56s |
| `labs/vinlab` | 194 | 0 | 8 | 0 | 0 | 0 | 1.24s |
| `labs/symptomlab` | 63 | 0 | 0 | 0 | 0 | 0 | 0.49s |
| `apps/wired` | 11 | 0 | 0 | 0 | 0 | 0 | 2.33s |

## Skipped tests

### `labs/gaslab`

```text
SKIPPED [1] tests/generative/test_fuzz.py:8: Fuzz generator not implemented in shared engine
SKIPPED [1] tests/test_cases.py:11: gaslab_cases.csv not yet derived
208 passed, 2 skipped, 4 deselected in 8.36s
```

### `labs/obdlab`

```text
SKIPPED [1] tests/generative/test_noise.py:8: blocked: T-TST-8 obdlab harness
SKIPPED [1] tests/generative/test_overlap.py:8: blocked: T-TST-8 obdlab harness
388 passed, 2 skipped in 0.54s
```

### `labs/comlab`

```text
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:17: phase 3: implement Pydantic validation
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:24: phase 3: implement DTC regex validator
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:32: phase 3: implement fallback tree
SKIPPED [1] tests/unit/test_lab_pipeline_aggregator.py:42: phase 3: implement legacy graceful degradation
510 passed, 4 skipped in 7.53s
```

### `labs/vinlab`

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

## Command tails

### `labs/gaslab`

Command: `cd /agent_workspace/labs/gaslab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
.....ss................................................................. [ 34%]
........................................................................ [ 68%]
..................................................................       [100%]
208 passed, 2 skipped, 4 deselected in 8.05s
```

### `labs/obdlab`

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

### `labs/dtclab`

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

### `labs/comlab`

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

### `labs/dnalab`

Command: `cd /agent_workspace/labs/dnalab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...........................                                              [100%]
27 passed in 0.12s
```

### `labs/vinlab`

Command: `cd /agent_workspace/labs/vinlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
.........................sssss.......................................... [ 35%]
.....................................................ss................. [ 71%]
................s.........................................               [100%]
194 passed, 8 skipped in 0.77s
```

### `labs/symptomlab`

Command: `cd /agent_workspace/labs/symptomlab && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...............................................................          [100%]
63 passed in 0.09s
```

### `apps/wired`

Command: `cd /agent_workspace/apps/wired && /agent_workspace/.venv-wired/bin/python -m pytest -q`
Exit code: `0`

```text
...........                                                              [100%]
11 passed in 1.79s
```

## OTel span test confirmation

```text
cd /agent_workspace && /agent_workspace/.venv-wired/bin/python -m pytest -q apps/wired/tests/test_tracing.py::test_spans_emitted_when_enabled
.                                                                        [100%]
pytest: 1 passed in 0.56s
```
