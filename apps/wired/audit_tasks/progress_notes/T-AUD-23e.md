# Progress Note — T-AUD-23e

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23e` (worktree per `T-AUD-23e.go.txt` lane rule) with spec commit `493c1d0` (`git log --oneline fix/T-AUD-24j..HEAD`), `git status --porcelain` empty at baseline, `check_verdicts.py --scope scope/T-AUD-23e.txt` fails with `VERDICTS FAIL 28 error(s)` (all `no verdict`), `check_verdicts.py` passes on `T-GASA-17.txt` (`20`), `T-AUD-23a.txt` (`25`), `T-AUD-23b.txt` (`29`), and `T-AUD-23d.txt` (`29`) per P3, and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 28 errors from `check_verdicts.py --scope scope/T-AUD-23e.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently holds only the `103` earlier verdicts (`20 + 25 + 29 + 29`).
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23e.txt`, `claims_comlab.csv`, `sources.csv`, and `verdicts.csv` confirms `28` root claims (`same_as` empty), all in `labs/comlab/registry/rules/sensor_fault.json` (P1; `CK0860` links to `CK0634` via `same_as`), `33` existing rows in `sources.csv` ending at `S036` so new IDs start at `S037` (P4), and `103` existing rows in `verdicts.csv`.
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23e.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 28 root claims in `scope/T-AUD-23e.txt` (`lambda_perception_delta`, upstream/downstream O2 voltage, MAF, MAP, ECT, and STFT/LTFT gates in `SF-001`–`SF-008`) against authoritative sources fetched via Firecrawl into `labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md` (reusing `S001`–`S036` where applicable), and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for `T-AUD-23e.txt` (`claims 28`) and the four P3 scopes, `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23e.go.txt` govern worktree branch naming (`agy/T-AUD-23e` instead of `fix/T-AUD-23e`), disallow `git commit`/`git push`/`git switch`/`git checkout`, and omit the branch/log paste from `RESULT_T-AUD-23e.md`.
- `lambda_perception_delta` `±0.03` gates are judged `CONTRADICTED` because `±0.03` sits inside the combined healthy sensor+combustion+analyser variation (`±5 %` healthy engine analyser Lambda in `S040`; `1–2 %` combustion variance + `±2 %` wideband error, up to `5 %`, in `S038`; `1.016 ± 0.007` LSU 4.9 in `S016` + `0.3 %` OIML R 99 calc MPE in `S014`) and is far tighter than Ford OEM's `-0.083 / +0.087` FAOS bias limit (`S037`), whereas `±0.05` (`CK0636`, `CK0637`) is judged `PARTLY` against `S037` (`OEM`: outside `±2 %` healthy UEGO target and matching `<= 0.05` lack-of-movement, while OEM bias limit `-0.083 / +0.087` is `> 20 %` larger).

## Step 1 Disclosure
- `verdicts CONFIRMED=3 CONTRADICTED=21 PARTLY=4`
- `retired 0 of 28 scope claims (retired.csv)`
- `sources 37 primary 10`
- `VERDICTS OK scope=T-AUD-23e.txt claims 28`
- `UNSOURCED` claims: **0** (all 28 claims sourced; no `UNSOURCED` rows).

## 28-Verdict Table

| claim | rule | value | verdict | source value | source |
|---|---|---|---|---|---|
| `CK0626` | `SF-001` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `±5 % (±0.05) healthy engine analyser Lambda range (S040); ±2 % (±0.02) wideband error + 1-2 % combustion variance (S038); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S040` (`TRADE`) |
| `CK0627` | `SF-001` | `o2_voltage ≥ 0.55 V` | `CONTRADICTED` | `0.10 - 0.90 V normal closed-loop switching pivoting at ~0.45 V (S021); 0.2 - 0.8 V (S024)` | `S021` (`TRADE`) |
| `CK0630` | `SF-002` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `±5 % (±0.05) healthy engine analyser Lambda range (S040); ±2 % (±0.02) wideband error + 1-2 % combustion variance (S038); Bosch LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S040` (`TRADE`) |
| `CK0631` | `SF-002` | `o2_voltage ≤ 0.35 V` | `CONTRADICTED` | `0.10 - 0.90 V normal closed-loop switching pivoting at ~0.45 V (S021); 0.2 - 0.8 V (S024)` | `S021` (`TRADE`) |
| `CK0634` | `SF-003` | `o2_voltage < 0.20 V` (pegged lean) | `CONFIRMED` | `(pegged < 0.20 V matches P0131 stuck-low threshold ~0.2 V in S039, S024, S026)` | `S039` (`TRADE`) |
| `CK0636` | `SF-003` | `lambda_perception_delta > 0.05` | `PARTLY` | `±2 % (±0.02) UEGO target band and -0.083 / +0.087 FAOS bias malfunction limits (<= 0.05 lambda change for lack-of-movement) in S037 (OEM); ±5 % healthy analyser Lambda in S040 (TRADE)` | `S037` (`OEM`) |
| `CK0637` | `SF-003` | `lambda_perception_delta < -0.05` | `PARTLY` | `±2 % (±0.02) UEGO target band and -0.083 / +0.087 FAOS bias malfunction limits (<= 0.05 lambda change for lack-of-movement) in S037 (OEM); ±5 % healthy analyser Lambda in S040 (TRADE)` | `S037` (`OEM`) |
| `CK0639` | `SF-003` | `o2_voltage ≤ 0.2 V` (instantaneous) | `PARTLY` | `~0.10-0.90 V normal closed-loop switching (S021); stuck-lean P0131 requires pegged < 0.2 V without switching (S039)` | `S039` (`TRADE`) |
| `CK0643` | `SF-004` | `MAF idle baseline ~1 g/s per L` | `CONFIRMED` | `(standard rule of thumb in S019; ~27 % average scatter across 9 healthy vehicles)` | `S019` (`TRADE`) |
| `CK0644` | `SF-004` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0645` | `SF-004` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0646` | `SF-004` | `maf ≥ 3.5 g/s` | `CONTRADICTED` | `2 to 7 g/s normal MAF at idle (15 to 25 g/s at 2500 rpm) depending on engine size (S020); ~1 g/s per L rule of thumb (S019)` | `S020` (`TRADE`) |
| `CK0649` | `SF-005` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0650` | `SF-005` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0651` | `SF-005` | `map_kpa < 35.0 kPa` | `CONTRADICTED` | `30 - 50 kPa normal MAP range at idle (40 - 60 kPa with larger camshaft) in S036; P0106 rationality checks \|MAP - Estimated MAP\| < 2.20-2.50 inHg (~7.5-8.5 kPa) in S037 OEM` | `S036` (`TRADE`) |
| `CK0654` | `SF-006` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0655` | `SF-006` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0656` | `SF-006` | `ect_c ≤ 60.0 °C` | `CONFIRMED` | `(CARB 13 CCR 1968.2 (f)(11.2.2)(C) 140 °F = 60.0 °C example stuck-cold limit; 71.1 °C warm-up cycle; S017/S029 75 °C)` | `S027` (`PRIMARY_LAW`) |
| `CK0657` | `SF-006` | `o2_downstream ≥ 0.6 V` | `CONTRADICTED` | `~0.7 V steady downstream voltage for working catalyst (S024); 0.45 - 0.85 V filtered secondary O2 range (S037 OEM); steady 0.4 - 0.5 V indicates sensor failure (S026)` | `S024` (`TRADE`) |
| `CK0661` | `SF-007` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0662` | `SF-007` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0663` | `SF-007` | `o2_voltage ≤ 0.2 V` | `PARTLY` | `Cold-start low voltage (< 0.2 V) when heater unpowered (S039 TRADE); open/inactive sensor often sits near 0.45 V PCM bias (0.27-0.50 V in S037 OEM; 450 mV in S036); healthy cycling hits 0.10-0.90 V (S021)` | `S039` (`TRADE`) |
| `CK0667` | `SF-008` | `lambda_perception_delta > 0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0668` | `SF-008` | `lambda_perception_delta < -0.03` | `CONTRADICTED` | `1-2 % combustion variation + ±2 % wideband accuracy target, up to 5 % across units (S038); ±5 % healthy analyser Lambda (S040); LSU 4.9 1.016 ± 0.007 (S016 OEM) + OIML R 99 0.3 % calc MPE (S014); Ford FAOS bias fault -0.083 / +0.087 (S037 OEM)` | `S038` (`TRADE`) |
| `CK0669` | `SF-008` | `shrtft1 > 5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (+/-8 % idle range in S030; -9 % to +11 % / -13 % to +18 % entry conditions in S037 OEM; +/-20 % combined in S029 OEM)` | `S030` (`TRADE`) |
| `CK0670` | `SF-008` | `shrtft1 < -5.0 %` | `CONTRADICTED` | `-10 % to +10 % normal STFT range (+/-8 % idle range in S030; -9 % to +11 % / -13 % to +18 % entry conditions in S037 OEM; +/-20 % combined in S029 OEM)` | `S030` (`TRADE`) |
| `CK0671` | `SF-008` | `longft1 > 3.0 %` | `CONTRADICTED` | `total STFT + LTFT within +/-20 % is normal; +/-35 % malfunction threshold (S029 OEM); 5 - 8 % normal aging LTFT, >= +/-10 % problem (S030, S019)` | `S029` (`OEM`) |
| `CK0672` | `SF-008` | `longft1 < -3.0 %` | `CONTRADICTED` | `total STFT + LTFT within +/-20 % is normal; +/-35 % malfunction threshold (S029 OEM); 5 - 8 % normal aging LTFT, >= +/-10 % problem (S030, S019)` | `S029` (`OEM`) |

## Disputes
1. **`lambda_perception_delta` `±0.03` vs `±0.05` vs OEM FAOS bias limit (`CK0626`, `CK0630`, `CK0636`, `CK0637`, `CK0644`, `CK0645`, `CK0649`, `CK0650`, `CK0654`, `CK0655`, `CK0661`, `CK0662`, `CK0667`, `CK0668`):** `S040` (*MOTOR Magazine*, `TRADE`) reports that on a correctly running engine, gas-analyser Lambda is `±5 %` of 1 (`±0.05`), and `S038` (*Hot Rod* Kettering Horiba lab test, `TRADE`) measures `1–2 %` combustion instability plus `±2 %` wideband error (up to `5 %` across consumer units), on top of `S016` (`Bosch LSU 4.9` `OEM`, `1.016 ± 0.007` at λ=1) and `S014` (`OIML R 99`, `0.3 %` calc MPE plus gas channel MPEs). Thus `±0.03` sits inside combined healthy variation (`CONTRADICTED`). Meanwhile `S037` (`Ford OEM`) holds healthy UEGO target control within `±2 %` (`±0.02`) and sets its actual `FAOS` rear-bias malfunction threshold at `-0.083 / +0.087` (`~±8.5 %`) while using `≤ 0.05` lambda change for lack-of-movement (`PARTLY` for `CK0636`/`CK0637` `±0.05`, vs `S040`'s `±5 %` healthy engine band).
2. **Upstream narrowband O2 voltage (`CK0627` `≥ 0.55 V`, `CK0631` `≤ 0.35 V`, `CK0634` `< 0.20 V`, `CK0639` `≤ 0.2 V`, `CK0663` `≤ 0.2 V`):** `S021` (`Fluke`, `TRADE`) and `S024` (`Underhood Service`, `TRADE`) put healthy closed-loop oscillation at `0.10–0.90 V` (`0.2–0.8 V` in `S024`) around `0.45 V` (`1–5 Hz`), so instantaneous freeze-frame `≥ 0.55 V` and `≤ 0.35 V` fire ~50 % of the time on a healthy sensor (`CONTRADICTED`). `CK0634` (`pegged < 0.20 V`) is `CONFIRMED` by `S039` (`P0131` stuck below `0.2 V`), whereas instantaneous `CK0639` (`≤ 0.2 V` without duration/no-switching check) is `PARTLY` because healthy `0.10–0.90 V` switching crosses `≤ 0.2 V` every second (twin of `CK0638` `≥ 0.8 V`). For `CK0663` (`SF-007` heater fault), `S039` confirms cold unpowered sensors can read `< 0.2 V`, whereas `S036` (`450 mV`) and `S037` (`Ford OEM` `0.27–0.50 V` open-circuit band) show inactive sensors commonly sit near `0.45 V` (`PARTLY`).
3. **Downstream O2 voltage (`CK0657` `o2_downstream ≥ 0.6 V`):** `S024` (`TRADE`) states a healthy working-catalyst rear O2 hovers around `0.7 V` and `S037` (`Ford OEM`) gives `0.45–0.85 V` filtered secondary O2 (`CONTRADICTED`), whereas `S026` (`TRADE`) notes a steady `0.4–0.5 V` mid-range voltage indicates sensor failure.
4. **MAF idle baseline & gate (`CK0643` `~1 g/s per L`, `CK0646` `≥ 3.5 g/s`):** `S019` (`Gears Magazine`, `TRADE`) states the `~1 g/s per L` rule of thumb (`CONFIRMED` on `CK0643`) while noting ~27 % empirical deviation across 9 healthy vehicles; `S020` (`ALLDATA`, `TRADE`) gives `2 to 7 g/s` at idle (`15–25 g/s` at `2500 rpm`), contradicting `CK0646` (`≥ 3.5 g/s`) as firing on healthy larger/non-idle engines and missing under-reading MAF faults.
5. **MAP idle threshold (`CK0651` `map_kpa < 35.0 kPa`):** `S036` (`The Tuning School`, `TRADE`) puts healthy idle MAP at `30–50 kPa` (`40–60 kPa` with larger cam), contradicting `< 35.0 kPa`; `S037` (`Ford OEM`) uses model-based `|MAP - Estimated MAP| < 2.20–2.50 inHg` (`~7.5–8.5 kPa`) for `P0106`.
6. **Fuel trims (`CK0669`–`CK0672`) & ECT (`CK0656`):** `S030` (`±10 %` STFT, `±8 %` idle, `5–8 %` LTFT), `S019` (`< ±10 %` LTFT), `S029` (`Toyota OEM`, `±20 %` combined normal, `±35 %` DTC), and `S037` (`Ford OEM`, `-9 to +11 %` / `-13 to +18 %` STFT monitor entry) contradict `±5.0 %` STFT and `±3.0 %` LTFT. For `CK0656`, `S027` (`CARB 13 CCR § 1968.2`, `PRIMARY_LAW`) uses `140 °F` (`60.0 °C`) as its example stuck-cold minimum-enable threshold (`CONFIRMED`), assuming the vehicle under test is warmed up.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23e.txt`):
  - `verdicts CONFIRMED=3 CONTRADICTED=21 PARTLY=4`
  - `retired 0 of 28 scope claims (retired.csv)`
  - `sources 37 primary 10`
  - `VERDICTS OK scope=T-AUD-23e.txt claims 28`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt`, `scope/T-AUD-23a.txt`, `scope/T-AUD-23b.txt`, `scope/T-AUD-23d.txt`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
  - `VERDICTS OK scope=T-AUD-23b.txt claims 29`
  - `VERDICTS OK scope=T-AUD-23d.txt claims 29`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/sources.csv`, `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv`
  - Untracked: `labs/gaslab/audit_tasks/wikiaudit/sources/S037.md`–`S040.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23e.md`, `apps/wired/audit_tasks/results/RESULT_T-AUD-23e.md`; `search/` deleted.

## CODE REVIEW
- Confirmed `sources.csv` (`S037`–`S040`) and `verdicts.csv` (28 rows in exact `T-AUD-23e.txt` order) were appended strictly below existing rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines.
- All 4 cited new source files (`S037.md`–`S040.md`) exist under `labs/gaslab/audit_tasks/wikiaudit/sources/`, unused scrapes and `search/` were deleted per R3, every quote matches its source file (whitespace-normalised, case-sensitive), all `TRADE` verdicts disclose so in `note` per R5, and all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/README.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-16T10:07:36Z` | `2026-11-16T10:16:49Z` | `9.2` | `ABSENT` |
