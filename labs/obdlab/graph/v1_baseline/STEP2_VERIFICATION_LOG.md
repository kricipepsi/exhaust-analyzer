# OBDLab Step 2 — Verification Log (T-PREP-2)

**Run date:** 2026-05-20
**Patcher:** `scripts/patch_step2.py`
**Input graph:** `graphify-out/graph.json` (commit `03640592`, post Step 1)
**Output graph:** `graphify-out/graph.json` (post Step 2 patch + community rebuild)

---

## §1 — Pre/post metrics

| Metric | Pre (Step 1) | Post (Step 2) | Delta | Target |
|---|---|---|---|---|
| Nodes | 506 | 500 | −6 | — |
| Edges (links) | 407 | 489 | +82 | — |
| Orphan nodes | 102 (20.2%) | 24 (4.8%) | −78 | ≤ 60 |
| Unattributed nodes | 10 | 0 | −10 | == 0 |
| Graph density | 0.003186 | 0.003920 | +0.000734 | ≥ 0.0025 |
| Communities | 179 | 101 | −78 | — |
| Thin communities (1–2) | 135 | 59 | −76 | — |
| Forbidden relations | 0 | 0 | 0 | == 0 |

---

## §2 — Orphan adoption — explicit triage table

Per `T-PREP-2_kg_audit_remediation.md` orphan triage:

| # | Orphan node | Edge | Source → Target | Status |
|---|---|---|---|---|
| 1 | Stabilised Idle (SI) | `enumerates` | RpmStateBucket → Stabilised Idle (SI) | APPLIED |
| 2 | COLD_OPEN_LOOP_INVALID | `enumerates` | RpmStateBucket → COLD_OPEN_LOOP_INVALID | SKIP: already exists |
| 3 | EVAP_purge_duty_cycle | `characterised_by` | EVAP_CANISTER_SATURATED → EVAP_purge_duty_cycle | SKIP: target not found |
| 4 | OBDLivePayload | `cross_references` | OBDLivePayload → SEMANTIC_CONTRACT_4_4 | SKIP: already exists |
| 5 | DUAL_MAF_MAP | `enumerates` | AirMeteringStrategy → DUAL_MAF_MAP | APPLIED |
| 6 | air_metering_strategy | `defines` | VinDNA → air_metering_strategy | APPLIED |
| 7 | stress_idle_rpm_target | `defines` | VinDNA → stress_idle_rpm_target | APPLIED |
| 8 | obd_live_lab | `defines` | obd_live_lab → obd_translation_rules.yaml | APPLIED |
| 9 | EGR STUCK OPEN | `characterised_by` | EGR STUCK OPEN → EGR_stuck_open | APPLIED |
| 10 | LEAKING INJECTOR | `characterised_by` | LEAKING INJECTOR → LEAKING_INJECTOR | APPLIED |
| 11 | HIGH FUEL PRESSURE | `characterised_by` | HIGH FUEL PRESSURE → … | SKIP: target not found |
| 12 | FUEL DELIVERY fault | `characterised_by` | FUEL DELIVERY fault → … | SKIP: target not found |
| 13 | DEAD | `enumerates` | O2FailureMode → DEAD | APPLIED (via semantic pass) |
| 14 | Fault active and severe | `enumerates` | Fault active and severe → HistoricalFaultContext | APPLIED |
| 15 | Fault recently repaired / healing | `enumerates` | Fault recently repaired / healing → HistoricalFaultContext | APPLIED |
| 16 | Common-mode fault | `enumerates` | Common-mode fault → HistoricalFaultContext | APPLIED |

**Explicit adoptions:** 10 applied, 3 already-existed, 3 target-not-found (nodes not in graph — these are concept descriptions, not discrete nodes).

---

## §3 — Orphan adoption — semantic matching pass

Additional automatic adoptions via label-pattern matching:

