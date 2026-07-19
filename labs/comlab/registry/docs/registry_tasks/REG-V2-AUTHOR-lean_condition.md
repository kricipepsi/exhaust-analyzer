### Goal ###

Author the first v2 registry rule file at `registry/rules/lean_condition.json` containing at least 3 competing rules for the `lean_condition` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. This task is the first REG-V2-AUTHOR-{family} session and establishes the authoring pattern all subsequent families will follow. The SCHEMA_V2_SPEC.md §7 worked examples (LC-001, LC-002) provide the template; this task produces the real file with real `passes_cases` entries drawn from `corpus_curated.csv`.

### Success criteria ###

- `registry/rules/lean_condition.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- At least 3 rules with unique `rule_id` values in the file (no solo survivor)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `lean_condition`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- `TIMING_RETARDED` chemistry appears as SUGGESTIVE evidence in at least one rule (closing the #1 v1 coverage gap)
- `LEAN_MIXTURE` chemistry appears as DEFINITIVE evidence in at least one rule
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py` continue to pass (23 tests)
- New test `registry/tests/test_lean_condition_rules.py::test_ruleset_validates` passes

### Context ###

lean_condition is the largest fault family in the curated corpus (53 cases). The v1 registry has 4 active rules (ERR-LC-001, ERR-LC-003, ERR-LC-004x2) all gated on LEAN_MIXTURE or LEAN_MISFIRE chemistry. The #1 v2 gap per CHEMISTRY_COVERAGE.md §3.2 is TIMING_RETARDED — ~15 lean_condition cases produce this chemistry but zero v1 rules accept it. The v2 evidence-tier model fixes this: TIMING_RETARDED becomes SUGGESTIVE evidence (consistent with lean_condition as a secondary knock-avoidance timing pull, but not diagnostic alone since it also appears in catalyst_failure, sensor_fault, cam_timing, and ecu_fault). The SCHEMA_V2_SPEC.md §7 worked examples (LC-001 classic air leak, LC-002 vacuum leak with trim correction) are the starting point. This task also covers the orphan v1 KG nodes ERR-LC-002 (MAF contamination), ERR-LC-005 (EGR stuck open), ERR-LC-006 (exhaust leak pre-upstream O2) by authoring rules that detect those specific lean-condition sub-types where the curated corpus provides distinct chemistry/OBD/DTC signatures.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/` — CREATE directory
2. `registry/rules/lean_condition.json` — CREATE: RuleSet JSON with >= 3 rules for lean_condition family. Minimum rules:
   - LC-001: Classic air leak (LEAN_MIXTURE DEFINITIVE + positive fuel trims SUGGESTIVE + P0171/P0174 DTC SUGGESTIVE)
   - LC-002: TIMING_RETARDED-aware lean detection (LEAN_MIXTURE DEFINITIVE + TIMING_RETARDED SUGGESTIVE, closes the #1 v1 gap)
   - LC-003: MAF contamination / under-reading lean (LEAN_MIXTURE DEFINITIVE + low MAF + negative trims or trims near zero despite lean chemistry — the ERR-LC-002 orphan reactivated)
3. `registry/tests/test_lean_condition_rules.py` — CREATE: targeted tests that load and validate the rule file

### Files to touch ###

- `registry/rules/` (CREATE directory)
- `registry/rules/lean_condition.json` (CREATE)
- `registry/tests/test_lean_condition_rules.py` (CREATE)

### Out of scope ###

- Other fault families (rich_mixture, misfire, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- OBD-driven families (vacuum_leak, overheating, charging_system) — different evidence profile, later in the queue
- The `INCOMPLETE_OXIDATION` / EGR-specific lean path (v1 ERR-E1-M032) — this is a narrow edge case; capture as a follow-up if the corpus has cases for it
- Integration shim or harness side-by-side — those belong to REG-V2-INTEGRATE
- Any Python evaluation logic — rules are JSON data; the schema is the only Python changed in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_lean_condition_rules.py --fix
pyright registry/tests/test_lean_condition_rules.py
pytest registry/tests/test_schema_v2.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/lean_condition.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/lean_condition.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/lean_condition.json').read_text())
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
pytest registry/tests/test_lean_condition_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-lean_condition`: Status=done, Files changed=3, Verification="{HEADLINE}"
