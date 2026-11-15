# Progress Note — T-AUD-23b

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23b` (worktree per `T-AUD-23b.go.txt` lane rule) with spec commit `8d95634` (`git log --oneline fix/T-AUD-23a..HEAD`), `git status --porcelain` empty, `check_verdicts.py --scope scope/T-AUD-23b.txt` fails with `VERDICTS FAIL 29 error(s)` (all `no verdict`), `check_verdicts.py --scope scope/T-GASA-17.txt` passes with `VERDICTS OK scope=T-GASA-17.txt claims 20` and `check_verdicts.py --scope scope/T-AUD-23a.txt` passes with `VERDICTS OK scope=T-AUD-23a.txt claims 25` (P3), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 29 errors from `check_verdicts.py --scope scope/T-AUD-23b.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently contains only the 20 `T-GASA-17` and 25 `T-AUD-23a` rows.
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23b.txt`, `claims_comlab.csv`, `claims_rest.csv`, `sources.csv`, and `verdicts.csv` confirms 29 root claims (`same_as` empty: 19 in `claims_comlab.csv`, 10 in `claims_rest.csv`), 8 linked claims pointing to them via `same_as` (P1), 10 existing rows in `sources.csv` (`S001`, `S002`, `S004`, `S005`, `S007`, `S008`, `S009`, `S011`, `S012`, `S013`; new IDs start at `S014`, P5), and 45 existing rows in `verdicts.csv` (P2=29, P3=20 and 25).
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23b.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 29 root claims in `scope/T-AUD-23b.txt` (O2 sensor, coolant sensor, airflow/VE, and exhaust-gas/analyser values) against authoritative sources fetched via Firecrawl into `labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md` (or reusing `S001`–`S013` where applicable), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23b.txt` (`claims 29`), `T-GASA-17.txt` (`claims 20`), and `T-AUD-23a.txt` (`claims 25`), `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23b.go.txt` govern worktree branch naming (`agy/T-AUD-23b` instead of `fix/T-AUD-23b`), disallow `git commit`/`git push`, and omit the branch/log paste from `RESULT_T-AUD-23b.md`.

## Step 1 Disclosure
- `verdicts CONFIRMED=5 CONTRADICTED=9 PARTLY=15`
- `sources 25 primary 10`
- `VERDICTS OK scope=T-AUD-23b.txt claims 29`
- `UNSOURCED` claims: **0** (all 29 claims sourced; no `UNSOURCED` rows).

## 29-Verdict Table

