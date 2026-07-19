# T-COMV2-MISFIRE-LOC-1 — misfire localiser gate (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-9` (OBD `per_cylinder_misfire_counts` emitter, **done**). **DEP-9 · proposal `EP-OBD-IN-07`** (`proposals.yaml`).
**Drill:** boot order → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `per_cylinder_misfire_counts` and wire a localiser in the router that separates a **single-cylinder** fault (ignition/injector on one cylinder) from **global starvation** (lean across all cylinders), feeding the `misfire_vs_fuelling` decision, behind a default-off flag. Absent counts are inert. Closes signal/noise for DEP-9.

### Context
A misfire concentrated on one cylinder is a cylinder-local fault; misfire spread evenly across cylinders points to global fuelling / starvation. The counts let COMLab pick the right branch instead of treating all misfire the same. Zero live COMLab reads today → orphan.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `per_cylinder_misfire_counts: dict[int, int] | None = None`. **Mirror the emitter's exact type** (`labs/obdlab/obdlab/schemas/payload.py:114` — `dict[int, int] | None`). Note: `wiki/02:62` abbreviates it `list[int]`; mirror the emitter `dict` (flag the shorthand in the note, no wiki edit from a coding task).
2. **`comlab/core/fault_atlas_router.py`** — add `enable_misfire_loc: bool = False`. Add a pure helper `_misfire_locality(per_cylinder_misfire_counts: dict[int, int] | None, total_trim_correction_delta: float | None) -> <locality>`:
   - `None`/empty counts → `UNAVAILABLE`; **one cylinder dominates** (its count ≫ the rest) → `SINGLE_CYLINDER`; counts **spread across cylinders** → `GLOBAL`.  `# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "Misfire localisation" (>+15 % trim + 1 cyl → SINGLE_CYLINDER; spread → GLOBAL) + 13_proposals_register.md §line48 (EP-OBD-IN-07)`.
   - **False-lean guard (the gate's actual purpose):** a misfire pumps fresh O₂ past the upstream sensor → a **false-lean** positive trim. The table is conditioned on `total_trim_correction_delta > +15 %` (already mirrored on `OBDLiveDataPayload`): SINGLE_CYLINDER + high positive trim ⇒ a localised ignition/injector fault is mis-reading as lean; GLOBAL spread + high positive trim ⇒ genuine fuel starvation. Use the trim as the corroborating context, not a separate input to mirror.
   - In `execute_triage_loop` **Phase 5** behind `self._enable_misfire_loc`: `SINGLE_CYLINDER` → evidence toward cylinder-local ignition/injection **and away from** a trim-driven fuelling mis-route (the `misfire_vs_fuelling` pre-route gate, `EP-COM-07`); `GLOBAL` → evidence toward the fuelling/starvation branch. Evidence re-rank, **not** override. Emit a `misfire_localised` span.
3. Falsy short-circuits keep single-point byte-identical: flag off · `None`/empty · `UNAVAILABLE`.

### Consumer (signal/noise)
`per_cylinder_misfire_counts` → `fault_atlas_router.py::execute_triage_loop` Phase 5 localiser → `misfire_vs_fuelling`. Closes the DEP-9 misfire orphan. Proposal `EP-OBD-IN-07` ships its consumer in this same change.

### Tests — `tests/` (ADD)
- `test_misfire_loc_inert_when_off`: a single-cylinder counts dict flag off, and `None` flag on → identical output.
- `test_misfire_loc_single_cylinder`: counts `{3: 40, 1: 1, 2: 0, 4: 1}` + `total_trim_correction_delta = 18.0`, flag on → cylinder-local evidence (not a fuelling mis-route) + `misfire_localised` fired.
- `test_misfire_loc_global`: evenly-spread counts + high positive trim → fuelling/starvation branch.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — `per_cylinder_misfire_counts` read in Phase 5 + the `enable_misfire_loc` branch that reaches it.
- Single-point **byte-identical** with flag off / counts absent / unavailable.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill both gate blocks in `progress_notes/T-COMV2-MISFIRE-LOC-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-MISFIRE-LOC-1.md`.

### Out of scope
Live activation / default-on; the "dominates" ratio re-tuning beyond what the wiki pins; consuming `freeze_frame_misfire_cylinder` (separate FF path); emitter changes; new fault families; graphify. **Critical reconciliation** (note, don't fix): emitter `dict` vs wiki/02 `list` shorthand — mirror the emitter, flag to architect.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "per_cylinder_misfire_counts" comlab/core/fault_atlas_router.py   # read site
grep -nI "enable_misfire_loc"          comlab/core/fault_atlas_router.py    # the branch that reaches it
"$PY" -m pytest tests/ -q -k "misfire_loc"
```
