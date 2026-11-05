# T-AUD-11d progress note

## Readiness challenge
(a) Starting state matches the task. Branch `fix/T-AUD-11d`, HEAD `a4db998` (`spec(T-AUD-11d)`, a descendant of `759653a`), `git status --porcelain` printed nothing. Base = `a4db998`. The Preconditions command printed `checked` only.
(b) The checker fails for the intended reason. Step 1 on the missing report raises `FileNotFoundError` for `audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md`. The report does not exist yet.
(c) Expected decisive value, derived from the checker source and not from the report: `sections 8/8`, `refs ok N/N` with both N equal, `REPORT OK`, exit 0. The counts I expect to be true from the code: 30 `patterns` entries and 3 `dna_gate:` lines in `routing_tag_map.yaml`; 17 `DTCRoutingTag` members; 2 fields in `DtcEmissionsView`; 7 `ff_*` flags in `FreezeFrameRecord`; 4 `Mode06MonitorState` members.
(d) No contradiction or missing decision prevents the work.
(e) Teach-back: the deliverable is one drift report with an `## <path>` section for each of the 8 DTCLab documents, each finding quoting the document line and the code line. The decisive check is `check_report.py` printing `sections 8/8`, equal `refs ok N/N` and `REPORT OK`.

## Assumptions worked past
- Doubtful cases kept out of the report (R4): README `multi-DTC patterns` (no code names a multi-DTC pattern, but the line is a role statement); `DTC_VOCABULARY.md:410` says manufacturer MIDs are layered on top via the dictionary JSON, while the JSON `_description` says they are layered by the caller; `DTC_VOCABULARY.md:205` `DTCState` is described as exposed to `dtclab/core/*` (it exists in `vocabulary.py`, no core module imports it, the code docstring says so); ADR-0004 and LLD §10 describe fail-at-import for the config files (the mapper loads the YAML in `DataFusionSanitizer.__init__`, the dictionary on the first `evaluate_monitor` call); `ECU_INTERNAL_HISTORY` range `P0600–P0699` in `DTC_VOCABULARY.md:122` is an enum comment, not a mapping claim.
- Where a document contradicts itself (for example `PRD_DTCLab.md:121` says 30 entries, `:56` says 32), I reported only the line that disagrees with the code.
- The "Wired adapter" claims are reported as MISSING with an ABSENT command that searches `apps` and `labs/comlab` for `classify_top3|rank_candidates`; the command shows no caller, nothing about other places.
- `labs/dtclab/dtclab/__pycache__` exists on disk; it is not tracked, I did not touch it.

## Time
phase | start | end | minutes | context at end
First action | 2026-11-05T20:55:23Z | 2026-11-05T21:00:48Z | 5 | ABSENT

## VERIFICATION GATE
- Step 1: `check_report.py` -> `sections 8/8, findings 44, refs ok 77/77`, `REPORT OK`, exit 0. The previous decisive failure (`FileNotFoundError`, no report) is gone.
- Step 2: `git diff --name-only HEAD~1 HEAD` -> `audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md` only.
- Step 3: `git log --oneline -3` -> `b103252` (mine), `a4db998` (spec), `759653a`. `git status --porcelain` -> the note only, before the RESULT was written.
- No test suite ran: the row writes a report only (task text).

## CODE REVIEW
- Scope: one new report file in the commit; no document, code, test or data file changed.
- Each finding was derived from the code read in this session. Counts quoted in the report come from `grep -c` commands shown in the report.
- Section 1 (README) holds `No drift detected.` The README names `multi-DTC patterns`; see Assumptions.
- The commit has no co-author trailer: `bash_guard` refused the commit command while the trailer text was in it.