| claim | value | verdict | source_value | source |
|---|---|---|---|---|
| `CK0432` | `~16 % vol` | `CONFIRMED` | `(matches 14.5-16 % CO2 at idle, S023; 0-16 % vol OIML R 99 range, S014)` | `S023` (`TRADE`) |
| `CK0537` | `≤ 0.6 % vol` | `CONTRADICTED` | `0 - 0.35 % O2 at idle for working engine and converter (< 0.5 % balanced); 0.3 - 0.7 % indicates converter not lighting off` | `S023` (`TRADE`) |
| `CK0547` | `≤ 300.0 ppm` | `CONTRADICTED` | `near 0 ppm at idle (healthy engine); meaningful NOx requires high combustion temperature under load` | `S028` (`TRADE`) |
| `CK0635` | `> 0.80 V` | `CONFIRMED` | `(matches ~0.8 V narrowband rich plateau when pegged, S024)` | `S024` (`TRADE`) |
| `CK0638` | `≥ 0.8 V` | `PARTLY` | `~0.10-0.90 V normal closed-loop switching (~0.8 V rich plateau in S024); pegged-rich fault requires no switching` | `S021` (`TRADE`) |
| `CK0859` | `> 0.7 V` | `PARTLY` | `0.7 V is a valid rich-zone example in CARB 13 CCR 1968.2 (e)(7.2.2)(C)(ii) (S027); typical narrowband rich swings reach 0.8-0.9 V (S024, S021)` | `S027` (`PRIMARY_LAW`) |
| `CK0714` | `0.4 V` | `CONTRADICTED` | `deteriorated TWC causes rear HO2 voltage to fluctuate up and down frequently across lean/rich (~0.1-0.9 V, S017 OEM); healthy TWC rear O2 hovers ~0.7 V (S024) and steady 0.4-0.5 V indicates sensor failure (S026)` | `S017` (`OEM`) |
| `CK0715` | `0.5 V` | `CONTRADICTED` | `deteriorated TWC causes rear HO2 voltage to fluctuate up and down frequently across lean/rich (~0.1-0.9 V, S017 OEM); healthy TWC rear O2 hovers ~0.7 V (S024) and steady 0.4-0.5 V indicates sensor failure (S026)` | `S017` (`OEM`) |
| `CK1021` | `> 0.5 Hz` | `CONFIRMED` | `(matches 0.5-2 times/s healthy upstream switching at idle)` | `S026` (`TRADE`) |
| `CK1022` | `< 0.25 Hz` | `PARTLY` | `0.5-2 Hz healthy upstream switching at idle (< 0.5 Hz is already slow/lazy; S021 gives 1-5 Hz)` | `S026` (`TRADE`) |
| `CK1350` | `1-2 Hz` | `CONFIRMED` | `(within 0.5-2 times/s at idle in S026 and 1-5 Hz swing in S021)` | `S026` (`TRADE`) |
| `CK1359` | `2-8 g/s per litre` | `CONTRADICTED` | `~1 g/s per litre of engine displacement at warm idle (2-7 g/s total at idle across passenger engines in S020)` | `S019` (`TRADE`) |
| `CK1371` | `2-6 g/s` | `PARTLY` | `~2 g/s at warm idle for a 2.0 L engine per ~1 g/s/L rule (S019); 2-7 g/s total spans small to large engines (S020)` | `S020` (`TRADE`) |
| `CK1368` | `> 80 °C` | `PARTLY` | `>= 75 °C (167 °F) OEM catalyst monitor enabling condition (S017); >= 71.1 °C (160 °F) CARB warm-up cycle (S027 PRIMARY_LAW)` | `S017` (`OEM`) |
| `CK1374` | `-40 °C` | `PARTLY` | `-40 °C (-40 °F) open-circuit / cold-bias default holds, but corresponds to extremely high/open resistance (~45,313 ohm at -40 °C in S015 OEM), not 'stuck at low resistance'` | `S025` (`TRADE`) |
| `CK1376` | `2-3 kohm` | `CONTRADICTED` | `243 ohm (~0.24 kohm) at 90 °C (Bosch NTC M12); 2,500 ohm (2.5 kohm +/- 5 %) is at 20 °C` | `S015` (`OEM`) |
| `CK1378` | `> 10 kohm` | `CONTRADICTED` | `2.5 kohm +/- 5 % (2,500 ohm) at 20 °C (Bosch NTC M12); > 10 kohm occurs below -5 to -10 °C` | `S015` (`OEM`) |
| `CK1326` | `< 120 ppm` | `CONTRADICTED` | `0 - 35 ppm HC at idle for a properly functioning engine and catalytic converter (< 35 ppm rule; 75 - 125 ppm indicates converter not lighting off)` | `S023` (`TRADE`) |
| `CK0189` | `0.0 – 200.0 %` | `PARTLY` | `Volumetric efficiency > 100 % occurs with forced induction (turbo/supercharged); naturally aspirated physical limit is ~130 %` | `S022` (`SECONDARY`) |
| `RK0087` | `0.0 - 200.0 %` | `PARTLY` | `Volumetric efficiency > 100 % occurs with forced induction; naturally aspirated physical limit is ~130 % (S022)` | `S022` (`SECONDARY`) |
| `RK0062` | `90.0 %` | `CONTRADICTED` | `>= 90 % VE indicates healthy full-load breathing (S019; S022 notes NA peaks up to ~130 % and forced induction > 100 %)` | `S019` (`TRADE`) |
| `RK0014` | `0.50 V` | `PARTLY` | `~0.45 V stoichiometric midpoint (S021; 0.450 V center in S024); ~0.4-0.5 V steady mid-range zone in S026` | `S021` (`TRADE`) |
| `RK0268` | `0.0 -` | `PARTLY` | `lambda 0.65 minimum measuring range on Bosch LSU 4.9 wideband sensor (S016 OEM); SAE J1979 PID 24/34/44 encoding starts at 0 (S012 SECONDARY)` | `S016` (`OEM`) |
| `RK0269` | `3.0 -` | `PARTLY` | `lambda 0.65 to air/infinity on Bosch LSU 4.9 (S016 OEM); standard OBD-II PID 24/34/44 caps at < 2 (S012 SECONDARY)` | `S016` (`OEM`) |
| `RK0275` | `1.5 V` | `PARTLY` | `0-1 V physical narrowband O2 output (~0.10-0.90 V in S021 TRADE); OBD-II PID 14/15 max 1.275 V (S012 SECONDARY)` | `S021` (`TRADE`) |
| `RK0362` | `22.0 %` | `PARTLY` | `0 to 16 % vol CO2 measuring range in OIML R 99 Table 1 (S014 PRIMARY_STANDARD); stoichiometric petrol exhaust max ~14.5-16 % (S023)` | `S014` (`PRIMARY_STANDARD`) |
| `RK0365` | `22.0 %` | `PARTLY` | `20.9 % vol atmospheric O2 reference (0 to 21 % vol OIML R 99 Table 1 O2 measuring range)` | `S014` (`PRIMARY_STANDARD`) |
| `RK0410` | `14.7 mass ratio` | `CONFIRMED` | `(matches commonly referred 14.7:1 petrol stoichiometry; S018 also notes 14.66:1 and 14.71:1)` | `S018` (`TRADE`) |
| `RK0416` | `25.0 %` | `PARTLY` | `0 to 5 % vol CO minimum measuring range in OIML R 99 Table 1 (exceeds typical 15-15.5 % commercial analyser ceiling; ui_payload.py:16 GAS_CO_MAX is 15.0 %)` | `S014` (`PRIMARY_STANDARD`) |

