# Result

## Status
completed

## Summary
A will_not_start session with no gas reading is now diagnosed by the T-COMA-1 family gate: the schema accepts no `gas_lab_output` for a non-starter only (R1), the aggregator runs with both lambda detectors inert (R2), and the composition skips GASLab (R3). Partial gas and a running engine still abort. R4-R6 done.

## Files changed
ingestion.py, lab_pipeline_aggregator.py, composition.py, ui_payload.py, test_t_aud_1a_inputs.py, test_t_aud_1c.py, new test_t_coma_2_non_starter_without_gas.py (commit d405b26); the note and this RESULT.

## Commands executed
The `### Verification ###` block, the base red run of the new file, and 3 mutant runs (each reverted with `git restore`).

## Validation evidence
- New file: base `5 failed, 1 passed`; fix `6 passed`. Mutants: M1 `2 failed, 4 passed`, M2 `1 failed, 5 passed`, M3 `3 failed, 3 passed` (test names in the note).
- comlab `531 passed, 4 skipped, 2 errors`; registry `5 failed, 502 passed, 4 deselected`; wired `85 passed`; ui `38 passed`.
- Probe: 9 P2 lines match (plus extra ns_* lines); `corpus 314`; `corpus equal: True`. ruff `All checks passed!`.

## Criteria
1. MET: new file, comlab, mutants as P3/P4.
2. MET: registry, wired, ui equal P4.
3. MET: P2 lines, P5 `corpus equal: True`.
4. MET: ruff clean; one commit on fix/T-COMA-2 after the spec commit; `git status --porcelain` lists only the note and this RESULT (before the RESULT existed: the note).

## Decisions the task did not specify
- Applied `rehearsal.patch` with `git apply` and copied the rehearsed test file unchanged.
- M3 mutant: reverted the perception-detector guard only (`if False`), which reproduces the base call on `None`.
- Commit has no trailer: `bash_guard` refuses the command text that carries one.

## Pre-existing changes preserved
none (clean tree at start).

## Rollback
`git -C repo reset` is barred on main only; on the task branch, `git revert d405b26`.

## Remaining risks or uncertainties
Repo-wide lab gates (dtclab, obdlab, ...) NOT RUN: report-only, Cowork runs them. The probe prints more than 9 lines (extra ns_* probes), all consistent with the fix.

Branch: fix/T-COMA-2
Log (`8931b9a..HEAD`): d405b26 feat(T-COMA-2): diagnose a non-starter without exhaust gas readings
