### Goal ###

Author the v2 registry rule file at `registry/rules/charging_system.json` containing **2 competing rules** for the new `charging_system` fault family (the last of three new families from `cvsgaps.md` gap analysis). Populate the 3 placeholder curated cases (NEW-charging_system-01 through -03) with realistic gas/OBD/DTC values representing system-voltage and ghost-misfire diagnostic patterns. This is a **DTC-only** family: the system-voltage DTCs P0562 and P0563 (per `DTC_VOCABULARY §15` of `DTCLab/docs/wiki/DTC_VOCABULARY.md`) are the sole diagnostic signal available because the v2 schema's `OBDEvidence` does not carry a `battery_voltage_v` PID and `corpus_curated.csv` has no `battery_v` column. Rules gate on raw `dtc_codes` lists with `strategy: "any_match"` (mirroring VL-002's pattern); no new `DTCRoutingTag` enum value is added. The two rules are: **CS-001** — direct DTC pathognomonic, and **CS-002** (renumbered from the earlier CS-003 draft) — ghost-misfire discriminator with double-GATING (charging DTC + clean chemistry) that dominates the misfire family's MF-004 by a controlled margin. This family has zero v1 rules and no prior Python evaluation logic to rebuild.

### Success criteria ###

- `registry/rules/charging_system.json` exists, parses as valid JSON, and validates against `RuleSet` model from `registry/schema_v2.py`
- Exactly **2 rules** with unique `rule_id` values (CS-001, CS-002)
- Every rule has `passes_cases` with at least one NEW-charging_system case ID that resolves to a `charging_system`-labelled row in `corpus_curated.csv`
- Every cited DTC code is grounded in `DTCLab/docs/wiki/DTC_VOCABULARY.md §15` — only P0562 and P0563 are cited as charging-system DTCs (P0620–P0626 are **not** in the wiki and are NOT used); P0300 is cited on CS-002's SUGGESTIVE entry per `DTC_VOCABULARY §15` line 522
- Every `DTCEvidence` and `ChemistryEvidence` entry carries a `wiki_ref` citation (no bare references)
- All rules are DTC-gated: every rule has at least one `DTCEvidence` entry with `tier: "GATING"` and `strategy: "any_match"`
- **No new `DTCRoutingTag` enum value added** — rules use raw `dtc_codes`; the schema_v2.py vocabulary mirror invariant stays intact (20 members)
- CS-001 has empty `chemistry_evidence`; CS-002 has exactly one `ChemistryEvidence` entry: `NORMAL_OPERATION` at tier `GATING` (the clean-chemistry condition is a precondition, not supporting evidence — this is the discriminator against MF-004)
- No solo survivor: the `charging_system` competition group has 2 rules, and every rule carries `confidence_ceiling`
- **CS-001 ceiling = 0.85** (matches OV-002's precedent for a single-specific-DTC pathognomonic rule); **CS-002 ceiling = 0.75** (one notch above MF-004's 0.70 to dominate ghost-misfire ambiguity on NEW-charging_system-03)
- The 3 NEW-charging_system placeholder rows in `corpus_curated.csv` are populated with realistic DTC values plus clean idle gas / OBD context (gas roughly NORMAL_OPERATION; ECT and RPM populated; battery voltage observed value is documented in the case `description` column only — not captured in any schema field)
- NEW-charging_system-02 is profiled as **overcharging** (P0563 system voltage high, e.g. battery 15.2 V) rather than alternator-regulator (which would have required P062x codes that DTC_VOCABULARY does not list as charging codes); both NEW-charging_system-01 (P0562, undervolt) and NEW-charging_system-02 (P0563, overvolt) are covered by CS-001
- `corpus_meta.json` placeholder notes updated from "Placeholder case. To be populated…" to "Populated during REG-V2-AUTHOR-charging_system — <one-line severity description>."
- Inner loop clean: JSON parse → schema validate → case-ID resolve
- Existing tests `registry/tests/test_schema_v2.py` and all 15 existing rule test files continue to pass (with particular attention to `test_misfire_rules.py` — MF-004 is **not** modified)
- New test `registry/tests/test_charging_system_rules.py::test_ruleset_validates` passes

### Context ###

