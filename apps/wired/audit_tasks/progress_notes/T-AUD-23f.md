# Progress Note — T-AUD-23f

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23f` (worktree per `T-AUD-23f.go.txt` lane rule) with spec commit `347028b` (`git log --oneline fix/T-AUD-24k..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23f.txt` fails with `VERDICTS FAIL 24 error(s)` (all `no verdict`), P3 passes on `T-GASA-17.txt` (`20`), `T-AUD-23a.txt` (`25`), `T-AUD-23b.txt` (`29`), `T-AUD-23d.txt` (`29`), and `T-AUD-23e.txt` (`28`), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 24 errors from `check_verdicts.py --scope scope/T-AUD-23f.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `131` earlier verdicts (`20 + 25 + 29 + 29 + 28`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23f.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `24` root claims (`same_as` empty): `14` in `labs/comlab/registry/rules/ecu_fault.json` and `10` in `labs/comlab/registry/rules/no_fault.json` (P1); `37` existing rows in `sources.csv` ending at `S040` so new IDs start at `S041` (P4); and `131` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23f.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 24 root claims in `scope/T-AUD-23f.txt` (ECU-fault and no-fault rule values) against authoritative sources fetched via Firecrawl into `labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md` (reusing `S001`–`S040` where applicable), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23f.txt` (`claims 24`) and the five P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23f.go.txt` govern worktree branch naming (`agy/T-AUD-23f` instead of `fix/T-AUD-23f`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23f.md`.
- `S041` (`https://www.dmv.de.gov/VehicleServices/inspections/pdfs/dtc_list.pdf`, Delaware Division of Motor Vehicles, `PRIMARY_REGULATOR`) was scraped via Firecrawl before Firecrawl account credits hit `0` (attempts for two additional trade/manual URLs failed on insufficient credits), so all remaining claims were verified against `S041` plus the rich existing corpus `S001`–`S040` (`S002`, `S011`, `S014`, `S016`, `S019`, `S023`, `S028`, `S029`, `S030`, `S032`, `S034`, `S035`, `S037`, `S038`, `S040`), as encouraged by R1.

## Step 1 Disclosure
- `verdicts CONFIRMED=8 CONTRADICTED=10 PARTLY=6`
- `retired 0 of 24 scope claims (retired.csv)`
- `sources 38 primary 11`
- `VERDICTS OK scope=T-AUD-23f.txt claims 24`
- `UNSOURCED` claims: **0** (all 24 claims sourced; no `UNSOURCED` rows).

## 24-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0377` | `EF-001` | `lambda_perception_delta > 0.02` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford UEGO ±2 % target and FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0378` | `EF-001` | `longft1 ≥ 14.0 %` | `PARTLY` | `LONGFT > 25 % for P0171 lean malfunction (S037 OEM); +35 % combined STFT+LTFT malfunction / ±20 % combined normal (S029 OEM); +20 to +25 % LTFT sets P0171 (S030 TRADE)` | `S037` (`OEM`) |
| `CK0379` | `EF-001` | `shrtft1 ≥ 20.0 %` | `PARTLY` | `LONGFT > 25 % and SHRTFT > 1 % for P0171, with -13 % to +18 % normal STFT entry range (S037 OEM); ±20 % combined normal / +35 % P0171 (S029 OEM); ±10 % STFT normal jumping to 25 %+ (S030 TRADE)` | `S037` (`OEM`) |
| `CK0382` | `EF-002` | `lambda_perception_delta < -0.02` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford UEGO ±2 % target and FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0383` | `EF-002` | `longft1 ≤ -10.0 %` | `PARTLY` | `-35 % or less average fuel trim for P0172 malfunction / within ±20 % combined normal (S029 OEM); -20 to -25 % LTFT sets P0172 while <= -10 % indicates a problem (S030 TRADE)` | `S029` (`OEM`) |
| `CK0384` | `EF-002` | `shrtft1 ≤ -15.0 %` | `PARTLY` | `-35 % or less average fuel trim for P0172 / within ±20 % combined normal (S029 OEM); -13 % to +18 % normal STFT entry (S037 OEM); ±10 % normal STFT jumping to 25 %+ and -20 to -25 % P0172 (S030 TRADE)` | `S029` (`OEM`) |
| `CK0387` | `EF-003` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford UEGO ±2 % target and FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0388` | `EF-003` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford UEGO ±2 % target and FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0389` | `EF-003` | `longft1` lower edge `-5.0 %` | `CONTRADICTED` | `±5 to 8 % normal LTFT near zero (S030 TRADE); < ±10 % acceptable (S019 TRADE); within ±20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0390` | `EF-003` | `longft1` upper edge `5.0 %` | `CONTRADICTED` | `±5 to 8 % normal LTFT near zero (S030 TRADE); < ±10 % acceptable (S019 TRADE); within ±20 % combined normal (S029 OEM)` | `S030` (`TRADE`) |
| `CK0391` | `EF-003` | `shrtft1` lower edge `-5.0 %` | `CONTRADICTED` | `-5 % to +5 % / -9 % to +11 % / -13 % to +18 % healthy closed-loop STFT monitor entry ranges (S037 OEM); -10 % to +10 % normal STFT and ±8 % idle (S030 TRADE)` | `S037` (`OEM`) |
| `CK0392` | `EF-003` | `shrtft1` upper edge `5.0 %` | `CONTRADICTED` | `-5 % to +5 % / -9 % to +11 % / -13 % to +18 % healthy closed-loop STFT monitor entry ranges (S037 OEM); -10 % to +10 % normal STFT and ±8 % idle (S030 TRADE)` | `S037` (`OEM`) |
| `CK0395` | `EF-004` | `P0600-P0699` (ECU internal DTC) | `PARTLY` | `P0600-P0699 = Computer and Auxiliary Outputs (includes internal P0601-P0606 processor/memory faults plus external P0600 serial link, P0608-P0609 VSS, P0620-P0622 generator, P0650 MIL, P0654-P0656 output circuits in S041; corroborated by S037 OEM)` | `S041` (`PRIMARY_REGULATOR`) |
| `CK0397` | `EF-005` | `CO+CO2+O2` `14 – 16 % vol` | `CONTRADICTED` | `Healthy tailpipe CO2+O2+CO = 15.84+0.48+0.02 = 16.34 % and misfire pre-cat = 16.93 % (S040); healthy idle sum up to 16.8 % (S023); statutory dilution void floor CO+CO2 < 6 % (S011 PRIMARY_LAW); optimum CO2 12-15 % (S032)` | `S040` (`TRADE`) |
| `CK0536` | `NF-001` | `co2 ≥ 14.5 % vol` | `CONFIRMED` | `(matches S023 14.5-16 % CO2 at idle for working engine and converter; S034 13-15 % and S032 12-15 % wider)` | `S023` (`TRADE`) |
| `CK0538` | `NF-001` | `nox ≤ 50.0 ppm` | `PARTLY` | `near 0 ppm at idle (S028); zero NOx at idle and < 500 ppm under load (S035); low at idle (S034)` | `S028` (`TRADE`) |
| `CK0539` | `NF-001` | `obd_lambda` lower edge `0.97` | `CONFIRMED` | `(matches statutory 1 ± 0.03 = 0.97-1.03 catalyst lambda window in S002, S001, S009; S037 OEM ±2 % UEGO target)` | `S002` (`PRIMARY_LAW`) |
| `CK0540` | `NF-001` | `obd_lambda` upper edge `1.03` | `CONFIRMED` | `(matches statutory 1 ± 0.03 = 0.97-1.03 catalyst lambda window in S002, S001, S009; S037 OEM ±2 % UEGO target)` | `S002` (`PRIMARY_LAW`) |
| `CK0543` | `NF-002` | `hc ≤ 30.0 ppm` | `CONFIRMED` | `(within 14.3 % of S023 0-35 ppm healthy working engine and converter idle HC; S034 < 50 ppm, S035 < 100 ppm, S001/S009 200 ppm fast-idle)` | `S023` (`TRADE`) |
| `CK0544` | `NF-002` | `co ≤ 0.05 % vol` | `CONTRADICTED` | `0.1 - 0.45 % CO at idle for properly functioning engine and converter (< 0.5 % balanced in S023); <= 0.3 % idle / <= 0.2 % fast-idle statutory limit (S001, S002, S009); < 0.5 % good (S035); ± 0.06 % Class I CO MPE (S014)` | `S023` (`TRADE`) |
| `CK0545` | `NF-002` | `co2 ≥ 14.6 % vol` | `CONFIRMED` | `(within 0.7 % of S023 14.5-16 % healthy working engine and converter idle CO2; S035 ~15 %, S040 15.84 % tailpipe; S034 13-15 %, S032 12-15 %)` | `S023` (`TRADE`) |
| `CK0546` | `NF-002` | `o2 ≤ 0.5 % vol` | `CONFIRMED` | `(matches S023 <.5 % balanced and S040 ~0.5 % / 0.48 % tailpipe; S023 table 0-0.35 %, S032/S035 < 1 %, S034 1-2 %)` | `S023` (`TRADE`) |
| `CK0548` | `NF-002` | `obd_lambda` lower edge `0.97` | `CONFIRMED` | `(matches statutory 1 ± 0.03 = 0.97-1.03 catalyst lambda window in S002, S001, S009; S037 OEM ±2 % UEGO target)` | `S002` (`PRIMARY_LAW`) |
| `CK0549` | `NF-002` | `obd_lambda` upper edge `1.03` | `CONFIRMED` | `(matches statutory 1 ± 0.03 = 0.97-1.03 catalyst lambda window in S002, S001, S009; S037 OEM ±2 % UEGO target)` | `S002` (`PRIMARY_LAW`) |

## Disputes
1. **`lambda_perception_delta` `±0.02` (`CK0377`, `CK0382`) and `±0.03` (`CK0387`, `CK0388`):** `S038` (*Hot Rod* Horiba lab test, `TRADE`) measures `1–2 %` combustion instability plus `±2 %` wideband accuracy target (up to `5 %` across units), `S040` (*MOTOR Magazine*, `TRADE`) puts healthy engine analyser Lambda at `±5 %` of 1, `S016` (`Bosch LSU 4.9`, `OEM`) specifies `1.016 ± 0.007` at λ=1, and `S014` (`OIML R 99`, `PRIMARY_STANDARD`) permits `0.3 %` calculation MPE plus gas channel MPEs. Meanwhile `S037` (`Ford`, `OEM`) holds closed-loop UEGO within `±2 %` (`±0.02`) and sets its actual FAOS rear-bias malfunction threshold at `-0.083 / +0.087`. Both `±0.02` and `±0.03` therefore sit inside combined healthy variation (`CONTRADICTED`).
2. **Fuel-trim saturation thresholds (`CK0378` LTFT `≥ 14.0 %`, `CK0379` STFT `≥ 20.0 %`, `CK0383` LTFT `≤ -10.0 %`, `CK0384` STFT `≤ -15.0 %`):** `S030` (`AA1Car`, `TRADE`) and `S019` (`Gears Magazine`, `TRADE`) treat `±10 %` LTFT as the onset of a fuel-trim problem (`5–8 %` normal aging) and `±20 to ±25 %` LTFT as typical P0171/P0172 thresholds, whereas OEM manuals set P0171/P0172 higher (`> 25 %` LTFT with `SHRTFT > 1 %` in `S037` `Ford OEM`; `±35 %` combined average in `S029` `Toyota OEM`, which treats `±20 %` combined as normal). All four `EF-001`/`EF-002` gates point in the right direction but sit `> 20 %` below OEM saturation (`PARTLY`).
3. **`P0600-P0699` scope (`CK0395`):** `EF-004` describes `P0600-P0699` solely as ECU internal hardware/software faults (and its `dtc_evidence` only checks `P0606`), whereas `S041` (`Delaware DMV`, `PRIMARY_REGULATOR`) defines `6 = COMPUTER AND AUXILIARY OUTPUTS` (`P0600-P0699 – Computer Output Circuit`) containing internal processor/memory codes (`P0601–P0606`, corroborated by `S037` `OEM` `P0602–P060C`) alongside external serial communication (`P0600`), VSS (`P0608–P0609`), generator (`P0620–P0622`), MIL (`P0650`), RPM (`P0654`), hot-lamp (`P0655`), and fuel-level (`P0656`) output circuits (`PARTLY`).
4. **Triangle gas sum `CO + CO2 + O2` in `14 – 16 % vol` (`CK0397`):** `S040` (`TRADE`) shows a real healthy tailpipe baseline at `15.84 + 0.48 + 0.02 = 16.34 %` (and pre-cat `16.10 %`, misfire pre-cat `16.93 %`), and `S023` (`TRADE`) healthy idle ranges (`CO2 14.5-16 % + O2 0-0.35 % + CO 0.1-0.45 %`) reach `16.8 %`, so the `16 %` upper cap rejects healthy tailpipe and genuine lean/misfire samples; meanwhile `S011` (`40 CFR 85.2215`, `PRIMARY_LAW`) sets the statutory dilution-void floor at `CO + CO2 < 6 %`, and `S032` (`12–15 %` optimum CO2) admits valid readings below `14 %` (`CONTRADICTED`). Also conflicts internally with `GAS_VOCABULARY §10.6` (`< 14` or `≥ 18`, with `16–18` as `EXTERNAL_O2_SUSPECT`).
5. **Warm-idle healthy `no_fault` bands (`CK0536`, `CK0538`, `CK0539`, `CK0540`, `CK0543`–`CK0546`, `CK0548`, `CK0549`):**
   - `CO <= 0.05 %` (`CK0544`): `S023` (`TRADE`) gives `0.1 - 0.45 %` healthy idle CO (`normally not zero`), `S001`/`S002`/`S009` (`PRIMARY_*`) allow up to `0.3 %` idle (`0.2 %` fast idle), `S035` gives `< 0.5 %`, and `S014` (`OIML R 99`) gives `± 0.06 % vol` Class I CO MPE (`CONTRADICTED`), even though `S040` shows a clean car at `0.02 %`.
   - `CO2 >= 14.5 / 14.6 %` (`CK0536`, `CK0545`) and `HC <= 30.0 ppm` (`CK0543`): `S023` specifically distinguishes working-cat idle (`14.5–16 % CO2`, `0–35 ppm HC`) from unlit converter (`13.5–14.5 % CO2`, `75–125 ppm HC`), confirming both within `20 %`, whereas `S034` (`13–15 % CO2`, `< 50 ppm HC`) and `S032` (`12–15 % CO2`) / `S035` (`< 100 ppm HC`) / `S001` (`200 ppm` legal fast-idle) give wider healthy tolerances.
   - `O2 <= 0.5 %` (`CK0546`): matches `S023` (`<.5% Balanced with <.5 CO`) and `S040` (`~.5%`, `0.48 %` baseline), while `S023`'s idle table lists `0–0.35 %` (`0.3–0.7 %` unlit cat), `S032`/`S035` give `< 1 %`, and `S034` gives `1–2 %`.
   - `obd_lambda` `0.97–1.03` (`CK0539`, `CK0540`, `CK0548`, `CK0549`): `S002`/`S001`/`S009` (`PRIMARY_*`) define `1 ± 0.03` for tailpipe lambda at raised idle, whereas `NF-001`/`NF-002` check `obd_lambda` (which `S037` `OEM` keeps within `±2 %` / `0.98–1.02` in healthy closed-loop, inside `0.97–1.03`).

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23f.txt`):
  - `verdicts CONFIRMED=8 CONTRADICTED=10 PARTLY=6`
  - `retired 0 of 24 scope claims (retired.csv)`
  - `sources 38 primary 11`
  - `VERDICTS OK scope=T-AUD-23f.txt claims 24`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`, `scope/T-AUD-23e.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/sources.csv`, `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv`
  - Untracked: `labs/gaslab/audit_tasks/wikiaudit/sources/S041.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23f.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23f.md`; `search/` deleted.

## CODE REVIEW
- Confirmed `sources.csv` (`S041`) and `verdicts.csv` (24 rows in exact `T-AUD-23f.txt` order) were appended strictly below existing rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines.
- Cited new source file `S041.md` exists under `labs/gaslab/audit_tasks/wikiaudit/sources/`, `search/` was deleted per R3, every quote matches its source file (whitespace-normalised, case-sensitive), all `TRADE` verdicts disclose so in `note` per R5, and all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/README.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T10:42:25Z` | `2026-11-16T10:50:48Z` | `8.4` | `ABSENT` |
