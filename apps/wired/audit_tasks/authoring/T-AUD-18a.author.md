# T-AUD-18a — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` (groups 5 and 7 of `reviews/REVIEW_T-AUD-11g.md`). T-AUD-18 was
split 2026-11-07 into 18a-18e (ledger). Rehearsal: `C:/4DApp/recheck/T-AUD-18a/` (`apply_fix.py`, `census.sh`,
`stale_patterns.txt`, `rehearsal.patch`).

### Verified context ###
1. **Code facts on `fix/T-AUD-17`:** the router defines `_ecu_fault_verdict`, `_ve_evidence_gate`, `_no_start_branch`,
   `_fuel_system_gate`; `ingestion.py` `o2_failure_mode` at line 399; `DTC_REGEX` `^[BCPU][0-3][0-9A-F]{3}$`;
   `_P030X_RE` `^P030[0-8]$`; siblings get `fault_name=sibling_id`; the MODERN era mask "Euro 5 & 6 vehicles
   (~2010-2020)", `[2010, 2020]`, rule pack deactivated; KG files in `comlab/config/kg/`. Observed (grep, read).
2. **DEP-4** already says the projector was retired (T-AUD-4q). Observed.
3. **Readers of the docs:** `test_t_aud_4q_no_projector.py` reads `CROSS_LAB_DEPENDENCIES.md`; comlab equal before and
   after (`503 passed, 4 skipped, 2 errors`). Observed.
4. **Rehearsal** (restored): census `stale 9 → 0`, `notes 0 → 7`; 3 documents changed. Observed.

### Rulings and the tradeoff that lost ###
- **R1 docs follow the code.** Lost: widening the P030x pattern to P0309 (a behaviour change; P0309 is a real
  cylinder-9 code, so it may belong in a later code row).
- **R2 MODERN mask stated, not changed.** Lost: editing the YAML to the 1990-2010 scope (config change, out of a docs row).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `notes 7`; 3 files |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-18a: COMLab dependency table, DTC regex, P030x, sibling name, KG path and MODERN mask match the code.

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 4) · `apply_fix.py` exits on any literal count other than 1 · traceability:
criteria 1-3 → steps 1-3 · 1c grep: hits only in criterion 3 ("only the note and the RESULT") and P2 ("exactly the 3")
— both quantify sets enumerated in Files to touch · cold read: not triggered (no hit in a ruling) · no finding.

### Correction history ###
(none)
