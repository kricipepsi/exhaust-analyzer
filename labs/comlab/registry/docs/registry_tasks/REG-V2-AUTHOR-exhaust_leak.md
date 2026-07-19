### Goal ###

Author the v2 registry rule file at `registry/rules/exhaust_leak.json` containing 3 competing rules for the `exhaust_leak` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 6 rules (ERR-EL-001..006) but only 5 curated cases — the v1 rules are essentially repetition of the same pattern (EXHAUST_AIR_LEAK + LTFT at different thresholds) plus one false-positive-prone NORMAL_OPERATION rule (ERR-EL-004). The v2 rules must collapse the redundant LTFT-threshold variants into one rule, drop the NORMAL_OPERATION false-positive path, and add a post-cat exhaust-leak rule covering the P2096 DTC path (downstream O2 lean signal). 3 rules, each targeting a distinct anatomical leak site.

### Success criteria ###

- `registry/rules/exhaust_leak.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 3 rules with unique `rule_id` values (collapsing v1's 6 redundant variants)
- Every rule has `passes_cases` with at least one curated case ID that resolves to an `exhaust_leak`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- `EXHAUST_AIR_LEAK` chemistry appears as DEFINITIVE evidence in at least 2 of the 3 rules (the primary exhaust-leak signature)
- At least one rule uses LTFT OBD evidence (pre-cat leak: O2 sees lean → ECU adds fuel)
- At least one rule uses P2096/P2098 DTC evidence (post-cat leak: downstream O2 lean signal)
- At least one rule uses HC OBD evidence (manifold/header leak: false air dilutes sample at probe)
- No rule uses NORMAL_OPERATION chemistry (ERR-EL-004 false-positive path removed)
- No solo survivor: at least 2 rules in the `exhaust_leak` competition group, and any rule that could fire alone carries a `confidence_ceiling`
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py` continue to pass
- New test `registry/tests/test_exhaust_leak_rules.py::test_ruleset_validates` passes

### Context ###

exhaust_leak has 5 curated cases covering three distinct leak sites: (1) pre-cat exhaust leak at manifold/header flange — false air enters before the upstream O2 sensor, O2 reads lean, ECU compensates with positive LTFT, chemistry shows EXHAUST_AIR_LEAK + elevated O2 with P0171 lean DTC (CSV-095, TC-048, YAML-CSV95); (2) post-cat exhaust leak between upstream and downstream O2 sensors — downstream sensor reads lean, P2096/P2098 "Post Catalyst Fuel Trim System Too Lean" DTC sets, cat efficiency diagnosis is confounded (case_045); (3) exhaust leak at or near the probe tip — HC elevated at idle from false air dilution, O2 elevated, with or without DTCs (PDF-HI-007).

The v1 exhaust_leak rules are the most redundant in the registry: ERR-EL-001 (LTFT ≥10%, wt 0.80), ERR-EL-002 (LTFT ≥8%, wt 0.75), ERR-EL-003 (LTFT ≥5%, wt 0.70), and ERR-EL-005 (LTFT ≥5%, wt 0.75, different DTC strategy) are four variants of the same pre-cat leak pattern differentiated only by LTFT threshold — a single v2 rule with an evidence-tier LTFT block replaces all four. ERR-EL-004 (NORMAL_OPERATION, GAS_ONLY, wt 0.55) fires on healthy baselines — the REGISTRY_AUDIT.md explicitly flags it as a false-positive risk. ERR-EL-006 (EXHAUST_AIR_LEAK, GAS_ONLY, wt 0.60) is chemistry-only with no OBD evidence — too weak to compete alone.

The v2 rules must cover three anatomically distinct leak sites (pre-cat, post-cat, probe-tip) with non-overlapping evidence profiles so they compete sensibly within the exhaust_leak group and against other families (lean_condition shares the LTFT-elevation signal; catalyst_failure shares the post-cat O2 signal).

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/exhaust_leak.json` — CREATE: RuleSet JSON with 3 rules for exhaust_leak family. Minimum rules:
   - EL-001: Pre-cat exhaust leak (EXHAUST_AIR_LEAK DEFINITIVE + longft1 ≥ 8.0% OBD SUGGESTIVE + P0171/P0174 DTC SUGGESTIVE) — false air enters before upstream O2, O2 reads lean, ECU adds fuel, chemistry confirms air dilution. Collapses v1's four LTFT-threshold variants (ERR-EL-001/002/003/005) into one evidence-accumulation rule. Covers CSV-095, TC-048, YAML-CSV95.
   - EL-002: Post-cat exhaust leak (EXHAUST_AIR_LEAK DEFINITIVE + P2096/P2098 DTC SUGGESTIVE + o2_downstream OBD SUGGESTIVE) — leak between upstream and downstream O2 sensors; downstream O2 sees lean, confounds cat efficiency diagnosis. Covers case_045.
   - EL-003: Probe-tip / manifold leak (EXHAUST_AIR_LEAK DEFINITIVE + HC elevated OBD SUGGESTIVE + O2 elevated OBD SUGGESTIVE) — false air dilutes sample at probe or header flange; HC and O2 both read high from dilution. No DTC required. Covers PDF-HI-007.
2. `registry/tests/test_exhaust_leak_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (EXHAUST_AIR_LEAK DEFINITIVE presence, LTFT OBD evidence, P2096 DTC path, HC/O2 OBD evidence, no NORMAL_OPERATION chemistry in any rule, competition group integrity), following the pattern in `test_catalyst_failure_rules.py`.

### Files to touch ###

- `registry/rules/exhaust_leak.json` (CREATE)
- `registry/tests/test_exhaust_leak_rules.py` (CREATE)

### Out of scope ###

- Other fault families (sensor_fault, ecu_fault, cam_timing, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 ERR-EL-004 false-positive behavior in COMLab — the v1 registry is frozen; v2 replaces it at cutover
- lean_condition family rules that also use LTFT elevation as a signal — the competition between exhaust_leak and lean_condition for LTFT-elevated cases is resolved by chemistry (EXHAUST_AIR_LEAK vs LEAN_MIXTURE), not by rule authoring
- catalyst_failure family rules that use post-cat O2 evidence — competition between exhaust_leak and catalyst_failure for P2096 cases is resolved by chemistry (EXHAUST_AIR_LEAK vs CATALYST_OVERWHELMED)
- NORMAL_OPERATION exhaust_leak path from v1 (ERR-EL-004) — this path is intentionally removed in v2 as a documented false-positive risk
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_exhaust_leak_rules.py --fix
pyright registry/tests/test_exhaust_leak_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/exhaust_leak.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/exhaust_leak.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/exhaust_leak.json').read_text())
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
pytest registry/tests/test_exhaust_leak_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-exhaust_leak`: Status=done, Files changed=2, Verification="{HEADLINE}"
