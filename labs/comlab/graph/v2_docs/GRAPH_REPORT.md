# Graph Report - comlab_docs  (2026-07-06)

## Corpus Check
- 80 files · ~27,656 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 445 nodes · 365 edges · 80 communities (30 shown, 50 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b7b2b9b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_5. Logging strategy|5. Logging strategy]]
- [[_COMMUNITY_11. What was kept, what was rejected from `COMLabDesign.md`|11. What was kept, what was rejected from `COMLabDesign.md`]]
- [[_COMMUNITY_4. Defensive input gates — who runs which check|4. Defensive input gates — who runs which check]]
- [[_COMMUNITY_11. Failure modes and recovery|11. Failure modes and recovery]]
- [[_COMMUNITY_5. The Fault-Atlas Knowledge Graph (KG) — the new piece|5. The Fault-Atlas Knowledge Graph (KG) — the new piece]]
- [[_COMMUNITY_2. Resource manifest|2. Resource manifest]]
- [[_COMMUNITY_3. Latency budget — per-stage allocation|3. Latency budget — per-stage allocation]]
- [[_COMMUNITY_6. Error & abort UX|6. Error & abort UX]]
- [[_COMMUNITY_6. Observability surfaces|6. Observability surfaces]]
- [[_COMMUNITY_10. Error-code taxonomy|10. Error-code taxonomy]]
- [[_COMMUNITY_6. `comlabcore` — pipeline modules|6. `comlab/core/` — pipeline modules]]
- [[_COMMUNITY_5. The result page — what's on Screen 6|5. The result page — what's on Screen 6]]
- [[_COMMUNITY_9. Out of scope for v1 (candidates for v2+)|9. Out of scope for v1 (candidates for v2+)]]
- [[_COMMUNITY_9. Cross-version compatibility|9. Cross-version compatibility]]
- [[_COMMUNITY_9. `tests` — layout and required tests|9. `tests/` — layout and required tests]]
- [[_COMMUNITY_4. The processing pipeline (HLD-level sequence)|4. The processing pipeline (HLD-level sequence)]]
- [[_COMMUNITY_7. JSON contracts — inbound and outbound|7. JSON contracts — inbound and outbound]]
- [[_COMMUNITY_3. `comlabschemas`|3. `comlab/schemas/`]]
- [[_COMMUNITY_8. Operational requirements|8. Operational requirements]]
- [[_COMMUNITY_10. Deployment model|10. Deployment model]]
- [[_COMMUNITY_12. Versioning, release, and rollback|12. Versioning, release, and rollback]]
- [[_COMMUNITY_7. Build validation script (the CI gate)|7. Build validation script (the CI gate)]]
- [[_COMMUNITY_8. Integration test harness|8. Integration test harness]]
- [[_COMMUNITY_6. DNA projection — who owns what|6. DNA projection — who owns what]]
- [[_COMMUNITY_8. Config schemas|8. Config schemas]]
- [[_COMMUNITY_1. Product vision & strategic value|1. Product vision & strategic value]]
- [[_COMMUNITY_7. Performance & accessibility|7. Performance & accessibility]]
- [[_COMMUNITY_5. `comlabprojection.py` and `comlabschemaslab_dna_views.py` (NEW)|5. `comlab/projection.py` and `comlab/schemas/lab_dna_views.py` (NEW)]]
- [[_COMMUNITY_2. Users|2. Users]]
- [[_COMMUNITY_7._comlab_analytics_power_loss_analytics.py|7._comlab_analytics_power_loss_analytics.py.md]]
- [[_COMMUNITY_ADR-0001 COMLab is the read-only prune→rank fusion spine|ADR-0001: COMLab is the read-only prune→rank fusion spine]]
- [[_COMMUNITY_ADR-0002 No cross-lab Python imports — mirror types over JSON|ADR-0002: No cross-lab Python imports — mirror types over JSON]]
- [[_COMMUNITY_ADR-0003 Signalnoise — every schema field needs a named, existing consumer|ADR-0003: Signal/noise — every schema field needs a named, existing consumer]]
- [[_COMMUNITY_ADR-0004 Scope is petrol 1990–2010 (Euro 1–5); Euro 6+ perks out of scope|ADR-0004: Scope is petrol 1990–2010 (Euro 1–5); Euro 6+ perks out of scope]]
- [[_COMMUNITY_ADR-0005 DNALab pre-resolves the horizon; COMLab never parses the VIN|ADR-0005: DNALab pre-resolves the horizon; COMLab never parses the VIN]]
- [[_COMMUNITY_ADR-0006 Separate the rule registry from the Fault-Atlas KG|ADR-0006: Separate the rule registry from the Fault-Atlas KG]]
- [[_COMMUNITY_ADR-0007 Brettschneider chemistry is ground truth; detect ECU perception contradiction|ADR-0007: Brettschneider chemistry is ground truth; detect ECU perception contradiction]]
- [[_COMMUNITY_ADR-0008 Emitter labs emit channels, not verdicts; fault fusion is COMLab, built last|ADR-0008: Emitter labs emit channels, not verdicts; fault fusion is COMLab, built last]]
- [[_COMMUNITY_ADR-0009 Two-operating-point Δ math lives in COMLab; additive with a single-point fallback|ADR-0009: Two-operating-point Δ math lives in COMLab; additive with a single-point fallback]]
- [[_COMMUNITY_ADR-0010 Deterministic 5-phase triage with a confidence floor and a catalyst-damage override|ADR-0010: Deterministic 5-phase triage with a confidence floor and a catalyst-damage override]]
- [[_COMMUNITY_ADR-0011 Surface the routing directive and input-echo audit in the outbound contract|ADR-0011: Surface the routing directive and input-echo audit in the outbound contract]]
- [[_COMMUNITY_BDD — COMLab|BDD — COMLab]]
- [[_COMMUNITY_Feature_Brettschneider_chemistry_overrules_ECU_perception|Feature_Brettschneider_chemistry_overrules_ECU_perception.md]]
- [[_COMMUNITY_Feature_Catalyst-damage-imminent_safety_override|Feature_Catalyst-damage-imminent_safety_override.md]]
- [[_COMMUNITY_Feature_Contract_validation_at_the_ingestion_gate|Feature_Contract_validation_at_the_ingestion_gate.md]]
- [[_COMMUNITY_Feature_Degradation_classification_and_graceful_fallback|Feature_Degradation_classification_and_graceful_fallback.md]]
- [[_COMMUNITY_Feature_Deterministic_registry_triage_with_a_confidence_floor|Feature_Deterministic_registry_triage_with_a_confidence_floor.md]]
- [[_COMMUNITY_Feature_Differential_siblings_panel|Feature_Differential_siblings_panel.md]]
- [[_COMMUNITY_Feature_ECU_hardware_digital-lie_detection|Feature_ECU_hardware_digital-lie_detection.md]]
- [[_COMMUNITY_Feature_Evidence_gates_suppress_unreliable_findings|Feature_Evidence_gates_suppress_unreliable_findings.md]]
- [[_COMMUNITY_Feature_KG_enrichment_and_registry_consistency|Feature_KG_enrichment_and_registry_consistency.md]]
- [[_COMMUNITY_Feature_Stage-A_fatal_gates_honour_suppression|Feature_Stage-A_fatal_gates_honour_suppression.md]]
- [[_COMMUNITY_Feature_Symptom_routing_suppresses_the_right_lab_sections|Feature_Symptom_routing_suppresses_the_right_lab_sections.md]]
- [[_COMMUNITY_Feature_Two-operating-point_delta_diagnosis|Feature_Two-operating-point_delta_diagnosis.md]]
- [[_COMMUNITY_References|References.md]]
- [[_COMMUNITY_COMLab DetailedDeployment Design (DLD)|COMLab Detailed/Deployment Design (DLD)]]
- [[_COMMUNITY_13._Open_questions_for_ops_sign-off|13._Open_questions_for_ops_sign-off.md]]
- [[_COMMUNITY_14._References|14._References.md]]
- [[_COMMUNITY_1._Scope_and_runtime_targets|1._Scope_and_runtime_targets.md]]
- [[_COMMUNITY_4._Boot_sequence|4._Boot_sequence.md]]
- [[_COMMUNITY_COMLab High-Level Design (HLD)|COMLab High-Level Design (HLD)]]
- [[_COMMUNITY_10._Change_protocol_—_how_this_HLD_evolves|10._Change_protocol_—_how_this_HLD_evolves.md]]
- [[_COMMUNITY_12._Open_questions_—_resolved_in_code_(v1.0_→_v2.0)|12._Open_questions_—_resolved_in_code_(v1.0_→_v2.0).md]]
- [[_COMMUNITY_13._References|13._References.md]]
- [[_COMMUNITY_1._What_COMLab_is,_in_one_sentence|1._What_COMLab_is,_in_one_sentence.md]]
- [[_COMMUNITY_2._Where_COMLab_sits_in_4DLab_(post-horizontal-DNA_flip)|2._Where_COMLab_sits_in_4DLab_(post-horizontal-DNA_flip).md]]
- [[_COMMUNITY_3._The_four_core_responsibilities|3._The_four_core_responsibilities.md]]
- [[_COMMUNITY_8._Module_layout_(HLD-level_—_LLD_finalises_file_boundaries)|8._Module_layout_(HLD-level_—_LLD_finalises_file_boundaries).md]]
- [[_COMMUNITY_9._Cross-cutting_rules_COMLab_must_honour|9._Cross-cutting_rules_COMLab_must_honour.md]]
- [[_COMMUNITY_COMLab Low-Level Design (LLD)|COMLab Low-Level Design (LLD)]]
- [[_COMMUNITY_11._Inner-loop_expectations|11._Inner-loop_expectations.md]]
- [[_COMMUNITY_12._References|12._References.md]]
- [[_COMMUNITY_1._Scope_and_non-goals|1._Scope_and_non-goals.md]]
- [[_COMMUNITY_2._Directory_blueprint_(final,_post-LLD)|2._Directory_blueprint_(final,_post-LLD).md]]
- [[_COMMUNITY_4._(reserved_for_future_schema_groups)|4._(reserved_for_future_schema_groups).md]]
- [[_COMMUNITY_COMLab Product Requirements Document (PRD)|COMLab Product Requirements Document (PRD)]]
- [[_COMMUNITY_10._Success_metrics_(how_we_know_it_works)|10._Success_metrics_(how_we_know_it_works).md]]
- [[_COMMUNITY_11._Open_questions_for_product_sign-off|11._Open_questions_for_product_sign-off.md]]
- [[_COMMUNITY_12._References|12._References.md]]
- [[_COMMUNITY_3._The_wizard_ingestion_flow|3._The_wizard_ingestion_flow.md]]

