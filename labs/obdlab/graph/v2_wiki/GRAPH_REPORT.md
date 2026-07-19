# Graph Report - research/chunks  (2026-06-09)

## Corpus Check
- Corpus is ~32,889 words - fits in a single context window. You may not need a graph.

## Summary
- 451 nodes · 494 edges · 62 communities (24 shown, 38 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 84 edges (avg confidence: 0.92)
- Token cost: 0 input · 2,163,281 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Truth-vs-Perception Core|Truth-vs-Perception Core]]
- [[_COMMUNITY_MAF Fault & Load-Cell Trims|MAF Fault & Load-Cell Trims]]
- [[_COMMUNITY_Delta-Trim Profiles & Eras|Delta-Trim Profiles & Eras]]
- [[_COMMUNITY_ECU Electrical Diagnosis|ECU Electrical Diagnosis]]
- [[_COMMUNITY_Wideband O2 & Failure Modes|Wideband O2 & Failure Modes]]
- [[_COMMUNITY_Trim Analytics & Fault Atlas|Trim Analytics & Fault Atlas]]
- [[_COMMUNITY_MAP Rationality & GDI Fuel|MAP Rationality & GDI Fuel]]
- [[_COMMUNITY_Trim Thresholds & DTC Routing|Trim Thresholds & DTC Routing]]
- [[_COMMUNITY_Mode 06 & Era Taxonomy|Mode 06 & Era Taxonomy]]
- [[_COMMUNITY_Misfire Localisation & Trim Bias|Misfire Localisation & Trim Bias]]
- [[_COMMUNITY_Readiness, FMEM & DTC Trust|Readiness, FMEM & DTC Trust]]
- [[_COMMUNITY_DTC State Machine|DTC State Machine]]
- [[_COMMUNITY_Ignition Forensics & O2 DTCs|Ignition Forensics & O2 DTCs]]
- [[_COMMUNITY_Combustion Integrity Scoring|Combustion Integrity Scoring]]
- [[_COMMUNITY_L1-L5 Tier Architecture|L1-L5 Tier Architecture]]
- [[_COMMUNITY_Downstream Trim Suppression|Downstream Trim Suppression]]
- [[_COMMUNITY_Catalyst Efficiency P0420|Catalyst Efficiency P0420]]
- [[_COMMUNITY_Catalyst Monitor Masking|Catalyst Monitor Masking]]
- [[_COMMUNITY_Euro 3 GDI Hardware|Euro 3 GDI Hardware]]
- [[_COMMUNITY_O2 Sensor Translation|O2 Sensor Translation]]
- [[_COMMUNITY_MAF Linearity Cross-Check|MAF Linearity Cross-Check]]
- [[_COMMUNITY_Euro 2 CAN Wideband|Euro 2 CAN Wideband]]
- [[_COMMUNITY_L1L2 Gas Translators|L1/L2 Gas Translators]]
- [[_COMMUNITY_Per-Bank Trim Delta|Per-Bank Trim Delta]]
- [[_COMMUNITY_Single-Bank Deviation|Single-Bank Deviation]]
- [[_COMMUNITY_Common-Mode Deviation|Common-Mode Deviation]]
- [[_COMMUNITY_Fuel-Trim Proposals Registry|Fuel-Trim Proposals Registry]]
- [[_COMMUNITY_History DTC & MIL|History DTC & MIL]]
- [[_COMMUNITY_Internal ECU Fault P0606|Internal ECU Fault P0606]]
- [[_COMMUNITY_Freeze-Frame Verification|Freeze-Frame Verification]]
- [[_COMMUNITY_P0300 Water Contamination|P0300 Water Contamination]]
- [[_COMMUNITY_CKP Dropout Misfires|CKP Dropout Misfires]]
- [[_COMMUNITY_Voltage Delta Proposal|Voltage Delta Proposal]]
- [[_COMMUNITY_Era-Impossible Fault Gating|Era-Impossible Fault Gating]]
- [[_COMMUNITY_Pegged-Trim Validity Gate|Pegged-Trim Validity Gate]]
- [[_COMMUNITY_Pre-OBD-II Trim Uncertainty|Pre-OBD-II Trim Uncertainty]]
- [[_COMMUNITY_Misfire vs Fuelling|Misfire vs Fuelling]]
- [[_COMMUNITY_Fuel System Status Input|Fuel System Status Input]]
- [[_COMMUNITY_Opposite-Bank O2 Swap|Opposite-Bank O2 Swap]]
- [[_COMMUNITY_Fuel Delivery Restriction|Fuel Delivery Restriction]]
- [[_COMMUNITY_Trim Rails & Sentinels|Trim Rails & Sentinels]]
- [[_COMMUNITY_Trim Validity Preconditions|Trim Validity Preconditions]]
- [[_COMMUNITY_P01xx-P02xx Metering DTCs|P01xx-P02xx Metering DTCs]]
- [[_COMMUNITY_P03xx Misfire DTCs|P03xx Misfire DTCs]]
- [[_COMMUNITY_P04xx-P06xx Emissions DTCs|P04xx-P06xx Emissions DTCs]]
- [[_COMMUNITY_LTFT Load-Cell Proposal|LTFT Load-Cell Proposal]]
- [[_COMMUNITY_DTC Enable Criteria|DTC Enable Criteria]]
- [[_COMMUNITY_Per-Cylinder Misfire Counts|Per-Cylinder Misfire Counts]]
- [[_COMMUNITY_Fuel-Trim Chunk Index|Fuel-Trim Chunk Index]]
- [[_COMMUNITY_Upstream vs Downstream Roles|Upstream vs Downstream Roles]]
- [[_COMMUNITY_Normalized OBD Lambda|Normalized OBD Lambda]]
- [[_COMMUNITY_P0442 EVAP Leak|P0442 EVAP Leak]]
- [[_COMMUNITY_Canister Load Case|Canister Load Case]]
- [[_COMMUNITY_Crossover Validity Case|Crossover Validity Case]]
- [[_COMMUNITY_Early Air Leak Case|Early Air Leak Case]]
- [[_COMMUNITY_Sensor Offset Case|Sensor Offset Case]]
- [[_COMMUNITY_EVAP Purge Case|EVAP Purge Case]]
- [[_COMMUNITY_Fuel Contamination Case|Fuel Contamination Case]]
- [[_COMMUNITY_Vacuum Leak Case|Vacuum Leak Case]]
- [[_COMMUNITY_Open-Loop Drive State|Open-Loop Drive State]]
- [[_COMMUNITY_Open-Loop Fault State|Open-Loop Fault State]]
- [[_COMMUNITY_Open-Loop Base State|Open-Loop Base State]]

