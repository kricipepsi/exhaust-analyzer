# Result — T-AUD-23g

## Status
completed

## Summary
Verified all **28** root code-audit claims in [T-AUD-23g.txt](file:///C:/4DApp/.agy/T-AUD-23g/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23g.txt) (`CT-002`–`CT-008` in [cam_timing.json](file:///C:/4DApp/.agy/T-AUD-23g/labs/comlab/registry/rules/cam_timing.json)), appending **28** verdicts (`CONFIRMED=4`, `CONTRADICTED=14`, `PARTLY=10`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23g/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) using existing authoritative sources (`S028`, `S030`, `S032`, `S037`, with cross-references to `S001`, `S009`, `S018`, `S019`, `S023`, `S029`, `S033`, `S034`, `S035`) without altering any existing row in `sources.csv` or `verdicts.csv`.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T11:02:30Z` | `2026-11-16T11:15:19Z` | `12.8` | `ABSENT` |

## Files changed
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23g/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+28 rows for all 28 scope claims; 0 lines removed)
- Created: [T-AUD-23g.md](file:///C:/4DApp/.agy/T-AUD-23g/apps/wired/audit_tasks/progress_notes/T-AUD-23g.md)
- Created: [RESULT_T-AUD-23g.md](file:///C:/4DApp/.agy/T-AUD-23g/apps/wired/audit_tasks/results/RESULT_T-AUD-23g.md)

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23g.txt` (`VERDICTS FAIL 28 error(s)`), P3 scopes (`T-GASA-17`, `T-AUD-23a`, `T-AUD-23b`, `T-AUD-23d`, `T-AUD-23e`, `T-AUD-23f`), `firecrawl --status`, and inspection of `claims_comlab.csv`, `cam_timing.json`, `verdicts.csv`, and `sources/S017.md`–`S041.md`.
- Python CSV append script adding 28 verdicts to `verdicts.csv` in UTF-8 with LF line endings.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23g.txt`
  2. `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`
  3. `git diff` removed-line count (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23g.txt`):**
  ```text
  verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=10
  retired 0 of 28 scope claims (retired.csv)
  sources 38 primary 11
  VERDICTS OK scope=T-AUD-23g.txt claims 28
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`, `T-AUD-23b.txt`, `T-AUD-23d.txt`, `T-AUD-23e.txt`, `T-AUD-23f.txt`):**
  ```text
  VERDICTS OK scope=T-GASA-17.txt claims 20
  VERDICTS OK scope=T-AUD-23a.txt claims 25
  VERDICTS OK scope=T-AUD-23b.txt claims 29
  VERDICTS OK scope=T-AUD-23d.txt claims 29
  VERDICTS OK scope=T-AUD-23e.txt claims 28
  VERDICTS OK scope=T-AUD-23f.txt claims 24
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `verdicts.csv`, `T-AUD-23g.md`, and `RESULT_T-AUD-23g.md` changed; no `search/` directory exists.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23g.txt claims 28` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the six P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 28-verdict table, searches for any `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23g.md](file:///C:/4DApp/.agy/T-AUD-23g/apps/wired/audit_tasks/progress_notes/T-AUD-23g.md) (`UNSOURCED=0`, 28-row table, 5 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only `verdicts.csv` + note/result changed, no `search/`) |

## Decisions the task did not specify
- **Source reuse without new scrapes (`S001`–`S041`):** `firecrawl --status` showed `-7 / 1,000` credits at session start, preventing new web scrapes; per R1, all 28 claims were verified using existing `S028` (`TRADE`), `S030` (`TRADE`), `S032` (`TRADE`), and `S037` (`OEM`), cross-referenced against `S001`, `S009`, `S018`, `S019`, `S023`, `S029`, `S033`, `S034`, and `S035`.
- **`CT-005` `[-5, 5]` trim-band split (`STFT` vs `LTFT`):** `CK0321`, `CK0323`, and `CK0324` (`stft_b1` in `[-5, 5]` as `"trims near zero"`) were marked `CONFIRMED` against `S037` (`Ford OEM` `Short Term Fuel Trim Range -5% to 5%`) and `S019` (cam issues keep trims normal absent misfire), whereas `CK0322`, `CK0325`, and `CK0326` (`ltft_b1` in `[-5, 5]`) were marked `PARTLY` because `S030` sets good aging LTFT at `5–8 %` (`±8 %` normal) and `S019` `< ±10 %` (`> 20 %` wider than `±5 %`).
- **`CT-008` `co2 in_range [12.5, 13.0]` split (`CK0338` vs `CK0339`):** `CK0338` (`12.5 %` lower edge) was marked `CONTRADICTED` because a `12.5 %` floor rejects severe `< 12 %` lack-of-combustion readings (`S032`) and sits inside `S032`'s `12–15 %` optimum band, while `CK0339` (`13.0 %` upper edge) was marked `PARTLY` (`8.3 %` from `S032`'s `< 12 %` and below `S023` `14.5–16 %` / `S035` `~15 %`, yet inside `S032` `12–15 %` optimum and touching `S034` `13–15 %` good).

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S041`) and `verdicts.csv` (`W0118`–`CK0549`) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `apps/wired/audit_tasks/progress_notes/T-AUD-23g.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-23g.md`.

## Remaining risks or uncertainties
- `CK0304`, `CK0305`, `CK0309`, `CK0332`–`CK0334`, `CK0336`–`CK0342` rely on `TRADE` 5-gas diagnostic references (`S023`, `S028`, `S032`, `S033`, `S034`, `S035`) rather than OEM cam-timing tailpipe emission tables, and `CK0320`/`CK0329` rely on `S037` (`Ford OEM`) rather than the paywalled SAE J2012 standard text.
