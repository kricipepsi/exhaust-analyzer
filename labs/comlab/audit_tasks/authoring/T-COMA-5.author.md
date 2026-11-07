# T-COMA-5 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C1_20261017.md` F-C1-3; `audit/FIX_PLAN.md` T-AUD-2; `labs/comlab/registry/integration_shim.py`
verdict builder. Rehearsal: `C:/4DApp/recheck/T-COMA-5/`.

### Verified context ###
1. **Still open on `04c5289`:** the C1 probes `-k "no_fault_winner or healthy or mechanism"` → 4 failed; the
   no-fault probe prints `verdict: NF-001 no_fault True WARNING_DEGRADED_PERFORMANCE`. Observed.
2. **The winner branch sets `is_fault_detected: True` and `WARNING_DEGRADED_PERFORMANCE` for every rule**, the
   no-fault family included; the `winner is None` branch already uses `_NO_FAULT_SEVERITY` (`"OPTIMAL_HEALTH"`).
   Observed.
3. **Through `wired.diagnose`:** pristine gas (HC 30, CO 0.1, CO2 15.0, O2 0.3, NOx 40) plus neutral OBD → NF-001;
   gas only → EF-004 `ecu_fault` (an F-C1-1-class sink, out of scope). Observed.
4. **Rehearsal** (restored): wired `113 → 115`; the new test `2 passed`, base `1 failed, 1 passed`; mutant (severity
   unchanged) `1 failed`; comlab `508 passed, 4 skipped`, ui `70` (equal); probe `verdict: NF-001 no_fault False
   OPTIMAL_HEALTH`, `1 passed`; ruff clean; `1 file changed, 4 insertions(+), 2 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Fix the flag and the severity in the shim's winner branch.** Lost: a UI-side mapping by family (the UI already
  renders `severity_level`; the contract says the producer owns both fields).
- **F-C1-1 stays T-AUD-2.** Lost: one big row (rule-firing changes move many corpus verdicts and need their own
  survey).
- **Operator 2026-11-07:** VIN work is parked; diagnosis correctness comes next. This is the first such row.
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `508 passed, 4 skipped`; `115 passed`; `70 passed` |
| step 2 | SIMULATED | `2 passed`; base `1 failed, 1 passed` |
| step 3 | SIMULATED | `verdict: NF-001 no_fault False OPTIMAL_HEALTH`; `1 passed, 6 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; `1 file changed, 4 insertions(+), 2 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-5: a no-fault winner reports is_fault_detected False and OPTIMAL_HEALTH (F-C1-3).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1, 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
