# T-AUD-22d progress note: COMLab global fault registry literal inventory

## Readiness challenge

- (a) Starting state matches task (with lane-rule branch `agy/T-AUD-22d`): `git log --oneline fix/T-COMA-32..HEAD` shows `53e862c` and `5d9df13`, `git status --porcelain` is empty, and preconditions print `checked` with no `MISSING` line.
- (b) Decisive check fails for the intended reason: step 1 prints `CLAIMS FAIL 303 error(s)` (all `uncovered`, P2); step 3 prints `CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 691` (P4).
- (c) Independently derived counts from `candidates_comlab.csv`: 303 non-auto candidates in `labs/comlab/comlab/config/global_fault_registry.json` (P1) — `base_weight` 104, `bonus_on_dtc_match` 104, `ui_diagnostic_string` 35, `value` 32, bare array numbers 8, `fault_wiki_page` 1, `remediation_map` 19 (P5); `knobs 208 internal 0` (P3).
- (d) No contradiction or missing decision prevents implementation. Choices left open by R1–R7 are recorded under `Assumptions worked past`.
- (e) Teach-back: append classified or `NON_DOMAIN` rows `CK0693`+ to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` for all 303 non-auto candidates of `global_fault_registry.json`, with empty `citation`, `same_as` to matching `W`/`CK` claims, and `suspect` for contradictions. Decisive check: step 1 prints `CLAIMS OK ... candidates 303` with no `ERROR`, step 2 prints `knobs 208 internal 208`, step 3 keeps `candidates 357` and `CK0001`-`CK0692` unchanged, and step 4 shows `0` removed lines.

## Assumptions worked past

1. **Lane rules (`T-AUD-22d.go.txt`):** branch is `agy/T-AUD-22d` (not `fix/T-AUD-22d`), no `git commit`/`push`/`switch`/`checkout`, only the three files in `### Files to touch ###` are written (no throwaway scripts/files on disk).
2. **`IN_RANGE` PID arrays:** following `CK0323`/`CK0324` (`T-AUD-22c`), each `IN_RANGE` two-line array emits two `DIAGNOSTIC_THRESHOLD` rows: `<pid> in_range lower edge` and `<pid> in_range upper edge`, with condition `<fault_id> <gas_lab_state>, IN_RANGE`.
3. **Scalar `obd_live_pids` values:** `condition` is `<fault_id> <gas_lab_state>, <operator>`, and `value` pairs the operator symbol (`>`, `≥`, `<`, `≤`) with the literal number.
4. **Condition numerals in prose (`ui_diagnostic_string`, `remediation_map`):** `at 2500 RPM` (backpressure test) and `at 20 C` (coil resistance test temperature) are captured in `condition` rather than emitted as separate RPM/temperature claims. Single DTC codes (`P0014/P0024`, `P0010/P0020`, `P0131/P0132/P0134`, `P0335/P0336`, `P0300`), mode numbers (`Mode 06`, `Mode $06`), and PID hex identifiers (`PID $0C`) are omitted or marked `NON_DOMAIN` per R5 (`K0986`, `K0993`, `K0996`, plus `fault_wiki_page` `K0813`).
5. **Classes for prose claims:** diagnostic cut-offs and fault-signature bands are `DIAGNOSTIC_THRESHOLD`; nominal healthy baselines/OEM component resistance/cleaning intervals/post-repair targets are `TYPICAL_RANGE`; `5 V` ECU sensor reference supply (`K0938`, `K0942`) is `ANALYSER_SPEC` (consistent with `CK0180`); `lambda_chem` `1.0` stoichiometric ground truth (`K1024`) is `PHYSICAL_CONSTANT` (`same_as W0079`).
6. **GDI cleaning interval formatting:** `K1023` (`60 000-100 000 km`) keeps the spaced thousands (`60 000-100 000`) so `check_code_claims.py`'s `NUM_RE` matches the line text.
7. **Duplicate `fault_id`s in `global_fault_registry.json`:** `ERR-CT-003`, `ERR-LC-004`, `ERR-MF-002`, and `ERR-SF-001` each appear twice in `registry`. Where an earlier `registry base_weight` or `registry bonus_on_dtc_match` row shares the exact `(quantity, fault_id, value)`, `same_as` points to the first occurrence (4 rows: `ERR-CT-003` `base_weight 0.8`, `ERR-MF-002` `base_weight 0.75` and `bonus_on_dtc_match 0.15`, `ERR-SF-001` `base_weight 0.7` and `bonus_on_dtc_match 0.0` — 5 rows total).
8. **`same_as` across files:** `W` links are set only on matching quantity, condition, and value (`W0322`, `W0323`, `W1390` ×3, `W0417`, `W0079`). `CK` links to `CK0001`-`CK0692` are set on exact fault/rule matches (`CK0465` for `ERR-MW-002`, `CK0520` for `ERR-MF-002` `RICH_MISFIRE`, `CK0634` for `ERR-SF-002` stuck lean `< 0.2 V`). `ERR-MW-005` `map_kpa < 30.0` cites `CK0469` (`MW-004`, removed in `T-COMA-32`) in `suspect` rather than `same_as` because the fault/gas state differs (`INCOMPLETE_COMBUSTION` vs `WORN_ENGINE`).