charging_system is the last new fault family per `cvsgaps.md`: "Sensor drift or noise from a failing alternator can trigger spurious faults (e.g., a 'ghost' misfire). The suite could be strengthened with dedicated cases for low-voltage conditions and excessive electrical noise." Plan §10.2 calls for 2–3 cases with detection signal "Low/bouncing voltage, sensor noise, ghost misfires."

The v1 registry has zero rules for charging_system; the 281-case corpus has no dedicated charging-system test cases. The 3 placeholder cases in `corpus_curated.csv` carry only `case_id`, `expected_top_fault_family=charging_system`, `expected_state=named_fault`, and confidence bounds 0.65–0.90 — all gas/OBD/DTC columns are blank.

**Wiki-grounded DTC vocabulary (the critical constraint).** A first draft of this spec proposed a CS-002 rule citing `["P0620", "P0621", "P0622", "P0625", "P0626"]` as generator/regulator codes. Verification against `DTCLab/docs/wiki/DTC_VOCABULARY.md §15` (lines 528–531) shows that **only P0562 and P0563 are in the wiki as charging-system codes**, both routed to `ECU_INTERNAL_HISTORY`. P0620–P0626 are not in the wiki. Per the registry's "every numeric literal carries a wiki citation" discipline, the alternator/regulator rule was dropped entirely; the family ships with 2 rules instead of 3. NEW-charging_system-02 was reassigned from "alternator regulator failure" to "overcharging" so it can be covered by CS-001's P0563 GATING.

**Why DTC-only and chemistry-light (in detail).** Charging-system faults are electrical, not combustion. A failing alternator does not change air–fuel ratio, does not retard timing in a way GASLab observes, and does not produce a Brettschneider lambda signature. The diagnostic signal lives entirely in (a) charging-DTC presence (P0562 system voltage low; P0563 system voltage high), (b) battery voltage telemetry which the registry corpus does not currently capture, and (c) downstream symptoms (ghost misfires) that overlap with the misfire family and cannot be uniquely attributed without the primary electrical signal. Because the v2 schema's `OBDEvidence` (schema_v2.py L153–189) carries no `battery_voltage_v` PID and `corpus_curated.csv` has no `battery_v` column, this task does not attempt indirect detection. Cases without charging DTCs are out of scope for this round (would require a corpus-contract expansion task — out of scope here per JAEGER plan §10 addendum, which paused all schema fixes).

**Why no `ELECTRICAL_HISTORY` routing tag is added.** Two scoping decisions confirmed before drafting this spec:

1. `Rule.dtc_evidence` is a list of `DTCEvidence` objects carrying `dtc_codes: list[str]` directly (schema_v2.py L200). `DTCRoutingTag` is referenced nowhere in `Rule` or its evidence classes — it is a manual mirror of DTCLab's enum, documented at schema_v2.py L102–109, and the rules do not consume it during evaluation. VL-002 in `rules/vacuum_leak.json` is the canonical pattern: raw P-codes (`["P0171", "P0174"]`) with `strategy: "any_match"`, no routing-tag indirection.
2. Adding `ELECTRICAL_HISTORY` would overlap with `ECU_INTERNAL_HISTORY` (schema_v2.py L121; `DTC_VOCABULARY §15` line 529 explicitly routes P0562/P0563 to `ECU_INTERNAL_HISTORY`). Two valid tags for the same DTC bucket would be undefined routing. The only coordinated enum precedent (`CYLINDER_FLUID_MISFIRE`, L106–109) was added via FIX-ENUM-1 with explicit COMLab/DTCLab coordination; an unauthorised mirror-drift add would break the schema_v2.py L7–8 invariant.

**Competition with the misfire family (the reckoning).** The earlier draft of this spec stated that "MF-001..006 will not fire DEFINITIVE on NORMAL chemistry." That was wrong. Reading `registry/rules/misfire.json` MF-004 directly:

- description: *"Ghost misfire — ECU hallucinates P0300 from electrical noise, loose ground, or flywheel play despite pristine combustion chemistry"*
- chemistry_evidence: `[{state: "NORMAL_OPERATION", tier: "DEFINITIVE"}]`
- dtc_evidence: `[{dtc_codes: ["P0300", "P0301", "P0302", "P0303", "P0304"], tier: "SUGGESTIVE"}]`
- confidence_ceiling: **0.70**

