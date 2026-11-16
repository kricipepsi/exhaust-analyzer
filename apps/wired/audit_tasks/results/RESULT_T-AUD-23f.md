# Result — T-AUD-23f

## Status
completed

## Summary
Verified all **24** root code-audit claims in [T-AUD-23f.txt](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23f.txt) (`EF-001`–`EF-005` in [ecu_fault.json](file:///C:/4DApp/.agy/T-AUD-23f/labs/comlab/registry/rules/ecu_fault.json) and `NF-001`–`NF-002` in [no_fault.json](file:///C:/4DApp/.agy/T-AUD-23f/labs/comlab/registry/rules/no_fault.json)), appending **1** new source (`S041`) to [sources.csv](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/sources.csv) and **24** verdicts (`CONFIRMED=8`, `CONTRADICTED=10`, `PARTLY=6`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) without altering any existing rows.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T10:42:25Z` | `2026-11-16T10:50:48Z` | `8.4` | `ABSENT` |

## Files changed
- Modified: [sources.csv](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/sources.csv) (+1 row: `S041`; 0 lines removed)
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+24 rows for all 24 scope claims; 0 lines removed)
- Created: [S041.md](file:///C:/4DApp/.agy/T-AUD-23f/labs/gaslab/audit_tasks/wikiaudit/sources/S041.md) (Delaware Division of Motor Vehicles OBD-II generic DTC list, `PRIMARY_REGULATOR`)
- Created: [T-AUD-23f.md](file:///C:/4DApp/.agy/T-AUD-23f/apps/wired/audit_tasks/progress_notes/T-AUD-23f.md)
- Created: [RESULT_T-AUD-23f.md](file:///C:/4DApp/.agy/T-AUD-23f/apps/wired/audit_tasks/results/RESULT_T-AUD-23f.md)
- Temporary `labs/gaslab/audit_tasks/wikiaudit/search/` directory deleted per R3.

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23f.txt` (`VERDICTS FAIL 24 error(s)`), P3 scopes (`T-GASA-17`, `T-AUD-23a`, `T-AUD-23b`, `T-AUD-23d`, `T-AUD-23e`), plus inspection of `claims_comlab.csv`, `ecu_fault.json`, `no_fault.json`, `perception_contradiction.py`, and `sources/S002.md`–`S040.md`.
- Firecrawl searches (`--sources web --json`) and scrape of `S041.md`.
- Python CSV append script adding `S041` to `sources.csv` and 24 verdicts to `verdicts.csv`, and removing `search/`.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23f.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`
  3. `git diff` removed-line count (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23f.txt`):**
  ```text
  verdicts CONFIRMED=8 CONTRADICTED=10 PARTLY=6
  retired 0 of 24 scope claims (retired.csv)
  sources 38 primary 11
  VERDICTS OK scope=T-AUD-23f.txt claims 24
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`, `T-AUD-23d.txt`, `T-AUD-23e.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  VERDICTS OK scope=T-AUD-23e.txt claims 28
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `sources.csv`, `verdicts.csv`, `sources/S041.md`, `T-AUD-23f.md`, and `RESULT_T-AUD-23f.md` changed; no `search/` directory remains.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23f.txt claims 24` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the five P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 24-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23f.md](file:///C:/4DApp/.agy/T-AUD-23f/apps/wired/audit_tasks/progress_notes/T-AUD-23f.md) (`UNSOURCED=0`, 24-row table, 5 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only scoped files + note/result present, no `search/`) |

## Decisions the task did not specify
- **Source reuse and `S041` addition:** Reused existing `S002` (`PRIMARY_LAW`, `1 ± 0.03` lambda), `S011` (`PRIMARY_LAW`, `CO + CO2 >= 6 %` dilution floor), `S014` (`PRIMARY_STANDARD`, OIML R 99 CO MPE `±0.06 %`), `S023` (`TRADE`, healthy idle 5-gas band), `S028` (`TRADE`, near-0 ppm idle NOx), `S029` (`OEM`, Toyota `±20 %` normal / `±35 %` P0171/P0172), `S030` (`TRADE`, `±10 %` STFT / `5–8 %` LTFT), `S037` (`OEM`, Ford `LONGFT > 25 %, SHRTFT > 1 %` P0171 and `-5% to 5%` STFT entry), `S038` (`TRADE`, `1–2 %` combustion + `±2 %` wideband error), and `S040` (`TRADE`, `±5 %` analyser Lambda and `16.34 %` healthy `CO+CO2+O2` sum) per R1; added `S041` (`PRIMARY_REGULATOR`, Delaware DMV generic DTC list defining `6 = COMPUTER AND AUXILIARY OUTPUTS` / `P0600-P0699`).
- **Two further Firecrawl scrapes skipped after credits exhausted:** After 4 search calls and the `S041.md` PDF scrape, Firecrawl credits reached `0` (`-7 / 1,000`), so two additional trade/manual scrapes failed on insufficient credits and all remaining claims were adjudicated using `S041` plus `S001`–`S040`.

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S040`) and `verdicts.csv` (`W0118`–`CK0672`) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/sources.csv labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `labs/gaslab/audit_tasks/wikiaudit/sources/S041.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23f.md`, and `apps/wired/audit_tasks/results/RESULT_T-AUD-23f.md`.

## Remaining risks or uncertainties
- `CK0536`, `CK0538`, `CK0543`–`CK0546` rely on `TRADE` 5-gas diagnostic references (`S023`, `S028`, `S032`, `S034`, `S035`, `S040`) rather than OEM factory emissions charts, and trade guides differ on exact CO2/HC/O2 idle edges (all recorded in `Disputes`).
- `CK0378`/`CK0379`/`CK0383`/`CK0384` compare generic ECU saturation rules against Toyota (`S029`) and Ford (`S037`) OEM calibration thresholds, which vary across OEMs.
