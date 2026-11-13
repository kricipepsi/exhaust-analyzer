# T-COMA-24 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-22; `labs/comlab/tests/unit/test_lab_pipeline_aggregator.py`;
`docs/COMLab_BDD.md` "Tests:" lines for validation and fatal gates. Rehearsal: `C:/4DApp/recheck/T-COMA-24/`.

### Verified context ###
1. **Still open on `68703b8`:** the file gives `1 passed, 4 skipped`; the BDD cites it for validation and fatal
   gates. Observed.
2. **Two of four pass today:** with all skips removed, `2 failed, 3 passed`; the two trim tests raise
   `KeyError: 'shrtft1'` on the fixture and target `sanitize_and_aggregate`, which has no production caller.
   Observed.
3. **Rehearsal** (restored; `git apply --check` of the saved diff passes): `applied 6 edits`, a second run exits 1;
   comlab `540/4 → 542/2`; step 2 `3 passed, 2 skipped` with the new reason; ruff clean; `2 files changed, 4
   insertions(+), 6 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Un-skip the passing two; keep the dead-path two skipped with a true reason.** Lost: rewriting the trim tests
  against `process()` (T-COMA-21's test already pins the shipped GAS_DOMINANT rule) and deleting the dead methods (a
  later row).
- Plan NONE, difficulty 1. Code row (tests): second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `542 passed, 2 skipped`; `186 passed`; `75 passed` |
| step 2 | SIMULATED | two `T-COMA-24` skip lines; `3 passed, 2 skipped` |
| step 3 | SIMULATED | ruff `All checks passed!`; `2 files changed, 4 insertions(+), 6 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-24: the BDD-cited aggregator tests run or say why not (F-C1-22).

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