## God Nodes (most connected - your core abstractions)
1. `LTFT` - 26 edges
2. `TOTAL_TRIM` - 17 edges
3. `lambda_chem` - 16 edges
4. `ECU_HARDWARE_CHECKER` - 16 edges
5. `fuel_trim_invalid` - 11 edges
6. `liar-library` - 11 edges
7. `VREF_RAIL_COLLAPSE` - 10 edges
8. `VACUUM_LEAK` - 9 edges
9. `STFT` - 8 edges
10. `SENSOR_GROUND_TRACE_OPEN` - 8 edges

## Surprising Connections (you probably didn't know these)
- `COMLab delta engine` --semantically_similar_to--> `COMLab delta-calculation script`  [INFERRED] [semantically similar]
  research/chunks/delta-relations/07_gas-transition-matrix-2speed.md → research/chunks/delta-relations/01_delta-method-and-formula.md
- `ECT` --raises--> `fuel_trim_invalid`  [INFERRED]
  research/chunks/ecu-diagnosis/05_sensor-ground-trace-open.md → research/chunks/fuel-trim/08_validity-preconditions.md
- `VACUUM_LEAK` --manifests_at--> `LOW_IDLE`  [INFERRED]
  research/chunks/delta-relations/02_profile-vacuum-leak.md → research/chunks/delta-relations/01_delta-method-and-formula.md
