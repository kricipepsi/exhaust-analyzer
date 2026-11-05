# Result

## Status
completed

## Summary
Frozen OBDLab runs (COLD_OPEN_LOOP_INVALID) now emit `normalized_obd_lambda = None` instead of 1.0, and `lambda_perception_delta` is computed only when the lambda is not None. The payload type is `float | None` (0.7-1.3 bounds kept for a value). The 5 P3 tests changed their expectation to None; `test_frozen_payload_has_no_lambda` is new.

## Files changed
- `labs/obdlab/obdlab/core/sensor_signal_translator.py`, `labs/obdlab/obdlab/schemas/payload.py` (R1, R2)
- `labs/obdlab/tests/conftest.py`, `tests/unit/test_sensor_signal_translator.py`, `tests/integration/test_pipeline_smoke.py`, `tests/regression/fixtures/case_03_cold_engine_frozen.json`, `tests/pid_logset/logset.json` (cases 23, 24 only) (R3)
- Note and this RESULT.

## Commands executed
`### Verification ###` steps 1-5 from `C:/4DApp/repo`; red run of the new test before the code edit; two mutant runs; `recheck/T-AUD-4f/mut/rehearse_base_vs_head.py` (a copy of Cowork's script with the 12-line cap removed and the patch inverted).

## Validation evidence
- Red: before the code edit the new test and `test_cold_engine_bucket_override` failed (`assert 1.0 is None`); 2 failed, 20 passed.
- Step 1: obdlab `391 passed, 2 skipped`.
- Step 2: wired `46 passed`, ui `30 passed`, dnalab `27 passed`.
- Step 3: comlab `526 passed, 4 skipped, 2 errors` (the known R0-2 collection errors).
- Step 4: `corpus: ... frozen 2 base frozen lambdas {None: 2} | verdict changes 0 | new exceptions 0`; `ect40: ... frozen 296 base frozen lambdas {None: 296} | verdict changes 0 | new exceptions 0`.
- Step 5: `All checks passed!`; `git status --porcelain` shows only the note and this RESULT.
- Mutant 1 (sentinel back to 1.0): `6 failed, 385 passed, 2 skipped`: the new test and the 5 P3 tests. Mutant 2 (delta guard removed): `1 failed, 390 passed`: `test_frozen_payload_has_no_lambda`. Both restored with `git restore`.
- R4, base (λ 1.0) vs head (None) on ECT 40: 296 frozen, 21 verdict changes, 0 new exceptions. Frozen verdict counts base → head: MF-001 67→70, RM-001 52→52, LC-001 41→42, CF-001 27→29, SF-001 26→23, LC-002 21→23, equal to P2. The 21 changes, each caused by λ 1.0 → None:
  era2_016 NF-001→LC-002; era3_009 NF-001→LC-002; era3_018 CF-001→SF-001; CASE-009 NF-001→EF-004; CASE-010 SF-001→LC-001; CASE-032 NF-001→EF-004; CASE-045 SF-001→MF-001; CASE-048 SF-002→MF-001; CSV-001 NF-001→EF-004; CSV-005 NF-001→EF-004; CSV-045 EF-003→CF-001; EXP-N004 EF-001→MF-001; EXP-N017 SF-001→SF-002; EXP-N018 SF-001→CF-001; EXT-220 NF-001→EF-004; EXT-231 NF-001→EF-004; YAML-CSV1 NF-001→EF-004; YAML-CSV45 EF-003→CF-001; YAML-CSV5 NF-001→EF-004; case_021 NF-001→EF-004; case_028 NF-001→EF-004.
  Full output: `C:/4DApp/recheck/T-AUD-4f/mut/base_vs_head.out`. No change other than P2's.

## Criteria
1. MET: step 1 `391 passed, 2 skipped`; mutants fail named tests (above).
2. MET: step 2 equals P4.
3. MET: step 4 prints 296 frozen, base lambdas all None, `verdict changes 0`; the 21 changes are listed above (from the inverted run, since `rehearse.out` shows only 12).
4. MET: ruff passes; commit on `fix/T-AUD-4f` after the spec commit; `git status --porcelain` lists only the note and this RESULT.

## Decisions the task did not specify
- `normalized_obd_lambda` has no default (required, nullable).
- `tests/pid_logset/test_pid_logset_wiring_gate.py` (not in Files to touch) was left unchanged; see Remaining risks.
- The R4 list came from an inverted copy of Cowork's script, since the original caps its list at 12 and now runs as a no-op.
- The commit has no attribution trailer: bash_guard refused it.

## Pre-existing changes preserved
none in `repo/` (clean at start).

## Rollback
`git revert` of the fix commit on `fix/T-AUD-4f`, or discard the branch.

## Remaining risks or uncertainties
`test_coverage_matrix_and_aggregate_rate` in `tests/pid_logset/test_pid_logset_wiring_gate.py` compares each logset lambda with floats; with None in the set it passes only because `any()` stops before None in the current set order. Float and None hashes are fixed in 3.14, so the order is stable, but a new logset case could expose a TypeError. Suggest a follow-up row to filter None there. pyright: NOT RUN (not required).

Branch: `fix/T-AUD-4f`
Log (`<base>..HEAD`, base `5f64322`): see the block below.

```
fix/T-AUD-4f
2f6a387 fix(T-AUD-4f): frozen OBDLab emits no lambda instead of a made-up 1.0
```
