# T-COMV2-ECU-FUSE-1 — ECU perception-vs-reality fuse (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** verify-existing-read + add fused verdict + mirror the orphaned twin-trim input. **Research:** OBD **Q1/Q4 closed** (`obdlab/research/AUDIT_ANSWERS_OBDLab.md`); cross RQ#3 partial (`STUDY_ecu_fault_gas_signatures_merge`).
**Blocked by:** `T-GV2-6d` (GAS true `chemical_state`/`lambda_chem`, **done**) · `T-OBDV2-ECU-PERCEPT-1` (OBD perception-delta emitter, **done**). **DEP-2.**
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** the perception-vs-truth axis is **already computed live** (`perception_contradiction.detect`); this task adds the **`ecu_fault` discrimination** on top of it — when fuel trim is railed on **both banks together** (symmetric) **and** the ECU's perceived λ diverges from gas-truth λ beyond era tolerance, the correction system is exhausted/lying (`ecu_fault`, `ERR-EF-001`), not a real lean/rich. Wire it as router evidence behind a default-off flag, and **finally mirror + consume the orphaned `total_trim_correction_delta_b2`** twin-trim input. Closes signal/noise for DEP-2.

### Context
`06_fault_atlas_families.md §RULE_COLLISION_SET` line 92: *"ecu_fault vs real lean/rich — shared snapshot LEAN/RICH at trim limit — separated by **gas↔OBD divergence magnitude** — lever: ECU-FUSE consumer."* The divergence itself is **already live**: `perception_contradiction.detect` (`:106`) computes `normalized_obd_lambda − lambda_chem` and emits a `bias_verdict` on every route (verify this first — it is the "what exists" half). What is **missing** is the `ecu_fault` verdict that combines that divergence with **trim saturation** and **bank symmetry**, and the **bank-2 twin-trim** input `total_trim_correction_delta_b2` is emitted by OBD (`payload.py:68`) but **not mirrored** on COMLab's `OBDLiveDataPayload` → orphan. The `ecu_fault` family is the audit's **irreducible-floor** family (27 STOP cases, ~9.6 %) — separable *only* via gas↔OBD divergence at fusion, never gas-only (`06 §CONCEPT_FAM_ECU`). Symmetry matters: both banks railed **together** = global/`ecu_fault`; asymmetric railed trim is BANK-FUSE's bank-localised case, not this.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `lambda_perception_delta: float | None = None` (emitter `payload.py:77`; OBD's perception-vs-commanded delta) and `total_trim_correction_delta_b2: float | None = None` (emitter `payload.py:68`; bank-2 twin, `None` when single-bank). Mirror **exact emitter types**, additive default-None → omitting them validates byte-identically. Comment the consumer (`# consumer: fault_atlas_router ecu_fault fuse — T-COMV2-ECU-FUSE-1`).
2. **`comlab/core/fault_atlas_router.py`** — add `enable_ecu_fuse: bool = False` to the constructor (mirror `enable_ctxmod` `:375`; store `self._enable_ecu_fuse`). Add a module-level pure helper near `:186`–`:269`:
   ```
   def _ecu_fault_verdict(normalized_obd_lambda, lambda_chem, era_lambda_tolerance,
                          total_trim_correction_delta, total_trim_correction_delta_b2)
       -> _EcuFaultVerdict(state: Literal["UNAVAILABLE","NO_FAULT","ECU_FAULT"], confidence):
       any required input None -> "UNAVAILABLE"                              # inert
       not (|total_trim_correction_delta| >= _ECU_FUSE_RAILED_TRIM_PCT 25)   -> "NO_FAULT"  # trim not saturated; >±25% = ERR-EF-001
       bank-asymmetric (both banks present and |b1 - b2| > 5.0)              -> "NO_FAULT"  # bank-local -> BANK-FUSE, not ecu_fault
       perception agrees (|normalized_obd_lambda - lambda_chem| <= era_lambda_tolerance) -> "NO_FAULT"  # ECU perceives truth -> real lean/rich
       else (railed + symmetric + divergent)                                -> "ECU_FAULT"
   ```
   `# wiki: 06_fault_atlas_families.md §RULE_COLLISION_SET line92 (gas↔OBD divergence magnitude) + §CONCEPT_FAM_ECU + 02_lab_input_contract.md §2 line70 (>±25 % saturated → ERR-EF-001) + line52/53 (_b2 twin / lambda_perception_delta) + perception_contradiction.detect (existing divergence read) + DEP-2 audit Q1/Q4`. Add `_ECU_FUSE_RAILED_TRIM_PCT = 25.0` and `_ECU_FUSE_CONFIDENCE = 0.80` in the `:57`–`:72` constants region (bank-symmetry bound reuses `_BANK_ASYMMETRY_BOUND_PCT = 5.0`).
