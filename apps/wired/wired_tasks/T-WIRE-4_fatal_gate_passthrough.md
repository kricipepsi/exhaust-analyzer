# T-WIRE-4 — FATAL-gate passthrough flag

### Goal ###
Thread COMLab's `enable_fatal_gates` flag from `diagnose()` through to
`LabPipelineAggregator(...)` and expose it as a `run_case` CLI flag
(`--fatal-gates`), default **off**. When enabled, an INVALID/incomplete sample
must reach the COMLab `FATAL_INCOMPLETE` outcome instead of a normal verdict.
Done when the flag is off by default (verdict unchanged from T-WIRE-1/2), and
with the flag on an INVALID fixture produces `FATAL_INCOMPLETE`.

### Success criteria ###
- `apps/wired/tests/test_fatal_gate.py::test_default_off_verdict_unchanged`
  passes: with the flag unset, a normal case yields the same verdict as without
  the parameter.
- `apps/wired/tests/test_fatal_gate.py::test_invalid_reaches_fatal_incomplete`
  passes: with `enable_fatal_gates=True`, an INVALID sample fixture yields a
  verdict/outcome of `FATAL_INCOMPLETE`.
- Smoke: `python -m wired.run_case --case <invalid> --fatal-gates` exits with the
  documented non-zero/flagged result.

### Context ###
**Blocked by T-WIRE-2.** COMLab already supports the gate via
`LabPipelineAggregator.__init__(..., enable_fatal_gates=False)` (verified
2026-06-28); this task only **threads** it — it adds no COMLab logic. The FATAL
gate wiring inside COMLab itself is a separate pending COMLab task
(`T-COMV2-FATAL-1`, on the comlab ledger) — if `enable_fatal_gates=True` does not
yet produce `FATAL_INCOMPLETE` because that COMLab task has not landed, mark this
task `blocked` on `T-COMV2-FATAL-1` and record it; do not implement the gate
logic in `wired`. Pin: `diagnose()` signature in `apps/wired/wired/composition.py`
(from T-WIRE-1); aggregator flag in
`labs/comlab/comlab/core/lab_pipeline_aggregator.py` `__init__`.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. The flag is an existing COMLab constructor
parameter; `wired` only forwards it.

### Deliverables ###
1. `apps/wired/wired/composition.py` — `diagnose(raw_inputs, *, enable_fatal_gates=False)`
   threaded into the aggregator constructor (MODIFY).
2. `apps/wired/wired/run_case.py` — `--fatal-gates` CLI flag (MODIFY).
3. `apps/wired/tests/test_fatal_gate.py` — the two success-criteria tests + an
   INVALID-sample fixture.

### Files to touch ###
- `apps/wired/wired/composition.py` (MODIFY)
- `apps/wired/wired/run_case.py` (MODIFY)
- `apps/wired/tests/test_fatal_gate.py` (CREATE)
- `apps/wired/tests/fixtures/oil_cases/INVALID_sample.json` (CREATE)

### Out of scope ###
Do not implement FATAL-gate logic inside COMLab (that is `T-COMV2-FATAL-1` on the
comlab ledger). Do not enable the gate by default. No other aggregator flags
(`enable_delta*`, `enable_vpwr_gate`) in this task. No UI, no harness. Do not edit
any lab beyond reading the constructor signature. Do not rebuild a graph.

### Verification ###
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
$PY -m py_compile apps/wired/wired/composition.py apps/wired/wired/run_case.py
$PY -m ruff check apps/wired/wired/composition.py apps/wired/wired/run_case.py
( cd apps/wired && /agent_workspace/.venv-wired/bin/pyright . )
$PY -m pytest -x -q apps/wired/tests/test_fatal_gate.py
```
All steps must pass.

### Progress hook ###
PROGRESS.md `T-WIRE-4`: Status=done, Files changed={COUNT}, Verification="enable_fatal_gates threaded; default-off unchanged; INVALID -> FATAL_INCOMPLETE"
