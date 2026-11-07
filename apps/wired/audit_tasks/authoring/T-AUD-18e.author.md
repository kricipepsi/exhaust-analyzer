# T-AUD-18e — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` (PRD, HLD, BDD findings of groups 1-2, `reviews/REVIEW_T-AUD-11g.md`)
and `audit/drift/2026-11-05_DRIFT_REPORT_comlab_adr.md` (4 findings, `reviews/REVIEW_T-AUD-11h.md`).
Rehearsal: `C:/4DApp/recheck/T-AUD-18e/` (`apply_fix.py`, `census.sh`, `rehearsal.patch`).

### Verified context ###
1. **Gates** (`core/lab_pipeline_aggregator.py` on `fix/T-AUD-18d`): order 001 (`validity not in ("VALID",
   "BORDERLINE")`), 002 (`engine_warmed`), 004 (`metadata.vin_confidence`), then 005
   (`check_schema_version(request.metadata.schema_version)`, minimum `"1.0"`); run only when `enable_fatal_gates`
   (default `False` in the aggregator and `wired.composition.diagnose`; `apps/ui/app.py:891` calls `diagnose(raw_inputs)`).
   The four messages quoted in the PRD table are the code's strings. Observed.
2. **Abort output:** full `OrchestratorFinalUIOutput`, `FATAL_INCOMPLETE`, `fault_code` = code, `fault_name`
   `Fatal Abort: <code>`, message in `display_headline` / `actionable_remediation`; no `ERR-VIN` in the package. Observed.
3. **Degradation:** `_map_degradation` → `GAS_DOMINANT` iff `suppress_gaslab`, else `FULL_FUSION`; `SINGLE_POINT`
   only in `analytics/delta_engine.py`; `run_fallback_tree` called only by `sanitize_and_aggregate`. Observed.
4. **ADRs:** `EGR_HISTORY` injection (`fault_atlas_router.py`), `EURO_6`/`EURO_7` in `EuroEmissionCategory` and in no
   `config/` file, MODERN → `_default_mask`, `enable_delta_v2: bool = False`. Observed.
5. **Already fixed:** PRD DTC regex and KG path (T-AUD-18a). The BDD already states that `BORDERLINE` passes. Observed.
6. **Rehearsal** (restored): census `0/0/0/0/2` → `9/8/3/4/0`; 7 files; comlab `503 passed, 4 skipped, 2 errors`
   equal. Observed.

### Rulings and the tradeoff that lost ###
- **R1 delta tables, behaviour to T-AUD-3.** Lost: in-place rewrites of the gate lists (T-AUD-3 may change the code
  under them, F-C1-9, 11-16; F-D2-7, 14); lost: deciding `BORDERLINE` here (a code decision, and the BDD and code agree).
- **R2 ADR sentences in place.** Lost: a delta table per ADR (one sentence each does not need a table).
- Docs row: no second-model review. Plan NONE, difficulty 1 (the ledger's d3 assumed rulings by the implementer; Cowork
  made them).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `PRD rows 9`; `HLD rows 8`; `BDD rows 3`; `adr_marks 4`; `adr_stale 0`; seven files |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-18e: COMLab PRD/HLD/BDD gate and degradation delta tables (9/8/3 rows); 4 ADR sentences follow code.

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 6) · `apply_fix.py` exits on any anchor or literal count other than 1 ·
traceability: criteria 1-3 → steps 1-3 · 1c grep: "exactly" in P2 is the measured seven-file list · cold read: not
triggered (d1, scripted, the 18a-18d pattern) · no finding.

### Correction history ###
(none)
