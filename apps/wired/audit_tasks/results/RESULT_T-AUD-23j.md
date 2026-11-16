# Result — T-AUD-23j

## Status
completed

## Summary
Verified all **24** root code-audit claims in [T-AUD-23j.txt](file:///C:/4DApp/.agy/T-AUD-23j/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23j.txt) (`VL-001`–`VL-003` in [vacuum_leak.json](file:///C:/4DApp/.agy/T-AUD-23j/labs/comlab/registry/rules/vacuum_leak.json), `OV-001`–`OV-004` in [overheating.json](file:///C:/4DApp/.agy/T-AUD-23j/labs/comlab/registry/rules/overheating.json), `IF-001`–`IF-004` in [ignition_fault.json](file:///C:/4DApp/.agy/T-AUD-23j/labs/comlab/registry/rules/ignition_fault.json), `EL-001`–`EL-003` in [exhaust_leak.json](file:///C:/4DApp/.agy/T-AUD-23j/labs/comlab/registry/rules/exhaust_leak.json), and `II-001`–`II-002` in [invalid_input.json](file:///C:/4DApp/.agy/T-AUD-23j/labs/comlab/registry/rules/invalid_input.json)), appending **24** verdicts (`CONFIRMED=5`, `CONTRADICTED=11`, `PARTLY=8`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23j/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) using existing authoritative sources (`S001`, `S011`, `S014`, `S023`, `S030`, `S032`, `S034`, `S036`, `S037`, `S041`, cross-referenced with `S005`, `S009`, `S018`, `S019`, `S025`, `S029`, `S033`, `S035`, `S040`) without altering any existing row in `sources.csv` or `verdicts.csv`.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T12:32:28Z` | `2026-11-16T12:38:03Z` | `5.6` | `ABSENT` |

## Files changed
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23j/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+24 rows for all 24 scope claims; 0 lines removed)
- Created: [T-AUD-23j.md](file:///C:/4DApp/.agy/T-AUD-23j/apps/wired/audit_tasks/progress_notes/T-AUD-23j.md)
- Created: [RESULT_T-AUD-23j.md](file:///C:/4DApp/.agy/T-AUD-23j/apps/wired/audit_tasks/results/RESULT_T-AUD-23j.md)

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23j.txt` (`VERDICTS FAIL 24 error(s)`), P3 scopes (`T-GASA-17`, `T-AUD-23a`, `T-AUD-23b`, `T-AUD-23d`, `T-AUD-23e`, `T-AUD-23f`, `T-AUD-23g`, `T-AUD-23h`, `T-AUD-23i`), `firecrawl --status`, test `firecrawl search` (402 credits exhausted; temporary `search/` removed), and inspection of `claims_comlab.csv`, the five rule JSONs, `verdicts.csv`, and `sources/S001.md`–`S041.md`.
- Python CSV append script adding 24 verdicts to `verdicts.csv` in UTF-8 with LF line endings (plus quote fix on `CK0437` in `S011.md`).
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23j.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`, `scope/T-AUD-23g.txt`, `scope/T-AUD-23h.txt`, `scope/T-AUD-23i.txt`
  3. `git diff` removed-line count (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23j.txt`):**
  ```text
  verdicts CONFIRMED=5 CONTRADICTED=11 PARTLY=8
  retired 0 of 24 scope claims (retired.csv)
  sources 38 primary 11
  VERDICTS OK scope=T-AUD-23j.txt claims 24
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`, `T-AUD-23d.txt`, `T-AUD-23e.txt`, `T-AUD-23f.txt`, `T-AUD-23g.txt`, `T-AUD-23h.txt`, `T-AUD-23i.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  VERDICTS OK scope=T-AUD-23e.txt claims 28
  VERDICTS OK scope=T-AUD-23f.txt claims 24
  VERDICTS OK scope=T-AUD-23g.txt claims 28
  VERDICTS OK scope=T-AUD-23h.txt claims 30
  VERDICTS OK scope=T-AUD-23i.txt claims 25
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `verdicts.csv`, `T-AUD-23j.md`, and `RESULT_T-AUD-23j.md` changed; no `search/` directory exists.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23j.txt claims 24` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the nine P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 24-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23j.md](file:///C:/4DApp/.agy/T-AUD-23j/apps/wired/audit_tasks/progress_notes/T-AUD-23j.md) (`UNSOURCED=0`, 24-row table, 6 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only `verdicts.csv` + note/result changed, no `search/`) |

## Decisions the task did not specify
- **Source reuse without new scrapes (`S001`–`S041`):** `firecrawl --status` showed `-7 / 1,000` credits at session start and a test `firecrawl search` returned HTTP `402`; per R1, all 24 claims were verified using existing `S001` (`PRIMARY_REGULATOR`), `S011` (`PRIMARY_LAW`), `S014` (`PRIMARY_STANDARD`), `S023` (`TRADE`), `S030` (`TRADE`), `S032` (`TRADE`), `S034` (`TRADE`), `S036` (`TRADE`), `S037` (`OEM`), and `S041` (`PRIMARY_REGULATOR`), cross-referenced with `S005`, `S009`, `S018`, `S019`, `S025`, `S029`, `S033`, `S035`, and `S040`.
- **Stronger-source precedence on `CK0689` (`shrtft1 ≥ 10 %`), `CK0597`/`CK0606` (`ect_c > 105 °C`):** Per R5, `S037` (`OEM`) governed over `TRADE` heuristics where they disagreed (`S037` closed-loop STFT entry up to `-9..+11 %` / `-13..+18 %` vs `S030` `+10 %` idle lean heuristic; `S037` `70–110 °C` operating ECT band vs `S036` `82.2–104.4 °C` / `S025` `90.6–98.9 °C`).
- **`CK0437` (`co2 < 5.0 %` in `II-002` open-air contamination):** Judged `CONFIRMED` against `S011` (`PRIMARY_LAW`, `40 CFR 85.2215` `CO + CO2 < 6 %` dilution void threshold, `16.7 %` away in `<` direction when `CO ≈ 0` in air-contaminated samples), rather than `S032` (`< 12 %` combustion loss used for `NS-001`/`NS-002` cranking in `T-AUD-23i`).

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S041`, 38 rows) and `verdicts.csv` (`W0118`–`CK0588`, 238 rows) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `apps/wired/audit_tasks/progress_notes/T-AUD-23j.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-23j.md`.

## Remaining risks or uncertainties
- Specific OEM coolant overheating alarm thresholds (`> 105 °C` / `> 115 °C`), cooling-idle RPM target curves, and full SAE J2012 `P0324` wording could not be fetched externally due to Firecrawl credit exhaustion (`402`); those claims rely on `S037` (`70–110 °C` / `115.6–127 °C` monitor bands, `CHT > 270 °F` `P1299`), `S001`/`S009` (`450–1,500 rpm` natural idle), and `S041`/`S037` (`P0325–P0334`, `P032A–P033D`).
- Fourteen verdicts (`CK0675`–`CK0677`, `CK0682`–`CK0683`, `CK0687`–`CK0688`, `CK0410`, `CK0420`, `CK0428`, `CK0401`, `CK0406`–`CK0407`, `CK0433`) rely on `TRADE` sources (`S023`, `S030`, `S032`, `S034`, `S036`) as primary cited sources.
