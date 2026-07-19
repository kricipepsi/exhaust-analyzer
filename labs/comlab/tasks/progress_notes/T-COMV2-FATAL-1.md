# T-COMV2-FATAL-1 progress note

Status: done
Date: 2026-06-21

## Scope Confirm

Wired the Stage-A fatal gates (`ERR-ABORT-00x` family) into `LabPipelineAggregator.process()`, controlled by the default-off `enable_fatal_gates: bool = False` flag.
- When `enable_fatal_gates` is `False`, the symptom routing path remains 100% byte-identical to the legacy/baseline behavior.
- When `enable_fatal_gates` is `True`, any tripped fatal gate raises `AggregatorAbort` and gets caught inside `process()`, returning a minimal `OrchestratorFinalUIOutput` carrying a `FATAL_INCOMPLETE` degradation mode with the matching error code and actionable remediation steps.
- Schema validation error handling (e.g. `case_013`) is left completely out of scope to avoid conflating the contract layer with the gate layer.

## Changed Files (this slice)

- [lab_pipeline_aggregator.py](file:///C:/Workspace/labs/comlab/comlab/core/lab_pipeline_aggregator.py) — Added `enable_fatal_gates` to constructor, wired `process()`, and added `_build_fatal_incomplete_output()`.
- [test_fatal_gate_wiring.py](file:///C:/Workspace/labs/comlab/tests/unit/test_fatal_gate_wiring.py) — Unit tests for flag-on/flag-off behaviors and specific abort validations.
- [test_comlab_regression.py](file:///C:/Workspace/labs/comlab/tests/regression/test_comlab_regression.py) — Integrated disjoint path regression testing and updated manifest assertions.
- [case_023_fatal_incomplete.json](file:///C:/Workspace/labs/comlab/tests/regression/fixtures/fatal/case_023_fatal_incomplete.json) — Schema-valid regression test case for fatal gates.

## Verification Gate

- `ruff check .` — Clean, no issues found.
- `pyright comlab/` — Clean (`0 errors, 0 warnings` when run from activated `.venv-comlab`).
- `pytest` — 509 passed, 4 skipped. Full suite passes cleanly.
- Flag-off path verification — confirmed `test_fatal_gates_inert_when_off` and `test_fatal_gates_healthy_unchanged` keep outputs byte-identical.
- Greps:
  - `grep -nI "run_fatal_gates_and_routing" comlab/core/lab_pipeline_aggregator.py`
  - `grep -nI "enable_fatal_gates" comlab/core/lab_pipeline_aggregator.py`
  - `grep -nI "_build_fatal_incomplete_output" comlab/core/lab_pipeline_aggregator.py`

## Code Review

- The `enable_fatal_gates` constructor parameter defaults to `False`. The instance variable is safely checked in `process()`.
- Catches `AggregatorAbort` in Stage A, routing directly to `_build_fatal_incomplete_output()` which skips subsequent stages (B-E).
- Placed regression fixture `case_023_fatal_incomplete.json` under `tests/regression/fixtures/fatal/` so the regular regression runner's glob path does not accidentally process it.
- Copied `_minimal_valid_payload()` locally to `test_fatal_gate_wiring.py` rather than importing it across package directories.
- Applied `# type: ignore[assignment]` to `horizon_lit: HorizonLit = horizon.value` to resolve static analysis/pyright errors.
