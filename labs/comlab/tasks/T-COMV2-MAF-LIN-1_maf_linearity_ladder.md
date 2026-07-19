# T-COMV2-MAF-LIN-1 — MAF linearity ladder (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted fields + wire their named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-10` (OBD `w_theo` + `sensor_error_delta` emitter, **done**). **DEP-11 · proposal `EP-OBD-11`** (`proposals.yaml`).
**Drill:** boot order → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `w_theo` + `sensor_error_delta` and wire a MAF-linearity **ladder** in the router that sharpens routing between a dirty/drifted connected MAF (`ERR-LC-002` / `P0101`) and an open-circuit MAF (`P0102`), behind a default-off flag. Absent fields are inert. Closes signal/noise for DEP-11.

### Context
`sensor_error_delta` is the non-linearity % deviation between the two airflow points vs theoretical (`w_theo`). A **5–12 %** gap is calibration drift / dirty MAF (`ERR-LC-002`); **>12–15 %** is a gross **component fault** (sets `P0101`, MAF range/performance). An **open-circuit MAF (`P0102`)** reads *no* signal — it is the separate contrast this feature must **not** mis-route a dirty-but-connected MAF into. Zero live COMLab reads today → orphan. Sharpen routing as evidence, don't assert a new fault.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `w_theo: float | None = None` and `sensor_error_delta: float | None = None` (mirror emitter `labs/obdlab/obdlab/schemas/payload.py:120,123`, exact type). Additive, default-absent. Comment the consumer.
2. **`comlab/core/fault_atlas_router.py`** — add `enable_maf_lin: bool = False` to the constructor. Add a pure helper `_maf_linearity_band(sensor_error_delta: float | None) -> <band>`:
   - `None` or `|Δ| < 5.0` → `WITHIN_SPEC` (no-op); `5.0 ≤ |Δ| ≤ 12.0` → `CALIBRATION_DRIFT`; `|Δ| > 12.0` → `COMPONENT_FAULT`.  `# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "MAF linearity ladder" (<3–4 healthy / 5–12 drift→ERR-LC-002 / >12–15 component→P0101; P0102=open-circuit) + 08_scoring_to_fusion_rework.md §line103`
   - In `execute_triage_loop` **Phase 5** behind `self._enable_maf_lin`: `CALIBRATION_DRIFT` → evidence toward `ERR-LC-002` (dirty MAF); `COMPONENT_FAULT` → evidence toward `P0101` (MAF range/performance). Either result is evidence the connected-MAF diagnosis is correct, i.e. **away** from open-circuit `P0102` (`wiki/05_fault_taxonomy.md`). Evidence re-rank, **not** override. Emit a `maf_linearity_applied` span.
3. Falsy short-circuits keep single-point byte-identical: flag off · fields `None` · `WITHIN_SPEC`.

### Consumer (signal/noise)
`w_theo` + `sensor_error_delta` → `fault_atlas_router.py::execute_triage_loop` Phase 5 linearity ladder. Closes the DEP-11 orphan. Proposal `EP-OBD-11` ships its consumer in this same change.

### Tests — `tests/` (ADD)
- `test_maf_lin_inert_when_off`: input with `sensor_error_delta = 18.0` flag off, and `None` flag on → identical output.
- `test_maf_lin_drift_routes_lc002`: `sensor_error_delta = 8.0`, flag on → `ERR-LC-002` rank raised + `maf_linearity_applied` fired.
- `test_maf_lin_component_routes_p0101`: `sensor_error_delta = 18.0`, flag on → `P0101` component-fault evidence (and not open-circuit `P0102`); `4.0` is inert.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — `sensor_error_delta` read in Phase 5 + the `enable_maf_lin` branch that reaches it.
- Single-point **byte-identical** with flag off / fields absent / within-spec.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill both gate blocks in `progress_notes/T-COMV2-MAF-LIN-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-MAF-LIN-1.md`.

### Out of scope
Live activation / default-on; re-tuning the ladder edges (wiki-pinned); adding new MAF fault nodes; emitter / `maf_linearity.py` changes; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "sensor_error_delta" comlab/core/fault_atlas_router.py   # read site
grep -nI "enable_maf_lin"     comlab/core/fault_atlas_router.py    # the branch that reaches it
"$PY" -m pytest tests/ -q -k "maf_lin"
```
