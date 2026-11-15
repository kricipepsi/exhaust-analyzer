# Result — T-AUD-23b

## Status
completed

## Summary
Verified all **29** root code-audit claims in [T-AUD-23b.txt](file:///C:/4DApp/.agy/T-AUD-23b/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23b.txt) (covering O2 sensors, coolant temperature thermistor resistance/preconditions, MAF/VE baselines, and exhaust-gas/analyser bounds), appending **15** new sources (`S014`–`S028`) to [sources.csv](file:///C:/4DApp/.agy/T-AUD-23b/labs/gaslab/audit_tasks/wikiaudit/sources.csv) and **29** verdicts (`CONFIRMED=5`, `CONTRADICTED=9`, `PARTLY=15`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23b/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) without modifying any existing rows.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T21:48:00Z` | `2026-11-15T22:06:29Z` | `18.5` | `ABSENT` |

## Files changed
- Modified: [sources.csv](file:///C:/4DApp/.agy/T-AUD-23b/labs/gaslab/audit_tasks/wikiaudit/sources.csv) (+15 rows: `S014`–`S028`; 0 lines removed)
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23b/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+29 rows for all 29 scope claims; 0 lines removed)
- Created: `labs/gaslab/audit_tasks/wikiaudit/sources/S014.md`–`S028.md` (15 cited sources: `OIML R 99`, `Bosch NTC M12`, `Bosch LSU 4.9`, `Toyota RAV4 P0420`, `Bridge Analyzers`, `Gears Magazine`, `ALLDATA`, `Fluke`, `Wikipedia Volumetric_efficiency`, `Walker Exhaust`, `Underhood Service`, `Apex Tech Nation P0118`, `Apex Tech Nation O2`, `CARB 13 CCR 1968.2`, `Crypton NOx`)
- Created: [T-AUD-23b.md](file:///C:/4DApp/.agy/T-AUD-23b/apps/wired/audit_tasks/progress_notes/T-AUD-23b.md)
- Created: [RESULT_T-AUD-23b.md](file:///C:/4DApp/.agy/T-AUD-23b/apps/wired/audit_tasks/results/RESULT_T-AUD-23b.md)
- Temporary `labs/gaslab/audit_tasks/wikiaudit/search/` directory and uncited draft scrapes deleted per R3.

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23b.txt`, `scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, plus claim CSV inspection.
- Firecrawl searches (`--sources web --json`) and scrapes (`S014.md`–`S028.md`).
- Python validation/append script adding `S014`–`S028` to `sources.csv` and 29 verdicts to `verdicts.csv`, after removing uncited scrapes and `labs/gaslab/audit_tasks/wikiaudit/search/`.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23b.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt` and `check_verdicts.py --scope scope/T-AUD-23a.txt`
  3. `git diff` removed-line check (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23b.txt`):**
  ```text
  verdicts CONFIRMED=5 CONTRADICTED=9 PARTLY=15
  sources 25 primary 10
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  ```
- **Step 2 (`T-GASA-17.txt` and `T-AUD-23a.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `sources.csv`, `verdicts.csv`, `sources/S014.md`–`S028.md`, `T-AUD-23b.md`, and `RESULT_T-AUD-23b.md` changed; no `search/` directory remains.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23b.txt claims 29` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints P3 (`T-GASA-17.txt` claims 20, `T-AUD-23a.txt` claims 25) | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 29-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23b.md](file:///C:/4DApp/.agy/T-AUD-23b/apps/wired/audit_tasks/progress_notes/T-AUD-23b.md) (`UNSOURCED=0`, 29-row table, 7 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only scoped files + note/result present, no `search/`) |

## Decisions the task did not specify
- **Source hierarchy and renumbering (`S014`–`S028`):** Used `PRIMARY_STANDARD` (`S014` OIML R 99), `PRIMARY_LAW` (`S027` CARB 13 CCR 1968.2), and `OEM` (`S015`–`S017` Bosch/Toyota) wherever free access existed; used `TRADE` (`S018`–`S021`, `S023`–`S026`, `S028`) and `SECONDARY` (`S022` Wikipedia `Volumetric_efficiency`, `S012` cross-ref) for workshop thresholds and boosted VE > 100%, disclosing source kind in `note` per R5 and renumbering kept files sequentially from `S014` after deleting uncited scrapes per R3.
- **Wide input bounds (`RK0268`, `RK0269`, `RK0275`, `RK0362`, `RK0365`, `RK0416`, `CK0189`, `RK0087`):** Marked `PARTLY` per R4 with physical sensor/combustion limits cited in `source_value`.

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S013`) and `verdicts.csv` (`W0118`–`CK1396`) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/sources.csv labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `labs/gaslab/audit_tasks/wikiaudit/sources/S014.md`–`S028.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23b.md`, and `apps/wired/audit_tasks/results/RESULT_T-AUD-23b.md`.

## Remaining risks or uncertainties
- Five claims (`CK0432`, `CK0537`, `CK0547`, `CK1326`, `RK0410` and workshop O2/MAF/VE thresholds) rely on `TRADE` sources or `SECONDARY` (`S022` for boosted VE > 100%) because OEM workshop manuals across arbitrary makes and paywalled SAE standards are not freely downloadable; verdicts remain fully documented and reproducible from the saved `S014`–`S028` texts.
