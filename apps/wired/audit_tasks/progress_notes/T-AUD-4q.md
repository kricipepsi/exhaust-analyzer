# T-AUD-4q progress note

## Readiness
(a) Start state matches: branch fix/T-AUD-4q, base 8d6e8c7 (descends from df7c2cc), `git status --porcelain` empty, preconditions print `checked` only.
(b) New test fails on base for the intended reason: `2 failed` (modules still importable; docs still hold `COMLab.project(`).
(c) Expected values are the P2/P3/P4 pins (25 tests removed, 2 added: 525-25+2 = 502 passed); P1 grep shows only test_projection.py imports the modules.
(d) No contradiction found.
(e) Delete the projector and its test, re-point docs, registry and three docstrings at the composition builders. Decisive check: new file `2 passed`, comlab `502 passed, 4 skipped, 2 errors`, other suites equal pins.

## Assumptions worked past
- gaslab/dna_view.py docstring names `lab_dna_views.py`; R4 rewrites it via apply_fix.py.
- The task's step-3 `git checkout -- labs/comlab/registry/case_library.html` names a path that git does not track (the file is under `registry/docs/`); it errored harmlessly and the registry suite left the tree clean.
- `bash_guard` refused the commit with the `Co-Authored-By` trailer; committed without it per AGENTS.md.

## VERIFICATION GATE
Step 1: 2 passed. Step 2: 502 passed, 4 skipped, 2 errors. Step 3: registry 5 failed, 502 passed, 4 deselected; gaslab 208 passed, 2 skipped, 4 deselected; obdlab 391 passed, 2 skipped; dtclab 590 passed; wired 101 passed; ui 52 passed. Step 4: ruff All checks passed. Red gate before the change: 2 failed.

## CODE REVIEW
Diff read: code diffs in the three lab files are docstring-only; the registry change is three consumer strings; deletions are the three R1 files. No scope drift.

## Time
phase | start | end | minutes | context at end
implement | 2026-11-06T14:33:02Z | 2026-11-06T14:34:47Z | see timestamps | ABSENT

## Revision 02 (redispatch, R6)
Start state: HEAD c8ecba9 on fix/T-AUD-4q, only note and RESULT untracked, apply_rev02.py present. Red gate: new file `1 failed, 2 passed` (test_dep4_row_names_no_projector_work), as P3 pins. Ran apply_rev02.py, copied the rehearsed test, committed as a second commit.

## VERIFICATION GATE (rev02, supersedes the first)
Step 1: 3 passed. Step 2: 503 passed, 4 skipped, 2 errors. Step 3: registry 5 failed, 502 passed, 4 deselected; gaslab 208 passed, 2 skipped, 4 deselected; obdlab 391 passed, 2 skipped; dtclab 590 passed; wired 101 passed; ui 52 passed. Step 4: ruff All checks passed; status lists only note and RESULT.

## CODE REVIEW (rev02)
R6 diff: one cell of CROSS_LAB_DEPENDENCIES.md (DEP-4) plus the third test. No scope drift.

## Time (rev02)
redispatch | 2026-11-06T14:45:04Z | 2026-11-06T14:46:17Z | see timestamps | ABSENT
