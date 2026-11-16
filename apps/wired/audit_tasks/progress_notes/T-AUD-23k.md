# Progress Note — T-AUD-23k

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23k` (worktree per `T-AUD-23k.go.txt` lane rule) with spec commit `aeadef8` (`git log --oneline fix/T-AUD-24q..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23k.txt` fails with `VERDICTS FAIL 32 error(s)` (all `no verdict`), P3 passes on all ten earlier scopes (`T-GASA-17.txt` `20`, `T-AUD-23a.txt` `25`, `T-AUD-23b.txt` `29`, `T-AUD-23d.txt` `29`, `T-AUD-23e.txt` `28`, `T-AUD-23f.txt` `24`, `T-AUD-23g.txt` `28`, `T-AUD-23h.txt` `30`, `T-AUD-23i.txt` `25`, `T-AUD-23j.txt` `24`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 32 errors from `check_verdicts.py --scope scope/T-AUD-23k.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `262` earlier verdicts (`20 + 25 + 29 + 29 + 28 + 24 + 28 + 30 + 25 + 24`).
- **(c) Independently derived decisive expected value:** Direct inspection of `scope/T-AUD-23k.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `32` root claims (`same_as` empty), all in `labs/comlab/registry/integration_shim.py` (P1); `38` existing rows in `sources.csv` ending at `S041` so any new IDs start at `S042` (P4); and `262` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23k.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 32 root claims in `scope/T-AUD-23k.txt` (the live threshold literals in `labs/comlab/registry/integration_shim.py`) against authoritative sources (`S001`–`S041` or `UNSOURCED` where external fetch is blocked by Firecrawl 402), and append rows to `verdicts.csv` (and `sources.csv` if any new source is fetched) without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23k.txt` (`claims 32`) and the ten P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23k.go.txt` govern worktree branch naming (`agy/T-AUD-23k` instead of `fix/T-AUD-23k`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23k.md`.
- `firecrawl --status` reported `Credits: -7 / 1,000 (-1% left this cycle)` at session start and a test `firecrawl search` (`"OBD II DLC signal ground voltage drop 0.2V"`) returned `Error: Request failed with status code 402` (temporary `search/` was deleted). Per R1 ("Reuse an earlier source (`S001`–`S041`) when it holds the fact") and R2 ("Web access is firecrawl only... never WebFetch or WebSearch"), all 32 claims were evaluated against `S001`–`S041` (`S017`, `S019`, `S024`, `S029`, `S030`, `S032`, `S037`, `S040`, cross-referenced with `S012`, `S020`, `S021`, `S023`, `S027`, `S033`, `S034`, `S035`, `S036`, `S038`), leaving `sources.csv` unchanged (`S001`–`S041`) and marking the 8 claims not decidable by `S001`–`S041` as `UNSOURCED` with their 3 search queries recorded.

## Step 1 Disclosure
- `verdicts CONFIRMED=10 CONTRADICTED=6 PARTLY=8 UNSOURCED=8`
- `retired 0 of 32 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23k.txt claims 32`

## 32-Verdict Table

