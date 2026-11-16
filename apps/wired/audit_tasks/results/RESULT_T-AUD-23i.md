# Result — T-AUD-23i

## Status
completed

## Summary
Verified all **25** root code-audit claims in [T-AUD-23i.txt](file:///C:/4DApp/.agy/T-AUD-23i/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23i.txt) (`NS-001`–`NS-005` in [non_starter.json](file:///C:/4DApp/.agy/T-AUD-23i/labs/comlab/registry/rules/non_starter.json)), appending **25** verdicts (`CONTRADICTED=14`, `PARTLY=11`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23i/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) using existing authoritative sources (`S001`, `S027`, `S030`, `S032`, `S040`, corroborated by `S009`, `S011`, `S019`, `S023`, `S025`, `S031`, `S034`, `S037`) without altering any existing row in `sources.csv` or `verdicts.csv`.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T11:42:09Z` | `2026-11-16T11:55:16Z` | `13.1` | `ABSENT` |

## Files changed
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23i/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+25 rows for all 25 scope claims; 0 lines removed)
- Created: [T-AUD-23i.md](file:///C:/4DApp/.agy/T-AUD-23i/apps/wired/audit_tasks/progress_notes/T-AUD-23i.md)
- Created: [RESULT_T-AUD-23i.md](file:///C:/4DApp/.agy/T-AUD-23i/apps/wired/audit_tasks/results/RESULT_T-AUD-23i.md)

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23i.txt` (`VERDICTS FAIL 25 error(s)`), P3 scopes (`T-GASA-17`, `T-AUD-23a`, `T-AUD-23b`, `T-AUD-23d`, `T-AUD-23e`, `T-AUD-23f`, `T-AUD-23g`, `T-AUD-23h`), `firecrawl --status`, test `firecrawl search` (402 credits exhausted; temporary `search/` removed), and inspection of `claims_comlab.csv`, `non_starter.json`, `verdicts.csv`, and `sources/S001.md`–`S041.md`.
- Python CSV append script adding 25 verdicts to `verdicts.csv` in UTF-8 with LF line endings.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23i.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`, `scope/T-AUD-23g.txt`, `scope/T-AUD-23h.txt`
  3. `git diff` removed-line count (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23i.txt`):**
  ```text
  verdicts CONTRADICTED=14 PARTLY=11
  retired 0 of 25 scope claims (retired.csv)
  sources 38 primary 11
  VERDICTS OK scope=T-AUD-23i.txt claims 25
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`, `T-AUD-23d.txt`, `T-AUD-23e.txt`, `T-AUD-23f.txt`, `T-AUD-23g.txt`, `T-AUD-23h.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  VERDICTS OK scope=T-AUD-23e.txt claims 28
  VERDICTS OK scope=T-AUD-23f.txt claims 24
  VERDICTS OK scope=T-AUD-23g.txt claims 28
  VERDICTS OK scope=T-AUD-23h.txt claims 30
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `verdicts.csv`, `T-AUD-23i.md`, and `RESULT_T-AUD-23i.md` changed; no `search/` directory exists.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23i.txt claims 25` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the eight P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 25-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23i.md](file:///C:/4DApp/.agy/T-AUD-23i/apps/wired/audit_tasks/progress_notes/T-AUD-23i.md) (`UNSOURCED=0`, 25-row table, 4 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only `verdicts.csv` + note/result changed, no `search/`) |

## Decisions the task did not specify
- **Source reuse without new scrapes (`S001`–`S041`):** `firecrawl --status` showed `-7 / 1,000` credits at session start and a test `firecrawl search` returned HTTP `402`; per R1, all 25 claims were verified using existing `S001` (`PRIMARY_REGULATOR`), `S027` (`PRIMARY_LAW`), `S030` (`TRADE`), `S032` (`TRADE`), and `S040` (`TRADE`), corroborated by `S009`, `S011`, `S019`, `S023`, `S025`, `S031`, `S034`, and `S037`.
- **Open-loop `STFT` (`CK0557`, `CK0558`, `CK0570`, `CK0571` `[-1.0, 1.0] %`) vs `LTFT` (`CK0559`, `CK0560`, `CK0572`, `CK0573` `[-1.0, 1.0] %`):** `LTFT` was judged `CONTRADICTED` because `S030` and `S027` (`KAM`) confirm LTFT retains its prior-drive stored value across shut-off (`±5–10 %` normally or wider with faults) and `[-1.0, 1.0] %` overlaps healthy closed-loop trims; `STFT` was judged `PARTLY` because `S030` confirms `"no fuel trim adjustments are made"` (`0 %`) before closed loop, while giving no `±1.0 %` tolerance, showing a `25 %` STFT scan-tool reading at `0 rpm`, and overlapping healthy closed-loop STFT (`-5 to +5 %` `S037`, `-10 to +10 %` `S030`).
- **CO2 cranking/no-combustion (`CK0552`, `CK0556`, `CK0563`, `CK0568` `< 5 %`; `CK0579` `< 8 %`) and running misfire (`CK0554` `≥ 10 %`; `CK0566` `≥ 8 %`):** All 7 judged `PARTLY` against `S032` (`< 12 %` lack of combustion), `S011` (`CO + CO2 < 6 %` idle-test void), `S040` (`11.83 %` pre-cat / `15.37 %` post-cat for 1-cyl misfire on 6-cyl), and `S023` (`25 %` drop for 1-cyl misfire on 4-cyl) rather than `UNSOURCED` because Firecrawl `402` blocked new external searches.

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S041`) and `verdicts.csv` (`W0118`–`CK0508`, 213 rows) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `apps/wired/audit_tasks/progress_notes/T-AUD-23i.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-23i.md`.

## Remaining risks or uncertainties
- Specific cranking-only exhaust CO2 measurements (`< 5 %` / `< 8 %`), petrol cranking-RPM ranges (`150–300 rpm`), and rich-misfire CO2 floors (`≥ 8 %`) could not be fetched externally due to Firecrawl credit exhaustion (`402`); those claims rely on `S032` (`< 12 %`), `S011` (`CO+CO2 < 6 %`), `S040` (`11.83 %`), and `S001`/`S009`/`S031`/`S037` (`450–600 rpm` idle/monitor boundaries).
- `CK0552`, `CK0554`, `CK0556`–`CK0560`, `CK0563`, `CK0566`, `CK0568`, `CK0570`–`CK0573`, and `CK0579` rely on `TRADE` sources (`S030`, `S032`, `S040`) as primary cited sources.
