# T-COMV2-VE-GATE-1 — VE-as-evidence circularity gate (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan). **Research:** OBD **Q5 closed** (`obdlab/research/AUDIT_ANSWERS_OBDLab.md`).
**Blocked by:** `T-OBDV2-2` (OBD emits `ve_pct`/`ve_validity`/`air_metering_strategy`, contract frozen, **done**). **DEP-6** (named existing consumer — **not** a new proposal).
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** wire the VE verdict so a VE fault is treated as **independent evidence only when the air-metering architecture is `DUAL_MAF_MAP_CROSSCHECK`** (two independent sensors cross-check). On a single-air-sensor vehicle the VE number is derived from the same sensor it would indict — **circular** — so route to **MAF/MAP/TPS rationality (P0068)** instead, never to a VE-based mixture verdict. Behind a default-off flag; `VALID`/`UNKNOWN`/absent inputs are inert. Closes signal/noise for DEP-6.

### Context
`ve_pct`/`ve_validity` are already mirrored on `OBDLiveDataPayload` (`ingestion.py:377–378`) but **no live COMLab code reads them** → orphan. The VE cross-check is only trustworthy when MAF and MAP are **independent** sensors (`air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`, which the `VinDNA` validator ties to `has_maf_sensor and has_map_sensor`, `ingestion.py:117`). With one air sensor, VE is back-computed from that sensor, so a "VE fault" just re-states the sensor's own reading — circular evidence (audit Q5). The faithful move: gate VE-as-evidence on the architecture, and on the single-sensor branch route to a **rationality** check (P0068 MAF/MAP/TPS + IAC/idle-MAP) rather than asserting a mixture fault.

**Contract-drift fix (do this here):** the COMLab mirror `ve_pct` is bounded `le=100.0` (`ingestion.py:377`) but the **emitter** bounds it `le=200.0` (`labs/obdlab/obdlab/schemas/payload.py:80` — "max 200 to accommodate thermal-shock steam overshoot"). Widen the COMLab mirror to `ge=0.0, le=200.0` to match the emitter exactly. `# wiki: OBDLab_KG_Wiki §6.4 (VE max 200, thermal-shock overshoot)` — architect-confirmed drift; recorded in `PROGRESS.md` out-of-band table.

### What to build
1. **`comlab/schemas/ingestion.py`** — (a) widen `OBDLiveDataPayload.ve_pct` to `Field(..., ge=0.0, le=200.0)` (drift fix above). (b) add `air_metering_strategy: AirMeteringStrategy | None = None` to **`SessionMetadata`** (`:151`), mirroring how `resolved_horizon` is the DNALab-resolved token the router already reads off `request.metadata` — default-None keeps legacy/no-DNA sessions inert. `AirMeteringStrategy` is already imported (`:22`). **Do not** put it on `OBDLiveDataPayload`: per `wiki/02 §4 CONCEPT_DNA_INPUT line172` it is a **DNALab** token, not an OBD field; `SessionMetadata` is the router's DNA-token carrier. Comment the consumer.
2. **`comlab/core/fault_atlas_router.py`** — add `enable_ve_gate: bool = False` to the constructor (mirror `enable_ctxmod` at `:375`; store `self._enable_ve_gate`). Add a module-level pure helper near `:186`–`:269`:
   ```
   def _ve_evidence_gate(ve_pct, ve_validity, air_metering_strategy)
       -> Literal["UNAVAILABLE", "VE_EVIDENCE", "CIRCULAR_RATIONALITY"]:
       ve_validity in (VALID, UNKNOWN) or air_metering_strategy is None -> "UNAVAILABLE"  # inert
       ve_validity is a FAULT_* and air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK     -> "VE_EVIDENCE"
       ve_validity is a FAULT_* and air_metering_strategy != DUAL_MAF_MAP_CROSSCHECK     -> "CIRCULAR_RATIONALITY"
   ```
   `# wiki: 02_lab_input_contract.md §2 line55 (ve_pct/ve_validity) + §4 line172 (air_metering_strategy DUAL gate) + vocabulary.py::VEValidity (FAULT_VE_IDLE_COLLAPSE/FAULT_MAF_CONTAMINATION/FAULT_VE_SENSOR_SKEW) + 06_fault_atlas_families.md §CONCEPT_FAM_LEAN/§CONCEPT_FAM_SENSOR + DEP-6 audit Q5`
