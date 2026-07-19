### Goal ###

Author the v2 registry rule file at `registry/rules/non_starter.json` containing 4 competing rules for the `non_starter` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has a single rule (ERR-NS-004) covering only INCOMPLETE_COMBUSTION chemistry at base_weight 0.60 — the weakest rule in the entire v1 registry. REGISTRY_AUDIT.md §3.1 flags non_starter as "Single rule. REAL-001/003 will recover post FIX-GAS-1." CHEMISTRY_COVERAGE.md §3.3 grades non_starter as LOW severity: "4 cases, 1 rule. 2 pipeline-bug cases recover post FIX-GAS-1." The v2 rebuild must expand from 1 to 4 rules covering the 3 distinct chemistry patterns observed in the 4 curated cases, with cross-family competition against mechanical_wear (INCOMPLETE_COMBUSTION shared) and misfire (LEAN_MISFIRE, RICH_MISFIRE shared).

### Success criteria ###

- `registry/rules/non_starter.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 4 rules with unique `rule_id` values (NS-001 through NS-004)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `non_starter`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 1 rule uses LEAN_MISFIRE chemistry as GATING (NS-001 — lean no-start / no-fuel, covers 3 of 4 cases)
- At least 1 rule uses RICH_MISFIRE chemistry as GATING (NS-002 — flooded rich no-start, covers REAL-003)
- At least 1 rule uses INCOMPLETE_COMBUSTION chemistry as GATING with rpm < 600 GATING (NS-003 — differentiator from mechanical_wear MW-005 which has rpm > 600 GATING)
- At least 1 rule is DTC-driven (NS-004 — fuel-delivery no-start, covers case_006 P0230)
- No solo survivor: the `non_starter` competition group has ≥ 2 rules, and at least 2 rules carry `confidence_ceiling`
- Every rule that shares a chemistry state with another family carries `confidence_ceiling` (LEAN_MISFIRE shared with misfire, RICH_MISFIRE shared with misfire, INCOMPLETE_COMBUSTION shared with mechanical_wear)
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py`, `test_exhaust_leak_rules.py`, `test_sensor_fault_rules.py`, `test_ecu_fault_rules.py`, `test_cam_timing_rules.py`, `test_mechanical_wear_rules.py` continue to pass
- New test `registry/tests/test_non_starter_rules.py::test_ruleset_validates` passes

### Context ###

non_starter has 4 curated cases. The v1 registry has 1 rule (ERR-NS-004) — the weakest in the v1 catalog — gating only on INCOMPLETE_COMBUSTION chemistry at base_weight 0.60 with no competing rules. REAL-001 and REAL-003 are currently pipeline-bug cases (HC > 20,000 ppm exceeds GASLab bound; will recover post FIX-GAS-1 when the bound widens to 30,000). The non_starter family shares three chemistry states with other families: INCOMPLETE_COMBUSTION with mechanical_wear (MW-005), LEAN_MISFIRE with misfire (MF-003), and RICH_MISFIRE with misfire (MF-002). The universal differentiator is rpm: non_starter cases have rpm either missing (REAL-001, REAL-003 — cranking only, no running PID data) or < 600 (case_006=200, case_007=300 — cranking speed), while mechanical_wear and misfire cases have rpm > 600 (engine IS running).

The 4 cases break down into three chemistry clusters:

**Cluster A — LEAN_MISFIRE no-start (3 cases):** REAL-001 (HC=20200, CO≈0, CO2=0.16%, O2=19.73%, λ=1.14 — cranking only, fuel never lit), case_006 (HC=0, CO=0, CO2=0.04%, O2=20.9%, λ=2.5 — no fuel delivery at all, DTC P0230 fuel pump), case_007 (HC=300, CO≈0, CO2=4.0%, O2=16.0%, λ=1.35 — weak fuel, barely lights). Common signal: LEAN_MISFIRE chemistry + CO2 near-atmospheric (< 5%) = no meaningful combustion. All have stft=ltft=0 (fuel trims frozen — engine not running). Differentiated from misfire-family LEAN_MISFIRE cases by rpm < 600 and CO2 < 5% (running misfire cases have CO2 ≥ 10% because some combustion is occurring).

**Cluster B — RICH_MISFIRE no-start (1 case):** REAL-003 (HC=26710, CO=3.24%, CO2=1.16%, O2=14.54%, λ=0.63 — extreme cold enrichment, flooded). RICH_MISFIRE chemistry + CO2 near-atmospheric + stft=ltft=0. Differentiated from misfire-family RICH_MISFIRE by rpm < 600 and CO2 < 5%.

**Cluster C — INCOMPLETE_COMBUSTION no-start (overlaps A+B):** REAL-001 and REAL-003 produce INCOMPLETE_COMBUSTION as a secondary chemistry state (partial/near-zero combustion yields incomplete combustion products). This is the only chemistry state the v1 rule (ERR-NS-004) gates on. The v2 rule (NS-003) adds the rpm < 600 GATING differentiator — mechanical_wear MW-005 gates on INCOMPLETE_COMBUSTION with rpm > 600 GATING.

**DTC-driven path:** case_006 carries P0230 (fuel pump primary circuit) — a DTC that directly explains a no-start. NS-004 provides a DTC-driven fallback path independent of chemistry state. Also accepts P0087 (fuel rail pressure too low) and P0190 (fuel rail pressure sensor circuit) for broader fuel-delivery no-start coverage. confidence_ceiling applied because DTC-only rules lack chemistry confirmation.

