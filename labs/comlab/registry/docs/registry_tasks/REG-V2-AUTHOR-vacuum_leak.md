### Goal ###

Author the v2 registry rule file at `registry/rules/vacuum_leak.json` containing 3 competing rules for the new `vacuum_leak` fault family (from cvsgaps.md gap analysis). Populate the 4 placeholder curated cases (NEW-vacuum_leak-01 through -04) with realistic gas/OBD values representing the vacuum-leak diagnostic pattern at idle and 2500 RPM. The vacuum_leak family shares LEAN_MIXTURE chemistry with `lean_condition`; the RPM-dependent fuel-trim pattern (trims elevated at idle, correcting at 2500 RPM as manifold vacuum drops) is the diagnostic differentiator. This is the first of three new OBD/voltage-driven families; it has zero v1 rules and no prior Python evaluation logic to rebuild.

### Success criteria ###

- `registry/rules/vacuum_leak.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 3 rules with unique `rule_id` values (VL-001 through VL-003)
- Every rule has `passes_cases` with at least one NEW-vacuum_leak case ID that resolves to a `vacuum_leak`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 1 rule uses LEAN_MIXTURE chemistry as DEFINITIVE with OBD trim + MAP evidence (VL-001 — classic vacuum leak)
- At least 1 rule is DTC-driven (VL-002 — P0171/P0174 GATING)
- At least 1 rule gates on elevated MAP at idle (VL-003 — large-bore leak, MAP > 50 kPa)
- No solo survivor: the `vacuum_leak` competition group has ≥ 2 rules, and every rule carries `confidence_ceiling` (LEAN_MIXTURE chemistry shared with lean_condition family)
- The 4 NEW-vacuum_leak placeholder rows in `corpus_curated.csv` are populated with realistic gas/OBD values (idle gas columns, OBD PIDs, 2500 RPM gas columns)
- `corpus_meta.json` placeholder notes updated from "To be populated" to "Populated during REG-V2-AUTHOR-vacuum_leak"
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py` and all 11 existing rule test files continue to pass
- New test `registry/tests/test_vacuum_leak_rules.py::test_ruleset_validates` passes

### Context ###

vacuum_leak is a new fault family per `cvsgaps.md` — "the most frequent root cause of a lean condition DTC." The v1 registry classifies vacuum leaks under `lean_condition` (EXT-202, EXT-214) with no dedicated diagnostic pathway. CHEMISTRY_COVERAGE.md §3.3 grades this as a new family with 4 placeholder cases: "OBD-driven: LEAN_MIXTURE chemistry + trim correction at 2500 RPM. Competing rule with lean_condition." The 4 placeholder cases in `corpus_curated.csv` carry only case_id and fault_family labels — all gas/OBD columns are blank.

The diagnostic signature of a vacuum leak, per GAS_VOCABULARY and Brady/Hall:
- **At idle (high manifold vacuum):** unmetered atmospheric air enters through the leak, leaning the mixture. Brettschneider lambda > 1.03 (LEAN_MIXTURE). Fuel trims go positive (LTFT ≥ +10%, STFT ≥ +5%) as the ECU compensates. MAP is elevated (> 40 kPa at hot idle vs normal 30-40 kPa) because the manifold can't pull as deep a vacuum — some of the "vacuum" is vented to atmosphere.
- **At 2500 RPM (low manifold vacuum):** the fixed-size leak contributes proportionally less air. Lambda returns toward stoich (1.00-1.02). Trims normalize. This RPM-dependent behavior is the key differentiator from a true lean_condition (MAF under-read, fuel delivery issue) where trims remain elevated at all engine speeds.

The 4 cases represent four severity/evidence profiles:
1. **NEW-vacuum_leak-01** — Moderate vacuum leak, no DTC yet. λ=1.08 idle → λ=1.01 at 2500 RPM. LTFT +15%, STFT +8%, MAP 48 kPa.
2. **NEW-vacuum_leak-02** — Small vacuum leak with P0171 DTC triggered. λ=1.04 idle → λ=1.00 at 2500 RPM. LTFT +12%, STFT +5%, MAP 42 kPa.
3. **NEW-vacuum_leak-03** — Large-bore leak (brake booster / PCV disconnect). λ=1.15 idle → λ=1.03 at 2500 RPM (still slightly lean). LTFT +25%, STFT +20%, MAP 60 kPa.
4. **NEW-vacuum_leak-04** — Moderate leak, bank-2 only (V-engine), P0174 DTC. λ=1.06 idle → λ=1.01 at 2500 RPM. LTFT +18%, STFT +10%, MAP 50 kPa.

