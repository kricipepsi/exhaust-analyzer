# T-COMV2-FATAL-1 — wire the fatal-gate path into process() (production; flagged)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** production wiring (an existing, tested method is never called on the live path — reach it and surface its verdict). **Research:** none.
**Blocked by:** — (the gate method and the `FATAL_INCOMPLETE` output type already exist). Logged as the "COMLab fatal terminal wiring" unplanned follow-up in `PROGRESS.md`.
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`.

> **One-line scope:** `LabPipelineAggregator.run_fatal_gates_and_routing()` (`:235`) implements the Stage-A fatal gates (`ERR-ABORT-001/002/004/005`) and is unit-tested, but `process()` (`:283`) never calls it — at `:356` it calls `route_symptom(request.symptom_dna)` **directly**, so the fatal gates are dead and there is no reachable `FATAL_INCOMPLETE` UI verdict. Wire `process()` to run the gates, catch `AggregatorAbort`, and return a clean `FATAL_INCOMPLETE` `OrchestratorFinalUIOutput`. Because this changes production verdicts, ship it behind a default-off `enable_fatal_gates` flag so the change is opt-in and `T-COMTST-4`'s pinned contract is updated deliberately, not silently.

### Context
`run_fatal_gates_and_routing(request)` (`:235`) calls `route_symptom` **and** raises `AggregatorAbort(code, message)` for `ERR-ABORT-001` (sample invalid), `-002` (engine not warmed), `-004` (VIN confidence NONE), `-005` (schema too old). `process()` at `:356` bypasses it (`directive = route_symptom(request.symptom_dna)`), so an invalid-sample / cold-engine / bad-VIN session today either Pydantic-rejects at ingestion or produces a **non-fatal** verdict — there is no `FATAL_INCOMPLETE` output the UI can show. The output type already supports it: `DegradationMode.FATAL_INCOMPLETE` (`schemas/vocabulary.py:570`) and `DegradationLit` includes `"FATAL_INCOMPLETE"` (`schemas/response.py:26`). `T-COMTST-4` regression-pins the **current** contract-rejection behaviour (`PROGRESS.md` Unplanned follow-ups: *"`process()` does not call `run_fatal_gates_and_routing()`, so the harness has no reachable `FATAL_INCOMPLETE` UI output to pin"*), so this task must update that pin in the same change. There is **no** abort→output builder today — add one.

### What to build
1. **`comlab/core/lab_pipeline_aggregator.py`** — add `enable_fatal_gates: bool = False` to `LabPipelineAggregator.__init__` (store `self._enable_fatal_gates`), mirroring the established default-off flag pattern. Optionally resolve from an env var if the aggregator already reads any (match the existing convention; otherwise constructor-only).
2. **`process()` Stage A (`:355`–`:357`)** — replace the bare `directive = route_symptom(...)` with:
   ```
   if self._enable_fatal_gates:
       try:
           directive = self.run_fatal_gates_and_routing(request)
       except AggregatorAbort as abort:
           return self._build_fatal_incomplete_output(request, abort, horizon)
   else:
       directive = route_symptom(request.symptom_dna)   # byte-identical legacy path
   ```
   (`run_fatal_gates_and_routing` itself calls `route_symptom`, so the success path is equivalent plus the gates.)
3. **Add `_build_fatal_incomplete_output(request, abort, horizon) -> OrchestratorFinalUIOutput`** — a focused builder that returns an output with `degradation_mode = "FATAL_INCOMPLETE"`, the `abort.code` (`ERR-ABORT-00x`) and `abort` remediation message surfaced in the UI fields, and the minimal required fields populated (mirror the construction at the existing `return OrchestratorFinalUIOutput(...)` sites `:409`/`:480` for required-field shape; do not run Stage B–E). Cite `# wiki:` for the `FATAL_INCOMPLETE` semantics (lld §6.3, `vocabulary.py:570`).
4. **`tests/`** — pin the new behaviour and protect the old: flag-off byte-identical; flag-on each `ERR-ABORT-00x` → `FATAL_INCOMPLETE` output with the right code; flag-on healthy request → unchanged verdict.
5. **`tests/regression/` (`T-COMTST-4`)** — add a **new** flag-on regression covering `FATAL_INCOMPLETE`, pinned via a **separate, schema-valid fixture that trips a gate** (e.g. `sample_validity=INVALID` → `ERR-ABORT-001`). Do **not** repurpose `case_013_invalid_input.json` — see **Audit corrections** below. Document the new golden in the progress note.

