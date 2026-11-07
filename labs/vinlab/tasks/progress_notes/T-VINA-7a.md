# T-VINA-7a progress note

## Readiness challenge
(a) Starting state matches: branch `fix/T-VINA-7a`, `git log 0552976..HEAD` = spec commit f621680, `git status --porcelain` empty; preconditions print `checked`. HEAD at start f621680.
(b) Test fails for the intended reason on the base: new test file copied (cmp ok); base vinlab `4 failed, 389 passed, 8 skipped` (3 x `unclosed database` ResourceWarning, 1 x blank-brand grade); probes f9/f14 `2 failed, 1 passed, 48 deselected` (P1: 3 `unclosed database` warnings).
(c) Decisive expected value, derived from the vocabulary (no brand means no engine, `NONE` = no engine): WMI 002 blank brand -> `VinConfidence.NONE`; every lookup leaves `[]` unclosed-database warnings. Matches the test.
(d) No contradiction or missing decision: the five files in Files to touch cover R1-R3; no stop (a)-(d) fires.
(e) Teach-back: `lookup_engine_ref` wraps both connections in `closing(...)` and `_compute_confidence` returns NONE for `wmi_brand_missing`, with docs and the one old PARTIAL test following. Decisive check: step 2 `61 passed, 2 skipped` (base `4 failed, 57 passed, 2 skipped`) and probes `3 passed`.

## Assumptions worked past
none. Commit trailer: the first commit attempt (chained, with a `Co-Authored-By` line) was refused by `bash_guard`; the commit was made as its own command without the trailer.

## R4 results
- Base failure (`git stash push` of vinlab/vinlab, vinlab/docs, test_decoder.py; step 2; `git stash pop`): `4 failed, 57 passed, 2 skipped`. Stash popped; `git diff --stat` back to 5 files, 12 insertions, 9 deletions.
- Mutant (line 81, second `closing(...)` turned back into plain `with sqlite3.connect(uri, uri=True) as conn:`): `1 failed, 60 passed, 2 skipped`. Line restored by hand; `cmp` against the pre-mutant copy identical; `git diff --stat` unchanged (5 files, 12 insertions, 9 deletions).
- `apply_fix.py` diff equals `rehearsal.patch` (index lines ignored).

## VERIFICATION GATE
1. vinlab `393 passed, 8 skipped`; wired `113 passed`; ui `70 passed`.
2. `61 passed, 2 skipped`.
3. `3 passed, 48 deselected`.
4. ruff `All checks passed!`; `git diff --stat 0552976 HEAD -- labs/vinlab/vinlab labs/vinlab/docs` `4 files changed, 10 insertions(+), 7 deletions(-)`; log: fba4eb4 (new) after f621680 (spec); `git status --porcelain` lists only the note (RESULT added after).
Verdict: CLEAN.

## CODE REVIEW
Scope: six paths, all in Files to touch. Every changed line traces to R1 or R2. No new field, key or function. No magic number. No cross-lab import. No network in tests. Findings: none. pyright and `ruff --select S`: NOT RUN (Verification names neither).

## Time
phase | start | end | minutes | context at end
first action to finish | 2026-11-07T16:07:28Z | 2026-11-07T16:09:38Z | 2.2 | ABSENT