## Disputes
1. **`CK0432` (`CO2 ceiling ~16 % vol`):** `S023` (Walker Exhaust, `14.5 - 16%`) and `S014` (OIML R 99 Table 1, `0 to 16 % vol` measuring range) support `~16 %`, whereas theoretical dry stoichiometric gasoline peaks at `~14.7–15.5 %` (COMLab wiki `W0194` states `~15.5 %`). Decided `CONFIRMED` on `~16 %` per `S023` and `S014`.
2. **`CK0635` (`> 0.80 V`), `CK0638` (`≥ 0.8 V`), and `CK0859` (`> 0.7 V`) (upstream narrowband O2 stuck-rich threshold):** `S027` (`CARB 13 CCR 1968.2`, `PRIMARY_LAW`) cites `0.7 Volts` as an example rich condition (`CK0859`), `S024` (`Underhood Service`, `TRADE`) gives `0.8 volts (rich)` (`CK0635`, `CK0638`), `S021` (`Fluke`, `TRADE`) gives `≈0.90V (rich)`, and internal `OBD_VOCABULARY §12.1` requires `pinned > 0.85 V`. `CK0635` (which explicitly states pegged/no-switching) is `CONFIRMED`; `CK0638` (instantaneous `>= 0.8 V` gating without duration/no-switching) and `CK0859` (`> 0.7 V`) are `PARTLY`.
3. **`CK1021` (`> 0.5 Hz`), `CK1022` (`< 0.25 Hz`), and `CK1350` (`1-2 Hz`) (upstream O2 switching frequency):** `S026` (`Apex Tech Nation`, `TRADE`) puts healthy warm-idle switching at `0.5-2 times per second` (`Hz`), confirming `CK1021` and `CK1350`, whereas `S021` (`Fluke`, `TRADE`) gives `1–5Hz swing` and `OBD_VOCABULARY §12.1` states `2–5 Hz (MPI) / 2–3 Hz (TBI)` with `< 0.5 Hz` slow/dying (leaving a `0.25–0.5 Hz` blind band on `CK1022` `< 0.25 Hz` -> `PARTLY`).
4. **`CK1368` (`catalyst efficiency test ECT precondition > 80 °C`):** `S017` (`Toyota RAV4 2GR-FE manual`, `OEM`) enables P0420 monitoring at `75°C (167°F) or more`, `S027` (`CARB 13 CCR 1968.2`, `PRIMARY_LAW`) defines the warm-up cycle at `71.1 °C (160 °F)`, internal `OBD_VOCABULARY §13.2` / `K1115` use `>= 70 °C`, while `kg/sensor_fault.json:136` states `> 80 °C` -> `PARTLY`.
5. **`CK0189`, `RK0087` (`0.0–200.0 %` VE), and `RK0062` (`_CUTOFF_VE_SKEW = 90.0 %`):** `S022` (`Wikipedia Volumetric_efficiency`, `SECONDARY`) notes `> 100 %` with forced induction and `~130 %` naturally aspirated limit (so `0-200 %` is valid for boosted engines -> `PARTLY`), and `S019` (`Gears Magazine`, `TRADE`) states `90% or above` is healthy breathing (contradicting `RK0062` -> `CONTRADICTED`), whereas `OBDLab_KG_Wiki.md §6.4` defines `0–100 %` bounds and `> 85 %` for `FAULT_VE_SENSOR_SKEW`.
6. **`RK0014` (`_ZONE_STOICH_BOUNDARY = 0.50 V`):** `S021` (`Fluke`) and `S024` (`Underhood Service`) put exact stoichiometry at `≈0.45 V` (`0.450 V`), `S026` notes a `0.4-0.5 V` steady mid-range band (matching code `0.40–0.50 V`), while `OBDLab_KG_Wiki.md §11.1` defines `STOICHIOMETRIC_CENTER` up to `0.59 V` -> `PARTLY`.
7. **`RK0410` (`WIDEBAND_AFR_STOICH = 14.7`):** `S018` (`Bridge Analyzers`, `TRADE`) states `14.66:1`, `"commonly referred to as 14.7:1"`, and `14.71:1`; `ui_payload.py:76` comment notes GASLab `AFR_STOICH` is `14.71` while wideband petrol display scaling uses `14.7` -> `CONFIRMED`.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23b.txt`):
  - `verdicts CONFIRMED=5 CONTRADICTED=9 PARTLY=15`
  - `sources 25 primary 10`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt` and `scope/T-AUD-23a.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/sources.csv`, `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv`
  - Untracked: `labs/gaslab/audit_tasks/wikiaudit/sources/S014.md`–`S028.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23b.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23b.md`; `search/` deleted.

## CODE REVIEW
- Confirmed `sources.csv` (`S014`–`S028`) and `verdicts.csv` (29 rows in exact `T-AUD-23b.txt` order) were appended strictly below existing rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines.
- All 15 cited new source files (`S014.md`–`S028.md`) exist under `labs/gaslab/audit_tasks/wikiaudit/sources/`, unused scrapes and `search/` were deleted per R3, every quote matches its source file (whitespace-normalised, case-sensitive), all `SECONDARY`/`TRADE` verdicts disclose so in `note` per R5, and all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/README.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T21:48:00Z` | `2026-11-15T22:06:29Z` | `18.5` | `ABSENT` |
