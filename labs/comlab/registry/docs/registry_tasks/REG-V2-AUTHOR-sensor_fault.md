### Goal ###

Author the v2 registry rule file at `registry/rules/sensor_fault.json` containing 6 competing rules for the `sensor_fault` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 6 rules (ERR-SF-001 through ERR-SF-006) but only ERR-SF-001 (O2 slow response, two perception-flag variants) and ERR-SF-002 (O2 fixed voltage) are executable — ERR-SF-003 (MAF under-reading), ERR-SF-004 (MAP drift), ERR-SF-005 (ECT stuck cold), and ERR-SF-006 (downstream O2 contaminated) are orphan KG nodes with no registry entries. The v2 rules must reactivate all 6 sensor-fault subtypes as evidence-tier rules, close the TIMING_RETARDED gap (~8 sensor_fault cases produce this chemistry with zero v1 rules accepting it), and use the O2 perception-flag truth-vs-perception pattern from ERR-SF-001 as the template for perception-only sensor faults. 6 rules, one per sensor fault anatomical site.

### Success criteria ###

- `registry/rules/sensor_fault.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 6 rules with unique `rule_id` values (SF-001 through SF-006, reactivating all 6 v1 sensor-fault subtypes)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `sensor_fault`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 2 rules use `NORMAL_OPERATION` chemistry as DEFINITIVE evidence (O2 perception-only faults — the ERR-SF-001/002 template)
- At least 2 rules use `TIMING_RETARDED` chemistry as SUGGESTIVE evidence (MAF/MAP sensor drift cases — closes the ~8-case Tier B gap)
- At least 2 rules carry a `perception_flag` (truth-vs-perception pattern — ground-truth chemistry is normal but ECU perception is skewed)
- At least 1 rule uses OBD ECT PID evidence (coolant temp sensor stuck cold)
- At least 1 rule uses OBD MAF PID evidence (MAF sensor under-reading)
- At least 1 rule uses OBD MAP PID evidence (MAP sensor calibration drift)
- At least 1 rule uses OBD downstream O2 PID evidence (downstream O2 sensor contaminated)
- At least 1 rule uses DTC evidence (O2 circuit DTCs P0131/P0132/P0134 for fixed-voltage sensor)
- No solo survivor: at least 2 rules carry a `confidence_ceiling`, and the `sensor_fault` competition group has ≥ 2 rules
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py`, `test_exhaust_leak_rules.py` continue to pass
- New test `registry/tests/test_sensor_fault_rules.py::test_ruleset_validates` passes

### Context ###

sensor_fault has 20 curated cases (16 kept from v1 + 4 that were dropped as sentinel/obsolete: CASE-010 leaded fuel, CASE-022 BARO edge, CASE-045 H2 cross-sensitivity, CASE-048 analyser thermal drift). The 20 kept cases span 6 anatomical sensor-fault sites, but v1 only executes 2 of 6 — 4 KG nodes are orphans. The active v1 rules both gate on `NORMAL_OPERATION` chemistry: ERR-SF-001 detects upstream O2 slow/lazy response via perception flag (truth-vs-perception — gas analyser lambda_chem is near-stoichiometric ground truth but OBD lambda perception is biased high or low), and ERR-SF-002 detects upstream O2 fixed voltage / dead sensor via O2 circuit DTCs.

The 4 orphan KG nodes (ERR-SF-003 through ERR-SF-006) are unreachable because they exist in the knowledge graph but have no registry entries in `global_fault_registry.json`. REGISTRY_AUDIT.md §5 flags these as "12 orphan KG nodes (21%)" — the sensor_fault family accounts for 4 of the 12. The v2 rules must reactivate all 4 as evidence-tier rules with proper chemistry and OBD evidence.

The CHEMISTRY_COVERAGE.md matrix shows sensor_fault's chemistry footprint is NORMAL_OPERATION (~4 cases, O2 perception faults) and TIMING_RETARDED (~8 cases, MAF/MAP sensor drift). TIMING_RETARDED has zero v1 rules — it is a Tier B gap. The v2 rules must accept TIMING_RETARDED as SUGGESTIVE evidence for sensor faults where timing is retarded as a secondary symptom (MAF under-reading causes lean mixture → ECU retards timing; MAP drift causes incorrect load calculation → timing adaptation).

O2_SENSOR_BIASED_LOW and O2_SENSOR_BIASED_HIGH are defined in the schema's ChemistryState enum (Tier D chemistry states) but have no v1 rules. The v2 perception-flag rules for O2 sensor faults should reference these chemistry states as SUGGESTIVE evidence where the case data supports it.