- `GAS-LEAN-001` --corresponds_to--> `VACUUM_LEAK`  [INFERRED]
  research/chunks/delta-relations/07_gas-transition-matrix-2speed.md → research/chunks/delta-relations/02_profile-vacuum-leak.md
- `lambda_chem` --emits_on_delta--> `perception_contradiction`  [INFERRED]
  research/chunks/ecu-diagnosis/01_method-load-pct-and-idle-bands.md → research/chunks/o2-logic/05_bias-vs-real-truth-perception.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **DeltaTrim formula: Total Trim at stress idle minus Total Trim at low idle** — entity_delta_trim, entity_total_trim, entity_stress_idle, entity_low_idle [EXTRACTED 1.00]
- **Two-speed-idle gas transition matrix (low idle to 2500 RPM, GAS-* cases)** — entity_delta_gas, entity_gas_vac_001, entity_gas_lean_001, entity_gas_eal_001, entity_gas_wpr_001, entity_gas_wvs_001, entity_gas_fc_001, entity_gas_esc_001, entity_gas_eso_001, entity_gas_evap_001, entity_gas_cnl_001, entity_gas_cov_001 [EXTRACTED 1.00]
- **ECU hardware fault family routed by the proposed checker via Tables 1-3** — entity_ecu_hardware_checker, entity_comparative_signature_tables, entity_ecu_capacitor_leak, entity_injector_driver_open, entity_injector_driver_short, entity_coil_driver_short, entity_sensor_ground_trace_open, entity_vref_rail_collapse [EXTRACTED 1.00]
- **** — entity_rich_mixture, entity_positive_trim, entity_o2_bias [EXTRACTED 1.00]
- **** — entity_lean_mixture, entity_negative_trim, entity_o2_bias [EXTRACTED 1.00]
- **** — field_normalized_obd_lambda, entity_lambda_chem, flag_perception_contradiction [EXTRACTED 1.00]
- **** — entity_composition_py, entity_downstream_trim_role_field, entity_obdlivepayload, entity_fault_atlas_router, entity_p2096, entity_p2099 [EXTRACTED 1.00]
- **** — entity_o2_normalizer_py, entity_ip, entity_normalized_obd_lambda, entity_wideband_offset_candidate, entity_comlab, entity_lambda_chem [EXTRACTED 1.00]
- **** — entity_l3, entity_lambda_obd, entity_lambda_chem, entity_lambda_delta_vector, entity_perception_contradiction [EXTRACTED 1.00]

## Communities (62 total, 38 thin omitted)

### Community 0 - "Truth-vs-Perception Core"
Cohesion: 0.06
Nodes (43): family_map.py, o2_normalizer.py, trim perception, COMLab lab_pipeline_aggregator, Thirty-case liar library (truth-perception/03), truth-perception index & disposition ledger (README), BIASED_OFFSET, COMLab (+35 more)

### Community 1 - "MAF Fault & Load-Cell Trims"
Cohesion: 0.06
Nodes (38): MAF double-whammy signature, MAF-x-RPM cell, run-condition envelope, COMLab load-cell trim analyzer, P0102, P0171, P0172, P0174 (+30 more)

### Community 2 - "Delta-Trim Profiles & Eras"
Cohesion: 0.09
Nodes (30): confirmed mixture problem, Field Service Mode, absence of DTC, COMLab delta-calculation script, delta-relations, DELTA_TRIM, Euro_Era_1, EXHAUST_BACKPRESSURE (+22 more)