Cross-family competition with `lean_condition` (LC-001, LC-002, LC-003):
- All three lean_condition rules gate on LEAN_MIXTURE chemistry + positive trims.
- LC-001 (λ > 1.03, LTFT ≥ 10%, STFT ≥ 5%, P0171/P0174) has the highest overlap with vacuum_leak VL-001. Differentiated by: (a) vacuum_leak rules carry `confidence_ceiling` to prevent outcompeting lean_condition on shared chemistry; (b) vacuum_leak VL-003 adds elevated MAP at idle (> 50 kPa) which lean_condition cases typically don't have; (c) the 2500 RPM lambda_2500 column differentiates at the case-data level (vacuum_leak cases normalize to λ ≤ 1.03 at 2500 RPM; lean_condition cases stay lean).
- LC-002 (LEAN_MIXTURE + TIMING_RETARDED + low MAP < 40 kPa + LTFT ≥ 3%) — low MAP is the opposite of the vacuum_leak MAP pattern.
- LC-003 (LEAN_MIXTURE + low MAF + LTFT ≥ 8% + P0101/P0102) — MAF-specific, different signal entirely.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/vacuum_leak.json` — CREATE: RuleSet JSON with 3 rules for vacuum_leak family. Minimum rules:
   - VL-001: Classic vacuum leak (chemistry + trim pattern). Chemistry-primary: LEAN_MIXTURE as DEFINITIVE. OBD: longft1 ge 10.0 as SUGGESTIVE, shrtft1 ge 5.0 as SUGGESTIVE (positive trims at idle — the trim elevation pattern). map_kpa gt 40.0 as SUGGESTIVE (elevated MAP at idle — weaker vacuum due to leak, normal hot-idle MAP is 30-40 kPa). confidence_ceiling = 0.85 because LEAN_MIXTURE chemistry is shared with lean_condition family (LC-001/LC-002/LC-003). Covers NEW-vacuum_leak-01, NEW-vacuum_leak-04.
   - VL-002: DTC-driven vacuum leak. DTC-primary: P0171, P0174 with strategy any_match as GATING (fuel system lean DTCs — the ECU has already detected the lean condition). Chemistry: LEAN_MIXTURE as SUGGESTIVE (consistent with the lean DTC). OBD: longft1 ge 8.0 as SUGGESTIVE, shrtft1 ge 3.0 as SUGGESTIVE. confidence_ceiling = 0.80 because DTC-only gating without chemistry DEFINITIVE evidence. Covers NEW-vacuum_leak-02.
   - VL-003: Large-bore vacuum leak (brake booster / PCV disconnect). Chemistry-primary: LEAN_MIXTURE as DEFINITIVE. OBD: map_kpa gt 50.0 as GATING (very high MAP at idle — manifold vacuum near collapse, > 50 kPa at hot idle is well above normal; wiki: OBD_VOCABULARY §3). longft1 ge 15.0 as SUGGESTIVE, shrtft1 ge 10.0 as SUGGESTIVE (very high trims trying to compensate for massive leak). confidence_ceiling = 0.80 because LEAN_MIXTURE chemistry is shared with lean_condition; the MAP gating is the key differentiator. Covers NEW-vacuum_leak-03.
2. `registry/tests/test_vacuum_leak_rules.py` — CREATE: targeted tests following the pattern in `test_non_starter_rules.py`. Tests: file exists, valid JSON, ruleset validates, exactly 3 rules, no duplicate IDs, all rule_ids match VL-00x pattern, every rule has passes_cases with ≥ 1 case, every passes_cases ID resolves in corpus_curated.csv, every rule has confidence_ceiling set, every rule has at least one chemistry_evidence entry, VL-001 has LEAN_MIXTURE DEFINITIVE, VL-002 has P0171/P0174 DTC with GATING, VL-003 has map_kpa gt 50.0 GATING, no rule has imports from any lab.
3. `registry/corpus_curated.csv` — MODIFY: populate the 4 NEW-vacuum_leak placeholder rows (rows for case IDs NEW-vacuum_leak-01 through -04) with realistic gas/OBD values per the severity profiles above. Fill idle gas columns (hc, co, co2, o2, nox, lambda_analyser), OBD columns (stft_b1, ltft_b1, map, rpm, ect, dtcs), and 2500 RPM gas columns (hc_2500, co_2500, co2_2500, o2_2500, nox_2500, lambda_2500). Leave other columns (stft_b2, ltft_b2, o2_upstream_classification, o2_downstream_voltage, maf, vehicle_speed, fuel_pressure, ff_*, vin_*, vin_noise_rpm, vin_co_type_approval, etc.) as blank unless a value is needed for rule evidence.
4. `registry/corpus_meta.json` — MODIFY: update the 4 NEW-vacuum_leak entries' `notes` field from "Placeholder case. To be populated with real gas/OBD values during REG-V2-AUTHOR-vacuum_leak." to "Populated during REG-V2-AUTHOR-vacuum_leak — <one-line severity description>."

### Files to touch ###

- `registry/rules/vacuum_leak.json` (CREATE)
- `registry/tests/test_vacuum_leak_rules.py` (CREATE)
- `registry/corpus_curated.csv` (MODIFY — 4 rows only, NEW-vacuum_leak-01 through -04)
- `registry/corpus_meta.json` (MODIFY — 4 entries only, notes field)

### Out of scope ###

- Other new families (overheating, charging_system) — each gets its own REG-V2-AUTHOR-{family} session
- lean_condition rule modifications — LC-001/LC-002/LC-003 are frozen; competition is handled via confidence_ceiling on the vacuum_leak side
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream
- Adding a dedicated VACUUM_LEAK routing tag to DTCRoutingTag — vacuum_leak uses existing LEAN_HISTORY / RICH_HISTORY routing tags via shared DTC patterns
- RPM-contextualized evidence in schema_v2.py — the current flat OBD evidence model is sufficient; the 2500 RPM differentiator lives in the case data (lambda_2500 column) and confidence_ceiling

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_vacuum_leak_rules.py --fix
pyright registry/tests/test_vacuum_leak_rules.py

# Existing tests must still pass
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q
pytest registry/tests/test_exhaust_leak_rules.py -x -q
pytest registry/tests/test_sensor_fault_rules.py -x -q
pytest registry/tests/test_ecu_fault_rules.py -x -q
pytest registry/tests/test_cam_timing_rules.py -x -q
pytest registry/tests/test_mechanical_wear_rules.py -x -q
pytest registry/tests/test_non_starter_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/vacuum_leak.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/vacuum_leak.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/vacuum_leak.json').read_text())
orphans = []
for r in rules['rules']:
    for cid in r['passes_cases']:
        if cid not in cases:
            orphans.append(f'{r[\"rule_id\"]}: {cid}')
if orphans:
    print('ORPHAN REFS:', orphans)
else:
    print(f'All {sum(len(r[\"passes_cases\"]) for r in rules[\"rules\"])} case refs resolve OK')
"

# Verify 4 curated cases now have populated values (not blank gas columns)
python3.14 -c "
import csv
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        if row['case_id'].startswith('NEW-vacuum_leak'):
            assert row['hc'], f'{row[\"case_id\"]}: hc is blank'
            assert row['lambda_analyser'], f'{row[\"case_id\"]}: lambda_analyser is blank'
            assert row['lambda_2500'], f'{row[\"case_id\"]}: lambda_2500 is blank'
            assert row['stft_b1'] or row['ltft_b1'], f'{row[\"case_id\"]}: both trims blank'
    print('All 4 vacuum_leak cases have populated values')
"

# Targeted tests
pytest registry/tests/test_vacuum_leak_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-vacuum_leak`: Status=done, Files changed=4, Verification="{HEADLINE}"