The truth-vs-perception pattern (Brettschneider lambda is ground truth, ECU is perception) is the architectural differentiator for sensor_fault rules — the gas analyser says "chemistry is normal" while the ECU says "something is wrong." This is the only fault family where the perception_flag field is the primary diagnostic signal.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/sensor_fault.json` — CREATE: RuleSet JSON with 6 rules for sensor_fault family. Minimum rules:
   - SF-001: Upstream O2 sensor slow/lazy response — biased high (NORMAL_OPERATION DEFINITIVE + O2_SENSOR_BIASED_HIGH SUGGESTIVE + o2_voltage OBD SUGGESTIVE + perception_flag="O2_SENSOR_BIASED_HIGH"). Gas analyser lambda_chem is near-stoichiometric ground truth but OBD lambda perception is biased high (sensor reads falsely lean → ECU over-fuels). No circuit DTC — sensor still switches, just too slowly. v1 ERR-SF-001 perception_flag path, v2 evidence-tier form.
   - SF-002: Upstream O2 sensor slow/lazy response — biased low (NORMAL_OPERATION DEFINITIVE + O2_SENSOR_BIASED_LOW SUGGESTIVE + o2_voltage OBD SUGGESTIVE + perception_flag="O2_SENSOR_BIASED_LOW"). Gas analyser lambda_chem is near-stoichiometric ground truth but OBD lambda perception is biased low (sensor reads falsely rich → ECU under-fuels). v1 ERR-SF-001 second perception-flag variant.
   - SF-003: Upstream O2 sensor fixed voltage / dead element (NORMAL_OPERATION DEFINITIVE + P0131/P0132/P0134 DTC SUGGESTIVE + o2_voltage OBD GATING). Sensor output is pegged (stuck rich > 0.7V or stuck lean < 0.2V) with no switching. Circuit DTC confirms electrical failure. v1 ERR-SF-002, v2 evidence-tier form.
   - SF-004: MAF sensor under-reading (TIMING_RETARDED SUGGESTIVE + maf OBD SUGGESTIVE + perception_flag="MAF_UNDER_READING"). MAF reads low → ECU under-fuels → lean mixture → ECU retards timing as secondary adaptation. May or may not carry P0171 lean DTC. v1 orphan ERR-SF-003 reactivated.
   - SF-005: MAP sensor calibration drift (TIMING_RETARDED SUGGESTIVE + map OBD SUGGESTIVE + perception_flag="MAP_DRIFT"). MAP reads incorrect absolute pressure → ECU calculates wrong load → timing and fuel adapt. v1 orphan ERR-SF-004 reactivated.
   - SF-006: ECT sensor stuck cold (ect OBD SUGGESTIVE + TIMING_RETARDED SUGGESTIVE). Coolant temp sensor reads stuck cold → ECU enriches mixture permanently → fuel trim adapts → timing may retard. Also covers downstream O2 sensor contamination (o2_downstream OBD SUGGESTIVE) when the primary signal is a sensor fault rather than a catalyst or exhaust leak. v1 orphans ERR-SF-005 and ERR-SF-006 merged into one OBD-driven rule (the two share the "stuck/wrong sensor reading" pattern and both are OBD-primary rather than chemistry-primary).
2. `registry/tests/test_sensor_fault_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (NORMAL_OPERATION DEFINITIVE presence in O2 perception rules, TIMING_RETARDED SUGGESTIVE presence in MAF/MAP rules, perception_flag presence, OBD PID coverage per sensor type, DTC evidence for fixed-voltage O2, competition group integrity, no solo survivor), following the pattern in `test_exhaust_leak_rules.py`.

### Files to touch ###

- `registry/rules/sensor_fault.json` (CREATE)
- `registry/tests/test_sensor_fault_rules.py` (CREATE)

### Out of scope ###

- Other fault families (ecu_fault, cam_timing, mechanical_wear, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 registry's ERR-SF-003 through ERR-SF-006 orphan state — the v1 registry is frozen; v2 replaces it at cutover
- lean_condition family rules that compete with sensor_fault for MAF/MAP drift cases — the competition between sensor_fault and lean_condition for MAF-under-reading cases is resolved by the perception_flag (sensor_fault rules are perception-primary; lean_condition rules are chemistry-primary)
- catalyst_failure family rules that compete with sensor_fault for downstream O2 contamination cases — competition between sensor_fault and catalyst_failure for downstream O2 signal anomalies is resolved by chemistry (catalyst_failure expects CATALYST_OVERWHELMED; sensor_fault expects NORMAL_OPERATION)
- ECT sensor, MAF sensor, or MAP sensor DTC-driven rules (P0115, P0101, P0105 etc.) — DTC-only sensor fault detection belongs to ecu_fault; sensor_fault rules use OBD PIDs and chemistry as primary evidence
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_sensor_fault_rules.py --fix
pyright registry/tests/test_sensor_fault_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q
pytest registry/tests/test_exhaust_leak_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/sensor_fault.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/sensor_fault.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/sensor_fault.json').read_text())
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

# Targeted tests
pytest registry/tests/test_sensor_fault_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-sensor_fault`: Status=done, Files changed=2, Verification="{HEADLINE}"
