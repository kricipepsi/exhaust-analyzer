### Goal ###

Author the v2 registry rule file at `registry/rules/catalyst_failure.json` containing at least 5 competing rules for the `catalyst_failure` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 7 KG nodes (ERR-CF-001..007) spanning CATALYST_OVERWHELMED, CATALYST_NOT_LIGHTING_OFF, NORMAL_OPERATION, and POA_SIGNATURE chemistry states — but the hard-gate architecture means CATALYST_OVERWHELMED is a late-stage signature that misses marginal degradation, the ~10 TIMING_RETARDED cases have zero rules, catalyst-masking patterns (clean tailpipe + elevated OBD trims hiding upstream problems) are unaddressed, flow-restriction patterns (CO2 collapse at 2500 RPM) are under-served, and perception-gap cases (OBD λ biased vs chemistry λ truth) have no explicit Brettschneider-override rules. The v2 rules must close all three gaps (TIMING_RETARDED, marginal catalyst, masking/perception), use CATALYST_HISTORY DTC evidence (P0420/P0430), and provide at least one rule with a `perception_flag` for OBD-λ-contradiction cases.

### Success criteria ###

- `registry/rules/catalyst_failure.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- At least 5 rules with unique `rule_id` values in the file (no solo survivor)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `catalyst_failure`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- `CATALYST_OVERWHELMED` chemistry appears as DEFINITIVE evidence in at least one rule (classic dead/overwhelmed catalyst fingerprint)
- `CATALYST_NOT_LIGHTING_OFF` chemistry appears as DEFINITIVE evidence in at least one rule (cold catalyst / heater failure)
- `NORMAL_OPERATION` chemistry appears as DEFINITIVE evidence in at least one rule (catalyst masking: cat cleans tailpipe while hiding upstream problems)
- `TIMING_RETARDED` chemistry appears as SUGGESTIVE evidence in at least one rule (closing the Tier B gap for ~10 catalyst_failure cases per CHEMISTRY_COVERAGE.md §3.2)
- At least one rule uses `CATALYST_HISTORY` DTC evidence (P0420, P0430)
- At least one rule carries a `perception_flag` (truth-vs-perception: chemistry λ is ground truth, OBD λ is perception — per PRD_4D_App.md §5 Brettschneider override)
- At least one rule uses OBD evidence for exhaust flow restriction (CO2 depression + O2 elevation at load, captured via OBD PIDs or chemistry delta between idle and high-idle)
- At least one rule covers the catalyst-masking sub-pattern: NORMAL_OPERATION chemistry + elevated LTFT (≥10%) OBD evidence + clean tailpipe
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py` continue to pass
- New test `registry/tests/test_catalyst_failure_rules.py::test_ruleset_validates` passes

### Context ###

catalyst_failure has 21 curated cases covering six distinct sub-patterns: (1) dead/overwhelmed catalyst with CATALYST_OVERWHELMED chemistry — high NOx breakthrough, P0420 set, post-cat gases show failed reduction (REAL-005, PDF-4G-01, case_010, case_034); (2) marginal/degraded catalyst where HC rises under load (CASE-016: HC 180→380 at 2500 RPM, cat no longer oxidizing); (3) catalyst masking where the cat cleans tailpipe gases perfectly (NORMAL_OPERATION) but OBD trims (LTFT ≥10%) reveal upstream mechanical wear or oil burn that the cat is compensating for (CSV-121, CSV-122, EXP-N008, EXT-232, EXT-233, CASE-015); (4) physical flow restriction from melted/collapsed substrate — CO2 drops at 2500 RPM, O2 rises, backpressure pumping loss, often with P0420 (EXT-207, EXT-208, EXT-213, CASE-013, EXP-N012); (5) cold catalyst / not lighting off from heater circuit failure or low ECT (CASE-026); (6) perception-gap cases where OBD λ is zero or significantly biased while chemistry λ is near stoich — ECU sees richer than reality, perception-contradiction symptom (PDF-HI-006, YAML-PDF_HI_006, YAML-PDF_4G_01, REAL-005).

The #1 coverage gap per CHEMISTRY_COVERAGE.md §3.2 is TIMING_RETARDED (~10 catalyst_failure cases produce this chemistry) — zero v1 rules accept it. The #2 gap is marginal-catalyst detection: v1's CATALYST_OVERWHELMED gate requires severe chemistry (NOx>500, CO2<13%), missing early-stage degradation where the cat is failing but hasn't fully collapsed. The #3 gap is catalyst masking: v1 has no rule for "cat is working so well it's hiding the real problem" — the NORMAL_OPERATION chemistry path in v1 routes to exhaust_leak and sensor_fault, not catalyst_failure. The #4 gap is perception: v1 has no explicit Brettschneider-override rule for cases where OBD λ contradicts chemistry λ.

