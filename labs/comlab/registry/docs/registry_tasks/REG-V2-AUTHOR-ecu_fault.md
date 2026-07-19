### Goal ###

Author the v2 registry rule file at `registry/rules/ecu_fault.json` containing 5 competing rules for the `ecu_fault` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has zero executable rules for ecu_fault — both KG nodes (ERR-EF-001 fuel_trim_saturated, ERR-EF-002 closed_loop_fuel_control_disabled) are orphans with no entries in `global_fault_registry.json`. The 28 ecu_fault cases are the third-largest family in the curated corpus and currently all fail with `no_fault` because zero rules accept any chemistry state. ecu_fault is the only family with zero chemistry coverage — it must be DTC-driven and OBD-driven, with chemistry as secondary evidence only. 5 rules covering trim saturation (positive + negative), closed-loop disabled, ECU internal DTCs, and TIMING_RETARDED chemistry.

### Success criteria ###

- `registry/rules/ecu_fault.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 5 rules with unique `rule_id` values (EF-001 through EF-005)
- Every rule has `passes_cases` with at least one curated case ID that resolves to an `ecu_fault`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 2 rules use OBD fuel trim evidence (longft1 / shrtft1 PIDs) as GATING or SUGGESTIVE — these are the trim-saturation rules
- At least 1 rule uses DTC evidence with `ECU_INTERNAL_HISTORY`-range codes (P0600-P0699)
- At least 1 rule uses `TIMING_RETARDED` chemistry as SUGGESTIVE evidence (closes the ~10-case Tier B gap for ecu_fault)
- At least 1 rule has empty `chemistry_evidence` (DTC-primary or OBD-primary rule with no chemistry gate)
- At least 2 rules carry a `confidence_ceiling` (no solo survivor — ecu_fault has only 2 v1 KG nodes, so v2 must ensure ≥ 2 competing rules with documented confidence bounds)
- No solo survivor: the `ecu_fault` competition group has ≥ 2 rules, and at least 2 rules carry `confidence_ceiling`
- Every rule's `passes_cases` entries are traceable to actual case data — rules for trim saturation reference cases where ltft/stft values match the rule's thresholds
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py`, `test_exhaust_leak_rules.py`, `test_sensor_fault_rules.py` continue to pass
- New test `registry/tests/test_ecu_fault_rules.py::test_ruleset_validates` passes

### Context ###

ecu_fault has 28 curated cases — the third-largest family after lean_condition (53) and misfire (44). Zero of the 28 cases have a working v1 rule. Both v1 KG nodes (ERR-EF-001 fuel_trim_saturated, ERR-EF-002 closed_loop_fuel_control_disabled) are orphans with no entries in `global_fault_registry.json`. REGISTRY_AUDIT.md §2.4 and §3.1 flag this as "the single largest gap" and "zero executable rules."

The 28 cases break down into two clusters based on CSV evidence:

**Cluster A — Trim saturation (~18-20 cases):** Fuel trims are pegged at or near the ECU's adaptation limits. CSV-041/ECU-001 (ltft=15.0, stft=25.0, P0171, "Physical rich; ECU sees lean"), case_001 (ltft=22.0, stft=25.0, P0171, "Classic false-lean DTC"), EXP-N002 (ltft=25.0, stft=25.0, P0171), CSV-123 (ltft=-12.0, stft=-18.0, P0172, "Physical lean; ECU sees rich"), case_013 (ltft=-18.0, stft=-20.0, P0172). These are truth-vs-perception cases — the ECU perceives a mixture condition that contradicts the gas analyzer. The trims are saturated because the ECU has adapted as far as it can. This maps to ERR-EF-001 (fuel_trim_saturated).

**Cluster B — Closed-loop disabled / trims frozen (~8-10 cases):** Fuel trims are at or near 0.0 with DTCs indicating the ECU cannot control fuel. CSV-072 (ltft=0.0, stft=0.0, P0606, "Gas perfect; P0606 ROM failure"), ECU-002 (ltft=0.0, stft=0.0, P0113, "Gas clean; ECT/MAP/TPS impossible"), ECU-003 (ltft=0.0, stft=0.0, P0201, injector circuit). The trims are frozen because the ECU has disabled closed-loop fuel control. This maps to ERR-EF-002 (closed_loop_fuel_control_disabled).

The CHEMISTRY_COVERAGE.md matrix shows ecu_fault's chemistry footprint is TIMING_RETARDED (~10 cases) and SAMPLE_INVALID (~2 cases) — both are secondary symptoms, not primary detection signals. ecu_fault is the only family where chemistry is explicitly a secondary concern: the primary signals are OBD fuel trim patterns and DTC codes. This is the hardest family to author because it breaks the chemistry-first pattern that works for every other family.

