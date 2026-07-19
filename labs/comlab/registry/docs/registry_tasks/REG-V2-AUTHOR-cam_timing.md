### Goal ###

Author the v2 registry rule file at `registry/rules/cam_timing.json` containing 6 competing rules for the `cam_timing` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 5 rules (ERR-CT-001 through ERR-CT-005) but 4 of 5 require the `vvt_equipped: true` precondition, leaving non-VVT engines with a single rule (ERR-CT-001, WRONG_VALVE_TIMING). The 9 cam_timing cases break into three clusters: mechanical base timing (1 case, no DTCs), VVT retard/phaser lag (5 cases, P0011), and VVT advance/phaser stuck (2 cases, P0012). The 1 remaining case is VVT solenoid electrical drift (no DTC). CHEMISTRY_COVERAGE.md §4.1 flags TIMING_RETARDED (~3 cases) as the chemistry gap for this family. 6 rules covering mechanical timing, VVT retard, VVT advance, ignition-misfire chemistry, VVT solenoid electrical, and TIMING_RETARDED chemistry.

### Success criteria ###

- `registry/rules/cam_timing.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 6 rules with unique `rule_id` values (CT-001 through CT-006)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `cam_timing`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 1 rule uses WRONG_VALVE_TIMING chemistry as GATING (CT-001 — mechanical base timing, non-VVT path)
- At least 2 rules use VVT_FAILURE chemistry as GATING (CT-002 retard, CT-003 advance)
- At least 1 rule uses IGNITION_MISFIRE chemistry as GATING (CT-004 — VVT phaser causing misfire-like emissions)
- At least 1 rule uses TIMING_RETARDED chemistry as SUGGESTIVE evidence (closes the ~3-case Tier B gap for cam_timing)
- At least 1 rule is DTC-primary with no chemistry requirement (CT-005 — VVT solenoid electrical, VVT_HISTORY DTCs as GATING)
- At least 1 rule has no `vvt_equipped` precondition (CT-001 — mechanical timing; v1 non-VVT gap closed)
- No solo survivor: the `cam_timing` competition group has ≥ 2 rules, and at least 2 rules carry `confidence_ceiling`
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py`, `test_exhaust_leak_rules.py`, `test_sensor_fault_rules.py`, `test_ecu_fault_rules.py` continue to pass
- New test `registry/tests/test_cam_timing_rules.py::test_ruleset_validates` passes

### Context ###

cam_timing has 9 curated cases. The v1 registry has 5 rules but 4 require `vvt_equipped: true`, leaving non-VVT engines with only ERR-CT-001 (WRONG_VALVE_TIMING with map_kpa < 30 kPa). REGISTRY_AUDIT.md §3.1 notes: "4 of 5 rules require vvt_equipped precondition. Non-VVT engines have 1 rule." CHEMISTRY_COVERAGE.md §4.1 grades cam_timing as MEDIUM severity with TIMING_RETARDED (~3 cases) as the primary chemistry gap.

The 9 cases break down into three clusters:

**Cluster A — Mechanical base timing (1 case):** MECH-004: retarded timing, HC/CO high, no DTCs. The physical cam timing is wrong (belt/chain off by a tooth) regardless of VVT. WRONG_VALVE_TIMING chemistry. No DTC expected — the ECU sees the timing error as a combustion problem, not a cam sensor problem. v1 rule ERR-CT-001 maps to this but adds an unnecessary map_kpa < 30 kPa constraint that may fail on this case.

