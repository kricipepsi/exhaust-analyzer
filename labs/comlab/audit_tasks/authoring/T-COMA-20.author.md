# T-COMA-20 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-16; `labs/comlab/comlab/core/fault_atlas_router.py` (Phase 3).
Rehearsal: `C:/4DApp/recheck/T-COMA-20/`.

### Verified context ###
1. **Still open on `6f58e89`:** the probe raises `AttributeError: 'NoneType' object has no attribute
   'confirmed_dtcs'` in Phase 3. Observed.
2. **Only one unguarded read:** of six `request.dtc_lab_output` reads in the router, five already test `None`
   (POA tags, no-start branch, P030x severity, v2 tags, downstream O2). Observed (`grep -n dtc_lab_output`).
3. **Rehearsal** (restored; `git apply --check` passes): comlab `524 → 527`; wired `186`; ui `73`; step 2
   `3 passed`, base `3 failed`; mutants A and B `3 failed` each; probe `v1 no-DTC -> OPTIMAL_HEALTH`, `1 passed`;
   corpus `changed 0 of 314`; ruff clean; `2 files changed, 43 insertions(+), 2 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **No DTC output = no codes, no MIL** (the v2 path's reading). Lost: aborting the v1 session on missing DTC data
  (`dtc_lab_output` is optional in the schema; wired omits it whenever the UI has no DTC input).
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `527 passed, 4 skipped`; `186 passed`; `73 passed` |
| step 2 | SIMULATED | `3 passed`; base `3 failed` |
| step 3 | SIMULATED | `v1 no-DTC -> OPTIMAL_HEALTH`; `1 passed` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `2 files changed, 43 insertions(+), 2 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-20: the v1 path gives a verdict with no DTCLab output (F-C1-16).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 3) · patch applies clean · traceability: criteria 1-2 → steps 1-5
and R3 · cold read: not triggered (d1, scripted patch) · no finding.

### Correction history ###
(none)
