# T-COMV2-FUELSYS-GATE-1 — fuel-system-status Stage-A gate (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-6` (OBD `fuel_system_status` emitter, **done**). **DEP-9 · proposal `EP-OBD-IN-03`** (`proposals.yaml:66`).
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `fuel_system_status` onto `OBDLiveDataPayload` and wire a **closed-loop gate** in the router, behind a default-off flag: when the ECU is **not** in closed loop (`OL`/`OL_DRIVE`/`OL_FAULT`), trim-driven lean/rich families lose evidence weight — fuel trim has no feedback meaning in open loop. `CL` and an absent field are inert. Closes signal/noise for DEP-9.

### Context
`fuel_system_status` is the live fuel-loop state OBDLab emits (`CL`/`OL`/`OL_DRIVE`/`OL_FAULT`). It is **not** mirrored onto COMLab's `OBDLiveDataPayload` today (it exists only on the DTC freeze-frame, `FreezeFrameRecord.fuel_system_status` — a different, async snapshot) → the OBD-live field has **zero live COMLab reads** → orphan. In open loop the ECU runs the base map with no O₂ feedback, so `total_trim_correction_delta` carries no mixture signal; a trim-driven lean/rich verdict in that state is a false read. This gate is the **COMLab-facing** reader; OBDLab's internal `trim_analytics_gate == OPEN_LOOP` (`vocabulary.py::TrimAnalyticsGate`) already gates its own analytics, so emit **evidence down-weighting**, never a new override.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `fuel_system_status: FuelSystemStatus | None = None` mirroring the emitter (`labs/obdlab/obdlab/schemas/payload.py:99`, type `FuelSystemStatus`; mirror as **optional default-None** so absence stays inert). `FuelSystemStatus` is already imported in `ingestion.py` (`:29`). Comment the consumer (`# consumer: fault_atlas_router fuel-system closed-loop gate — T-COMV2-FUELSYS-GATE-1`).
2. **`comlab/core/fault_atlas_router.py`** — add `enable_fuelsys_gate: bool = False` to the constructor (mirror `enable_ctxmod` at `:375`; store `self._enable_fuelsys_gate` next to `:398`). Add a module-level pure helper near the other verdict helpers (`:186`–`:269`):
   ```
   def _fuel_system_gate(fuel_system_status) -> Literal["CLOSED_LOOP", "OPEN_LOOP_GATED", "UNAVAILABLE"]:
       None                          -> "UNAVAILABLE"   # field absent / legacy no-OBD
       FuelSystemStatus.CL           -> "CLOSED_LOOP"   # O2 feedback active — trim is meaningful, no-op
       OL / OL_DRIVE / OL_FAULT      -> "OPEN_LOOP_GATED"  # base map, no feedback — trim not diagnostic
   ```
   `# wiki: 02_lab_input_contract.md §2 CONCEPT_OBD_INPUT line58 (fuel_system_status CL/OL/OL_DRIVE/OL_FAULT) + vocabulary.py::TrimAnalyticsGate.OPEN_LOOP ("fuel_sys_status != Closed_Loop — no trim feedback") + 13_proposals_register.md A-row (EP-OBD-IN-03)`
3. **`comlab/core/fault_atlas_router.py::execute_triage_loop` Phase 5** — add a block mirroring the BANK-FUSE block at `:917–954`, behind `self._enable_fuelsys_gate and obd_live_data is not None`. When `_fuel_system_gate(...) == "OPEN_LOOP_GATED"`: for each scored row whose KG `fault_family` is **trim-driven** (`lean_condition`, `rich_mixture`), **demote** as conflict-aware evidence — `demoted = min(score_val, _OPEN_LOOP_TRIM_CONFIDENCE_CAP)`; only write back when `demoted < score_val` (mirror the misfire demote at `:986–991`). Emit a `fuel_system_gated` span event with `fuel_system_status`, `score_before`, `score_after`. Add the constant `_OPEN_LOOP_TRIM_CONFIDENCE_CAP = 0.60` in the constants region (`:57`–`:72`), cited to `MIN_CONFIDENCE_THRESHOLD` (`:57`, 0.70) so a gated trim family drops below the winner floor. Evidence, **not** an override or flat bump (`wiki/08 §CONCEPT_EVIDENCE_INPUTS`).
4. Three falsy short-circuits keep behaviour byte-identical: flag off · field `None` · `CLOSED_LOOP`.

### Consumer (signal/noise)
`fuel_system_status` → `fault_atlas_router.py::execute_triage_loop` Phase 5 closed-loop gate (reachable on the live route via `request.obd_live_data`). Closes the DEP-9 orphan for the OBD-live `fuel_system_status`. Proposal `EP-OBD-IN-03` ships its consumer in this same change.

### Tests — `tests/` (ADD)
- `test_fuelsys_inert_when_off`: an `OL_FAULT` input with `enable_fuelsys_gate=False` **and** a `CL` input with it on → `OrchestratorFinalUIOutput` identical to baseline (no demote, no span event).
- `test_fuelsys_open_loop_demotes_trim`: a 2-family request where a `lean_condition`/`rich_mixture` row is the winner; `enable_fuelsys_gate=True` + `fuel_system_status=OL` drops it below `MIN_CONFIDENCE_THRESHOLD` and fires `fuel_system_gated`; `CL` does not.
- `test_fuelsys_absent_is_inert`: `fuel_system_status=None` with the flag on → byte-identical to baseline.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — the read site (`fuel_system_status` in `fault_atlas_router.py`) **and** the `enable_fuelsys_gate` branch — prove the field is read in a reachable path.
- Single-point **byte-identical** with flag off / field absent / `CL` (a full-pipeline test through the router with the flag default-off must match baseline).
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-FUELSYS-GATE-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-FUELSYS-GATE-1.md`.

### Out of scope
The **`CL → OL_FAULT`-across-RPM Δ-signature** (needs a second operating-point frame — that is a two-point follow-up, not this single-point gate); **flipping the `enable_fuelsys_gate` default to on** (live activation is a separate follow-up); reading the DTC freeze-frame `fuel_system_status` (a different snapshot — this task is the OBD-live field only); surfacing the gate into UI output; emitter changes; new fault families; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "fuel_system_status" comlab/core/fault_atlas_router.py    # read site
grep -nI "enable_fuelsys_gate" comlab/core/fault_atlas_router.py   # the branch that reaches it
"$PY" -m pytest tests/ -q -k "fuelsys"
```
