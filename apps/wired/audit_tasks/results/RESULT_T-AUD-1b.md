# Result

## Status
completed

## Summary
R1-R4 are done in the working tree and every gate passes except the commit: `bash_guard` refuses the mandated commit identity. Nothing is staged or committed.

## Files changed
Modified: 7 `labs/*/pyproject.toml`, `apps/wired/pyproject.toml`, `requirements.txt`. Created: `constraints.txt` (3 header lines, 48 pins), `apps/wired/tests/test_t_aud_1b_manifests.py`, the note and its `.blocker.json`.

## Commands executed
Task First action, Preconditions and Verification steps 1-7; clean-venv `pip install --dry-run --report`; three mutant runs. Details in `progress_notes/T-AUD-1b.md`.

## Validation evidence
Step 2: `install exit 0`, `unpinned-or-off []`, `imports-ok`. Step 4 `41 passed`, step 5 `30 passed`, step 6 `2 passed`, ruff `All checks passed!`. Step 3 in a fresh second venv: exit 1, `No matching distribution found for fourdapp-dnalab`; standalone dnalab names `fourdapp-symptomlab`, exit 1. Mutants: M1 2 failed, M2 1 failed, M3 1 failed.

## Criteria
1. MET: 5 tests pass, wired `41 passed`, 3 mutants fail as named.
2. MET: step 2 output above.
3. MET, in a second fresh venv (decision 1): venv2 output above.
4. MET: ui `30 passed`, probes `2 passed`.
5. MET (round 2): ruff passes; one `fix(T-AUD-1b):` commit `186aa0a`; `git status --porcelain` lists only the note, its blocker JSON and the RESULT.

## Decisions the task did not specify
1. Step 3 run in a fresh second venv, because the step-2 venv already holds the `fourdapp-*` dists and the dry-runs succeed there (soft finding in the blocker JSON).
2. `-c constraints.txt` placed on its own line before `streamlit==1.59.0`, after the header comment.

## Pre-existing changes preserved
none present in `repo/` at the start (`git status --porcelain` empty).

## Rollback
`git restore` the 9 modified files; delete `constraints.txt` and the test file (untracked).

## Remaining risks or uncertainties
The Render build is untested. The commit is owed: Cowork or a redispatch with a guard that admits the identity.

Branch: `git -C repo branch --show-current` -> `fix/T-AUD-1b`. `git -C repo log --oneline fix/T-AUD-1c..HEAD` -> `bea265a audit: author T-AUD-1b ...` (spec commit only; no commit of mine).

## Round 2
Status is now `completed`. Step 3 re-run in `venv2`: count 2, exit 1; standalone dnalab names `fourdapp-symptomlab`, exit 1. Commit `186aa0a` made as its own command after `git add`.

```
$ git -C repo branch --show-current
fix/T-AUD-1b
$ git -C repo log --oneline fix/T-AUD-1c..HEAD
186aa0a fix(T-AUD-1b): unique fourdapp-* dist names, dnalab lab deps, pinned constraints.txt
573f76e audit: T-AUD-1b step 7 wording (commit count independent of spec commits)
5c3c0bb audit: T-AUD-1b correction 01 (B3: step 3 in venv2; commit as its own command)
bea265a audit: author T-AUD-1b (F-P5-1/2/4: fourdapp-* dist names, dnalab lab deps, constraints.txt); ledger
```

## Time
round 1: 2026-11-03T19:32:07Z to 19:40:30Z, 8 min. Round 2: 19:43:07Z to 19:44:04Z, 1 min. Context at end: ABSENT.