## Figures (criterion 4)

Step 1 whole-group figures:
- `classes ANALYSER_SPEC=28 DIAGNOSTIC_THRESHOLD=370 INTERNAL_PARAMETER=448 NON_DOMAIN=140 PHYSICAL_CONSTANT=7 TYPICAL_RANGE=32`
- `suspect 46 same_as_wiki 27`
- `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025`

New rows only (`CK0693`-`CK1026`, 334 rows covering all 303 non-auto candidates):
- Classes: `INTERNAL_PARAMETER 208` (all 208 scoring knobs), `DIAGNOSTIC_THRESHOLD 105`, `TYPICAL_RANGE 14`, `NON_DOMAIN 4` (`K0813`, `K0986`, `K0993`, `K0996`), `ANALYSER_SPEC 2`, `PHYSICAL_CONSTANT 1`.
- Links and suspects: `suspect 12`, `same_as_wiki 7`, `same_as` an earlier `CK` `20`, empty `citation` `334` (per R6).

## New suspect claims (12)

| claim | cand / line | quantity & value | reason |
|---|---|---|---|
| CK0714 | K0453 / L184 | `o2_b1s2_v in_range lower edge` `0.4` V | `OBD_VOCABULARY §12.5` and `wiki/07 §7.3` state a dead/degraded catalyst causes post-cat O2 to switch (mirroring upstream), not sit flat at `0.4–0.5 V` reference voltage; with `CO > 1.5 %` (`K0451`) a live narrowband sensor reads rich (`> 0.6 V`) |
| CK0715 | K0454 / L185 | `o2_b1s2_v in_range upper edge` `0.5` V | same as `CK0714` |
| CK0757 | K0561 / L603 | `ect_c` `> 90.0` °C | `MW-003` in `labs/comlab/registry/rules/mechanical_wear.json:98` (`CK0464`) tightened v1 `ERR-MW-002` from `> 90.0` to `> 95.0 °C`; `OBD_VOCABULARY §23.1` `FAN_RANGE` is `95–105 °C` |
| CK0770 | K0587 / L700 | `map_kpa` `< 30.0` kPa | low compression causes weak manifold vacuum (higher absolute MAP), whereas `< 30.0 kPa` tests strong vacuum; contradicts `K0586` (`10-15 inHg` ≈ 50–67 kPa) and `T-COMA-32` removed this threshold from `MW-004` (`CK0469`) |
| CK0779 | K0602 / L761 | `map_kpa` `< 30.0` kPa | retarded cam timing with low compression causes weak manifold vacuum (higher absolute MAP, `wiki/06b:43`, `K0978` `10-15 inHg`), whereas `< 30.0 kPa` tests strong vacuum |
| CK0788 | K0620 / L827 | `hc` `1000-3000` ppm | `wiki/06b:41` (`W0697`) gives `CAM_TIMING_RETARDED_MAP` idle HC as `400–1200 ppm` (and 2500 rpm `200–600 ppm`), not `1000–3000 ppm` |
| CK0799 | K0638 / L912 | `co2` `3-6` % vol | `wiki/04 §4.14` (`W0350`/`W0351`) defines cranking `INCOMPLETE_COMBUSTION` as `5.0 ≤ CO2 < 8.0 %` and routes `CO2 < 5.0 %` to `LEAN_MISFIRE` |
| CK0859 | K0789 / L1480 | `o2_voltage stuck rich` `> 0.7` V | `OBD_VOCABULARY §12.1` sets narrowband `STUCK_RICH` at pinned `> 0.85 V` (and `SF-003` `CK0635`/`CK0638` gate at `> 0.80 V` / `≥ 0.8 V`) |
| CK0934 | K0911 / L2249 | `co2` `3-6` % vol | `wiki/04 §4.14` (`W0350`/`W0351`) defines cranking `INCOMPLETE_COMBUSTION` as `5.0 ≤ CO2 < 8.0 %` and routes `CO2 < 5.0 %` to `LEAN_MISFIRE` |
| CK1021 | K1024 / L2813 | `upstream O2 switching frequency (healthy)` `> 0.5` Hz | `OBD_VOCABULARY §12.1` sets healthy narrowband switching frequency at `2–5 Hz` (MPI) or `2–3 Hz` (TBI) and classifies `< 0.5 Hz` as slow/dying |
| CK1022 | K1024 / L2813 | `upstream O2 switching frequency (lazy)` `< 0.25` Hz | `OBD_VOCABULARY §12.1` already classifies `< 0.5 Hz` as slow/dying, not `< 0.25 Hz` |
| CK1024 | K1025 / L2814 | `o2_voltage stuck rich` `> 0.7` V | `OBD_VOCABULARY §12.1` sets narrowband `STUCK_RICH` at pinned `> 0.85 V` (and `SF-003` `CK0635`/`CK0638` gate at `> 0.80 V` / `≥ 0.8 V`) |

