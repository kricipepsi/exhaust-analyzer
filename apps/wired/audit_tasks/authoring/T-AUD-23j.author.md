# T-AUD-23j — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-24o, 146 live threshold
roots stay unverified (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice takes five small rule files (vacuum_leak, overheating, ignition_fault, exhaust_leak, invalid_input; catalyst_failure held only the sentinel). Survey by
Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 24 roots in five files.** Listed on fa5bb38 with `roots.py`; CK0365 (catalyst_failure, a zero-reading sentinel) dropped as in T-AUD-23d. R4's claim lists
   equal the scope file (diff empty).
2. **Checker: scope 23j `VERDICTS FAIL 24 error(s)`; nine earlier scopes OK.** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24k/promoted.json`; the 24o tip gives the identical file): invalid_input expected 20, verdict 6, right 6; exhaust_leak 10/9/7; ignition_fault 4/2/2.
   vacuum_leak, overheating: no expected cases.** `recheck/T-AUD-23e/fam24k.py`.
4. **Sources S001-S041 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **The small rule files together, before the Python literals.** They finish the v2 rule files. Lost: integration_shim
  32 (liveness not measured).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 24 error(s)` (P2) |
| step 2 | RAN | the nine P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23j: verify 24 small-file rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 1 finding (DIRECT, minor: Routing said six files, the scope has five), fixed before commit (`C:/4DApp/recheck/scratch/coldread_T-AUD-23j.md`).

### Correction history ###
(none)
