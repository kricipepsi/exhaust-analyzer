# T-AUD-4a — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **The defect holds** at `49060ac`: `_PID_DISPATCH["o2_downstream"]` is `(("ff", "o2_voltage_b1s1"),)`, the same
   source as `"o2_voltage"`. Observed.
2. **Resolver rehearsal** (stdin, `labs/comlab`): base gives 0.85 / 0.85 / 0.85 (two-source `o2_downstream`, FF-only
   `o2_downstream`, `o2_voltage`); with the R1 entry 0.1 / None / 0.85. Observed.
3. **No B1S2 in DTCLab's freeze frame**: `grep -rn "b1s2" labs/dtclab/dtclab --include=*.py` prints nothing. So R1 has
   no FF fallback. Observed.
4. **Corpus effect** (`rehearse.py`, `rehearse.out`): the v7 cases carry no FF B1S1, so the base resolves
   `o2_downstream` to None on all 314; R1 gives 11 measured values, 1 score change (CASE-022), 0 verdict changes.
   The audit's 0.85 V example needs a DTC freeze frame (UI runs with DTCs). Observed.
5. **The audit probe is stale**: `test_c4_probes.py -k f4` fails `KeyError: 'diag'` on the base (its spy no longer
   fires). Observed.
6. **Only SF-006 and EL-002** read `"pid": "o2_downstream"` (`grep -rln` over `registry/rules/`). Observed.

### Rulings and the tradeoff that lost ###
- Measured channel only, no FF fallback. Lost: fall back to B1S1 when no live reading (the defect itself).
- v1 router alias out of scope. Lost: one fix for both paths (v1 is not the production path; F-C4-5).
- Difficulty 2, plan NONE (one entry, three tests); code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `27 passed` (2026-11-05, `49060ac`) |
| step 2 | RAN | base `84 passed` |
| step 3 | RAN | comlab `526 passed, 4 skipped, 2 errors` (at `3c2d512`/`324fd5a`, comlab unchanged since); wired `41 passed`, ui `30 passed` (at `324fd5a`) |
| step 4 | SIMULATED | `rehearse.py` patches R1 in memory: P4 |
| step 5 | DEFERRED | ruff and the log are the observables |

### Exclusivity ###
No other implementer runs. T-AUD-4b-e follow in order; none touches `integration_shim.py`'s O₂ entries.

### Progress hook ###
T-AUD-4a: o2_downstream reads obd downstream_o2_v (no FF fallback); 11 corpus cases gain a value, 0 verdicts change.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`"o2_downstream": (("ff", "o2_voltage_b1s1"),)`,
`"downstream_o2_v": (("obd", "downstream_o2_v"),)`) · counts: 27 + 3 = 30; 84 + 3 = 87 · traceability: criteria 1-4 →
steps 1-5, R2 tests → criterion 1. cold read: skipped (difficulty 2; the second review covers the code).

### Correction history ###
(none)
