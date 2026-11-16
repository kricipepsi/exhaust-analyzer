# T-AUD-23k — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23j the v2 rule files are
verified; 122 live threshold roots remain, all in Python (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice
takes `integration_shim.py`, the largest. Survey by Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 32 roots, all in `integration_shim.py`.** Listed on e5f59fa with `roots.py`. R4's claim lists equal the
   scope file (diff empty).
2. **Live:** the literals sit in the state classifiers (lines 661-851) and `_score_rule` (851-984) of the module
   that defines `RegistryV2Router`, the default router (`grep -n "^def \|^class "`).
3. **Checker: scope 23k `VERDICTS FAIL 32 error(s)`; ten earlier scopes OK.** Run.
4. **Sources S001-S041 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **The shim before the smaller Python files.** It is the v2 router itself, so its thresholds act on every default
  verdict. Lost: delta_engine.py 16 and the long tail of 1-9-literal files.
- **Expected wall-clock 55 min** (32 claims, more kinds of fact). Lost: splitting it in two (the claims share the
  same sources).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 32 error(s)` (P2) |
| step 2 | RAN | the ten P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23k: verify 32 v2 router thresholds.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings; its note (CK0236 at :381, outside 661-984) folded into R4 (`C:/4DApp/recheck/scratch/coldread_T-AUD-23k.md`).

### Correction history ###
(none)