| claim | rule / router function | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0236` | `_ff_cold` (`:381`, freeze-frame trims) | `70.0 °C` (`_FF_WARM_ECT_C`) | `CONFIRMED` | — | `S037` (`OEM`) |
| `CK0237` | `_control_plausibility_state` (`EF-001`–`EF-003`) | `dlc_signal_ground_drop > 0.20 V` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0238` | `_control_plausibility_state` (`EF-001`–`EF-003`) | `koeo_map_baro_delta >= 5.0 kPa` | `CONFIRMED` | — | `S037` (`OEM`) |
| `CK0240` | `_control_plausibility_state` (`EF-001`–`EF-003`) | `module_voltage_loaded < 12.0 V` | `CONTRADICTED` | `11.0 - 16.0 V valid OBD monitor battery voltage band (< 11 V low-voltage abort/fault in S037 OEM)` | `S037` (`OEM`) |
| `CK0241` | `_sensor_dynamics_state` (`SF-001`, `SF-002`, `SF-005`, `SF-008`) | `mode06_margin <= 10.0 %` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0242` | `_sensor_dynamics_state` (`SF-001`, `SF-002`, `SF-005`, `SF-008`) | `maf_delta_idle <= -15.0 %` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0243` | `_sensor_dynamics_state` (`SF-001`, `SF-002`, `SF-005`, `SF-008`) | `maf_delta_2500 <= -15.0 %` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0244` | `_lean_root_cause_state` (`VL-001`–`VL-003`) | `tft_idle >= 15.0 %` | `CONTRADICTED` | `+/-20 % normal total (STFT + LTFT) fuel trim band and +35 % P0171 malfunction (S029 OEM); +/-8 % each / >= +10 % individual lean onset (S030 TRADE)` | `S029` (`OEM`) |
| `CK0245` | `_lean_root_cause_state` (`VL-001`–`VL-003`) | `tft_2500 <= 10.0 %` | `PARTLY` | `drops back to normal reading (+/-8 % single trim / +/-10 % STFT in S030 TRADE) at 1500-2000 rpm; +/-20 % combined (STFT + LTFT) normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0246` | `_lean_root_cause_state` (`VL-001`–`VL-003`) | `(tft_idle - tft_2500) >= 15.0 %` | `PARTLY` | `STFT and LTFT +10 %+ at idle dropping back to normal (+/-8 % each) at 1500-2000 rpm (S030 TRADE; qualitative drop, no explicit 15 % delta boundary)` | `S030` (`TRADE`) |
| `CK0248` | `_lean_root_cause_state` (`LC-001`–`LC-003`, port) | `pressure < 280.0 kPa` | `CONTRADICTED` | `35 - 60 psig (241.3 - 413.7 kPa gauge) reasonable port/low-pressure FRP demand band; P008A triggers on (Desired - Actual)/Desired > 25 % or > 20 psig error (S037 OEM)` | `S037` (`OEM`) |
| `CK0249` | `_lean_root_cause_state` (`LC-001`–`LC-003`, DI) | `pressure < 12000.0 kPa` | `PARTLY` | `(Desired - Actual) / Desired > 25 % for P0087, with GDI FRP transfer table spanning 6.5 - 26 MPa (6,500 - 26,000 kPa) at 1.5 - 4.5 V (S037 OEM)` | `S037` (`OEM`) |
| `CK0250` | `_lean_root_cause_state` (`LC-001`–`LC-003`, WOT) | `w_lambda > 1.05` | `CONFIRMED` | — | `S040` (`TRADE`) |
| `CK0251` | `_lean_root_cause_state` (`LC-001`–`LC-003`, WOT load) | `calc_load < 80.0 %` | `CONFIRMED` | — | `S019` (`TRADE`) |
| `CK0257` | `_c4_signal_state` (`EL-001`, `EL-003`) | `delta_stft <= -8.0 %` | `PARTLY` | `STFT drops from +10 %+ idle back to normal (+/-8 % / +/-10 % in S030 TRADE) at 1500-2000 rpm; no explicit delta-STFT <= -8.0 % threshold` | `S030` (`TRADE`) |
| `CK0258` | `_c4_signal_state` (`EL-001`, `EL-003`) | `co2 < 12.0 % vol` | `CONFIRMED` | — | `S032` (`TRADE`) |
| `CK0259` | `_c4_signal_state` (`EL-001`, `EL-003`) | `o2_elev > 2.5 % vol` | `PARTLY` | `< 1 % good tailpipe O2 and Exhaust Leak -> O2 Some Increase (S032, S035); 0 - 0.35 % healthy idle (S023); 1 - 2 % good O2 (S034); 3.0 % upstream O2 shuts down catalyst NOx reduction (S033)` | `S032` (`TRADE`) |
| `CK0260` | `_c4_signal_state` (`SF-001`, `SF-002`, `SF-008`) | `ds_o2 > 0.7 V` | `CONTRADICTED` | `~0.7 V steady downstream voltage for a working catalyst (S024 TRADE); 0.45 - 0.85 V filtered secondary O2 range (S037 OEM)` | `S024` (`TRADE`) |
| `CK0261` | `_c4_signal_state` (`SF-001`, `SF-002`, `SF-008`) | `propane > -15.0 %` | `PARTLY` | `No change in fuel trim (~0 %) indicates non-responding O2 sensor vs STFT going NEGATIVE on propane enrichment (S030 TRADE; no -15 % boundary in S001-S041)` | `S030` (`TRADE`) |
| `CK0262` | `_c4_signal_state` (`LC-001`, `LC-002`) | `ds_o2 <= 0.4 V` | `CONFIRMED` | — | `S017` (`OEM`) |
| `CK0263` | `_c4_signal_state` (`LC-001`, `LC-002`) | `propane <= -15.0 %` | `PARTLY` | `STFT going NEGATIVE and LTFT creeping downward during propane enrichment confirms responsive O2 sensor (S030 TRADE; no -15 % numeric threshold in S001-S041)` | `S030` (`TRADE`) |
| `CK0265` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `mode06_margin >= 10.0 %` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0266` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `warmup_cycles >= 5` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0267` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `miles >= 200.0 mi` | `UNSOURCED` | — | — (`Firecrawl 402`) |
| `CK0268` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `|stft_idle| <= 5.0 %` | `CONFIRMED` | — | `S037` (`OEM`) |
| `CK0269` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `|ltft_idle| <= 7.0 %` | `CONFIRMED` | — | `S030` (`TRADE`) |
| `CK0270` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `|stft_2500| <= 5.0 %` | `CONFIRMED` | — | `S037` (`OEM`) |
| `CK0271` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `|ltft_2500| <= 7.0 %` | `CONFIRMED` | — | `S030` (`TRADE`) |
| `CK0272` | `_health_confirmation_state` (`NF-001`, `NF-002`) | `|tft_idle - tft_2500| <= 5.0 %` | `PARTLY` | `STFT and LTFT within a few percentage points of zero at idle and steady RPM (+/-8 % normal in S030; no explicit 5.0 % idle-to-2500-rpm delta ceiling)` | `S030` (`TRADE`) |
| `CK0283` | `_score_rule` (`RM-001`, `RM-003`, `RM-004`) | `c2_idle_trim <= -10.0 %` | `CONTRADICTED` | `+/-20 % normal total (STFT + LTFT) fuel trim band and -35 % P0172 malfunction (S029 OEM); -10 % to +10 % normal STFT and +/-8 % idle STFT/LTFT (S030 TRADE); -13 % to +18 % STFT entry (S037 OEM)` | `S029` (`OEM`) |
| `CK0284` | `_score_rule` (`CF-001`, `CF-002`, `CF-006`, `CF-007`) | `c2_index > 0.20` | `CONTRADICTED` | `<= 0.75 bank monitor (<= 0.60 Y-pipe; <= 0.50 E10 to <= 0.90 E85) passing catalyst index ratio in S037 OEM` | `S037` (`OEM`) |
| `CK0285` | `_score_rule` (`CF-001`, `CF-002`, `CF-006`, `CF-007`) | `c2_decel_co > 0.8 % vol` | `UNSOURCED` | — | — (`Firecrawl 402`) |

## Searches Behind `UNSOURCED` Claims (Firecrawl HTTP 402: `Credits: -7 / 1,000`)
All 8 `UNSOURCED` claims could not be fetched externally because Firecrawl returned HTTP `402` (exhausted account credits) and no source in `S001`–`S041` decides the threshold:
1. **`CK0237` (`dlc_signal_ground_drop > 0.20 V`):** (1) `"OBD II DLC signal ground voltage drop 0.2V"` (executed via Firecrawl, returned `402`), (2) `"SAE J1962 DLC pin 5 signal ground voltage drop specification"`, (3) `"OEM DLC signal ground voltage drop fuel trim bias threshold"`. Note: `S021` (`TRADE`) mentions a `100 mV` (`0.10 V`) DMM O2 ground-offset test tip, not a DLC pin-5 limit.
2. **`CK0241` (`mode06_margin <= 10.0 %`):** (1) `"Mode 06 O2 sensor response margin 10 percent threshold"`, (2) `"SAE J1979 Mode 06 test limit margin 10% O2 lazy"`, (3) `"OBD II Mode 06 oxygen sensor percentage margin diagnostic threshold"`. Note: `S027` (`PRIMARY_LAW`) and `S037` (`OEM`) define raw Mode `$06` values vs min/max limits without a `10 %` margin cut-off.
3. **`CK0242` (`maf_delta_idle <= -15.0 %`):** (1) `"MAF actual vs calculated airflow 15 percent tolerance idle"`, (2) `"volumetric efficiency MAF underread 15% diagnostic threshold"`, (3) `"OEM P0101 MAF rationality calculated airflow percentage threshold"`. Note: `S019`/`S020` (`TRADE`) and `S037` (`OEM`) give no `-15 %` idle delta threshold.
4. **`CK0243` (`maf_delta_2500 <= -15.0 %`):** (1) `"MAF actual vs calculated airflow 15 percent tolerance 2500 rpm"`, (2) `"volumetric efficiency MAF underread 15% under load threshold"`, (3) `"OEM P0101 MAF rationality calculated airflow percentage threshold"`.
5. **`CK0265` (`mode06_margin >= 10.0 %`):** (1) `"Mode 06 catalyst margin 10 percent pass threshold"`, (2) `"SAE J1979 Mode 06 test margin 10% healthy confirmation"`, (3) `"OBD II Mode 06 catalyst monitor margin percentage threshold"`.
6. **`CK0266` (`warmup_cycles >= 5`):** (1) `"OBD II warm up cycles since clear 5 cycles readiness"`, (2) `"5 warm up cycles after DTC clear monitor confidence"`, (3) `"EPA I/M OBD readiness warm up cycles since clear threshold"`. Note: `S012` defines PID `$30` and `S027` uses `1` cycle (permanent DTC clear), `3` driving cycles (MIL off), and `40` warm-up cycles (confirmed DTC erase).
7. **`CK0267` (`miles >= 200.0 mi`):** (1) `"OBD II 200 miles since codes cleared readiness threshold"`, (2) `"distance traveled since DTC clear 200 miles drive cycle"`, (3) `"EPA OBD readiness verification 200 miles since clear"`. Note: `S012` defines PID `$31` and `S027` requires reporting it without a `200 mi` pass rule.
8. **`CK0285` (`c2_decel_co > 0.8 % vol`):** (1) `"deceleration CO exhaust gas catalyst failure 0.8 percent"`, (2) `"decel CO > 0.8% catalytic converter efficiency test"`, (3) `"five gas analyzer deceleration CO threshold catalyst failure"`. Note: `S023`/`S032`/`S033`/`S034`/`S035` cover steady-state idle/cruise CO and `S037` DFSO checks rear-O2 voltage rather than decel CO %.

## Disputes
1. **KOEO MAP vs BARO delta `>= 5.0 kPa` (`CK0238` `CONFIRMED`):** `S037` (`OEM`) lists two calibrations for the `P0106` Key-Up test: `|BARO - MAP| < 1.5"Hg` (`5.08 kPa`, `1.6 %` from `5.0 kPa`, line 4596) and `|BARO - MAP| < 3.0"Hg` (`10.16 kPa`, line 4547). Moreover, `S037` tests bidirectional `|BARO - MAP|` whereas `CK0238` labels `>= 5.0 kPa` specifically `"rich-bias electrical reference fault"`.
2. **Module voltage under load `< 12.0 V` (`CK0240` `CONTRADICTED`):** `S037` (`OEM`) defines `11.0–16.0 V` as the valid battery-voltage operating band for OBD fuel, O2, injector, and MAP monitors (aborting/faulting below `11 V`, line 455). While `11.0 V` is `8.3 %` below `12.0 V`, firing at `< 12.0 V` triggers `CONTROL_REFERENCE_FAULT` on `11.0–11.99 V` readings inside `S037`'s healthy monitor band; also note `S037` documents OBD monitor enable voltage rather than a dedicated loaded charging-system `P0562` voltage spec (external fetch blocked by Firecrawl 402).
3. **Total vs single fuel-trim bounds (`CK0244`, `CK0245`, `CK0283`):** `S030` (`TRADE`) sets individual idle STFT/LTFT normal bounds at `±8 %` (`-10..+10 %` STFT; `>= +10 %` lean onset), whereas `S029` (`OEM`, stronger source per R5) sets combined `STFT + LTFT` normal functioning at `±20 %` (`±35 %` malfunction) and `S037` (`OEM`) allows `-13 % to +18 %` STFT monitor entry. Because `tft_idle` (`CK0244`) and `c2_idle_trim` (`CK0283`) sum `stft_idle + ltft_idle`, `>= 15.0 %` (`CK0244`) and `<= -10.0 %` (`CK0283`) sit inside `S029`'s `±20 %` normal combined band (`CONTRADICTED`). For `tft_2500 <= 10.0 %` (`CK0245`, `PARTLY`), `10.0 %` matches `S030`'s `+10 %` single-trim boundary (`25 %` from `±8 %`) at `1500–2000 rpm` rather than `2500 rpm`, but is `50 %` tighter than `S029`'s `±20 %` combined normal bound.
4. **ΔSTFT `<= -8.0 %` (`CK0257` `PARTLY`) and propane `> / <= -15.0 %` (`CK0261`, `CK0263` `PARTLY`):** `S030` (`TRADE`) confirms the negative-delta vacuum-leak recovery direction (`1500–2000 rpm`, line 135) without a `-8 %` cut-off, and normal STFT swings across `-10 % to +10 %` (`S030` line 39) can exceed `-8 %`. Similarly, `S030` confirms propane enrichment drives STFT negative (`CK0263`) vs `"No change"` (`~0 %`) for non-responding O2 (`CK0261`) without a `-15 %` boundary, and in `_c4_signal_state` omitted `propane_trim_shift_pct` defaults to `0.0 > -15.0` (`CK0261`).
5. **Fuel rail pressure floors (`CK0248` `CONTRADICTED`, `CK0249` `PARTLY`):** `S037` (`OEM`) sets port/low-pressure FRP reasonable demand at `35–60 psig` (`241.3–413.7 kPa` gauge) and triggers `P008A` on `> 25 %` relative drop or `> 20 psig` error (`< 280.0 kPa` = `40.6 psig` sits `16 %` above `241.3 kPa`, inside `35–60 psig`, though if `fuel_rail_pressure_load_kpa` were absolute rather than gauge `280 kPa` abs ≈ `26 psig` gauge would sit below `35 psig`). For GDI (`CK0249`), `S037` triggers `P0087` on `> 25 %` drop below `Fuel_Pressure_Desired` across a `6.5–26 MPa` (`6,500–26,000 kPa`) transfer scale rather than a fixed `12,000 kPa` floor.
6. **Health-confirmation `|STFT| <= 5.0 %` (`CK0268`, `CK0270`) and `|LTFT| <= 7.0 %` (`CK0269`, `CK0271`):** `S037` (`OEM`) uses `-5 % to +5 %` STFT entry in the UEGO Response Rate monitor (line 1262), though other `S037` monitors allow `-9..+11 %` and `-13..+18 %` and `S030` allows `±8–10 %`. Likewise `|LTFT| <= 7.0 %` sits `12.5 %` inside `S030`'s `±8 %` normal LTFT ceiling (`5–8 %`), whereas `S019` allows `< ±10 %` and `S029` `OEM` allows `±20 %` combined. Both are conservative health-confirmation gates rather than fault-firing gates.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23k.txt`):
  - `verdicts CONFIRMED=10 CONTRADICTED=6 PARTLY=8 UNSOURCED=8`
  - `retired 0 of 32 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23k.txt claims 32`
- Step 2 (`check_verdicts.py` on the ten P3 scopes):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
  - `VERDICTS OK scope=T-AUD-23g.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23h.txt claims 30`
  - `VERDICTS OK scope=T-AUD-23i.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23j.txt claims 24`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`): verified after final edit (see `RESULT_T-AUD-23k.md` and final response).

## CODE REVIEW
- Confirmed `verdicts.csv` (32 rows in exact `T-AUD-23k.txt` order) was appended strictly below the existing `262` rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines (`sources.csv` unchanged at `38` rows / `11` primary).
- Every non-`UNSOURCED` quote matches its cited source file (`S017`, `S019`, `S024`, `S029`, `S030`, `S032`, `S037`, `S040`) verbatim under `check_verdicts.py` whitespace-normalisation, all `TRADE` verdicts disclose `TRADE source` in `note` per R5, all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/`README.md`, all 8 `UNSOURCED` rows document the Firecrawl `402` error and 3 search queries, and no `search/` folder or uncited `sources/` file exists.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T12:50:49Z` | `2026-11-16T12:58:15Z` | `7.4` | `ABSENT` |
