# Result

## Status
completed

## Summary
R1: validator passes `vin_dna` to `_run_dtclab`. R2: oracle tests take paths from `__file__` and run `sys.executable` in the repo root. R3: five build-corpus tests skip when local Jaeger/harness data is absent. Applied with Cowork's `apply_fix.py`; diff read before commit.

## Files changed
- apps/wired/v7/load_corpus.py
- apps/wired/v7/tests/test_oracle_repin.py
- labs/comlab/registry/tests/test_build_corpus.py
- (notes) labs/comlab/audit_tasks/progress_notes/T-COMA-9.md, this RESULT

## Commands executed
First action; preconditions; P1 baseline (validator, oracle file, build_corpus); `apply_fix.py`; Verification steps 1-4; R5 mutant and manual restore; one commit.

## Validation evidence
- base: validator `TypeError: _run_dtclab() missing 1 required positional argument: 'vin_dna'`; oracle `8 failed`; build_corpus `5 failed, 24 passed`
- validator: `Parsed and validated 314/314 cases successfully.`, `Corpus validation is clean!`
- oracle file: `8 passed` from apps/wired; `8 passed` from repo root
- test_build_corpus.py: `24 passed, 5 skipped`
- comlab `510 passed, 4 skipped`; wired `123 passed`; ui `70 passed`
- ruff: `All checks passed!`
- `git diff --stat 3974488 HEAD -- apps/wired/v7 labs/comlab/registry`: `3 files changed, 15 insertions(+), 4 deletions(-)`
- R5: `1 failed, 7 passed`

## Criteria
1. MET: steps 1-3 and R5 as above.
2. MET: ruff clean, diff stat as P2, one new commit after the spec commit. `git status --porcelain` before this RESULT listed only the note; after it, the note and this RESULT.

## Decisions the task did not specify
- The commit message has no attribution trailer: `bash_guard` refused the first commit attempt that included it. The message is otherwise as AGENTS.md requires.

## Pre-existing changes preserved
none present in the repo (clean start).

## Rollback
`git -C repo reset` is barred on main only; on the task branch: `git revert 34085fe`, or `git restore` of the three paths from `d5875af`.

## Remaining risks or uncertainties
- The yardstick hash-lock test fails for a real reason; it is T-COMA-10, untouched.

branch: fix/T-COMA-9
```
34085fe fix(T-COMA-9): v7 validator passes vin_dna to dtclab; data-dependent dev tests run anywhere or skip
d5875af coma: spec(T-COMA-9): v7 validator and data-dependent dev tests (Linux 053); register T-COMA-10 (yardstick)
```
