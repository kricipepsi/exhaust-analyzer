# Progress Note — T-AUD-23a

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-23a` (worktree per `T-AUD-23a.go.txt` lane rule) with spec commit `f1af66c` (`git log --oneline fix/T-AUD-22h..HEAD`), `git status --porcelain` empty, `check_verdicts.py --scope scope/T-AUD-23a.txt` fails with `VERDICTS FAIL 25 error(s)` (all `no verdict`), `check_verdicts.py --scope scope/T-GASA-17.txt` passes with `VERDICTS OK scope=T-GASA-17.txt claims 20` (P3), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 25 errors from `check_verdicts.py --scope scope/T-AUD-23a.txt` are `ERROR scope <cid>: no verdict` because `verdicts.csv` currently contains only the 20 T-GASA-17 rows.
- **(c) Independently derived decisive expected value:** Direct scan of `scope/T-AUD-23a.txt`, `claims_comlab.csv`, `claims_rest.csv`, `sources.csv`, and `verdicts.csv` confirms 25 root claims (`same_as` empty: 11 in `claims_comlab.csv`, 14 in `claims_rest.csv`), 34 linked claims pointing to them via `same_as` (P1), 8 existing rows in `sources.csv` (`S001`, `S002`, `S004`, `S005`, `S007`, `S008`, `S009`, `S011`; new IDs start at `S012`, P5), and 20 existing rows in `verdicts.csv` (P2=25, P3=20).
- **(d) No contradiction or missing decision prevents implementation:** Rulings R1–R6, `wikiaudit/README.md`, and `T-AUD-23a.go.txt` lane rules are consistent; `sources.csv` and `verdicts.csv` are clean UTF-8.
- **(e) Teach-back:** Verify each of the 25 root claims in `scope/T-AUD-23a.txt` against primary standards/regulators or secondary/trade references (fetched via Firecrawl into `labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md`, or reusing `S001`/`S002`/`S005`/`S009` where applicable) and append rows to `sources.csv` and `verdicts.csv` without altering any existing row. Done is verified when `check_verdicts.py` prints `VERDICTS OK` for both `T-AUD-23a.txt` (`claims 25`) and `T-GASA-17.txt` (`claims 20`), `search/` and any uncited `sources/` files are deleted, and `git diff` shows `0` removed lines on both CSVs.

## Assumptions worked past
- Lane rules in `C:\4DApp\.agy\T-AUD-23a.go.txt` govern worktree branch naming (`agy/T-AUD-23a` instead of `fix/T-AUD-23a`), disallow `git commit`/`git push`, and omit the branch/log paste from `RESULT_T-AUD-23a.md`.

## Step 1 Disclosure
- `verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=7`
- `sources 10 primary 8`
- `VERDICTS OK scope=T-AUD-23a.txt claims 25`
- `UNSOURCED` claims: **0** (all 25 claims sourced; no `UNSOURCED` rows).

## 25-Verdict Table

| claim | value | verdict | source_value | source |
|---|---|---|---|---|
| `CK0179` | `-254.0 – 254.0 %` | `CONTRADICTED` | `STFT + LTFT sum spans -200 % to +198.44 % (each PID 06-09 spans -100 % to +99.22 %, 99.2 % rounded)` | `S012` (`SECONDARY`) |
| `CK0181` | `-127.0 – 127.0 %` | `CONTRADICTED` | `-100 % to +99.22 % (+99.2 % in S012; formula (100/128)*A - 100)` | `S012` (`SECONDARY`) |
| `RK0030` | `-127 - 127 %` | `CONTRADICTED` | `-100 % to +99.22 % (+99.2 % in S012; PID 07/09 share PID 06 scaling (100/128)*A - 100)` | `S012` (`SECONDARY`) |
| `RK0031` | `-127.0 %` | `CONTRADICTED` | `-100 % minimum (PIDs 06-09)` | `S012` (`SECONDARY`) |
| `RK0032` | `127.0 %` | `CONTRADICTED` | `+99.22 % maximum (+99.2 % rounded in S012; PIDs 06-09 at A=255)` | `S012` (`SECONDARY`) |
| `RK0082` | `-127 - 127 %` | `CONTRADICTED` | `-100 % to +99.22 % (+99.2 % rounded in S012)` | `S012` (`SECONDARY`) |
| `RK0191` | `-127.0 %` | `CONTRADICTED` | `-100 % minimum (PIDs 06-09)` | `S012` (`SECONDARY`) |
| `RK0192` | `127.0 %` | `CONTRADICTED` | `+99.22 % maximum (+99.2 % rounded in S012; PIDs 06-09)` | `S012` (`SECONDARY`) |
| `RK0204` | `140.0 °C` | `PARTLY` | `215 °C SAE J1979 PID 0F encodable maximum (-40 to 215 °C, formula A - 40)` | `S012` (`SECONDARY`) |
| `RK0247` | `500.0 g/s` | `PARTLY` | `655.35 g/s SAE J1979 PID 10 encodable maximum (0 to 655.35 g/s, formula (256A+B)/100)` | `S012` (`SECONDARY`) |
| `RK0384` | `16383 rpm` | `PARTLY` | `16,383.75 rpm SAE J1979 PID 0C encodable maximum (0 to 16,383.75 rpm, formula (256A+B)/4)` | `S012` (`SECONDARY`) |
| `RK0386` | `215.0 °C` | `CONFIRMED` | `(matches PID 05: -40 to 215 °C)` | `S012` (`SECONDARY`) |
| `RK0394` | `215.0 °C` | `CONFIRMED` | `(matches PID 0F: -40 to 215 °C)` | `S012` (`SECONDARY`) |
| `RK0399` | `0.000 V` | `CONFIRMED` | `(matches PID 14/15: 0 to 1.275 V)` | `S012` (`SECONDARY`) |
| `RK0400` | `1.275 V` | `CONFIRMED` | `(matches PID 14/15: 0 to 1.275 V)` | `S012` (`SECONDARY`) |
| `CK0482` | `P0300-P0304` | `CONTRADICTED` | `P0300 (random/multiple cylinder misfire) and P0301-P0312 (cylinders 1 to 12); P0300-P0319 misfire code block` | `S013` (`TRADE`) |
| `CK0535` | `≤ 0.5 % vol` | `CONTRADICTED` | `CO <= 0.3% at idle (and <= 0.2% at fast idle) for default catalyst-car basic emissions test; 0.5% idle only for pre-9/2002 cat cars (S009)` | `S001` (`PRIMARY_REGULATOR`) |
| `CK1384` | `1.0 % vol` | `CONTRADICTED` | `0.5% vol at natural idle (0.3% at raised speed) for cat cars 1/8/95-31/8/2002 (S009; S002 8.2.1.2(b)(ii) 0.5% idle / 0.3% high idle); 3.5% vol for pre-1/8/95 non-Annex cars (S009) and Euro 1 type-II (S005)` | `S009` (`PRIMARY_REGULATOR`) |
| `CK1385` | `150 ppm` | `PARTLY` | `200 ppm at raised speed for cat cars 1/8/95-31/8/2002 (no natural-idle HC requirement); 1200 ppm natural idle for pre-1/8/95 non-Annex cars` | `S009` (`PRIMARY_REGULATOR`) |
| `CK1386` | `0.10 -` | `CONTRADICTED` | `1 ± 0.03 (0.97-1.03) at raised speed for cat cars (S002 8.2.1.2(c), S009 from 1/8/95); no lambda requirement for pre-1/8/95 non-cat cars (S009)` | `S002` (`PRIMARY_LAW`) |
| `CK1389` | `0.5 % vol` | `CONTRADICTED` | `0.3% vol at natural idle (0.2% at raised speed) from 1/9/2002 (S009, S002 8.2.1.2(b)(ii) fn 7); 0.5% idle / 0.3% raised idle applied only to early Euro 3 cars before 1/9/2002` | `S009` (`PRIMARY_REGULATOR`) |
| `CK1390` | `55 ppm` | `PARTLY` | `200 ppm at raised speed (no natural-idle HC requirement)` | `S009` (`PRIMARY_REGULATOR`) |
| `CK1391` | `0.05 -` | `CONTRADICTED` | `1 ± 0.03 (0.97-1.03) at raised speed (S002 8.2.1.2(c), S009, S001)` | `S002` (`PRIMARY_LAW`) |
| `CK1395` | `15 ppm` | `PARTLY` | `200 ppm at raised speed in UK MOT (S009, S001); Euro 5/6 Type 2 idle test covers CO only with no HC limit (S008)` | `S009` (`PRIMARY_REGULATOR`) |
| `CK1396` | `0.02 -` | `PARTLY` | `1 ± 0.03 (0.97-1.03) at raised speed (S002 8.2.1.2(c), S009, S001)` | `S002` (`PRIMARY_LAW`) |

## Disputes
1. **`CK1384` (`HORIZON_LEGACY`, Euro 1 & 2, `gas_co_max_pct: 1.0 %`):** Subject of the 2026-11-15 operator DISPUTE. `S005` (`91/441/EEC` Euro 1 Type II) allows `3.5 %` idle CO (`4.5 %` adjustment range) and `S009` allows `3.5% vol` for pre-`1/8/95` non-Annex cars, whereas `S009` (`1/8/95–31/8/2002` cat cars) and `S002` (`2014/45/EU` 8.2.1.2(b)(ii)) enforce `0.5 %` natural idle (`0.3 %` raised idle) for catalyst vehicles. Decided `CONTRADICTED` against the `0.5 %` Euro 1–2 catalyst-car statutory limit (`eras_sensitivity_masks.yaml` also diverges from `COMWIKI-04` `1.5 %` and has no Python consumer).
2. **`CK1389` (`HORIZON_ADAPTIVE`, Euro 3 & 4, `gas_co_max_pct: 0.5 %`):** Subject of the 2026-11-15 operator DISPUTE. `S009` (`From 1/9/2`) and `S002` (8.2.1.2(b)(ii) fn 7) require `0.3 %` natural idle (`0.2 %` raised idle), whereas early Euro 3 vehicles first used `1/2001–31/8/2002` fell under `S009`'s `0.5 %` natural-idle (`0.3 %` raised-idle) band. Decided `CONTRADICTED` against the `0.3 %` Euro 3–4 statutory limit (`COMWIKI-04` gives `1.0 %`; no Python consumer reads `gas_co_max_pct`).
3. **`CK0535` (`no_fault.json` NF-001 `co <= 0.5 % vol`):** Same root tension as `W0185`: `S001`, `S009` (`From 1/9/2`), and `S002` enforce `0.3 %` natural idle (`0.2 %` fast idle) for catalyst cars from `1/9/2002`, while `S009` allowed `0.5 %` natural idle for `1/8/95–31/8/2002` cat cars. Decided `CONTRADICTED` against the `0.3 %` default catalyst-car limit.
4. **`CK1386` (`0.10`), `CK1391` (`0.05`), and `CK1396` (`0.02`) (`lambda_tolerance`):** `S002` (8.2.1.2(c)) and `S009` (`1/8/95+` cat cars) set `1 ± 0.03` (`0.97–1.03`) at raised idle (while pre-`1/8/95` non-cat cars in `S009` have no lambda requirement). In COMLab Python (`lab_pipeline_aggregator.py`, `perception_contradiction.py`, `fault_atlas_router.py`), `lambda_tolerance` is actually consumed as the ECU-vs-chemistry delta gate `|normalized_obd_lambda - lambda_chem| <= era_lambda_tolerance`, not a tailpipe exhaust limit. Following R4 (compare against the legal limit for each labelled Euro stage), `0.10` and `0.05` are `CONTRADICTED` (looser than `±0.03`), and `0.02` is `PARTLY` (tighter than `±0.03`, with its COMLab role recorded).
5. **`CK1385` (`150 ppm`), `CK1390` (`55 ppm`), `CK1395` (`15 ppm`) (`gas_hc_max_ppm`):** `S009` and `S001` set `200 ppm` at raised idle for catalyst cars (`S009` also sets `1200 ppm` natural idle for pre-`1/8/95` non-Annex cars; `S008` sets no Euro 5/6 idle HC limit). Additionally, `eras_sensitivity_masks.yaml` (`150 / 55 / 15 ppm`) disagrees with `COMWIKI-04` (`300 / 200 / 150 ppm`) and has no live Python consumer. All three are tighter than `200 ppm` -> `PARTLY`.
6. **STFT/LTFT max rounding (`99.2 %` vs `99.22 %`):** `S012` displays `99.2` (1 decimal) from `(100/128)*255 - 100 = 99.21875 %`, whereas `OBDLab_KG_Wiki.md` and `ui_payload.py` round to `99.22 %`. Both reflect the same SAE J1979 formula and both contradict `±127` / `±254`.

## VERIFICATION GATE
- Step 1 (`check_verdicts.py --scope scope/T-AUD-23a.txt | tail -3`):
  - `verdicts CONFIRMED=4 CONTRADICTED=14 PARTLY=7`
  - `sources 10 primary 8`
  - `VERDICTS OK scope=T-AUD-23a.txt claims 25`
- Step 2 (`check_verdicts.py --scope scope/T-GASA-17.txt | tail -1`):
  - `VERDICTS OK scope=T-GASA-17.txt claims 20`
- Step 3 (`git diff` removed lines on `sources.csv` & `verdicts.csv`; `git status --porcelain`):
  - Removed lines: `0`
  - Modified: `labs/gaslab/audit_tasks/wikiaudit/sources.csv`, `labs/gaslab/audit_tasks/wikiaudit/verdicts.csv`
  - Untracked: `labs/gaslab/audit_tasks/wikiaudit/sources/S012.md`, `labs/gaslab/audit_tasks/wikiaudit/sources/S013.md`, `apps/wired/audit_tasks/progress_notes/T-AUD-23a.md` (and `apps/wired/audit_tasks/results/RESULT_T-AUD-23a.md`); `search/` deleted.

## CODE REVIEW
- Confirmed `sources.csv` (`S012`–`S013`) and `verdicts.csv` (25 rows in `T-AUD-23a.txt` order) were appended strictly below existing rows in clean UTF-8 with LF line endings and `0` removed/altered existing lines.
- Every cited source file under `labs/gaslab/audit_tasks/wikiaudit/sources/` exists (`S012.md`, `S013.md`), unused scratch (`S013.md` 13 CCR 1968.2 draft and `search/` folder) was removed per R3, every quote matches its fetched/existing source file, all `SECONDARY`/`TRADE` verdicts state so in `note` per R5, and all `CONTRADICTED`/`PARTLY` rows carry `source_value` per R1/README.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | `2026-11-15T21:35:13Z` | `2026-11-15T21:41:54Z` | `6.7` | `ABSENT` |
