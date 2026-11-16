# Progress Note — T-AUD-23j

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23j` (worktree per `T-AUD-23j.go.txt` lane rule) with spec commit `31449b3` (`git log --oneline fix/T-AUD-24o..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23j.txt` fails with `VERDICTS FAIL 24 error(s)` (all `no verdict`), P3 passes on all nine earlier scopes (`T-GASA-17.txt` `20`, `T-AUD-23a.txt` `25`, `T-AUD-23b.txt` `29`, `T-AUD-23d.txt` `29`, `T-AUD-23e.txt` `28`, `T-AUD-23f.txt` `24`, `T-AUD-23g.txt` `28`, `T-AUD-23h.txt` `30`, `T-AUD-23i.txt` `25`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 24 errors from `check_verdicts.py --scope scope/T-AUD-23j.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `238` earlier verdicts (`20 + 25 + 29 + 29 + 28 + 24 + 28 + 30 + 25`).
- **(c) Independently derived decisive expected value:** Direct inspection of `scope/T-AUD-23j.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `24` root claims (`same_as` empty): `8` in `vacuum_leak.json`, `6` in `overheating.json`, `4` in `ignition_fault.json`, `3` in `exhaust_leak.json`, `3` in `invalid_input.json` (P1); `38` existing rows in `sources.csv` ending at `S041` so any new IDs start at `S042` (P4); and `238` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23j.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 24 root claims in `scope/T-AUD-23j.txt` (evidence gates of `vacuum_leak.json`, `overheating.json`, `ignition_fault.json`, `exhaust_leak.json`, and `invalid_input.json`) against authoritative sources (`S001`–`S041` or new Firecrawl-fetched sources `S042+`), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23j.txt` (`claims 24`) and the nine P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23j.go.txt` govern worktree branch naming (`agy/T-AUD-23j` instead of `fix/T-AUD-23j`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23j.md`.
- `firecrawl --status` reported `Credits: -7 / 1,000 (-1% left this cycle)` at session start and a test `firecrawl search` (`"petrol engine overheating coolant temperature threshold 105 C"`) returned `Error: Request failed with status code 402` (temporary `search/` was deleted). Per R1 ("Reuse an earlier source (`S001`–`S041`) when it holds the fact"), all 24 claims are adjudicated against the existing `PRIMARY_LAW`, `PRIMARY_REGULATOR`, `PRIMARY_STANDARD`, `OEM`, and `TRADE` corpus (`S001`, `S011`, `S014`, `S023`, `S030`, `S032`, `S034`, `S036`, `S037`, `S041`, cross-referenced with `S005`, `S009`, `S018`, `S019`, `S025`, `S029`, `S033`, `S035`, `S040`), leaving `sources.csv` unchanged (`S001`–`S041`).

## Step 1 Disclosure
- `verdicts CONFIRMED=5 CONTRADICTED=11 PARTLY=8`
- `retired 0 of 24 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23j.txt claims 24`
- `UNSOURCED` claims: **0** (all 24 claims sourced against `S001`–`S041`; no `UNSOURCED` rows).

