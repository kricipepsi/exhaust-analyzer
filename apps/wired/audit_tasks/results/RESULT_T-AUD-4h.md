# Result

## Status
completed

## Summary
`diagnose` now passes the user's DTC codes to OBDLab as `active_dtcs` (`_with_user_dtcs`, explicit non-empty wins), and the registry shim no longer scores `ff` trims (`short_term_ft1`, `long_term_ft1`) when the freeze frame's `coolant_temp_c` is below 70.0.

## Files changed
- `apps/wired/wired/composition.py` (helper + call)
- `labs/comlab/registry/integration_shim.py` (`_FF_WARM_ECT_C`, `_ff_cold`, guard)
- `labs/comlab/registry/tests/test_integration_shim.py` (+4 parametrized cases)
- `apps/wired/tests/test_t_aud_4h_active_dtcs.py` (new, 3 tests)
- note and this RESULT

## Commands executed
The `### Verification ###` steps 1-5 verbatim; the R4 mutants by in-place `sed` edits, each undone (diff stat unchanged at 62 insertions, 1 deletion afterwards).

## Validation evidence
- Red gate: before the code, the helper test file failed at collection (ImportError) and ECT 40.0 and 69.9 failed (2 failed, 2 passed).
- Step 1: `test_integration_shim.py` `44 passed`; `registry/tests` `5 failed, 502 passed, 4 deselected`, the 5 FAILED all `test_build_corpus.py`.
- Step 2: wired `49 passed`; comlab `526 passed, 4 skipped, 2 errors`; obdlab `391 passed, 2 skipped`; ui `30 passed`.
- Step 3: only the note (and RESULT) untracked; suites wrote nothing.
- Step 4: `[ff] verdict changes 0 | gate changes 0 {} | new exceptions 0`; `UI=1 [dtc] verdict changes 0 | gate changes 0 {} | new exceptions 0`. Base gates in both: `{'VALID': 289, 'O2_FAULT_ACTIVE': 3, 'ENGINE_COLD': 2, None: 2, 'CKP_CMP_FAULT_ACTIVE': 1}`, equal.
- Step 5: ruff `All checks passed!`.
- R4 mutants: `<` → `<=` fails `test_freeze_frame_trims_follow_ff_coolant[70.0-3.0]`; route skipped fails `test_user_codes_become_active_dtcs`; explicit-wins check removed fails `test_explicit_active_dtcs_win`. Each 1 failed.
- R5: the changes in P2's `rehearse.out` (`ff`: 1 verdict change, era2_012 SF-008 → SF-001, cause "cold FF trims dropped") and `rehearse_ui.out` (`dtc`: 4 gate changes, VALID → O2_FAULT_ACTIVE 3, → CKP_CMP_FAULT_ACTIVE 1, cause "user codes routed") are the effects of removing the script patches. On the fixed code the script patches are unnecessary, so the base run already contains them and the deltas print 0. No change outside P2's list appeared.

## Criteria
1. MET - step 1 counts equal P3; mutants each fail the named test.
2. MET - step 2 equals P3/P4.
3. MET - step 4 lines above, base gates equal.
4. MET - ruff clean; commit `5c29e87` on `fix/T-AUD-4h` after spec commit `dd24964`; `git status --porcelain` lists only the note and RESULT.

## Decisions the task did not specify
- Non-numeric `coolant_temp_c` is treated as absent (no gate).
- `_with_user_dtcs` accepts any `dtc_inputs` and raises TypeError for non-dict, as `_as_dict` does.
- Note and RESULT left uncommitted (criterion 4 expects them in `git status`).

## Pre-existing changes preserved
None existed in `repo/` at start (`git status --porcelain` empty).

## Rollback
`git -C repo revert 5c29e87` on the branch, or `git restore` of the four paths from `dd24964`.

## Remaining risks or uncertainties
Pyright not run (not in Verification). Repo-wide report-only gates (dtclab, gaslab, symptomlab, vinlab, dnalab) NOT RUN; Cowork runs them.

Branch: `fix/T-AUD-4h`

```
5c29e87 fix(T-AUD-4h): user DTC codes reach OBDLab; cold freeze-frame trims not scored
```
(`git log --oneline dd24964..HEAD`)
