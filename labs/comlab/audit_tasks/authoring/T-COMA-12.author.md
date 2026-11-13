# T-COMA-12 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-18, F-C1-19, F-C1-20; `labs/comlab/comlab/core/fault_atlas_router.py`;
`labs/comlab/comlab/config/tag_discriminator.yaml`; wiki 07 §RULE_CAT_OVERRIDE. Rehearsal: `C:/4DApp/recheck/T-COMA-12/`.

### Verified context ###
1. **Still open on `101f042`:** `_P030X_RE` is `^P030[0-8]$`. The lift loop runs `for tag in _v2_routing_tags`
   with no de-duplication (LEAN_HISTORY, EVAP_HISTORY and BOOST_HISTORY all map to lean_condition). Both abstain
   sites compare `<= ABSTAIN_MARGIN` with no epsilon. Audit probes: `2 failed, 1 passed`. The F-C1-18 probe passes
   because its NORMAL_OPERATION, tags-only input no-fires since T-COMA-6. Observed.
2. **Rehearsal** (restored): new test `13 passed`, base `9 failed, 4 passed`; mutant A (no dedupe) `4 failed`;
   mutant B (epsilon 0) `1 failed`; comlab `510 passed, 4 skipped` (equal); wired `143 → 156`; ui `70`; probes
   `3 passed`; corpus `changed 0 of 314`; ruff clean; `1 file changed, 22 insertions(+), 13 deletions(-)` plus the
   50-line test. Observed.

### Rulings and the tradeoff that lost ###
- **One lift per family** (the yaml says "bounded additive lift"). Lost: one lift per distinct tag (two different
  lean tags would still stack).
- **Epsilon 1e-9, the shim's convention.** Lost: rounding the gap to 2 decimals (that changes behaviour near other
  values).
- **`[0-9]` per the docs.** Lost: covering P0310-P0312 (no document asks for it; 10+ cylinder engines).
- Three findings in one row: one file, scripted, rehearsed together. Plan NONE, difficulty 1. Code row: second-model
  review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `156 passed`; `70 passed` |
| step 2 | SIMULATED | `13 passed`; base `9 failed, 4 passed` |
| step 3 | SIMULATED | `3 passed` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `2 files changed, 72 insertions(+), 13 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-12: one discriminator lift per family; float-safe abstain margin; P0309 in the override pattern.

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 2) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-5 and R5 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
