# T-AUD-23i — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23h, 171 live threshold
roots stay unverified (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice takes `non_starter.json`. Survey by
Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 25 roots, all in `non_starter.json`.** Listed on be68dfc with `roots.py`. No sentinel. R4's claim lists
   equal the scope file (diff empty).
2. **Checker: scope 23i `VERDICTS FAIL 25 error(s)`; eight earlier scopes OK.** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24k/promoted.json`; rule data unchanged since 24k): non_starter expected 6,
   verdict 5, right 5.** `recheck/T-AUD-23e/fam24k.py`.
4. **Sources S001-S041 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **non_starter before the shim and the small rule files.** It is the last large v2 rule file. Lost: integration_shim
  32 (liveness not measured) and the five small rule files together (25 roots, 2-10 corpus cases each).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 25 error(s)` (P2) |
| step 2 | RAN | the eight P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23i: verify 25 NS rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23i.md`).

### Correction history ###
(none)
