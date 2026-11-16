# T-AUD-23f — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-22 umbrella (operator 2026-11-13: verify every domain literal). After T-AUD-23e, 253 live threshold
roots stay unverified (filter `C:/4DApp/recheck/T-AUD-23e/roots.py`). This slice takes `ecu_fault.json` and
`no_fault.json`. Survey by Cowork. Lane: Hydrogen high (difficulty 3).

### Verified context ###
1. **Scope: 24 roots, 14 in `ecu_fault.json` and 10 in `no_fault.json`.** Listed on 860aca2 with `roots.py`. No
   sentinel among them. R4's claim lists equal the scope file (diff empty).
2. **Checker: scope 23f `VERDICTS FAIL 24 error(s)`; 17/23a/23b/23d/23e OK (20, 25, 29, 29, 28).** Run.
3. **Corpus (v7, 314, `recheck/T-AUD-24k/promoted.json`): ecu_fault expected 31, verdict 16, right 14; no_fault
   expected 18, verdict 21, right 18.** `recheck/T-AUD-23e/fam24k.py`.
4. **Sources S001-S040 exist.** `sources.csv`.

### Rulings and the tradeoff that lost ###
- **ecu_fault + no_fault before cam_timing / mechanical_wear / shim.** ecu_fault misses the most cases of any family
  left (17 of 31); no_fault's bands decide every healthy verdict. Lost: cam_timing 28 (expected 11, right 7) and
  mechanical_wear 30 (expected 4): fewer corpus cases at stake.
- **No-fault gates judged as healthy bands** (R4): too tight or too loose is CONTRADICTED. Lost: the fault-gate
  wording, which does not fit a gate whose job is to accept healthy readings.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | pre-state `VERDICTS FAIL 24 error(s)` (P2) |
| step 2 | RAN | the five P3 lines |
| step 3 | SIMULATED | no CSV edit yet: `0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23f: verify 24 EF/NF rule values.

### Cold read ###
FOCUSED, spec-cold-reader 2026-11-16: 0 findings (`C:/4DApp/recheck/scratch/coldread_T-AUD-23f.md`).

### Correction history ###
(none)
