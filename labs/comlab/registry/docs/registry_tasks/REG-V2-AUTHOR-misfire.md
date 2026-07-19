### Goal ###

Author the v2 registry rule file at `registry/rules/misfire.json` containing at least 5 competing rules for the `misfire` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 10 rules for this family (ERR-MF-002..007 across IGNITION_MISFIRE, LEAN_MISFIRE, RICH_MISFIRE + 3 ERR-IF-* rules also gated on IGNITION_MISFIRE + ERR-E2-I104) — but 30 of 44 curated misfire cases are DTCLab-enum-crashed (will recover post FIX-ENUM-1) and the remaining 14 route to wrong families or no_fault. The v2 rules must add TIMING_RETARDED awareness (~8 cases), SAMPLE_INVALID gating (~10 cases), CYLINDER_FLUID_MISFIRE DTC evidence (the new enum from FIX-ENUM-1), ghost-misfire detection (NORMAL_OPERATION chemistry + MISFIRE_HISTORY DTC = ECU hallucination), and ECU-blindness perception-gap rules (gas-evident misfire with MISFIRE_HISTORY strategy=none_present).

### Success criteria ###

- `registry/rules/misfire.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- At least 5 rules with unique `rule_id` values in the file (no solo survivor)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `misfire`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- `IGNITION_MISFIRE` chemistry appears as DEFINITIVE evidence in at least one rule (collapses v1's 5 IGNITION_MISFIRE-gated rules)
- `LEAN_MISFIRE` chemistry appears as DEFINITIVE evidence in at least one rule
- `RICH_MISFIRE` chemistry appears as DEFINITIVE evidence in at least one rule
- `NORMAL_OPERATION` chemistry appears as DEFINITIVE evidence in at least one rule (ghost-misfire pattern: clean chemistry + P0300 hallucination)
- `SAMPLE_INVALID` chemistry appears as GATING evidence in at least one rule (closing the SAMPLE_INVALID gap for ~10 misfire cases)
- `TIMING_RETARDED` chemistry appears as SUGGESTIVE evidence in at least one rule (closing the TIMING_RETARDED gap for ~8 misfire cases)
- At least one rule uses `MISFIRE_HISTORY` DTC evidence (P0300-P0312) — the core misfire DTC family
- At least one rule uses `CYLINDER_FLUID_MISFIRE` DTC routing tag evidence (coolant-in-cylinder misfire path from FIX-ENUM-1)
- At least one rule uses `MISFIRE_HISTORY` with strategy `none_present` (ECU-blindness perception gap: gas shows misfire, ECU counter=0)
- At least one rule carries a `perception_flag` (truth-vs-perception: gas chemistry is ground truth, ECU misfire counter is perception)
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py` continue to pass
- New test `registry/tests/test_misfire_rules.py::test_ruleset_validates` passes

### Context ###

