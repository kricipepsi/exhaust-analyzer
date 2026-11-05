### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `recheck/T-AUD-11h/check_report.py` on `sample_good.md` (12 sections, 1 finding): `sections 12/12, findings 1, refs ok 2/2`, `REPORT OK`, exit 0; on `sample_bad.md` (bad tag, no refs): `REPORT BAD` |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive the findings; confirmed drifts → a COMLab ADR fixes, merged into T-AUD-18.

### Cold read ###
Derived from T-AUD-11g by fixed substitutions (P1 = the 12 `docs/adr/` files, report name `_comlab_adr`, P3 = a 12-section checker, branch base `7a9da66`) plus the calibration
rules from REVIEW_T-AUD-11b and 11c (P1 is the `.md` files of `docs/`; a quote holds the drifting value; a role line met through
another lab is not drift; an ignored data path absent on this host is not drift). Grep for `11g` and `8/8`: only the lineage, the wall-clock baseline, the base branch and the out-of-scope pointer remain. The vocabulary copies left 11h for T-AUD-18 (a doc-vs-doc resync, not a code check).
P1 order equals `DOCS` in the 11h checker. No contradiction found.

### Notes ###
- Docs row: no second-model review. P1 excludes `graph/`, `wiki/` and the lab's `wiki/` and `graph/`.
