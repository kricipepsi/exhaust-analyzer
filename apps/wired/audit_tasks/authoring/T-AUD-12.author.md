# T-AUD-12 — authoring sidecar (Windows Cowork, 2026-11-06)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_symptomlab.md`, `reviews/REVIEW_T-AUD-11a.md`. Rehearsal:
`C:/4DApp/recheck/T-AUD-12/` (`apply_fix.py`, `rehearsal.patch`, `census.sh`).

### Verified context ###
1. **Each upheld finding re-read at its doc line** on `fix/T-AUD-4t`: PRD:30, PRD:98, PRD:203, HLD:50, HLD:190,
   LLD:104, DLD:78, DLD:92, DLD:124, DLD:174-178, BDD (7 `tests/test_` paths), ADR-0002 Decision. Observed.
2. **All five named test files exist under `labs/symptomlab/tests/unit/`** (they did not when 11a ran). Observed.
3. **ADR-0008 (Accepted) fixes the catalog at 21 pairs;** `validator.py` raises unless exactly 21. Observed.
4. **Rehearsal** (restored): census base `stale 18`, after `stale 0`; `paths 5 missing 0` both; symptomlab 72 passed;
   six docs, 32 insertions / 25 deletions. Observed.

### Rulings and the tradeoff that lost ###
- **Keep the 21-pair cap; fix the wording** (KR4, ADR-0002). Lost: a truly open vocabulary (deriving the count from
  the YAML), which would void ADR-0008 and drop the guard against an accidentally edited catalog.
- **`oil_consumption` is described as shipped** (the YAML's 7th tier_1). Lost: nothing; the deferred text was stale.
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `paths 5 missing 0` |
| step 2 | SIMULATED | `72 passed` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-12: SymptomLab docs match the code (11 drift findings of 11a fixed; 21-pair cap kept).

### Cold read ###
own pass 2026-11-06: P1-P2 measured · `apply_fix.py` exits on any literal count other than 1 (5 and 7 for the test-path
replacements) · traceability: criteria 1-3 → steps 1-3 · patched: repo-wide baselines written · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "only"); 0 findings, 0 patched — 4 calls.

### Correction history ###
(none)
