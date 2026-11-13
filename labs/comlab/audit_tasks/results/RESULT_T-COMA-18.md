# Result

## Status
completed

## Summary
RM-004 (`gdi_equipped: true`) is pruned as `hardware_gate` unless the VIN decode says GDI, the era is MODERN, or no era is sent. `fuel_delivery_type` now flows wired -> `SessionMetadata` -> aggregator metadata -> shim.

## Files changed
integration_shim.py, ingestion.py, lab_pipeline_aggregator.py, wired/composition.py, apps/wired/tests/test_t_coma_18_gdi_hardware_gate.py (new), the note and this RESULT.

## Commands executed
`git apply rehearsal.patch`; `cp` + `cmp` of the test; R4 base and four mutant runs; Verification steps 1-5 as written; commits 2a3ccd1 and a556cb6 (correction 1: R5, R6).

## Validation evidence
comlab `517 passed, 4 skipped`; wired `186 passed`; ui `73 passed`; tunable_reweight `2 passed`; new test `10 passed` (base `5 failed, 4 passed` before R5; mutants A `3 failed, 6 passed`, B/C/D `1 failed, 8 passed`, E `1 failed, 9 passed`); C1 probes `LEGACY rich -> ['RM-001', ('LC-002'` and `3 passed, 7 deselected`; corpus `changed 0 of 314`; ruff `All checks passed!`; diff stat `5 files changed, 121 insertions(+)`.

## Criteria
1. MET: steps 1-4 and R4 counts as pinned.
2. MET: ruff clean, 121 insertions, one new commit a556cb6 after the correction spec commit 15cc332; R6 gives `1 failed, 9 passed`; porcelain lists only the note (and this RESULT).

## Decisions the task did not specify
The commit has no Co-Authored-By trailer: bash_guard refused the first commit command that carried it. No other decisions.

## Pre-existing changes preserved
none (clean tree at start).

## Rollback
`git revert a556cb6 2a3ccd1` on `fix/T-COMA-18`.

## Remaining risks or uncertainties
py_compile, pyright and `ruff --select S` NOT RUN (not in the task's Verification). The other REG-V2 rules and CT-001 stay out of scope per the task.

Branch: `fix/T-COMA-18`
```
a556cb6 fix(T-COMA-18): assert RM-004 pruned in GDI tests; test the prune record (correction 1)
15cc332 coma: spec(T-COMA-18) correction 1: stronger GDI tests, prune-record test, docstring
2a3ccd1 fix(T-COMA-18): prune GDI-only RM-004 on a non-GDI, non-MODERN car (F-C1-6)
206f21b coma: spec(T-COMA-18): RM-004 needs a GDI decode or the MODERN era (F-C1-6)
```
