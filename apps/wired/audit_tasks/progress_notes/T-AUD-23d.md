# Progress Note — T-AUD-23d

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23d` (worktree per `T-AUD-23d.go.txt` lane rule) with spec commit `f780041` (`git log --oneline fix/T-GASA-19..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23d.txt` fails with `VERDICTS FAIL 29 error(s)` (all `no verdict`), `check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, and `scope/T-AUD-23b.txt` pass with `20`, `25`, and `29` claims respectively (P3), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 29 errors from `check_verdicts.py --scope scope/T-AUD-23d.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the 74 earlier verdicts (`20` + `25` + `29`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23d.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `29` root claims (`same_as` empty), all located in `labs/comlab/registry/rules/{misfire,rich_mixture,lean_condition,catalyst_failure}.json` (P1), `25` existing rows in `sources.csv` ending at `S028` so new IDs start at `S029` (P4), and `74` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23d.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 29 root claims in `scope/T-AUD-23d.txt` (fuel trims, exhaust gases, lambda, MAP, and MAF gates in the MF, RM, LC, and CF rules) against authoritative sources fetched via Firecrawl into `labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md` (reusing `S001`–`S028` where applicable), and append rows to `sources.csv` and `verdicts.csv` without modifying any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23d.txt` (`claims 29`) and the three P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23d.go.txt` govern worktree branch naming (`agy/T-AUD-23d` instead of `fix/T-AUD-23d`), disallow `git commit`/`git push`, and omit the branch/log paste from `RESULT_T-AUD-23d.md`.
- Fuel-trim `±10.0 %` LTFT gates (`CK0351`, `CK0441`, `CK0612`) are judged `CONFIRMED` against trade training texts (`S019`, `S030`) that explicitly name `±10 %` as the diagnostic boundary, while documenting OEM combined-trim/DTC thresholds (`S029` Toyota `20 %` combined normal, `±35 %` DTC) in `note` and `Disputes`; `±8.0 %` (`CK0448`, `CK0516`, `CK0615`), `±5.0 %` (`CK0442`, `CK0517`, `CK0520`, `CK0613`, `CK0619`), and `3.0 %` (`CK0444`) sit inside/at the healthy `±8 %` / `< ±10 %` band and are judged `CONTRADICTED`.

## Step 1 Disclosure
- `verdicts CONFIRMED=7 CONTRADICTED=14 PARTLY=8`
- `retired 0 of 29 scope claims (retired.csv)`
- `sources 33 primary 10`
- `VERDICTS OK scope=T-AUD-23d.txt claims 29`
- `UNSOURCED` claims: **0** (all 29 claims sourced; no `UNSOURCED` rows).

## 29-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0347` | `CF-001` | `nox ≥ 250.0 ppm` | `PARTLY` | `Expect zero NOx at idle, and less than 500 ppm under load (S035); near 0 ppm at idle (S028); pre-cat 1800-2500 ppm reduced by ~2000 ppm under load (S033)` | `S035` (`TRADE`) |
| `CK0348` | `CF-001` | `co2 ≤ 14.0 % vol` | `CONFIRMED` | `(13.5-14.5 % converter not lighting off vs 14.5-16 % healthy idle CO2 in S023; <= 14.0 % within 3.4 % of 14.5 %)` | `S023` (`TRADE`) |
| `CK0351` | `CF-002` | `longft1 ≥ 10.0 %` | `CONFIRMED` | `(> +/-10 % out-of-range LTFT in S019; >= +10 % problem in S030)` | `S019` (`TRADE`) |
| `CK0352` | `CF-002` | `hc < 100.0 ppm` | `CONTRADICTED` | `0 - 35 ppm HC at idle for a properly functioning engine and converter; 75 - 125 ppm indicates converter not lighting off` | `S023` (`TRADE`) |
| `CK0355` | `CF-003` | `co2 ≤ 11.0 % vol` | `CONFIRMED` | `(CO2 under 12 % indicates lack of combustion in S032; 11.0 % within 8.3 % of 12 %)` | `S032` (`TRADE`) |
| `CK0356` | `CF-003` | `o2 ≥ 4.0 % vol` | `PARTLY` | `0.5 - 1.0 % closed-loop O2; 3.0 % upstream O2 shuts down catalyst NOx reduction (S033); 0 - 0.35 % idle O2 with working cat (S023), < 1 % tailpipe (S032, S035)` | `S033` (`TRADE`) |
| `CK0358` | `CF-004` | `co2 ≥ 13.0 % vol` | `CONTRADICTED` | `14.5 - 16 % CO2 at idle for properly functioning engine and converter; 13.5 - 14.5 % for converter not lighting off` | `S023` (`TRADE`) |
| `CK0362` | `CF-005` | `nox ≥ 150.0 ppm` | `PARTLY` | `Expect zero NOx at idle, and less than 500 ppm under load (S035); near 0 ppm at idle (S028)` | `S035` (`TRADE`) |
| `CK0367` | `CF-007` | `hc ≥ 150.0 ppm` | `CONFIRMED` | `(0-35 ppm healthy vs 75-125 ppm converter not lighting off in S023; 150 ppm is +20.0 % above 125 ppm)` | `S023` (`TRADE`) |
| `CK0441` | `LC-001` | `longft1 ≥ 10.0 %` | `CONFIRMED` | `(> +/-10 % out-of-range LTFT in S019; +10 % or higher indicates lean in S030)` | `S019` (`TRADE`) |
| `CK0442` | `LC-001` | `shrtft1 ≥ 5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (S030); normal range may be as high as +/-8 %` | `S030` (`TRADE`) |
| `CK0444` | `LC-002` | `longft1 ≥ 3.0 %` | `CONTRADICTED` | `total STFT + LTFT within +/-20 % is normal; P0171 lean malfunction threshold >= +35 % (S029 OEM); +/-8 % normal / >= +10 % problem in S030` | `S029` (`OEM`) |
| `CK0445` | `LC-002` | `map_kpa < 40.0 kPa` | `CONTRADICTED` | `30 - 50 kPa normal MAP range at idle (S036)` | `S036` (`TRADE`) |
| `CK0447` | `LC-003` | `maf < 3.5 g/s` | `CONTRADICTED` | `2 to 7 g/s normal MAF PID value at idle depending on engine size (S020); ~1 g/s per litre displacement (S019)` | `S020` (`TRADE`) |
| `CK0448` | `LC-003` | `longft1 ≥ 8.0 %` | `CONTRADICTED` | `+/-8 % normal STFT/LTFT range (5-8 % normal aging LTFT in S030; +/- <10 % acceptable in S019); problem at >= +10 %` | `S030` (`TRADE`) |
| `CK0513` | `MF-001` | `hc ≥ 200.0 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal late-model HC in S034); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal ceiling (S001)` | `S034` (`TRADE`) |
| `CK0514` | `MF-001` | `o2 ≥ 1.5 % vol` | `PARTLY` | `0 - 0.35 % O2 (< 0.5 % balanced) at idle for working engine and converter (S023); < 1 % normal tailpipe O2 (S032, S035)` | `S023` (`TRADE`) |
| `CK0516` | `MF-002` | `longft1 ≥ 8.0 %` | `CONTRADICTED` | `+/-8 % normal STFT/LTFT range (5-8 % normal aging LTFT in S030; +/- <10 % acceptable in S019); problem at >= +10 %` | `S030` (`TRADE`) |
| `CK0517` | `MF-002` | `shrtft1 ≥ 5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (S030); normal range may be as high as +/-8 %` | `S030` (`TRADE`) |
| `CK0520` | `MF-003` | `longft1 ≤ -5.0 %` | `CONTRADICTED` | `+/-8 % normal LTFT range (5-8 % normal depending on engine condition in S030); +/- <10 % acceptable (S019); problem at <= -10 %` | `S030` (`TRADE`) |
| `CK0524` | `MF-004` | `hc < 200.0 ppm` | `CONTRADICTED` | `0 - 35 ppm HC at idle for properly functioning engine and converter (S023); < 50 ppm late-model (S034); 200 ppm is MOT fast-idle legal limit (S001)` | `S023` (`TRADE`) |
| `CK0527` | `MF-005` | `hc ≥ 200.0 ppm` | `PARTLY` | `1,600 to 2,000 ppm HC for one misfiring spark plug (< 50 ppm normal late-model HC in S034); 0 - 35 ppm healthy idle (S023); 200 ppm MOT fast-idle legal ceiling (S001)` | `S034` (`TRADE`) |
| `CK0528` | `MF-005` | `o2 ≥ 1.5 % vol` | `PARTLY` | `0 - 0.35 % O2 (< 0.5 % balanced) at idle for working engine and converter (S023); < 1 % normal tailpipe O2 (S032, S035)` | `S023` (`TRADE`) |
| `CK0611` | `RM-001` | `lambda_chem < 0.97` | `CONFIRMED` | `(matches 1 +/- 0.03 statutory catalyst lambda window 0.97-1.03 in S002, S001, S009)` | `S002` (`PRIMARY_LAW`) |
| `CK0612` | `RM-001` | `longft1 ≤ -10.0 %` | `CONFIRMED` | `(> +/-10 % out-of-range LTFT in S019; <= -10 % rich problem in S030)` | `S019` (`TRADE`) |
| `CK0613` | `RM-001` | `shrtft1 ≤ -5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (S030); normal range may be as high as +/-8 %` | `S030` (`TRADE`) |
| `CK0615` | `RM-002` | `longft1 ≤ -8.0 %` | `CONTRADICTED` | `+/-8 % normal LTFT range (5-8 % normal depending on engine condition in S030); +/- <10 % acceptable (S019); problem at <= -10 %` | `S030` (`TRADE`) |
| `CK0619` | `RM-003` | `longft1 ≤ -5.0 %` | `CONTRADICTED` | `+/-8 % normal LTFT range (5-8 % normal depending on engine condition in S030); +/- <10 % acceptable (S019); problem at <= -10 %` | `S030` (`TRADE`) |
| `CK0622` | `RM-004` | `longft1 ≤ -15.0 %` | `PARTLY` | `-35 % LTFT in GDI HPFP internal crankcase leak case (GM Bulletin 14858, S031); -20 to -25 % typical P0172 rich DTC threshold (S030); -10 % LTFT problem boundary (S019, S030)` | `S031` (`TRADE`) |

