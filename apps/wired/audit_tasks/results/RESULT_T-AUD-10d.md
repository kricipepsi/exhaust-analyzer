# Result

## Status
completed

## Summary
Ran `apply_fix.py`; the results pane now shows the severity banner, the skipped-lab notices, the Horizon caption and the Impacted Subsystems line. Copy lives in three new `ui_payload` helpers; a new test pins them.

## Files changed
- apps/ui/app.py (+12), apps/ui/ui_payload.py (+38), apps/ui/tests/test_t_aud_10d_result_panels.py (new)
- progress note and this RESULT

## Commands executed
`### Verification ###` steps 1-4; base failure via `git stash push apps/ui/app.py apps/ui/ui_payload.py` / `git stash pop`; `$PY -I apply_fix.py`.

## Validation evidence
- Base: ui `61 passed`, wired `106 passed`, 0 app.py references.
- After: ui `65 passed`; wired `106 passed`; new test `4 passed`; on base code `4 failed`.
- ruff: `All checks passed!`; `git diff --stat`: `2 files changed, 50 insertions(+)`.
- Probe: `rendered: {'horizon': True, 'gas skipped disclosure': True}`.

## Criteria
1. MET: steps 1-2 give the P2 counts, 4 of 4 fail on base, step 4 gives P3.
2. MET: ruff clean; one commit 1797ed4 after the spec commits; `git status --porcelain` listed only the note (the RESULT is written after).

## Decisions the task did not specify
- Committed without a `Co-Authored-By` trailer because `bash_guard` refused the first attempt.

## Pre-existing changes preserved
none (clean start).

## Rollback
`git -C repo reset` is not needed: revert commit 1797ed4 on `fix/T-AUD-10d`.

## Remaining risks or uncertainties
Probe still fails on `user_input_echo_audit` and `is_fault_detected` (T-AUD-10e), as P3 expects; I did not re-run those assertions.

Branch: fix/T-AUD-10d
```
1797ed4 feat(T-AUD-10d): results pane shows severity banner, skipped-lab notices, horizon, impacted subsystems (F-C5-7)
a1599c2 spec(T-AUD-10d): First action names both spec commits
9a53012 spec(T-AUD-10d): rename T-AUD-10b1/10b2 to 10d/10e (pack id pattern takes one letter)
953a202 spec(T-AUD-10b1): results pane severity banner, skipped-lab notices, horizon, impacted subsystems (F-C5-7); split 10b
```

## Revision 02
Status: completed

Summary: `apps/ui/tests/test_t_aud_10d_result_panels.py` is now the r02 test (`cmp` identical): exact copy for every severity, notice and horizon, and the banner, notices and horizon before `if verdict.abstained:`. New commit `2d6edba`.

Validation evidence:
- Step 1: ui `65 passed`; wired `106 passed`. Step 2: `4 passed`. Step 3: `All checks passed!`; `2 files changed, 50 insertions(+)`; status only the note and this RESULT. Step 4: `rendered: {'horizon': True, 'gas skipped disclosure': True}`.
- R4 mutant (banner moved below the abstain split): `1 failed, 3 passed`; app.py restored and `cmp` identical.

Criteria: 1 MET (steps 1, 2, 4 and the mutant, above). 2 MET (ruff clean; one new commit; status only the note and RESULT).

Decisions the task did not specify: the commit has no `Co-Authored-By` trailer, because `bash_guard` refused the command with it. The first mutant script hit a cp1252 read error and changed nothing; the rerun used utf-8.

```
fix/T-AUD-10d
2d6edba test(T-AUD-10d): exact copy for every severity, notice and horizon; pin the banner placement above the abstain split
d936f86 spec(T-AUD-10d) revision 02: exact copy and placement in the test (second review)
1797ed4 feat(T-AUD-10d): results pane shows severity banner, skipped-lab notices, horizon, impacted subsystems (F-C5-7)
a1599c2 spec(T-AUD-10d): First action names both spec commits
9a53012 spec(T-AUD-10d): rename T-AUD-10b1/10b2 to 10d/10e (pack id pattern takes one letter)
953a202 spec(T-AUD-10b1): results pane severity banner, skipped-lab notices, horizon, impacted subsystems (F-C5-7); split 10b
```
Rollback: `git revert 2d6edba` on the task branch. Remaining risks: none new.
