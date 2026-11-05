# T-AUD-4j — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C5-4 holds** at the 4i tip: the UI's only tag is `blue_smoke_on_cold_start_clears`, not a prior key. Observed.
2. **F-C5-5 holds**: `symptom_dna = {}` on `VINDecodeError`; the audit probe `test_f5_symptom_dropped_without_vin` fails
   on base. Observed.
3. **Corpus convention** (`tag_census.py`): the 64 tagged cases, P2. **Rehearsals**: `tag_rehearse.py` base 17 → fixed
   0; the probe passes on the rehearsed fix; the census is identical (`changes {} of 314`). Observed.
4. **Pins** (`apply_fix.py`, restored): P3. Observed.

### Rulings and the tradeoff that lost ###
- Tag by the corpus convention (prolonged crank → non_starter when it will not start, else hard_start_cold). Lost:
  `lean_no_start` for one corpus row (not a prior key) and a tag for stalls (no prior key).
- Resolve the triage alone on a VIN failure, with SymptomLab, not DNALab. Lost: a DNALab API change (out of the app
  scope; `build_vehicle_dna` would need a VIN-optional path).
- One row for both (one symptom path, UI and composition). Difficulty 3, plan NONE. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | rehearsed fix: new 4 and 3, ui 38 (base 34), wired 65 (base 62); mutants 1 failed each |
| step 2 | RAN | comlab `526/4/2 errors` (base and fix) |
| step 3 | RAN | `git status --porcelain` empty after the suites |
| step 4 | RAN | tag_rehearse `[fixed] changed 0`; probe f5 passes on the fix; census `changes {} of 314` |
| step 5 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-4k follows.

### Progress hook ###
T-AUD-4j: the UI symptom tag is a prior key; the triage reaches COMLab when the VIN does not decode.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`triage["csv_primary_symptom"] = "blue_smoke_on_cold_start_clears"`,
`except VINDecodeError:`, `symptom_dna = {}` in that branch, `def _missing(`, the four UI labels); new names absent at
base · counts: ui 34 + 4 = 38, wired 62 + 3 = 65 · traceability: criteria 1-4 → steps 1-5 · no finding. cold read:
skipped (the second review covers the code).

### Correction history ###
(none)
