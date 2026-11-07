# T-AUD-18c — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` COMLab_DLD section (group 4 of `reviews/REVIEW_T-AUD-11g.md`).
Rehearsal: `C:/4DApp/recheck/T-AUD-18c/` (`apply_fix.py`, `census.sh`, `rehearsal.patch`).

### Verified context ###
1. **Absent on `fix/T-AUD-18a`** (the report's ABSENT commands, re-run for sizes): no `build_validate*`, no
   `stage_latency_ms` / stage events, no `KGConsistencyError` / exit 78, no `run_orchestrator`, no orjson, no
   `schema_version` in `schemas/response.py`. Registry `du -b` 110240; `kg/*.json` `du -cb` 191093. Observed.
2. **Entry point:** `composition.py::diagnose` calls `LabPipelineAggregator(...).process(request)`. Observed.
3. **Rehearsal** (restored): census `0/0/1` → `5/2/0`; 1 file; comlab `503 passed, 4 skipped, 2 errors` equal. Observed.

### Rulings and the tradeoff that lost ###
- **R1 marks, design kept.** Lost: deleting the sections (loses the design the building row reads).
- **R2 budgets kept.** Lost: replacing them with the sizes (the budget is a ceiling, not a measurement).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `notimpl 5`; `measured 2`; `orjson_claim 0`; one file |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-18c: COMLab DLD marks 5 absent operations not implemented; orjson claim dropped; sizes measured.

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 3) · `apply_fix.py` exits on any literal count other than 1 · traceability:
criteria 1-3 → steps 1-3 · 1c grep: hits in P2 ("only", one file) and Pinned prose ("Every file") — no hit in a ruling or
criterion after rewording criterion 3 · cold read: not triggered · no finding.

### Correction history ###
(none)