MF-004's domain ("loose ground, electrical noise") overlaps directly with charging-system electrical noise by description. Its evidence pattern fires on every NEW-charging_system-03 case. The first-draft CS-003 (chemistry SUGGESTIVE, ceiling 0.70) would tie MF-004 at 0.70 with strictly weaker chemistry evidence — losing the diagnostic specificity that was the entire point of the rule.

CS-002 in this revised spec resolves the overlap by **strengthening evidence**, not by modifying MF-004:

| Attribute | MF-004 (frozen) | CS-002 (this task) |
|---|---|---|
| Chemistry `NORMAL_OPERATION` | DEFINITIVE | **GATING** (precondition, not supporting evidence) |
| Charging DTC (P0562/P0563) | not present | **GATING** (`strategy: "any_match"`) |
| `P0300` misfire DTC | SUGGESTIVE | SUGGESTIVE |
| `hc < 200` (idle HC) | SUGGESTIVE | not used |
| ceiling | 0.70 | **0.75** |
| competition_group | `"misfire"` | `"charging_system"` |

On NEW-charging_system-03 (P0300 + P0562 + NORMAL chemistry):
- MF-004 fires: chemistry NORMAL DEFINITIVE + P0300 SUGGESTIVE → ceiling 0.70
- CS-002 fires: charging DTC GATING + chemistry NORMAL GATING + P0300 SUGGESTIVE → ceiling 0.75