3. **`comlab/core/fault_atlas_router.py::execute_triage_loop` Phase 5** — add a block (mirror BANK-FUSE `:917–954`) behind `self._enable_ve_gate and obd_live_data is not None`, reading `request.metadata.air_metering_strategy`:
   - `"VE_EVIDENCE"` → **promote** the `lean_condition` member matching the VE fault as conflict-aware evidence (`max(score_val, _VE_EVIDENCE_CONFIDENCE)`): `FAULT_VE_IDLE_COLLAPSE` → idle vacuum-leak member, `FAULT_MAF_CONTAMINATION` → MAF under-read member, `FAULT_VE_SENSOR_SKEW` → sensor-over-read member (resolve the member ids from `comlab/config/kg/lean_condition.json` / `sensor_fault.json`; **do not invent ids** — if a clean 1:1 member is not present, promote the family and record the gap in the progress note).
   - `"CIRCULAR_RATIONALITY"` → do **not** promote any VE/lean member; instead promote the **MAF/MAP/TPS rationality** route (P0068 family member if present in the KG; else flag `ve_circular_rationality` as a span event and leave scores unchanged — the point is to *withhold* the circular VE verdict, not to fabricate P0068). 
   - Add constants `_VE_EVIDENCE_CONFIDENCE = 0.80` (mirror `_BANK_ASYMMETRY_CONFIDENCE`) in the `:57`–`:72` region. Emit a `ve_evidence_applied` / `ve_circular_rationality` span event.
4. Three falsy short-circuits keep behaviour byte-identical: flag off · `ve_validity in (VALID, UNKNOWN)` · `air_metering_strategy is None`.

### Consumer (signal/noise)
`ve_pct`/`ve_validity` (OBD) + `air_metering_strategy` (DNA, via `SessionMetadata`) → `fault_atlas_router.py::execute_triage_loop` Phase 5 VE gate (reachable on the live route). Closes the DEP-6 orphan. Named existing consumer — no new proposal id.

### Tests — `tests/` (ADD)
- `test_ve_gate_inert_when_off`: a `FAULT_VE_IDLE_COLLAPSE` + `DUAL_MAF_MAP_CROSSCHECK` input with `enable_ve_gate=False`, **and** `VALID`/`UNKNOWN`/`air_metering_strategy=None` with it on → identical `OrchestratorFinalUIOutput` to baseline.
- `test_ve_dual_promotes_lean`: `DUAL_MAF_MAP_CROSSCHECK` + `FAULT_VE_IDLE_COLLAPSE` raises the matching `lean_condition` member + fires `ve_evidence_applied`.
- `test_ve_single_sensor_is_circular`: same VE fault but `air_metering_strategy=MAP_ONLY_SPEED_DENSITY` does **not** promote a lean/VE member (fires `ve_circular_rationality`); proves the circularity gate.
- `test_ve_pct_accepts_overshoot`: `ve_pct=150.0` now validates (drift fix) where it previously raised.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — read site (`ve_validity` in `fault_atlas_router.py`) **and** the `enable_ve_gate` branch — prove the field is read in a reachable path.
- Single-point **byte-identical** with flag off / `VALID`/`UNKNOWN` / `air_metering_strategy` absent.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-VE-GATE-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row + out-of-band drift note) · `progress_notes/T-COMV2-VE-GATE-1.md`.

### Out of scope
**Populating `SessionMetadata.air_metering_strategy` upstream** (the assembler/adapter wiring is a separate change; default-None here keeps it inert until then); **flipping `enable_ve_gate` default to on** (live activation is a separate follow-up); authoring a new P0068 KG node if one does not already exist (withhold the circular verdict, do not fabricate — register a proposal in a follow-up); the idle-MAP/IAC corroboration channel; emitter changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "ve_validity\|air_metering_strategy" comlab/core/fault_atlas_router.py   # read site
grep -nI "enable_ve_gate" comlab/core/fault_atlas_router.py                       # the branch that reaches it
"$PY" -m pytest tests/ -q -k "ve_gate or ve_pct or ve_dual or ve_single"
```
