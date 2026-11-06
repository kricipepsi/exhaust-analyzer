# T-AUD-4n — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4n/` (`apply_fix.py`, `rehearsal.patch`, `tests/`).

### Verified context ###
1. **No reader** of fuel blend, mileage or `lambda_2500` outside the UI (P1). Observed.
2. **Rehearsal** (restored): new file base `4 failed`, fix `4 passed`; ui 41 → 45; wired 85; the tuple mutant fails
   `test_payload_sends_no_lambda_2500`; ruff clean. A first draft of the widget test read `at.radio` and passed on the
   base (the inputs are keyed checkboxes); it now reads checkbox keys and fails on the base. Observed.

### Rulings and the tradeoff that lost ###
- **Remove, not wire.** Fuel blend and mileage have no consumer anywhere; `high_idle_lambda` is computed by GASLab from
  the gases. Lost: the inputs, which a future GASLab ethanol stoich or a wear prior could use (each would need its own
  row with a named consumer).
- **F-C5-10 split.** Notes, the OBD high-idle panel, the Mode $06 state and the two hard-coded gas status fields each
  have a would-be consumer and need wiring rulings: T-AUD-4r. Lost: closing F-C5-10 in one row.
- Plan NONE, difficulty 2: deletions only, quoted and rehearsed. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `rehearsal.patch` + the test file: `4 passed`; ui `45 passed` (base 41 with the new file deselected) |
| step 2 | SIMULATED | wired `85 passed` |
| step 3 | SIMULATED | no `fuel_blend`, `mileage` or `lambda_2500` in the two files after the patch |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4n: the UI stops offering Fuel blend, Mileage and the high-idle measured lambda, which no code reads.

### Cold read ###
own pass 2026-11-06: P1-P3 measured · literals found once (the two `_check_radio` lines, `gas_high_lambda = None`, the
`key="gas_lambda_high"` line, `"gas_lambda_2500": gas_high_lambda,`, the tuple, the three FIELD_HELP keys, the two
test_ui asserts) · counts: ui 41 + 4 = 45 · traceability: criteria 1-4 → steps 1-4 · no finding. cold read 2026-11-06:
not triggered (1c hits: "only" in Context and Out of scope names no set a ruling defines).

### Correction history ###
(none)
