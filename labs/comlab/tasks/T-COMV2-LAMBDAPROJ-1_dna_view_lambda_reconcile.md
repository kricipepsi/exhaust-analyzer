# T-COMV2-LAMBDAPROJ-1 — DNA-view λ projection-path reconcile (FU-4 / DEP-4)

**Authored:** 2026-06-21 (architect, Cowork). **Stage:** 4. **Type:** contract reconcile (fix a wrong projection path so an already-named consumer field stops coming back `None`). **Research:** none (contract, not research).
**Blocked by:** — (GAS emit `T-GV2-3` **done**; this is the COMLab read path). **DEP-4 · proposal `vehicle-dna-projection-paths`** (`config/proposals/entries.yaml:251`, consumer `projection.py:project`).
**Drill:** boot order (`COMLAB_TASKS_START_HERE.md`) → `PROGRESS.md` → **this file** → scope-confirm → code. **Load skills:** `comlab-python`, `comlab-verification-loop`, `comlab-code-review`. (Not a fusion-consumer — no `comlab-fusion-consumer`.)

> **One-line scope:** `projection.py::project` reads the Certificate-of-Conformity λ window inputs (`target_lambda_v112`, `co_high_idle`, `co_low_idle`) from the **wrong nesting level** of `VinDNA` — from a nested `emissions.*` dict that does not carry them — so `GasLabDnaView` gets `None` and GASLab's Brettschneider/CoC λ window + 2500 RPM CO ceiling silently lose their per-vehicle target. Re-point the reads to the level `VinDNA` actually declares them at, so the projected view carries real values. This closes the DEP-4 "λ in/out divergent until S4" reconcile. No new field, no flag — a path correction with a regression test.

### Context
`project` (`comlab/projection.py:40`) builds `GasLabDnaView` and currently reads `emissions.get("target_lambda_v112")` / `co_low_idle` / `co_high_idle` (`projection.py:79`–`:81`) from an `emissions` sub-dict. The registered proposal `vehicle-dna-projection-paths` (`config/proposals/entries.yaml:251`–`:270`) records the exact defect and fix: these CoC empirical fields live at **top level** `vin_dna.target_lambda_v112` / `vin_dna.co_high_idle` (not `vin_dna.emissions.*`), while only equipment flags belong under `vin_dna.emissions.*`. Because the path is wrong, `GasLabDnaView.target_lambda_v112` → GASLab's CoC λ window and `GasLabDnaView.co_high_idle` → GASLab's 2500 RPM CO ceiling are fed `None` today → the consumer exists but reads nothing (the DEP-4 divergence). **Step 1 is to confirm the actual top-level location in the raw payload, not in a Pydantic model.** `project()` is **dict-based** — it reads `vehicle_dna_json["vin_dna"]` (`projection.py:51`) and never validates through `comlab/schemas/ingestion.py::VinDNA` (that mirror is off the projection path — do **not** use its field set as the source of truth; it is incomplete and irrelevant here). Confirm against the **upstream emitter** `labs/vinlab/vinlab/models.py::VinDNA`, which declares these CoC fields at **top level** (`:228/:231/:232`) and parses them from the **top level** of the payload (`payload.get("target_lambda_v112")` …, `:301/:304/:305`); only equipment flags sit under nested `emissions`. The DNALab fixture (`labs/dnalab/tests/conftest.py:59–63`) confirms the same JSON shape. So the raw `vin_dna` dict **does carry** these at top level → follow the proposal's `from → to` exactly. (A prior coder STOP-flagged a "contract gap" after inspecting the off-path Pydantic mirror — that was a false positive; see PROGRESS.md "LAMBDAPROJ contract-gap reconciliation".)

### What to build
1. **`comlab/projection.py::project`** — re-point the three CoC reads (`:79`–`:81`) to the level `VinDNA` declares them at, per the proposal `from → to`:
   - `target_lambda_v112`: `vin_dna.emissions.target_lambda_v112` → `vin_dna.target_lambda_v112`
   - `co_high_idle`: `vin_dna.emissions.co_high_idle` → `vin_dna.co_high_idle`
   - `co_low_idle`: same correction if it shares the defect (confirm against `VinDNA`).
   Keep equipment-flag reads (`*_equipped`, `downstream_o2_present`, …) under `emissions.*` unchanged. Comment each repointed read with the consumer (`# consumer: GasLabDnaView.<field> — DEP-4 / proposal vehicle-dna-projection-paths`).
2. **No schema change.** Step 1 already confirms the fields are present at the **top level of the raw payload** (upstream `vinlab.models.VinDNA`), so the re-point lands a real value. The STOP-and-flag escape applies only if the upstream emitter itself stopped declaring them at top level — **not** the absence of the field from the off-path Pydantic mirror `comlab/schemas/ingestion.py::VinDNA` (that absence is expected and irrelevant; do not add a field to it from this task).
3. Mark the proposal `vehicle-dna-projection-paths` consumed/shipped in `config/proposals/entries.yaml` if the file tracks status (match sibling entries).

### Consumer (signal/noise)
`VinDNA.target_lambda_v112` + `VinDNA.co_high_idle` (+ `co_low_idle`) → `projection.py::project` → `GasLabDnaView.target_lambda_v112` / `co_high_idle` → GASLab Brettschneider/CoC λ window + 2500 RPM CO ceiling. Named existing consumer (`GasLabDnaView`); this task makes the read **reach a non-`None` value**. Closes DEP-4.

### Tests — `tests/` (ADD/EXTEND)
- `test_projection_lambda_paths`: a `VehicleDNA` whose `vin_dna.target_lambda_v112` / `co_high_idle` carry real values → the projected `GasLabDnaView` carries those exact values (proves the read now lands). Before the fix this returns `None`.
- `test_projection_equipment_flags_unchanged`: an equipment flag under `vin_dna.emissions.*` still projects correctly (proves the fix is surgical and didn't move the wrong reads).
- Full suite green; no other view fields change.

### Success criteria (done = all)
- **Read-lands gate:** a grep + a test show `GasLabDnaView.target_lambda_v112`/`co_high_idle` are populated from the corrected path (not `None`) on a populated `VinDNA`.
- `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q` clean (`PY=../../.sandbox-py/bin/python3.14`).
- Flip ledger row → `done`; fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-LAMBDAPROJ-1.md`. **STOP.**

### Files to touch
`comlab/projection.py` · `config/proposals/entries.yaml` (status only, if tracked) · `tests/` (**ADD**) · `tasks/PROGRESS.md` (flip row) · `progress_notes/T-COMV2-LAMBDAPROJ-1.md`. (`schemas/ingestion.py` — read-only confirm of `VinDNA` field level.)

### Out of scope
**Adding fields to `VinDNA`** (if a field is genuinely missing at the expected level, STOP and flag — it is an upstream contract task, not this); the `lab_dna_views.py` *output*-side reconcile beyond the three CoC λ inputs (if a separate output divergence exists, log it as an unplanned follow-up); GASLab emitter changes; the registry; graphify.

### Verification
```bash
cd labs/comlab; PY=../../.sandbox-py/bin/python3.14
ruff check . && pyright comlab/ && "$PY" -m pytest -x -q
grep -nI "target_lambda_v112\|co_high_idle\|co_low_idle" comlab/projection.py   # confirm re-pointed reads
"$PY" -m pytest tests/ -q -k "projection"
```