**Cluster B — VVT retard / phaser lag (5 cases, P0011):** CSV-115 (retarded intake cam, HC up, CO2 down, NOx < 80 — LOW NOx is the key differentiator from lean_condition), CSV-116 (VVT phaser sluggish, late combustion, LOW NOx), EXT-209 (retarded cam at idle, HC=350, CO2 depressed, trims mildly negative, phaser catches up at 2500 RPM), CASE-018 (HC delta 250→850ppm at 2500RPM, spark advance fluctuating mid-load, CO2 drops under load), EXP-N007 (oil sludge restricts cam phaser, HC up + low CO2, P0011). All carry P0011 (Intake Camshaft Position Timing Over-Advanced Bank 1). The LOW NOx signature differentiates these from lean_condition (which shows HIGH NOx > 800ppm). VVT_FAILURE chemistry with TIMING_RETARDED as secondary evidence.

**Cluster C — VVT advance / phaser stuck (2 cases, P0012):** EXT-210 (over-advanced cam at idle, HC elevated, CO2 depressed, trims negative, cam returns to normal at 2500 RPM, cold rattle on start), case_042 (VVT phaser stuck advanced — knock and rich). Both carry P0012 (Intake Camshaft Position Timing Over-Retarded Bank 1). VVT_FAILURE chemistry; the advance vs retard distinction is DTC-driven.

**Solenoid electrical (1 case, no DTC, UNCOVERABLE):** EXP-N023: solenoid coil resistance drifted 8→40Ω, phaser sluggish, HC up at 2500 RPM. No DTC stored, stft=2.0, ltft=1.0 — trims near zero. No MAP or RPM data in the CSV row. This case is uncoverable with the current OBD PID set (solenoid resistance is not a captured PID). Documented as an Unplanned follow-up. CT-005 covers the VVT electrical pattern where a DTC IS present (e.g., EXP-N007 with P0011).

Cross-family competition: cam_timing competes with mechanical_wear (both see WRONG_VALVE_TIMING chemistry), lean_condition (VVT retard cases show lean-like HC/CO2 depression but differ on NOx — cam_timing: NOx < 80ppm; lean_condition: NOx > 800ppm), and misfire (IGNITION_MISFIRE chemistry from VVT phaser causing late combustion).

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/cam_timing.json` — CREATE: RuleSet JSON with 6 rules for cam_timing family. Minimum rules:
   - CT-001: Mechanical base timing error (WRONG_VALVE_TIMING). Chemistry-primary rule: WRONG_VALVE_TIMING as GATING evidence. No VVT precondition (non-VVT path — closes the v1 gap where only 1 rule worked without vvt_equipped). No DTC requirement — mechanical timing errors on non-VVT engines produce no cam sensor DTC. Covers MECH-004. v1 ERR-CT-001 reactivated, with the map_kpa constraint removed (the v1 constraint may not hold for all mechanical timing cases).
   - CT-002: VVT retard / phaser lag (VVT_FAILURE + P0011). Chemistry-primary rule: VVT_FAILURE as GATING evidence. P0011 DTC as SUGGESTIVE (VVT_HISTORY range). TIMING_RETARDED chemistry as SUGGESTIVE evidence (closes the ~3-case Tier B gap for cam_timing). OBD evidence: HC elevated at 2500 RPM relative to idle as SUGGESTIVE (phaser lag under load). Covers CSV-115, CSV-116, EXT-209, CASE-018, EXP-N007. v1 ERR-CT-003 reactivated, expanded with TIMING_RETARDED.
   - CT-003: VVT advance / phaser stuck (VVT_FAILURE + P0012). Chemistry-primary rule: VVT_FAILURE as GATING evidence. P0012 DTC as SUGGESTIVE (VVT_HISTORY range). Covers EXT-210, case_042. v1 ERR-CT-004 reactivated, with DTC evidence added (v1 was GAS_ONLY at 0.55 confidence with no DTC tie-in).
   - CT-004: IGNITION_MISFIRE with cam timing. Chemistry-primary rule: IGNITION_MISFIRE as GATING evidence. VVT DTCs (P0011, P0012) as SUGGESTIVE (VVT_HISTORY range). Covers VVT cases where the phaser problem produces misfire-like emissions (late combustion → incomplete burn → ignition-misfire chemistry). v1 ERR-CT-002 reactivated.
   - CT-005: VVT solenoid/actuator electrical fault. DTC-primary rule: VVT_HISTORY range DTCs (P0010-P0023) with strategy `any_match` as GATING evidence. No chemistry requirement — the electrical nature of the fault means chemistry may be NORMAL_OPERATION or ambiguous. OBD evidence: shrtft1 and longft1 near zero as SUGGESTIVE (solenoid drift causes marginal trim response, not the saturation pattern of ecu_fault). confidence_ceiling required (sole DTC-primary rule in the set). Covers EXP-N007 (P0011 confirmed — shared with CT-002; case appearing in two competing rules is valid, competition scoring resolves it). EXP-N023 is NOT covered — it has no DTC, no MAP, no RPM; this case is uncoverable with the current OBD PID set. Documented as an Unplanned follow-up.
   - CT-006: TIMING_RETARDED with cam timing (Tier B gap closer). Chemistry-aware rule: TIMING_RETARDED as SUGGESTIVE evidence. VVT DTCs (P0011, P0012, P0013, P0014, P0021, P0022, P0023, P0024) as GATING evidence with strategy `any_match`. Covers the ~3 cases where GASLab emits TIMING_RETARDED chemistry and cam timing DTCs are present — these are cases where the ECU detects the cam timing fault but the gas analyser sees only the secondary combustion effect. confidence_ceiling applied because TIMING_RETARDED chemistry is shared across 7 families and cam_timing is not the only consumer.
2. `registry/tests/test_cam_timing_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (WRONG_VALVE_TIMING chemistry gate in CT-001, VVT_FAILURE chemistry gate in CT-002/CT-003, IGNITION_MISFIRE chemistry gate in CT-004, VVT_HISTORY DTC evidence in CT-005, TIMING_RETARDED SUGGESTIVE evidence in CT-002/CT-006, non-VVT path in CT-001 — no vvt_equipped precondition, confidence_ceiling on CT-005/CT-006, competition group integrity, no solo survivor, all 9 case IDs resolve), following the pattern in `test_ecu_fault_rules.py`.

