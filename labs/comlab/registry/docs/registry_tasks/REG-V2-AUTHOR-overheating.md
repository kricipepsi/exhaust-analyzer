### Goal ###

Author the v2 registry rule file at `registry/rules/overheating.json` containing 4 competing rules for the new `overheating` fault family (from cvsgaps.md gap analysis). Populate the 4 placeholder curated cases (NEW-overheating-01 through -04) with realistic gas/OBD values representing overheating diagnostic patterns. This is the first **OBD-primary** family in the registry: the diagnostic signals are coolant temperature (ECT), idle RPM, and DTCs. Gas chemistry plays little or no diagnostic role for classic overheating — `HIGH_COMBUSTION_TEMP` (NOx ≥ 1500 ppm per GAS_VOCABULARY §10.5) is unreachable at idle on a street engine, so three of four rules carry no `chemistry_evidence`. Only OV-003 (head gasket / coolant loss) carries `COOLANT_LEAK_INTERNAL` chemistry as SUGGESTIVE, because the gas fingerprint (CO₂ displaced, NOx suppressed) supports the diagnosis alongside the primary ECT+P0117 signal. This is the second of three new cvsgaps.md families; it has zero v1 rules and no prior Python evaluation logic to rebuild.

### Success criteria ###

- `registry/rules/overheating.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 4 rules with unique `rule_id` values (OV-001 through OV-004)
- Every rule has `passes_cases` with at least one NEW-overheating case ID that resolves to an `overheating`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation — ECT thresholds cite `OBD_VOCABULARY §23.1`, RPM thresholds cite `OBD_VOCABULARY §23.2`, DTCs cite `DTC_VOCABULARY §4` (no bare magic numbers)
- At least 3 of 4 rules have empty `chemistry_evidence` (OV-001, OV-002, OV-004) — this is an OBD-primary family; the only rule with chemistry is OV-003 (COOLANT_LEAK_INTERNAL SUGGESTIVE)
- At least 1 rule is DTC-driven (OV-002 — P0128 thermostat GATING)
- At least 1 rule handles a non-DTC overheating scenario (OV-004 — fan failure, no DTC, no elevated RPM)
- No solo survivor: the `overheating` competition group has ≥ 2 rules, and every rule carries `confidence_ceiling`
- The 4 NEW-overheating placeholder rows in `corpus_curated.csv` are populated with realistic gas/OBD values (idle gas columns, OBD PIDs including ECT and RPM, 2500 RPM gas columns)
- `corpus_meta.json` placeholder notes updated from "To be populated" to "Populated during REG-V2-AUTHOR-overheating"
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py` and all 14 existing rule test files continue to pass
- New test `registry/tests/test_overheating_rules.py::test_ruleset_validates` passes

### Context ###

overheating is a new fault family per `cvsgaps.md` — "a major survey notes [cooling system faults] as a leading engine problem." The v1 registry has zero rules for overheating; the 281-case corpus has no dedicated overheating test cases. The plan §10.2 specifies 3-4 cases with detection signal: "High coolant temp + RPM behaviour; not always DTC-driven." The 4 placeholder cases in `corpus_curated.csv` carry only case_id and fault_family labels — all gas/OBD columns are blank.

**Why OBD-primary and chemistry-light.** GAS_VOCABULARY §10.5 defines `high_combustion_temp` as NOx ≥ 1500 ppm. At idle (650–1100 RPM) on a modern emission-controlled street engine, NOx does not reach 1500 ppm even with the thermostat stuck closed — the engine is producing negligible load. All realistic overheating case values (NOx 200–600 ppm) fall in the `elevated_idle` or `high_idle` bands, so GASLab will never emit `HIGH_COMBUSTION_TEMP` for these cases. Rules that gate on HIGH_COMBUSTION_TEMP as DEFINITIVE would never fire — the spec contradicts itself. The honest design: three of four rules carry empty `chemistry_evidence` (like EF-001/EF-002/EF-003 in ecu_fault). Only OV-003 carries COOLANT_LEAK_INTERNAL as SUGGESTIVE, because the gas pattern (CO₂ displaced, NOx suppressed) may be emitted by GASLab's rule engine given the synthetic values — but the emission is not guaranteed, so the tier is SUGGESTIVE, not DEFINITIVE, and `confidence_ceiling` is lowered accordingly.

