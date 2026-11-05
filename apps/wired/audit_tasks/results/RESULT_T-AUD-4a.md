# Result

## Status
completed

## Summary
`_PID_DISPATCH["o2_downstream"]` now reads `obd_live_data.downstream_o2_v` with no freeze-frame fallback. Three tests added.

## Files changed
- labs/comlab/registry/integration_shim.py (one entry + comment)
- labs/comlab/registry/tests/test_integration_shim.py (import + 3 tests)
- progress note and this RESULT

## Commands executed
`### Verification ###` steps 1-5 from C:/4DApp/repo; red gate run before the edit; two mutant runs.

## Validation evidence
- Red gate before edit: `2 failed, 28 passed` (the two NEW tests).
- Step 1: `30 passed`. Step 2: `87 passed`.
- Step 3: comlab `526 passed, 4 skipped, 2 errors`; wired `41 passed`; ui `30 passed`.
- Step 4 (head -5):
  - cases 314 route reached (base) 311 exceptions Counter({'EXC:PIDValidationError': 2, 'EXC:DTCFormatError': 1})
  - base o2_downstream resolved non-None 11 | live downstream_o2_v non-None 11 | equal to B1S1 0
  - after o2_downstream non-None 11
  - resolved value changes 0 | SF-006/EL-002 score changes 0 | verdict changes 0
  The script's "base" already reads the new dispatch, as the spec states. P4's before figures (0 non-None; CASE-022 `{SF-006: 0.65}` -> `{EL-002: 0.8, SF-006: 0.7}`) come from Cowork's recorded rehearse.out, not from a run of mine. No case changes beyond P4's.
- Mutants: base entry -> test_o2_downstream_reads_measured_downstream and test_o2_downstream_absent_without_live_reading fail (2 failed, 28 passed); obd+ff fallback -> test_o2_downstream_absent_without_live_reading fails (1 failed, 29 passed).
- Step 5: ruff `All checks passed!`.

## Criteria
1. MET: 30 passed; both mutants fail named tests.
2. MET: 87 passed; step 3 equals P3.
3. MET: step 4 prints non-None 11 after, 0 changes against the new base.
4. MET: ruff clean; commit on fix/T-AUD-4a; `git status --porcelain` shows the note and RESULT only.

## Decisions the task did not specify
- Tests use `_resolve_pid_from_payload` (spec allows it or `_build_observation`); imported at the top of the test file.
- The commit message carries no attribution trailer: bash_guard refused any command containing the trailer text.

## Pre-existing changes preserved
None in repo/. C:/4DApp loop-pack changes (LOOP_STATE.md etc.) untouched.

## Rollback
`git -C repo revert 1d8aa51` on fix/T-AUD-4a, or reset the branch to 12f853a.

## Remaining risks or uncertainties
None found. Repo-wide gates for other labs were not run (Cowork runs them at review): NOT RUN.

Branch: fix/T-AUD-4a
```
1d8aa51 fix(T-AUD-4a): registry o2_downstream reads measured downstream_o2_v
12f853a spec(T-AUD-4a): registry o2_downstream reads the measured downstream channel
1afdecc ledger(wired): T-AUD-4 split into 4a-4e (deferred rows); T-AUD-1d folds into 4b
```
