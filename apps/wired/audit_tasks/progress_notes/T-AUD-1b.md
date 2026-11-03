# T-AUD-1b progress note

## Readiness
- (a) Starting state matches: branch fix/T-AUD-1b, HEAD bea265a (base = spec commit, child of 78a48b6), `git status --porcelain` empty. Baselines on the base: wired 36 passed, ui 30 passed, 2 deploy probes 2 passed (P4 holds).
- (b) The 5 new tests will fail on the base for the intended reason (names unprefixed, no `-c` line); I run them red before any manifest edit.
- (c) Expected values derived from the task: 8 `fourdapp-` names; wired suite 36 + 5 = 41; constraints at least 48 lines (47 third-party + six).
- (d) No contradiction found. `fix/T-AUD-1c` exists (78a48b6), so step 7's log range resolves.
- (e) Deliverable: rename 8 dists to `fourdapp-*`, give dnalab its two lab deps, pin the closure in `constraints.txt` and reference it from `requirements.txt`, with 5 manifest tests. Decisive check: a clean venv installs at the pins and imports the app, and removing `-e labs/dnalab` makes resolution fail naming `fourdapp-dnalab`.

## Assumptions worked past
- Step 3 cannot give its expected failures in the step-2 venv: the `fourdapp-*` dists are already installed there, so both dry-runs exit 0 (count 0). I ran step 3 in a second fresh venv (`recheck/T-AUD-1b/venv2`): exit 1 with `No matching distribution found for fourdapp-dnalab` (count 2), and standalone `labs/dnalab` names `fourdapp-symptomlab`, exit 1. Soft finding in the blocker JSON. I found it after the edits, because only running the step shows it.
- The commit is refused by `bash_guard` (the mandated `-c user.name=...` identity; same as T-AUD-1a). Hard finding in the blocker JSON. I did not work around it. Nothing is staged.
- A stray bare `python -` call opened a REPL for a moment. It wrote nothing.

## Verification (from C:/4DApp/repo)
- Step 1 `venv-ok`. Step 2: `install exit 0`, `unpinned-or-off []`, `imports-ok`.
- Report: 55 installs, 47 third-party + `six` = 48 pin lines (P2 holds). `constraints.txt`: 3 `#` header lines + 48 pins.
- Step 3 (venv2): see Assumptions. Step 4: `41 passed`. Step 5: `30 passed`. Step 6: `2 passed`. Step 7: ruff `All checks passed!`.
- Step 7 git lines: NOT MET. `git log --oneline fix/T-AUD-1c..HEAD` shows only the spec commit bea265a; the working tree holds the 9 modified files plus the untracked `constraints.txt`, test file and notes.
- Red gate: on the base, 4 of 5 new tests failed; `test_every_local_dependency_has_an_editable_line` passed vacuously (no `fourdapp-*` dependency existed). Mutant M1 (dnalab renamed back) exercises it.
- Mutants: M1 dnalab renamed back -> 2 failed (`test_local_dists_are_prefixed`, `test_every_local_dependency_has_an_editable_line`). M2 `-c` line removed -> 1 failed (`test_requirements_use_pinned_constraints`). M3 dnalab deps emptied -> 1 failed (`test_dnalab_declares_its_lab_imports`). Files restored; 5 passed after.

## VERIFICATION GATE
Steps 1-6 and ruff: PASS. Commit and step-7 git lines: BLOCKED (bash_guard).

## CODE REVIEW
Scope: 9 manifests/requirements files plus `constraints.txt` and the test file, all in `### Files to touch ###`. No `.py` outside the new test. No finding.

## Time
phase | start | end | minutes | context at end
all | 2026-11-03T19:32:07Z | 2026-11-03T19:40:30Z | 8 | ABSENT

## Round 2
- Step 3 as corrected, in `venv2` (0 `fourdapp` dists installed): without `-e labs/dnalab` count 2, exit 1 (`No matching distribution found for fourdapp-dnalab`); standalone `labs/dnalab` prints `fourdapp-symptomlab`, exit 1.
- Commit: `git add` of the 11 paths as its own command, then the commit as its own command. It succeeded: `186aa0a fix(T-AUD-1b): unique fourdapp-* dist names, dnalab lab deps, pinned constraints.txt`.
- Step 7: ruff `All checks passed!`; `git log --oneline fix/T-AUD-1c..HEAD` shows 3 `audit:` commits plus my 1 `fix(T-AUD-1b):` commit; `git status --porcelain` lists the note, its `.blocker.json` and the RESULT only.
- The round-1 hard finding (commit refused) is resolved by correction 01. I did not re-run steps 2, 4-6: no tracked file changed since round 1.

### Time (round 2)
phase | start | end | minutes | context at end
round 2 | 2026-11-03T19:43:07Z | 2026-11-03T19:44:04Z | 1 | ABSENT
