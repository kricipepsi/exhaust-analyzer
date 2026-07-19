# T-COMV2-NOSTART-1 — no-start branch: security-lockout vs mechanical (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror two emitted DTC signals + wire the named reader → close anti-orphan). **Research:** OBD **Q8 closed**; DTC emitter `T-DTCV2-NOSTART-1` (+`-FIX`), **done**.
**Blocked by:** `T-DTCV2-NOSTART-1` (DTCLab `Mode06MonitorState.MONITOR_ABORTED` + `FreezeFrameRecord.ff_fuel_spark_cut_at_crank`, **done**). **DEP-8 · proposal `EP-DTC-NOSTART-1`** (`config/proposals/proposals.yaml:57`).
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** DTCLab emits two raw no-start discriminators it deliberately does **not** judge — a Mode-$06 monitor that returned `MONITOR_ABORTED` (the test never ran), and a freeze-frame `ff_fuel_spark_cut_at_crank` flag (fuel **and** spark cut while stationary at crank). COMLab is the named judge. When **both** are present, the ECU is deliberately cutting fuel and spark — the signature of a **security/immobiliser lockout**, not a broken part → promote the `non_starter` security node. When the monitor aborted **without** a deliberate cut, it's a **mechanical** no-start (CKP no-RPM, fuel/spark hardware) → promote the mechanical no-start nodes. Wire behind a default-off flag. Closes signal/noise for DEP-8.

### Context
Neither signal is mirrored on COMLab's DTC inbound schema today → both are genuine Stage-4 orphans. (1) COMLab's `Mode06MonitorState` is an **alias of `Mode06Status`** (`schemas/vocabulary.py` ~`:508`) carrying only `{PASSED, PENDING_FAIL_MARGINAL, CRITICAL_FAIL}` — it is **missing `MONITOR_ABORTED`**, the value the emitter added (`labs/dtclab/dtclab/schemas/vocabulary.py:78`). (2) COMLab's `FreezeFrameRecord` (`schemas/ingestion.py:263`–`:270`) declares 6 derived §12.3 flags and is **missing the 7th**, `ff_fuel_spark_cut_at_crank` (emitter `labs/dtclab/dtclab/schemas/freeze_frame.py:95`, `bool = False`). The wiki names the target for this pair: *`T-COMV2-NOSTART-1` | DTC Mode-06 monitor-aborted + FF cut-state | **security-lockout vs mechanical no-start*** (`wiki/08_scoring_to_fusion_rework.md` line 98), routing within the **non_starter** family (`wiki/06_fault_atlas_families.md §CONCEPT_FAM_NONSTART`, lines 71-73, *"no-spark / no-fuel / … + freeze-frame cut-state (T-COMV2-NOSTART-1)"*). **CAN-era is already gated at the emitter:** `MONITOR_ABORTED` is emitted *only* for CAN-era no-start (`labs/dtclab/docs/DTC_VOCABULARY.md` §10.3/§13). COMLab **does not re-gate on era** — the router request carries **no VinDNA** (`schemas/ingestion.py:452`–`:453`), so `euro_emission_category` is unreachable here; consuming the already-gated `MONITOR_ABORTED` is the correct single-lab move. Security vs mechanical maps to existing KG nodes (`config/kg/non_starter.json`): `ERR-NS-005` ("Engine cranks but does not start … check immobiliser status and security light") is the security path; `ERR-NS-001/002` (spark), `ERR-NS-003` (fuel), `ERR-NS-004` (weak spark) are mechanical. No new node is invented.

### What to build
1. **`comlab/schemas/vocabulary.py`** — add `MONITOR_ABORTED = "MONITOR_ABORTED"` to the `Mode06Status` enum (`# wiki: DTC_VOCABULARY §10.3/§13 — Incomplete/all-zero monitor; CAN-era no-start only`). Update the now-stale "identical values … alias" comment + the "tri-state" docstring to record the 4th value mirrors the emitter. Keep `Mode06MonitorState = Mode06Status`.
2. **`comlab/schemas/ingestion.py::FreezeFrameRecord`** — add `ff_fuel_spark_cut_at_crank: bool = False` to the §12.3 derived-flags block (`:263`–`:270`), mirroring the emitter's exact type/default. Comment the consumer (`# consumer: fault_atlas_router no-start branch — T-COMV2-NOSTART-1`).
3. **`comlab/core/fault_atlas_router.py`** — add `enable_nostart: bool = False` to the constructor (mirror `enable_ecu_fuse` at `:482`; store `self._enable_nostart` near `:509`). Add a module-level pure helper near the other verdict helpers (`:204`–`:380`):
   ```
   def _no_start_branch(mode_06_monitors, ff_fuel_spark_cut_at_crank)
       -> Literal["UNAVAILABLE", "MECHANICAL", "SECURITY_LOCKOUT"]:
       not mode_06_monitors (None/empty dict)                       -> "UNAVAILABLE"   # no DTC monitors -> single-lab inert
       no monitor.state == MONITOR_ABORTED                          -> "UNAVAILABLE"   # not a no-start monitor-abort
       MONITOR_ABORTED present and ff_fuel_spark_cut_at_crank        -> "SECURITY_LOCKOUT"  # ECU cuts BOTH fuel+spark at crank = immobiliser
       MONITOR_ABORTED present and not ff_fuel_spark_cut_at_crank    -> "MECHANICAL"     # aborted w/o deliberate cut = mechanical no-start
   ```
   `# wiki: 08_scoring_to_fusion_rework.md line 98 (Mode-06 monitor-aborted + FF cut-state -> security vs mechanical) + 06_fault_atlas_families.md §CONCEPT_FAM_NONSTART lines 71-73 + DTC_VOCABULARY §10.3/§13 (MONITOR_ABORTED CAN-era-gated) + §12.3 (ff_fuel_spark_cut_at_crank) + proposal EP-DTC-NOSTART-1`. Add constants in the `:61`–`:79` region: `_NOSTART_CONFIDENCE = 0.80` (`# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER`), `_NOSTART_SECURITY_NODES = frozenset({"ERR-NS-005"})` and `_NOSTART_MECHANICAL_NODES = frozenset({"ERR-NS-001", "ERR-NS-002", "ERR-NS-003", "ERR-NS-004"})` (both `# wiki: 06_fault_atlas_families.md §CONCEPT_FAM_NONSTART + config/kg/non_starter.json`).
