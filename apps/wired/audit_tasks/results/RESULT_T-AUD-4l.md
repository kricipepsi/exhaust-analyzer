# Result

## Status
completed

## Summary
`OrchestratorInboundRequest` gains `vehicle_dna: VehicleDNA | None` and a before-validator `_metadata_from_vehicle_dna`
that derives `metadata`, refuses both shapes ("not both"), and carries `symptom_dna` and `has_catalyst`. The F-D2-2 probe passes.

## Files changed
- `labs/comlab/comlab/schemas/ingestion.py` (+33)
- `labs/comlab/tests/unit/test_t_aud_4l_inbound_vehicle_dna.py` (new, 4 tests)

## Commands executed
`### Verification ###` steps 1-5 from `C:/4DApp/repo` in Git Bash; three mutant runs; probe on base.

## Validation evidence
- new file: `4 passed` (before the fix: `4 failed`)
- comlab: `530 passed, 4 skipped, 2 errors` (P3)
- registry/tests minus render: `5 failed, 502 passed, 4 deselected` (P4)
- wired `65 passed`; ui `38 passed`
- probe: `1 passed, 13 deselected` (base `1 failed, 13 deselected`)
- ruff: `All checks passed!`
- mutants: validator skipped `4 failed`; both-shapes check removed fails `test_both_shapes_are_refused`; `has_catalyst` carry removed fails `test_symptom_and_catalyst_come_from_vehicle_dna`
- Repo-wide gates (dtclab etc.): NOT RUN (report-only; Cowork runs them at review)

## Criteria
1. MET: new file and comlab equal P3; each mutant fails its named tests.
2. MET: registry, wired, ui equal P4.
3. MET: probe passes.
4. MET: ruff clean; one commit after the spec commit on `fix/T-AUD-4l`; `git status --porcelain` lists only the note and the RESULT.

## Decisions the task did not specify
- Converted the test file from CRLF to LF to match the repo's `eol=lf`.
- Commit has no attribution trailer, because bash_guard refuses it in the commit command.

## Pre-existing changes preserved
none in `repo/`; `C:/4DApp` working-tree changes untouched.

## Rollback
`git -C repo reset` is not used; revert commit c2292c9 on `fix/T-AUD-4l`.

## Remaining risks or uncertainties
`gas_lab_output` stays required (out of scope, T-AUD-4e).

Branch: fix/T-AUD-4l
Log (`25f5988..HEAD`): c2292c9 fix(T-AUD-4l): COMLab accepts vehicle_dna at the top level and derives metadata (F-D2-2)

## Revision 02 (R5)
Added test_non_default_schema_and_confidence_are_derived; new file 5 passed, comlab 531 passed, 4 skipped, 2 errors, ruff clean. Only the test file changed.

Every failing test of every mutant:
- validator skipped (4 failed): test_vehicle_dna_shape_derives_metadata, test_both_shapes_are_refused, test_symptom_and_catalyst_come_from_vehicle_dna, test_top_level_values_win
- both-shapes check removed (1 failed): test_both_shapes_are_refused
- has_catalyst carry removed (1 failed): test_symptom_and_catalyst_come_from_vehicle_dna
- schema_version/vin_confidence lines deleted (1 failed): test_non_default_schema_and_confidence_are_derived

Log (25f5988..HEAD, includes spec commit ea0be68): see branch lines below.
214818a test(T-AUD-4l): non-default schema_version and confidence are derived (R5)
ea0be68 spec(T-AUD-4l): revision 02 — non-default derivation test (review nit upheld)
c2292c9 fix(T-AUD-4l): COMLab accepts vehicle_dna at the top level and derives metadata (F-D2-2)