Cross-family competition:
- **misfire:** Shares LEAN_MISFIRE and RICH_MISFIRE chemistry. Differentiated by rpm (non_starter: < 600 or missing; misfire: > 600) and CO2 (non_starter: < 5% near-atmospheric; misfire: ≥ 10% — combustion IS occurring, just poorly).
- **mechanical_wear:** Shares INCOMPLETE_COMBUSTION chemistry. Differentiated by rpm (non_starter NS-003: rpm < 600 GATING; mechanical_wear MW-005: rpm > 600 GATING). This is a clean binary split.
- **lean_condition:** REAL-001 has λ=1.14 (lean) but CO2=0.16% (no combustion). lean_condition cases have CO2 ≥ 12% (combustion IS occurring, just lean). The CO2 level is the differentiator.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/non_starter.json` — CREATE: RuleSet JSON with 4 rules for non_starter family. Minimum rules:
   - NS-001: LEAN_MISFIRE no-start. Chemistry-primary rule: LEAN_MISFIRE as GATING evidence. OBD: rpm < 600 as SUGGESTIVE (engine not running — when rpm data is available), co2 < 5.0% as SUGGESTIVE (no meaningful combustion — CO2 near atmospheric at 0.04-4.0%). stft in_range [-1.0, 1.0] as SUGGESTIVE with ltft in_range [-1.0, 1.0] as SUGGESTIVE (fuel trims frozen at zero — engine not in closed-loop fuel control). confidence_ceiling applied because LEAN_MISFIRE chemistry is shared with misfire family (MF-003). Covers REAL-001, case_006, case_007.
   - NS-002: RICH_MISFIRE no-start (flooded). Chemistry-primary rule: RICH_MISFIRE as GATING evidence. OBD: rpm < 600 as SUGGESTIVE, co2 < 5.0% as SUGGESTIVE, ect_c < 30.0 degC as SUGGESTIVE (cold-engine flood — REAL-003 is "extreme cold enrichment"). stft in_range [-1.0, 1.0] + ltft in_range [-1.0, 1.0] as SUGGESTIVE (trims frozen). confidence_ceiling applied because RICH_MISFIRE chemistry is shared with misfire family (MF-002). Covers REAL-003.
   - NS-003: INCOMPLETE_COMBUSTION no-start (v1 ERR-NS-004 reactivated). Chemistry-primary rule: INCOMPLETE_COMBUSTION as GATING evidence. OBD: rpm < 600 as GATING evidence (this is the mechanical_wear differentiator — MW-005 has rpm > 600 GATING on the same chemistry state). co2 < 8.0% as SUGGESTIVE. confidence_ceiling applied because INCOMPLETE_COMBUSTION chemistry is shared with mechanical_wear (MW-005). Covers REAL-001, REAL-003.
   - NS-004: DTC-driven fuel-delivery no-start. DTC-primary rule: P0230 (fuel pump primary circuit), P0087 (fuel rail pressure too low), P0190 (fuel rail pressure sensor circuit) with strategy any_match as GATING evidence. Chemistry: LEAN_MISFIRE as SUGGESTIVE (lean no-start is consistent with fuel delivery failure). OBD: rpm < 600 as SUGGESTIVE. confidence_ceiling applied because DTC-only rule without a chemistry GATING gate — this is a fallback path that shouldn't outcompete chemistry-primary rules NS-001/NS-003. Covers case_006.
2. `registry/tests/test_non_starter_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (LEAN_MISFIRE GATING in NS-001, RICH_MISFIRE GATING in NS-002, INCOMPLETE_COMBUSTION GATING + rpm < 600 GATING in NS-003, DTC any_match GATING in NS-004, confidence_ceiling on all 4 rules, competition group integrity, no solo survivor, all 4 case IDs resolve), following the pattern in `test_mechanical_wear_rules.py`.

### Files to touch ###

- `registry/rules/non_starter.json` (CREATE)
- `registry/tests/test_non_starter_rules.py` (CREATE)

### Out of scope ###

- Other fault families (vacuum_leak, overheating, charging_system, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 registry's ERR-NS-004 — the v1 registry is frozen; v2 replaces it at cutover
- FIX-GAS-1 (widening HC bound from 20,000 to 30,000) — that is a paused Tier 1 schema fix in the Jaeger plan; REAL-001 and REAL-003 will reach the router after that fix lands
- misfire family rules (MF-002, MF-003) that share LEAN_MISFIRE and RICH_MISFIRE chemistry — competition is resolved by rpm and CO2 level (non_starter: rpm < 600, CO2 < 5%; misfire: rpm > 600, CO2 ≥ 10%)
- mechanical_wear family rule MW-005 that shares INCOMPLETE_COMBUSTION chemistry — competition is resolved by the rpm gate (NS-003: rpm < 600; MW-005: rpm > 600)
- lean_condition family rules that could fire on REAL-001's λ=1.14 — competition is resolved by CO2 level (non_starter: CO2 < 5% near-atmospheric; lean_condition: CO2 ≥ 12%)
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_non_starter_rules.py --fix
pyright registry/tests/test_non_starter_rules.py
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

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/non_starter.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/non_starter.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/non_starter.json').read_text())
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
pytest registry/tests/test_non_starter_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-non_starter`: Status=done, Files changed=2, Verification="{HEADLINE}"
