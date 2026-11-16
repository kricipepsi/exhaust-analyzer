# Progress Note — T-AUD-23g

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23g` (worktree per `T-AUD-23g.go.txt` lane rule) with spec commit `5e8f441` (`git log --oneline fix/T-AUD-24l..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23g.txt` fails with `VERDICTS FAIL 28 error(s)` (all `no verdict`), P3 passes on `T-GASA-17.txt` (`20`), `T-AUD-23a.txt` (`25`), `T-AUD-23b.txt` (`29`), `T-AUD-23d.txt` (`29`), `T-AUD-23e.txt` (`28`), and `T-AUD-23f.txt` (`24`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 28 errors from `check_verdicts.py --scope scope/T-AUD-23g.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `155` earlier verdicts (`20 + 25 + 29 + 29 + 28 + 24`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23g.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `28` root claims (`same_as` empty), all in `labs/comlab/registry/rules/cam_timing.json` (P1); `38` existing rows in `sources.csv` ending at `S041` so any new IDs start at `S042` (P4); and `155` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23g.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 28 root claims in `scope/T-AUD-23g.txt` (`cam_timing.json` CT-002 to CT-008 rule values) against authoritative sources (`S001`–`S041` or new Firecrawl-fetched sources `S042+`), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23g.txt` (`claims 28`) and the six P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23g.go.txt` govern worktree branch naming (`agy/T-AUD-23g` instead of `fix/T-AUD-23g`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23g.md`.
- `firecrawl --status` reported `Credits: -7 / 1,000 (-1% left this cycle)` at session start, so no new external scrapes could be billed. Per R1 ("Reuse an earlier source (`S001`–`S041`) when it holds the fact"), all 28 claims were adjudicated from the existing authoritative `OEM`, `TRADE`, and `PRIMARY_*` corpus (`S001`, `S009`, `S018`, `S019`, `S023`, `S028`, `S029`, `S030`, `S032`, `S033`, `S034`, `S035`, `S037`), leaving `sources.csv` unchanged (`S001`–`S041`).

## Step 1 Disclosure
- `verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=10`
- `retired 0 of 28 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23g.txt claims 28`
- `UNSOURCED` claims: **0** (all 28 claims sourced; no `UNSOURCED` rows).

## 28-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0304` | `CT-002` | `NOx < 80 ppm` | `CONTRADICTED` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034); retarded timing lowers NOx (S032)` | `S028` (`TRADE`) |
| `CK0305` | `CT-002` | `NOx > 800 ppm` (lean discriminator) | `PARTLY` | `near 0 ppm at idle even when lean without load (S028, S035); < 500 ppm under load (S035); 1800-2500 ppm pre-cat / ~2000 ppm failing under load (S033); Very Lean decreases NOx (S032)` | `S028` (`TRADE`) |
| `CK0306` | `CT-002` | `stft > 2.0 %` | `CONTRADICTED` | `±8 % idle normal / -10 % to +10 % normal STFT (S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT entry (S037 OEM); cam issues keep trims normal absent misfire (S019)` | `S030` (`TRADE`) |
| `CK0307` | `CT-002` | `stft_b1 >= 2.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT / ±8 % idle normal (S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT entry (S037 OEM); cam issues keep trims normal absent misfire (S019)` | `S030` (`TRADE`) |
| `CK0309` | `CT-003` | `nox < 80.0 ppm` | `CONTRADICTED` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034); retarded timing lowers NOx (S032)` | `S028` (`TRADE`) |
| `CK0310` | `CT-003` | `stft_b1 >= 2.0 %` | `CONTRADICTED` | `±8 % idle normal / -10 % to +10 % normal STFT (S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT entry (S037 OEM); cam issues keep trims normal absent misfire (S019)` | `S030` (`TRADE`) |
| `CK0313` | `CT-004` | `stft_b1 < -5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT / ±8 % idle normal (S030); -9 % to +11 % / -13 % to +18 % closed-loop STFT entry (S037 OEM); cam issues keep trims normal absent misfire (S019)` | `S030` (`TRADE`) |
| `CK0314` | `CT-004` | `ltft_b1 < -5.0 %` | `CONTRADICTED` | `±5 to 8 % good LTFT / ±8 % normal (S030); < ±10 % acceptable LTFT and cam issues keep trims normal (S019); ±20 % combined normal / -35 % rich malfunction (S029 OEM)` | `S030` (`TRADE`) |
| `CK0316` | `CT-004` | `stft_b1 <= -5.0 %` | `CONTRADICTED` | `±8 % idle normal / -10 % to +10 % normal STFT (S030); -5 % to +5 % / -9 % to +11 % / -13 % to +18 % closed-loop STFT entry (S037 OEM); cam issues keep trims normal absent misfire (S019)` | `S030` (`TRADE`) |
| `CK0317` | `CT-004` | `ltft_b1 <= -5.0 %` | `CONTRADICTED` | `±5 to 8 % good LTFT / ±8 % normal (S030); < ±10 % acceptable LTFT (S019); ±20 % combined normal / -35 % rich malfunction (S029 OEM)` | `S030` (`TRADE`) |
| `CK0320` | `CT-005` | `VVT_HISTORY P0010-P0023` | `PARTLY` | `P0010-P0025 VCT/VVT monitor DTCs (including P0013 and P0017 in S037 OEM; P0024-P0025 Bank 2 exhaust cam timing omitted by P0010-P0023)` | `S037` (`OEM`) |
| `CK0321` | `CT-005` | `stft_b1 in_range -5 – 5 %` | `CONFIRMED` | `(matches S037 OEM -5 % to 5 % Short Term Fuel Trim Range for normal/near-zero trims; S030 ±8-10 % / S037 -13..+18 % wider)` | `S037` (`OEM`) |
| `CK0322` | `CT-005` | `ltft_b1 in_range -5 – 5 %` | `PARTLY` | `within a few percentage points of zero ideally, 5 to 8 % good LTFT / ±8 % normal (S030); < ±10 % acceptable and cam issues keep trims normal (S019); ±20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0323` | `CT-005` | `stft_b1` lower edge `-5.0 %` | `CONFIRMED` | `(matches lower edge -5 % of S037 OEM -5 % to 5 % Short Term Fuel Trim Range; S030 ±8-10 % / S037 -13..+18 % wider)` | `S037` (`OEM`) |
| `CK0324` | `CT-005` | `stft_b1` upper edge `5.0 %` | `CONFIRMED` | `(matches upper edge +5 % of S037 OEM -5 % to 5 % Short Term Fuel Trim Range; S030 ±8-10 % / S037 -13..+18 % wider)` | `S037` (`OEM`) |
| `CK0325` | `CT-005` | `ltft_b1` lower edge `-5.0 %` | `PARTLY` | `±5 to 8 % good LTFT / ±8 % normal (S030); < ±10 % acceptable (S019); ±20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0326` | `CT-005` | `ltft_b1` upper edge `5.0 %` | `PARTLY` | `±5 to 8 % good LTFT / ±8 % normal (S030); < ±10 % acceptable (S019); ±20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0329` | `CT-006` | `VVT_HISTORY P0011-P0024` | `PARTLY` | `P0010-P0025 VCT/VVT monitor DTCs (P0011-P0024 omits P0010 Bank 1 actuator circuit and P0025 Bank 2 exhaust cam over-retarded; CT-006 dtc_evidence also omits P0015 and P0025)` | `S037` (`OEM`) |
| `CK0332` | `CT-007` | `hc >= 180.0 ppm` | `PARTLY` | `Very retarded Timing -> HC Some Increase (Slightly retarded -> Some decrease) in S032; 0-35 ppm healthy idle / 75-125 ppm unlit cat (S023); < 50 ppm normal (S034); < 100 ppm good (S035); 200 ppm fast-idle MOT limit (S001, S009)` | `S032` (`TRADE`) |
| `CK0333` | `CT-007` | `co2 < 13.0 % vol` | `CONFIRMED` | `(13.0 % within 8.3 % of S032 < 12 % lack of combustion; S032 Very retarded Timing -> CO2 Some-large Decrease; below S023 14.5-16 % / S035 ~15 % / S034 13-15 %)` | `S032` (`TRADE`) |
| `CK0334` | `CT-007` | `nox < 80.0 ppm` | `CONTRADICTED` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034); retarded timing lowers NOx (S032)` | `S028` (`TRADE`) |
| `CK0336` | `CT-008` | `hc` lower edge `250.0 ppm` | `PARTLY` | `Very retarded Timing -> HC Some Increase (S032); 0-35 ppm healthy / 75-125 ppm unlit cat (S023); < 50 ppm normal / 1,600-2,000 ppm single-cylinder misfire (S034); < 100 ppm good (S035); 200 ppm fast-idle MOT limit (S001)` | `S032` (`TRADE`) |
| `CK0337` | `CT-008` | `hc` upper edge `300.0 ppm` | `PARTLY` | `Very retarded Timing -> HC Some Increase (S032); 0-35 ppm healthy / 75-125 ppm unlit cat (S023); < 50 ppm normal / 1,600-2,000 ppm single-cylinder misfire (S034); < 100 ppm good (S035); 200 ppm fast-idle MOT limit (S001)` | `S032` (`TRADE`) |
| `CK0338` | `CT-008` | `co2` lower edge `12.5 % vol` | `CONTRADICTED` | `12 - 15 % optimum CO2 and < 12 % indicates lack of combustion (S032); 13 - 15 % good (S034); 14.5 - 16 % healthy idle / 13.5 - 14.5 % unlit cat (S023); ~15 % good (S035)` | `S032` (`TRADE`) |
| `CK0339` | `CT-008` | `co2` upper edge `13.0 % vol` | `PARTLY` | `12 - 15 % optimum CO2 and < 12 % indicates lack of combustion (S032); 13 - 15 % good (S034); 14.5 - 16 % healthy idle / 13.5 - 14.5 % unlit cat (S023); ~15 % good (S035)` | `S032` (`TRADE`) |
| `CK0340` | `CT-008` | `o2` lower edge `1.5 % vol` | `CONTRADICTED` | `retarded timing -> O2 No change / No Change, < 1 % good tailpipe O2 (S032); 1 - 2 % good O2 (S034); 0 - 0.35 % healthy idle O2 (S023); <= 1 % good (S035)` | `S032` (`TRADE`) |
| `CK0341` | `CT-008` | `o2` upper edge `2.0 % vol` | `CONTRADICTED` | `retarded timing -> O2 No change / No Change, < 1 % good tailpipe O2 (S032); 1 - 2 % good O2 (S034); 0 - 0.35 % healthy idle O2 (S023); <= 1 % good (S035)` | `S032` (`TRADE`) |
| `CK0342` | `CT-008` | `nox < 40.0 ppm` | `CONTRADICTED` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034); retarded timing lowers NOx (S032)` | `S028` (`TRADE`) |

## Disputes
1. **Low-NOx cam-timing gates (`CK0304`, `CK0309`, `CK0334` `< 80 ppm`; `CK0342` `< 40 ppm`) and `lean_condition` NOx discriminator (`CK0305` `> 800 ppm`):**
   - `S032` (`Smog Tech Institute`, `TRADE`) confirms retarded timing lowers NOx (`Slightly retarded timing` and `Very retarded Timing` → `Large Decrease`; `Variable valve timing has now replaced the EGR valve on many applications`), and `S018` (`Bridge Analyzers`, `TRADE`) confirms valve timing overlap/lift/duration alters inlet charge dilution and combustion temperature like EGR.
   - However, `S028` (`Crypton`, `TRADE`) states `"NOx only occures ( in meaningful quantities) with engine under load at high temperature"` and `"NOx is naturally near 0 ppm at idle"`, corroborated by `S035` (`AVI OnDemand`, `TRADE`: `"Expect zero NOx at idle, and less than 500 ppm under load"`) and `S034` (`Underhood Service`, `TRADE`: `"low at idle"`). Therefore `< 80 ppm` and `< 40 ppm` sit inside the healthy warm-idle NOx band (`CONTRADICTED`), and `> 800 ppm` (`CK0305`) cannot discriminate lean_condition at warm idle (where NOx stays ~0 ppm per `S028`/`S035`) and is `> 20 %` away from `S035`'s `< 500 ppm` loaded ceiling and `S033`'s `~2000 ppm` loaded cat-fail (`1800–2500 ppm` pre-cat), while `S032` notes `Very Lean Mixture` actually reduces NOx (`PARTLY`).
2. **Fuel-trim deviations on cam timing (`CK0306`/`CK0307`/`CK0310` `stft > 2.0 / >= 2.0 %`; `CK0313`/`CK0314`/`CK0316`/`CK0317` `stft/ltft < -5.0 / <= -5.0 %`):**
   - All seven sit inside the healthy closed-loop STFT (`±8–10 %` in `S030`; `-5..+5 %`, `-9..+11 %`, `-13..+18 %` in `S037` `OEM`) and LTFT (`5–8 %` good / `±8 %` normal in `S030`; `< ±10 %` in `S019`; `±20 %` combined in `S029` `OEM`) bands (`CONTRADICTED`).
   - Additionally, `S019` (`Gears Magazine`, `TRADE`) explicitly states that cam issues leave fuel trims normal unless incomplete combustion or misfire develops (`"The same holds true for restricted exhaust or cam issues. Unless the engine runs so poorly that there’s incomplete combustion or a misfire, the air/fuel mixture will likely be correct"`), and `S030` notes misfire/incomplete combustion passes unburned O2 into the exhaust and drives trims **positive** (not negative as `CT-004` claims).
3. **`CT-005` "trims near zero" `in_range [-5, 5]` (`CK0321`–`CK0326`):**
   - `S019` (`TRADE`) supports normal trims on cam issues absent misfire, and `S037` (`Ford OEM`) literally specifies `Short Term Fuel Trim Range | -5% | 5%` for one closed-loop monitor (`CONFIRMED` for `CK0321`, `CK0323`, `CK0324`), though `S037` also uses `-9..+11 %` and `-13..+18 %` and `S030` puts normal STFT at `±8 %` idle / `±10 %` overall.
   - For LTFT (`CK0322`, `CK0325`, `CK0326`), `S030` (`TRADE`) sets `"within a few percentage points of zero"` ideally and `5 %` as the lower edge of `"5 to 8 percent"` good LTFT (`±8 %` normal; `S019` `< ±10 %`), so `[-5, 5]` is `> 20 %` narrower than healthy aging LTFT (`PARTLY`).
4. **VVT DTC ranges (`CK0320` `P0010-P0023`; `CK0329` `P0011-P0024`):**
   - `S037` (`Ford OEM`) `VCT Monitor Operation` documents `P0010`–`P0025` (plus `P0013`, `P0017` under `VVT`), explicitly including `P0024` (Exhaust Cam Over-Advanced Bank 2) and `P0025` (Exhaust Cam Over-Retarded Bank 2). `CT-005`'s `P0010-P0023` truncates `P0024–P0025` (even though `CT-005`'s own `dtc_evidence` includes them) and includes crank/cam correlation `P0016–P0018`, while `CT-006`'s `P0011-P0024` truncates `P0010` and `P0025` (and its `dtc_evidence` omits `P0015` and `P0025`) (`PARTLY` for both).
5. **Four-gas signatures of retarded cam timing (`CK0332`, `CK0333`, `CK0336`–`CK0341`):**
   - **HC (`CK0332` `>= 180`, `CK0336`–`CK0337` `250–300 ppm`):** `S032` reports `Very retarded Timing` raises HC (`Some Increase`, whereas `Slightly retarded timing` gives `Some decrease`), and `180–300 ppm` exceeds healthy idle (`0–35 ppm` `S023`, `< 50 ppm` `S034`, `< 100 ppm` `S035`), but no source gives `180` or `250–300 ppm` as a retarded-cam threshold (`S023` unlit cat `75–125 ppm`, `S001`/`S009` fast-idle legal limit `200 ppm`, `S034` misfire `1,600–2,000 ppm`), and capping `CT-008` (`DEFINITIVE`) at `300 ppm` excludes worse incomplete combustion (`PARTLY`).
   - **CO2 (`CK0333` `< 13.0 %`; `CK0338`–`CK0339` `12.5–13.0 %`):** Trade sources disagree on the normal floor: `S023` gives `14.5–16 %` (`13.5–14.5 %` unlit cat), `S035` `~15 %`, `S034` `13–15 %` good, and `S032` `12–15 %` optimum with `< 12 %` indicating lack of combustion (`Very retarded Timing` → `Some-large Decrease`). `< 13.0 %` (`CK0333`) sits within `8.3 %` (`< 20 %`) of `S032`'s `< 12 %` and below `S023`/`S034`/`S035` (`CONFIRMED`); `CK0339` (`<= 13.0 %` upper edge of `12.5–13.0 %`) shares the `S032`/`S034` overlap (`PARTLY`); whereas `CK0338` (`>= 12.5 %` lower edge) rejects `< 12 %` lack of combustion and sits inside `S032`'s `12–15 %` optimum (`CONTRADICTED`).
   - **O2 (`CK0340`–`CK0341` `1.5–2.0 %`):** `S032` explicitly records `No change` / `No Change` in O2 for both `Slightly retarded timing` and `Very retarded Timing`, while `S034` places `1–2 %` inside its good O2 range (versus `0–0.35 %` in `S023` and `< 1 %` in `S032`/`S035`), so `1.5–2.0 %` is unsupported for retarded cam timing (`CONTRADICTED`).

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23g.txt`):
  - `verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=10`
  - `retired 0 of 28 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23g.txt claims 28`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`, `scope/T-AUD-23f.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` (`sources.csv` unchanged, `S001`–`S041` reused)
  - Untracked: `apps/wired/audit_tasks/progress_notes/T-AUD-23g.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23g.md`; no `search/` folder.

## CODE REVIEW
- Confirmed `verdicts.csv` (28 rows in exact `T-AUD-23g.txt` order) was appended strictly below the existing `155` rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines (`sources.csv` unchanged at `38` rows / `11` primary).
- Every quote matches its cited source file (`S028`, `S030`, `S032`, `S037`) verbatim under `check_verdicts.py` whitespace-normalisation, all `TRADE` verdicts disclose `TRADE source` in `note` per R5, all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/`README.md`, and no `search/` folder or uncited `sources/` file exists.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T11:02:30Z` | `2026-11-16T11:15:19Z` | `12.8` | `ABSENT` |
