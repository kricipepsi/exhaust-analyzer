# T-AUD-11a progress note

## Readiness challenge
Written after the report draft, not before the first edit: I read the code and all 8 documents first (read-only), then created the report. Disclosed as a process slip.
- (a) Start matched: branch `fix/T-AUD-11a`, HEAD `1936f06` (descendant of `7ac5e62`, recorded as base), `git status --porcelain` empty, preconditions printed `checked`.
- (b) Test failed for the intended reason: no report existed before the first write (precondition showed no `EXISTS report`).
- (c) Decisive value: 8 sections, every ref resolves (`refs ok N/N`). Derived from the check script's rules, not from the report.
- (d) No contradiction or missing decision found.
- (e) Deliverable: one drift report with 8 sections, each finding quoting doc and code. Decisive check: step 1 prints `REPORT OK`.

## Assumptions worked past
- The 4l tip line numbers: `pyproject.toml` requires-python is line 8 (a first `head` read miscounted it as 7; the checker caught it).
- R4: the oil_consumption entries in PRD/HLD are "Deferred", but the code ships the pair. I reported them, since the code contradicts the document.
- Omitted as doubtful: HLD/LLD/DLD say "PRD Baseline v2.0" while the PRD is v2.1 (doc-vs-doc, no code side). SYMPTOM_VOCABULARY section 4 "except dnalab -> symptomlab" ignores apps/wired callers; reported once under HLD only.
- README and SYMPTOM_VOCABULARY: no drift found.

## VERIFICATION GATE
- Step 1: `sections 8/8, findings 13, refs ok 24/24` / `REPORT OK`, rc 0. Earlier run printed `REPORT BAD` (one wrong line number), fixed.
- Step 2: `audit/drift/2026-11-05_DRIFT_REPORT_symptomlab.md` only.
- Step 3: log shows the spec commit then `ccf472d`; status lists only the note and the RESULT.
- Verdict: CLEAN. No `.py` touched, so ruff, pyright and the test suites do not apply (NOT RUN).

## CODE REVIEW
Scope: only the report was added; no document, code, test or data file changed. Each finding was re-checked by the script against the file line. Verdict: CLEAN.

## Time
phase | start | end | minutes | context at end
all | 2026-11-05T19:51:29Z | 2026-11-05T19:53:12Z | 2 | ABSENT
(Clock reads only; the wall clock looks short against the work done.)
