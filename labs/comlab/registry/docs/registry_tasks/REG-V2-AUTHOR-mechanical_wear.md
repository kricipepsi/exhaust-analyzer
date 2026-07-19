### Goal ###

Author the v2 registry rule file at `registry/rules/mechanical_wear.json` containing 6 competing rules for the `mechanical_wear` fault family. Each rule uses the evidence-tier model (DEFINITIVE / SUGGESTIVE / GATING) defined in `schema_v2.py`. The v1 registry has 6 rules (ERR-MW-001 through ERR-MW-006) covering 5 chemistry states: INCOMPLETE_COMBUSTION, COOLANT_LEAK_INTERNAL, WORN_PISTON_RINGS, WORN_VALVE_SEALS, WORN_ENGINE. REGISTRY_AUDIT.md §3.1 notes cross-family confusion: "lean vs mechanical_wear overlap" and CHEMISTRY_COVERAGE.md §4.1 grades mechanical_wear as LOW severity with TIMING_RETARDED (~3 cases) as the primary chemistry gap. Cross-family competition with lean_condition (lean-like signatures), cam_timing (WRONG_VALVE_TIMING chemistry), non_starter (INCOMPLETE_COMBUSTION chemistry), and catalyst_failure (WORN_PISTON_RINGS label confusion). 6 rules covering worn rings/oil consumption, worn valve seals, coolant-in-combustion/HG breach, low compression/worn engine, INCOMPLETE_COMBUSTION differentiation, and TIMING_RETARDED chemistry overlap.

### Success criteria ###

- `registry/rules/mechanical_wear.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly 6 rules with unique `rule_id` values (MW-001 through MW-006)
- Every rule has `passes_cases` with at least one curated case ID that resolves to a `mechanical_wear`-labelled row in `corpus_curated.csv`
- Every numeric threshold carries a `wiki_ref` citation (no bare magic numbers)
- At least 1 rule uses WORN_PISTON_RINGS chemistry as GATING (MW-001 — oil consumption / ring wear)
- At least 1 rule uses WORN_VALVE_SEALS chemistry as GATING (MW-002 — valve stem seal wear)
- At least 1 rule uses COOLANT_LEAK_INTERNAL chemistry as GATING (MW-003 — HG breach / coolant in combustion)
- At least 1 rule uses WORN_ENGINE chemistry as GATING (MW-004 — low compression / general wear)
- At least 1 rule uses INCOMPLETE_COMBUSTION chemistry as GATING (MW-005 — general mechanical wear with running-engine precondition)
- At least 1 rule uses TIMING_RETARDED chemistry as SUGGESTIVE evidence (MW-006 — closes the ~3-case Tier B gap for mechanical_wear)
- No solo survivor: the `mechanical_wear` competition group has ≥ 2 rules, and at least 2 rules carry `confidence_ceiling`
- At least 1 rule uses DTC `none_present` strategy for VVT codes to differentiate mechanical_wear TIMING_RETARDED from cam_timing (MW-006)
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py`, `test_lean_condition_rules.py`, `test_rich_mixture_rules.py`, `test_misfire_rules.py`, `test_catalyst_failure_rules.py`, `test_exhaust_leak_rules.py`, `test_sensor_fault_rules.py`, `test_ecu_fault_rules.py`, `test_cam_timing_rules.py` continue to pass
- New test `registry/tests/test_mechanical_wear_rules.py::test_ruleset_validates` passes

### Context ###

mechanical_wear has 11 curated cases. The v1 registry has 6 rules — the most of any family outside catalyst_failure — but REGISTRY_AUDIT.md identifies cross-family confusion as the primary failure mode: "Rules exist but cross-family confusion common (lean vs mechanical_wear overlap)." The v1 chemistry-to-family mapping is mostly correct (WORN_PISTON_RINGS → mechanical_wear, COOLANT_LEAK_INTERNAL → mechanical_wear) but labelled cases exist in catalyst_failure and sensor_fault that produce mechanical_wear chemistries. CHEMISTRY_COVERAGE.md §3.3 shows mechanical_wear has 5 v1-registered chemistry states; the only gap is TIMING_RETARDED (~3 cases, shared with 6 other families).

