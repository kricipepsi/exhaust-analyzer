# T-AUD-23d — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23a/23b/23c, 310 live
threshold roots stay unverified (DIAGNOSTIC_THRESHOLD/TYPICAL_RANGE/LEGAL_LIMIT, no `same_as`, no verdict, not in v1
files). This slice takes the v2 rule files of the four most frequent verdict families. Survey by Cowork. Lane:
Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 30 candidates, 29 after dropping CK0365** (`obd_lambda le 0.1`, `catalyst_failure.json:282`: the rule text
   says "OBD lambda is zero", a sentinel). One claim names a root in `same_as`. Listed on 5765513
   (recheck/scratch/scope_T-AUD-23d.txt).
2. **Checker: scope 23d `VERDICTS FAIL 29 error(s)`; 17/23a/23b OK (20, 25, 29).** Run.
3. **Corpus families (v7, 314): misfire 70, rich 53, lean 50, catalyst 33 = 206.** recheck/T-GASA-FEURO/promoted.json.
4. **Sources S001-S028 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **Slice by verdict weight, not by file order.** Lost: the 32 integration_shim.py literals first (mostly gates
  shared by many rules, but most are internal tie-breaks, harder to source).
- **R4's 20 % band for CONFIRMED.** SUGGESTIVE gates are weight, not decisions; a near value in the right direction
  is the source's claim. Lost: exact match only (would make nearly every trim gate PARTLY and give no signal).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 29 error(s)` (P2) |
| step 2 | RAN | the three P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23d: verify 29 MF/RM/LC/CF rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23d.md`).

### Correction history ###
(none)