## God Nodes (most connected - your core abstractions)
1. `5. Logging strategy` - 17 edges
2. `11. What was kept, what was rejected from `COMLabDesign.md`` - 17 edges
3. `4. Defensive input gates — who runs which check` - 15 edges
4. `11. Failure modes and recovery` - 14 edges
5. `5. The Fault-Atlas Knowledge Graph (KG) — the new piece` - 14 edges
6. `2. Resource manifest` - 12 edges
7. `3. Latency budget — per-stage allocation` - 12 edges
8. `6. Error & abort UX` - 11 edges
9. `6. Observability surfaces` - 10 edges
10. `10. Error-code taxonomy` - 9 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (80 total, 50 thin omitted)

### Community 0 - "5. Logging strategy"
Cohesion: 0.11
Nodes (18): 5.1 Library and format, 5.2 Per-stage event vocabulary, 5.3 Per-stage latency fields, 5.4 Audit record, 5.5 Log levels, 5. Logging strategy, Graph relations (explicit), Stage: End-to-end (+10 more)

### Community 1 - "11. What was kept, what was rejected from `COMLabDesign.md`"
Cohesion: 0.11
Nodes (18): 11. What was kept, what was rejected from `COMLabDesign.md`, From the proposal: 250 ms latency target, From the proposal: 2.5 MB total config size envelope, From the proposal: 4-script module count (drops `symptom_router.py`), From the proposal: Absence of `SymptomDNA` in the inbound payload, From the proposal: `fault_enrichment` block in the outbound payload, From the proposal: `global_fault_registry.json` as flat rule registry, From the proposal: Hard-coded `0.0` injection for missing trims on legacy cars (+10 more)

