# Result — T-AUD-23e

## Status
completed

## Summary
Verified all **28** root code-audit claims in [T-AUD-23e.txt](file:///C:/4DApp/.agy/T-AUD-23e/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23e.txt) (`SF-001`–`SF-008` rule values in [sensor_fault.json](file:///C:/4DApp/.agy/T-AUD-23e/labs/comlab/registry/rules/sensor_fault.json): `lambda_perception_delta`, upstream/downstream O2 voltage, MAF, MAP, ECT, and STFT/LTFT gates), appending **4** new sources (`S037`–`S040`) to [sources.csv](file:///C:/4DApp/.agy/T-AUD-23e/labs/gaslab/audit_tasks/wikiaudit/sources.csv) and **28** verdicts (`CONFIRMED=3`, `CONTRADICTED=21`, `PARTLY=4`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23e/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) without altering any existing rows.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T10:07:36Z` | `2026-11-16T10:16:49Z` | `9.2` | `ABSENT` |

## Files changed
- Modified: [sources.csv](file:///C:/4DApp/.agy/T-AUD-23e/labs/gaslab/audit_tasks/wikiaudit/sources.csv) (+4 rows: `S037`–`S040`; 0 lines removed)
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23e/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+28 rows for all 28 scope claims; 0 lines removed)
- Created: `labs/gaslab/audit_tasks/wikiaudit/sources/S037.md`–`S040.md` (4 cited sources: Ford Motorcraft MY 2024–2025 OBD System Operation Summary, Hot Rod wideband lambda comparison test, Apex Tech Nation P0131 guide, MOTOR Magazine Feb 2010 exhaust gas analyser Lambda diagnostics)
- Created: [T-AUD-23e.md](file:///C:/4DApp/.agy/T-AUD-23e/apps/wired/audit_tasks/progress_notes/T-AUD-23e.md)
- Created: [RESULT_T-AUD-23e.md](file:///C:/4DApp/.agy/T-AUD-23e/apps/wired/audit_tasks/results/RESULT_T-AUD-23e.md)
- Temporary `labs/gaslab/audit_tasks/wikiaudit/search/` directory and uncited draft scrapes deleted per R3.

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23e.txt`, `scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, plus `claims_comlab.csv` and `sensor_fault.json` inspection.
- Firecrawl searches (`--sources web --json`) and scrapes (`S037.md`–`S040.md`).
- Python quote pre-verification and CSV append script adding `S037`–`S040` to `sources.csv` and 28 verdicts to `verdicts.csv`.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23e.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, and `scope/T-AUD-23d.txt`
  3. `git diff` removed-line check (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23e.txt`):**
  ```text
  verdicts CONFIRMED=3 CONTRADICTED=21 PARTLY=4
  retired 0 of 28 scope claims (retired.csv)
  sources 37 primary 10
  VERDICTS OK scope=T-AUD-23e.txt claims 28
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`, `T-AUD-23d.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `sources.csv`, `verdicts.csv`, `sources/S037.md`–`S040.md`, `T-AUD-23e.md`, and `RESULT_T-AUD-23e.md` changed; no `search/` directory remains.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23e.txt claims 28` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the four P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 28-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23e.md](file:///C:/4DApp/.agy/T-AUD-23e/apps/wired/audit_tasks/progress_notes/T-AUD-23e.md) (`UNSOURCED=0`, 28-row table, 6 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only scoped files + note/result present, no `search/`) |

## Decisions the task did not specify
- **Source reuse and selection (`S019`–`S021`, `S024`, `S027`, `S029`, `S030`, `S036` + `S037`–`S040`):** Reused existing `S019` (`~1 g/s per L` MAF), `S020` (`2–7 g/s` idle MAF), `S021` (`0.10–0.90 V` O2 switching), `S024` (`~0.7 V` healthy working-cat rear O2), `S027` (`PRIMARY_LAW` CARB `140 °F = 60.0 °C` stuck-cold ECT), `S029` (`OEM` Toyota `±20 %` normal combined fuel trim), `S030` (`TRADE` `±10 %` normal STFT), and `S036` (`30–50 kPa` idle MAP) per R1; added `S037` (`OEM` Ford OBD summary for UEGO target `±2 %` and FAOS bias `-0.083 / +0.087`), `S038` (`TRADE` Hot Rod wideband accuracy + combustion variance), `S039` (`TRADE` Apex Tech Nation P0131 `< 0.2 V` stuck-low & cold-start heater voltage), and `S040` (`TRADE` MOTOR Magazine `±5 %` healthy engine analyser Lambda).
- **`lambda_perception_delta` split (`±0.03` vs `±0.05`):** Contradicted `±0.03` as sitting inside combined healthy variation (`S040` `±5 %` analyser Lambda, `S038` `1–2 %` combustion + `±2 %` wideband, `S016` `1.016 ± 0.007` + `S014` `0.3 %` calc MPE) and tighter than `S037`'s `-0.083 / +0.087` OEM bias limit; marked `±0.05` (`CK0636`, `CK0637`) `PARTLY` against `S037` (`OEM`: above `±2 %` UEGO target and matching `<= 0.05` lack-of-movement, while OEM bias limit `-0.083 / +0.087` is `> 20 %` larger).

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S036`) and `verdicts.csv` (`W0118`–`CK0622`) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/sources.csv labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `labs/gaslab/audit_tasks/wikiaudit/sources/S037.md`–`S040.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23e.md`, and `apps/wired/audit_tasks/results/RESULT_T-AUD-23e.md`.

## Remaining risks or uncertainties
- Several trade-sourced boundaries (`S019`–`S021`, `S024`, `S030`, `S036`, `S038`–`S040`) are shop/diagnostic references rather than vehicle-wide OEM specs; OEM thresholds (`S029`, `S037`) and statutory text (`S027`) are cross-referenced in `Disputes`.