## 24-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0675` | `VL-001` (obd) | `longft1 ≥ 10.0 %` | `CONFIRMED` | — | `S030` (`TRADE`) |
| `CK0676` | `VL-001` (obd) | `shrtft1 ≥ 5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (+/-8 % idle range in S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT monitor entry (S037 OEM); +/-20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0677` | `VL-001` (obd) | `map_kpa > 40.0 kPa` | `CONTRADICTED` | `30 - 50 kPa normal idle MAP range for typical engines (40 - 60 kPa with larger camshaft in S036); 95 - 105 kPa atmospheric / disconnected vacuum line` | `S036` (`TRADE`) |
| `CK0682` | `VL-002` (obd) | `longft1 ≥ 8.0 %` | `CONTRADICTED` | `+/-8 % normal STFT/LTFT range (5 - 8 % normal depending on engine condition in S030; < +/-10 % acceptable in S019); +/-20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0683` | `VL-002` (obd) | `shrtft1 ≥ 3.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (+/-8 % idle range in S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT monitor entry (S037 OEM); +/-20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0687` | `VL-003` (obd) | `map_kpa > 50.0 kPa` | `CONFIRMED` | — | `S036` (`TRADE`) |
| `CK0688` | `VL-003` (obd) | `longft1 ≥ 15.0 %` | `PARTLY` | `+/-8 % normal LTFT / >= +10 % lean problem onset (S030, S019); +20 to +25 % P0171 (S030); > +25 % LONGFT P0171 (S037 OEM); +/-20 % combined normal and +35 % P0171 (S029 OEM)` | `S030` (`TRADE`) |
| `CK0689` | `VL-003` (obd) | `shrtft1 ≥ 10.0 %` | `CONTRADICTED` | `-9 % to +11 % and -13 % to +18 % healthy closed-loop STFT monitor entry ranges (S037 OEM); -10 % to +10 % normal STFT jumping 25 %+ (S030 TRADE); +/-20 % combined normal (S029 OEM)` | `S037` (`OEM`) |
| `CK0593` | `OV-001` (obd) | `rpm > 1000.0 rpm` | `CONTRADICTED` | `450 - 1,500 rpm normal natural idle band (S001, S009 PRIMARY_REGULATOR); S037 OEM P1299 fail-safe cooling activates fuel shut-off rather than high idle; S025 TRADE links 1,500+ rpm high idle to cold ECT` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0597` | `OV-002` (obd) | `ect_c > 105.0 °C` | `CONTRADICTED` | `70 - 110 °C (160 - 230 °F) normal operating ECT monitor band and up to 240 - 250 °F (115.6 - 121.1 °C) / 127 °C in S037 monitors (S037 OEM); 180 - 220 °F (82.2 - 104.4 °C) operating ECT (S036 TRADE); 195 - 210 °F (90.6 - 98.9 °C) warm ECT (S025 TRADE)` | `S037` (`OEM`) |
| `CK0601` | `OV-003` (obd) | `ect_c > 115.0 °C` | `PARTLY` | `70 - 110 °C (160 - 230 °F) fuel-monitor ECT band and up to 115.6 - 127 °C (240 - 250 °F / 127 °C) other monitor ceilings, with P1299 fail-safe cooling at CHT > 270 °F / 132.2 °C (S037 OEM); 82.2 - 104.4 °C normal ECT (S036 TRADE)` | `S037` (`OEM`) |
| `CK0605` | `OV-004` (desc) | `rpm < 1000 rpm` | `PARTLY` | `450 - 1,500 rpm normal natural idle band (S001, S009 PRIMARY_REGULATOR); no 1,000 rpm hot-idle vs cooling-idle split in S001-S041` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0606` | `OV-004` (obd) | `ect_c > 105.0 °C` | `CONTRADICTED` | `70 - 110 °C (160 - 230 °F) normal operating ECT monitor band and up to 240 - 250 °F (115.6 - 121.1 °C) / 127 °C in S037 monitors (S037 OEM); 180 - 220 °F (82.2 - 104.4 °C) operating ECT (S036 TRADE); 195 - 210 °F (90.6 - 98.9 °C) warm ECT (S025 TRADE)` | `S037` (`OEM`) |
| `CK0607` | `OV-004` (obd) | `rpm < 1000.0 rpm` | `PARTLY` | `450 - 1,500 rpm normal natural idle band (S001, S009 PRIMARY_REGULATOR); no 1,000 rpm hot-idle vs cooling-idle split in S001-S041` | `S001` (`PRIMARY_REGULATOR`) |
| `CK0410` | `IF-001` (obd) | `shrtft1 ≥ 5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (+/-8 % idle range in S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT monitor entry (S037 OEM); +/-20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0412` | `IF-002` (desc) | `P0324–P0334` | `PARTLY` | `P0325 - P0334 Knock Sensor 1 & 2 circuit DTCs in S041 (P0324 absent in S041 and S037); S037 OEM adds P032A, P032C, P032D, P033A, P033C, P033D (Knock Sensor 3 & 4) and P130D` | `S041` (`PRIMARY_REGULATOR`) |
| `CK0420` | `IF-002` (obd) | `hc ≥ 200.0 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal late-model HC in S034); 2,482 ppm pre-cat / 817 ppm post-cat misfire (S040); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal ceiling (S001)` | `S034` (`TRADE`) |
| `CK0428` | `IF-003` (obd) | `hc ≥ 200.0 ppm` | `PARTLY` | `Very retarded Timing -> HC Some Increase (Slightly retarded -> Some decrease) and Ignition misfire -> HC Large increase (S032); 1,600 - 2,000 ppm misfire (S034) / 817 - 2,482 ppm (S040); < 50 ppm normal (S034); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle ceiling (S001)` | `S032` (`TRADE`) |
| `CK0401` | `EL-001` (obd) | `longft1 ≥ 8.0 %` | `CONTRADICTED` | `+/-8 % normal STFT/LTFT range (5 - 8 % normal depending on engine condition in S030; < +/-10 % acceptable in S019); +/-20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0406` | `EL-003` (obd) | `hc ≥ 200.0 ppm` | `CONTRADICTED` | `Exhaust Leak -> HC Some Decrease (dilution lowers HC, CO, CO2 while raising O2 in S032); 0 - 35 ppm healthy idle HC (S023); < 50 ppm normal (S034); < 100 ppm good (S035)` | `S032` (`TRADE`) |
| `CK0407` | `EL-003` (obd) | `o2 ≥ 3.0 % vol` | `PARTLY` | `< 1 % good tailpipe O2 and Exhaust Leak -> O2 Some Increase (S032, S035); 0 - 0.35 % healthy idle (S023); 1 - 2 % good O2 (S034); 3.0 % upstream O2 shuts down catalyst NOx reduction (S033)` | `S032` (`TRADE`) |
| `CK0433` | `II-001` (obd) | `co2 > 16.0 % vol` | `CONFIRMED` | — | `S023` (`TRADE`) |
| `CK0436` | `II-002` (obd) | `o2 > 18.0 % vol` | `CONFIRMED` | — | `S014` (`PRIMARY_STANDARD`) |
| `CK0437` | `II-002` (obd) | `co2 < 5.0 % vol` | `CONFIRMED` | — | `S011` (`PRIMARY_LAW`) |

