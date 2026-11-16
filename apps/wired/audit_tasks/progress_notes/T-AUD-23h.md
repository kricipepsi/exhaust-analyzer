# Progress Note — T-AUD-23h

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23h` (worktree per `T-AUD-23h.go.txt` lane rule) with spec commit `9105e57` (`git log --oneline fix/T-AUD-24m..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23h.txt` fails with `VERDICTS FAIL 30 error(s)` (all `no verdict`), P3 passes on all seven earlier scopes (`T-GASA-17.txt` `20`, `T-AUD-23a.txt` `25`, `T-AUD-23b.txt` `29`, `T-AUD-23d.txt` `29`, `T-AUD-23e.txt` `28`, `T-AUD-23f.txt` `24`, `T-AUD-23g.txt` `28`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 30 errors from `check_verdicts.py --scope scope/T-AUD-23h.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `183` earlier verdicts (`20 + 25 + 29 + 29 + 28 + 24 + 28`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23h.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `30` root claims (`same_as` empty), all in `labs/comlab/registry/rules/mechanical_wear.json` (P1); `38` existing rows in `sources.csv` ending at `S041` so any new IDs start at `S042` (P4); and `183` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23h.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 30 root claims in `scope/T-AUD-23h.txt` (`MW-001`–`MW-009` rule values in `mechanical_wear.json`) against authoritative sources (`S001`–`S041` or new Firecrawl-fetched sources `S042+`), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23h.txt` (`claims 30`) and the seven P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23h.go.txt` govern worktree branch naming (`agy/T-AUD-23h` instead of `fix/T-AUD-23h`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23h.md`.
- `firecrawl --status` reported `Credits: -7 / 1,000 (-1% left this cycle)` at session start and a test `firecrawl search` returned `Error: Request failed with status code 402`, so no new external scrapes could be billed. Per R1 ("Reuse an earlier source (`S001`–`S041`) when it holds the fact"), all 30 claims are adjudicated against the existing `OEM`, `TRADE`, `PRIMARY_LAW`, and `PRIMARY_REGULATOR` corpus (`S001`, `S002`, `S009`, `S016`, `S023`, `S025`, `S027`, `S028`, `S030`, `S031`, `S032`, `S034`, `S035`, `S037`, `S040`), leaving `sources.csv` unchanged (`S001`–`S041`).

## Step 1 Disclosure
- `verdicts CONFIRMED=10 CONTRADICTED=4 PARTLY=16`
- `retired 0 of 30 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23h.txt claims 30`
- `UNSOURCED` claims: **0** (all 30 claims sourced against `S001`–`S041`; no `UNSOURCED` rows).

## 30-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0452` | `MW-001` (v1 removed) | `shrtft1 -10 – 10 %` | `CONFIRMED` | `(matches S030 -10 % to +10 % normal STFT; S037 OEM -9..+11 % / -13..+18 %)` | `S030` (`TRADE`) |
| `CK0453` | `MW-001` | `hc > 200 ppm` | `PARTLY` | `Leaking piston rings / Worn Engine -> HC increase (S032); 0 - 35 ppm healthy idle / 75 - 125 ppm unlit cat (S023); < 50 ppm normal late-model (S034); < 100 ppm good (S035); 200 ppm UK MOT fast-idle legal limit (S001, S009)` | `S032` (`TRADE`) |
| `CK0454` | `MW-001` (misfire desc) | `hc > 200 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal late-model HC in S034); 817 ppm post-cat / 2,482 ppm pre-cat misfire (S040); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal limit (S001)` | `S034` (`TRADE`) |
| `CK0455` | `MW-001` | `hc >= 200.0 ppm` | `PARTLY` | `Leaking piston rings / Worn Engine -> HC increase (S032); 0 - 35 ppm healthy idle / 75 - 125 ppm unlit cat (S023); < 50 ppm normal late-model (S034); < 100 ppm good (S035); 200 ppm UK MOT fast-idle legal limit (S001, S009)` | `S032` (`TRADE`) |
| `CK0456` | `MW-001` | `co2 < 13.0 % vol` | `CONFIRMED` | `(13.0 % within 8.3 % of S032 < 12 % lack of combustion; S032 Worn Engine / Compression loss CO2 decrease; S023 14.5-16 %, S034 13-15 %, S035 ~15 %)` | `S032` (`TRADE`) |
| `CK0457` | `MW-001` | `o2 >= 1.5 % vol` | `PARTLY` | `0 - 0.35 % O2 (< 0.5 % balanced) at idle for working engine and converter (S023); < 1 % normal tailpipe O2 (S032, S035); 1 - 2 % good O2 (S034); S032 Worn Engine -> O2 Some Decrease vs Compression loss -> Some Increase` | `S023` (`TRADE`) |
| `CK0460` | `MW-002` | `hc >= 200.0 ppm` | `PARTLY` | `Worn Engine -> HC Some Increase and vacuum/sealing faults higher HC at idle than under load (S032); 0 - 35 ppm healthy idle (S023); < 50 ppm normal (S034); < 100 ppm good (S035); 200 ppm fast-idle legal limit (S001)` | `S032` (`TRADE`) |
| `CK0461` | `MW-002` | `co2 < 13.0 % vol` | `CONFIRMED` | `(13.0 % within 8.3 % of S032 < 12 % lack of combustion; S032 Worn Engine CO2 Some Decrease; S023 14.5-16 %, S034 13-15 %, S035 ~15 %)` | `S032` (`TRADE`) |
| `CK0464` | `MW-003` | `ect_c > 95.0 °C` | `CONTRADICTED` | `70 - 110 °C (160 - 230 °F) normal operating ECT monitor band and typical 192 °F (88.9 °C) thermostat (S037 OEM); 195 - 210 °F (90.6 - 98.9 °C) normal warm ECT (S025 TRADE)` | `S037` (`OEM`) |
| `CK0465` | `MW-003` (v1) | `ect_c > 90.0 °C` | `CONTRADICTED` | `70 - 110 °C (160 - 230 °F) normal operating ECT monitor band and typical 192 °F (88.9 °C) thermostat (S037 OEM); 195 - 210 °F (90.6 - 98.9 °C) normal warm ECT (S025 TRADE)` | `S037` (`OEM`) |
| `CK0468` | `MW-004` | `CO2 < 12 % vol` | `CONFIRMED` | `(exact match to S032 CO2 will drop below 12 %; Worn Engine / Compression loss CO2 Some Decrease; S023 14.5-16 %, S034 13-15 %, S035 ~15 %)` | `S032` (`TRADE`) |
| `CK0472` | `MW-005` | `rpm > 600 rpm` | `CONFIRMED` | `(matches S037 OEM 600 rpm minimum monitor entry speed; S027 CARB engine start 150 rpm below warm idle; S001 450-1,500 rpm / S031 550 rpm low-idle edge)` | `S037` (`OEM`) |
| `CK0473` | `MW-005` | `rpm > 600 rpm` | `CONFIRMED` | `(matches S037 OEM 600 rpm minimum monitor entry speed; S027 CARB engine start 150 rpm below warm idle; S001 450-1,500 rpm / S031 550 rpm low-idle edge)` | `S037` (`OEM`) |
| `CK0474` | `MW-005` | `co2 < 13.0 % vol` | `CONFIRMED` | `(13.0 % within 8.3 % of S032 < 12 % lack of combustion; S023 14.5-16 %, S034 13-15 %, S035 ~15 %)` | `S032` (`TRADE`) |
| `CK0475` | `MW-005` | `o2 >= 1.5 % vol` | `PARTLY` | `0 - 0.35 % O2 (< 0.5 % balanced) at idle for working engine and converter (S023); < 1 % normal tailpipe O2 (S032, S035); 1 - 2 % good O2 (S034)` | `S023` (`TRADE`) |
| `CK0476` | `MW-005` | `hc >= 200.0 ppm` | `PARTLY` | `Compression loss -> HC Some-large Increase / Worn Engine -> HC Some Increase (S032); 0 - 35 ppm healthy idle / 75 - 125 ppm unlit cat (S023); < 50 ppm normal (S034); < 100 ppm good (S035); 200 ppm fast-idle MOT limit (S001)` | `S032` (`TRADE`) |
| `CK0479` | `MW-006` | `VVT_HISTORY P0010-P0025` | `CONFIRMED` | `(matches S037 OEM VCT Monitor Operation P0010-P0025 range, incl. P0013 and P0017 under Stop-Start VVT)` | `S037` (`OEM`) |
| `CK0483` | `MW-007` | `hc > 200 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal in S034); 817 ppm post-cat / 2,482 ppm pre-cat misfire (S040); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal ceiling (S001)` | `S034` (`TRADE`) |
| `CK0484` | `MW-007` | `o2 < 4.0 % vol` | `CONFIRMED` | `(matches S040 4.0 % O2 6-cyl pre-cat misfire derivation, 3.94 % measured vs 0.48 % baseline; post-cat 0.44 %)` | `S040` (`TRADE`) |
| `CK0485` | `MW-007` | `hc >= 200.0 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal in S034); 817 ppm post-cat / 2,482 ppm pre-cat misfire (S040); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal ceiling (S001)` | `S034` (`TRADE`) |
| `CK0486` | `MW-007` | `co2 < 13.0 % vol` | `CONFIRMED` | `(13.0 % within 8.3 % of S032 < 12 % lack of combustion; S040 11.83 % misfire vs 15.84 % baseline; S023 14.5-16 %, S034 13-15 %, S035 ~15 %)` | `S032` (`TRADE`) |
| `CK0487` | `MW-007` | `nox < 80.0 ppm` | `CONTRADICTED` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034); Ignition misfire -> NOx Some-large decrease (S032)` | `S028` (`TRADE`) |
| `CK0491` | `MW-008` | `hc >= 500.0 ppm` | `PARTLY` | `0 - 35 ppm healthy idle HC (S023); < 50 ppm normal (S034); < 100 ppm good (S035); 200 ppm fast-idle MOT limit (S001); S032/S031 confirm crankcase hydrocarbon ingestion via PCV enriches idle` | `S032` (`TRADE`) |
| `CK0493` | `MW-008` | `high_idle_hc < 250.0 ppm` | `PARTLY` | `<= 200 ppm HC at fast idle 2,500-3,000 rpm (S001, S009 PRIMARY_REGULATOR); S032/S031 confirm vacuum/crankcase-PCV idle faults drop at higher engine speed` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0495` | `MW-008` | `lambda_chem < 0.94` | `PARTLY` | `0.95 - 1.05 healthy analyser Lambda (S040); 0.97 - 1.03 statutory window (S002 PRIMARY_LAW, S001); 0.995 - 1.005 peak cat (S023); S032/S031 confirm crankcase PCV vapors enrich mixture while S034 notes PCV vacuum leaks add O2` | `S040` (`TRADE`) |
| `CK0500` | `MW-009` | `hc >= 500.0 ppm` | `PARTLY` | `0 - 35 ppm healthy idle HC (S023); < 50 ppm normal (S034); < 100 ppm good (S035); 200 ppm fast-idle legal limit (S001); 1,600 - 2,000 ppm misfire (S034)` | `S023` (`TRADE`) |
| `CK0502` | `MW-009` | `co < 0.15 % vol` | `CONTRADICTED` | `0.1 - 0.45 % CO at idle for properly functioning engine and converter (< 0.5 % balanced in S023); <= 0.3 % idle / <= 0.2 % fast-idle statutory limit (S001, S002, S009); < 0.5 % good (S035); 0.02 % clean late-model tailpipe (S040)` | `S023` (`TRADE`) |
| `CK0504` | `MW-009` | `lambda_chem >= 0.99` | `PARTLY` | `0.995 - 1.005 peak stoichiometric catalyst Lambda (S023) and 0.990 - 1.010 at lambda 1 (S016 OEM), vs 0.97 - 1.03 statutory window (S002 PRIMARY_LAW, S001) and ±5 % (0.95 - 1.05, baseline 1.023) healthy analyser Lambda (S040)` | `S023` (`TRADE`) |
| `CK0506` | `MW-009` | `lambda_chem <= 1.01` | `PARTLY` | `0.995 - 1.005 peak stoichiometric catalyst Lambda (S023) and 0.990 - 1.010 at lambda 1 (S016 OEM), vs 0.97 - 1.03 statutory window (S002 PRIMARY_LAW, S001) and ±5 % (0.95 - 1.05, baseline 1.023) healthy analyser Lambda (S040)` | `S023` (`TRADE`) |
| `CK0508` | `MW-009` | `high_idle_hc < 200.0 ppm` | `PARTLY` | `<= 200 ppm HC at fast idle 2,500-3,000 rpm (S001, S009 PRIMARY_REGULATOR); 0 - 35 ppm healthy idle (S023); < 50 ppm normal (S034)` | `S001` (`PRIMARY_REGULATOR`) |

## Disputes
1. **Warm coolant temperature gates in `MW-003` (`CK0464` `ect_c > 95.0 °C`, `CK0465` v1 `ect_c > 90.0 °C`):**
   - `S037` (`Ford OEM`) specifies `70 °C to 110 °C` (`160–230 °F`) as the normal warm-engine fuel-monitor operating band (with `192 °F` / `88.9 °C` typical thermostat regulating temperature and `230 °F` / `110 °C` as the stuck-high fault limit), and `S025` (`Apex Tech Nation`, `TRADE`) gives `195–210 °F` (`90.6–98.9 °C`) as normal warmed-up operating ECT. Both `> 90.0 °C` and `> 95.0 °C` sit squarely inside healthy warm operation and fire on healthy engines (`CONTRADICTED`).
2. **Low-NOx gate in `MW-007` (`CK0487` `nox < 80.0 ppm`):**
   - `S032` (`Smog Tech Institute`, `TRADE`) confirms `Ignition misfire` and `Compression loss` cause `Some-large decrease` in NOx, and `MW-007` uses `< 80.0 ppm` to separate mechanical wear from lean/hot combustion. However, `S028` (`Crypton`, `TRADE`: `"NOx is naturally near 0 ppm at idle"`) and `S035` (`AVI OnDemand`, `TRADE`: `"Expect zero NOx at idle, and less than 500 ppm under load"`) show healthy idling engines sit at ~`0 ppm`, so `< 80.0 ppm` fires on every healthy warm-idle sample (`CONTRADICTED`, matching `CK0304`, `CK0309`, `CK0334`).
3. **`O2 < 4.0 %` misfire boundary (`CK0484`) and `O2 >= 1.5 %` (`CK0457`, `CK0475`):**
   - `S040` (`MOTOR Magazine`, `TRADE`) explicitly derives `4.0% O2` (`3.94 %` measured pre-cat vs `0.48 %` healthy tailpipe baseline) as the pre-catalyst single-cylinder ignition misfire boundary on a 6-cylinder engine (`CONFIRMED` on `CK0484`), while also showing that post-catalyst O2 fell to `0.44 %` when the converter was still lighting off and that 4-/8-cylinder single-cylinder misfires scale differently (`~5.75 %` / `~3.1 %`).
   - For `o2 >= 1.5 %` (`CK0457`, `CK0475`), `S023` (`0–0.35 %`), `S032` (`< 1 %`), and `S035` (`<= 1 %`) place `1.5 %` at `+50 %` (`> 20 %`) above the `1 %` healthy ceiling, whereas `S034` (`Underhood Service`, `TRADE`) puts `1–2 %` in its good O2 range, and `S032`'s Quick Reference Chart gives `Worn Engine -> O2 Some Decrease` vs `Compression loss -> O2 Some Increase` (`PARTLY`).
4. **CO2 `< 13.0 %` (`CK0456`, `CK0461`, `CK0474`, `CK0486`) vs `< 12 %` (`CK0468`):**
   - `S032` (`TRADE`) defines `Optimum CO2 is 12% to 15 %` and `"CO2 under 12% would indicate a lack of combustion"` (exact match for `CK0468` `CO2 < 12 %`, `CONFIRMED`). `13.0 %` sits within `8.3 %` (`< 20 %`) of `< 12 %` and below `S023` (`14.5–16 %` healthy, `13.5–14.5 %` unlit cat) and `S035` (`~15 %`), though touching the `13–15 %` good floor in `S034` and `12–15 %` in `S032` (`CONFIRMED`, consistent with `CK0333`).
5. **HC thresholds (`>= 200` in `CK0453`–`CK0455`, `CK0460`, `CK0476`, `CK0483`, `CK0485`; `>= 500` in `CK0491`, `CK0500`; high-idle `< 250` / `< 200` in `CK0493`, `CK0508`):**
   - `S023` (`0–35 ppm`), `S034` (`< 50 ppm`), and `S035` (`< 100 ppm`) put healthy warm-idle HC well below `200 ppm`, and `S001`/`S009` (`PRIMARY_REGULATOR`) set `200 ppm` as the UK MOT fast-idle (`2,500–3,000 rpm`) statutory ceiling.
   - For misfire (`CK0454`, `CK0483`, `CK0485`), `S034` (`1,600–2,000 ppm`) and `S040` (`817 ppm` post-cat / `2,482 ppm` pre-cat) are `> 20 %` above `200 ppm` (`PARTLY`).
   - For oil-burning rules (`MW-001` rings, `MW-002` valve seals, `MW-008` PCV, `MW-009` turbo seals), `S032` confirms leaking piston rings and worn engines elevate HC and vacuum/sealing faults show higher HC at idle than under load, and `S031` confirms crankcase-PCV vapors enrich idle and attenuate at higher RPM; however, `S001`–`S041` contain no numeric `200`/`500`/`250`/`200 ppm` boundaries for valve stem seals, stuck-open PCV, or turbocharger turbine seal oil cracking, and Firecrawl returned HTTP `402` (`-7 / 1,000` credits) preventing new searches (`PARTLY`).
6. **`MW-008` PCV lambda (`CK0495` `< 0.94`) and `MW-009` turbo-seal stoichiometric gates (`CK0502` `CO < 0.15 %`, `CK0504` `lambda >= 0.99`, `CK0506` `lambda <= 1.01`):**
   - `CK0502` (`co < 0.15 %`): `S023` puts healthy idle CO at `0.1–0.45 %` (`S001` `<= 0.3 %` idle / `<= 0.2 %` fast idle; `S035` `< 0.5 %`), so `< 0.15 %` cuts inside `S023`'s healthy idle band (`CONTRADICTED`, twin of `CK0544`), even though `S040` shows a clean late-model tailpipe at `0.02 %`.
   - `CK0504` / `CK0506` (`0.99–1.01`): `S023` (`0.995–1.005` peak catalyst efficiency, within `0.5 %`) and `S016` (`Bosch OEM` `0.990–1.010` at lambda 1) match `0.99–1.01`, whereas `S040` reports healthy calculated tailpipe Lambda varies `±5 %` (`0.95–1.05`, e.g. `1.023` baseline) and `S002` sets `0.97–1.03`, with no turbo-seal attribution in `S001`–`S041` (`PARTLY`).
   - `CK0495` (`lambda < 0.94`): sits `1.1 %` below `S040`'s `0.95` healthy floor (`0.97` statutory in `S002`), and `S032`/`S031` confirm crankcase-PCV hydrocarbon ingestion enriches the mixture, though `S032` associates rich CO with *plugged* PCV / fuel in oil while `S034` links PCV leaks to *lean* O2 (`PARTLY`).
7. **Running-engine gate (`CK0472`, `CK0473` `rpm > 600`):**
   - `S037` (`Ford OEM`) literally specifies `600 rpm` as a monitor minimum (`Engine speed | 600 rpm | 2500 rpm`, plus `500–580 rpm` on other monitors) and `S027` (`CARB 13 CCR § 1968.2`, `PRIMARY_LAW`) defines engine start at `150 rpm` below normal warm idle (`CONFIRMED`), while `S001` (`PRIMARY_REGULATOR`) allows natural idle down to `450 rpm` (`450–1,500 rpm`) and `S031` notes a 5.3L V8 idling at `550 rpm`.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23h.txt`):
  - `verdicts CONFIRMED=10 CONTRADICTED=4 PARTLY=16`
  - `retired 0 of 30 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23h.txt claims 30`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`, `scope/T-AUD-23g.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
  - `VERDICTS OK scope=T-AUD-23g.txt claims 28`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` (`sources.csv` unchanged, `S001`–`S041` reused)
  - Untracked: `apps/wired/audit_tasks/progress_notes/T-AUD-23h.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23h.md`; no `search/` folder.

## CODE REVIEW
- Confirmed `verdicts.csv` (30 rows in exact `T-AUD-23h.txt` order) was appended strictly below the existing `183` rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines (`sources.csv` unchanged at `38` rows / `11` primary).
- Every quote matches its cited source file (`S001`, `S023`, `S028`, `S030`, `S032`, `S034`, `S037`, `S040`) verbatim under `check_verdicts.py` whitespace-normalisation, all `TRADE` verdicts disclose `TRADE source` in `note` per R5, all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/`README.md`, and no `search/` folder or uncited `sources/` file exists.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T11:26:31Z` | `2026-11-16T11:33:46Z` | `7.2` | `ABSENT` |