### Community 2 - "4. Defensive input gates — who runs which check"
Cohesion: 0.12
Nodes (16): 4.1 Producer-lab gates (run on submit of screens 2, 3, 4 — not COMLab), 4.2 COMLab gates (run in Stage A of the pipeline, on the assembled payload), 4.3 Null vs zero — the integrity rule, 4. Defensive input gates — who runs which check, Gate: Decimal-misplacement sentinel, Gate: DNA-relative RPM ceiling, Gate: DTC format, Gate: Engine warmed (final guard) (+8 more)

### Community 3 - "11. Failure modes and recovery"
Cohesion: 0.12
Nodes (15): 11.1 Failure-to-recovery matrix, 11.2 Graceful degradation paths (not failures), 11.3 No automatic retry inside COMLab, 11. Failure modes and recovery, Failure: Analytics divide-by-zero / NaN, Failure: Boot time exceeds 1.5 s, Failure: Config file missing at boot, Failure: KG lookup miss at runtime (`ERR-stage_c_kg.err_lookup_miss`) (+7 more)

### Community 4 - "5. The Fault-Atlas Knowledge Graph (KG) — the new piece"
Cohesion: 0.12
Nodes (15): 5.1 What it is and what it is not, 5.2 What a node carries — the consumer-justified field set, 5.3 Differential siblings — runtime top-3 vs editor-curated, 5.4 The on-disk shape (HLD-level — LLD will finalise the JSON schema), 5.5 Consistency contract with the rule registry, 5. The Fault-Atlas Knowledge Graph (KG) — the new piece, Field: `component_group`, Field: `differential_siblings` (+7 more)