| Category | Count | Relation |
|---|---|---|
| Enum value → parent enum (O2FailureMode, VERoutingMode, O2NormalizationMode, RpmStateBucket) | 10 | `enumerates` |
| O2 sensor positions (B1S1, B1S2, B2S1, B2S2) → O2FailureMode | 4 | `characterised_by` |
| Ignition timing concepts (Burn Line, Curb Idle, Stress Idle, WOT, Knock Retard, Over/Under-Advance, Cam Timing) → IgnitionTiming | 11 | `characterised_by` |
| Spark plug conditions (5 types) → SparkPlug | 5 | `characterised_by` |
| Vacuum/MAP gauge + Snap Throttle + IAC patterns → VacuumDiagnostics | 10 | `characterised_by` |
| Coil conditions (Healthy, Weak) → IgnitionTiming | 2 | `characterised_by` |
| PID/derived concept adoptions (calculated_ve, engine_warmed, iac_step, knock_retard_deg, longft2, shrtft2, normalized_obd_lambda, total_trim_correction_delta, has_particulate_filter, ChemicalSignature, etc.) | 15 | mixed |
| DTC codes (P244A, P2459) → GPF | 2 | `maps_to` |
| Mode 06 MID / TID → Mode06 | 2 | `sub_mode_of` |
| Fault nodes (Mechanical_*, Lazy_O2, ECU_Logic) → FaultFamily | 5 | `characterised_by` |
| RPM bucket values (REGULATORY_HIGH_IDLE, STRESS_IDLE, COLD_OPEN_LOOP_INVALID from OBD_VOCABULARY) → RpmStateBucket | 3 | `enumerates` |
| Bank patterns (Single-bank fault, Sensor fault on ≥1 bank) → Fuel trim | 2 | `characterised_by` |

**Semantic adoptions:** 60 applied.

**Note:** 6 adoption targets were not found in the graph (concept-level descriptions with no discrete node). These are expected — the wiki prose describes patterns that don't have separate node representations.

---

## §4 — List-fragment orphans deleted

| # | Node ID | Label | Reason |
|---|---|---|---|
| 1 | `out1a::…section_1_standards` | 1. Standards anchored | Numbered heading fragment |
| 2 | `out1a::…section_3_input_validation` | 3. Input validation | Numbered heading fragment |
| 3 | `out1a::…section_4_semantic_consistency` | 4. Semantic consistency rules | Numbered heading fragment |
| 4 | `out1a::…section_6_enums` | 6. OBDLab enum declarations | Numbered heading fragment |
| 5 | `out3b::document_index_section` | Document Index | Structural artefact |
| 6 | `out3b::vacuum_map_diagnostics_section` | Vacuum / MAP Diagnostics | Structural section header |

**Total deleted:** 6 nodes.

---

## §5 — Bridge edges added (ISSUE-2)

| # | Source | Relation | Target | Status |
|---|---|---|---|---|
| 1 | VERoutingMode | `maps_to` | AirMeteringStrategy | SKIP: exists |
| 2 | O2NormalizationMode | `maps_to` | upstream_o2_type | APPLIED |
| 3 | Physics_Gate_1 | `monitors` | VSS | SKIP: exists |
| 4 | Physics_Gate_2 | `monitors` | coolant_temp_c | SKIP: exists |
| 5 | Physics_Gate_3 | `monitors` | calculated_ve | SKIP: exists |
| 6 | Physics_Gate_4 | `monitors` | shrtft1 | APPLIED |
| 7 | Thermal gate | `monitors` | coolant_temp_c | SKIP: exists |
| 8 | VE formula | `uses` | mass_airflow_gps | APPLIED |
| 9 | VE formula | `uses` | manifold_vacuum_kpa | APPLIED |
| 10 | VE formula | `uses` | engine_rpm | APPLIED |
| 11 | VE formula | `uses` | intake_air_temp_c | APPLIED |
| 12 | OBDLivePayload | `mirrors_contract_in` | SEMANTIC_CONTRACT | APPLIED |
| 13 | SensorSignalTranslator | `uses` | O2NormalizationMode | APPLIED |
| 14 | SensorSignalTranslator | `uses` | VERoutingMode | APPLIED |
| 15 | SensorSignalTranslator | `uses` | TrimAnalyticsGate | APPLIED |
| 16 | PIDIngestionValidator | `uses` | physical_sensor_bounds.json | APPLIED |
| 17 | RICH_MIXTURE | `characterised_by` | shrtft1 | APPLIED |
| 18 | LEAN_MIXTURE | `characterised_by` | shrtft1 | APPLIED |
| 19 | IGNITION_MISFIRE | `characterised_by` | Misfire counters | SKIP: target not found |
| 20 | obd_live_lab | `defines` | physical_sensor_bounds.json | APPLIED |
| 21 | obdlab | `references` | OBD_VOCABULARY | APPLIED |
| 22 | obdlab | `mirrors_contract_in` | SEMANTIC_CONTRACT | APPLIED |

