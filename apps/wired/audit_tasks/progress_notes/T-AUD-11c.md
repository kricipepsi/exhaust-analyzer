# T-AUD-11c progress note

## Readiness challenge
(a) Starting state matches task: branch `fix/T-AUD-11c`, HEAD `fcc2516` (spec dispatch index, descendant of `972f3eb`), `git status --porcelain` in `repo/` printed nothing. Base = `fcc2516`.
(b) No test applies (report-only row). The decisive checker `check_report.py` fails today: the report file does not exist (Preconditions printed no `EXISTS`).
(c) Expected value derived from the task text: `sections 8/8`, `refs ok N/N` with both N equal, `REPORT OK`. Each ref is re-checked by the script against the line it names.
(d) No contradiction found. Preconditions: `checked`, no `MISSING`, no `EXISTS`.
(e) Teach-back: I write one drift report for the 8 VINLab documents, one section each, in P1 order. Each finding quotes the document line and the code line; step 1 must print `REPORT OK`.

## Assumptions worked past
- `rated_rpm` source: PRD/HLD/DLD/VOCAB name `P14_rated_rpm` of the specimens CSV; the decoder reads `vref.db` column `rated_rpm`. `tools/build_vref_db.py:854` reads `P14_rated_rpm` into that column at build time. Not reported (R4: build-time provenance).
- `_RENAULT_I3` holds `H4Bt`, which the 3-char family regex can never match. The documents list the same set, so no document-code drift. Not reported.
- `open_vref_readonly` has no caller and its docstring says the decoder uses it in `__init__`. The documents only list the function. Not reported.
- `pyproject.toml` declares `requires-python >=3.11`; PRD says Python 3.14. The range is satisfied (R1). Not reported.
- `Emissions.downstream_trim_role` and `has_catalyst` are never set by the decoder (defaults only). The documents give the defaults. Not reported (doubtful).
- `labs/vinlab/mysql_data/` is named by README, PRD, HLD and ADR-0001 but is absent from the working tree and from `git ls-files`. Reported once, under the README.
- `__init__.py:4` says model years 1990-2020; H2 in `decoder.py:131` is 1990-2010 and ADR-0008 says 1990-2020 fleet (data context). Code-internal docstring; ADR line is narrative. Not reported (doubtful).
- Commit trailer: `bash_guard` refused the commit command while its message held the attribution line. I committed without the trailer.

## VERIFICATION GATE
Step 1: `sections 8/8, findings 20, refs ok 38/38` / `REPORT OK` (exit 0). Previous failure (no report file) gone.
Step 2: `git diff --name-only HEAD~1 HEAD` -> `audit/drift/2026-11-05_DRIFT_REPORT_vinlab.md` only.
Step 3: `git log --oneline -3` -> `6f0ffc9`, `fcc2516`, `3e20cf3`; `git status --porcelain` -> the note only (RESULT written after).
Verdict: CLEAN. No test suite applies (report only).

## CODE REVIEW
Scope: one new markdown file; no code, document or data file changed. Findings re-read against the code lines they quote; the checker confirmed 38 of 38 quotes on their lines. Doubtful cases are listed under Assumptions. No blocking finding.

## Time
phase | start | end | minutes | context at end
all | 2026-11-05T20:41:36Z | 2026-11-05T20:45:40Z | 4 | ABSENT
