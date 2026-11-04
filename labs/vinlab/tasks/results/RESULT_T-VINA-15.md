# Result

## Status
completed

## Summary
In `_derive_air_metering`, a stored has_maf=0 with has_map=0 now becomes unknown (None/None), so the decoder heuristic runs as for a NULL row. Added 9 tests.

## Files changed
- labs/vinlab/vinlab/decoder.py (+5)
- labs/vinlab/tests/unit/test_sensor_unknown.py (new)
- labs/vinlab/tasks/progress_notes/T-VINA-15.md, labs/vinlab/tasks/results/RESULT_T-VINA-15.md (new)

## Commands executed
Task First action, Preconditions, Verification steps 1-6, and the three mutant runs (see the note).

## Validation evidence
- vinlab 353 passed, 8 skipped; test_sensor_unknown 9 passed; dnalab 27, wired 41, ui 30 passed; probes 14 passed, 37 deselected.
- effect.py: decoded 1131, changed 13 {('MAP_ONLY_SPEED_DENSITY', 'DUAL_MAF_MAP_CROSSCHECK'): 13}. ruff: All checks passed.
- Before R1 the new tests gave 3 failed. M1 3 failed, M2 3 failed, M3 1 failed.

## Criteria
1. MET: steps 1, 2 and mutants M1-M3 as R3.
2. MET: step 3 (27/41/30) and step 4 (14 passed).
3. MET: step 5, 13 VINs, all to DUAL_MAF_MAP_CROSSCHECK.
4. MET: ruff clean; one commit after the spec commit; `git status --porcelain` lists only the note and the RESULT.

## Decisions the task did not specify
- Committed without the co-author trailer: the shell guard refused the command text that carried it.

## Pre-existing changes preserved
None present (clean tree at start).

## Rollback
`git revert 32d3d1c` on fix/T-VINA-15, or `git restore` both paths before any push.

## Remaining risks or uncertainties
The 68 rows still store 0/0 in vref.db (out of scope, R4); the fix is decoder-side only.

## Branch and log
fix/T-VINA-15

32d3d1c fix(T-VINA-15): treat a stored 0/0 air-sensor row as unknown
51566ca vina: T-VINA-15 spec (decoder reads a stored 0/0 air-sensor pair as unknown)

## Round 2
Status: completed. Correction 01 (R5) applied on top of round 1; commit 18b60a1.
- Summary: the 0/0 rule now skips CARBURETOR; the real-VIN test asserts (True, True) and DUAL_MAF_MAP_CROSSCHECK; new test_carburettor_zero_zero_is_kept.
- Validation: vinlab 354 passed, 8 skipped; test_sensor_unknown 10 passed; dnalab 27, wired 41, ui 30; probes 14 passed, 37 deselected; effect.py vs 51566ca changed 13, vs round 1 changed 0; ruff clean.
- Mutants: M4 2 failed; M5 1 failed (M1-M3 from round 1 unchanged).
- Criteria 1-4: MET (same commands; step 5 now archives 51566ca; P3 counts matched).
- Decisions not specified: none. Commit again without a co-author trailer (shell guard).
- Rollback: git revert 18b60a1.
- Branch: fix/T-VINA-15

18b60a1 fix(T-VINA-15): scope the 0/0 rule to injected engines, assert exact strategy
511ffbd vina: T-VINA-15 correction 01 (carburettor scope, exact strategy assert)
32d3d1c fix(T-VINA-15): treat a stored 0/0 air-sensor row as unknown
51566ca vina: T-VINA-15 spec (decoder reads a stored 0/0 air-sensor pair as unknown)
