# T-AUD-23g — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23f, 229 live threshold
roots stay unverified (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice takes `cam_timing.json`. Survey by
Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 28 roots, all in `cam_timing.json`.** Listed on e650e3e with `roots.py`. No sentinel. R4's claim lists
   equal the scope file (diff empty); the R4 values match `claims_comlab.csv` (spot check of 9).
2. **Checker: scope 23g `VERDICTS FAIL 28 error(s)`; six earlier scopes OK.** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24k/promoted.json`; rule data unchanged by 24l): cam_timing expected 11,
   verdict 9, right 7.** `recheck/T-AUD-23e/fam24k.py`.
4. **Sources S001-S041 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **cam_timing before mechanical_wear / non_starter / shim.** It is the largest rule file left with corpus cases at
  stake (11). Lost: mechanical_wear 30 (expected 4, verdict 0) and non_starter 25 (expected 6, right 5).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 28 error(s)` (P2) |
| step 2 | RAN | the six P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23g: verify 28 CT rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23g.md`).

### Correction history ###
(none)
