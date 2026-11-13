# T-COMA-19 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-15; `labs/comlab/comlab/schemas/ingestion.py::SessionMetadata`;
`labs/comlab/tests/unit/test_abort_incomplete.py`. Rehearsal: `C:/4DApp/recheck/T-COMA-19/`.

### Verified context ###
1. **Still open on `59f3e41`:** the probe fails for `''`, `HORIZON_FOO` and `horizon_legacy` (each becomes
   `HORIZON_MODERN`). Observed.
2. **Producers:** wired derives the era from the Euro category (`_derive_horizon`), the `vehicle_dna` path passes
   `vin.resolved_horizon.value`; every test fixture sends one of the three values, except the one pin that encoded
   the defect (`test_abort_incomplete_unknown_horizon_defaults_modern`). Observed (grep of `resolved_horizon` in
   `labs/comlab/tests` and `apps`).
3. **Rehearsal** (restored; `git apply --check` passes): comlab `517 → 524`; wired `186`; ui `73`; step 2
   `11 passed`, base `6 failed, 5 passed`; mutants A `2 failed`, B `5 failed`; probe `1 passed, 2 skipped`;
   corpus `changed 0 of 314`; ruff clean; `3 files changed, 44 insertions(+), 4 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Reject at the schema, normalise case.** Lost: the wiki 04 Euro fallback (`SessionMetadata` carries no Euro
  category), and the "flag it" option (a LOW_CERTAINTY verdict on an unknown era still runs with MODERN's 0.02 λ
  tolerance).
- **Leave the aggregator's MODERN fallbacks.** Lost: deleting them (defence for a non-schema caller; a later row).
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `524 passed, 4 skipped`; `186 passed`; `73 passed` |
| step 2 | SIMULATED | `11 passed`; base `6 failed, 5 passed` |
| step 3 | SIMULATED | two `schema rejected` skips; `1 passed, 2 skipped` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `3 files changed, 44 insertions(+), 4 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-19: an unknown resolved_horizon is rejected; case is normalised (F-C1-15).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 3) · patch applies clean · traceability: criteria 1-2 → steps 1-5
and R4 · cold read: not triggered (d1, scripted patch) · no finding.

### Correction history ###
(none)
