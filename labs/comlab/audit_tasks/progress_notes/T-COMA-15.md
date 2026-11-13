# T-COMA-15 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-15, one spec commit 4de9540 over 68dd691, `git status --porcelain` empty, preconditions `checked`. P1 on base: comlab 510 passed, 4 skipped; wired 170 passed; ui 70 passed.
(b) Test is expected to fail on base for the intended reason (inverted label/rows); confirmed by running it before the edit (below).
(c) Independent expected value: `delta = obd_lambda - lambda_chem`; delta > tol means sensor reads lean, so O2_SENSOR_BIASED_LOW. Base code line 217-221 returns BIASED_HIGH for delta > tol, so base is inverted; SF-001 row is `gt 0.03` on base, must become `lt -0.03`.
(d) No contradiction or missing decision found.
(e) Deliverable: swap the two bias labels and the SF-001/SF-002 delta rows, update the three pins, and add the new test. Decisive check: new test 6 passed (4 failed, 2 passed on base) and corpus `vs before 18 of 314`, `vs expected 0 of 314`.

## Assumptions worked past
- e2e mock `sensor_biased_high()` keeps its name; after R1 it yields O2_SENSOR_BIASED_LOW (task Context).

## R5 results
- Base (new test run on the unedited base code, before `rehearse.py`; no stash needed, same code state): `4 failed, 2 passed`.
- Mutant A (labels swapped back at lines 222/231): `2 failed, 4 passed`.
- Mutant B (SF-001 row `gt 0.03`, SF-002 row `lt -0.03`): `2 failed, 4 passed`.
- Each restored by file copy from `C:/4DApp/recheck/T-COMA-15/pt/*.bak`; `cmp` identical; `git diff --stat` back to `5 files changed, 36 insertions(+), 35 deletions(-)`; new test `6 passed` again.

## VERIFICATION GATE
1: comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`. 2: `6 passed`. 3: line 222 `O2_SENSOR_BIASED_LOW`, line 231 `O2_SENSOR_BIASED_HIGH`. 4: `vs before 18 of 314`, `vs expected 0 of 314`. 5: ruff `All checks passed!`; `6 files changed, 76 insertions(+), 35 deletions(-)`; commit e8f1e84 on fix/T-COMA-15 after spec commit 4de9540; `git status --porcelain` lists only the note (RESULT written after). Verdict: CLEAN.

## CODE REVIEW
Scope: six files, all in Files to touch; diff read and matches R1-R3. No new field or literal beyond the rows R2 names. Out-of-scope items (rule description wording, mock names, UI copy, D2 probe) untouched. Mock `sensor_biased_high()` now yields O2_SENSOR_BIASED_LOW, as the task records.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T11:30:24Z | 2026-11-13T11:32:48Z | 2 | ABSENT
(Clock reads from `date -u`; the end time is the commit time, the RESULT followed within the minute.)

## Correction 1
- Start: branch fix/T-COMA-15 at c651f31; `git status --porcelain` listed only the note and the RESULT; preconditions `checked`.
- R7 base failure: corrected test copied (`cmp` identical) before `correct1.py`; step 2 gave `2 failed, 4 passed`.
- R6: `correct1.py` printed `applied`; SF-001 now says "sensor reads falsely rich, ECU under-fuels", SF-002 "falsely lean, ECU over-fuels".
- Assumption worked past: the commit message has no co-author trailer; `bash_guard` refused the command with the trailer text.
- VERIFICATION GATE: 1: comlab `510 passed, 4 skipped`; wired `176 passed`; ui `70 passed`. 2: `6 passed`. 3: line 222 `O2_SENSOR_BIASED_LOW`, line 231 `O2_SENSOR_BIASED_HIGH`. 4: `vs before 18 of 314`, `vs expected 0 of 314`. 5: ruff `All checks passed!`; `git diff --stat e8f1e84 HEAD` `2 files changed, 10 insertions(+), 7 deletions(-)`; new commit c2212f5; `git status --porcelain` lists only the note and the RESULT. Verdict: CLEAN.
- CODE REVIEW: both changed files are in Files to touch; the JSON diff is two description strings; the test diff is the copied `_c1` file. No other file changed.

## Time (correction 1)
phase | start | end | minutes | context at end
correction 1 | 2026-11-13T11:41:29Z | 2026-11-13T11:42:50Z | 1 | ABSENT
