# T-VINA-7a — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C6_20261017.md` F-C6-14, F-C6-9; `audit/scratch/C6/test_c6_probes.py`. Rehearsal:
`C:/4DApp/recheck/T-VINA-7a/`.

### Verified context ###
1. **All four T-VINA-7 findings are open** on `0552976`: C6 probes `-k "f7_ or f9_ or f10_ or f14_"` → `6 failed,
   2 passed`. Observed.
2. **F-C6-14:** `lookup_engine_ref` opens one or two connections with `with sqlite3.connect(...)`, which commits but
   does not close; `_build_normalised_index` already closes in `finally`; `open_vref_readonly` has no caller
   (`grep -rn open_vref_readonly` → the definition and `__all__` only). Observed.
3. **F-C6-9:** `_compute_confidence` gives NONE only for `engine_not_in_csv`; T-VIN-FIX-1 ruled `wmi_brand_missing`
   "at most PARTIAL" and `test_decoder.py` pins it (`115ZZZZZZAZZZZZZZ`). The vocabulary row and HLD line say
   PARTIAL; `vds_engine_ambiguous` is already in the vocabulary. Observed.
4. **Rehearsal** (restored): vinlab `389 → 393 passed, 8 skipped`; step 2 `61 passed, 2 skipped`, base `4 failed`;
   mutant (second connect unclosed) `1 failed`; wired `113`, ui `70`, dnalab `27`, comlab `508 passed, 4 skipped`
   (equal); ruff clean; probes `3 passed`; source+docs `4 files changed, 10 insertions(+), 7 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Split T-VINA-7 into 7a (F-C6-14 + F-C6-9, mechanical), 7b (F-C6-7, the checksum market rule) and 7c (F-C6-10,
  Path B).** Lost: one d3 row with a plan gate (7b needs its own market ruling and data survey).
- **`closing()` per lookup.** Lost: one connection reused as the old docstring claimed (a long-lived handle in a
  Streamlit process; per-lookup cost is small and the index is cached).
- **Blank brand → NONE**, replacing T-VIN-FIX-1's "at most PARTIAL". Lost: the PARTIAL that let a blank brand be
  "spotted" (the flags are not serialised, so the grade cannot show which flag fired; NONE is the honest grade with no
  engine).
- Plan NONE, difficulty 2. Code row: second-model review at acceptance.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `393 passed, 8 skipped`; `113 passed`; `70 passed` |
| step 2 | SIMULATED | `61 passed, 2 skipped`; base `4 failed, 57 passed, 2 skipped` |
| step 3 | SIMULATED | `3 passed, 48 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; `4 files changed, 10 insertions(+), 7 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-7a: vref.db lookups close their connections (F-C6-14); a blank-brand WMI grades NONE (F-C6-9).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1, 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R4 · cold read: not triggered (d2, scripted) · no finding.

### Correction history ###
(none)