3. **`execute_triage_loop` Phase 5** — add a block (mirror BANK-FUSE `:917–954`) behind `self._enable_ecu_fuse and obd_live_data is not None`, reading `obd_live_data.normalized_obd_lambda`, `request.gas_lab_output.lambda_chem`, the active `era_lambda_tolerance` (same value `perception_contradiction` is called with — thread it through, do not hard-code), `obd_live_data.total_trim_correction_delta`, `obd_live_data.total_trim_correction_delta_b2`. When `state == "ECU_FAULT"`, **promote** scored rows whose KG `fault_family == "ecu_fault"` as conflict-aware evidence (`max(score_val, verdict.confidence)`). Emit an `ecu_fault_fused` span event (`b1`, `b2`, `perception_delta`, `score_before/after`). Evidence, **not** an override (`wiki/08 §CONCEPT_EVIDENCE_INPUTS`).
4. Falsy short-circuits keep behaviour byte-identical: flag off · any required input `None` · trim not railed · asymmetric · perception in-tolerance.

### Consumer (signal/noise)
`lambda_perception_delta` + `total_trim_correction_delta_b2` (+ existing `normalized_obd_lambda`, gas `lambda_chem`) → `fault_atlas_router.py::execute_triage_loop` Phase 5 `ecu_fault` fuse (reachable on the live route). Closes the DEP-2 orphan and finally consumes the bank-2 twin-trim `_b2`. Named existing consumer (`ecu_fault` family already in the KG); no new proposal id.

### Tests — `tests/` (ADD)
- `test_ecu_fuse_inert_when_off`: the full ECU-fault tuple with `enable_ecu_fuse=False`, **and** any required input `None` with it on → identical `OrchestratorFinalUIOutput` to baseline.
- `test_ecu_fuse_promotes_ecu_fault`: railed symmetric trim (`b1=+30, b2=+30`) + divergent λ (`normalized_obd_lambda` − `lambda_chem` > era tolerance) raises an `ecu_fault` row + fires `ecu_fault_fused`.
- `test_ecu_fuse_rejects_real_lean`: same railed trim but **perception agrees** (|Δλ| ≤ tolerance) → `NO_FAULT`, no promotion (proves it does not steal real lean/rich).
- `test_ecu_fuse_rejects_asymmetric`: railed but `b1=+30, b2=-5` (|b1−b2|>5) → `NO_FAULT` (that is BANK-FUSE's case).
- **Verify-existing:** `test_perception_axis_still_live` — assert `perception_contradiction.detect` is still invoked on the standard route and its `bias_verdict` unchanged with `enable_ecu_fuse=False` (the "what exists" half is untouched).

### Success criteria (done = all)
- **Consumer-read gate:** two greps — read site (`total_trim_correction_delta_b2`/`lambda_perception_delta` in `fault_atlas_router.py`) **and** the `enable_ecu_fuse` branch — prove the orphaned `_b2` is read in a reachable path.
- Single-point **byte-identical** with flag off / inputs absent / trim-not-railed / asymmetric / perception-agrees.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-ECU-FUSE-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-ECU-FUSE-1.md`.

### Out of scope
**Modifying `perception_contradiction.detect`** (it already computes the divergence — read it, do not re-author the perception axis); **flipping `enable_ecu_fuse` default to on** (live activation is a separate follow-up); the `o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE` two-stage offset path (that is `T-COMV2-O2OFFSET-1`, blocked on `T-OBDV2-4`); new `ecu_fault` KG nodes beyond `ERR-EF-001`; surfacing the fuse into UI output; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "total_trim_correction_delta_b2\|lambda_perception_delta" comlab/core/fault_atlas_router.py   # read site (orphaned _b2)
grep -nI "enable_ecu_fuse" comlab/core/fault_atlas_router.py                                            # the branch that reaches it
"$PY" -m pytest tests/ -q -k "ecu_fuse or perception_axis"
```