### Community 5 - "2. Resource manifest"
Cohesion: 0.14
Nodes (13): 2.1 In-memory footprint at steady state, 2.2 On-disk config envelope (the 2.5 MB hard limit), 2.3 No persistent state, 2.4 Reference hardware profile, 2. Resource manifest, Asset: `config/kg/*.json` (13 per-family files), Asset: `eras_sensitivity_masks.yaml`, Asset: `global_fault_registry.json` (+5 more)

### Community 6 - "3. Latency budget — per-stage allocation"
Cohesion: 0.14
Nodes (13): 3. Latency budget — per-stage allocation, Graph relations (explicit), Stage: DNA projection (A.6), Stage: Fault-atlas walk (Stage B), Stage: JSON parse + Pydantic gate (Stage A.1), Stage: KG resolve (Stage C), Stage: Power-loss analytics (Stage D), Stage: Routing directive + degradation classify (A.4 + A.5) (+5 more)

### Community 7 - "6. Error & abort UX"
Cohesion: 0.15
Nodes (12): 6.1 Error message principles, 6.2 Error code → user-facing copy map, 6.3 Degraded modes (not errors), 6. Error & abort UX, Code: `ERR-ABORT-001`, Code: `ERR-ABORT-002`, Code: `ERR-ABORT-004`, Code: `ERR-ABORT-005` (+4 more)

### Community 8 - "6. Observability surfaces"
Cohesion: 0.17
Nodes (11): 6.1 Tracing (as-built), 6. Observability surfaces, Dashboard: Aborts by code, Dashboard: Catalyst-imminent overrides, Dashboard: Degradation mode share, Dashboard: Fatal abort rate, Dashboard: Fault family share, Dashboard: p95 stage latency (+3 more)

### Community 9 - "10. Error-code taxonomy"
Cohesion: 0.18
Nodes (10): 10. Error-code taxonomy, Code: `ERR-ABORT-001`, Code: `ERR-ABORT-002`, Code: `ERR-ABORT-004`, Code: `ERR-ABORT-005`, Code: `ERR-CONTRACT-001`, Code: `ERR-CONTRACT-002`, Code: `ERR-CONTRACT-003` (+2 more)