## VERIFICATION GATE

```
# 1.
classes ANALYSER_SPEC=28 DIAGNOSTIC_THRESHOLD=370 INTERNAL_PARAMETER=448 NON_DOMAIN=140 PHYSICAL_CONSTANT=7 TYPICAL_RANGE=32
suspect 46 same_as_wiki 27
CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025
# 2.
knobs 208 internal 208
# 3.
CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 1025
# 4.
0
 M apps/wired/audit_tasks/codeaudit/claims_comlab.csv
?? apps/wired/audit_tasks/progress_notes/T-AUD-22d.md
?? apps/wired/audit_tasks/results/RESULT_T-AUD-22d.md
```

Earlier decisive failure (`CLAIMS FAIL 303 error(s)`, all `uncovered`) is absent, and no `ERROR` line is printed.

## CODE REVIEW

- `git diff --numstat -- apps/wired/audit_tasks/codeaudit/claims_comlab.csv`: `334 0`, `0` removed lines; rows `CK0001`-`CK0692` (691 rows) are unchanged.
- UTF-8 with LF line endings preserved (`claims_comlab.csv` has 0 CRLF); no double-encoded fields or JSON `\uXXXX` escapes (passes `check_code_claims.py` `mojibake()` check).
- Every numeric value in `value` matches the source line text via `check_code_claims.py`.
- Only `claims_comlab.csv`, `T-AUD-22d.md`, and `RESULT_T-AUD-22d.md` were written; no registry, rule, config, wiki, or vocabulary file was modified.

## Time

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | 2026-11-15T18:19:20Z | 2026-11-15T18:25:37Z | 6.3 | ABSENT |
