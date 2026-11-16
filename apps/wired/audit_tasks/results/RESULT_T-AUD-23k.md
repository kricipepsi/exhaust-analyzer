# Result — T-AUD-23k

## Status
completed

## Summary
Verified all **32** root code-audit claims in [T-AUD-23k.txt](file:///C:/4DApp/.agy/T-AUD-23k/labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23k.txt) covering the v2 router threshold literals in [integration_shim.py](file:///C:/4DApp/.agy/T-AUD-23k/labs/comlab/registry/integration_shim.py) (`_ff_cold` at `:381`, `_control_plausibility_state`, `_sensor_dynamics_state`, `_lean_root_cause_state`, `_c4_signal_state`, `_health_confirmation_state`, and `_score_rule` C2 checks at `:661–984`), appending **32** verdicts (`CONFIRMED=10`, `CONTRADICTED=6`, `PARTLY=8`, `UNSOURCED=8`) to [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23k/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) using existing authoritative sources (`S017`, `S019`, `S024`, `S029`, `S030`, `S032`, `S037`, `S040`, cross-referenced with `S012`, `S020`, `S021`, `S023`, `S027`, `S033`, `S034`, `S035`, `S036`, `S038`) without altering any existing row in `sources.csv` or `verdicts.csv`.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T12:50:49Z` | `2026-11-16T12:58:15Z` | `7.4` | `ABSENT` |

## Files changed
- Modified: [verdicts.csv](file:///C:/4DApp/.agy/T-AUD-23k/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv) (+32 rows for all 32 scope claims; 0 lines removed)
- Created: [T-AUD-23k.md](file:///C:/4DApp/.agy/T-AUD-23k/apps/wired/audit_tasks/progress_notes/T-AUD-23k.md)
- Created: [RESULT_T-AUD-23k.md](file:///C:/4DApp/.agy/T-AUD-23k/apps/wired/audit_tasks/results/RESULT_T-AUD-23k.md)

## Commands executed
- Baseline & preconditions: `check_verdicts.py --scope scope/T-AUD-23k.txt` (`VERDICTS FAIL 32 error(s)`), P3 scopes (`T-GASA-17`, `T-AUD-23a`, `T-AUD-23b`, `T-AUD-23d`, `T-AUD-23e`, `T-AUD-23f`, `T-AUD-23g`, `T-AUD-23h`, `T-AUD-23i`, `T-AUD-23j`), `firecrawl.cmd --status` (`Credits: -7 / 1,000`), test `firecrawl.cmd search` (`Error: Request failed with status code 402`; temporary `search/` removed), and inspection of `claims_comlab.csv`, `integration_shim.py`, `ingestion.py`, `rules/*.json`, `verdicts.csv`, and `sources/S001.md`–`S041.md`.
- Python quote-verification and CSV append script adding 32 verdicts to `verdicts.csv` in UTF-8 with LF line endings.
- Verification Steps 1–3:
  1. `check_verdicts.py --scope scope/T-AUD-23k.txt`
  2. `check_verdicts.py` on all ten P3 scopes (`T-GASA-17` through `T-AUD-23j`)
  3. `git diff` removed-line count (`0`) on `sources.csv` and `verdicts.csv` and `git status --porcelain`.

## Validation evidence
- **Step 1 (`T-AUD-23k.txt`):**
  ```text
  verdicts CONFIRMED=10 CONTRADICTED=6 PARTLY=8 UNSOURCED=8
  retired 0 of 32 scope claims (retired.csv)
  sources 38 primary 11
  VERDICTS OK scope=T-AUD-23k.txt claims 32
  ```
- **Step 2 (`T-GASA-17.txt`, `T-AUD-23a.txt`–`T-AUD-23j.txt`):**
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
  VERDICTS OK scope=T-AUD-23j.txt claims 24
  ```
- **Step 3 (`git diff` removed lines & `git status --porcelain`):**
  - Removed lines on `sources.csv` and `verdicts.csv`: `0`
  - Only `verdicts.csv`, `T-AUD-23k.md`, and `RESULT_T-AUD-23k.md` changed; no `search/` directory exists.

## Criteria
| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | Step 1 prints `VERDICTS OK scope=T-AUD-23k.txt claims 32` and no `ERROR` line | `MET` | Step 1 output above |
| 2 | Step 2 prints the ten P3 lines | `MET` | Step 2 output above |
| 3 | Note discloses step 1 `verdicts` and `sources` lines, 32-verdict table, searches for every `UNSOURCED`, and `Disputes` list | `MET` | [T-AUD-23k.md](file:///C:/4DApp/.agy/T-AUD-23k/apps/wired/audit_tasks/progress_notes/T-AUD-23k.md) (`UNSOURCED=8` searches, 32-row table, 6 dispute items) |
| 4 | Only `sources.csv`, `verdicts.csv`, and new `sources/` files change; no existing row changes (`step 3: 0`); no `search/` folder | `MET` | Step 3 output (`0` removed lines, only `verdicts.csv` + note/result changed, no `search/`) |

## Decisions the task did not specify
- **Source reuse and `UNSOURCED` handling under Firecrawl `402`:** `firecrawl --status` reported `-7 / 1,000` credits at session start and a test `firecrawl search` returned HTTP `402`; per R1 and R2, 24 claims were verified against existing `S001`–`S041` sources (`S017`, `S019`, `S024`, `S029`, `S030`, `S032`, `S037`, `S040`), while the 8 claims not decidable by `S001`–`S041` (`CK0237`, `CK0241`, `CK0242`, `CK0243`, `CK0265`, `CK0266`, `CK0267`, `CK0285`) were recorded as `UNSOURCED` per R4 with their 3 search queries and the `402` block documented.
- **Stronger-source / healthy-band adjudication on `CK0240`, `CK0244`, `CK0248`, `CK0283`, `CK0284`:** Per R4/R5, gates firing inside `OEM` healthy/valid operating bands (`S037` `11.0–16.0 V` monitor battery band for `CK0240`, `S037` `35–60 psig` = `241.3–413.7 kPa` port FRP band for `CK0248`, `S037` `<= 0.50–0.75` passing catalyst index ratio for `CK0284`, `S029` `±20 %` normal combined `STFT + LTFT` for `CK0244` and `CK0283`) were marked `CONTRADICTED`.

## Pre-existing changes preserved
- Clean worktree at start; all existing rows in `sources.csv` (`S001`–`S041`, 38 rows) and `verdicts.csv` (`W0118`–`CK0437`, 262 rows) preserved verbatim (`0` removed lines).

## Rollback
- `git restore labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` and delete `apps/wired/audit_tasks/progress_notes/T-AUD-23k.md` and `apps/wired/audit_tasks/results/RESULT_T-AUD-23k.md`.

## Remaining risks or uncertainties
- Eight claims (`CK0237`, `CK0241`, `CK0242`, `CK0243`, `CK0265`, `CK0266`, `CK0267`, `CK0285`) remain `UNSOURCED` because Firecrawl credits are exhausted (`402`) and `S001`–`S041` do not contain those specific OEM/EPA/SAE thresholds (DLC ground drop `0.20 V`, Mode `$06` `10 %` margin, MAF `-15 %` calculated delta, `5` warm-up cycles / `200 mi` post-clear readiness, `0.8 %` decel CO).
- Thirteen verdicts (`CK0245`, `CK0246`, `CK0250`, `CK0251`, `CK0257`, `CK0258`, `CK0259`, `CK0260`, `CK0261`, `CK0263`, `CK0269`, `CK0271`, `CK0272`) cite `TRADE` sources (`S019`, `S024`, `S030`, `S032`, `S040`) as primary cited sources.