### Community 3 - "ECU Electrical Diagnosis"
Cohesion: 0.09
Nodes (30): burn_ms, calculated_engine_load_pct, ChemicalSignature.LEAN_MIXTURE, COMLab electrical-health pre-check, Comparative Signature Tables (Tables 1-3), control_module_voltage_v, detect_compensated_rich, ECT (+22 more)

### Community 4 - "Wideband O2 & Failure Modes"
Cohesion: 0.07
Nodes (28): Wideband pumping-current logic (o2-logic/08), o2-logic index & dedup ledger (README), COMLab perception-contradiction detector, DEAD, ecu-diagnosis, HEATER_FAULT, Ip, normalized_obd_lambda (+20 more)

### Community 5 - "Trim Analytics & Fault Atlas"
Cohesion: 0.08
Nodes (27): fault_atlas_router, RPM-dependence of trim, Three-Speed Test, trim authority, upstream drift, global_fault_registry.json, COMLab delta engine, COMLab trim analytics (+19 more)

### Community 6 - "MAP Rationality & GDI Fuel"
Cohesion: 0.11
Nodes (23): MAF/MAP/TPS rationality + inferred BARO (pids-protocol/02), GDI high-pressure fuel diagnostics (pids-protocol/04), EP-OBD-11, fault_atlas GDI fuel branch, fault_atlas MAF-contamination discriminator, frp_actual, frp_desired, HPFP (+15 more)

### Community 7 - "Trim Thresholds & DTC Routing"
Cohesion: 0.10
Nodes (21): analytics_preconditions, fault-atlas routing, Normal operating ranges and DTC thresholds, Trim-pattern decision tree, Bank-to-bank comparison, P0128, P0130, P0161 (+13 more)

### Community 8 - "Mode 06 & Era Taxonomy"
Cohesion: 0.10
Nodes (20): Mode 06 + Freeze Frame no-start method (pids-protocol/01), pids-protocol index & disposition ledger (README), Euro emission standards eras (taxonomy/01), Era fault-case catalogue (taxonomy/02), taxonomy index & disposition ledger (README), comlab/config/proposals/, COMLab fault_atlas, DNALab (+12 more)

### Community 9 - "Misfire Localisation & Trim Bias"
Cohesion: 0.11
Nodes (19): localised cylinder fault, MISFIRE_FALSE_LEAN, fault_atlas misfire localiser, P0201, P0301, NEGATIVE_TRIM, O2_BIAS, POSITIVE_TRIM (+11 more)

### Community 10 - "Readiness, FMEM & DTC Trust"
Cohesion: 0.12
Nodes (19): Readiness monitors and absence-of-DTC trust (pids-protocol/06), FMEM / limp-home substituted values (pids-protocol/07), absence-of-DTC inference, analytics_preconditions, battery disconnect, COMLab trim analytics, ECU_Consistency_Score, FMEM (+11 more)

### Community 11 - "DTC State Machine"
Cohesion: 0.12
Nodes (19): DTC state machine and confidence weighting (pids-protocol/08), composition.py, downstream_trim_role, dtc_state, CONFIRMED, HISTORY, PENDING, PERMANENT (+11 more)

### Community 12 - "Ignition Forensics & O2 DTCs"
Cohesion: 0.12
Nodes (17): O2 DTC families (o2-logic/07), Secondary ignition waveform forensics (pids-protocol/03), CATALYST_OVERWHELMED, ChemicalSignature.IGNITION_MISFIRE, COIL_DRIVER_SHORT, combustion-integrity, deceptive_lambda, HC (+9 more)

### Community 13 - "Combustion Integrity Scoring"
Cohesion: 0.16
Nodes (15): Combustion integrity + oxygen-usage (truth-perception/04), Chemical_Efficiency_Score, combustion failure, COMLab delta engine, DELTA_GAS, DILUTION_FAIL, fault_atlas misfire family, GAS_SAMPLE_VALID (+7 more)