Cross-family competition: ecu_fault trim-saturation rules compete with lean_condition (both see P0171 + positive trims) and rich_mixture (both see P0172 + negative trims). The differentiator is the truth-vs-perception gap — ecu_fault rules fire when the ECU's fuel trim adaptation contradicts the gas analyzer's chemistry, while lean_condition/rich_mixture rules fire when chemistry and trims agree. The perception_flag field is not used for ecu_fault (perception_flag records chemistry-state deception; trim deception is a different mechanism).

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/ecu_fault.json` — CREATE: RuleSet JSON with 5 rules for ecu_fault family. Minimum rules:
   - EF-001: Fuel trim saturated — positive (max enrichment). OBD-primary rule: longft1 >= 15.0 AND shrtft1 >= 20.0 as GATING evidence. P0171 DTC as SUGGESTIVE. No chemistry gate — the trim pattern is the primary signal. Covers the "false-lean" cases where ECU adds fuel against a rich or normal gas signature. v1 orphan ERR-EF-001 reactivated.
   - EF-002: Fuel trim saturated — negative (max enleanment). OBD-primary rule: longft1 <= -12.0 AND shrtft1 <= -15.0 as GATING evidence. P0172 DTC as SUGGESTIVE. No chemistry gate. Covers the "false-rich" cases where ECU pulls fuel against a lean or normal gas signature. v1 orphan ERR-EF-001 second polarity.
   - EF-003: Closed-loop fuel control disabled / trims frozen. OBD-primary rule: longft1 in_range [-3.0, 3.0] AND shrtft1 in_range [-3.0, 3.0] as GATING evidence (trims frozen near zero — ECU has stopped adapting). DTC evidence as SUGGESTIVE (any P0600-P0699 ECU internal, or sensor circuit codes P0113/P0201 that cause limp-mode). No chemistry gate — the frozen-trim pattern is the primary signal. v1 orphan ERR-EF-002 reactivated.
   - EF-004: ECU internal DTC — P0600-P0699 range. DTC-primary rule: `ECU_INTERNAL_HISTORY`-range codes (P0606, P0601, etc.) with strategy `any_match` at SUGGESTIVE tier. TIMING_RETARDED chemistry as SUGGESTIVE evidence for the ~10 cases where ECU fault causes timing retardation as a secondary symptom. OBD trim evidence as SUGGESTIVE (any trim anomaly — either saturated or frozen — supports the ECU-internal diagnosis).
   - EF-005: SAMPLE_INVALID with ECU fault. Chemistry-aware rule: SAMPLE_INVALID as SUGGESTIVE evidence (measurement anomaly signal — the gas triangle is unphysical, possibly because ECU fault corrupts sensor data). OBD trim or DTC evidence as GATING (at least one of: trims saturated, trims frozen, or P06xx DTC present). Covers the ~2 SAMPLE_INVALID ecu_fault cases.
2. `registry/tests/test_ecu_fault_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (trim saturation OBD evidence in EF-001/EF-002, frozen-trim pattern in EF-003, ECU_INTERNAL_HISTORY DTC evidence in EF-004, TIMING_RETARDED chemistry coverage, SAMPLE_INVALID coverage in EF-005, empty chemistry_evidence valid for OBD-primary rules, competition group integrity, no solo survivor, all 28 case IDs resolve), following the pattern in `test_sensor_fault_rules.py`.

### Files to touch ###

- `registry/rules/ecu_fault.json` (CREATE)
- `registry/tests/test_ecu_fault_rules.py` (CREATE)

### Out of scope ###

- Other fault families (cam_timing, mechanical_wear, non_starter, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 registry's ERR-EF-001/ERR-EF-002 orphan state — the v1 registry is frozen; v2 replaces it at cutover
- lean_condition family rules that compete with ecu_fault for P0171 + positive trim cases — competition between ecu_fault and lean_condition for trim-saturation cases is resolved by the truth-vs-perception pattern (ecu_fault rules fire when trims contradict chemistry; lean_condition rules fire when trims and chemistry agree)
- rich_mixture family rules that compete with ecu_fault for P0172 + negative trim cases — same competition resolution as lean_condition
- sensor_fault family rules for O2 sensor bias that also produce P0171/P0172 — O2 bias cases have NORMAL_OPERATION chemistry with perception_flag; ecu_fault trim-saturation cases have trims at extremes regardless of chemistry
- DTC vocabulary expansion — P0600-P0699 codes beyond P0606 are defined in the DTCRoutingTag.ECU_INTERNAL_HISTORY enum value; individual code enumeration belongs to DTC vocabulary maintenance, not rule authoring
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_ecu_fault_rules.py --fix
pyright registry/tests/test_ecu_fault_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q
pytest registry/tests/test_exhaust_leak_rules.py -x -q
pytest registry/tests/test_sensor_fault_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/ecu_fault.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/ecu_fault.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/ecu_fault.json').read_text())
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
pytest registry/tests/test_ecu_fault_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-ecu_fault`: Status=done, Files changed=2, Verification="{HEADLINE}"
