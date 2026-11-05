### Gate rehearsal ###
| step | status | evidence |
|---|---|---|
| step 1 | SIMULATED | `recheck/T-AUD-11b/check_report.py` on `sample_good.md` (8 sections, 1 finding): `sections 8/8, findings 1, refs ok 2/2`, `REPORT OK`; on `sample_bad.md` (bad tag, no refs): `REPORT BAD`, exit 1 |
| step 2 | DEFERRED | `git diff --name-only HEAD~1 HEAD` lists only the report |
| step 3 | DEFERRED | spec commit + implementer commit; porcelain shows only note and RESULT |

### Progress hook ###
Reviewer: re-derive the findings; confirmed drifts → a DNALab docs fix row (as T-AUD-12 for SymptomLab).

### Cold read ###
Derived from the accepted pilot T-AUD-11a by fixed substitutions (lab, paths, P1/P2/P3, branch base `3dfc3ea`) plus
the two calibration rules from REVIEW_T-AUD-11a. Grep for `symptomlab` and stray `11a` references: only the pilot
citation and the base branch remain, as intended. P1 order equals `DOCS` in the 11b checker. No contradiction found.

### Notes ###
- Docs row: no second-model review. P1 excludes `graph/` (generated copies) and `wiki/`, as the pilot did.
