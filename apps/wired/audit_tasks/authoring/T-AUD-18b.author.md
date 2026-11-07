# T-AUD-18b — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` COMLab_LLD section (22 bullets; group 3 of
`reviews/REVIEW_T-AUD-11g.md`). Rehearsal: `C:/4DApp/recheck/T-AUD-18b/` (`apply_fix.py`, `rehearsal.patch`).

### Verified context ###
1. **The 22 bullets** are the report's measured facts (11g reviewed 16 of 73 directly, the rest by quote or ABSENT
   command); the table restates them, two `SymptomDNA` bullets in one row. Observed (report read).
2. **Rehearsal** (restored): 21 table rows, 1 heading, one file, 29 insertions; comlab `503 passed, 4 skipped,
   2 errors` equal. Observed.

### Rulings and the tradeoff that lost ###
- **R1 one delta table.** Lost: rewriting 22 listings in place (about three times the edit, past this session's context
  budget; the table makes each wrong listing traceable now).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `deltas 21 heading 1`; one file |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-18b: COMLab LLD gains a 21-row shipped-code delta table (group 3 of 11g).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 2) · `apply_fix.py` exits unless the anchor occurs once · traceability:
criteria 1-3 → steps 1-3 · 1c grep: no hit in a ruling or criterion · cold read: not triggered · no finding.

### Correction history ###
(none)
