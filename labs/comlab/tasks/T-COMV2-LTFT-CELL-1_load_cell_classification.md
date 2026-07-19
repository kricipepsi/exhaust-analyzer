# T-COMV2-LTFT-CELL-1 — load-cell LTFT classification (orphan-closer; default-off)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** orphan-closer consumer (mirror emitted field + wire its named reader → close anti-orphan).
**Blocked by:** `T-OBDV2-11` (OBD `ltft_cell_vector` emitter, **done**). **DEP-12 · proposal `EP-OBD-12`** (`proposals.yaml`).
**Drill:** boot order → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`, **`comlab-fusion-consumer`**.

> **One-line scope:** mirror OBD `ltft_cell_vector` and wire a classifier in the router that labels the lean distribution **GLOBAL vs LOCALISED** and feeds family selection, behind a default-off flag. Absent vector is inert. Closes signal/noise for DEP-12. *(Idle-vs-part-throttle refinement is deferred — see Deliverable 2; it needs an OEM cell→region map the emitter does not yet supply.)*

### Context
`ltft_cell_vector` is the per-load-cell long-term fuel-trim map. Its **shape** discriminates cause: lean across all cells → global cause (MAF / fuel pressure / O₂ bias); lean in a subset → a localised cause (e.g. vacuum leak at idle, or mid-range delivery). Zero live COMLab reads today → orphan. v1 classifies the **computable** GLOBAL/LOCALISED split and feeds family selection as evidence; the finer idle-vs-part-throttle split needs the OEM cell-index→region map (`fuel-trim/13` provides only a GMH example), so it is deferred — flag, don't guess.

### What to build
1. **`comlab/schemas/ingestion.py::OBDLiveDataPayload`** — add `ltft_cell_vector: dict[int, float] | None = None`. **Mirror the emitter's exact type** (`labs/obdlab/obdlab/schemas/payload.py:117` — `dict[int, float] | None`). Note: `wiki/02_lab_input_contract.md:64` abbreviates it `list[float]`; the emitter `dict` is the contract — **mirror the dict, do not change it** (flag the wiki shorthand in the progress note, no wiki edit from a coding task).
2. **`comlab/core/fault_atlas_router.py`** — add `enable_ltft_cell: bool = False`. Add a pure helper `_ltft_cell_pattern(ltft_cell_vector: dict[int, float] | None) -> <pattern>` computing **only the distribution that the dict alone supports**:
   - `None`/empty → `UNAVAILABLE`; lean (`> +5 %`) **across all populated cells** → `GLOBAL`; lean **in a subset of cells** → `LOCALISED`; otherwise → `WITHIN_SPEC`.  `# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS "LTFT load-cell distribution" (GLOBAL vs LOCALISED; idle/part-throttle deferred — needs OEM cell map) + 08_scoring_to_fusion_rework.md §line104`.  Lean threshold reuses the `wiki/02 §2` authority bands (`> +5 %`).
   - **Idle-only vs part-throttle-only is NOT computable from the dict alone** — the cell index → operating-region map is OEM-specific (`fuel-trim/13`: "the cell index itself encodes operating context", GMH example only). v1 stops at GLOBAL/LOCALISED; the idle/part-throttle refinement is deferred until a cell→region map is contracted from the emitter (note it, do not invent indices).
   - In `execute_triage_loop` **Phase 5** behind `self._enable_ltft_cell`: `GLOBAL` → evidence toward a global cause (MAF / fuel-pressure / O₂-bias); `LOCALISED` → evidence toward a region-specific cause (`wiki/06_fault_atlas_families.md`). Evidence re-rank, **not** override. Emit a `ltft_cell_classified` span.
3. Falsy short-circuits keep single-point byte-identical: flag off · `None`/empty · `UNAVAILABLE`.

### Consumer (signal/noise)
`ltft_cell_vector` → `fault_atlas_router.py::execute_triage_loop` Phase 5 cell classifier → family selection. Closes the DEP-12 orphan. Proposal `EP-OBD-12` ships its consumer in this same change.

### Tests — `tests/` (ADD)
- `test_ltft_cell_inert_when_off`: a subset-lean vector flag off, and `None` flag on → identical output.
- `test_ltft_cell_localised_routes_region`: a subset-lean vector flag on → `LOCALISED` region-specific family rank raised + `ltft_cell_classified` fired.
- `test_ltft_cell_global_routes_supply`: all-cell-lean → `GLOBAL` family (MAF / fuel-pressure / O₂-bias); within-spec vector is inert.

### Success criteria (done = all)
- **Consumer-read gate:** two greps — `ltft_cell_vector` read in Phase 5 + the `enable_ltft_cell` branch that reaches it.
- Single-point **byte-identical** with flag off / vector absent / unavailable.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill both gate blocks in `progress_notes/T-COMV2-LTFT-CELL-1.md`. **STOP.**

### Files to touch
`comlab/schemas/ingestion.py` · `comlab/core/fault_atlas_router.py` · `tests/` (**ADD**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-LTFT-CELL-1.md`.

### Out of scope
Live activation / default-on; the **idle-vs-part-throttle refinement** and any cell-index→operating-region map (deferred — needs an emitter-supplied region map; `fuel-trim/13` gives only a GMH example); emitter changes; new fault families; graphify. **Critical reconciliation** (note, don't fix in code): emitter type `dict` vs wiki/02 `list` shorthand — mirror the emitter, flag to architect.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "ltft_cell_vector" comlab/core/fault_atlas_router.py   # read site
grep -nI "enable_ltft_cell" comlab/core/fault_atlas_router.py    # the branch that reaches it
"$PY" -m pytest tests/ -q -k "ltft_cell"
```
