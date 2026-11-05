### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `recheck/T-AUD-11g/check_report.py` on `sample_good.md` (8 sections, 1 finding): `sections 8/8, findings 1, refs ok 2/2`, `REPORT OK`, exit 0; on `sample_bad.md` (bad tag, no refs): `REPORT BAD` |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive the findings; confirmed drifts → a COMLab docs fix row (as T-AUD-12 to 17).

### Cold read ###
Derived from T-AUD-11f by fixed substitutions (lab, paths, P1/P2/P3, branch base `d8dd7d4`) plus the calibration
rules from REVIEW_T-AUD-11b and 11c (P1 is the `.md` files of `docs/`; a quote holds the drifting value; a role line met through
another lab is not drift; an ignored data path absent on this host is not drift). Grep for `obdlab` and `11f`: only the lineage, the wall-clock baseline and the base branch remain. Split ruling: COMLab has 21 documents (333 KB); 11g takes the 8 core ones so the 8-section checker and the per-lab size hold; the 11 ADRs and the two vocabulary copies (which differ from their lab originals by 52 and 4 diff lines: a doc-vs-doc check) are T-AUD-11h. Tradeoff lost: one report per lab; 11h needs rows_max past 60.
P1 order equals `DOCS` in the 11g checker. No contradiction found.

### Notes ###
- Docs row: no second-model review. P1 excludes `graph/`, `wiki/` and the lab's `wiki/` and `graph/`.
