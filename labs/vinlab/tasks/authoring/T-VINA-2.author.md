# T-VINA-2 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Finding:** F-C6-3 rest (`audit/reports/R1_C6_20261017.md`): "European VINs that do not code the year there
   (Mercedes) all decode as 2001"; T-VINA-1 left the probes `WDB1240261A102470`, `WDD1770441J098476` red.
2. **Measured (P3)** on the 1,364 real VINs (`recheck/T-VINA-2/measure*.py`): 137 decode as 2001 (VF1 38, WDB 24,
   WME 13, VF7 7, WDD 6 …). The check digit does not separate the groups (`WDB1240261A102470` passes mod-11 by
   chance; `validate_vin_checksum` bypasses every German WMI). Positions 4-9 numeric does: 47 of 47 Mercedes/smart
   VINs with digits there have position 10 = `1`; the 6 with letters carry year codes.
3. **Rehearsed (P2)** on `recheck/T-VINA-2/rh3/vinlab` (`make_rh.py`): vinlab `224 passed, 8 skipped`, new file
   `8 passed`, probes `1 failed, 7 passed`, M1 and M2 `3 failed` each; dnalab 27, wired 41, ui 30 against the copy.
4. **Base (P1)** on `02ebfba` (fix/T-VINA-8): vinlab `216 passed, 8 skipped`; probes `3 failed, 5 passed`.

### Rulings and the tradeoff that lost ###
- The numeric type-code test. Lost: the check digit (P3: a 1-in-11 coincidence passes, and European VINs carry no
  check digit by rule); a blanket WMI rule (it would drop the North American years).
- Renault `VF1` left out → T-VINA-9. Lost: including it on the corpus pattern alone (no 1990s letters in 103 VINs):
  the suite documents `VF1CB05CF25935016` as a 2002 Clio, so a source must settle it.
- The set is the measured WMIs; `WDF` (no VIN in the corpus) is out. Lost: the whole Mercedes list from `wmi.csv`
  (the US-built `4JG`, `55S` carry years).
- Plan NONE, difficulty 2: a measured 2-line rule, rehearsed.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `make_rh.py` copy: `224 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `8 passed` |
| step 3 | SIMULATED | copy on `PYTHONPATH`: `27 passed`, `41 passed`, `30 passed` |
| step 4 | SIMULATED | copy on `PYTHONPATH`: `1 failed, 7 passed` |
| step 5 | DEFERRED | the doc edit is R5's; observable: at least 2 `_TYPE_CODE_WMIS` lines |
| step 6 | DEFERRED | ruff and the commit |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-2: Mercedes/smart VINs with a numeric type code at 4-9 decode with model_year None; NA form keeps the year.

### Cold read ###
own pass 2026-11-04: anchors grep 1 each · P1 on the base · P2 on the copy · traceability: criteria 1-5 → steps 1-6 ·
JUDGEMENT criteria: 0.
cold read 2026-11-04: skipped (Plan: NONE, difficulty 2, rehearsed edits).

### Correction history ###
- **01 (2026-11-04, Cowork review of round 1; not accepted).** Re-run: vinlab `224 passed, 8 skipped`, probes
  `1 failed, 7 passed`, all lab suites at their counts (comlab 526/4/2 with `--continue-on-collection-errors`, dtclab
  590, gaslab 208, obdlab 388, symptomlab 72); edits equal the rehearsal modulo CRLF. Codex (second_review.py, peak →
  codex) APPROVE WITH CORRECTIONS: F1 the non-Mercedes test misses the WMI condition UPHELD (R6.2; rehearsed
  `_resolve_year("VF11234562A123456", {})` → `(2002, None)`); F2 "plant code" unsourced UPHELD (R6.1; my P3 wording).