### Files to touch ###

- `registry/rules/cam_timing.json` (CREATE)
- `registry/tests/test_cam_timing_rules.py` (CREATE)

### Out of scope ###

- Other fault families (mechanical_wear, non_starter, vacuum_leak, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 registry's ERR-CT-001 through ERR-CT-005 — the v1 registry is frozen; v2 replaces it at cutover
- mechanical_wear family rules that compete with cam_timing for WRONG_VALVE_TIMING chemistry — competition between cam_timing and mechanical_wear is resolved by DTC presence (cam_timing: P0011/P0012/VVT codes present; mechanical_wear: no VVT codes, different chemistry signature)
- lean_condition family rules that compete with cam_timing for lean-like HC/CO2 signatures — competition resolved by NOx level (cam_timing: NOx < 80ppm; lean_condition: NOx > 800ppm) per the case descriptions
- misfire family rules that compete with cam_timing for IGNITION_MISFIRE chemistry — competition resolved by VVT DTC presence (cam_timing: P0011/P0012 present; misfire: P0300-P0304 present, no VVT codes)
- TIMING_OVER_ADVANCED chemistry — defined in schema but has zero Jaeger-confirmed cases; schema slot only, no rule authoring needed at this time
- FLAT_CAMSHAFT chemistry — defined in schema but zero confirmed cases; schema slot only
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_cam_timing_rules.py --fix
pyright registry/tests/test_cam_timing_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q
pytest registry/tests/test_exhaust_leak_rules.py -x -q
pytest registry/tests/test_sensor_fault_rules.py -x -q
pytest registry/tests/test_ecu_fault_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/cam_timing.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/cam_timing.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/cam_timing.json').read_text())
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
pytest registry/tests/test_cam_timing_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-cam_timing`: Status=done, Files changed=2, Verification="{HEADLINE}"
