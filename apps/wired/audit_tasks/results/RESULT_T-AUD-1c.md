# Result

## Status
completed

## Summary
R1: `validate_widgets` requires the 12 freeze-frame fields whenever `"dtc" in payload`, with the message `<label> is required when DTC data is entered.` R2: the engine gas message now reads `Low-idle gas readings are incomplete. Tick GASLab and enter: <fields>.` and the `gas_module` help says it is required for every run.

## Files changed
`apps/ui/ui_payload.py`, `apps/wired/wired/composition.py`, `apps/ui/tests/test_t_aud_1c.py` (new), the note, this RESULT.

## Commands executed
The Verification block steps 1-6 from `C:/4DApp/repo`; pyright report-only.

## Validation evidence
1. `apps/ui/tests`: `30 passed`. 2. 9 acceptance probes: `9 passed`. 3. C1 `42 failed, 2 passed`; C4 `9 failed, 3 passed`; C5 `13 failed, 6 passed` (unchanged). 4. `apps/wired`: `36 passed`. 5. ruff `All checks passed!`. Pyright `0 errors`. Red gate: `test_r1_pending_only_requires_ff` failed on the base before the edit.

## Criteria
1. MET: six tests in `test_t_aud_1c.py`.
2. MET: `30 passed`.
3. MET: P2 9 passed, P3 unchanged, P4 36 passed.
4. MET: one commit e37bf50 above `audit-r2`.

## Decisions the task did not specify
- Reworded one docstring line in `validate_widgets` to match R1.
- The commit has no attribution trailer; `bash_guard` refused the command with it.
- The PIN test's mutant was not run separately.

## Pre-existing changes preserved
none present (clean tree at start).

## Rollback
`git revert e37bf50` on `fix/T-AUD-1c`, or reset the branch to `f4f8fc1`.

## Remaining risks or uncertainties
The PIN test's mutant (FF loop without the `"dtc" in payload` test) was reasoned, not run.

Branch: `fix/T-AUD-1c`
`git log --oneline f4f8fc1..HEAD`: `e37bf50 fix(T-AUD-1c): require freeze frame whenever a DTC dict is sent; gas message names GASLab`
