# T-COMV2-O2OFFSET-1 — wideband-offset confirm vs gas truth (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (the OBD-live field is already mirrored — wire its named reader → close anti-orphan). **Research:** OBD **Q9 closed** (`obdlab/research/AUDIT_ANSWERS_OBDLab.md`; emitter `T-OBDV2-4` + `T-OBDV2-FIX-2`, **done**).
**Blocked by:** `T-OBDV2-4` (OBD `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` emitter, **done**) · `T-GV2-6d`/`T-GV2-3` (GAS `lambda_chem`, **done**). **DEP-7 · proposal `EP-OBD-17`** (`config/proposals/proposals.yaml:29`).
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** OBD already flags a wideband O₂ sensor that is reading a persistent constant offset (`o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE`) — a *candidate*, not a verdict. This task adds the **confirmation** COMLab is uniquely able to make: cross-check the candidate against gas-truth λ. When `lambda_chem` says the mixture is actually stoichiometric (gas reads true) **while** the O₂ channel claims a fault, the sensor is lying with a calibration offset → promote the **`sensor_fault`** family (the perception-vs-truth O₂ nodes) as evidence behind a default-off flag. When gas λ confirms a *real* lean/rich, the candidate is masking a true mixture fault → stay inert. Closes signal/noise for DEP-7.

### Context
`o2_failure_mode` is **already mirrored** on `OBDLiveDataPayload` (`schemas/ingestion.py:402`, required `O2FailureMode`) but **read by no live COMLab path** → it is on the `FU-OBD-ORPHAN-1` list (`obdlab/tasks/PROGRESS.md`) and is a genuine Stage-4 orphan. `WIDEBAND_OFFSET_CANDIDATE` is the only value with no consumer (the others route through the existing perception axis). The discrimination is COMLab's by design: a constant-offset wideband sensor produces a *believable* λ that the OBD channel cannot self-disprove — only the independent gas chemistry can. This is the `sensor_fault` family's defining "perception ≠ truth, gas reads true" axis (`wiki/06_fault_atlas_families.md §CONCEPT_FAM_SENSOR`, line 37). The target the wiki names for this exact pair is **"wideband-calibration sensor_fault"** (`wiki/08_scoring_to_fusion_rework.md` line 97: *`T-COMV2-O2OFFSET-1` | OBD `WIDEBAND_OFFSET_CANDIDATE` + GAS `lambda_chem` | wideband-calibration sensor_fault*). The stoichiometric ("gas reads true") band is `lambda_chem ∈ [0.97, 1.03]` (`wiki/02_lab_input_contract.md` line 28: λ<0.97 rich, >1.03 lean). No new KG node is invented — the `sensor_fault` family already carries the O₂-perception nodes `ERR-SF-001`/`ERR-SF-002` (`config/kg/sensor_fault.json`); this is evidence promotion of that family, the same shape as ECU-FUSE promoting `ecu_fault`.

### What to build
1. **`comlab/schemas/ingestion.py`** — **no schema change** (`o2_failure_mode` already mirrored at `:402`; `GasLabPayload.lambda_chem` at `:179`). Verify only; do not re-add.
2. **`comlab/core/fault_atlas_router.py`** — add `enable_o2_offset: bool = False` to the constructor (mirror `enable_ecu_fuse` at `:482`; store `self._enable_o2_offset` next to `:509`). Add a module-level pure helper near the other verdict helpers (`:204`–`:380`):
   ```
   def _resolve_o2_sensor_fault(o2_failure_mode, lambda_chem)
       -> Literal["UNAVAILABLE", "NO_FAULT", "WIDEBAND_OFFSET"]:
       o2_failure_mode is None or lambda_chem is None        -> "UNAVAILABLE"   # inert
       o2_failure_mode != WIDEBAND_OFFSET_CANDIDATE           -> "NO_FAULT"      # not a candidate
       not (_O2_STOICH_LAMBDA_LO <= lambda_chem
            <= _O2_STOICH_LAMBDA_HI)                          -> "NO_FAULT"      # gas reads a REAL lean/rich -> candidate masks a true fault, defer
       else (candidate + gas confirms stoichiometric)         -> "WIDEBAND_OFFSET"  # sensor offset confirmed
   ```
   `# wiki: 08_scoring_to_fusion_rework.md line 97 (WIDEBAND_OFFSET_CANDIDATE + lambda_chem -> wideband-calibration sensor_fault) + 06_fault_atlas_families.md §CONCEPT_FAM_SENSOR line 37 (perception != truth, gas reads true) + 02_lab_input_contract.md line 28 (lambda_chem stoich band 0.97-1.03) + proposal EP-OBD-17`. Add constants in the `:61`–`:79` region: `_O2_STOICH_LAMBDA_LO = 0.97` and `_O2_STOICH_LAMBDA_HI = 1.03` (`# wiki: 02_lab_input_contract.md line 28`) and `_O2_OFFSET_CONFIDENCE = 0.80` (`# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER`, matching `_ECU_FUSE_CONFIDENCE`).
