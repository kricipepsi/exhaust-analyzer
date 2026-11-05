# Result

## Status
completed

## Summary
DTCLab now gets a DNA view. `_build_dtc_dna_view` in `composition.py` projects vin_dna (after overrides); `_run_dtclab(dtc_inputs, vin_dna)` passes it to `DataFusionSanitizer`. The audit VIN with P0401 loses `EGR_HISTORY`; `de_cat` reaches DTCLab.

## Files changed
- apps/wired/wired/composition.py (MODIFY)
- apps/wired/tests/test_t_aud_4d_dtc_dna_view.py (CREATE, 13 tests)
- note and this RESULT

## Commands executed
The `### Verification ###` steps 1-5; three mutant runs; pyright and `ruff --select S`.

## Validation evidence
- New file `13 passed`; wired `62 passed`.
- dtclab `590 passed`; ui `30 passed`; comlab `526 passed, 4 skipped, 2 errors`.
- Step 4: `cases 207 exceptions 1 verdicts {...}`, `tag sets 206 digest f5414b25634aae41` (equals P2; no stop).
- ruff `All checks passed!`; pyright 0 errors.
- Red run before the code: `ImportError: cannot import name '_build_dtc_dna_view'`.
- Mutants: no view `2 failed`; HORIZON_ADAPTIVE->MODERN `1 failed`; `model_year is None` removed `1 failed`.

## Criteria
1. MET: 13 passed, 62 passed; mutants fail their tests.
2. MET: 590 / 30 / 526+4 skipped+2 errors.
3. MET: digest f5414b25634aae41, 1 exception.
4. MET: ruff clean; commit bdf9b87 on fix/T-AUD-4d after a830148; porcelain lists only note and RESULT.

## Decisions the task did not specify
- Wrapped enum/model arguments in their types and aliased the DTC `AirMeteringStrategy` and `VinConfidence` (name clash with COMLab imports) to pass pyright, which rejected the rehearsal's plain strings.
- Ran `ruff --select I --fix` on composition.py once (import order after the new import block).

## Pre-existing changes preserved
None existed in the clone (porcelain was empty).

## Rollback
`git revert bdf9b87` on fix/T-AUD-4d, or `git restore` before further commits.

## Remaining risks or uncertainties
`ruff --select S` reports S101 on the new test's asserts (the usual pytest pattern). Repo-wide lab suites not run (Cowork's).

Branch: fix/T-AUD-4d
`git log --oneline a830148..HEAD`: `bdf9b87 fix(T-AUD-4d): DTCLab gets its DNA view; HIGH catalyst/EGR gates and de_cat reach it`
