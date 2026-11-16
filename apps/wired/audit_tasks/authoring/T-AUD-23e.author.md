# T-AUD-23e — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23d, 281 live threshold
roots stay unverified (DIAGNOSTIC_THRESHOLD/TYPICAL_RANGE/LEGAL_LIMIT, no `same_as`, no verdict or retirement, not in
v1 files, no NOT LIVE/RESOLVED). This slice takes `sensor_fault.json`. Survey by Cowork. Lane: Hydrogen high
(difficulty 3).

### Verified context ###
1. **Scope: 28 roots, all in `labs/comlab/registry/rules/sensor_fault.json`.** Listed on 5344629 with
   `C:/4DApp/recheck/T-AUD-23e/roots.py` (counts per file: shim 32, mechanical_wear 30, cam_timing 28, sensor_fault
   28, non_starter 25; total 281). No sentinel among them.
2. **Checker: scope 23e `VERDICTS FAIL 28 error(s)`; 17/23a/23b/23d OK (20, 25, 29, 29).** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24j/promoted.json`): sensor_fault verdict 37, right 16, expected 25.**
   `C:/4DApp/recheck/T-AUD-23e/fam.py`.
4. **Delta sign: `delta = normalized_obd_lambda - lambda_chem`** (`perception_contradiction.py:180`).
5. **Sources S001-S036 exist.** `sources.csv`. R4's claim lists equal the scope file (diff empty).

### Rulings and the tradeoff that lost ###
- **sensor_fault before the shim.** It is the family with the most wrong verdicts left (21 of 37). Lost: the 32
  integration_shim.py literals (most are internal tie-breaks reached only from a lazy router import; liveness not
  measured).
- **R4's 20 % band for CONFIRMED,** as in T-AUD-23d. Lost: exact match only.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 28 error(s)` (P2) |
| step 2 | RAN | the four P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23e: verify 28 SF rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23e.md`).

### Correction history ###
(none)