### Community 10 - "6. `comlab/core/` — pipeline modules"
Cohesion: 0.18
Nodes (10): 6.1 `horizon_context_injector.py` — rewritten in place, 6.2 `symptom_router.py`, 6.3 `lab_pipeline_aggregator.py` — Stage A completed, 6.4 `fault_atlas_router.py` — Stage B completed, 6.5 `fault_atlas_kg.py` — NEW, 6.6 `perception_contradiction.py` — λ-truth vs λ-perception (as-built), 6.7 `ecu_hardware_checker.py` — ECU digital-lie detector (as-built, DEP-9), 6.8 `observability/_tracer.py` — tracer shim (as-built) (+2 more)

### Community 11 - "5. The result page — what's on Screen 6"
Cohesion: 0.18
Nodes (10): 5.1 Verdict header, 5.2 Fault enrichment block, 5.3 Differential siblings panel, 5.4 Performance analytics, 5.5 User-input echo audit (Q4 ruling), 5.6 Lab routing directive panel (Q6 ruling), 5.7 Execution meta footer, 5.8 Result-page layout when a fatal abort fires (+2 more)

### Community 12 - "9. Out of scope for v1 (candidates for v2+)"
Cohesion: 0.18
Nodes (10): 9. Out of scope for v1 (candidates for v2+), Graph relations (explicit), Item: Cold-start fault analysis, Item: Diesel powertrains, Item: Free-text symptom AI parser, Item: Multi-fault verdicts (e.g. "fault A AND fault B simultaneously"), Item: OEM-specific deep DTCs (U-codes, manufacturer-specific), Item: Part-cost / labour-hour estimation (+2 more)

### Community 13 - "9. Cross-version compatibility"
Cohesion: 0.20
Nodes (9): 9.1 `schema_version` matrix, 9.2 KG file `schema_version`, 9.3 Backward-compatibility release rule, 9. Cross-version compatibility, Graph relations (explicit), Producer ships: `vehicle_dna.schema_version == "0.9"`, Producer ships: `vehicle_dna.schema_version == "1.0"`, Producer ships: `vehicle_dna.schema_version == "1.2"` (+1 more)

### Community 14 - "9. `tests/` — layout and required tests"
Cohesion: 0.22
Nodes (8): 9.1 `tests/fixtures/`, 9.2 `tests/unit/`, 9.3 `tests/e2e/`, 9.4 `tests/e2e/test_kg_registry_consistency.py` (critical), 9.5 `tests/e2e/test_pipeline_round_trip.py`, 9.6 `tests/e2e/test_error_codes.py`, 9. `tests/` — layout and required tests, Graph relations (explicit)

### Community 15 - "4. The processing pipeline (HLD-level sequence)"
Cohesion: 0.25
Nodes (7): 4.1 Stage A — `lab_pipeline_aggregator.py`, 4.2 Stage B — `fault_atlas_router.py` (the rule engine), 4.3 Stage C — `fault_atlas_kg.py` (NEW — Fault-Atlas Knowledge Graph), 4.4 Stage D — `power_loss_analytics.py`, 4.5 Stage E — `response.py` (serializer), 4. The processing pipeline (HLD-level sequence), Graph relations (explicit)

### Community 16 - "7. JSON contracts — inbound and outbound"
Cohesion: 0.25
Nodes (7): 7.1 Inbound: `OrchestratorInboundRequest`, 7.2 What COMLab reads from where, 7.3 Routing directive (internal), 7.4 Outbound: `OrchestratorFinalUIOutput` (NEW shape), 7.5 Error shapes, 7. JSON contracts — inbound and outbound, Graph relations (explicit)

### Community 17 - "3. `comlab/schemas/`"
Cohesion: 0.29
Nodes (6): 3.1 `vocabulary.py` — locked enums, 3.2 `ingestion.py` — `OrchestratorInboundRequest` and friends, 3.3 `response.py` — `OrchestratorFinalUIOutput` extended, 3.4 `kg.py` — Fault-Atlas KG types (NEW), 3. `comlab/schemas/`, Graph relations (explicit)