3. **`execute_triage_loop` Phase 5** — add a block (mirror the BANK-FUSE promote block at `:1032`–`:1069`) behind `self._enable_o2_offset and obd_live_data is not None`, reading `obd_live_data.o2_failure_mode` and `request.gas_lab_output.lambda_chem`. When `_resolve_o2_sensor_fault(...) == "WIDEBAND_OFFSET"`, **promote** scored rows whose KG `fault_family == "sensor_fault"` as conflict-aware evidence (`promoted = max(score_val, _O2_OFFSET_CONFIDENCE)`; skip when `promoted <= score_val`). Emit an `o2_offset_confirmed` span event (`o2_failure_mode`, `lambda_chem`, `score_before`/`score_after`). Evidence, **not** an override (`wiki/08 §CONCEPT_EVIDENCE_INPUTS`).
4. **`config/proposals/proposals.yaml:31`** — the `EP-OBD-17` `consumer:` string currently reads `...fault_atlas_router.py:FaultAtlasRouter._resolve_o2_sensor_fault`. Reconcile it to the symbol you actually ship (module-level `_resolve_o2_sensor_fault`, drop the `FaultAtlasRouter.` prefix) in this same change so the citation matches the code.
5. Falsy short-circuits keep behaviour byte-identical: flag off · `lambda_chem`/`o2_failure_mode` absent · mode ≠ `WIDEBAND_OFFSET_CANDIDATE` · gas λ outside the stoich band (real fault).

### Consumer (signal/noise)
`o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE` (+ gas `lambda_chem`) → `fault_atlas_router.py::execute_triage_loop` Phase 5 `sensor_fault` promote (reachable on the live route via `request.obd_live_data`). Closes the DEP-7 / `FU-OBD-ORPHAN-1` orphan on `o2_failure_mode`. Proposal `EP-OBD-17` ships its consumer in this same change (no new fault node — promotes the existing `sensor_fault` family).

### Tests — `tests/` (ADD)
- `test_o2_offset_inert_when_off`: a `WIDEBAND_OFFSET_CANDIDATE` + stoichiometric-λ request with `enable_o2_offset=False`, **and** any required input `None` with it on → `OrchestratorFinalUIOutput` identical to baseline (no promote, no span event).
- `test_o2_offset_promotes_sensor_fault`: `o2_failure_mode=WIDEBAND_OFFSET_CANDIDATE` + `lambda_chem=1.00` with the flag on → a `sensor_fault` row is promoted and `o2_offset_confirmed` fires.
- `test_o2_offset_rejects_real_lean`: same candidate but `lambda_chem=1.20` (gas reads a real lean) → `NO_FAULT`, no promotion (proves it does not steal a true mixture fault).
- `test_o2_offset_non_candidate_inert`: `o2_failure_mode=NO_FAULT`/`STUCK_LEAN` with the flag on → byte-identical to baseline.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — the read site (`o2_failure_mode` in `fault_atlas_router.py`) **and** the `enable_o2_offset` branch — prove the orphaned field is read in a reachable path.
- Single-point **byte-identical** with flag off / inputs absent / non-candidate / real-fault λ.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-O2OFFSET-1.md`. **STOP.**

### Files to touch
`comlab/core/fault_atlas_router.py` · `config/proposals/proposals.yaml` (consumer-string reconcile) · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-O2OFFSET-1.md`. (`schemas/ingestion.py` — verify only, no change.)

### Out of scope
**Modifying the existing perception axis** (`perception_contradiction.detect` already handles the non-candidate O₂ modes — read it for context, do not re-author it); **inventing a dedicated `ERR-SF` wideband node** (promote the existing `sensor_fault` family; a new node is a separate taxonomy change); **flipping `enable_o2_offset` default to on** (live activation is a separate follow-up); the ECU-hardware / bank paths (`T-COMV2-ECU-FUSE-1`/`ECU-HW-1`, already `done`); surfacing the confirmation into UI output; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "o2_failure_mode" comlab/core/fault_atlas_router.py     # read site (orphaned field)
grep -nI "enable_o2_offset" comlab/core/fault_atlas_router.py    # the branch that reaches it
"$PY" -m pytest tests/ -q -k "o2_offset"
```
