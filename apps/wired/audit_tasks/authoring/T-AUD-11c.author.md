### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `recheck/T-AUD-11c/check_report.py` on `sample_good.md` (8 sections, 1 finding): `sections 8/8, findings 1, refs ok 2/2`, `REPORT OK`, exit 0; on `sample_bad.md` (bad tag, no refs): `REPORT BAD` |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive the findings; confirmed drifts → a VINLab docs fix row (as T-AUD-12, T-AUD-13).

### Cold read ###
Derived from T-AUD-11b by fixed substitutions (lab, paths, P1/P2/P3, branch base `972f3eb`) plus the two calibration
rules from REVIEW_T-AUD-11b (P1 is the whole `docs/` listing; a quote holds the drifting value; a role line met through
another lab is not drift). Grep for `dnalab` and stray `11b`: only the caller `labs/dnalab/dnalab/assembly.py` (P2), the base branch and the calibration citations remain.
P1 order equals `DOCS` in the 11c checker. No contradiction found.

### Notes ###
- Docs row: no second-model review. P1 excludes `graph/`, `wiki/` and the loose `labs/vinlab/*.md` notes.