The 11 cases break down into four clusters:

**Cluster A — Oil consumption / ring wear (4 cases, WORN_PISTON_RINGS chemistry):** MECH-001 (HC persists at 2500rpm, oil burn), EXT-223 (worn rings, HC elevated at idle, drops at 2500 RPM — ring flutter seals at higher RPM), CSV-117 (snap-throttle HC spikes to ~950, idle normal, oil burn-off), case_044 (high HC with normal CO and λ≈1.0, oil consumption / rings). All show elevated HC with near-normal CO and λ. The key OBD signal: HC at idle vs 2500 RPM — worn rings produce higher HC at idle (oil slips past rings at low RPM, lower vacuum) and lower HC at 2500 RPM (ring flutter seals, vacuum increases). This is the opposite pattern of lean_condition where HC worsens with RPM.

**Cluster B — Valve stem seal wear (1 case, WORN_VALVE_SEALS chemistry):** CSV-118 (HC plume on snap-throttle, bluish smoke). Valve stem seals leak oil into the combustion chamber under high vacuum (deceleration / snap-throttle closed). The HC spike is transient — not a steady-state condition. Differentiated from ring wear by the transient/snap-throttle pattern vs steady elevated HC.

**Cluster C — Coolant in combustion / head gasket breach (4 cases, COOLANT_LEAK_INTERNAL chemistry):** MECH-002 (coolant in combustion, CO2 depressed), CSV-119 (HC>900 + O2>3 + white sweet smoke, CO2 depressed), CSV-120 (severe HG breach, coolant burning in chamber, cylinder-pressure cross-talk), EXT-224 (head gasket breach between cylinders 3-4, combustion pressure cross-talk, FF captured). The COOLANT_LEAK_INTERNAL chemistry is distinctive — coolant quenches combustion, producing elevated HC + elevated O2 + depressed CO2 simultaneously. OBD: ect_c elevated (coolant loss concentrates heat in remaining coolant), MAP signature of pressure cross-talk between adjacent cylinders.

**Cluster D — Low compression / general wear (2 cases, WORN_ENGINE + INCOMPLETE_COMBUSTION):** MECH-006 (weak cylinders, CO2<12%), EXT-222 (low compression on 3 cylinders, acceptable idle but fails under load, FF: 3100 RPM). Both show severely depressed CO2 (<12-13%) — the hallmark of incomplete combustion from mechanical sealing failure. MAP may show low vacuum at idle.

**TIMING_RETARDED overlap (~3 cases):** per CHEMISTRY_COVERAGE.md, ~3 curated cases produce TIMING_RETARDED chemistry with a mechanical_wear label. These are cases where low compression causes late/incomplete combustion → TIMING_RETARDED chemistry. Differentiated from cam_timing by the ABSENCE of VVT DTCs (P0010-P0025) — cam_timing TIMING_RETARDED cases carry VVT codes; mechanical_wear TIMING_RETARDED cases do not.

