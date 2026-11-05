### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `check_report.py` on `recheck/T-AUD-11a/sample_good.md` (8 sections, 2 findings, one ABSENT): `sections 8/8, findings 2, refs ok 3/3`, `REPORT OK`, exit 0; on `sample_bad.md` (bad class, bad quote, line past end, empty sections, 7 sections): 5 PROBLEM lines, `REPORT BAD`, exit 1 |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive 3+ findings from their quotes; each confirmed drift → a fix row; calibrates 11b-11h.

### Cold read ###
Own pass (read-only report row, format checked by a script). P1 order equals `DOCS` in check_report.py; the R2 bullet
shape equals the checker's regex (rehearsed). R4 (future-work text) is a judgement rule; its doubtful cases go to the
note, so the report stays checkable. No contradiction found.

### Notes ###
- Docs row: no second-model review (CLAUDE.md step 6). Cowork re-derives findings at review.
- Pilot choice: SymptomLab is the smallest set (8 docs, 45.7 KB; comlab 340 KB, semantic 140 KB). Tradeoff lost:
  comlab first would hit the most-used lab first but cannot fit one session.
