# T-COMA-13 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-8; `labs/comlab/docs/COMLab_BDD.md`; ADR-0010;
`labs/comlab/registry/integration_shim.py` (`_resolve_single_source`, `_trims_blocked`, `_ff_cold`). Rehearsal:
`C:/4DApp/recheck/T-COMA-13/`.

### Verified context ###
1. **Still open on `dd8ff2d`:** the probe prints `OL_FAULT -> LC-001 lean_condition 0.95` on NORMAL_OPERATION gas
   with +20 % LTFT and +10 % STFT. T-COMA-6 strict support does not stop it: two trim rows are strict support.
   F-C1-7 is already closed (the probe gives `NS-NO-RULE`). Observed.
2. **The shim has two trim gates:** live trims are dropped when `trim_analytics_gate` is not VALID; freeze-frame
   trims are dropped when ECT < 70 °C. Neither reads `fuel_system_status`, which `wired` fills on
   `obd_live_data`, and which the freeze frame carries itself. Observed.
3. **Rehearsal** (restored): new test `11 passed`, base `7 failed, 4 passed`; mutants A (live) and B (freeze frame)
   `4 failed` each; comlab `510 passed, 4 skipped` (equal); wired `156 → 167`; ui `70`; probe `OL_FAULT ->
   OPTIMAL_HEALTH`, `1 passed`; corpus `changed 0 of 314`; ruff clean; `1 file changed, 14 insertions(+),
   3 deletions(-)` plus the 52-line test. Observed.

### Rulings and the tradeoff that lost ###
- **Suppress per source, in the existing gate.** Lost: ADR-0010's 0.60 cap on the verdict. That needs a
  trim-provenance path through the router; the BDD names suppression, and the probe accepts either.
- **Each source by its own status.** Lost: one global status (the live block's status says nothing about a freeze
  frame captured earlier, and the reverse).
- **No status means closed loop (today's behaviour).** Lost: treating unknown as open. That would drop trims from
  every input without a status (the v7 corpus would move).
- Plan NONE, difficulty 1. Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `167 passed`; `70 passed` |
| step 2 | SIMULATED | `11 passed`; base `7 failed, 4 passed` |
| step 3 | SIMULATED | `CL -> LC-001 lean_condition 0.95`; `OL_FAULT -> OPTIMAL_HEALTH no_fault 0.0`; `1 passed` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `2 files changed, 66 insertions(+), 3 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-13: trims reported in an open fuel loop are not scored (F-C1-8).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-5 and R4 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
