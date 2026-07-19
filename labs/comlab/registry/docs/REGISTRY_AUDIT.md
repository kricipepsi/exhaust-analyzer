# REGISTRY AUDIT — v1 Rule Inventory and Patch-vs-Rebuild Decision

**Generated:** 2026-05-27
**Inputs:**
- `COMLab/comlab/config/global_fault_registry.json` (53 executable rule registrations)
- `COMLab/comlab/config/kg/*.json` (58 knowledge graph nodes across 12 families)
- `registry/corpus_curated.csv` (252 curated cases)
- `registry/CORPUS_AUDIT.md` (AUDIT-CORPUS deliverable)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md`
- `COMLab/comlab/core/fault_atlas_router.py` (routing/pruning/scoring logic)

---

## 1. Executive Summary

The v1 rule set consists of **53 executable rule registrations** (in `global_fault_registry.json`) backed by **58 knowledge-graph nodes** (in `config/kg/*.json`). The KG nodes are repair documentation — they carry fault descriptions, remediation steps, and differential-sibling links but contain no routing logic. The executable rules are chemistry-gated: each rule's `cross_domain_matrix.gas_lab_state` field acts as a mandatory gate key. If GASLab does not emit that exact chemistry state for a case, the rule is pruned before evaluation.

**Root cause of the 60% prune rate:** Only 11 unique `gas_lab_state` values exist across all 53 rules. The curated corpus spans 13 fault families with diverse chemistry signatures — many cases produce states that match zero rules. Additionally, 24 of 53 rules use `REQUIRE_MATCH` or `REQUIRE_DTC` DTC fallback strategies, meaning they are pruned when the expected DTC is absent even if the chemistry gate passes.

**Decision: REBUILD v2.** The v1 architecture is fundamentally un-patchable. Individual prune-condition tweaks would recover some cases but cannot address the core flaw: chemistry states are hard-coded gate keys rather than evidence-tier weights. A rebuild with an evidence-tier model (definitive / suggestive / gating) plus rule competition groups and confidence ceilings is required to cover the full curated corpus.

---

## 2. Rule Inventory

### 2.1 KG Nodes by Fault Family (58 total)

These are the repair-knowledge nodes in `COMLab/comlab/config/kg/`. They are NOT executable rules — they carry documentation, remediation steps, and differential-sibling links. The executable rules in `global_fault_registry.json` reference them by `fault_id`.

| Family | File | Node IDs | Count |
|---|---|---|---|
| `lean_condition` | `lean_condition.json` | ERR-LC-001 through ERR-LC-007 | 7 |
| `rich_mixture` | `rich_mixture.json` | ERR-RM-001 through ERR-RM-007 | 7 |
| `misfire` | `misfire.json` | ERR-MF-001 through ERR-MF-007 | 7 |
| `catalyst_failure` | `catalyst_failure.json` | ERR-CF-001 through ERR-CF-007 | 7 |
| `exhaust_leak` | `exhaust_leak.json` | ERR-EL-001 through ERR-EL-006 | 6 |
| `sensor_fault` | `sensor_fault.json` | ERR-SF-001 through ERR-SF-006 | 6 |
| `mechanical_wear` | `mechanical_wear.json` | ERR-MW-001 through ERR-MW-006 | 6 |
| `cam_timing` | `cam_timing.json` | ERR-CT-001 through ERR-CT-005 | 5 |
| `ignition_fault` | `ignition_fault.json` | ERR-IF-001 through ERR-IF-003 | 3 |
| `ecu_fault` | `ecu_fault.json` | ERR-EF-001, ERR-EF-002 | 2 |
| `non_starter` | `non_starter.json` | ERR-NS-004 | 1 |
| `no_fault` | `no_fault.json` | OPTIMAL_HEALTH | 1 |
| **Total** | | | **58** |

### 2.2 Executable Rule Registrations (53 total)

Each entry in `global_fault_registry.json` maps a `fault_id` to a `cross_domain_matrix` that gates on chemistry state + OBD PIDs + DTCs. Some fault_ids appear multiple times with different gating conditions (e.g., ERR-LC-004 appears for both LEAN_MIXTURE and LEAN_MISFIRE).

#### Chemistry States Used (11 unique)

| gas_lab_state | Rules using it | Curated families addressed |
|---|---|---|
| `LEAN_MIXTURE` | 4 (ERR-LC-001, ERR-LC-003, ERR-LC-004×2) | lean_condition |
| `LEAN_MISFIRE` | 3 (ERR-LC-004, ERR-MF-003, ERR-MF-005, ERR-MF-007) | lean_condition, misfire |
| `RICH_MIXTURE` | 5 (ERR-RM-003, ERR-RM-004, ERR-RM-005, ERR-RM-006, ERR-RM-007) | rich_mixture |
| `RICH_MISFIRE` | 1 (ERR-MF-002) | misfire (rich variant) |
| `IGNITION_MISFIRE` | 6 (ERR-E2-I104, ERR-IF-001, ERR-IF-002, ERR-IF-003, ERR-MF-002, ERR-MF-004, ERR-MF-006, ERR-CT-002) | misfire, ignition_fault, cam_timing |
| `INCOMPLETE_OXIDATION` | 0 (starter rule ERR-E1-M032 only — legacy, no KG node) | lean_condition (EGR-specific) |
| `INCOMPLETE_COMBUSTION` | 3 (ERR-MW-001, ERR-MW-005, ERR-NS-004) | mechanical_wear, non_starter |
| `CATALYST_OVERWHELMED` | 5 (ERR-CF-001, ERR-CF-002, ERR-CF-003, ERR-CF-004, ERR-CF-005 subset) | catalyst_failure |
| `CATALYST_NOT_LIGHTING_OFF` | 1 (ERR-CF-007) | catalyst_failure |
| `NORMAL_OPERATION` | 4 (ERR-CF-005, ERR-EL-004, ERR-CT-005, ERR-SF-001×2, ERR-SF-002) | catalyst_failure (masking), exhaust_leak, cam_timing, sensor_fault |
| `EXHAUST_AIR_LEAK` | 5 (ERR-EL-001, ERR-EL-002, ERR-EL-003, ERR-EL-005, ERR-EL-006) | exhaust_leak |
| `POA_SIGNATURE` | 3 (ERR-CF-006, ERR-RM-001, ERR-RM-002) | catalyst_failure, rich_mixture |
| `WORN_PISTON_RINGS` | 1 (ERR-MW-003) | mechanical_wear |
| `WORN_VALVE_SEALS` | 1 (ERR-MW-004) | mechanical_wear |
| `WORN_ENGINE` | 1 (ERR-MW-006) | mechanical_wear |
| `WRONG_VALVE_TIMING` | 2 (ERR-CT-001, ERR-CT-003) | cam_timing |
| `VVT_FAILURE` | 2 (ERR-CT-003, ERR-CT-004) | cam_timing |
| `COOLANT_LEAK_INTERNAL` | 1 (ERR-MW-002) | mechanical_wear |
| `GDI_HPFP_INTERNAL_SEAL_LEAK` | 1 (ERR-E3-F501) | rich_mixture (GDI only) |

Note: The Jaeger analysis identified `TIMING_RETARDED`, `SAMPLE_INVALID`, `WORN_PISTON_RINGS`, `VVT_FAILURE`, and `RICH_MIXTURE` as the 5 most common chemistries in failing traces. Of these, only `WORN_PISTON_RINGS` and `VVT_FAILURE` exist as named gas_lab_state values. `TIMING_RETARDED` and `SAMPLE_INVALID` have zero matching rules — these cases are guaranteed to prune.

#### DTC Fallback Strategies

| Strategy | Count | Effect |
|---|---|---|
| `PROCEED_ON_MATCH_OR_EMPTY` | 26 | Rule fires if DTC matches OR if no DTCs present |
| `REQUIRE_MATCH` | 14 | Rule pruned if required DTC absent |
| `GAS_ONLY` | 10 | No DTC gating — chemistry-only |
| `REQUIRE_DTC` | 3 | Rule pruned if any DTC absent (stricter than REQUIRE_MATCH) |

**24 of 53 rules require at least one DTC match.** This is a significant prune contributor for cases that present the correct chemistry but lack the specific DTC the rule expects.

### 2.3 Full Rule Registration Table

| # | fault_id | gas_lab_state | DTC strategy | base_weight | OBD constraints | preconditions | perception_flag |
|---|---|---|---|---|---|---|---|
| 1 | ERR-E1-M032 | INCOMPLETE_OXIDATION | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | manifold_vacuum_kpa IN_RANGE [30,50] | — | — |
| 2 | ERR-E2-I104 | IGNITION_MISFIRE | REQUIRE_MATCH | 0.70 | shrtft1 > 15.0 | — | — |
| 3 | ERR-E3-F501 | GDI_HPFP_INTERNAL_SEAL_LEAK | PROCEED_ON_MATCH_OR_EMPTY | 0.90 | longft1 ≤ -23.0 | — | — |
| 4 | ERR-CF-001 | CATALYST_OVERWHELMED | REQUIRE_MATCH | 0.80 | o2_b1s2_v > 0.6 | — | — |
| 5 | ERR-CF-002 | CATALYST_OVERWHELMED | REQUIRE_MATCH | 0.90 | calc_load_pct > 60.0 | — | — |
| 6 | ERR-CF-003 | CATALYST_OVERWHELMED | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | map_kpa > 75.0 | — | — |
| 7 | ERR-CF-004 | CATALYST_OVERWHELMED | REQUIRE_MATCH | 0.90 | o2_b1s2_v IN_RANGE [0.4,0.5] | — | — |
| 8 | ERR-CF-005 | NORMAL_OPERATION | GAS_ONLY | 0.75 | longft1 ≤ -10.0 | — | — |
| 9 | ERR-CF-006 | POA_SIGNATURE | REQUIRE_MATCH | 0.80 | longft1 ≥ -10.0 | — | — |
| 10 | ERR-CF-007 | CATALYST_NOT_LIGHTING_OFF | PROCEED_ON_MATCH_OR_EMPTY | 0.70 | ect_c < 75.0 | — | — |
| 11 | ERR-EL-001 | EXHAUST_AIR_LEAK | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | longft1 ≥ 10.0 | — | — |
| 12 | ERR-EL-002 | EXHAUST_AIR_LEAK | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | longft1 ≥ 8.0 | — | — |
| 13 | ERR-EL-003 | EXHAUST_AIR_LEAK | PROCEED_ON_MATCH_OR_EMPTY | 0.70 | longft1 ≥ 5.0 | — | — |
| 14 | ERR-EL-004 | NORMAL_OPERATION | GAS_ONLY | 0.55 | (none) | — | — |
| 15 | ERR-EL-005 | EXHAUST_AIR_LEAK | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | longft1 ≥ 5.0 | — | — |
| 16 | ERR-EL-006 | EXHAUST_AIR_LEAK | GAS_ONLY | 0.60 | (none) | — | — |
| 17 | ERR-IF-001 | IGNITION_MISFIRE | REQUIRE_MATCH | 0.85 | shrtft1 > 15.0 | — | — |
| 18 | ERR-IF-002 | IGNITION_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.70 | shrtft1 > 10.0 | — | — |
| 19 | ERR-IF-003 | IGNITION_MISFIRE | REQUIRE_MATCH | 0.80 | shrtft1 > 12.0 | — | — |
| 20 | ERR-MW-001 | INCOMPLETE_COMBUSTION | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | (none) | — | — |
| 21 | ERR-MW-002 | COOLANT_LEAK_INTERNAL | PROCEED_ON_MATCH_OR_EMPTY | 0.90 | ect_c > 90.0 | — | — |
| 22 | ERR-MW-003 | WORN_PISTON_RINGS | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | shrtft1 IN_RANGE [-10,10] | — | — |
| 23 | ERR-MW-004 | WORN_VALVE_SEALS | GAS_ONLY | 0.70 | (none) | — | — |
| 24 | ERR-MW-005 | INCOMPLETE_COMBUSTION | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | map_kpa < 30.0 | — | — |
| 25 | ERR-MW-006 | WORN_ENGINE | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | (none) | — | — |
| 26 | ERR-CT-001 | WRONG_VALVE_TIMING | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | map_kpa < 30.0 | — | — |
| 27 | ERR-CT-002 | IGNITION_MISFIRE | REQUIRE_MATCH | 0.75 | shrtft1 IN_RANGE [-10,10] | vvt_equipped: true | — |
| 28 | ERR-CT-003 | WRONG_VALVE_TIMING | REQUIRE_MATCH | 0.80 | shrtft1 > 5.0 | vvt_equipped: true | — |
| 29 | ERR-CT-004 | VVT_FAILURE | GAS_ONLY | 0.55 | (none) | vvt_equipped: true | — |
| 30 | ERR-CT-005 | NORMAL_OPERATION | REQUIRE_MATCH | 0.80 | (none) | vvt_equipped: true | — |
| 31 | ERR-NS-004 | INCOMPLETE_COMBUSTION | GAS_ONLY | 0.60 | (none) | — | — |
| 32 | ERR-LC-001 | LEAN_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | shrtft1 > 15.0 | — | — |
| 33 | ERR-LC-003 | LEAN_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | shrtft1 > 10.0 | — | — |
| 34 | ERR-LC-004 | LEAN_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | shrtft1 > 10.0 | — | — |
| 35 | ERR-LC-004 | LEAN_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | shrtft1 > 10.0 | — | — |
| 36 | ERR-RM-001 | POA_SIGNATURE | GAS_ONLY | 0.75 | (none) | — | — |
| 37 | ERR-RM-002 | POA_SIGNATURE | GAS_ONLY | 0.70 | (none) | — | — |
| 38 | ERR-RM-003 | RICH_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | longft1 ≤ -15.0 | — | — |
| 39 | ERR-RM-004 | RICH_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | longft1 ≤ -12.0 | — | — |
| 40 | ERR-RM-005 | RICH_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | longft1 ≤ -23.0 | — | — |
| 41 | ERR-RM-006 | RICH_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.70 | longft1 ≤ -10.0 | — | — |
| 42 | ERR-RM-007 | RICH_MIXTURE | PROCEED_ON_MATCH_OR_EMPTY | 0.85 | longft1 ≤ -20.0 | — | — |
| 43 | ERR-MF-002 | IGNITION_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | shrtft1 > 5.0 | — | — |
| 44 | ERR-MF-003 | LEAN_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | shrtft1 > 5.0 | — | — |
| 45 | ERR-MF-004 | IGNITION_MISFIRE | REQUIRE_MATCH | 0.85 | shrtft1 > 15.0 | — | — |
| 46 | ERR-MF-005 | LEAN_MISFIRE | REQUIRE_MATCH | 0.85 | shrtft1 > 15.0 | — | — |
| 47 | ERR-MF-006 | IGNITION_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.70 | (none) | — | — |
| 48 | ERR-MF-007 | LEAN_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | shrtft1 > 5.0 | fuel_delivery_type: GDI | — |
| 49 | ERR-MF-002 | RICH_MISFIRE | PROCEED_ON_MATCH_OR_EMPTY | 0.75 | longft1 ≤ -5.0 | — | — |
| 50 | ERR-CT-003 | VVT_FAILURE | PROCEED_ON_MATCH_OR_EMPTY | 0.80 | (none) | — | — |
| 51 | ERR-SF-002 | NORMAL_OPERATION | REQUIRE_MATCH | 0.85 | (none) | — | — |
| 52 | ERR-SF-001 | NORMAL_OPERATION | GAS_ONLY | 0.70 | (none) | — | O2_SENSOR_BIASED_HIGH |
| 53 | ERR-SF-001 | NORMAL_OPERATION | GAS_ONLY | 0.70 | (none) | — | O2_SENSOR_BIASED_LOW |

### 2.4 KG Nodes Without Executable Rules (Orphan Nodes)

These KG nodes have no corresponding entry in `global_fault_registry.json` — they can never fire:

| KG Node | Family | Reason |
|---|---|---|
| ERR-LC-002 (maf_sensor_contaminated) | lean_condition | No registry entry |
| ERR-LC-005 (egr_stuck_open) | lean_condition | Covered by ERR-E1-M032 but not by its own fault_id |
| ERR-LC-006 (exhaust_leak_pre_upstream_o2) | lean_condition | No registry entry |
| ERR-LC-007 (secondary_air_injection_stuck_on) | lean_condition | No registry entry |
| ERR-MF-001 (coil_on_plug_insulation_arc) | misfire | Covered by ERR-E2-I104 but not by its own fault_id |
| ERR-EF-001 (fuel_trim_saturated) | ecu_fault | No registry entry |
| ERR-EF-002 (closed_loop_fuel_control_disabled) | ecu_fault | No registry entry |
| ERR-SF-003 (maf_sensor_under_reading) | sensor_fault | No registry entry |
| ERR-SF-004 (map_sensor_calibration_drift) | sensor_fault | No registry entry |
| ERR-SF-005 (coolant_temp_sensor_stuck_cold) | sensor_fault | No registry entry |
| ERR-SF-006 (downstream_o2_sensor_contaminated) | sensor_fault | No registry entry |
| OPTIMAL_HEALTH | no_fault | Handled as sentinel in router, not via registry |

**12 of 58 KG nodes (21%) are unreachable.** The `ecu_fault` family has zero working rules — both its KG nodes are orphans. The `sensor_fault` family has only ERR-SF-001 and ERR-SF-002 active; the other 4 nodes are unreachable.

---

## 3. Firing Matrix

### 3.1 Per-Family Rule Coverage Against Curated Corpus

Based on CORPUS_AUDIT.md §5.1 per-case v1 behavior data and the rule inventory above:

| Fault Family | Curated Cases | Rules with Matching Chemistry | Rules Active (non-orphan) | v1 Behavior | Assessment |
|---|---|---|---|---|---|
| `lean_condition` | 53 | 5 (LEAN_MIXTURE + LEAN_MISFIRE) | 4 (ERR-LC-001, 003, 004×2) | Most cases: MISMATCH → no_fault | Only 4 rules for 53 cases; 2 are the same fault_id. Missing ERR-LC-002 (MAF contamination — the most common real-world lean cause). |
| `misfire` | 44 | 10 (IGNITION_MISFIRE, LEAN_MISFIRE, RICH_MISFIRE) | 8 (plus 3 via ERR-IF-*) | 29 cases: DTCLab enum crash. Rest: wrong family or no_fault. | 30 pipeline-bug cases will recover post FIX-ENUM-1. Remaining 14 need better routing. Missing the most common misfire KG node (ERR-MF-001). |
| `ecu_fault` | 28 | 0 | **0** | All 28: MISMATCH → no_fault | **Zero executable rules.** Both KG nodes (ERR-EF-001, ERR-EF-002) are orphans. This is the single largest gap. |
| `rich_mixture` | 23 | 7 (RICH_MIXTURE + POA_SIGNATURE) | 7 | Most: MISMATCH → no_fault | Rules exist but chemistry gating fails for non-POA rich cases. |
| `catalyst_failure` | 21 | 7 (CATALYST_OVERWHELMED, NORMAL_OPERATION, POA_SIGNATURE, CATALYST_NOT_LIGHTING_OFF) | 7 | Most: MISMATCH → no_fault | 5 of 7 rules require CATALYST_OVERWHELMED. Cases with marginal catalysts that don't trigger this state are uncovered. |
| `sensor_fault` | 20 | 3 (NORMAL_OPERATION) | 3 (ERR-SF-001×2, ERR-SF-002) | Mixed. Some PASS, most MISMATCH. | Only O2 sensor faults executable. MAF, MAP, ECT, and downstream O2 sensor rules are all orphans. |
| `no_fault` | 17 | — | 0 (sentinel via router) | 15 PASS or not in run window. | Healthy baseline cases. Prune failure on 60% of disease cases sends them here incorrectly. |
| `mechanical_wear` | 11 | 6 (INCOMPLETE_COMBUSTION, COOLANT_LEAK_INTERNAL, WORN_PISTON_RINGS, WORN_VALVE_SEALS, WORN_ENGINE) | 6 | Most: MISMATCH → wrong family | Rules exist but cross-family confusion common (lean vs mechanical_wear overlap). |
| `cam_timing` | 9 | 5 (WRONG_VALVE_TIMING, IGNITION_MISFIRE, VVT_FAILURE, NORMAL_OPERATION) | 5 | Mixed. Some PASS, most MISMATCH. | 4 of 5 rules require vvt_equipped precondition. Non-VVT engines have 1 rule. |
| `exhaust_leak` | 5 | 6 (EXHAUST_AIR_LEAK, NORMAL_OPERATION) | 6 | Most: MISMATCH → no_fault | More rules than cases, but chemistry gating mismatches. ERR-EL-004 fires on NORMAL_OPERATION — likely false positives on healthy cases. |
| `non_starter` | 4 | 1 (INCOMPLETE_COMBUSTION) | 1 | 2 pipeline-bug (GASLab HC bounds), 2 MISMATCH. | Single rule. REAL-001/003 will recover post FIX-GAS-1. |
| `ignition_fault` | 3 | 3 (IGNITION_MISFIRE) | 3 | Most: MISMATCH → no_fault | All 3 rules require DTC matches. DTC-less cases uncovered. |
| `invalid_input` | 2 | 0 | 0 | 1 sentinel-keep (case_011), 1 covered. | Sentinel cases are expected to fail — explicit validation test. |

### 3.2 Prune Analysis by Chemistry State

From the Jaeger analysis, the 5 most common chemistries in failing traces and their rule coverage:

| Chemistry (from Jaeger) | Cases | Matching rules | Prune reason |
|---|---|---|---|
| `TIMING_RETARDED` | 64 | 0 | **No rule registers this chemistry state.** Guaranteed 100% prune. |
| `SAMPLE_INVALID` | 17 | 0 | **No rule registers this chemistry state.** Guaranteed 100% prune. |
| `WORN_PISTON_RINGS` | (in top 5) | 1 (ERR-MW-003) | Chemistry gate passes but shrtft1 must be IN_RANGE [-10,10] — fails if trims are outside. |
| `VVT_FAILURE` | 10 | 2 (ERR-CT-003, ERR-CT-004) | ERR-CT-003 requires vvt_equipped + P0014/P0024 DTC. ERR-CT-004 is GAS_ONLY but at 0.55 confidence. |
| `RICH_MIXTURE` | (in top 5) | 5 | Chemistry gate passes but all require specific longft1 thresholds and may face DTC gating. |

**Two of the five most-frequent chemistries have zero matching rules.** This alone accounts for 81 of the 239 failing cases (34%). Combined with orphan KG nodes (especially all of ecu_fault, 28 cases), the prune bottleneck is a direct consequence of the chemistry-gated architecture.

---

## 4. Patch vs Rebuild Decision

### 4.1 What a Patch Would Look Like

A patch strategy would:
1. Add missing chemistry states to existing rules (e.g., add `TIMING_RETARDED` entries)
2. Create registry entries for the 12 orphan KG nodes
3. Relax DTC gating on rules where chemistry evidence is strong
4. Add rules for the uncovered families (ecu_fault, sensor_fault variants)

**Estimated effort:** 8–12 sessions. Each new chemistry-state registration is one JSON entry. Each orphan node needs a cross_domain_matrix designed against the curated corpus. The 12 orphans + 2 new chemistry states for existing rules + ecu_fault rules ≈ 25–30 new registry entries.

**Projected recovery:** 60–100 cases (of 203 comlab.aggregate failures). The patch would NOT fix:
- Cases where chemistry state is ambiguous between families (lean_condition vs mechanical_wear vs cam_timing overlap)
- Cases where the chemistry classifier itself produces wrong states
- Cases where rule competition is needed but no weight mechanism exists

**Projected ceiling:** ~40–50% accuracy on the curated corpus (up from ~17-18%), limited by the fundamental architecture.

### 4.2 What a Rebuild Looks Like

A rebuild strategy (per `JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10):
1. Define v2 schema with evidence tiers (definitive / suggestive / gating)
2. Replace chemistry-state gating with evidence-weighted scoring
3. Add rule competition groups (≥2 rules per family per chemistry signature)
4. Add confidence ceilings for solo-survivor and cold-engine scenarios
5. Author all rules as JSON data, one family per session
6. Wire v2 in parallel with v1 behind a flag; cut over when v2 ≥ v1 on curated corpus

**Estimated effort:** 17 sessions (AUDIT-CHEM + REG-V2-SCHEMA + 13 family authoring sessions + REG-V2-INTEGRATE)

**Projected ceiling:** ≥75% on curated corpus (per plan §10.4), with architectural headroom for further improvement.

### 4.3 Decision: REBUILD

The v1 architecture has three fatal flaws that cannot be patched:

1. **Chemistry-state-as-gate:** The `gas_lab_state` field is a mandatory gate. Cases whose chemistry doesn't produce one of 11 pre-registered states are guaranteed to fail. The plan's §10 already identifies this as the v2 pivot — evidence tiers replace hard gates.

2. **Orphan knowledge:** 12 of 58 KG nodes (21%) have no executable path. The entire `ecu_fault` family (28 curated cases, the third-largest) has zero working rules. These aren't edge cases — they're core diagnostic categories.

3. **No competition mechanism:** Rules fire in isolation. When a chemistry state matches only one rule, that rule wins by default with no confidence penalty. When multiple rules fire, there's no weight model to resolve ambiguity. The plan's FIX-SCORE-SOLO-1 and competition groups address this.

The rebuild starts from a stronger foundation: a 252-case curated corpus with known ground truth, 58 well-written KG nodes that contain excellent repair documentation, and a proven Jaeger observability pipeline to measure progress. The v1 KG nodes are reusable — v2 rules reference the same fault_ids with new evidence-tier wrappers.

**The patch path is not shorter.** It requires designing ad-hoc chemistry-state additions that would be thrown away at v2 cutover. The rebuild produces a schema that every future rule shares, turning 25–30 one-off JSON edits into 13 structured authoring sessions against a validated template.

---

## 5. Bottom Line

| Metric | Value |
|---|---|
| v1 executable rules | 53 registry entries in `global_fault_registry.json` |
| v1 KG nodes | 58 (12 orphan — 21% unreachable) |
| Unique chemistry states gating rules | 11 |
| Rules requiring DTC match | 24 (45%) |
| Families with zero executable rules | 1 (`ecu_fault` — 28 curated cases) |
| Top 2 failing chemistries with zero rules | `TIMING_RETARDED` (64 cases), `SAMPLE_INVALID` (17 cases) |
| v1 accuracy on curated corpus (projected) | ~17–18% (42 PASS / ~240 evaluable) |
| Patch ceiling (projected) | ~40–50% |
| Rebuild target | ≥75% |
| **Decision** | **REBUILD v2** |

The rebuild proceeds to AUDIT-CHEM (chemistry × fault-family matrix), then REG-V2-SCHEMA (evidence-tier model), then one REG-V2-AUTHOR-{family} session per fault family.

---

*End of REGISTRY_AUDIT.md*
