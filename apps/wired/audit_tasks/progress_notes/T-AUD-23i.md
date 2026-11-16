# Progress Note — T-AUD-23i

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23i` (worktree per `T-AUD-23i.go.txt` lane rule) with spec commit `4d7a160` (`git log --oneline fix/T-AUD-24n..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23i.txt` fails with `VERDICTS FAIL 25 error(s)` (all `no verdict`), P3 passes on all eight earlier scopes (`T-GASA-17.txt` `20`, `T-AUD-23a.txt` `25`, `T-AUD-23b.txt` `29`, `T-AUD-23d.txt` `29`, `T-AUD-23e.txt` `28`, `T-AUD-23f.txt` `24`, `T-AUD-23g.txt` `28`, `T-AUD-23h.txt` `30`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 25 errors from `check_verdicts.py --scope scope/T-AUD-23i.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `213` earlier verdicts (`20 + 25 + 29 + 29 + 28 + 24 + 28 + 30`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23i.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `25` root claims (`same_as` empty), all in `labs/comlab/registry/rules/non_starter.json` (P1); `38` existing rows in `sources.csv` ending at `S041` so any new IDs start at `S042` (P4); and `213` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23i.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 25 root claims in `scope/T-AUD-23i.txt` (`NS-001`–`NS-005` rule values in `non_starter.json`) against authoritative sources (`S001`–`S041` or new Firecrawl-fetched sources `S042+`), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23i.txt` (`claims 25`) and the eight P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23i.go.txt` govern worktree branch naming (`agy/T-AUD-23i` instead of `fix/T-AUD-23i`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23i.md`.
- `firecrawl --status` reported `Credits: -7 / 1,000 (-1% left this cycle)` at session start and a test `firecrawl search` returned `Error: Request failed with status code 402`, so no new external scrapes could be billed (temporary `search/` was deleted). Per R1 ("Reuse an earlier source (`S001`–`S041`) when it holds the fact"), all 25 claims are adjudicated against the existing `PRIMARY_LAW`, `PRIMARY_REGULATOR`, `OEM`, and `TRADE` corpus (`S001`, `S009`, `S011`, `S019`, `S023`, `S025`, `S027`, `S030`, `S031`, `S032`, `S034`, `S037`, `S040`), leaving `sources.csv` unchanged (`S001`–`S041`).

## Step 1 Disclosure
- `verdicts CONTRADICTED=14 PARTLY=11`
- `retired 0 of 25 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23i.txt claims 25`
- `UNSOURCED` claims: **0** (all 25 claims sourced against `S001`–`S041`; no `UNSOURCED` rows).

## 25-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0552` | `NS-001` (desc) | `CO2 < 5 % vol` | `PARTLY` | `< 12 % CO2 indicates lack of combustion (S032); CO + CO2 < 6 % voids EPA idle test (S011 PRIMARY_LAW); 11.83 % pre-cat misfire (S040)` | `S032` (`TRADE`) |
| `CK0553` | `NS-001` (desc) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0554` | `NS-001` (desc) | `CO2 ≥ 10 % vol` | `PARTLY` | `11.83 % pre-cat / 15.37 % post-cat CO2 for 1-cyl misfire on 6-cyl (S040); 25 % CO2 drop for 1-cyl misfire on 4-cyl (~10.9-12 % from 14.5-16 %, S023); < 12 % combustion-loss threshold (S032)` | `S040` (`TRADE`) |
| `CK0555` | `NS-001` (obd) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0556` | `NS-001` (obd) | `co2 < 5.0 % vol` | `PARTLY` | `< 12 % CO2 indicates lack of combustion (S032); CO + CO2 < 6 % voids EPA idle test (S011 PRIMARY_LAW); 11.83 % pre-cat misfire (S040)` | `S032` (`TRADE`) |
| `CK0557` | `NS-001` (obd) | `stft_b1 ≥ -1.0 %` | `PARTLY` | `0 % active fuel trim adjustment in open loop before closed loop (S030); counterexample 25 % STFT displayed at 0 rpm (S030); healthy closed-loop STFT -5 to +5 % (S037 OEM) and -10 to +10 % (S030)` | `S030` (`TRADE`) |
| `CK0558` | `NS-001` (obd) | `stft_b1 ≤ 1.0 %` | `PARTLY` | `0 % active fuel trim adjustment in open loop before closed loop (S030); counterexample 25 % STFT displayed at 0 rpm (S030); healthy closed-loop STFT -5 to +5 % (S037 OEM) and -10 to +10 % (S030)` | `S030` (`TRADE`) |
| `CK0559` | `NS-001` (obd) | `ltft_b1 ≥ -1.0 %` | `CONTRADICTED` | `Stored prior-drive LTFT retained across shut-off in KAM (S030 TRADE, S027 PRIMARY_LAW); normal LTFT +/-5 to 8 % (S030) and < +/-10 % (S019)` | `S030` (`TRADE`) |
| `CK0560` | `NS-001` (obd) | `ltft_b1 ≤ 1.0 %` | `CONTRADICTED` | `Stored prior-drive LTFT retained across shut-off in KAM (S030 TRADE, S027 PRIMARY_LAW); normal LTFT +/-5 to 8 % (S030) and < +/-10 % (S019)` | `S030` (`TRADE`) |
| `CK0563` | `NS-002` (desc) | `CO2 < 5 % vol` | `PARTLY` | `< 12 % CO2 indicates lack of combustion (S032); CO + CO2 < 6 % voids EPA idle test (S011 PRIMARY_LAW); 11.83 % pre-cat misfire (S040)` | `S032` (`TRADE`) |
| `CK0564` | `NS-002` (desc) | `ECT < 30 °C` | `CONTRADICTED` | `10 - 30 °C (50 - 86 °F) normal cold-start band (S027 PRIMARY_LAW); -6.7 to 37.8 °C (20 - 100 °F) CSER cold-start band (S037 OEM); 21.1 °C (70 °F) normal cold soak vs -40 °C (-40 °F) extreme-cold flooding enrichment (S025 TRADE)` | `S027` (`PRIMARY_LAW`) |
| `CK0565` | `NS-002` (desc) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0566` | `NS-002` (desc) | `CO2 ≥ 8 % vol` | `PARTLY` | `11.83 % pre-cat / 15.37 % post-cat CO2 for 1-cyl misfire on 6-cyl (S040); < 12 % combustion-loss threshold (S032); 13 - 15 % good (S034)` | `S040` (`TRADE`) |
| `CK0567` | `NS-002` (obd) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0568` | `NS-002` (obd) | `co2 < 5.0 % vol` | `PARTLY` | `< 12 % CO2 indicates lack of combustion (S032); CO + CO2 < 6 % voids EPA idle test (S011 PRIMARY_LAW); 11.83 % pre-cat misfire (S040)` | `S032` (`TRADE`) |
| `CK0569` | `NS-002` (obd) | `ect_c < 30.0 °C` | `CONTRADICTED` | `10 - 30 °C (50 - 86 °F) normal cold-start band (S027 PRIMARY_LAW); -6.7 to 37.8 °C (20 - 100 °F) CSER cold-start band (S037 OEM); 21.1 °C (70 °F) normal cold soak vs -40 °C (-40 °F) extreme-cold flooding enrichment (S025 TRADE)` | `S027` (`PRIMARY_LAW`) |
| `CK0570` | `NS-002` (obd) | `stft_b1 ≥ -1.0 %` | `PARTLY` | `0 % active fuel trim adjustment in open loop before closed loop (S030); counterexample 25 % STFT displayed at 0 rpm (S030); healthy closed-loop STFT -5 to +5 % (S037 OEM) and -10 to +10 % (S030)` | `S030` (`TRADE`) |
| `CK0571` | `NS-002` (obd) | `stft_b1 ≤ 1.0 %` | `PARTLY` | `0 % active fuel trim adjustment in open loop before closed loop (S030); counterexample 25 % STFT displayed at 0 rpm (S030); healthy closed-loop STFT -5 to +5 % (S037 OEM) and -10 to +10 % (S030)` | `S030` (`TRADE`) |
| `CK0572` | `NS-002` (obd) | `ltft_b1 ≥ -1.0 %` | `CONTRADICTED` | `Stored prior-drive LTFT retained across shut-off in KAM (S030 TRADE, S027 PRIMARY_LAW); normal LTFT +/-5 to 8 % (S030) and < +/-10 % (S019)` | `S030` (`TRADE`) |
| `CK0573` | `NS-002` (obd) | `ltft_b1 ≤ 1.0 %` | `CONTRADICTED` | `Stored prior-drive LTFT retained across shut-off in KAM (S030 TRADE, S027 PRIMARY_LAW); normal LTFT +/-5 to 8 % (S030) and < +/-10 % (S019)` | `S030` (`TRADE`) |
| `CK0576` | `NS-003` (desc) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0578` | `NS-003` (obd) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0579` | `NS-003` (obd) | `co2 < 8.0 % vol` | `PARTLY` | `< 12 % CO2 indicates lack of combustion (S032); CO + CO2 < 6 % voids EPA idle test (S011 PRIMARY_LAW); 11.83 % pre-cat running misfire (S040)` | `S032` (`TRADE`) |
| `CK0585` | `NS-004` (obd) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0588` | `NS-005` (obd) | `rpm < 600 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal idle band (S001, S009 PRIMARY_REGULATOR); 500 - 600 rpm Ford running-monitor entry (S037 OEM); 550 rpm V8 idle (S031 TRADE); engine start 150 rpm below warm idle (S027 PRIMARY_LAW)` | `S001` (`PRIMARY_REGULATOR`) |

## Disputes
1. **Engine-speed cranking/no-start gate `rpm < 600` (`CK0553`, `CK0555`, `CK0565`, `CK0567`, `CK0576`, `CK0578`, `CK0585`, `CK0588`):**
   - `T-AUD-23h` (`CK0472`, `CK0473`) confirmed `rpm > 600` as a Ford OEM running-monitor minimum (`S037` EGT rationality `600–2,500 rpm`), while `S037` also uses `500 rpm` (CKP ignition check / UEGO lean-to-rich) and `550 rpm` (L4430), and `S027` (`CARB 13 CCR § 1968.2`, `PRIMARY_LAW`) defines engine start at `150 rpm` below normal warm drive idle.
   - From the no-start side (`rpm < 600`), `S001` and `S009` (`PRIMARY_REGULATOR`) specify normal natural idle down to `450 rpm` (`450–1,500 rpm`), and `S031` (`TRADE`) shows a running 5.3L V8 idling at `550 rpm`. Per R4 ("A boundary that a healthy idling engine can fall under is `CONTRADICTED`"), `< 600 rpm` fires on healthy low-idle engines (`CONTRADICTED`). Note `S001`–`S041` contain no petrol cranking-RPM figure (`150–300 rpm`) and Firecrawl returned `402`.
2. **CO2 thresholds (`CK0552`/`CK0556`/`CK0563`/`CK0568` `< 5 %`, `CK0579` `< 8 %`, `CK0554` `≥ 10 %`, `CK0566` `≥ 8 %`):**
   - `S032` (`TRADE`) puts lack of combustion at `CO2 < 12 %` (vs `12–15 %` optimum, `13–15 %` good in `S034`, `14.5–16 %` healthy idle in `S023`), and `S011` (`40 CFR 85.2215`, `PRIMARY_LAW`) voids idle-emissions measurements when `CO + CO2 < 6 %`. Neither `< 5 %` nor `< 8 %` is within `20 %` of `S032`'s `< 12 %` (`58.3 %` and `33.3 %` away, `PARTLY`), and `S011`'s `< 6 %` is a combined `CO + CO2` idle-test dilution void threshold rather than a cranking `CO2` limit (`Firecrawl 402` blocked external cranking-CO2 lookups).
   - For running misfire descriptions (`CK0554` `≥ 10 %`, `CK0566` `≥ 8 %`), `S040` (`TRADE`) measures `11.83 %` pre-cat (`15.37 %` post-cat) for a running 1-cyl misfire on a 6-cyl engine (and `S023` notes a 1-cyl misfire on a 4-cyl drops CO2 by `25 %`, ~`10.9–12 %` from `14.5–16 %`), supporting running single-cylinder misfires staying well above no-combustion; however, `S040` is a single-cylinder case rather than a lower bound for all/multi-cylinder misfires (`CK0554` `PARTLY`), `8 %` is `32.4 %` (`> 20 %`) below `S040`'s `11.83 %` (`CK0566` `PARTLY`), and `NS-002`'s `CO2 >= 8 %` (`CK0566`) directly collides at `8.0 %` with `NS-003`'s `co2 < 8.0 %` (`CK0579`).
3. **Extreme cold enrichment coolant gate `ECT < 30 °C` (`CK0564`, `CK0569`):**
   - `S025` (`TRADE`) confirms colder ECT drives richer cold-start delivery and `-40 °F` (`-40 °C`) commands maximum enrichment capable of flooding an engine, while `S037` (`OEM`) runs Cold Start Emission Reduction (`CSER`) from `20 °F` to `100 °F` (`-6.7 °C` to `37.8 °C`). However, `S027` (`CARB 13 CCR § 1968.2`, `PRIMARY_LAW`) explicitly treats `10–30 °C` (`50–86 °F`) as a standard ambient cold start, and `S025` treats `70 °F` (`21.1 °C < 30 °C`) as a normal morning cold soak; `< 30 °C` therefore fires on healthy ambient cold starts rather than extreme cold flooding (`CONTRADICTED`).
4. **Open-loop fuel trims `STFT`/`LTFT in -1.0..1.0 %` (`CK0557`–`CK0560`, `CK0570`–`CK0573`):**
   - **LTFT (`CK0559`, `CK0560`, `CK0572`, `CK0573`):** `S030` (`TRADE`) and `S027` (`CARB KAM`, `PRIMARY_LAW`) establish that LTFT is retained in memory across engine shut-off, so during open-loop cranking/no-start the ECU retains its prior-drive LTFT (`±5–8 %` / `< ±10 %` normally in `S030`/`S019`, or wider if a fault existed), and `[-1.0, 1.0] %` also fires on healthy closed-loop trims (`CONTRADICTED`).
   - **STFT (`CK0557`, `CK0558`, `CK0570`, `CK0571`):** `S030` (`TRADE`) confirms `"no fuel trim adjustments are made"` (`0 %`) before closed loop (corroborated by `S025` `"fuel trims are locked out"`), matching STFT at `0` while cranking; however, `S030` gives no `±1.0 %` tolerance, shows a scan-tool counterexample with `Engine RPM is zero` displaying `25 %` STFT, and `[-1.0, 1.0] %` also overlaps healthy closed-loop STFT (`-5 to +5 %` in `S037` `OEM`, `-10 to +10 %` in `S030`, `PARTLY`).

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23i.txt`):
  - `verdicts CONTRADICTED=14 PARTLY=11`
  - `retired 0 of 25 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23i.txt claims 25`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`, `scope/T-AUD-23g.txt`, `scope/T-AUD-23h.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
  - `VERDICTS OK scope=T-AUD-23g.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23h.txt claims 30`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` (`sources.csv` unchanged, `S001`–`S041` reused)
  - Untracked: `apps/wired/audit_tasks/progress_notes/T-AUD-23i.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23i.md`; no `search/` folder.

## CODE REVIEW
- Confirmed `verdicts.csv` (25 rows in exact `T-AUD-23i.txt` order) was appended strictly below the existing `213` rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines (`sources.csv` unchanged at `38` rows / `11` primary).
- Every quote matches its cited source file (`S001`, `S027`, `S030`, `S032`, `S040`) verbatim under `check_verdicts.py` whitespace-normalisation, all `TRADE` verdicts disclose `TRADE source` in `note` per R5, all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/`README.md`, and no `search/` folder or uncited `sources/` file exists.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T11:42:09Z` | `2026-11-16T11:55:16Z` | `13.1` | `ABSENT` |
