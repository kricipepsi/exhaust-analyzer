# T-AUD-10a — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/FIX_PLAN.md` T-AUD-10 (F-C5-7, 8, 12); this slice F-C5-8 (`audit/reports/R1_C5_20261017.md`).
Rehearsal: `C:/4DApp/recheck/T-AUD-10a/` (`measure.py`, `apply_fix.py`, `test_t_aud_10a_distinct_siblings.py`,
`rehearsal.patch`).

### Verified context ###
1. **Code on `fix/T-COMA-4`:** `apps/ui/app.py:948` and `:987` iterate `verdict.differential_siblings[:2]`;
   `DifferentialSiblingOut` carries `fault_family` (`labs/comlab/comlab/schemas/response.py`). Observed.
2. **Corpus:** 311 results (3 errors); 306 carry 5 siblings; today 172 repeat the winner's family; the helper gives
   2/1/0 cards for 283/23/5. `measure.py`. Observed.
3. **Rehearsal** (restored): ui `57 → 60 passed`; the new test `3 passed`, `3 failed` on the base; wired `106`; ruff
   clean; 2 source files `21 insertions(+), 2 deletions(-)`. Observed.
4. **Base:** `apps/ui/app.py` and `ui_payload.py` are in the unmerged chain: the row stacks on its tip (FALLBACK_LANES
   Lane 1). Observed.

### Rulings and the tradeoff that lost ###
- **R1 no padding.** Lost: padding to 2 cards with a same-family sibling (today's defect).
- **R2 helper in `ui_payload`.** Lost: inline filtering in each loop (two copies; not unit-testable).
- **T-AUD-10 split:** 10a F-C5-8 (this), 10b F-C5-7 (horizon, routing disclosure, echo, impacted subsystems, severity
  ribbon), 10c F-C5-12 (decode through `wired`, tied to F-C5-9). Lost: one row (three unrelated UI changes).
- Code row: second-model review at acceptance. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `60 passed`; `106 passed` |
| step 2 | SIMULATED | `3 passed`; base `3 failed` |
| step 3 | SIMULATED | ruff clean; stat `21 insertions(+), 2 deletions(-)`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-10a: UI sibling cards show up to 2 distinct families (F-C5-8); 172 → 0 winner-family repeats on the corpus.

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 2, 3) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
