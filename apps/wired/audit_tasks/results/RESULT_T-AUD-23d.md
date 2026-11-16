# Result — T-AUD-23d

## Status
completed

## Summary
Verified all **29** root code-audit claims in [T-AUD-23d.txt](file:///C:/4DApp/.agy/T-AUD-23d/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23d.txt) (MF, RM, LC, and CF rule gates: fuel trims, exhaust gases, lambda, MAP, and MAF), appending **8** new sources (`S029`–`S036`) to [sources.csv](file:///C:/4DApp/.agy/T-AUD-23d/labs/gaslab/audit_tasks/wikiaudit/sources.csv) and **29** verdicts (`CONFIRMED=7`, `CONTRADICTED=14`, `PARTLY=8`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23d/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) without modifying any existing rows.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T09:19:13Z` | `2026-11-16T09:30:52Z` | `11.7` | `ABSENT` |

## Files changed
- Modified: [sources.csv](file:///C:/4DApp/.agy/T-AUD-23d/labs/gaslab/audit_tasks/wikiaudit/sources.csv) (+8 rows: `S029`–`S036`; 0 lines removed)
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23d/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+29 rows for all 29 scope claims; 0 lines removed)
- Created: `labs/gaslab/audit_tasks/wikiaudit/sources/S029.md`–`S036.md` (8 cited sources: Toyota RAV4 2AZ-FE Repair Manual P0171/P0172, AA1Car Fuel Trim, MOTOR Trouble Shooter June 2018, Smog Tech Institute 5-Gas, MOTOR Cat Smarts May 1999, Underhood Service Engine Analyzers, AVI OnDemand 5-Gas, The Tuning School Good Data)
- Created: [T-AUD-23d.md](file:///C:/4DApp/.agy/T-AUD-23d/apps/wired/audit_tasks/progress_notes/T-AUD-23d.md)
- Created: [RESULT_T-AUD-23d.md](file:///C:/4DApp/.agy/T-AUD-23d/apps/wired/audit_tasks/results/RESULT_T-AUD-23d.md)
- Temporary `labs/gaslab/audit_tasks/wikiaudit/search/` directory and uncited draft scrapes deleted per R3.

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23d.txt`, `scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, plus `claims_comlab.csv` and rule JSON inspection.
- Firecrawl searches (`--sources web --json`) and scrapes (`S029.md`–`S036.md`).
- Python quote-check and CSV append script adding `S029`–`S036` to `sources.csv` and 29 verdicts to `verdicts.csv`.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23d.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, and `scope/T-AUD-23b.txt`
  3. `git diff` removed-line check (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23d.txt`):**
  ```text
  verdicts CONFIRMED=7 CONTRADICTED=14 PARTLY=8
  retired 0 of 29 scope claims (retired.csv)
  sources 33 primary 10
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `sources.csv`, `verdicts.csv`, `sources/S029.md`–`S036.md`, `T-AUD-23d.md`, and `RESULT_T-AUD-23d.md` changed; no `search/` directory remains.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23d.txt claims 29` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the three P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 29-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23d.md](file:///C:/4DApp/.agy/T-AUD-23d/apps/wired/audit_tasks/progress_notes/T-AUD-23d.md) (`UNSOURCED=0`, 29-row table, 6 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only scoped files + note/result present, no `search/`) |

## Decisions the task did not specify
- **Source reuse and selection (`S002`, `S019`, `S020`, `S023` + `S029`–`S036`):** Reused existing `S002` (`PRIMARY_LAW` for `CK0611`), `S019` (`±10 %` LTFT), `S020` (`2–7 g/s` idle MAF), and `S023` (working-cat vs unlit-cat CO2/HC/O2) per R1; added `S029` (`OEM` Toyota P0171/P0172 manual) and `S030`–`S036` (`TRADE` training/analyser/OEM-recall texts) for healthy STFT/LTFT bands, GDI HPFP leak LTFT, combustion-loss CO2, catalyst O2 shutdown, misfire HC, idle/loaded NOx, and idle MAP kPa.
- **Fuel-trim boundary split (`±10 %` vs `±8 %` / `±5 %` / `3 %`):** Confirmed `±10.0 %` LTFT (`CK0351`, `CK0441`, `CK0612`) per `S019`/`S030` trade boundary (`> ±10 %`), and contradicted `±8.0 %`, `±5.0 %`, and `3.0 %` because they sit at/inside the healthy `±8 %` / `< ±10 %` (`S030`/`S019`) and `±20 %` combined (`S029`) normal bands.

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S028`) and `verdicts.csv` (`W0118`–`CK1396`) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/sources.csv labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `labs/gaslab/audit_tasks/wikiaudit/sources/S029.md`–`S036.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23d.md`, and `apps/wired/audit_tasks/results/RESULT_T-AUD-23d.md`.

## Remaining risks or uncertainties
- Exhaust-gas and workshop fuel-trim/MAP thresholds rely on `TRADE` sources (`S019`, `S020`, `S023`, `S030`–`S036`) alongside `S029` (`OEM`) and `S002` (`PRIMARY_LAW`) because vehicle-wide OEM 5-gas cutpoints do not exist as a single standard; all verdicts are traceable to the committed `sources/` texts and `Disputes`.