Cross-family competition:
- **lean_condition:** Both see elevated HC + O2. Differentiated by: mechanical_wear has normal-to-depressed CO2 (not elevated O2 from lean burn), normal λ (not >1.03), and HC drops at 2500 RPM (rings seal) vs lean_condition where HC rises with RPM.
- **cam_timing:** Shares WRONG_VALVE_TIMING chemistry (mechanical base timing vs worn chain/belt). Differentiated by DTC presence (cam_timing: VVT codes; mechanical_wear: no VVT codes). Also shares TIMING_RETARDED chemistry (MW-006 uses DTC none_present on VVT codes to differentiate).
- **non_starter:** Shares INCOMPLETE_COMBUSTION chemistry. Differentiated by RPM: mechanical_wear has rpm > 600 (engine running); non_starter has rpm = 0 or cranking-only.
- **catalyst_failure:** Some cases labelled catalyst_failure produce WORN_PISTON_RINGS chemistry (cross-family confusion). Competition resolved by chemistry-primary routing: WORN_PISTON_RINGS GATING → mechanical_wear rules fire first.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/mechanical_wear.json` — CREATE: RuleSet JSON with 6 rules for mechanical_wear family. Minimum rules:
   - MW-001: Worn piston rings / oil consumption. Chemistry-primary rule: WORN_PISTON_RINGS as GATING evidence. OBD: HC at idle elevated with HC dropping at 2500 RPM (HC_2500 < HC_idle pattern, where the analyser shows HC falling at higher RPM — ring flutter seals under load) as SUGGESTIVE. Differentiated from lean_condition (HC rises with RPM) and catalyst_failure (λ and CO2 differ). v1 ERR-MW-003 reactivated with OBD evidence added (v1 was GAS_ONLY + shrtft1 IN_RANGE [-10,10] constraint that may fail cases with trim response to oil burning). Covers MECH-001, EXT-223, CSV-117, case_044.
   - MW-002: Worn valve stem seals. Chemistry-primary rule: WORN_VALVE_SEALS as GATING evidence. OBD: no steady-state OBD evidence required — the chemistry state alone carries the signal (valve seal leak is a transient snap-throttle phenomenon that the gas analyser captures as WORN_VALVE_SEALS chemistry). v1 ERR-MW-004 reactivated (v1 was GAS_ONLY at 0.70). confidence_ceiling applied because this is the only rule in the set that gates on WORN_VALVE_SEALS (single-chemistry rule within a multi-rule family — the ceiling applies when this rule is the sole survivor against other families, not within mechanical_wear). Covers CSV-118.
   - MW-003: Coolant in combustion / head gasket breach. Chemistry-primary rule: COOLANT_LEAK_INTERNAL as GATING evidence. OBD: ect_c > 95.0 as SUGGESTIVE (coolant loss raises remaining coolant temperature), CO2 < 13.0% as SUGGESTIVE (coolant quenches combustion, suppressing CO2 formation). v1 ERR-MW-002 expanded with CO2 evidence (v1 had only ect_c > 90.0). Covers MECH-002, CSV-119, CSV-120, EXT-224.
   - MW-004: Low compression / worn engine. Chemistry-primary rule: WORN_ENGINE as GATING evidence. OBD: CO2 < 12.0% as SUGGESTIVE (severely depressed CO2 is the hallmark of sealing failure — combustion products escape past rings/valves before full oxidation). map_kpa < 30.0 as SUGGESTIVE (low vacuum from weak cylinders at idle — v1 ERR-MW-005 carried this constraint). v1 ERR-MW-006 expanded with MAP + CO2 evidence (v1 had no OBD constraints). Covers MECH-006, EXT-222.
   - MW-005: INCOMPLETE_COMBUSTION chemistry with running-engine precondition. Chemistry-primary rule: INCOMPLETE_COMBUSTION as GATING evidence (shared with non_starter family). OBD: rpm > 600 as GATING evidence (engine IS running — this is the mechanical_wear/non_starter differentiator: non_starter cases never reach running RPM). CO2 < 13.0% as SUGGESTIVE (incomplete combustion depresses CO2 yield). confidence_ceiling applied because INCOMPLETE_COMBUSTION chemistry is shared with non_starter — when this rule fires as sole survivor, confidence is capped. Covers MECH-006, EXT-222 (these cases produce both WORN_ENGINE and INCOMPLETE_COMBUSTION chemistry — competing rules MW-004 and MW-005 both fire, competition scoring resolves). v1 ERR-MW-001 reactivated with running-engine gate and non_starter awareness.
   - MW-006: TIMING_RETARDED chemistry overlap — Tier B gap closer. Chemistry-aware rule: TIMING_RETARDED as SUGGESTIVE evidence (late combustion from low compression produces retarded combustion phasing). DTC: VVT_HISTORY range DTCs (P0010-P0025) with strategy `none_present` as GATING evidence — NO VVT DTCs may be present (this is the cam_timing differentiator: cam_timing TIMING_RETARDED cases carry VVT codes; mechanical_wear TIMING_RETARDED cases do not). OBD: no specific OBD requirement — the DTC none_present gate is the key differentiator. confidence_ceiling applied because TIMING_RETARDED chemistry is shared across 7 families. Covers the ~3 TIMING_RETARDED cases where the curated label is mechanical_wear and no VVT DTCs are present. v1 had no equivalent rule (TIMING_RETARDED had zero v1 registrations).
2. `registry/tests/test_mechanical_wear_rules.py` — CREATE: targeted tests with evidence-tier coverage checks (WORN_PISTON_RINGS chemistry gate in MW-001, WORN_VALVE_SEALS chemistry gate in MW-002, COOLANT_LEAK_INTERNAL chemistry gate in MW-003, WORN_ENGINE chemistry gate in MW-004, INCOMPLETE_COMBUSTION chemistry gate + rpm GATING in MW-005, TIMING_RETARDED SUGGESTIVE + VVT none_present DTC gate in MW-006, confidence_ceiling on MW-002/MW-005/MW-006, competition group integrity, no solo survivor, all 11 case IDs resolve), following the pattern in `test_cam_timing_rules.py`.

### Files to touch ###

- `registry/rules/mechanical_wear.json` (CREATE)
- `registry/tests/test_mechanical_wear_rules.py` (CREATE)

### Out of scope ###

- Other fault families (non_starter, vacuum_leak, overheating, charging_system, etc.) — each gets its own REG-V2-AUTHOR-{family} session
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Fixing the v1 registry's ERR-MW-001 through ERR-MW-006 — the v1 registry is frozen; v2 replaces it at cutover
- lean_condition family rules that compete with mechanical_wear for lean-like HC/O2 signatures — competition is resolved by CO2 and λ differences (mechanical_wear: CO2 depressed, λ normal; lean_condition: CO2 normal/elevated, λ > 1.03)
- cam_timing family rules that compete with mechanical_wear for WRONG_VALVE_TIMING and TIMING_RETARDED chemistry — competition is resolved by VVT DTC presence (cam_timing: VVT codes present; mechanical_wear: no VVT codes) per MW-006's none_present gate
- non_starter family rules that share INCOMPLETE_COMBUSTION chemistry — competition is resolved by RPM gate (MW-005: rpm > 600; non_starter: rpm = 0 or cranking-only)
- catalyst_failure cross-family confusion (cases labelled catalyst_failure that produce WORN_PISTON_RINGS chemistry) — resolved by chemistry-primary routing in the integration shim; this is REG-V2-INTEGRATE scope
- Any Python evaluation logic — rules are JSON data; the schema is the only Python touched in this workstream

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_mechanical_wear_rules.py --fix
pyright registry/tests/test_mechanical_wear_rules.py
pytest registry/tests/test_schema_v2.py -x -q
pytest registry/tests/test_lean_condition_rules.py -x -q
pytest registry/tests/test_rich_mixture_rules.py -x -q
pytest registry/tests/test_misfire_rules.py -x -q
pytest registry/tests/test_catalyst_failure_rules.py -x -q
pytest registry/tests/test_exhaust_leak_rules.py -x -q
pytest registry/tests/test_sensor_fault_rules.py -x -q
pytest registry/tests/test_ecu_fault_rules.py -x -q
pytest registry/tests/test_cam_timing_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/mechanical_wear.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/mechanical_wear.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/mechanical_wear.json').read_text())
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
pytest registry/tests/test_mechanical_wear_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-mechanical_wear`: Status=done, Files changed=2, Verification="{HEADLINE}"