## Disputes
1. **Fuel-trim thresholds across `S030`/`S019` (`TRADE`) vs `S029`/`S037` (`OEM`) (`CK0675`, `CK0682`, `CK0688`, `CK0689`, `CK0401`):**
   - **LTFT `≥ 10 %` (`CK0675` `CONFIRMED`) vs `≥ 8 %` (`CK0682`, `CK0401` `CONTRADICTED`) vs `≥ 15 %` (`CK0688` `PARTLY`):** `S030` (`TRADE`) sets healthy idle/aging LTFT at `±8 %` (`5–8 %`) and flags `≥ +10 %` as lean/problem (`S019` `< ±10 %`), confirming `CK0675` (`≥ 10 %`) while contradicting `≥ 8 %` (`CK0682`, `CK0401`). However, `S029` (`OEM`) treats combined `STFT + LTFT` within `±20 %` as normal (setting P0171 at `+35 %`), `S037` (`OEM`) sets P0171 at `LONGFT > 25 %`, and `S030` puts P0171 at `+20–25 %`; consequently `CK0688` (`≥ 15 %` in `VL-003`) sits `50 %` above `+10 %` and `25–57 %` (`> 20 %`) below `20–35 %` (`PARTLY`).
   - **STFT `≥ 10 %` (`CK0689` `CONTRADICTED`):** `S030` (`TRADE`) line 135 under idle vacuum-leak diagnosis flags `≥ +10 %` as LEAN (`±8 %` idle normal), whereas `S030` line 39 states STFT normally spans `-10 % to +10 %` (jumping `25 %+` transiently) and `S037` (`OEM`, stronger source) allows `-9 % to +11 %` and `-13 % to +18 %` closed-loop STFT monitor entry (`S029` `OEM` `±20 %` combined normal). Per R5, `S037` `OEM` governs (`CONTRADICTED`).
2. **MAP weak-vacuum threshold `> 50.0 kPa` (`CK0687` `CONFIRMED`):**
   - `S036` (`TRADE`) sets typical warm-idle MAP at `30–50 kPa` (matching `> 50.0 kPa` at the upper boundary), but notes engines with a larger camshaft idle at `40–60 kPa` and a disconnected vacuum line / near-atmospheric reading (`VL-003` description) reads `95–105 kPa`.
3. **Overheating ECT & cooling-idle thresholds (`CK0593`, `CK0597`, `CK0601`, `CK0605`, `CK0606`, `CK0607`):**
   - **ECT `> 105 °C` (`CK0597`, `CK0606` `CONTRADICTED`) vs `> 115 °C` (`CK0601` `PARTLY`):** `S036` (`TRADE`) gives `180–220 °F` (`82.2–104.4 °C`) and `S025` (`TRADE`) gives `195–210 °F` (`90.6–98.9 °C`) as normal warm operating ECT, whereas `S037` (`OEM`, stronger source) places the normal operating ECT monitor band at `70–110 °C` (`160–230 °F`, with other monitors enabled up to `240–250 °F` = `115.6–121.1 °C` / `127 °C`) and activates `P1299` fail-safe cooling at `CHT > 270 °F` (`132.2 °C`). Thus `> 105 °C` falls inside `S037`'s `70–110 °C` normal band (`CONTRADICTED`; furthermore `OV-002` pairs `> 105 °C` with `P0128`, which `S037` defines as ECT *below* `< 172 °F / 77.8 °C`), while `> 115 °C` (`CK0601`) exceeds `70–110 °C` and sits `13 %` below `132.2 °C` CHT without an explicit `115 °C` ECT overheat spec in `S001`–`S041` (`PARTLY`).
   - **Idle RPM `> 1000` (`CK0593` `CONTRADICTED`) / `< 1000` (`CK0605`, `CK0607` `PARTLY`):** `S001`/`S009` (`PRIMARY_REGULATOR`) define normal natural idle across `450–1,500 rpm`, and `S037` `P1299` uses fuel shut-off rather than high idle when overheating (while `S025` links `1,500+ rpm` high idle to cold start); no source in `S001`–`S041` confirms a `1,000 rpm` `ECU_COOLING_IDLE` / `NORMAL_HOT_IDLE` split (`Firecrawl 402`).
