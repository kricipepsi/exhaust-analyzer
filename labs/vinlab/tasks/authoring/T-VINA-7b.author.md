# T-VINA-7b — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C6_20261017.md` F-C6-7; `labs/vinlab/vinlab/decoder.py::validate_vin_checksum`; wiki 10
§10.3. Survey and rehearsal: `C:/4DApp/recheck/T-VINA-7b/` (`market_census*.py`, read-only over the Nio registry).

### Verified context ###
1. **Census, 750,354 unique petrol VINs** (Nio files 1-3): today `10,334` rejected. Region rule alone (enforce iff
   `vin[0]` in 1-5, no dummy bypass): `474` rejected, `346` NA VINs newly rejected. Observed (`market_census.py`).
2. **The 346 by position 9:** `0` on 3HG 134, 1C4 116, 1HG 43 (293); letters (L, A, H, C, Z) on most of the rest.
   With the dummy bypass kept: `134` rejected; `6` newly rejected (3VW 2, 4JG 2, 5UX 1, 546 1), one of them the
   pinned `4JG1631541A010177` (`test_type_code_year.py`). Observed (`market_census_pos9.py`, `_r2.py`).
3. **Union with the country bypass:** `128` rejected; `10,206` non-NA VINs gain a decode; `0` newly rejected.
   `3N1` (Nissan Mexico) is 95 of the 128 and fails today too. Observed (`market_census_r3.py`).
4. **Rehearsal** (restored): vinlab `393 → 403 passed, 8 skipped`; step 2 `67 passed, 2 skipped`, base `6 failed`;
   mutants: region 1-4 `1 failed`, country bypass dropped `1 failed`, dummy bypass dropped `2 failed`; wired `113`,
   ui `70`, dnalab `27`, comlab `508 passed, 4 skipped` (equal); ruff clean; the patched decoder rejects `128`
   registry VINs (census flips `{}`); `2 files changed, 17 insertions(+), 5 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Add the ISO 3780 region test; keep the country bypass and the `0` dummy.** Lost: the audit's full ask (region
  only, `0` enforced), which rejects 346 real registry cars; and region-plus-dummy without the country test, which
  rejects 6 real cars (NA plants of European makers). The country test's "US WMI filed as GERMANY" is information for
  this market, not an error.
- **No new grade or flag.** Lost: a PARTIAL for an unchecked digit (not asked; no consumer).
- **`3N1` not added to the OPSI corrupt prefixes here.** Lost: 95 more decodes; it needs its own look (registered as
  this row's follow-up, not a row yet).
- Plan NONE, difficulty 3 (a gate change with a data ruling, fully rehearsed). Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `403 passed, 8 skipped`; `113 passed`; `70 passed` |
| step 2 | SIMULATED | `67 passed, 2 skipped`; base `6 failed, 61 passed, 2 skipped` |
| step 3 | SIMULATED | ruff `All checks passed!`; `2 files changed, 17 insertions(+), 5 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-7b: a non-NA ISO 3780 region skips the check digit (registry rejections 10,334 → 128, none new; F-C6-7).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (facts 1-4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-3 and R3 · cold read: not triggered (scripted) · no finding.

### Correction history ###
(none)