## Disputes
1. **Fuel-trim `±10.0 %` vs `±8.0 %` vs OEM DTC thresholds (`CK0351`, `CK0441`, `CK0612`, `CK0448`, `CK0516`, `CK0615`):** `S019` (`Gears Magazine`, `TRADE`) and `S030` (`AA1Car`, `TRADE`) name `±10 %` as the LTFT fault-investigation boundary (`CONFIRMED` on `CK0351`, `CK0441`, `CK0612`), while `S030` puts normal aging LTFT at `5–8 %` (`Normal range may be high as plus or minus 8`, contradicting `±8.0 %` on `CK0448`, `CK0516`, `CK0615`) and P0171/P0172 DTC triggers at `±20–25 %`; meanwhile `S029` (`Toyota RAV4 2AZ-FE Repair Manual`, `OEM`) accepts total STFT+LTFT within `±20 %` as normal and sets P0171/P0172 at `±35 %`.
2. **`CK0348` (`CF-001` `co2 ≤ 14.0 %`) and `CK0358` (`CF-004` `co2 ≥ 13.0 %`):** `S023` (`Walker Exhaust`, `TRADE`) puts working-converter idle CO2 at `14.5–16 %` and non-lit-off converter CO2 at `13.5–14.5 %` (confirming `CK0348` `≤ 14.0 %`, and contradicting unbounded `CK0358` `≥ 13.0 %` which fires on `14.5–16 %` healthy readings), whereas `S032` (`Smog Tech Institute`, `TRADE`, `12–15 %` optimum; `> 12 %` healthy engine even with failing cat) and `S034` (`Underhood Service`, `TRADE`, `13–15 %` good) overlap `13.0–14.5 %`.
3. **`CK0355` (`CF-003` `co2 ≤ 11.0 %`):** `S032` (`Smog Tech Institute`, `TRADE`) states `CO2 under 12%` indicates lack of combustion (within `8.3 %` of `11.0 %` → `CONFIRMED`), whereas `S023` (`Walker Exhaust`) gives `13.5–14.5 %` for unlit catalyst and `S032` attributes `< 12 %` to general combustion loss rather than specifically catalyst flow restriction.
4. **`CK0352` (`CF-002` `hc < 100.0 ppm`) and `CK0367` (`CF-007` `hc ≥ 150.0 ppm`):** `S023` (`Walker Exhaust`, `TRADE`) puts working-converter idle HC at `0–35 ppm` and unlit converter at `75–125 ppm` (contradicting `CK0352` `< 100.0 ppm` as "pristine" and confirming `CK0367` `≥ 150.0 ppm` within `+20.0 %` of `125 ppm`; `S034` gives `< 50 ppm`), whereas `S035` (`AVI OnDemand`, `TRADE`) says `< 100 ppm` is good and `S001`/`S009` (`PRIMARY_REGULATOR`) set the UK MOT fast-idle statutory ceiling at `200 ppm`.
5. **`CK0513` / `CK0527` (`hc ≥ 200.0 ppm`) and `CK0514` / `CK0528` (`o2 ≥ 1.5 %`) for ignition misfire:** `S034` (`Underhood Service`, `TRADE`) cites `1,600–2,000 ppm` HC for a misfiring spark plug (`> 20 %` above `200 ppm` → `PARTLY`, while `S001` uses `200 ppm` as the UK MOT statutory ceiling); for O2, `S023` (`0–0.35 %`), `S032` (`< 1 %`), and `S035` (`≤ 1 %`) place `1.5 %` above healthy idle (`> 20 %` above `1 %` → `PARTLY`), whereas `S034` (`Underhood Service`) gives `1–2 %` as a good O2 range.
6. **`CK0611` (`RM-001` `lambda_chem < 0.97`):** `S002` (`Directive 2014/45/EU`, `PRIMARY_LAW`, corroborated by `S001`/`S009`) sets the statutory catalyst lambda window at `1 ± 0.03` (`0.97–1.03`), confirming `< 0.97` as rich outside the statutory window; by contrast `GASLab`/`COMLab` internal wiki `W0411` defines `RICH_MIXTURE` as `λ < 0.95` and `W1238` puts `0.92–0.97` in `BORDERLINE_RICH`.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23d.txt`):
  - `verdicts CONFIRMED=7 CONTRADICTED=14 PARTLY=8`
  - `retired 0 of 29 scope claims (retired.csv)`
  - `sources 33 primary 10`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/sources.csv`, `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv`
  - Untracked: `labs/gaslab/audit_tasks/wikiaudit/sources/S029.md`–`S036.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23d.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23d.md`; `search/` deleted.

## CODE REVIEW
- Confirmed `sources.csv` (`S029`–`S036`) and `verdicts.csv` (29 rows in exact `T-AUD-23d.txt` order) were appended strictly below existing rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines.
- All 8 cited new source files (`S029.md`–`S036.md`) exist under `labs/gaslab/audit_tasks/wikiaudit/sources/`, unused scrapes and `search/` were deleted per R3, every quote matches its source file (whitespace-normalised, case-sensitive), all `TRADE` verdicts disclose so in `note` per R5, and all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/README.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T09:19:13Z` | `2026-11-16T09:30:52Z` | `11.7` | `ABSENT` |
