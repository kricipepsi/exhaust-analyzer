# T-COMA-11 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C1_20261017.md` F-C1-10; `labs/comlab/comlab/core/fault_atlas_router.py` v2 re-sorts.
Rehearsal: `C:/4DApp/recheck/T-COMA-11/`.

### Verified context ###
1. **Still open on `d319e8c`:** two sites set `confidence_score` from `scored_rules[0]` after a re-sort without
   checking it is the verdict's rule; the probe prints `reported: 0.95 own raw score: 0.9` (NS-001's 0.95 on MF-002).
   Observed.
2. **Corpus (314 v7 cases, `before.json` vs `after.json`):** 17 confidences change (e.g. CASE-013 LC-002 1.0 → 0.96,
   CASE-016 1.0 → 0.91); 0 fault code, family or abstain changes. Observed (`conf.py`).
3. **Rehearsal** (restored): wired `123 → 127`; the new test `4 passed`, base `4 failed`; mutant (discriminator site
   reverted) `2 failed, 2 passed`; comlab `510 passed, 4 skipped`, ui `70` (equal); probe passes; ruff clean;
   `1 file changed, 14 insertions(+), 2 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Report the named rule's own score; keep the winner.** Lost: letting the re-sort pick a new winner (a ranking
  change that moves verdicts; T-AUD-2 owns it).
- Plan NONE, difficulty 1. Code row: second-model review. Rows past 50 % by the operator's instruction (2026-11-07).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `127 passed`; `70 passed` |
| step 2 | SIMULATED | `4 passed`; base `4 failed` |
| step 3 | SIMULATED | `reported: 0.9 own raw score: 0.9`; `1 passed, 6 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; `1 file changed, 14 insertions(+), 2 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-11: the verdict confidence is the named fault's own score after the re-sorts (F-C1-10).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1-3) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