### Audit corrections (2026-06-21, architect) — read before coding

A second coder flagged a real ambiguity in step 5. These four corrections are binding; everything else in the plan is verified correct against the live code.

1. **(Blocking) Keep the new FATAL_INCOMPLETE fixture out of the default glob.** `test_comlab_regression` is parametrized over `_fixture_paths()`, which globs **every** `case_*.json` and runs each through `LabPipelineAggregator()` with the flag **off**. A FATAL_INCOMPLETE fixture dropped into `tests/regression/fixtures/` would be picked up by that flag-off run, produce a normal verdict (gates inert), and fail its `expected` assertion. Put flag-on fixtures in a **separate path** (e.g. `tests/regression/fixtures/fatal/`) and point only the new `test_comlab_regression_fatal_gates()` at that subdir so the two globs stay disjoint. Bump the `test_regression_fixture_manifest` count assert `5–7` → `5–8`.

2. **(Scope) `ValidationError` / `ERR-CONTRACT-001` is out of scope — do not touch `case_013`.** Schema rejection (the malformed `"invalid_p0302"` DTC) fires inside `OrchestratorInboundRequest.model_validate`, **before** `process()` exists, so `enable_fatal_gates` can never affect it (confirmed: the `expected_validation_error` branch validates the model and returns before the aggregator is constructed). Do **not** catch `ValidationError` and convert it to `FATAL_INCOMPLETE` — that conflates the contract layer (`ERR-CONTRACT-*`) with the gate layer (`ERR-ABORT-*`, family `invalid_input`). `case_013` keeps its `ERR-CONTRACT-001` pin unchanged, flag-independent.

3. **(pyright) Carry the type-ignore on the horizon literal.** In `_build_fatal_incomplete_output`, `horizon_lit: HorizonLit = horizon.value` needs `# type: ignore[assignment]` — same as the existing `:303` line — or the `pyright` gate fails.

4. **(Tests) Copy the helper, don't cross-import.** `_minimal_valid_payload()` lives in `tests/e2e/test_error_codes.py`. Copy it into the new test module rather than importing across test dirs.

### Consumer (signal/noise)
No new field. This makes the existing `DegradationMode.FATAL_INCOMPLETE` / `ERR-ABORT-00x` outputs **reachable** on the live `process()` path (the named consumer is the UI degradation banner). Default-off so production verdicts are unchanged until activation is chosen.

### Tests — `tests/` (ADD/EXTEND)
- `test_fatal_gates_inert_when_off`: invalid sample / cold engine / VIN NONE with `enable_fatal_gates=False` → identical to today's behaviour (no `FATAL_INCOMPLETE`).
- `test_fatal_gate_sample_invalid` / `_engine_not_warmed` / `_vin_none` / `_schema_old`: flag on → `OrchestratorFinalUIOutput.degradation_mode == "FATAL_INCOMPLETE"` carrying the matching `ERR-ABORT-00x`.
- `test_fatal_gates_healthy_unchanged`: flag on, a valid request → same verdict as flag-off (gates pass, normal routing).
- `T-COMTST-4` regression updated (both flag states pinned).

### Success criteria (done = all)
- **Reach gate:** a grep shows `run_fatal_gates_and_routing` is now called from `process()`, behind `enable_fatal_gates`.
- Flag-off path **byte-identical** to baseline (full-pipeline regression).
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-FATAL-1.md`. **STOP.**

### Files to touch
`comlab/core/lab_pipeline_aggregator.py` · `tests/` (**ADD**) · `tests/regression/` (`T-COMTST-4` pin update) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-FATAL-1.md`.

### Out of scope
**Flipping `enable_fatal_gates` default to on** (live activation is a separate owner-gated follow-up — this task only makes it reachable and tested); adding new `ERR-ABORT-*` codes or changing the gate thresholds in `run_fatal_gates_and_routing` (wire the existing gates as-is); Stage B–E behaviour; the `route_symptom` logic; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "run_fatal_gates_and_routing\|enable_fatal_gates\|_build_fatal_incomplete_output" comlab/core/lab_pipeline_aggregator.py
"$PY" -m pytest tests/ -q -k "fatal"
"$PY" -m pytest tests/regression/ -q
```
