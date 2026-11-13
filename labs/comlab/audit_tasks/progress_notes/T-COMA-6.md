# T-COMA-6 progress note

## Readiness challenge
(a) Starting state matches: branch `fix/T-COMA-6`, one commit `8f1690b` after `49214a9`, `git status --porcelain` empty; all 10 precondition files exist. Base counts equal P1 (comlab `510 passed, 4 skipped`; wired `127 passed`; ui `70 passed`; probes `3 failed, 13 deselected`, first verdict `LC-002 ... True WARNING_DEGRADED_PERFORMANCE`).
(b) The new test fails on the base code for the intended reason: `9 failed, 4 passed`, the pinned base count (command: step 2 before R1).
(c) Expected decisive value: P3 `verdict: OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH` and `changed 0 of 314`; the test pin is `13 passed`; derived from the task's P2/P3, not from the code.
(d) No contradiction prevents work. One soft defect, below.
(e) Deliverable: on NORMAL_OPERATION gas a rule fires only with strict support (R1), and a no-fire verdict abstains `no_rule` (R2), with the two old pins updated (R3), applied by `rehearse.py` plus the copied test. The decisive check is the 13-test file going `9 failed` to `13 passed` while the probes go `3 failed` to `3 passed` and the v7 corpus changes 0 of 314.

## Assumptions worked past
- Soft defect: Verification step 1 runs `git checkout -- labs/comlab/registry/case_library.html`. That path does not exist (`ls` says no such file). The tracked file is `labs/comlab/registry/docs/case_library.html` (AGENTS.md names it). I restore that path. Reviewer can detect this from the note; no data loss.

## Time
phase | start | end | minutes | context at end
baseline+red gate | 2026-11-13T10:32:43Z | 2026-11-13T10:33:35Z | 1 | ABSENT
edit+gates+R5+commit | 2026-11-13T10:33:35Z | 2026-11-13T10:35:38Z | 2 | ABSENT

## R5 results
Base shim (stash): `9 failed, 4 passed`. Mutant A: `1 failed, 12 passed`. Mutant B: `2 failed, 11 passed`.
Restored by copying a saved good copy over the shim (`cmp` identical; `git diff --stat` back to `4 files changed, 44 insertions(+), 4 deletions(-)` before the commit).

## VERIFICATION GATE
1. comlab `510 passed, 4 skipped`; wired `140 passed`; ui `70 passed`.
2. New test `13 passed`.
3. `verdict: OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH`; `3 passed, 13 deselected`.
4. `changed 0 of 314`.
5. ruff `All checks passed!`; `5 files changed, 114 insertions(+), 4 deletions(-)`; spec commit plus `9e0df5d`; status lists only the note (RESULT written after).

## CODE REVIEW
Diff read: R1 helper, two call sites and the constant; R2 elif; R3 two pins; new test copied (`cmp` ok). Every line traces to Files to touch. Anti-orphan: `_strict_support` and `_GATING_KEY_WEAK_SUPPORT` are read in the shim. No out-of-scope edit.

## Decision on the commit
`bash_guard` refused every commit command whose text held the attribution trailer, so the commit has no trailer.

## Correction 1
Readiness (correction): (a) branch `fix/T-COMA-6`, HEAD `118f675`, status listed only the note and RESULT; all 12 preconditions exist. (b) R7 red gate: with the `_c1` test copied (`cmp` ok) and before `correct1.py`, step 2 gave `3 failed, 13 passed`. (c) Expected after: `16 passed`, wired `143 passed`, `changed 0 of 314`, diff stat `2 files changed, 26 insertions(+), 6 deletions(-)` (P2). (d) No contradiction. (e) A NORMAL chemistry row stays a row but is never support or the chemistry anchor (R6, `correct1.py` plus the copied test); decisive check: `3 failed, 13 passed` becomes `16 passed`.

R6 applied with `correct1.py` (`applied`). Commit `c086c3e` has no Co-Authored-By trailer: `bash_guard` refused the commit text that held it (the same as in `9e0df5d`).

### VERIFICATION GATE (correction 1)
1. comlab `510 passed, 4 skipped`; wired `143 passed`; ui `70 passed`.
2. New test `16 passed`.
3. `verdict: OPTIMAL_HEALTH no_fault 0.0 False OPTIMAL_HEALTH`; `3 passed, 13 deselected`.
4. `changed 0 of 314`.
5. ruff `All checks passed!`; `2 files changed, 26 insertions(+), 6 deletions(-)`; status lists only the note and RESULT.

### CODE REVIEW (correction 1)
Diff read: `rows` keeps each chemistry row and sets it unsatisfied when its state is NORMAL; `chem_gate` excludes a NORMAL row. Test copied (`cmp` ok). Both files are in Files to touch. No out-of-scope edit.

### Time (correction 1)
phase | start | end | minutes | context at end
correction 1 | 2026-11-13T10:44:30Z | 2026-11-13T10:45:54Z | 1 | ABSENT
