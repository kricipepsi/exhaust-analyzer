# T-COMA-16 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_D1_20261017.md` F-D1-12; `labs/comlab/wiki/09_calibration_confidence.md`;
`labs/comlab/comlab/core/fault_atlas_router.py`; `v3/reports/V3_TOPK_CEILING_2026-06-30.md`;
`v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md`; `v3/V3_PROGRESS.md`; `apps/wired/ship_tasks/reports/SHIP_VERIFY_2026-07-07.md`.

### Verified context ###
1. **Still open on `127c19e`:** the two constants cite only the TOPK report. That report's §6 recommends
   `abstain_floor <0.80, abstain_margin <0.05`. The 0.02 margin is the owner-picked T-V3-3D commit (V3_PROGRESS row
   T-V3-3D "ABSTAIN_MARGIN 0.05->0.02"; SHIP_VERIFY F-1). The sweep is in the abstain checkpoint, Tier 3 (0.02:
   77.89 %, 229 of 294). The checkpoint records the floor as inert (0 of 297). Wiki 09 has tier bands but no abstain
   section. Observed.
2. **No test reads the graph cache** that indexes wiki 09 (`labs/comlab/graph/v2_current`). Observed.
3. **Rehearsal** (restored): comlab `510 passed, 4 skipped`, wired `176`, ui `70` (all equal); ruff clean;
   `CONCEPT_ABSTAIN` count 3; both constants cite the section; `2 files changed, 21 insertions(+), 3 deletions(-)`.
   Observed.

### Rulings and the tradeoff that lost ###
- **State each value's own source, in the wiki.** Lost: citing the TOPK report for both (wrong for the margin), or
  changing the margin to the report's 0.05 (that is a value decision the owner already made in T-V3-3D).
- **The no-rule abstention (T-COMA-6) and the epsilon (T-COMA-12) are documented in the same section,** because they
  decide `abstain_reason` too.
- Docs row (comments and wiki): no second review (CLAUDE.md step 6). Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `176 passed`; `70 passed` |
| step 2 | SIMULATED | `3`; `2` |
| step 3 | SIMULATED | ruff `All checks passed!`; `2 files changed, 21 insertions(+), 3 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-16: abstain thresholds documented in wiki 09 §CONCEPT_ABSTAIN and cited (F-D1-12).

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
