# T-COMA-25 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: T-COMA-24 residual (F-C1-22); `labs/comlab/comlab/core/lab_pipeline_aggregator.py`
(`run_fallback_tree`, `sanitize_and_aggregate`); `docs/COMLab_HLD.md` §0; `docs/Vocabulary/SEMANTIC_CONTRACT.md`.
Rehearsal: `C:/4DApp/recheck/T-COMA-25/`.

### Verified context ###
1. **No production caller:** the only `.py` references are the two methods and the two skipped tests; `process()`
   reads the directive itself (`_map_degradation`, `_gas_sample_reasons`). Observed (grep over `labs`, `apps`).
2. **The stub was wrong where it ran:** it raised `NotImplementedError` for every non-non-starter session. Observed.
3. **Rehearsal** (restored; `git apply --check` passes): `applied 6 edits`, a second run exits 1; comlab
   `542 passed, 2 skipped → 542 passed`; wired `186`; ui `75`; corpus `changed 0 of 314`; ruff clean (after removing
   the unused `DegradationMode` import); `4 files changed, 4 insertions(+), 55 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Delete, do not implement.** Lost: building the HLD fallback tree (the shipped `process()` already covers the
  directive; the tree's abort for missing trims is not in the shipped contract).
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `542 passed`; `186 passed`; `75 passed` |
| step 2 | SIMULATED | no output |
| step 3 | SIMULATED | `changed 0 of 314` |
| step 4 | SIMULATED | ruff `All checks passed!`; `4 files changed, 4 insertions(+), 55 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-25: dead run_fallback_tree / sanitize_and_aggregate removed.

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