ERR-CF-001 through ERR-CF-004 (CATALYST_OVERWHELMED) are the most heavily registered v1 rules; ERR-CF-005 (NORMAL_OPERATION) is the only v1 catalyst rule that doesn't require visible gas failure; ERR-CF-006 (POA_SIGNATURE, weight 0.55) handles a narrow cross-family path; ERR-CF-007 (CATALYST_NOT_LIGHTING_OFF) has one rule at low weight. The v2 rules must broaden chemistry acceptance (especially TIMING_RETARDED), add catalyst-masking evidence paths, cover flow restriction, and add perception-flag rules for OBD-λ-contradiction cases.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/catalyst_failure.json` — CREATE: RuleSet JSON with >= 5 rules for catalyst_failure family. Minimum rules:
   - CF-001: Dead/overwhelmed catalyst (CATALYST_OVERWHELMED DEFINITIVE + CATALYST_HISTORY DTC SUGGESTIVE + elevated NOx + low CO2 OBD evidence) — classic post-cat failure fingerprint. Collapses v1's four CATALYST_OVERWHELMED-gated rules (ERR-CF-001..004) into one evidence-accumulation model. Covers REAL-005, PDF-4G-01, case_010, case_034.
   - CF-002: Catalyst masking — clean tailpipe hiding upstream problems (NORMAL_OPERATION DEFINITIVE + LTFT ≥ 10% OBD SUGGESTIVE + perception_flag) — cat is doing its job so well that post-cat gases are pristine, but OBD fuel trims betray upstream mechanical wear or oil burn. Covers CSV-121, CSV-122, EXP-N008, EXT-232, EXT-233, CASE-015.
   - CF-003: Flow restriction — physical exhaust blockage (CATALYST_OVERWHELMED DEFINITIVE + CO2 ≤ 10.0% OBD SUGGESTIVE at high-idle + O2 ≥ 4.0% OBD SUGGESTIVE at high-idle) — melted/collapsed substrate causes backpressure: CO2 collapses under load, O2 rises as exhaust backs up. Covers EXT-207, EXT-208, EXT-213, CASE-013, EXP-N012.
   - CF-004: Cold catalyst / not lighting off (CATALYST_NOT_LIGHTING_OFF DEFINITIVE + CATALYST_HISTORY DTC SUGGESTIVE + ECT OBD SUGGESTIVE) — cat below light-off temp, heater circuit failure or low ECT. Covers CASE-026, PDF-HI-006.
   - CF-005: TIMING_RETARDED-aware marginal catalyst (TIMING_RETARDED SUGGESTIVE + CATALYST_OVERWHELMED SUGGESTIVE + CATALYST_HISTORY DTC SUGGESTIVE + NOx OBD evidence) — closes the Tier B chemistry gap for ~10 catalyst_failure cases that produce TIMING_RETARDED but should route to catalyst_failure. Knock-avoidance timing pull masks the catalyst signature; this rule accepts TIMING_RETARDED as suggestive rather than gating hard on CATALYST_OVERWHELMED.
   - CF-006: Perception-gap catalyst failure (CATALYST_OVERWHELMED DEFINITIVE + OBD λ = 0 or significantly biased OBD SUGGESTIVE + perception_flag) — Brettschneider override: chemistry says cat is overwhelmed, but OBD λ reads zero or significantly biased (ECU O2 sensor perception failure). Covers PDF-HI-006, YAML-PDF_HI_006, YAML-PDF_4G_01, REAL-005 (perception-gap subset).
   - CF-007: Marginal HC breakthrough (CATALYST_OVERWHELMED SUGGESTIVE + HC elevated at 2500 RPM OBD SUGGESTIVE + CATALYST_HISTORY DTC SUGGESTIVE) — early-stage cat degradation where HC rises under load but cat hasn't fully collapsed. Covers CASE-016, case_024 (freeze-frame cat evidence with clean idle).
2. `registry/tests/test_catalyst_failure_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (CATALYST_OVERWHELMED DEFINITIVE, CATALYST_NOT_LIGHTING_OFF DEFINITIVE, NORMAL_OPERATION DEFINITIVE, TIMING_RETARDED SUGGESTIVE, CATALYST_HISTORY DTC, perception_flag presence, OBD flow-restriction evidence, LTFT masking evidence), following the pattern in `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, and `test_misfire_rules.py`.

### Files to touch ###

- `registry/rules/catalyst_failure.json` (CREATE)
- `registry/tests/test_catalyst_failure_rules.py` (CREATE)

### Out of scope ###

- Other fault families (sensor_fault, ecu_fault, exhaust_leak, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing DTCLab enum crash (FIX-ENUM-1) or any paused Tier 1 schema fix — those re-enter the queue after v2 cutover
- rich_mixture family cases where P0420 is a masking DTC (e.g., case_023 — rich feed gas overwhelming cat, not cat failing) — those belong to REG-V2-AUTHOR-rich_mixture
- exhaust_leak family rules (ERR-EL-004 NORMAL_OPERATION cross-family path) — those belong to REG-V2-AUTHOR-exhaust_leak
- sensor_fault family rules (ERR-SF-001 perception_flag O2 path) — those belong to REG-V2-AUTHOR-sensor_fault
- POA_SIGNATURE chemistry (ERR-CF-006) as a standalone rule — POA_SIGNATURE is cross-family (rich_mixture + catalyst_failure); the catalyst_failure POA path is folded into CF-001's CATALYST_OVERWHELMED evidence rather than requiring a separate rule
- ECT-based thermal precondition rules — if cold engine prevents catalyst evaluation, that's a router-level concern (REG-V2-INTEGRATE), not a per-rule authoring task
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_catalyst_failure_rules.py --fix
pyright registry/tests/test_catalyst_failure_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/catalyst_failure.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/catalyst_failure.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/catalyst_failure.json').read_text())
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
pytest registry/tests/test_catalyst_failure_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-catalyst_failure`: Status=done, Files changed=2, Verification="{HEADLINE}"
