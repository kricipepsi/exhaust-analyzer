# T-WIRE-1 — compose the labs into COMLab (`diagnose()`)

### Goal ###
Stand up the `wired` package and its single composition entry point
`diagnose(raw_inputs) -> OrchestratorFinalUIOutput` in
`apps/wired/wired/composition.py`. It runs DNALab + GASLab (with high-idle) +
OBDLab + DTCLab, maps each typed output into a COMLab payload, builds one
`OrchestratorInboundRequest`, and calls
`LabPipelineAggregator().process(request)`. Done when `diagnose()` on a minimal
valid input returns an `OrchestratorFinalUIOutput` whose
`diagnostic_verdict.fault_code` is populated, the high-idle gas block is
forwarded onto the COMLab `GasLabPayload`, no deferred-fusion import exists, and
`registry_guard.py` expects 73 rules.

### Success criteria ###
- `apps/wired/tests/test_composition.py::test_diagnose_returns_verdict` passes
  (write it failing first): a minimal raw-input dict -> `diagnose()` returns an
  `OrchestratorFinalUIOutput` with a non-empty `diagnostic_verdict.fault_code`.
- `apps/wired/tests/test_composition.py::test_high_idle_forwarded` passes: a raw
  input carrying `*_high` gas values produces a COMLab `GasLabPayload` whose
  high-idle fields are populated (not dropped).
- Smoke: `/agent_workspace/.venv-wired/bin/python -c "from wired import diagnose"`
  exits 0 (run from `/agent_workspace`).
- `grep -rn "deferred" apps/wired/wired/composition.py` finds no fusion-path
  import.

### Context ###
This is the first wired task and the foundation for T-WIRE-2/3/4. **Blocked by
gaslab `T-GV2-2`** (COMLab `ChemicalSignature` mirror must be 34-value before a
GAS payload carrying a new `CAM_TIMING_*` value is accepted — see
`WIRING_PREP.md` Section A). Adapt the prior composition
`ARCHIVE/wiredV2/wiredv2/composition.py` (634 lines — READ-NARROW, grep a pattern
and adapt; never import from `ARCHIVE/`). The three things the prior version gets
wrong for the current tree: (1) it imports a deferred fusion path that no longer
exists — drop those imports + every helper that uses them; (2) it does not
forward the high-idle gas block — forward it (composition-contract skill §3);
(3) it predates `SessionMetadata.air_metering_strategy` — forward that optional
DNA token (the VE gate reads it).

Pin these exact targets (do not whole-read): COMLab inbound
`labs/comlab/comlab/schemas/ingestion.py:488` and the payload mirrors at lines
151/165/289/324; output `labs/comlab/comlab/schemas/response.py:132`; the live
verdict path `labs/comlab/registry/integration_shim.py`. Lab entry-point
signatures are in the composition-contract skill §2 (verified 2026-06-28).
Registry guard: a pending registry follow-up records `registry_guard.py` must
expect **73** rules, not 68, or the side-by-side harness raises
`RegistryActivationError` (`labs/comlab/registry/docs/REGISTRY_PROGRESS.md`).

Load skills: wired-composition-contract.

### Consumer (signal/noise) ###
`apps/wired` maps existing lab fields into existing COMLab payload mirrors — it
adds **no new schema field**. For each mapped field, name the COMLab reader in a
`# consumer:` comment (e.g. `ve_pct` -> `fault_atlas_router` VE-evidence gate;
`per_bank_trim_delta` -> bank-asymmetry verdict; `o2_failure_mode` -> wideband
offset confirm). If a lab field has **no** nameable COMLab reader, do not map it.
No new field/enum/fault is introduced by this task.

### Deliverables ###
1. `apps/wired/pyproject.toml` — editable package `wired`, depends on the labs.
2. `apps/wired/wired/__init__.py` — exports `diagnose`.
3. `apps/wired/wired/composition.py` — `diagnose()` + per-lab mappers + the two
   vocab translators (`_map_o2_sensor_type`, `_derive_horizon` fallback).
4. `apps/wired/wired/registry_guard.py` — REG-V2 activation guard expecting 73 rules.
5. `apps/wired/tests/test_composition.py` — the two success-criteria tests + a
   minimal fixture.

### Files to touch ###
- `apps/wired/pyproject.toml` (CREATE)
- `apps/wired/wired/__init__.py` (CREATE)
- `apps/wired/wired/composition.py` (CREATE)
- `apps/wired/wired/registry_guard.py` (CREATE)
- `apps/wired/tests/test_composition.py` (CREATE)

### Out of scope ###
No oil-case fixtures or CLI runner (that is T-WIRE-2). No OTel tracing (T-WIRE-3).
No FATAL-gate threading (T-WIRE-4) — construct the aggregator with defaults
(`enable_fatal_gates=False`). No UI, no CSV harness. Do not edit any file under
`labs/`. Do not rebuild any knowledge graph. Surgical-change rule: every line
traces to a Deliverable; adjacent improvements -> `T##b` follow-up rows.

### Verification ###
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
$PY -m pip install -e apps/wired
# Inner loop
$PY -m py_compile apps/wired/wired/composition.py apps/wired/wired/registry_guard.py
$PY -m ruff check apps/wired/wired/
( cd apps/wired && /agent_workspace/.venv-wired/bin/pyright . )   # U-WV2-3: run from apps/wired
# Structural
$PY -c "from wired import diagnose; print('import ok')"
grep -n "air_metering_strategy" apps/wired/wired/composition.py
! grep -rn "deferred" apps/wired/wired/composition.py
grep -n "73" apps/wired/wired/registry_guard.py
# Functional
$PY -m pytest -x -q apps/wired/tests/test_composition.py
```
All steps must pass.

### Progress hook ###
PROGRESS.md `T-WIRE-1`: Status=done, Files changed={COUNT}, Verification="diagnose() returns OrchestratorFinalUIOutput; high-idle forwarded; no deferred path; guard=73"