**ECT operational thresholds (OBD_VOCABULARY §23.1 — new section added this session):**

| Band | ECT range | Diagnostic meaning |
|---|---|---|
| `NORMAL_OPERATING` | 88 – 95°C | Thermostat open; steady-state |
| `ELEVATED_TEMP` | 105 – 110°C | Thermostat sticking, fan degradation, or coolant loss — below dash warning |
| `OVERHEATING_THRESHOLD` | ≥ 108°C | Sustained at idle = cooling-system fault probable |
| `SEVERE_OVERHEAT` | ≥ 115°C | ECU forces OL_FAULT enrichment to cool catalyst; dash warning triggers |
| `CRITICAL_OVERHEAT` | ≥ 120°C | Head-gasket damage risk; coolant boiling risk |

**Idle RPM in overheating context (OBD_VOCABULARY §23.2):**

| RPM band | Range | Meaning |
|---|---|---|
| `NORMAL_HOT_IDLE` | 650 – 900 RPM | Normal warm-engine idle |
| `ECU_COOLING_IDLE` | 1000 – 1200 RPM | ECU-elevated idle target during detected overheat |
| `IDLE_NOT_ELEVATED` | < 1000 RPM | No ECU cooling response — undetected overheat |

The diagnostic discriminator (OBD_VOCABULARY §23.3): ECT ≥ 108°C + RPM ≥ 1000 → ECU-detected overheat (thermostat stuck closed, coolant loss). ECT ≥ 105°C + RPM < 1000 → undetected overheat (fan failure where ECT sensor location misses the hot spot, or gradual coolant loss below sensor threshold).

The 4 cases represent four severity/etiology profiles:
1. **NEW-overheating-01** — Thermostat stuck partially closed, moderate overheat, no DTC yet. ECT=112°C (OVERHEATING_THRESHOLD), RPM=1050 (ECU_COOLING_IDLE). Gas: λ=1.01, HC=15 ppm, CO=0.15%, CO₂=14.8%, O₂=0.4%, NOx=550 ppm (high_idle band — elevated but below HIGH_COMBUSTION_TEMP). At 2500 RPM: λ=1.00, HC=10 ppm, CO=0.10%, CO₂=15.0%, O₂=0.3%, NOx=350 ppm (radiator airflow cools the engine at speed).
2. **NEW-overheating-02** — Thermostat failure with P0128 DTC. ECT=108°C (OVERHEATING_THRESHOLD), RPM=950 (NORMAL_HOT_IDLE — ECU has not elevated idle despite the DTC). Gas: λ=1.00, HC=10 ppm, CO=0.10%, CO₂=15.0%, O₂=0.3%, NOx=400 ppm. At 2500 RPM: λ=1.00, HC=8 ppm, CO=0.08%, CO₂=15.2%, O₂=0.2%, NOx=250 ppm.
3. **NEW-overheating-03** — Head gasket failure → internal coolant leak. ECT=120°C (CRITICAL_OVERHEAT), RPM=1100 (ECU_COOLING_IDLE). P0117 DTC. Gas: λ=1.03 (slight lean from steam displacement), HC=30 ppm (steam quenches flame), CO=0.25% (partial combustion), CO₂=12.5% (displaced by steam — below combustion_deficit per GAS_VOCABULARY §10.3), O₂=2.0% (moderate), NOx=200 ppm (suppressed by steam quench). At 2500 RPM: λ=1.02, HC=20 ppm, CO=0.15%, CO₂=13.5%, O₂=1.5%, NOx=150 ppm. The gas fingerprint (CO₂ low, NOx suppressed, HC moderate) is consistent with the COOLANT_LEAK_INTERNAL pattern per GAS_WIKI §7.32.
4. **NEW-overheating-04** — Electric radiator fan failure, no DTC generated yet. ECT=106°C (ELEVATED_TEMP — above normal but below OVERHEATING_THRESHOLD), RPM=850 (NORMAL_HOT_IDLE — no ECU detection). Gas: λ=1.00, HC=8 ppm, CO=0.08%, CO₂=15.1%, O₂=0.2%, NOx=380 ppm. At 2500 RPM: λ=1.00, HC=6 ppm, CO=0.06%, CO₂=15.3%, O₂=0.2%, NOx=220 ppm. The distinguishing feature: ECT is elevated but RPM stays in normal range because the ECU hasn't detected the fan failure.

