# T-AUD-10d progress note

## Readiness challenge
(a) Start state matches: branch fix/T-AUD-10d, `git log b8ec171..HEAD` = 3 spec commits (a1599c2, 9a53012, 953a202), `git status --porcelain` empty. Base P1: ui `61 passed`, wired `106 passed`, 0 refs in app.py.
(b) The new test file is untracked. With the two source files stashed, it fails on the base code: 3 tests hit the missing `SEVERITY_BANNER`/`routing_notices`/`HORIZON_MEANING`, and the app.py text check misses its needles. Shown after the edit.
(c) Expected values, derived from PRD 5.1 and the era table: error "Critical: do not drive."; ui 61 + 4 = 65; wired unchanged 106; diff 50 insertions.
(d) No contradiction found; all preconditions pass.
(e) Deliverable: the results pane shows banner, skipped-lab notices, horizon with era and impacted subsystems, with copy in three ui_payload helpers. Decisive check: the new test gives `4 passed` (and `4 failed` on base), ui 65 passed, probe P3 prints both True.

## Assumptions worked past
- The commit has no `Co-Authored-By` trailer: `bash_guard` refused the first commit command whose text held the trailer, so I committed without it (AGENTS.md § git).

## Base failure (R3 procedure)
`git stash push apps/ui/app.py apps/ui/ui_payload.py`; new test: `4 failed in 1.04s`; `git stash pop` restored the edit.

## Probe P3
`rendered: {'horizon': True, 'gas skipped disclosure': True}` (step 4; an extra grep hit `rendered: {shown}` is unrelated text).

## VERIFICATION GATE
step 1: ui `65 passed`, wired `106 passed`. step 2: `4 passed`. step 3: `All checks passed!`, `2 files changed, 50 insertions(+)`, status listed only the note before the commit. step 4: P3 line above. Verdict: CLEAN (in-scope).

## CODE REVIEW
Diff read in full: every line is R1/R2 from apply_fix.py, no other app.py change. Anti-orphan: the three helpers and the three constants are read in app.py and the test.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-07T08:10:30Z | 2026-11-07T08:12:01Z | 1.5 | ABSENT

## Revision 02
Readiness: (a) start state matched: branch `fix/T-AUD-10d`, HEAD `d936f86`, status listed only the note and the RESULT. (b) The R4 test passes on the committed code (placement is already right), so the red check is the mutant. (c) Expected mutant result `1 failed, 3 passed`. (d) No defect found. (e) Deliverable: the test file equals the r02 copy; its decisive check is the mutant, which moves the banner below the abstain split and must fail only the placement test.
Assumption worked past: the commit has no `Co-Authored-By` trailer, because `bash_guard` refused the commit command with it.
- `cp` then `cmp` of the test against `test_t_aud_10d_result_panels_r02.py`: identical.
- Step 2: `4 passed`.
- Mutant (app.py copied to `recheck/T-AUD-10d/mut/app.py`, banner lines moved above `st.subheader("🔧 Actionable Remediation")`, one level deeper): `1 failed, 3 passed`. A first mutant script failed to read app.py (cp1252 decode) and changed nothing; I reran it with utf-8. app.py restored, `cmp` identical, `git diff` of app.py empty.
- Step 1: ui `65 passed`, wired `106 passed`. Step 3: `All checks passed!`, `2 files changed, 50 insertions(+)`, status lists only the note and the RESULT. Step 4: `rendered: {'horizon': True, 'gas skipped disclosure': True}`.
- Commit `2d6edba` on `fix/T-AUD-10d`.
- Time: revision 02 | 2026-11-07T08:18:17Z | 2026-11-07T08:19:23Z (plus note writing) | about 2 | ABSENT
