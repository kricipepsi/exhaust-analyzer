# Result

## Status
completed

## Summary
A PARTIAL or NONE decode now puts the form in basic mode (R1, `apps/ui/app.py`). Basic mode sends `overrides.upstream_o2_type = NARROWBAND` when the form used the volts field (R2, `apps/ui/ui_payload.py`). Four tests added (R3).

## Files changed
- `repo/apps/ui/app.py`, `repo/apps/ui/ui_payload.py` (rehearsal.patch applied unchanged)
- `repo/apps/ui/tests/test_t_aud_4o_partial_decode_basic_mode.py` (new, copy of the rehearsed file)
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-4o.md`, this RESULT

## Commands executed
The `### Verification ###` steps 1-4 as written; the two mutant runs; `git apply` of the patch; one commit.

## Validation evidence
New file `4 passed`; ui `49 passed`; wired `85 passed`; f9_wideband.py: `Upstream O₂ (V)` (0-1) and EF-004 FULL_FUSION both ways; ruff `All checks passed!`. M1 `1 failed, 3 passed` (test_partial_decode_is_basic_mode). M2 `2 failed, 2 passed` (test_basic_mode_pins_narrowband, test_partial_wideband_vin_runs_in_basic_mode).

## Criteria
1 MET (new file 4 passed, ui 49 passed, mutants as named). 2 MET (wired 85 passed). 3 MET (f9_wideband.py output). 4 MET (ruff clean; commit 3f7589e after spec 54eace8; status lists only the note and this RESULT).

## Decisions the task did not specify
none. One note: the red gate on the base was run on the rehearsed file from `recheck/` before copying: `3 failed, 1 passed`. The AppTest failure there was a path error (file outside `apps/ui/tests`), so it is not a clean base check for that one test. M1 covers that test failing for the intended reason.

## Pre-existing changes preserved
The tree was clean at start.

## Rollback
`git -C repo revert 3f7589e` on `fix/T-AUD-4o`, or `git restore` before any push.

## Remaining risks or uncertainties
pyright was NOT RUN. Repo-wide gates are left to Cowork.

Branch: fix/T-AUD-4o
```
3f7589e fix(T-AUD-4o): a PARTIAL decode is basic mode; basic mode pins the NARROWBAND O2 type (F-C5-9)
54eace8 spec(T-AUD-4o): a PARTIAL decode is basic mode; basic mode pins the O2 type (F-C5-9)
```
