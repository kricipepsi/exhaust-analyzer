# Result

## Status
completed

## Summary
LC-002 now fires only on LEAN_MIXTURE and MF-005 only on IGNITION_MISFIRE. Both chemistry rows are GATING, and the base weights rise by 0.10 (0.81 to 0.91, 0.75 to 0.85). The commit also carries the three REVIEW_T-COMA-27 test hardenings, the new sink-gate test and four re-stated pins. All P2 counts reproduced. Corpus family accuracy is 221 of 314 (before 216).

## Files changed
Commit `9a32ea6`: `labs/comlab/registry/rules/lean_condition.json`, `labs/comlab/registry/rules/misfire.json`, `labs/comlab/registry/tests/test_mechanical_wear_rules.py`, `labs/comlab/tests/unit/test_t_coma_27_unrouted_states.py`, `labs/comlab/tests/unit/test_t_coma_28_sink_chemistry_gate.py` (new), `labs/comlab/tests/unit/test_differential_surfacing.py`, `labs/comlab/tests/unit/test_tunable_reweight.py`, `apps/wired/tests/test_t_coma_11_reported_confidence.py`, `apps/wired/tests/test_t_coma_6_firing_predicate.py`.
Untracked: `progress_notes/T-COMA-28.md`, `progress_notes/T-COMA-28.blocker.json`, this RESULT. Runtime: `C:/4DApp/recheck/T-COMA-28/pt/`.

## Commands executed
First action and Preconditions (verbatim); a red run of the staged new test on the base; `$PY -I C:/4DApp/recheck/T-COMA-28/rehearse.py`; `git diff`; Verification steps 1-5 (verbatim); `git add <9 paths>`; `git commit`.

## Validation evidence
- Red on base: `3 failed, 3 passed` (`[CAM_TIMING_ADVANCED]`, `[TIMING_RETARDED]`, `test_gating_tiers`).
- rehearse: `applied 12 edits`.
- Step 1: `569 passed`; `186 passed`; `75 passed`.
- Step 2: `508 passed, 5 skipped`; `29 passed`.
- Step 3: `LC-002 score: None MF-005 score: None map_kpa: 35.0`; `1 failed, 13 passed, 2 deselected`. The failure is `test_every_chemical_signature_has_a_v2_rule` (FLAT_CAMSHAFT, INCOMPLETE_OXIDATION, out of scope).
- Step 4: `changed 32 of 314`; `family accuracy 221 of 314 (before 216)`; `gained 9 lost 4`.
- Step 5: `All checks passed!`; `9 files changed, 77 insertions(+), 13 deletions(-)`.

## Criteria
| # | verdict | evidence |
|---|---|---|
| 1 | MET | rehearse printed `applied 12 edits`; steps 1-4 output matches P2 exactly (above) |
| 2 | MET, with one note | ruff clean; P2 diff stat; one new commit `9a32ea6` after spec `a80b5f2`. Porcelain lists the note, the RESULT and the header-authorised `T-COMA-28.blocker.json` |

## Decisions the task did not specify
- R4 says "8 cases", but the staged test has 6. I used it unchanged and recorded a soft STALE-ANCHOR in `T-COMA-28.blocker.json` (the validator printed `OK`). P2's 569 = 563 + 6.
- The blocker record is a third untracked file at the end. The header authorises it, but criterion 2 names only the note and the RESULT.
- Pyright and the skill's wider task-end gate were not run, because the task's Verification does not mandate them: `NOT RUN`.

## Pre-existing changes preserved
None in the repo: the starting porcelain was empty.

## Rollback
`git -C C:/4DApp/repo reset --hard a80b5f2` on `fix/T-COMA-28` only, or `git revert 9a32ea6`.

## Remaining risks or uncertainties
- The corpus loses 4 cases alongside the 9 gains. These are Cowork's rehearsed figures; I did not inspect the four individually.
- FLAT_CAMSHAFT and INCOMPLETE_OXIDATION still have no rule (out of scope).

## Branch and log
```
$ git -C repo branch --show-current
fix/T-COMA-28
$ git -C repo log --oneline 3cd8541..HEAD
9a32ea6 fix(T-COMA-28): LC-002 and MF-005 gate on their own chemistry (F-C1-2)
a80b5f2 coma: spec(T-COMA-28): LC-002 and MF-005 gate on their chemistry (F-C1-2 slice 2)
```
