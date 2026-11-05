### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `recheck/T-AUD-11d/check_report.py` on `sample_good.md` (8 sections, 1 finding): `sections 8/8, findings 1, refs ok 2/2`, `REPORT OK`, exit 0; on `sample_bad.md` (bad tag, no refs): `REPORT BAD` |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive the findings; confirmed drifts → a DTCLab docs fix row (as T-AUD-12, 13, 14).

### Cold read ###
Derived from T-AUD-11c by fixed substitutions (lab, paths, P1/P2/P3, branch base `759653a`) plus the calibration
rules from REVIEW_T-AUD-11b and 11c (P1 is the `.md` files of `docs/`; a quote holds the drifting value; a role line met through
another lab is not drift; an ignored data path absent on this host is not drift). Grep for `vinlab` and `11c`: only the lineage (11c score), wall-clock baseline and P1-P3 population cells remain.
P1 order equals `DOCS` in the 11d checker. No contradiction found.

### Notes ###
- Docs row: no second-model review. P1 excludes `graph/`, `wiki/` and `docs/audits/`.
