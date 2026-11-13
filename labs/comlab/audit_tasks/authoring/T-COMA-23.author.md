# T-COMA-23 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_D2_20261017.md` F-D2-7; `docs/COMLab_PRD.md` §5.1 and the abort copy; `docs/COMLab_HLD.md`
§0 row §7.5; `labs/comlab/comlab/core/lab_pipeline_aggregator.py::abort_incomplete`; `apps/ui/app.py` result panel;
`apps/wired/wired/composition.py` (`abort_incomplete` callers). Rehearsal: `C:/4DApp/recheck/T-COMA-23/`.

### Verified context ###
1. **Live today:** `wired.composition.diagnose` returns `abort_incomplete(...)` for incomplete and out-of-range input
   (two call sites); the abort sets `severity_level="OPTIMAL_HEALTH"`; `app.py` renders `severity_banner(...)` with no
   abort branch, so the user sees green "No fault detected." The audit's "no live impact" held only for the
   fatal-gate path. Observed (grep of `abort_incomplete`, `FATAL`, `ERR-` in `apps/ui`).
2. **The shape deviation is already recorded:** HLD §0 row §7.5 states that an abort returns a full
   `OrchestratorFinalUIOutput`. Observed.
3. **Rehearsal** (restored; `git apply --check` passes): ui `73 → 75`; comlab `540`; wired `186`; step 2 `2 passed`,
   base `2 failed`; mutant A `1 failed, 1 passed`; T-AUD-10d's source-needle test still passes; ruff clean;
   `3 files changed, 45 insertions(+), 2 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Fix the rendering, keep the payload.** Lost: a new `SeverityLit` value or the HLD error union (a schema change
  for every consumer; the §0 table already records the single shape). The UI keys on `degradation_mode`, which is
  `FATAL_INCOMPLETE` exactly for an abort.
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `540 passed, 4 skipped`; `186 passed`; `75 passed` |
| step 2 | SIMULATED | `2 passed`; base `2 failed` |
| step 3 | SIMULATED | ruff `All checks passed!`; `3 files changed, 45 insertions(+), 2 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-23: an aborted session shows a red error banner, not "No fault detected." (F-D2-7).

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 3) · patch applies clean · traceability: criteria 1-2 → steps 1-3
and R4 · cold read: not triggered (d1, scripted patch) · no finding.

### Correction history ###
(none)