Cross-family note: overheating has no direct competition with existing families. No existing rule family uses ECT or RPM thresholds as primary evidence. The confidence_ceiling values can be higher than for families that share chemistry with lean_condition (e.g., vacuum_leak), because overheating is diagnostic-orthogonal — a case can simultaneously be lean and overheating. The main diagnostic challenge: ECT thresholds alone are a weak classifier; the RPM-differential matrix (§23.3) and the absence/presence of specific DTCs (P0128, P0117) provide the diagnostic specificity.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/overheating.json` — CREATE: RuleSet JSON with 4 rules for overheating family. Minimum rules:
   - OV-001: Classic overheating — thermostat stuck closed (no DTC required). OBD-primary: ect gt 110.0 as DEFINITIVE (OVERHEATING_THRESHOLD per OBD_VOCABULARY §23.1; 110°C is above the 108°C threshold, giving a 2°C margin above the diagnostic boundary). rpm gt 1000.0 as SUGGESTIVE (ECU_COOLING_IDLE per OBD_VOCABULARY §23.2). chemistry_evidence: [] — HIGH_COMBUSTION_TEMP is unreachable at idle NOx levels (GAS_VOCABULARY §10.5 min 1500 ppm) on a street engine. confidence_ceiling = 0.85 (ECT DEFINITIVE is a strong direct signal; no chemistry backing, but overheating is diagnostic-orthogonal to other families — no shared-chemistry ceiling required). Covers NEW-overheating-01.
   - OV-002: DTC-driven thermostat failure. DTC-primary: P0128 with strategy any_match as GATING (coolant thermostat malfunction per DTC_VOCABULARY §4). OBD: ect gt 105.0 as SUGGESTIVE (ELEVATED_TEMP per OBD_VOCABULARY §23.1). chemistry_evidence: []. confidence_ceiling = 0.85 (P0128 is a definitive thermostat DTC — DTC-gated with consistent ECT elevation). Covers NEW-overheating-02.
   - OV-003: Coolant loss / head gasket internal leak. OBD-primary: ect gt 115.0 as DEFINITIVE (SEVERE_OVERHEAT per OBD_VOCABULARY §23.1). DTC: P0117 with strategy any_match as SUGGESTIVE (ECT circuit low — coolant loss exposes sensor to steam pockets per DTC_VOCABULARY §4). chemistry_evidence: COOLANT_LEAK_INTERNAL as SUGGESTIVE (gas fingerprint consistent with coolant ingress per GAS_VOCABULARY §3; emission by GASLab's rule engine is not guaranteed at these values, but the CO₂-displaced/NOx-suppressed pattern is present per GAS_WIKI §7.32). confidence_ceiling = 0.82 (SEVERE_OVERHEAT ECT + P0117 + SUGGESTIVE chemistry; ceiling lowered because chemistry emission is not guaranteed). Covers NEW-overheating-03.
   - OV-004: Silent fan failure (no DTC, no elevated RPM). OBD-primary: ect gt 105.0 as DEFINITIVE (ELEVATED_TEMP per OBD_VOCABULARY §23.1 — the primary and only strong signal). rpm lt 1000.0 as SUGGESTIVE (IDLE_NOT_ELEVATED per OBD_VOCABULARY §23.2 — ECU hasn't detected the overheat, consistent with fan failure where the ECT sensor doesn't see the radiator-side temperature). chemistry_evidence: []. confidence_ceiling = 0.70 (weakest signal of the four — no DTC, modest ECT elevation, and the RPM lt threshold is the only differentiator from OV-001). Covers NEW-overheating-04.
2. `registry/tests/test_overheating_rules.py` — CREATE: targeted tests following the pattern in `test_vacuum_leak_rules.py`. Tests: file exists, valid JSON, ruleset validates, exactly 4 rules, no duplicate IDs, all rule_ids match OV-00x pattern, every rule has passes_cases with ≥ 1 case, every passes_cases ID resolves in corpus_curated.csv, every rule has confidence_ceiling set, OV-001/OV-002/OV-004 have empty chemistry_evidence, OV-003 has COOLANT_LEAK_INTERNAL SUGGESTIVE, OV-001 has ect gt 110.0 DEFINITIVE and rpm gt 1000.0 SUGGESTIVE, OV-002 has P0128 DTC with GATING and ect gt 105.0 SUGGESTIVE, OV-003 has ect gt 115.0 DEFINITIVE and P0117 SUGGESTIVE, OV-004 has ect gt 105.0 DEFINITIVE and rpm lt 1000.0 SUGGESTIVE, no rule has imports from any lab.
3. `registry/corpus_curated.csv` — MODIFY: populate the 4 NEW-overheating placeholder rows (rows for case IDs NEW-overheating-01 through -04) with realistic gas/OBD values per the severity profiles above. Fill idle gas columns (hc, co, co2, o2, nox, lambda_analyser), OBD columns (stft_b1, ltft_b1, map, rpm, ect, dtcs), and 2500 RPM gas columns (hc_2500, co_2500, co2_2500, o2_2500, nox_2500, lambda_2500). Leave other columns (stft_b2, ltft_b2, o2_upstream_classification, o2_downstream_voltage, maf, vehicle_speed, fuel_pressure, ff_*, vin_*, vin_noise_rpm, vin_co_type_approval, etc.) as blank unless a value is needed for rule evidence.
4. `registry/corpus_meta.json` — MODIFY: update the 4 NEW-overheating entries' `notes` field from "Placeholder case. To be populated with real gas/OBD values during REG-V2-AUTHOR-overheating." to "Populated during REG-V2-AUTHOR-overheating — <one-line severity description>."

### Files to touch ###

- `registry/rules/overheating.json` (CREATE)
- `registry/tests/test_overheating_rules.py` (CREATE)
- `registry/corpus_curated.csv` (MODIFY — 4 rows only, NEW-overheating-01 through -04)
- `registry/corpus_meta.json` (MODIFY — 4 entries only, notes field)

### Out of scope ###

- Other new families (charging_system) — gets its own REG-V2-AUTHOR-charging_system session
- DTC-driven cooling system codes beyond P0116-P0128 (P0125, P0480, P0481 fan codes) — out of scope for petrol v1
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream
- Adding a new ChemistryState enum value for overheating-specific chemistry — existing COOLANT_LEAK_INTERNAL covers the one chemistry-using rule; HIGH_COMBUSTION_TEMP is correctly unused
- RPM-contextualized evidence in schema_v2.py — the current flat OBD evidence model is sufficient; the ECT + RPM differentiator lives in case data and rule thresholds
- Cooling system faults beyond petrol scope (diesel EGR cooler, hybrid inverter cooling)

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_overheating_rules.py --fix
pyright registry/tests/test_overheating_rules.py

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
pytest registry/tests/test_vacuum_leak_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/overheating.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/overheating.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/overheating.json').read_text())
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
        if row['case_id'].startswith('NEW-overheating'):
            assert row['hc'], f'{row[\"case_id\"]}: hc is blank'
            assert row['lambda_analyser'], f'{row[\"case_id\"]}: lambda_analyser is blank'
            assert row['lambda_2500'], f'{row[\"case_id\"]}: lambda_2500 is blank'
            assert row['ect'], f'{row[\"case_id\"]}: ect is blank'
            assert row['rpm'], f'{row[\"case_id\"]}: rpm is blank'
    print('All 4 overheating cases have populated values')
"

# Targeted tests
pytest registry/tests/test_overheating_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-overheating`: Status=done, Files changed=4, Verification="{HEADLINE}"
