# T-AUD-24d — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23b verdicts CK1359, CK1376, CK1378 CONTRADICTED; CK1371, CK1374 PARTLY (Bosch NTC table S015, MAF
~1 g/s/L S019/S020). Survey by Cowork (difficulty 2: no cold read; second review kept). Lane: Hydrogen medium.

### Verified context ###
1. **The five strings are user-facing (KG ui_remediation_steps / mechanical_failure_mode; registry
   ui_diagnostic_string) and appear nowhere else in labs/ or apps/ outside notes** (grep). Observed on b920f2d.
2. **mechanical_failure_mode max_length=280 (schemas/kg.py:55)**: a first, longer item-3 text made 195 comlab tests
   fail (string_too_long); the R1 text is 2 characters shorter than the old. Observed.
3. **With R1 applied (recheck/T-AUD-24d_rehearsal.patch): comlab 609, registry 510/5, wired 189, ui 76 — equal.**
   Observed and restored.
4. **The heredoc halves a typed backslash: the OLD-1 match needs the JSON escape `\u2013` as bytes.** Observed
   (MEMORY hazard); R1/R2 say so.

### Rulings and the tradeoff that lost ###
- **Exact text replacement, not JSON re-serialisation**: keeps escapes and diffs minimal. Lost: json.dump (rewrites
  every escape in two large files).
- **CK1368 (> 80 °C) left**: PARTLY, defensible against OEM 75 °C. Lost: changing a defensible value.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `609 passed` |
| step 2 | SIMULATED | patch applied: `510 passed, 5 skipped` |
| step 3 | SIMULATED | patch applied: `189 passed` |
| step 4 | SIMULATED | patch applied: `76 passed` |
| step 5 | SIMULATED | pre `TEXT FAIL [5 old] [5 new]`; patched `TEXT OK [] []` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24d: ECT NTC table, ECT cold-bias physics and idle MAF guidance corrected (5 strings).

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