CS-002 wins by one ceiling notch with strictly stronger gating discipline (two GATING entries vs MF-004's zero GATING entries — MF-004 has no GATING evidence at all in the existing file).

On a real ghost-misfire **without** a charging DTC (P0300 + NORMAL only):
- MF-004 fires: NORMAL DEFINITIVE + P0300 SUGGESTIVE → 0.70 verdict "ghost misfire" (unattributed)
- CS-002 does **not** fire: charging-DTC GATING entry is absent in observed DTCs, so the rule is gated out

Clean separation. The 0.75 ceiling reflects residual ambiguity (some real-misfire chemistries are subtle and can be confused with NORMAL at low gas-analyser resolution); 0.85 would over-claim specificity that depends on a DTC the wiki acknowledges as a generic ECU-internal code.

**Why `NORMAL_OPERATION` at tier `GATING` is the novel pattern.** Chemistry-GATING itself is *widespread* in the registry — verified by `grep` across `registry/rules/*.json` at spec-authoring time, 15 instances across 6 files:

| File | Rules | States gated |
|---|---|---|
| `cam_timing.json` | CT-001..004 | WRONG_VALVE_TIMING, VVT_FAILURE, IGNITION_MISFIRE |
| `mechanical_wear.json` | MW-001..005 | WORN_PISTON_RINGS, WORN_VALVE_SEALS, COOLANT_LEAK_INTERNAL, WORN_ENGINE, INCOMPLETE_COMBUSTION |
| `non_starter.json` | NS-001..003 | LEAN_MISFIRE, RICH_MISFIRE, INCOMPLETE_COMBUSTION |
| `misfire.json` | MF-006 | SAMPLE_INVALID |
| `rich_mixture.json` | RM-003 | SAMPLE_INVALID |
| `ecu_fault.json` | EF-005 | SAMPLE_INVALID |

Every existing chemistry-GATING use gates on an **anomalous** state (a specific fault signature, or `SAMPLE_INVALID`). CS-002 is the first rule in the registry to gate on `NORMAL_OPERATION` — i.e. on the *absence* of any anomalous chemistry signature. This is the genuinely novel pattern; it should be flagged in CODE REVIEW section A as such, not as "first chemistry-GATING."

The schema supports `NORMAL_OPERATION` GATING cleanly (`EvidenceTier.GATING` on `ChemistryEvidence`; `NORMAL_OPERATION` is a valid `ChemistryState` enum value per schema_v2.py L42). Semantically, GATING means "must be present for the rule to evaluate." For CS-002, the clean-chemistry condition is structurally part of the rule's discriminator from MF-004 — it is not background context. Using SUGGESTIVE here would lose to MF-004's DEFINITIVE on chemistry; the rule needs chemistry as a gate, not as supporting evidence. The CODE REVIEW skill's section A item *"Rules-as-data discipline — no diagnostic logic added inside a rule callback or similar escape hatch"* passes (the GATING tier is a schema-supported field, not a code escape).

**Router-behavior assumption (load-bearing, not verified in this task).** The "NORMAL_OPERATION GATING" pattern only works as intended if the COMLab router treats *missing chemistry* (GASLab returned no sample — analyser offline, no idle gas captured, sampling failed) as **"rule does not fire"** rather than as **"impute NORMAL_OPERATION."** The two scenarios diverge sharply:

- **Hard-absence semantics (intended):** missing chemistry ⇒ CS-002's `NORMAL_OPERATION` GATING entry is unsatisfied ⇒ rule does not fire. On a real misfire case where chemistry was simply not captured, MF-001..003 / MF-005 (which gate on anomalous chemistry) also don't fire, but MF-004 (which gates on NORMAL_OPERATION DEFINITIVE) would behave the same way — both rules fail symmetrically. Discriminator preserved.
- **Imputation semantics (catastrophic):** missing chemistry ⇒ router defaults to NORMAL_OPERATION ⇒ CS-002 fires on every case with missing chemistry that happens to also have a charging DTC + P0300. Worse, on a real misfire case where chemistry was anomalous but not captured, CS-002 fires falsely and the diagnosis is mis-attributed to "charging" when it should be misfire-unknown.

The router lives in `COMLab/comlab/core/fault_atlas_router.py` (per JAEGER plan §2 reality table). The registry workstream is self-contained and cannot inspect or verify COMLab's chemistry-handling semantics — that boundary is set by the import-direction rule (schema_v2.py L4: *"No imports from any lab, COMLab, or 4DLabWired"*). The assumption is documented here and carried forward as a **REG-V2-INTEGRATE verification gate**: before cutover, the side-by-side harness must include at least one case with missing chemistry + a charging DTC, and verify CS-002 does not fire. If the router uses imputation semantics, the v2 schema or the CS-002 rule must be revised at integration time — not a fix for this task.

This is captured as a follow-up row in `REGISTRY_PROGRESS.md` "Unplanned follow-ups" at task close: *"CS-002 NORMAL_OPERATION-GATING assumes router uses hard-absence semantics for missing chemistry. Verify at REG-V2-INTEGRATE."*

**Ceiling discipline (corrected).** OV-002 in `rules/overheating.json` ships at confidence_ceiling **0.85** for the same archetype as CS-001: single specific DTC, DTC-pathognomonic, single-fault diagnosis (P0128 thermostat). Matching that precedent, CS-001 ships at 0.85. The earlier draft cap of 0.80 had no rationale; corrected.

The 3 cases (severity / etiology profiles):

1. **NEW-charging_system-01** — System voltage low. P0562 DTC active. Clean idle gas (NORMAL): λ=1.00, HC=8 ppm, CO=0.08 %, CO₂=15.0 %, O₂=0.3 %, NOx=380 ppm. OBD: ECT=88 °C, RPM=850. DTC: `["P0562"]`. At 2500 RPM: λ=1.00, HC=6 ppm, CO=0.06 %, CO₂=15.2 %, O₂=0.2 %, NOx=280 ppm. `description`: "Battery voltage 11.8 V at idle (undervolt). Schema does not capture battery voltage; DTC is the diagnostic signal." Covered by CS-001.
2. **NEW-charging_system-02** — System voltage high (overcharging). P0563 DTC active. Clean idle gas (NORMAL): λ=1.00, HC=10 ppm, CO=0.10 %, CO₂=14.9 %, O₂=0.4 %, NOx=350 ppm. OBD: ECT=92 °C, RPM=880. DTC: `["P0563"]`. At 2500 RPM: λ=1.00, HC=8 ppm, CO=0.08 %, CO₂=15.1 %, O₂=0.3 %, NOx=260 ppm. `description`: "Battery voltage 15.2 V at idle (overvolt — voltage regulator failure manifesting as overcharge). Schema does not capture battery voltage; DTC is the diagnostic signal." Covered by CS-001.
3. **NEW-charging_system-03** — Charging-induced ghost misfire. Voltage instability causes O₂-sensor noise that the ECU mis-attributes as a random misfire. P0300 fires together with P0562. Gas chemistry is clean (combustion is fine — the misfire is electrical-sensor noise, not real): λ=1.00, HC=12 ppm, CO=0.10 %, CO₂=14.8 %, O₂=0.4 %, NOx=320 ppm. OBD: ECT=90 °C, RPM=830 (slightly rough), MAP=33 kPa. DTC: `["P0562", "P0300"]`. At 2500 RPM: λ=1.00, HC=10 ppm, CO=0.08 %, CO₂=15.0 %, O₂=0.3 %, NOx=240 ppm. `description`: "Ghost misfire — gas chemistry NORMAL but ECU reports P0300; battery voltage 11.5 V bouncing 0.4 V observed. Schema does not capture battery voltage; charging DTC + clean chemistry is the discriminator from real misfire." Covered by CS-002.

Load skills: (none — no on-demand domain skills authored yet per _INDEX.md)

### Deliverables ###

1. `registry/rules/charging_system.json` — CREATE: RuleSet JSON with **2 rules** for charging_system family.

   - **CS-001** — System voltage fault (low or high).
     - `dtc_evidence`: `[{dtc_codes: ["P0562", "P0563"], strategy: "any_match", tier: "GATING", wiki_ref: "DTC_VOCABULARY §15"}]`
     - `chemistry_evidence`: `[]`
     - `obd_evidence`: `[]`
     - `base_weight`: 0.75
     - `competition_group`: `"charging_system"`
     - `confidence_ceiling`: **0.85** (matches OV-002 precedent)
     - `passes_cases`: `["NEW-charging_system-01", "NEW-charging_system-02"]`
     - `source_wiki_refs`: `["DTC_VOCABULARY §15"]`

   - **CS-002** — Charging-induced ghost misfire.
     - `dtc_evidence`:
       - `{dtc_codes: ["P0562", "P0563"], strategy: "any_match", tier: "GATING", wiki_ref: "DTC_VOCABULARY §15"}` — a charging DTC must be present (discriminator from MF-004)
       - `{dtc_codes: ["P0300"], strategy: "any_match", tier: "SUGGESTIVE", wiki_ref: "DTC_VOCABULARY §15"}` — P0300 random misfire as supporting evidence
     - `chemistry_evidence`: `[{state: "NORMAL_OPERATION", tier: "GATING", wiki_ref: "GAS_VOCABULARY §3"}]` — clean combustion is a precondition; this is the discriminator from MF-004
     - `obd_evidence`: `[]`
     - `base_weight`: 0.70
     - `competition_group`: `"charging_system"`
     - `confidence_ceiling`: **0.75** (one notch above MF-004's 0.70 to dominate ghost-misfire ambiguity on NEW-charging_system-03)
     - `passes_cases`: `["NEW-charging_system-03"]`
     - `source_wiki_refs`: `["DTC_VOCABULARY §15", "GAS_VOCABULARY §3"]`

2. `registry/tests/test_charging_system_rules.py` — CREATE: targeted tests following the pattern in `test_vacuum_leak_rules.py`. Tests:
   - `test_file_exists` — file present
   - `test_valid_json` — parses
   - `test_ruleset_validates` — `RuleSet.model_validate` succeeds and `fault_family == FaultFamily.CHARGING_SYSTEM`
   - `test_exactly_two_rules` — exactly 2 rules (CS-001 + CS-002)
   - `test_no_duplicate_rule_ids`
   - `test_rule_ids_follow_pattern` — all match `^CS-00[12]$`
   - `test_every_rule_has_passes_cases` — every rule has ≥ 1 case
   - `test_every_passes_case_resolves` — every case ID in `passes_cases` appears in `corpus_curated.csv`
   - `test_every_rule_has_confidence_ceiling`
   - `test_every_rule_is_dtc_gated` — every rule has at least one `DTCEvidence` with `tier == GATING` and `strategy == "any_match"`
   - `test_cs_001_dtc_codes` — CS-001's single GATING DTC entry has `dtc_codes == ["P0562", "P0563"]`
   - `test_cs_001_no_chemistry` — CS-001 has empty `chemistry_evidence` and empty `obd_evidence`
   - `test_cs_001_ceiling_matches_overheating_precedent` — CS-001 ceiling is 0.85 (matches OV-002)
   - `test_cs_002_has_two_dtc_entries` — CS-002 has exactly 2 `DTCEvidence` entries
   - `test_cs_002_charging_dtc_gating` — CS-002's GATING entry has `dtc_codes == ["P0562", "P0563"]`
   - `test_cs_002_p0300_suggestive` — CS-002's SUGGESTIVE entry has `dtc_codes == ["P0300"]`
   - `test_cs_002_chemistry_normal_gating` — CS-002 has exactly one `ChemistryEvidence`: `NORMAL_OPERATION` at tier `GATING`
   - `test_cs_002_ceiling_dominates_mf_004` — CS-002 ceiling (0.75) is strictly greater than MF-004's ceiling (0.70) read from `rules/misfire.json`
   - `test_competition_group_charging_system` — every rule's `competition_group == "charging_system"`
   - `test_no_routing_tag_added` — `DTCRoutingTag` enum still has exactly 20 members; guards against unauthorised mirror drift
   - `test_no_unauthorised_dtc_codes` — only P0562, P0563, P0300 appear in any DTCEvidence across the file (P062x family explicitly forbidden as it is not in DTC_VOCABULARY §15)

3. `registry/corpus_curated.csv` — MODIFY: populate the 3 NEW-charging_system placeholder rows (case IDs NEW-charging_system-01 through -03) with realistic values per the severity profiles above. Fill: idle gas columns (`hc`, `co`, `co2`, `o2`, `nox`, `lambda_analyser`), OBD columns (`map`, `rpm`, `ect`, `dtcs`), 2500 RPM gas columns (`hc_2500`, `co_2500`, `co2_2500`, `o2_2500`, `nox_2500`, `lambda_2500`), and `description` (one-line summary noting the observed battery voltage value that the schema does not capture). Leave fuel-trim columns (`stft_b1`, `ltft_b1`, etc.), MAF, vehicle_speed, fuel_pressure, ff_*, vin_* as blank unless required by rule evidence (none are required under the DTC-only design).

4. `registry/corpus_meta.json` — MODIFY: update the 3 NEW-charging_system entries' `notes` field from "Placeholder case. To be populated with real gas/OBD values during REG-V2-AUTHOR-charging_system." to "Populated during REG-V2-AUTHOR-charging_system — <one-line severity description>."

### Files to touch ###

- `registry/rules/charging_system.json` (CREATE)
- `registry/tests/test_charging_system_rules.py` (CREATE)
- `registry/corpus_curated.csv` (MODIFY — 3 rows only, NEW-charging_system-01 through -03)
- `registry/corpus_meta.json` (MODIFY — 3 entries only, notes field)

### Out of scope ###

- Adding any DTC codes outside `DTC_VOCABULARY §15` — explicitly P0620–P0626 (generator/regulator) are excluded because they are not in the wiki; if they need to enter the registry, that is a wiki-update task plus a follow-up REG-V2-AUTHOR-charging_system-v2
- Adding `battery_voltage_v` to `OBDEvidence` or a `battery_v` column to `corpus_curated.csv` — would be a separate REG-V2-SCHEMA-* and corpus-migration task; deferred per JAEGER plan §10 addendum
- Adding `ELECTRICAL_HISTORY` (or any other value) to `DTCRoutingTag` — rules use raw `dtc_codes`; the routing-tag enum is a coordinated mirror of DTCLab and is not modified by registry-authoring tasks
- Conditional `confidence_ceiling` — `Rule.confidence_ceiling` is one fixed `float | None`; the rule-split design (CS-001 vs CS-002 with different fixed ceilings) encodes the conditional logic under the existing schema
- Indirect-only (no-DTC) charging-system detection — would require either battery-voltage corpus expansion or a new idle-rpm-variance PID, neither of which exists today
- Modifications to `rules/misfire.json` — MF-004 is **frozen**; competition with CS-002 is handled entirely on the CS-002 side via the double-GATING + ceiling-0.75 pattern
- Modifications to `rules/ecu_fault.json` — EF-001..005 are frozen; the wiki's routing of P0562/P0563 to `ECU_INTERNAL_HISTORY` is an observation about DTCLab's routing tag, not a rule-level overlap (no EF rule gates on P0562 or P0563 specifically per `rules/ecu_fault.json` review)
- Any Python evaluation logic — rules are JSON data; the only Python touched in this workstream is the new test file
- Harness side-by-side or integration shim — those belong to REG-V2-INTEGRATE
- Cross-family overlap with vacuum_leak, overheating, sensor_fault — independently authored and tested
- Verification of COMLab router's missing-chemistry semantics — the registry is self-contained and cannot inspect `COMLab/comlab/core/fault_atlas_router.py`; the CS-002 NORMAL_OPERATION-GATING design assumes hard-absence semantics ("missing chemistry ⇒ rule does not fire") rather than imputation ("missing chemistry ⇒ default to NORMAL_OPERATION"). This assumption is logged as a REG-V2-INTEGRATE verification gate (an "Unplanned follow-ups" row will be added to `REGISTRY_PROGRESS.md` at task close) and is **not** verifiable in this task.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/tests/test_charging_system_rules.py --fix
pyright registry/tests/test_charging_system_rules.py

# Existing tests must still pass — MF-004 is NOT modified
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
pytest registry/tests/test_non_starter_rules.py -x -q
pytest registry/tests/test_vacuum_leak_rules.py -x -q
pytest registry/tests/test_overheating_rules.py -x -q

# Inner loop — JSON rule file
python3.14 -c "import json; json.load(open('registry/rules/charging_system.json'))" && echo "json-ok"
python3.14 -c "import pathlib, json; from registry.schema_v2 import RuleSet; \
  data = json.loads(pathlib.Path('registry/rules/charging_system.json').read_text()); \
  rs = RuleSet.model_validate(data); \
  print(f'Validated: {len(rs.rules)} rules in family {rs.fault_family.value}')"

# Case-ID resolution
python3.14 -c "
import csv, json, pathlib
cases = set()
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        cases.add(row['case_id'])
rules = json.loads(pathlib.Path('registry/rules/charging_system.json').read_text())
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

# Verify 3 curated cases now have populated values
python3.14 -c "
import csv
with open('registry/corpus_curated.csv', newline='') as f:
    for row in csv.DictReader(f):
        if row['case_id'].startswith('NEW-charging_system'):
            assert row['hc'], f'{row[\"case_id\"]}: hc is blank'
            assert row['lambda_analyser'], f'{row[\"case_id\"]}: lambda_analyser is blank'
            assert row['lambda_2500'], f'{row[\"case_id\"]}: lambda_2500 is blank'
            assert row['dtcs'], f'{row[\"case_id\"]}: dtcs is blank'
            assert row['ect'], f'{row[\"case_id\"]}: ect is blank'
            assert row['rpm'], f'{row[\"case_id\"]}: rpm is blank'
    print('All 3 charging_system cases have populated values')
"

# Schema mirror invariant — DTCRoutingTag count unchanged at 20
python3.14 -c "
from registry.schema_v2 import DTCRoutingTag
n = len(list(DTCRoutingTag))
assert n == 20, f'DTCRoutingTag has {n} members, expected 20 (mirror invariant broken)'
print(f'DTCRoutingTag mirror intact: {n} members')
"

# Wiki-grounding invariant — only P0562/P0563/P0300 appear in DTCEvidence
python3.14 -c "
import json, pathlib, re
data = json.loads(pathlib.Path('registry/rules/charging_system.json').read_text())
allowed = {'P0562', 'P0563', 'P0300'}
seen = set()
for r in data['rules']:
    for de in r.get('dtc_evidence', []):
        for code in de['dtc_codes']:
            seen.add(code)
extra = seen - allowed
assert not extra, f'Unauthorised DTC codes in charging_system rules: {sorted(extra)} (only P0562/P0563/P0300 grounded in DTC_VOCABULARY §15)'
print(f'All DTC codes wiki-grounded: {sorted(seen)}')
"

# Targeted tests
pytest registry/tests/test_charging_system_rules.py -x -q

# Full regression — all registry tests
pytest registry/tests/ -x -q
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-AUTHOR-charging_system`: Status=done, Files changed=4, Verification="{HEADLINE}"