4. **`execute_triage_loop` Phase 5** — add a block (mirror the BANK-FUSE promote block at `:1032`–`:1069`, but keyed on `request.dtc_lab_output`) behind `self._enable_nostart and request.dtc_lab_output is not None`. Read `dtc_output.mode_06_monitors` and `dtc_output.freeze_frame.ff_fuel_spark_cut_at_crank`; compute `_no_start_branch(...)`. Pick the node set by verdict (`SECURITY_LOCKOUT → _NOSTART_SECURITY_NODES`, `MECHANICAL → _NOSTART_MECHANICAL_NODES`, else skip); **promote** scored rows whose `row.fault_id` is in that set as conflict-aware evidence (`promoted = max(score_val, _NOSTART_CONFIDENCE)`; skip when `promoted <= score_val`). Emit a `no_start_branch_applied` span event (`verdict`, `ff_fuel_spark_cut_at_crank`, `rule_id`, `score_before`/`score_after`). Evidence, **not** an override (`wiki/08 §CONCEPT_EVIDENCE_INPUTS`).
5. Falsy short-circuits keep behaviour byte-identical: flag off · `dtc_lab_output` absent · no `MONITOR_ABORTED` monitor.

### Consumer (signal/noise)
`Mode06MonitorState.MONITOR_ABORTED` (via `dtc_lab_output.mode_06_monitors[].state`) + `FreezeFrameRecord.ff_fuel_spark_cut_at_crank` → `fault_atlas_router.py::execute_triage_loop` Phase 5 no-start branch (reachable on the live route via `request.dtc_lab_output`). Closes the DEP-8 orphan on both emitted signals. Proposal `EP-DTC-NOSTART-1` ships its consumer in this same change (no new fault node — promotes existing `non_starter` nodes).

### Tests — `tests/` (ADD)
- `test_nostart_inert_when_off`: a `MONITOR_ABORTED` + `ff_fuel_spark_cut_at_crank=True` request with `enable_nostart=False`, **and** `dtc_lab_output=None` with it on → `OrchestratorFinalUIOutput` identical to baseline.
- `test_nostart_security_lockout`: flag on, a monitor with `state=MONITOR_ABORTED` + `ff_fuel_spark_cut_at_crank=True` → `ERR-NS-005` promoted and `no_start_branch_applied` fires with `verdict=SECURITY_LOCKOUT`.
- `test_nostart_mechanical`: flag on, `MONITOR_ABORTED` + `ff_fuel_spark_cut_at_crank=False` → a `_NOSTART_MECHANICAL_NODES` row promoted, `verdict=MECHANICAL`.
- `test_nostart_no_aborted_inert`: monitors present but none `MONITOR_ABORTED` → byte-identical to baseline.
- **Schema round-trip:** `MONITOR_ABORTED` parses on `Mode06MonitorResult.state`, and `ff_fuel_spark_cut_at_crank` round-trips through `FreezeFrameRecord.model_dump()`.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — the read site (`ff_fuel_spark_cut_at_crank` / `MONITOR_ABORTED` in `fault_atlas_router.py`) **and** the `enable_nostart` branch — prove the orphaned signals are read in a reachable path.
- Single-point **byte-identical** with flag off / `dtc_lab_output` absent / no `MONITOR_ABORTED`.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-NOSTART-1.md`. **STOP.**

### Files to touch
`comlab/schemas/vocabulary.py` · `comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-NOSTART-1.md`.

### Out of scope
**Re-gating on `euro_emission_category` / CAN-era** (already gated at the emitter; the router request has no VinDNA — consume `MONITOR_ABORTED` as-is); **inventing new `ERR-NS` nodes** (promote the existing `non_starter` nodes; taxonomy changes are separate); **flipping `enable_nostart` default to on** (live activation is a separate follow-up); the engine-state OBD-suppression path (`GAS_DOMINANT` on `cranking`/`will_not_start`, `wiki/01` line 70 — already live, do not touch); surfacing into UI output; emitter / DTCLab changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "ff_fuel_spark_cut_at_crank\|MONITOR_ABORTED" comlab/core/fault_atlas_router.py   # read site (orphaned signals)
grep -nI "enable_nostart" comlab/core/fault_atlas_router.py                                 # the branch that reaches it
"$PY" -m pytest tests/ -q -k "nostart or no_start"
```
