### Goal ###

Author the v2 registry rule file at `registry/rules/rich_mixture.json` containing at least 3 competing rules for the `rich_mixture` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. This task follows the authoring pattern established by REG-V2-AUTHOR-lean_condition. The v1 registry has 7 rules for this family (ERR-RM-001..007) — the best-covered family — but they are all gated on RICH_MIXTURE or POA_SIGNATURE chemistry with only longft1 OBD thresholds. The v2 rules must add DTC evidence (P0172/P0175 via RICH_HISTORY), SAMPLE_INVALID gating awareness, and proper competition groups with catalyst_failure for POA_SIGNATURE cases.

### Success criteria ###

- `registry/rules/rich_mixture.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- At least 3 rules with unique `rule_id` values in the file (no solo survivor)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `rich_mixture`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- `RICH_MIXTURE` chemistry appears as DEFINITIVE evidence in at least one rule
- `POA_SIGNATURE` chemistry appears as SUGGESTIVE evidence in at least one rule (catalyst_failure competition group awareness)
- `SAMPLE_INVALID` chemistry appears as GATING evidence in at least one rule (closing the SAMPLE_INVALID gap for rich_mixture cases)
- At least one rule uses `RICH_HISTORY` DTC evidence (P0172/P0175) — v1 had zero DTC-aware rich rules
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py` and `registry/tests/test_lean_condition_rules.py` continue to pass
- New test `registry/tests/test_rich_mixture_rules.py::test_ruleset_validates` passes

### Context ###

rich_mixture is the best-covered family in v1 with 7 rules (ERR-RM-001..007) and 23 curated cases. The v1 rules are all chemistry-gated: 5 on RICH_MIXTURE with varying longft1 thresholds (≤ -10% through ≤ -23%), and 2 on POA_SIGNATURE (GAS_ONLY, no OBD or DTC evidence). The #1 gap per CHEMISTRY_COVERAGE.md §4.2 is that none of these rules use DTC evidence — P0172 (Bank 1 Too Rich) and P0175 (Bank 2 Too Rich) are among the most common DTCs and should contribute SUGGESTIVE evidence. The #2 gap is that SAMPLE_INVALID cases (~2 in rich_mixture) have no gating rule — the v1 prune drops them before evaluation. Additionally, the POA_SIGNATURE chemistry state is shared with catalyst_failure (ERR-CF-006 also gates on it), so v2 rich_mixture rules using POA_SIGNATURE must carry appropriate confidence ceilings and compete fairly with the catalyst_failure family. The GDI_HPFP_INTERNAL_SEAL_LEAK path exists in v1 (ERR-E3-F501) but is narrow — v2 should carry it forward as a SUGGESTIVE chemistry state with fuel-pressure OBD evidence for GDI-equipped cases.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/rich_mixture.json` — CREATE: RuleSet JSON with >= 3 rules for rich_mixture family. Minimum rules:
   - RM-001: Classic rich mixture (RICH_MIXTURE DEFINITIVE + negative longft1/shrft1 SUGGESTIVE + P0172/P0175 DTC SUGGESTIVE) — collapses v1's 5 RICH_MIXTURE + longft1-threshold rules into one evidence-accumulation model
   - RM-002: POA-aware rich detection (RICH_MIXTURE DEFINITIVE + POA_SIGNATURE SUGGESTIVE with confidence_ceiling) — for cases where a failing catalyst creates rich-appearing exhaust; competes with catalyst_family POA rules
   - RM-003: SAMPLE_INVALID gating for rich mixture (SAMPLE_INVALID GATING + RICH_MIXTURE DEFINITIVE) — ensures rich mixture can still fire when sample quality is marginal, closing the SAMPLE_INVALID gap
   - RM-004 (optional): GDI HPFP internal seal leak (GDI_HPFP_INTERNAL_SEAL_LEAK SUGGESTIVE + RICH_MIXTURE DEFINITIVE + fuel_pressure PID evidence + precondition `gdi_equipped: true`) — carries forward the v1 ERR-E3-F501 GDI path
2. `registry/tests/test_rich_mixture_rules.py` — CREATE: targeted tests that load and validate the rule file, following the pattern in `test_lean_condition_rules.py`

### Files to touch ###

- `registry/rules/rich_mixture.json` (CREATE)
- `registry/tests/test_rich_mixture_rules.py` (CREATE)

### Out of scope ###

- Other fault families (misfire, catalyst_failure, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- EVAP_CANISTER_SATURATED and VACUUM_REGULATOR_DIAPHRAGM_RUPTURE chemistry states — Tier D states in CHEMISTRY_COVERAGE.md; schema slots exist but no case data. Capture as follow-ups if the corpus gains cases
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream
- TIMING_RETARDED awareness for rich→retarded overlap — the CHEMISTRY_COVERAGE prioritized table mentions this but the chemistry × family matrix shows zero TIMING_RETARDED cases in rich_mixture. If future audit data confirms TIMING_RETARDED-rich overlap cases, it becomes a follow-up rule

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_rich_mixture_rules.py --fix
pyright registry/tests/test_rich_mixture_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/rich_mixture.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/rich_mixture.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/rich_mixture.json').read_text())
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
pytest registry/tests/test_rich_mixture_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-rich_mixture`: Status=done, Files changed=2, Verification="{HEADLINE}"
