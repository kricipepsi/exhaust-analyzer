# T-AUD-4c — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **Gate 5 reads a missing count as a recent clear** at the 4b tip:
   `drive_cycles = sanitized_pids.get("drive_cycles_since_clear", 0)` then `if drive_cycles is None or drive_cycles < 1:`.
   Observed (read).
2. **Rehearsal** (`rehearse.py`, `rehearse.out`): 297 v7 cases with OBD; none carries `drive_cycles_since_clear`.
   Base: corpus shape 289 `CODES_RECENTLY_CLEARED`, UI shape 293. With an absent key passing gate 5: those become
   `VALID`; the cold, O₂-fault and CKP gates are unchanged; UI-shape verdict changes 0 (COMLab reads no gate: F-C4-2).
   Observed.
3. **Existing tests**: `test_gate5_drive_cycles_none_fails` pins None → blocked; `test_gate5_codes_cleared_fails`
   pins 0 → blocked. Base of the two OBDLab files: `81 passed`. Observed.

### Rulings and the tradeoff that lost ###
- Unknown (absent or None) passes gate 5; only a stated count below 1 blocks. Lost: keep None blocking (every UI run
  would suppress trim evidence once T-AUD-4g makes COMLab honour the gate — F-C3-3 "expected").
- T-AUD-4c is gate 5 only. Routing the user's DTC codes as `active_dtcs` moves to T-AUD-4g, where the gate first has
  a reader. The cold λ (F-C3-1) is T-AUD-4f. Lost: one larger row; it would cross the 50 % context line mid-row.
- Difficulty 2, plan NONE; code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `81 passed` (2026-11-05, 4b tip) |
| step 2 | RAN | obdlab `388 passed, 2 skipped`; wired `46 passed`; ui `30 passed` |
| step 3 | SIMULATED | `rehearse.py` patches gate 5 in memory: P2 |
| step 4 | DEFERRED | ruff and the log are the observables |

### Exclusivity ###
No other implementer runs. T-AUD-4f also edits OBDLab (`sensor_signal_translator.py`), after this row.

### Progress hook ###
T-AUD-4c: OBDLab gate 5 treats an unknown drive-cycle count as unknown; 289/293 corpus runs become VALID; 0 verdicts.

### Cold read ###
own pass 2026-11-05: P1-P3 measured · literals found once (`drive_cycles = sanitized_pids.get("drive_cycles_since_clear", 0)`,
`test_gate5_drive_cycles_none_fails`) · counts: 81 − 1 + 2 = 82; obdlab 388 + 1 = 389 · traceability: criteria 1-4 →
steps 1-4. cold read: skipped (difficulty 2; the second review covers the code).

### Correction history ###
- **02 (2026-11-05, review; revision before acceptance).** Cowork's re-run equals the RESULT (82, obdlab 389/2,
  others = base; "None blocks" mutant 2 failed; ruff clean). Second review (DeepSeek): APPROVE WITH CORRECTIONS.
  F1 MED (boundary mutant `< 2` survives) upheld: Cowork ran it over the whole obdlab suite, `389 passed`. F2 MED
  (ruff line length) not upheld: `All checks passed!`. LOW reporting items not upheld (re-derived by Cowork); the
  loader's `int` type is outside the write scope. → R2 (02), test file only.