### Community 14 - "L1-L5 Tier Architecture"
Cohesion: 0.18
Nodes (12): Five-tier L1-L5 architecture (truth-perception/01), Lambda-Delta vector and scoring (truth-perception/02), bank_symmetry, ECU_HARDWARE_FAULT, L3, Lambda_Delta_Vector, lambda_obd, Lean-Blind ECU (+4 more)

### Community 15 - "Downstream Trim Suppression"
Cohesion: 0.28
Nodes (9): Downstream trim suppression (o2-logic/06), DownstreamTrimRole, DownstreamTrimRole.CATALYST_MONITOR_ONLY, DownstreamTrimRole.NONE, DownstreamTrimRole.SECONDARY_FUEL_TRIM, P2096, P2099, post-cat trim suppression (+1 more)

### Community 16 - "Catalyst Efficiency P0420"
Cohesion: 0.50
Nodes (4): P0420, B1S2, S2-post-cat, CATALYST_EFFICIENCY_LOSS

### Community 17 - "Catalyst Monitor Masking"
Cohesion: 0.50
Nodes (4): catalyst monitor, P0136, P0141, systemic_masking

### Community 18 - "Euro 3 GDI Hardware"
Cohesion: 0.50
Nodes (4): electronic thermostat, Euro_Era_3, GDI, GPF

### Community 19 - "O2 Sensor Translation"
Cohesion: 0.67
Nodes (3): composition.py, translation rule, O2 sensor types and physics

### Community 20 - "MAF Linearity Cross-Check"
Cohesion: 0.67
Nodes (3): MAF linearity theoretical-airflow cross-check (pids-protocol/05), delta-relations/04, maf-linearity

### Community 21 - "Euro 2 CAN Wideband"
Cohesion: 0.67
Nodes (3): CAN bus, Euro_Era_2, wideband A/F sensor

### Community 22 - "L1/L2 Gas Translators"
Cohesion: 0.67
Nodes (3): L1, L2, OBDLab/GASLab translators

### Community 23 - "Per-Bank Trim Delta"
Cohesion: 0.67
Nodes (3): per_bank_trim_delta, T-COMV2-BANK-FUSE-1, T-OBDV2-BANK-ASYM-1

## Ambiguous Edges - Review These
- `N-002` → `diagnostic_blindness`  [AMBIGUOUS]
  research/chunks/truth-perception/03_thirty-case-liar-library.md · relation: exemplifies_class
- `systemic_masking` → `catalyst monitor`  [AMBIGUOUS]
  research/chunks/truth-perception/03_thirty-case-liar-library.md · relation: hides_fault_behind_catalyst

## Knowledge Gaps
- **207 isolated node(s):** `fuel-trim/04_trim-pattern-decision-tree`, `RpmStateBucket.STABILIZED_IDLE`, `RpmStateBucket.STRESS_IDLE`, `calculated_engine_load_pct`, `detect_compensated_rich` (+202 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **38 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `N-002` and `diagnostic_blindness`?**
  _Edge tagged AMBIGUOUS (relation: exemplifies_class) - confidence is low._
- **What is the exact relationship between `systemic_masking` and `catalyst monitor`?**
  _Edge tagged AMBIGUOUS (relation: hides_fault_behind_catalyst) - confidence is low._
- **Why does `TOTAL_TRIM` connect `Delta-Trim Profiles & Eras` to `MAF Fault & Load-Cell Trims`, `Readiness, FMEM & DTC Trust`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `ECU_HARDWARE_CHECKER` connect `ECU Electrical Diagnosis` to `Ignition Forensics & O2 DTCs`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `lambda_chem` (e.g. with `normalized_obd_lambda` and `perception_contradiction`) actually correct?**
  _`lambda_chem` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `FORCED_INDUCTION`, `TURBO_BOOST_LEAK`, `GAS-VAC-001` to the rest of the system?**
  _233 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Truth-vs-Perception Core` be split into smaller, more focused modules?**
  _Cohesion score 0.05647840531561462 - nodes in this community are weakly interconnected._