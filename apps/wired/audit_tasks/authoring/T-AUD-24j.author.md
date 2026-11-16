# T-AUD-24j — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23d CONTRADICTED 14; Cowork ruling `reviews/RULING_T-AUD-24j.md` (3 to fix, 11 not). Survey and corpus
by Cowork (difficulty 2: no cold read; second review kept, code row). Lane: Hydrogen medium.

### Verified context ###
1. **Corpus (v7, 314) with R1-R2: 10 changed, all LC-002 → LC-001; family 221 → 221; code 117 → 126.** R2 alone: 0.
   Measured on 1c64e43 (recheck/T-AUD-24j/).
2. **Suites with R1-R4: comlab 610 → 611, registry 510/5, gaslab 280.** Without R4 the comlab suite fails 1
   (`test_lc002_fires_on_lean_chemistry_at_its_old_score`). Rehearsed and restored (rehearsal.diff).
3. **R4 test on base rule data: 2 failed.** Run.
4. **Step 3 base `24j FAIL (('lt', 40.0), 100.0, 200.0)`; patched `24j OK`.** Run.

### Rulings and the tradeoff that lost ###
- **`gt 50`, not `gt 40`.** Same corpus result; 50 is the top of the healthy idle band (S036). Lost: `gt 40` (VL-001's
  value, inside the healthy band).
- **HC 50.** S034's late-model `< 50 ppm`; S023's 35 is tighter. Lost: 35 (one TRADE chart; 0 change either way).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `611 passed` |
| step 2 | SIMULATED | patch applied: `510 passed, 5 skipped` |
| step 3 | SIMULATED | pre `24j FAIL`; patched `24j OK (('gt', 50.0), 50.0, 50.0)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24j: LC-002 MAP gt 50; CF-002/MF-004 HC < 50; code accuracy +9.

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
