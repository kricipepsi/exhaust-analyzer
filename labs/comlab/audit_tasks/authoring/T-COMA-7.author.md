# T-COMA-7 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C1_20261017.md` F-C1-4; wiki 07 §RULE_CAT_OVERRIDE; ADR-0010;
`labs/comlab/comlab/core/fault_atlas_router.py`. Rehearsal: `C:/4DApp/recheck/T-COMA-7/`.

### Verified context ###
1. **Still open on `42cf560`:** the probe prints `verdict: MF-001 misfire severity: WARNING_DEGRADED_PERFORMANCE`.
   The v2 branch returns `OrchestratorFinalUIOutput(**v2_output)` before the legacy Step 4
   `apply_catalyst_damage_override`; `_req = sanitized.get("request")` is in scope. Observed.
2. **`apply_catalyst_damage_override` reads only `request.dtc_lab_output`** (`mil_flashing`, `confirmed_dtcs`
   against `^P030[0-9]$`); its `verdict` argument is unused. Observed.
3. **`wired` carries `mil_flashing`** from the DTC input (`composition.py`, the DTCLab sanitizer call). Observed.
4. **Rehearsal** (restored): wired `115 → 121`; the new test `6 passed`, base `3 failed, 3 passed`; mutant
   (override skipped) `3 failed`; comlab `508 passed, 4 skipped`, ui `70` (equal); probe `CRITICAL_IMMEDIATE_STOP`;
   v7 corpus fault code and family unchanged on 314 of 314; ruff clean; `1 file changed, 12 insertions(+),
   1 deletion(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Call the existing override on the v2 result.** Lost: duplicating the rule in the shim (two homes for one safety
  rule); refactoring the override's signature (an unused `verdict` stays, `None` passed with a type-ignore).
- **F-C1-1 is T-COMA-6 (registered, deferred).** Its survey (`C:/4DApp/recheck/T-COMA-6/firing_survey.py`) shows
  seven rules firing on a healthy car; the `none_present`-only change moved the sink (MF-005 → CF-002) with 0 corpus
  changes, so it is not shipped alone.
- Plan NONE, difficulty 2. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `508 passed, 4 skipped`; `121 passed`; `70 passed` |
| step 2 | SIMULATED | `6 passed`; base `3 failed, 3 passed` |
| step 3 | SIMULATED | `verdict: MF-001 misfire severity: CRITICAL_IMMEDIATE_STOP`; `1 passed, 6 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; `1 file changed, 12 insertions(+), 1 deletion(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-7: flashing MIL + P030x forces CRITICAL_IMMEDIATE_STOP on the default path (F-C1-4, safety).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1, 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R3 · cold read: not triggered (d2, scripted) · no finding.

### Correction history ###
(none)