### Community 18 - "8. Operational requirements"
Cohesion: 0.29
Nodes (6): 8.1 Session audit trail, 8.2 No network requirement after launch, 8.3 Config update flow, 8.4 Observability surfaces, 8. Operational requirements, Graph relations (explicit)

### Community 19 - "10. Deployment model"
Cohesion: 0.33
Nodes (5): 10.1 v1 — in-process library, 10.2 v2 candidate — microservice, 10.3 What we do not deploy, 10. Deployment model, Graph relations (explicit)

### Community 20 - "12. Versioning, release, and rollback"
Cohesion: 0.33
Nodes (5): 12.1 Release cadence, 12.2 Rollback model, 12.3 Canary, 12. Versioning, release, and rollback, Graph relations (explicit)

### Community 21 - "7. Build validation script (the CI gate)"
Cohesion: 0.33
Nodes (5): 7.1 What the script enforces (in order — fail-fast), 7.2 What the script does NOT do (deliberately), 7.3 Two-reviewer rule integration, 7. Build validation script (the CI gate), Graph relations (explicit)

### Community 22 - "8. Integration test harness"
Cohesion: 0.33
Nodes (5): 8.1 Fixture sourcing, 8.2 Fixture refresh policy, 8.3 Synthetic stress cases, 8. Integration test harness, Graph relations (explicit)

### Community 23 - "6. DNA projection — who owns what"
Cohesion: 0.33
Nodes (5): 6.1 Projection ownership, 6.2 Why COMLab still re-projects internally, 6.3 What lives in each view, 6. DNA projection — who owns what, Graph relations (explicit)

### Community 24 - "8. Config schemas"
Cohesion: 0.33
Nodes (5): 8.1 `global_fault_registry.json`, 8.2 `kg/_kg_schema.json` and per-family files (Q2 ruling), 8.3 `eras_sensitivity_masks.yaml` (existing), 8. Config schemas, Graph relations (explicit)

### Community 25 - "1. Product vision & strategic value"
Cohesion: 0.33
Nodes (5): 1.1 What COMLab is, from the user's perspective, 1.2 Strategic value, 1.3 What COMLab is *not*, 1. Product vision & strategic value, Graph relations (explicit)

### Community 26 - "7. Performance & accessibility"
Cohesion: 0.33
Nodes (5): 7.1 Latency commitment to the user, 7.2 Accessibility, 7.3 Mobile-first, 7. Performance & accessibility, Graph relations (explicit)

### Community 27 - "5. `comlab/projection.py` and `comlab/schemas/lab_dna_views.py` (NEW)"
Cohesion: 0.40
Nodes (4): 5.1 `comlab/schemas/lab_dna_views.py`, 5.2 `comlab/projection.py`, 5. `comlab/projection.py` and `comlab/schemas/lab_dna_views.py` (NEW), Graph relations (explicit)

### Community 28 - "2. Users"
Cohesion: 0.40
Nodes (4): 2. Users, Graph relations (explicit), Persona: **Skilled owner-operator** (secondary), Persona: **Workshop technician** (primary)

### Community 29 - "7._comlab_analytics_power_loss_analytics.py.md"
Cohesion: 0.50
Nodes (3): 7.1 `comlab/analytics/delta_engine.py` — two-operating-point Δ (as-built, NEW), 7. `comlab/analytics/power_loss_analytics.py`, Graph relations (explicit)

## Knowledge Gaps
- **319 isolated node(s):** `Graph relations (explicit)`, `Graph relations (explicit)`, `Graph relations (explicit)`, `Graph relations (explicit)`, `Graph relations (explicit)` (+314 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **50 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Graph relations (explicit)`, `Graph relations (explicit)`, `Graph relations (explicit)` to the rest of the system?**
  _319 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `5. Logging strategy` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `11. What was kept, what was rejected from `COMLabDesign.md`` be split into smaller, more focused modules?**
  _Cohesion score 0.10526315789473684 - nodes in this community are weakly interconnected._
- **Should `4. Defensive input gates — who runs which check` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `11. Failure modes and recovery` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `5. The Fault-Atlas Knowledge Graph (KG) — the new piece` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Should `2. Resource manifest` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._