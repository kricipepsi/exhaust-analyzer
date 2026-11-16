# T-AUD-23h — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23g, 201 live threshold
roots stay unverified (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice takes `mechanical_wear.json`. Survey by
Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 30 roots, all in `mechanical_wear.json`.** Listed on a4bca05 with `roots.py`. No sentinel. R4's claim lists
   equal the scope file (diff empty); the R4 values match `claims_comlab.csv` (spot check by sight).
2. **Checker: scope 23h `VERDICTS FAIL 30 error(s)`; seven earlier scopes OK.** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24k/promoted.json`; rule data unchanged since 24k): mechanical_wear expected 4,
   verdict 0, right 0.** `recheck/T-AUD-23e/fam24k.py`.
4. **Sources S001-S041 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **mechanical_wear before non_starter / shim.** It is the largest rule file left; the family never fires in the
  corpus (0 of 4). Lost: non_starter 25 (expected 6, right 5), integration_shim 32 (liveness not measured).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 30 error(s)` (P2) |
| step 2 | RAN | the seven P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23h: verify 30 MW rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23h.md`).

### Correction history ###
(none)
