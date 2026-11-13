# T-COMA-21 progress note

## Readiness
(a) Starting state matches: branch `fix/T-COMA-21`, one commit c988cb9 after 8dc0b43, `git status --porcelain` empty; P1 base counts reproduced (comlab 527 passed 4 skipped; wired 186; ui 73; step-3 probes 4 failed).
(b) The new test fails on base for the intended reason (R5 base run below, `10 failed, 1 passed`).
(c) Expected value derived from the rulings: `_map_degradation` gives GAS_DOMINANT for suppress_gaslab, suppress_obd_live_pids, or obd_live_data None; rating is the score band 0.80/0.50, capped under GAS_DOMINANT, LOW on abstain/INVALID. Step 2 must give 11 passed.
(d) No contradiction found; the patch and test are Cowork's rehearsal files.
(e) Teach-back: apply rehearsal.patch (R1-R3) and add Cowork's test, so `degradation_mode` reflects OBD absence and the rating follows the verdict score. The decisive check is step 2 `11 passed` (base `10 failed, 1 passed`), step 3 `4 passed`, and verdicts `changed 0 of 314`.

## Assumptions worked past
- The commit message omits the attribution trailer: `bash_guard` refuses a command whose text names the tool in a trailer.

## R5 results
- Base (aggregator stashed): `10 failed, 1 passed`. Patched: `11 passed`.
- Mutant A (drop `or request.obd_live_data is None`): `1 failed, 10 passed`.
- Mutant B (drop `or directive.suppress_obd_live_pids`): `1 failed, 10 passed`.
- Mutant C (drop `or degradation_mode == "GAS_DOMINANT"`): `1 failed, 10 passed`.
- Mutant D (drop `verdict.abstained or `): `1 failed, 10 passed`.
- Mutant E (`<` to `<=` on `_TIER_HIGH_MIN`): `1 failed, 10 passed`.
- Each mutant was reverted by copying back the patched file; `cmp` identical. Restored `git diff --stat`: `3 files changed, 33 insertions(+), 23 deletions(-)` (plus the untracked test).

## VERIFICATION GATE
- step 1: comlab `538 passed, 4 skipped`; wired `186 passed`; ui `73 passed`
- step 2: `11 passed` (base `10 failed, 1 passed`)
- step 3: `4 passed, 14 deselected` (base `4 failed`)
- step 4: `changed 0 of 314`
- step 5: `All checks passed!`; `4 files changed, 110 insertions(+), 23 deletions(-)`; commit 3ed6cb0 after spec commit c988cb9; `git status --porcelain` listed only the note.
- Verdict: CLEAN. pyright and `ruff --select S` were not required by the task: NOT RUN.

## CODE REVIEW
The diff is Cowork's rehearsal patch, read in full. Every line traces to R1-R3. The numeric literals carry wiki citations. `_confidence_from_horizon` is deleted and has no remaining caller (ruff clean). No findings.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T15:20:40Z | 2026-11-13T15:22:50Z | 2 | ABSENT

## Correction 1 readiness
(a) Starting state matches: branch `fix/T-COMA-21`, HEAD 9d47a65 (spec correction) over 3ed6cb0; `git status --porcelain` lists only the note and the RESULT; preconditions printed `checked`.
(b) The two new tests must pass only with the R6 patch; mutants F and G in R7 show each fails when its line is removed.
(c) Expected: step 2 `13 passed`; F and G each `1 failed, 12 passed`; comlab `540 passed, 4 skipped`; diff stat `4 files changed, 126 insertions(+), 23 deletions(-)`.
(d) No contradiction found.
(e) Apply correction1.patch (docstring and BDD row name the `suppress_gaslab` trigger; two tests added), then mutate lines F and G. Decisive check: step 2 `13 passed` and each mutant `1 failed, 12 passed`.

## Correction 1
- R6: `git apply correction1.patch` clean; test `cmp` identical to `test_t_coma_21_mode_and_rating_c1.py`. Step 2: `13 passed`.
- R7 mutant F (drop `directive.suppress_gaslab or ` at the R1 condition): `1 failed, 12 passed`.
- R7 mutant G (first `ExecutionMeta` site passes `"FULL_FUSION"`): `1 failed, 12 passed`.
- Each mutant was put back by copying the good file; `cmp` identical.

### VERIFICATION GATE (correction 1)
- step 1: comlab `540 passed, 4 skipped`; wired `186 passed`; ui `73 passed`
- step 2: `13 passed`
- step 3: `4 passed, 14 deselected`
- step 4: `changed 0 of 314`
- step 5: `All checks passed!`; `4 files changed, 126 insertions(+), 23 deletions(-)`; new commit c176043 after spec commit 9d47a65; `git status --porcelain` lists only the note and the RESULT.
- Verdict: CLEAN. pyright and `ruff --select S` NOT RUN (the task does not require them).

### CODE REVIEW (correction 1)
The diff is Cowork's correction1.patch, read in full: a docstring, one BDD table row and two tests. Every line traces to R6. No findings.

### Assumptions worked past
- The commit has no attribution trailer: `bash_guard` refuses a commit command that carries it (this session it printed a nested-launch/plugin-dir error).

### Time (correction 1)
phase | start | end | minutes | context at end
correction 1 | 2026-11-13T15:30:42Z | 2026-11-13T15:32:07Z | 1 | ABSENT
