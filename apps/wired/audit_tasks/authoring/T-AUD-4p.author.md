# T-AUD-4p — authoring sidecar (Windows Cowork, 2026-11-06)

Survey: `C:/4DApp/recheck/scratch/survey_T-AUD-4p.md`. Rehearsal: `C:/4DApp/recheck/T-AUD-4p/` (`apply_fix.py`,
`rehearsal.patch`, `tests/`, `cw/corpus_fix.json`).

### Verified context ###
1. **F-C4-5 holds, narrowed.** `trim_analytics_gate` now has a v2 reader (`integration_shim.py:394`); 15 of 16 fields do
   not. Observed (survey § 3).
2. **Five fields have no reader on any path** (P1): `grep -rn` over `apps`, `labs/comlab`, `labs/obdlab`,
   `labs/gaslab` shows only the producing lab, the mirror, the composition mapping and tests. Observed.
3. **The mirrors are plain `BaseModel`** (no `ConfigDict`), so fixtures that pass dropped keys still validate. Observed:
   comlab 525 = 531 − 6 removed bound cases, no other change.
4. **Rehearsal** (restored): new file base `4 failed`, fix `4 passed`; wired 85 → 89; comlab 525/4/2; gaslab 208,
   obdlab 391, dtclab 590, vinlab 376, dnalab 27, symptomlab 72; registry 5F/502P (= base); ruff clean; corpus 0/314
   differ. Observed.

### Rulings and the tradeoff that lost ###
- **Drop the five unread fields from the COMLab mirror** (rule 4: a field ships only with a named consumer). Lost:
  wiring `high_idle_co2/o2/nox` into `_PID_DISPATCH` (no registry rule reads them, so the wire would still be dead) and
  keeping `maf_status/map_status` for a future VE-weight consumer (re-add them with that consumer).
- **Label the ten v1-only fields; do not port the v1 gates here.** Lost: making each named consumer reachable on the
  default path (the report's "expected"). Porting seven v1 gates into registry rules is design work with verdict
  movement; it is registered as T-AUD-4t.
- Plan NONE, difficulty 2 (`--model claude-sonnet-5-5 --effort medium`): quoted, rehearsed, 0 verdict movement. Code
  row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `4 passed`; wired `89 passed` |
| step 2 | SIMULATED | comlab `525 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | `corpus 314`; `differ 0` |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4p: no COMLab mirror field claims a consumer it lacks; five unread fields dropped, ten labelled v1-only.

### Cold read ###
own pass 2026-11-06: P1-P5 measured · every `apply_fix.py` literal matched once on the base · counts: wired 85 + 4 =
89, comlab 531 − 6 = 525 · traceability: criteria 1-4 → steps 1-4 · 1c hit in R3 ("Each … becomes <one text>" vs `apply_fix.py`'s suffixed and added comments): R3 patched to name `apply_fix.py`'s comments as the final text; checks CLEAN again.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (R3); 0 findings, 0 patched — 20994 tok, 4 calls.

### Correction history ###
(none)