4. **Knock-sensor DTC range `P0324–P0334` (`CK0412` `PARTLY`):**
   - `S041` (`PRIMARY_REGULATOR`) lists `P0325–P0334` as Knock Sensor 1 & 2 circuit faults (bounded by `P0323` Ignition Speed and `P0335` CKP) and omits `P0324`, while `S037` (`OEM`) adds Knock Sensor 3 & 4 codes `P032A`, `P032C`, `P032D`, `P033A`, `P033C`, `P033D` and `P130D` (`SAE J2012` paywalled; `Firecrawl 402`).
5. **Late-timing HC (`CK0428` `PARTLY`) and exhaust-leak HC/O2 (`CK0406` `CONTRADICTED`, `CK0407` `PARTLY`):**
   - In `S032`, `Very retarded Timing` raises HC (`Some Increase`), whereas `Slightly retarded timing` reduces HC (`Some decrease`); `200 ppm` matches the `S001` fast-idle statutory limit rather than `817–2,000+ ppm` misfire (`S034`, `S040`).
   - In `EL-003` (`CK0406`), `S032` explicitly lists `Exhaust Leak -> HC Some Decrease` because ambient-air dilution lowers HC, CO, and CO2 while raising O2 (`CONTRADICTED` against `EL-003`'s claim that HC rises `"from dilution"`, whereas only pre-sensor manifold leaks can indirectly enrich via O2-sensor skew per `S032`/`S040`).
   - For `CK0407` (`o2 >= 3.0 %`), `S033` cites `3.0 % O2` for upstream catalyst NOx-reduction shutdown rather than a tailpipe/probe air-leak threshold, while `S023`/`S032`/`S034`/`S035` put healthy tailpipe O2 at `0–2 %` (`> 20 %` below `3.0 %`, `PARTLY`).
6. **Invalid-input gas bounds (`CK0433`, `CK0436`, `CK0437` `CONFIRMED`):**
   - `CK0433` (`co2 > 16.0 %`): `S023` (`14.5–16 %`) and `S014` `PRIMARY_STANDARD` (`0–16 % vol` OIML R 99 analyser range) put the ceiling at `16 %`, vs `12–15 %` (`S032`), `13–15 %` (`S034`), `~15 %` (`S035`), `15.84 %` (`S040`), and theoretical dry stoichiometric petrol peak ~`15.2–15.5 %`.
   - `CK0436` (`o2 > 18.0 %`): `S014` ambient reference air is `20.9 % vol` (`13.9 %` above `18.0 %`; `~21 %` in `S018`, `S040`), and `S005` `PRIMARY_LAW` spans `18–21 % vol` synthetic air.
   - `CK0437` (`co2 < 5.0 %`): `S011` `PRIMARY_LAW` voids exhaust tests when `CO + CO2 < 6 %` (`16.7 %` above `5.0 %`, matching `CO2 < 5 %` when `CO ≈ 0` in air-contaminated samples), whereas `S005` puts purified air at `≤ 400 ppm` (`0.04 %`) `CO2` and `S032` puts combustion loss at `< 12 %`.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23j.txt`):
  - `verdicts CONFIRMED=5 CONTRADICTED=11 PARTLY=8`
  - `retired 0 of 24 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23j.txt claims 24`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`, `scope/T-AUD-23g.txt`, `scope/T-AUD-23h.txt`, `scope/T-AUD-23i.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
  - `VERDICTS OK scope=T-AUD-23g.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23h.txt claims 30`
  - `VERDICTS OK scope=T-AUD-23i.txt claims 25`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` (`sources.csv` unchanged, `S001`–`S041` reused)
  - Untracked: `apps/wired/audit_tasks/progress_notes/T-AUD-23j.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23j.md`; no `search/` folder.

## CODE REVIEW
- Confirmed `verdicts.csv` (24 rows in exact `T-AUD-23j.txt` order) was appended strictly below the existing `238` rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines (`sources.csv` unchanged at `38` rows / `11` primary).
- Every quote matches its cited source file (`S001`, `S011`, `S014`, `S023`, `S030`, `S032`, `S034`, `S036`, `S037`, `S041`) verbatim under `check_verdicts.py` whitespace-normalisation, all `TRADE` verdicts disclose `TRADE source` in `note` per R5, all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/`README.md`, and no `search/` folder or uncited `sources/` file exists.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T12:32:28Z` | `2026-11-16T12:38:03Z` | `5.6` | `ABSENT` |