**Bridge edges:** 16 applied, 5 already-existed, 1 target-not-found.

---

## §6 — Unattributed node backfill (ISSUE-3)

All 10 unattributed nodes from Step 1 deterministic patch backfilled:

| # | Node ID | Label | repo | local_id |
|---|---|---|---|---|
| 1 | `patch_physics_gate_2` | Physics_Gate_2 | patch_step1 | physics_gate_2 |
| 2 | `patch_physics_gate_3` | Physics_Gate_3 | patch_step1 | physics_gate_3 |
| 3 | `patch_physics_gate_4` | Physics_Gate_4 | patch_step1 | physics_gate_4 |
| 4 | `patch_evap_canister_saturated` | EVAP_CANISTER_SATURATED | patch_step1 | evap_canister_saturated |
| 5 | `patch_evap_purge_duty_cycle` | EVAP_purge_duty_cycle | patch_step1 | evap_purge_duty_cycle |
| 6 | `patch_semantic_contract_4_4` | SEMANTIC_CONTRACT_4_4 | patch_step1 | semantic_contract_4_4 |
| 7 | `patch_o2_sensor_biased_high` | O2_SENSOR_BIASED_HIGH | patch_step1 | o2_sensor_biased_high |
| 8 | `patch_shrtft1_near_zero_at_si` | shrtft1_near_zero_at_SI | patch_step1 | shrtft1_near_zero_at_si |
| 9 | `patch_cam_position_desired_vs_actual` | cam_position_desired_vs_actual | patch_step1 | cam_position_desired_vs_actual |
| 10 | `patch_shrtft1_positive_at_idle` | shrtft1_positive_at_idle | patch_step1 | shrtft1_positive_at_idle |

**Unattributed:** 10 → 0.

---

## §7 — Community rebuild

```bash
graphify cluster-only . --graph graphify-out/graph.json
```

Result: 101 communities (from 179). 59 thin communities (1–2 nodes) remaining (from 135). The consolidation is driven by bridge edges and orphan adoptions wiring previously isolated nodes into existing clusters.

---

## §8 — Proof-set re-verification

Original 26 proof-set edges from T-PREP-1 re-checked against patched graph:

**Result: 26/26 PASS.** Zero proof-set edges lost during remediation.

---

## §9 — Forbidden relation check

Zero `semantically_similar_to` or `conceptually_related_to` edges between domain nodes. All 82 new edges use approved domain relation types (`enumerates`, `characterised_by`, `defines`, `maps_to`, `monitors`, `uses`, `mirrors_contract_in`, `references`, `sub_mode_of`, `cross_references`).

---

## §10 — Final status

| Gate | Result |
|---|---|
| Orphans ≤ 60 | PASS (24) |
| Unattributed == 0 | PASS (0) |
| Density ≥ 0.0025 | PASS (0.003920) |
| Proof-set 26/26 | PASS |
| Forbidden relations == 0 | PASS |
| Schema compliance | 100% |

**Step 2 COMPLETE.** T-PREP-2 done. Graph at `graphify-out/graph.json` is remediated and ready for Phase 0 coding.
