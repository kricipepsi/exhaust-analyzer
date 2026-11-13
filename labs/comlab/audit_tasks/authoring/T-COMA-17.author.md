# T-COMA-17 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-13, F-C1-14; ADR-0007; `labs/gaslab/gaslab/validity_gates.py`;
`labs/comlab/comlab/core/lab_pipeline_aggregator.py` (`run_fatal_gates_and_routing`, `process`);
`apps/ui/ui_payload.py::routing_notices`. Rehearsal: `C:/4DApp/recheck/T-COMA-17/`.

### Verified context ###
1. **Still open on `1046999`:** the F-C1-13 probe prints `INVALID -> LC-002 lean_condition True FULL_FUSION`; the
   F-C1-14 probe prints `EXTERNAL_O2_SUSPECT -> ERR-ABORT-001 FATAL_INCOMPLETE`; both fail. Observed.
2. **Corpus population (`survey.py`):** of 314 v7 cases, 37 are INVALID, 67 EXTERNAL_O2_SUSPECT, 207 VALID, 3 fail
   before the shim. Of the 37 INVALID: 28 expect a real fault (22 correct today), 9 expect `invalid_input` (6
   correct, by II-001/II-002, which read gas PIDs). Observed.
3. **Options measured (`options.py`, changes only on INVALID; non-INVALID verdicts unchanged in every option):**
   status quo 216/314 (INVALID 28/37); abort 197 (9/37); gas PIDs blanked 206 (18/37); blanked except the II-* rows
   212 (24/37); and the same with no-verdict → invalid_input 212. Observed.
4. **Why INVALID is not "untrustworthy" here:** GASLab's triangle gate marks a sum above 18 % INVALID. Air dilution
   gives that sum, and air in the sample is the finding for the exhaust-leak and misfire cases (CSV-129/130,
   EXT-238/239, CSV-052, ECU-008: all correct when scored). The low band (13.4-13.9 %) holds plausible closed-loop
   readings that score correctly. Observed (sums in the `options.py` output).
5. **Rehearsal** (restored; `git apply --check` passes): comlab `510 → 517 passed, 4 skipped`; wired `176`; ui
   `70 → 73`; new comlab test `7 passed` (base `3 failed, 4 passed`); ui test `3 passed` (base `2 failed, 1
   passed`); mutants A `3 failed`, B/C/D `1 failed` each; probes `1 failed, 1 passed`; corpus `changed 0 of 314`
   against a base `before.json` taken today (the T-COMA-6 `before.json` predates T-COMA-15 and shows 18); ruff clean;
   `6 files changed, 177 insertions(+), 8 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Scored and flagged, not aborted.** Lost: ADR-0007's abort (−19 correct families, and it removes the
  exhaust-leak verdicts where air in the sample is the evidence). The abort stays available with
  `enable_fatal_gates=True`. ADR-0007 is amended in place.
- **No gas-PID blanking.** Lost: "drop gas PIDs only" (−10, or −4 if II-* keep raw gas). It moves cam-timing and
  catalyst cases to lean_condition on trim-only evidence.
- **The flag rides `lab_routing_directive.reasons`.** Lost: a new `ExecutionMeta` field (an LLD §3.3 schema change
  for every consumer). The reasons list already reaches the UI.
- **O2-suspect warns** (the vocabulary's "warn but continue"), with no confidence change. Lost: a cut to
  `DEGRADED_ASSURANCE` (67 corpus cases; no measured basis).
- The F-C1-13 probe's expectation ("FATAL_INCOMPLETE or no fault") is superseded by this ruling; the probe stays.
- Plan NONE, difficulty 2 (contract + UI, scripted). Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `517 passed, 4 skipped`; `176 passed`; `73 passed` |
| step 2 | SIMULATED | `7 passed`; `3 passed`; base `3 failed, 4 passed` and `2 failed, 1 passed` |
| step 3 | SIMULATED | `INVALID -> LC-002 lean_condition True FULL_FUSION`; `1 failed, 1 passed` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `6 files changed, 177 insertions(+), 8 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-17: an INVALID gas sample is scored at LOW_CERTAINTY with a notice; O2-suspect continues (F-C1-13/14).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 5) · patch applies clean · traceability: criteria 1-2 → steps 1-5
and R5 · cold read: not triggered (d2, scripted patch) · no finding.

### Correction history ###
(none)
