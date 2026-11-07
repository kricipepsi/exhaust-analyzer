# T-COMA-8 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C1_20261017.md` F-C1-9; `labs/comlab/comlab/core/lab_pipeline_aggregator.py::process`.
Rehearsal: `C:/4DApp/recheck/T-COMA-8/`.

### Verified context ###
1. **Still open on `e65c2d0`:** the probe prints `in: PARTIAL  out: HIGH`. Two sites in `process` hard-code `"HIGH"`:
   the routed path (after `self._router.route`) and the `fault_code` test-hook path. Observed.
2. **Through `wired`, after the fix:** `WME01MC01XH072806` → PARTIAL, `UNKNOWNVIN0000000` → NONE (full pipeline ran).
   Observed.
3. **Rehearsal** (restored): comlab `508 → 510`, wired `121 → 123`, ui `70`; base `2 failed` each; mutant (second site
   HIGH) comlab test `1 failed, 1 passed` (the wired test alone did not see it: it runs the routed path only);
   probe `out: PARTIAL`; corpus 0 of 314 changed; ruff clean; `1 file changed, 2 insertions(+), 2 deletions(-)`.
   Observed.

### Rulings and the tradeoff that lost ###
- **Echo only.** Lost: GAS_DOMINANT and the confidence cap for PARTIAL in the same row (a behaviour change that moves
  verdicts; it needs its own ruling under T-AUD-2).
- **Two tests:** the wired test proves the user-facing value; the comlab test covers the `fault_code` site the wired
  path cannot reach.
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `123 passed`; `70 passed` |
| step 2 | SIMULATED | `2 passed`; `2 passed`; base `2 failed` each |
| step 3 | SIMULATED | `in: PARTIAL  out: PARTIAL degradation: FULL_FUSION`; `1 passed, 6 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; `1 file changed, 2 insertions(+), 2 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-8: execution_meta.vin_confidence echoes the decode grade on both builder paths (F-C1-9).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1, 3) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
