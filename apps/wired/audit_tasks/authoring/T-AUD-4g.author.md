# T-AUD-4g — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C4-2 holds** at the 4f tip: no non-test reader of `trim_analytics_gate` in `labs/comlab`; the shim's trim PIDs
   read `obd_live_data.shrtft1`/`longft1`, then the freeze frame. Observed (read; survey
   `C:/4DApp/recheck/scratch/survey_T-AUD-4g.md` A1-A6). The audit's `composition.py:337` anchor is now line 457.
2. **Rehearsal** (`C:/4DApp/recheck/T-AUD-4g/rehearse.py`, `rehearse.out`), two variants on 297 cases:
   - `live` (the ruling): as-is 0 changes; ECT 40: 5 changes, 0 new exceptions, 206 of 295 blocked keep an FF trim.
   - `all` (FF fallback blocked too): as-is 2 changes; ECT 40: 47 changes.
   Observed.
3. **The corpus FF trims copy the live trims** in 207 of 207 cases with a freeze frame, and their FF coolant
   temperature is ≥ 70 °C in 199 (`ffcheck.py`). Forcing only the live ECT to 40 leaves a warm FF. Observed.
4. **Pins** (Cowork's `apply_fix.py` on the working copy, restored): P3. Observed.
5. **4f review F2** is latent: `any(lam > 1.01 …)` short-circuits before the None in `lambdas`; obdlab passes 391 today.
   Observed (read + pass count).

### Rulings and the tradeoff that lost ###
- Block the live trims only (`live`). The gate is computed from live PIDs, and the freeze frame is a separate ECU
  snapshot with its own thermal state. Lost: `all` (47 ECT-40 changes, closer to the audit's zeroed-trims probe), which
  would erase the FF evidence in 206 cases; in this corpus those FF values are copies, a corpus artefact.
- The FF trims get their own cold gate (FF coolant temperature) in T-AUD-4h, with the `active_dtcs` routing (F-C3-3
  rest). Lost: one larger row (DTC routing needs a new composition contract; plan likely REQUIRED).
- `select_perception_lambda` substituting `lambda_measured` is classified by design (handoff 1800 item, 4f review F4).
- Plan NONE, difficulty 3: one guard, measured pins. Lost: the handoff's estimate (plan REQUIRED, difficulty 4), which
  counted the DTC routing now in 4h. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base shim `30 passed`, registry `5 failed, 488 passed, 4 deselected`; rehearsed fix `40`, `5 failed, 498 passed`; mutant `9 failed, 31 passed` |
| step 2 | RAN | comlab `526/4/2 errors`, obdlab `391/2`, wired 46, ui 30 (base and rehearsed fix) |
| step 3 | RAN | `git status --porcelain` empty after the suites with the render test deselected |
| step 4 | RAN | `rehearse.py corpus,ect40 live` on the rehearsed fix: `rehearse_fixed.out` |
| step 5 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-4h follows (DTC routing, FF trim gate).

### Progress hook ###
T-AUD-4g: the registry shim honours OBDLab's trim_analytics_gate for the live trims; 5 cold-case verdicts change.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`trim_analytics_gate → suppresses trim findings when
blocked`, `trim_analytics_gate=TrimAnalyticsGate`, "Trim analytics blocked upstream are not used",
`def test_coverage_matrix_and_aggregate_rate`, the `lambdas = {…}` line, `def _resolve_single_source`); new test names
absent at base · counts: shim 30 + 8 + 1 + 1 = 40, registry 488 + 10 = 498, mutant 8 + 1 = 9 · traceability: criteria
1-4 → steps 1-5 · finding: R1 cited "OBD_VOCABULARY.md §221" (a line, not a section) → rewritten to the row's text.
cold read: skipped (the second review covers the code).

### Correction history ###
(none)
