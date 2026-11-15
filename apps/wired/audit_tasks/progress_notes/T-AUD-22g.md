# Progress Note — T-AUD-22g

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-22g` (worktree per lane rule) with spec commits `f135b50` and `b6bfa24` (`git log --oneline fix/T-AUD-22f..HEAD`), `git status --porcelain` empty, `check_code_claims.py --group rest --files 'labs/*'` fails with `CLAIMS FAIL 202 error(s)` (P1=202, P2), full `--group rest` fails with `CLAIMS FAIL 540 error(s)` (matching P1+P3=202+338), and all precondition files `checked`.
- **(b) Test fails for intended reason:** All 202 errors from `check_code_claims.py --group rest --files 'labs/*'` are `uncovered` on the 202 non-auto candidates under `labs/`; `claims_rest.csv` currently holds only the header line.
- **(c) Independently derived decisive expected value:** Direct scan of `candidates_rest.csv` finds 789 total candidates (249 `auto=NON_DOMAIN`, 540 to classify), of which 202 non-auto candidates sit under `labs/` across 20 files (OBDLab 125, DTCLab 76, SymptomLab 1; largest files match P4: `mode_06_hex_dictionary.json` 33, `physical_sensor_bounds.json` 30, `ve_engine.py` 25, `routing_tag_map.yaml` 19, `payload.py` 14), leaving 338 `apps/` candidates uncovered (P3).
- **(d) No contradiction or missing decision:** Rulings R1–R7 and lane rules (`T-AUD-22g.go.txt`) align with `codeaudit/README.md`, `wikiaudit/README.md`, and `check_code_claims.py`; `claims_rest.csv` is UTF-8.
- **(e) Teach-back:** Append classified claim rows (or `NON_DOMAIN` rows) starting at `RK0001` in candidates order to `apps/wired/audit_tasks/codeaudit/claims_rest.csv` covering all 202 `labs/` P1 candidates, with `citation` checked against cited in-repo documents and `same_as` linked to GASLab wiki claims (`W0001`–`W1693`) or earlier `RK` claims where identical. Done is verified by `check_code_claims.py --group rest --files 'labs/*'` printing `CLAIMS OK`, `--group rest` printing `CLAIMS FAIL 338 error(s)` (no `apps/` candidates covered), and `0` removed lines in `git diff`.

## Assumptions worked past
- **Multi-number expressions split per claim (`K0025`, `K0079`, `K0083`, `K0085`, `K0102`, `K0105`, `K0110`, `K0111`):** Eight candidates bundle two independent physical/threshold quantities in one line (Fahrenheit offset `32.0` + ratio `5.0 / 9.0`; `60.0` s/min + `2.0` rev/cycle; default `14.0` V + `0 - 18` V schema range; `load > 70%` + `rpm < 1500`; `rpm < 1000` + `load < 25%`; `rpm > 2000` + `load > 45%`), so each emits two `RK` rows under the same `cand_id`, giving 210 claim rows over 202 candidates.
- **Historical trim/VE/IAT code discrepancies cross-referenced cleanly (`CK` not placed in `same_as`):** Consistent with `check_code_claims.py` (which only accepts `W\d{4}` or earlier `RK\d{4}` in `same_as`), COMLab mirrors (`CK0046`, `CK0181`, `CK0182`, `CK0186`, `CK0189`, `CK0193`, `CK0194`) are noted in the `suspect` rationale strings rather than `same_as`.
- **Unarchived source doc citations preserved verbatim:** Two `dtclab/core/freeze_frame_extractor.py` thresholds (`K0103`, `K0104`) cite `DTC_WIKI.md` (`§3`, `§8.2`), which is not present in `labs/` or `Vault/`, and seven `ve_engine.py` entries (`K0064`–`K0069`, `K0071`) cite `BP §1.B / §1.C` or `BP §2` (no standalone `BP` doc exists in the clone, though `LLD_OBDLab.md §6–§7` echoes the six target VE fractions). Recorded verbatim and disclosed below.

## Step 1 Disclosure & Claims Summary
- **Scope covered:** 202 non-auto `labs/` candidates across 20 files -> **210** claims (`RK0001`–`RK0210`).
- **Classes:** `ANALYSER_SPEC=45`, `DIAGNOSTIC_THRESHOLD=34`, `INTERNAL_PARAMETER=31`, `NON_DOMAIN=75`, `PHYSICAL_CONSTANT=21`, `TYPICAL_RANGE=4`.
- **`same_as`:** `same_as_wiki=5` (`W0066` x1, `W0079` x2, `W0116` x1, `W0118` x1); `same_as_rk=28`.
- **Empty `citation`:** `28` claims total (`11` unreferenced code defaults/math/clamp parameters `RK0044`, `RK0046`, `RK0048`, `RK0063`, `RK0067`, `RK0069`, `RK0070`, `RK0071`, `RK0076`, `RK0090`, `RK0110`; `17` `NON_DOMAIN` sentinels/notes/guards).
- **"Citation not found" in repo (`labs/` or `Vault/`):** `9` claims total (`2` citing missing `DTC_WIKI.md`: `RK0092` (`K0103`), `RK0093` (`K0104`); `7` citing unarchived `BP`: `RK0052`–`RK0057` (`K0064`–`K0069`), `RK0059` (`K0071`)).
- **`suspect`: `20` claims:**
  1. `RK0014` (`K0015`, `labs/obdlab/obdlab/core/o2_normalizer.py:31`): `0.50 V` — `OBDLab_KG_Wiki.md §11.1` puts `STOICHIOMETRIC_CENTER` at `0.41-0.59 V` and `RICH_STATE` at `0.60-0.90 V`; code uses `0.50 V` upper bound (cf. `CK0046`).
  2. `RK0030` (`K0031`, `labs/obdlab/obdlab/core/pid_ingestion_validator.py:99`): `-127 - 127 %` — cited chunk `research/chunks/fuel-trim/13` has no `-127/+127` bound; SAE J1979 `OBDLab_KG_Wiki.md §3.1` specifies `-100.0` to `+99.22%` (cf. `CK0181`).
  3. `RK0031` (`K0037`, `labs/obdlab/obdlab/core/semantic_consistency_checker.py:18`): `-127.0 %` — `OBDLab_KG_Wiki.md §3.1` and `§4 Physics_Gate_4` specify `-100.0%` minimum; `-127.0` is raw byte rail (cf. `CK0181`).
  4. `RK0032` (`K0038`, `labs/obdlab/obdlab/core/semantic_consistency_checker.py:19`): `127.0 %` — `OBDLab_KG_Wiki.md §3.1` and `§4 Physics_Gate_4` specify `+99.22%` maximum; `127.0` is raw byte rail (cf. `CK0181`).
  5. `RK0062` (`K0074`, `labs/obdlab/obdlab/core/ve_engine.py:50`): `90.0 %` — `OBDLab_KG_Wiki.md §6.4` and `§10.3` specify `> 85%` for `FAULT_VE_SENSOR_SKEW`; `90.0%` comes from `§4 Physics_Gate_3`.
  6. `RK0082` (`K0094`, `labs/obdlab/obdlab/schemas/payload.py:53`): `-127 - 127 %` (`shrtft1`) — `OBDLab_KG_Wiki.md §3.1` specifies `-100.0` to `+99.22%` for SAE J1979 fuel trim (cf. `CK0181`).
  7. `RK0083` (`K0095`, `labs/obdlab/obdlab/schemas/payload.py:57`): `-127 - 127 %` (`longft1`) — `OBDLab_KG_Wiki.md §3.1` specifies `-100.0` to `+99.22%` for SAE J1979 fuel trim (cf. `CK0182`).
  8. `RK0084` (`K0096`, `labs/obdlab/obdlab/schemas/payload.py:60`): `-127 - 127 %` (`shrtft2`) — `OBDLab_KG_Wiki.md §3.1` specifies `-100.0` to `+99.22%` for SAE J1979 fuel trim (cf. `CK0193`).
  9. `RK0085` (`K0097`, `labs/obdlab/obdlab/schemas/payload.py:63`): `-127 - 127 %` (`longft2`) — `OBDLab_KG_Wiki.md §3.1` specifies `-100.0` to `+99.22%` for SAE J1979 fuel trim (cf. `CK0194`).
  10. `RK0087` (`K0099`, `labs/obdlab/obdlab/schemas/payload.py:81`): `0.0 - 200.0 %` (`ve_pct`) — `OBDLab_KG_Wiki.md §6.4` rejects VE above `100%` rather than `200%`; cf. `CK0189` and COMLab `0-100%`.
  11. `RK0088` (`K0100`, `labs/obdlab/obdlab/schemas/payload.py:106`): `-40 - 140 °C` (`intake_air_temp_c`) — `OBDLab_KG_Wiki.md §3.1` specifies `-40` to `80°C` for `intake_air_temp_c` (cf. `CK0186`).
  12. `RK0191` (`K0759`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:30`): `-127.0 %` (`shrtft1` min) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `-100.0%` SAE J1979 minimum; `-127.0` is raw byte rail (cf. `CK0181`).
  13. `RK0192` (`K0760`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:31`): `127.0 %` (`shrtft1` max) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `+99.22%` SAE J1979 maximum; `127.0` is raw byte rail (cf. `CK0181`).
  14. `RK0194` (`K0763`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:36`): `-127.0 %` (`longft1` min) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `-100.0%` SAE J1979 minimum; `-127.0` is raw byte rail (cf. `CK0182`).
  15. `RK0195` (`K0764`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:37`): `127.0 %` (`longft1` max) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `+99.22%` SAE J1979 maximum; `127.0` is raw byte rail (cf. `CK0182`).
  16. `RK0197` (`K0767`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:42`): `-127.0 %` (`shrtft2` min) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `-100.0%` SAE J1979 minimum; `-127.0` is raw byte rail (cf. `CK0193`).
  17. `RK0198` (`K0768`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:43`): `127.0 %` (`shrtft2` max) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `+99.22%` SAE J1979 maximum; `127.0` is raw byte rail (cf. `CK0193`).
  18. `RK0200` (`K0771`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:48`): `-127.0 %` (`longft2` min) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `-100.0%` SAE J1979 minimum; `-127.0` is raw byte rail (cf. `CK0194`).
  19. `RK0201` (`K0772`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:49`): `127.0 %` (`longft2` max) — `OBDLab_KG_Wiki.md §3.1` and `§4` specify `+99.22%` SAE J1979 maximum; `127.0` is raw byte rail (cf. `CK0194`).
  20. `RK0204` (`K0775`, `labs/obdlab/obdlab/config/physical_sensor_bounds.json:55`): `140.0 °C` (`intake_air_temp_c` max) — `OBDLab_KG_Wiki.md §3.1` specifies `80°C` max for `intake_air_temp_c`; `140.0°C` matches coolant max (cf. `CK0186`).

## VERIFICATION GATE
- `C:/4DApp/.venv/Scripts/python.exe apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest --files 'labs/*'` -> `classes ANALYSER_SPEC=45 DIAGNOSTIC_THRESHOLD=34 INTERNAL_PARAMETER=31 NON_DOMAIN=75 PHYSICAL_CONSTANT=21 TYPICAL_RANGE=4` / `suspect 20 same_as_wiki 5` / `CLAIMS OK group=rest scope=labs/* candidates 202 covered claims 210` (0 errors).
- `C:/4DApp/.venv/Scripts/python.exe apps/wired/audit_tasks/codeaudit/check_code_claims.py --group rest` -> `CLAIMS FAIL 338 error(s)` (all 338 `uncovered` under `apps/`, unchanged from baseline).
- `git diff --numstat apps/wired/audit_tasks/codeaudit/claims_rest.csv` -> `210	0	apps/wired/audit_tasks/codeaudit/claims_rest.csv` (`0` removed lines).

## CODE REVIEW
- Checked `claims_rest.csv` header (`claim_id,cand_id,file,line,quantity,value,unit,condition,class,citation,same_as,suspect`), monotonic `RK0001`–`RK0210` numbering in exact `candidates_rest.csv` order, UTF-8 without mojibake, and `same_as` integrity (zero `CK` targets; 5 `W` targets; 28 earlier `RK` targets).
- Verified scope isolation: zero `apps/` candidates covered; zero modifications to source files, `candidates_rest.csv`, or `check_code_claims.py`.

## Time
| Start UTC | End UTC | Elapsed | Budget | Notes |
|---|---|---|---|---|
| `2026-11-15T19:04:54Z` | `2026-11-15T19:15:03Z` | ~10 min | 25 min | Audited 202 `labs/` candidates across 20 files against wikis/docs/chunks and GASLab/COMLab ledgers; emitted 210 claims (`RK0001`–`RK0210`). |
