# Result

## Status
completed

## Summary
`ui_payload._csv_primary_symptom` now tags the UI tier pair with a symptom-prior key (`running_rough`, `non_starter`, `hard_start_cold`). `composition._symptom_without_vin` keeps the resolved triage when the VIN does not decode, so routing applies to an empty VIN.

## Files changed
`apps/ui/ui_payload.py`, `apps/wired/wired/composition.py`, `apps/ui/tests/test_t_aud_4j_symptom_tag.py` (new), `apps/wired/tests/test_t_aud_4j_symptom_without_vin.py` (new), the note and this RESULT.

## Commands executed
The `### Verification ###` block steps 1-5 verbatim; the two mutant runs (see the note).

## Validation evidence
- Step 1: `4 passed`; `3 passed`; ui `38 passed`; wired `65 passed` (P3).
- Step 2: comlab `526 passed, 4 skipped, 2 errors` (P4).
- Step 4: `[base] changed 17`, `[fixed] changed 0`; `cases 64; fixed tag equals corpus tag in 62`; probe `test_f5_symptom_dropped_without_vin` `1 passed, 18 deselected`; census `{'cases': 314, 'undecoded': 8}`, `changes {} of 314`.
- Step 5: `All checks passed!`.
- R5: P2's base-to-fixed change is 17 of 64 verdicts to 0; no other change.
- Mutants: `symptom_dna = {}` restored fails `test_routing_applies_without_a_decodable_vin`; the rough-idle tag back to `blue_smoke_on_cold_start_clears` fails `test_tier_pair_tag[…Rough Idle…running_rough]` (and `test_every_ui_tag_is_a_prior_key`).
- Repo-wide gates (dtclab, obdlab, gaslab, symptomlab, vinlab, dnalab): NOT RUN (Cowork runs them at review).

## Criteria
1. MET: step 1 counts equal P3; both mutants fail their named tests.
2. MET: comlab equals P4.
3. MET: `[fixed] changed 0`; probe passes; `changes {} of 314`.
4. MET: ruff clean; commit `6470496` on `fix/T-AUD-4j` after the spec commit; `git status --porcelain` lists only the note and the RESULT.

## Decisions the task did not specify
- The `# consumer:` comment in `_csv_primary_symptom` names "COMLab symptom prior (labs/comlab/comlab/config/symptom_prior.yaml mappings)".
- `test_every_ui_tag_is_a_prior_key` collects the tags the three test cases produce and checks they are keys of the prior's `mappings`.

## Pre-existing changes preserved
None existed (`git status --porcelain` was empty at start).

## Rollback
`git revert 6470496` on `fix/T-AUD-4j`, or `git restore` before any push.

## Remaining risks or uncertainties
The corpus tag differs from the fixed tag in 2 of 64 cases (stalls and `lean_no_start`; no prior key). Out of scope per the task.

Branch: `fix/T-AUD-4j`
```
6470496 fix(T-AUD-4j): UI symptom tag is a prior key; triage survives an undecodable VIN
8b12cd9 spec(T-AUD-4j): UI symptom tag is a prior key; triage survives an undecodable VIN
```
