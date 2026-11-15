# T-AUD-22e progress note: COMLab knowledge-graph literal inventory

## Readiness challenge

- (a) Starting state matches task (with lane-rule branch `agy/T-AUD-22e`): `git log --oneline fix/T-AUD-22d..HEAD` shows `4d1bb1f spec(T-AUD-22e): classify the COMLab knowledge-graph literals (261)`, `git status --porcelain` is empty, and preconditions print `checked` with no `MISSING` line.
- (b) Decisive check fails for the intended reason: step 1 prints `CLAIMS FAIL 261 error(s)` (all `uncovered`, P2); step 3 prints `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025` (P4).
- (c) Independently derived counts from `candidates_comlab.csv`: 261 non-auto candidates in `labs/comlab/comlab/config/kg/*` across 14 files (P1) — `schema_version` 13, `_kg_schema.json` 9 (union 22, P3), `mechanical_failure_mode` 27, list strings 212 (P5); `claims_comlab.csv` currently has 1025 rows ending at `CK1026`.
- (d) No contradiction or missing decision prevents implementation. Choices left open by R1–R7 are recorded under `Assumptions worked past`.
- (e) Teach-back: append classified or `NON_DOMAIN` rows `CK1027`+ to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` for all 261 non-auto candidates of `labs/comlab/comlab/config/kg/*.json`, with empty `citation`, `same_as` to matching `W` or earlier `CK` claims, and `suspect` for contradictions. Decisive check: step 1 prints `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/kg/* candidates 261 covered claims <N>` with no `ERROR`, step 2 prints `schema 22 non_domain 22`, step 3 keeps `candidates 303` and `CK0001`-`CK1026` unchanged, and step 4 shows `0` removed lines.

## Assumptions worked past

1. **Lane rules (`T-AUD-22e.go.txt`):** branch is `agy/T-AUD-22e` (not `fix/T-AUD-22e`), no `git commit`/`push`/`switch`/`checkout`, only the three files in `### Files to touch ###` are written (no throwaway scripts/files on disk).
2. **Schema lines (`R3`):** all 13 `"schema_version"` lines and all 9 `_kg_schema.json` lines (22 total) are recorded as single `NON_DOMAIN` rows with empty `quantity`–`suspect`.
3. **Non-domain prose numbers (`R4`):** DTC codes (`P0011`/`P0021`, `P0014`/`P0024`, `P0140`/`P0160`, `P0300`–`P0312`, `P0335`, `P0420`/`P0430`, `P0562`–`P0643`), Mode/TID/CID/PID identifiers (`Mode 06`, `Mode $06`, `Mode 07`, `PID 0C`, `TID $01-$09`, `CID $01-$99`), cylinder/bank indices (`cylinder 1`, `bank 1`, `bank 2`), and sample/part counts (`2-3 representative cylinders`) are omitted when the line carries domain values, or marked `NON_DOMAIN` (one row) when the line has no domain values (`24` non-schema `NON_DOMAIN` rows + `22` schema `NON_DOMAIN` rows = `46` `NON_DOMAIN` rows total).
4. **Condition formatting (`R4`):** every domain row begins `condition` with the enclosing node ID (`ERR-...`) and states the operating/test condition from the sentence; test conditions embedded as qualifiers (e.g. `at 2500 RPM` on backpressure/catalyst ΔT, `at 20 °C` / `at 90 °C` on coil/solenoid/ECT resistance, `1000 km` in `> 1 L per 1000 km`, `30 s` in `> 1 drop per 30 s`) stay in `condition`/`unit` rather than creating separate spurious claims, while standalone test speeds/durations (`2500 rpm` on load/EGR/snap-throttle checks, `10 min` idle warm-up/leak-down, `5 min` warm-up/CL transition, `60 s` / `30 s` / `2 s` timing targets) are emitted as claims when stated as procedure targets (`R5`).
5. **Classes (`R5`):** fault cut-offs and confirmation/failure thresholds are `DIAGNOSTIC_THRESHOLD`; nominal OEM component resistances, healthy baselines, cleaning/oil-change intervals, and post-repair targets are `TYPICAL_RANGE`; `5 V` ECU sensor reference supply (including `5.00 +/- 0.10 V` tolerance) and narrowband stoich center / `12 V` relay switching waveform (`0->12V->0 V`) are `ANALYSER_SPEC`; `lambda 1.0` stoichiometric ground truth is `PHYSICAL_CONSTANT`.
6. **UTF-8 encoding (`R7`) and number matching:** JSON `\uXXXX` escapes are decoded to literal UTF-8 (`—`, `±`, `−`, `≥`, `≤`, `°`, `Ω`, `–`, `→`, `∞`); spaced thousands in `60 000–100 000` (`K1657`) are preserved so `check_code_claims.py` `NUM_RE` matches the source line.
7. **`same_as` and `suspect` (`R6`):** `citation` is empty on all new rows; `same_as` points to a `W` claim or an earlier `CK` claim (including `CK0693`-`CK1026` or an earlier `CK1027`+ row) only when quantity, condition, and value match; contradictions with `W`, `OBD_VOCABULARY`, or earlier `CK` claims are flagged in `suspect`.

## Hand-back blocker (UNSATISFIABLE — hard stop recorded)

- Blocker record: `apps/wired/audit_tasks/progress_notes/T-AUD-22e.blocker.json` (`blocker-record/2`, validated `OK` by `validate_blocker_record.py`).
- **Root defect:** `apps/wired/audit_tasks/codeaudit/check_code_claims.py:29,109` extracts `NUM_RE = re.compile(r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")` against the raw, undecoded `text` column in `candidates_comlab.csv`. Across 44 claims in `labs/comlab/comlab/config/kg/*.json`, the JSON source embeds `\u00b1`, `\u2013`, `\u2212`, or `\u2192` immediately before digits (e.g. `\u00b110`, `2000\u20133000`, `< \u221210`, `0\u219212V`, `2\u20138`), causing `NUM_RE` to concatenate the hex digits onto the domain number (`110`, `20133000`, `221210`, `219212`, `20138`). Under `R7` (clean UTF-8 `±`, `-`, `—`), `R1`/`codeaudit/README.md` (numeric `value` as written), and the prohibition on editing `check_code_claims.py`, `candidates_comlab.csv`, or `kg/*.json`, step 1 fails on all 44 rows (`CLAIMS FAIL 44 error(s)`), while step 3 also fails on those same 44 KG rows when iterating `claims_comlab.csv`.

## Figures (criterion 4)

- **Scope appended (`CK1027`–`CK1380`):** 354 new rows covering all 261 non-auto KG candidates (`K1026`–`K1889`, 0 `uncovered`). Total rows in `claims_comlab.csv`: 1379 (`CK0001`–`CK1380`).
- **Step 1 / Step 3 status:** `CLAIMS FAIL 44 error(s)` (blocked solely on `check_code_claims.py:109` raw `\uXXXX` concatenation across 44 `CK1071`..`CK1369` rows; 310/354 new rows and all `same_as`, `class`, coverage, and `mojibake` checks pass).
- **New KG row `classes` (`CK1027`–`CK1380`):** `ANALYSER_SPEC=11 DIAGNOSTIC_THRESHOLD=170 NON_DOMAIN=46 PHYSICAL_CONSTANT=2 RULE_OF_THUMB=9 TYPICAL_RANGE=116`.
- **Links (`CK1027`–`CK1380`):** `same_as_wiki 15`, `same_as` to earlier `CK` = `90`, `citation` = `""` on all 354 rows.
- **Step 2 (`schema`):** `schema 22 non_domain 22` (`_kg_schema.json` 9 + `schema_version` 13).

## New suspect claims (19)

1. `CK1091` (`K1145`, `catalyst_failure.json:87`, `ERR-CF-004`): `o2_b1s2_v = ~0.45 V` — `OBD_VOCABULARY §12.5` and `wiki/07 §7.3` state a dead/degraded catalyst causes post-cat O2 to switch mirroring upstream (`1:1`); with tailpipe `CO > 1.5 %` a live narrowband reads rich (`> 0.6 V`), not flat at `~0.45 V` (same defect as `CK0714`/`CK0715`).
2. `CK1098` (`K1151`, `catalyst_failure.json:94`, `ERR-CF-004`): `co = ≤ 0.5 % vol` — post-repair working-catalyst ceiling of `<= 0.5 %` at 2500 rpm exceeds working-cat idle CO ceilings (`W0185` 0.1–0.3 %, `W0192` `< 0.3 %`) and the UK MOT 2500 rpm limit `<= 0.20 %` (`W1110`; same gap as `CK0535`).
3. `CK1119` (`K1198`, `catalyst_failure.json:193`, `ERR-CF-009`): `co = < 0.5 % vol` — post-repair working-catalyst ceiling of `< 0.5 %` exceeds the `< 0.3 %` post-cat CO rule (`W0192`), 0.1–0.3 % normal working-cat idle range (`W0185`), and UK MOT `<= 0.30 %` idle limit (`W1109`; same gap as `CK0535`).
4. `CK1254` (`K1582`, `mechanical_wear.json:189`, `ERR-MW-007`): `hc = 150-500 ppm` — `wiki/06a §POA` (`W0600`) and GasLab `POA_SIGNATURE` table (`W1622`) set severe/diagnostic POA oil burning at `HC > 500 ppm` (`500–20000 ppm`), and `MW-008`/`MW-009` rules (`CK0491`, `CK0500`) gate at `hc >= 500 ppm`; `150-500 ppm` lies below that floor.
5. `CK1255` (`K1582`, `mechanical_wear.json:189`, `ERR-MW-007`): `co = < 0.5 % vol` — `wiki §POA_SIGNATURE` (`W0652`) gives `CO ~ 0 %` (`MW-009` `CK0502` gates at `CO < 0.15 %`; UK MOT idle CO limit `W1109` is `<= 0.30 %`); `< 0.5 %` is looser than both.
6. `CK1286` (`K1691`, `non_starter.json:15`, `ERR-NS-004`): `co2 = 4 % vol` — `wiki/04 §4.14` (`W0350`/`W0351`) defines cranking `INCOMPLETE_COMBUSTION` as `5.0 <= CO2 < 8.0 %` and routes `CO2 < 5.0 %` to `LEAN_MISFIRE` (same contradiction as `CK0799`/`CK0934`).
7. `CK1315` (`K1724`, `non_starter.json:106`, `ERR-NS-002`, `same_as CK0934`): `co2 = 3-6 % vol` — `wiki/04 §4.14` (`W0350`/`W0351`) defines cranking `INCOMPLETE_COMBUSTION` as `5.0 <= CO2 < 8.0 %` and routes `CO2 < 5.0 %` to `LEAN_MISFIRE` (as `CK0799`/`CK0934`).
8. `CK1326` (`K1745`, `rich_mixture.json:21`, `ERR-RM-001`): `hc = < 120 ppm` — working-cat idle HC ceilings are `<= 35 ppm` (`W0173`) and `<= 50 ppm` (`W0174`; pre-cat ceiling `<= 100 ppm` `W0176`); `120 ppm` falls inside `CATALYST_NOT_LIGHTING_OFF` 75–125 ppm (`W0440`) and exceeds every other KG post-repair idle target (`< 100` or `<= 50 ppm`).
9. `CK1349` (`K1823`, `sensor_fault.json:16`, `ERR-SF-001`, `same_as CK1021`): `upstream O2 switching frequency (healthy) = > 0.5 Hz` — `OBD_VOCABULARY §12.1` sets healthy narrowband switching frequency at 2–5 Hz (MPI) or 2–3 Hz (TBI) and classifies `< 0.5 Hz` as slow/dying (as `CK1021`).
10. `CK1350` (`K1823`, `sensor_fault.json:16`, `ERR-SF-001`): `upstream O2 switching frequency (ideal) = 1-2 Hz` — `OBD_VOCABULARY §12.1` sets healthy narrowband switching at 2–5 Hz (MPI) or 2–3 Hz (TBI), faster than the 1–2 Hz stated here.
11. `CK1351` (`K1823`, `sensor_fault.json:16`, `ERR-SF-001`, `same_as CK1022`): `upstream O2 switching frequency (lazy) = < 0.25 Hz` — `OBD_VOCABULARY §12.1` already classifies `< 0.5 Hz` as slow/dying rather than `< 0.25 Hz` (as `CK1022`).
12. `CK1353` (`K1827`, `sensor_fault.json:20`, `ERR-SF-001`, `same_as CK1021`): `upstream O2 switching frequency (healthy) = > 0.5 Hz` — `OBD_VOCABULARY §12.1` sets healthy narrowband switching frequency at 2–5 Hz (MPI) or 2–3 Hz (TBI) and classifies `< 0.5 Hz` as slow/dying (as `CK1021`).
13. `CK1355` (`K1835`, `sensor_fault.json:40`, `ERR-SF-002`, `same_as CK0859`): `o2_voltage stuck rich = > 0.7 V` — `OBD_VOCABULARY §12.1` sets narrowband `STUCK_RICH` at pinned `> 0.85 V` (and `SF-003` `CK0635`/`CK0638` gate at `> 0.80` / `>= 0.8 V`), not `> 0.7 V` (as `CK0859`/`CK1024`).
14. `CK1359` (`K1842`, `sensor_fault.json:64`, `ERR-SF-003`): `MAF idle baseline = 2-8 g/s per litre` — `OBD_VOCABULARY §16.2` and `SF-004` (`CK0643`) set curb-idle MAF at `~1 g/s per litre` (and 3–5 g/s/L at 4000 rpm; 8–10 g/s/L is WOT); 2–8 g/s/L spans loaded/WOT rather than idle.
15. `CK1368` (`K1866`, `sensor_fault.json:136`, `ERR-SF-006`): `catalyst efficiency test ECT precondition = > 80 °C` — `OBD_VOCABULARY §13.2` and `K1115` (`ERR-CF-001`) set the catalyst monitor enable gate at `ECT >= 70 °C`, not `> 80 °C`.
16. `CK1371` (`K1875`, `sensor_fault.json:160`, `ERR-SF-007`): `MAF warm idle spec (2.0 L engine) = 2-6 g/s` — `OBD_VOCABULARY §16.2` sets curb-idle MAF at `~1 g/s per litre` (~2 g/s for 2.0 L) and 3–5 g/s/L at 4000 rpm; 2–6 g/s allows 3x normal idle flow (`SF-004` `CK0646` flags idle `maf >= 3.5 g/s`).
17. `CK1374` (`K1884`, `sensor_fault.json:182`, `ERR-SF-008`): `ect_c open/cold-bias reading = -40 °C` — describes `-40 °C` cold bias as "stuck at low resistance"; automotive ECT sensors are NTC thermistors (`labs/obdlab/research/chunks/ecu-diagnosis/05_sensor-ground-trace-open.md`, `AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md §4.2.5`) where `-40 °C` is open-circuit / maximum resistance, not low resistance.
18. `CK1376` (`K1886`, `sensor_fault.json:185`, `ERR-SF-008`): `ECT sensor resistance at 90 °C = 2-3 kohm` — NTC automotive ECT thermistors read ~2–3 kohm at 20 °C and ~0.2–0.3 kohm at 90 °C (~10x lower); also calls cold-enrichment fault "stuck-low resistance" whereas cold reading on an NTC thermistor is high/open resistance.
19. `CK1378` (`K1886`, `sensor_fault.json:185`, `ERR-SF-008`): `ECT sensor resistance at 20 °C = > 10 kohm` — NTC automotive ECT thermistors read ~2–3 kohm at 20 °C rather than `> 10 kohm` (typical `> 10 kohm` is below 0 °C); also calls cold-enrichment fault "stuck-low resistance".

## VERIFICATION GATE

- Step 1 (`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/kg/*'`): **FAIL (`CLAIMS FAIL 44 error(s)`)** — all 44 errors are `value number(s) [...] not in the line text` on lines where `candidates_comlab.csv` has unescaped `\u00b1`/`\u2013`/`\u2212`/`\u2192` immediately before digits (`CK1071..CK1369`); 0 `uncovered` errors.
- Step 2 (schema `NON_DOMAIN` check): **PASS (`schema 22 non_domain 22`)**.
- Step 3 (`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/global_fault_registry.json'`): **FAIL (`CLAIMS FAIL 44 error(s)`)** — fails on the same 44 KG rows because `check_code_claims.py` validates every row in `claims_comlab.csv`; rows `CK0001`–`CK1026` have 0 errors.
- Step 4 (`git diff` removed lines & `git status`): `0` removed lines in `claims_comlab.csv`; modified `claims_comlab.csv`, plus untracked `T-AUD-22e.md`, `T-AUD-22e.blocker.json` (authorized by spec header line 14), and `RESULT_T-AUD-22e.md`.

## CODE REVIEW

- Reviewed `claims_comlab.csv`: UTF-8, LF line endings preserved, `CK0001`–`CK1026` untouched (`0` removed lines), `CK1027`–`CK1380` strictly monotonic in `candidates_comlab.csv` order, `citation` empty on all 354 new rows, all 261 target candidates covered, no double-encoded UTF-8 (`mojibake`), and all 19 domain contradictions flagged in `suspect`.
- Did NOT weaken gates or forge `\uXXXX` / concatenated numbers into `claims_comlab.csv` to bypass `check_code_claims.py:109`. Handed back cleanly per `recording-implementer-handback-blockers`.

## Time

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| Total session | 2026-11-15T18:31:41Z | 2026-11-15T18:45:50Z | 14.2 | ~60% |