misfire is the second-largest family with 44 curated cases covering five distinct sub-patterns: (1) physical ignition misfire from failed coils/plugs/wires (CSV-101..104, EXT-234..236) — the v1 IGNITION_MISFIRE + shrtft1 path; (2) lean-induced misfire from vacuum leaks (EXP-N021, PDF-HI-002) — LEAN_MISFIRE chemistry; (3) rich/mechanical misfire from injector or compression issues (PDF-4G-02, PDF-4G-05) — RICH_MISFIRE chemistry; (4) ghost misfire where ECU hallucinates P0300 despite pristine combustion (CSV-066, CSV-107, CSV-108, ECU-007, EXP-N016, EXT-225, EXT-226, EXT-228) — NORMAL_OPERATION chemistry + electrical-noise-induced false CKP detection; (5) ECU blindness where gas chemistry clearly shows misfire but ECU misfire counter=0 (CSV-052, CSV-105, CSV-106, ECU-008, EXT-237) — IGNITION_MISFIRE chemistry + zero ECU misfire counts = perception gap. The #1 gap per CHEMISTRY_COVERAGE.md §4.1 is that 30 of 44 cases crash at DTCLab validation (CYLINDER_FLUID_MISFIRE enum gap — will auto-recover post FIX-ENUM-1). The #2 gap is SAMPLE_INVALID (~10 cases) with no v1 misfire rule accepting it. The #3 gap is TIMING_RETARDED (~8 cases) — knock-avoidance timing pull produces misfire-like signatures that v1's chemistry-gated prune eliminates. ERR-MF-001 (coil_on_plug_insulation_arc) — the most common real-world misfire KG node — is an orphan in v1 with no registry entry. The v2 rules must cover all five sub-patterns and close all three gaps.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/misfire.json` — CREATE: RuleSet JSON with >= 5 rules for misfire family. Minimum rules:
   - MF-001: Classic ignition misfire (IGNITION_MISFIRE DEFINITIVE + MISFIRE_HISTORY DTC SUGGESTIVE + high HC/O2 OBD evidence) — collapses v1's 5 IGNITION_MISFIRE-gated rules (ERR-MF-002/004/006, ERR-E2-I104, ERR-IF-003) into one evidence-accumulation model
   - MF-002: Lean misfire (LEAN_MISFIRE DEFINITIVE + LEAN_HISTORY DTC SUGGESTIVE + CYLINDER_FLUID_MISFIRE DTC SUGGESTIVE) — for vacuum-leak-induced misfire with coolant-in-cylinder evidence; carries forward v1 ERR-MF-003/005/007 + ERR-LC-004 LEAN_MISFIRE path
   - MF-003: Rich misfire (RICH_MISFIRE DEFINITIVE + RICH_HISTORY DTC SUGGESTIVE + negative longft1 OBD evidence) — carries forward v1 ERR-MF-002 RICH_MISFIRE path
   - MF-004: Ghost misfire (NORMAL_OPERATION DEFINITIVE + MISFIRE_HISTORY DTC SUGGESTIVE + perception_flag) — ECU hallucination pattern: clean combustion chemistry + P0300 triggered by electrical noise, loose ground, or flywheel play. Low base_weight with confidence_ceiling
   - MF-005: ECU blindness perception gap (IGNITION_MISFIRE DEFINITIVE + MISFIRE_HISTORY DTC none_present SUGGESTIVE + perception_flag) — gas chemistry ground-truth shows misfire but ECU counter=0; Brettschneider override
   - MF-006: SAMPLE_INVALID + TIMING_RETARDED gating (SAMPLE_INVALID GATING + IGNITION_MISFIRE DEFINITIVE + TIMING_RETARDED SUGGESTIVE) — closes both Tier B chemistry gaps for misfire cases; fires when sample quality is marginal AND gas signature is ignition-misfire-like with knock-avoidance timing pull
2. `registry/tests/test_misfire_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (IGNITION_MISFIRE DEFINITIVE, LEAN_MISFIRE DEFINITIVE, RICH_MISFIRE DEFINITIVE, NORMAL_OPERATION DEFINITIVE, SAMPLE_INVALID GATING, TIMING_RETARDED SUGGESTIVE, MISFIRE_HISTORY DTC, CYLINDER_FLUID_MISFIRE DTC, MISFIRE_HISTORY none_present strategy, perception_flag presence), following the pattern in `test_lean_condition_rules.py` and `test_rich_mixture_rules.py`

### Files to touch ###

- `registry/rules/misfire.json` (CREATE)
- `registry/tests/test_misfire_rules.py` (CREATE)

### Out of scope ###

- Other fault families (catalyst_failure, sensor_fault, ecu_fault, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing DTCLab enum crash (FIX-ENUM-1) — that is a paused Tier 1 schema fix, not a registry task. v2 rules reference CYLINDER_FLUID_MISFIRE as a DTC routing tag that already exists in the schema_v2 vocabulary
- IGNITION_FAULT family cases (3 cases, gated on IGNITION_MISFIRE + REQUIRE_MATCH DTC) — those belong to REG-V2-AUTHOR-ignition_fault, not this task
- CAM_TIMING family cases that share IGNITION_MISFIRE chemistry (ERR-CT-002) — those belong to REG-V2-AUTHOR-cam_timing
- GDI-specific misfire sub-patterns (CASE-033, CASE-038) beyond what LEAN_MISFIRE + CYLINDER_FLUID_MISFIRE covers — GDI_INTAKE_VALVE_CARBON is a Tier D chemistry state with no corpus evidence; schema slot exists, rule deferred
- Cold-start misfire cases (CASE-021, EXT-225) that differ only in ECT precondition — these should be covered by MF-001 with the ECT OBD evidence; do not create a separate cold-start-only rule
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_misfire_rules.py --fix
pyright registry/tests/test_misfire_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/misfire.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/misfire.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/misfire.json').read_text())
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
pytest registry/tests/test_misfire_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-misfire`: Status=done, Files changed=2, Verification="{HEADLINE}"
