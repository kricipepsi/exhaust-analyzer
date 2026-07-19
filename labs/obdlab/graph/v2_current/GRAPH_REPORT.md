# Graph Report - 4DLabV2\labs\obdlab  (2026-06-06)

## Corpus Check
- 57 files · ~44,753 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1245 nodes · 1664 edges · 103 communities (75 shown, 28 thin omitted)
- Extraction: 91% EXTRACTED · 9% INFERRED · 0% AMBIGUOUS · INFERRED: 156 edges (avg confidence: 0.68)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f7544224`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 53|Community 53]]
- [[_COMMUNITY_Community 54|Community 54]]
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 57|Community 57]]
- [[_COMMUNITY_Community 58|Community 58]]
- [[_COMMUNITY_Community 59|Community 59]]
- [[_COMMUNITY_Community 60|Community 60]]
- [[_COMMUNITY_Community 61|Community 61]]
- [[_COMMUNITY_Community 62|Community 62]]
- [[_COMMUNITY_Community 63|Community 63]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 69|Community 69]]
- [[_COMMUNITY_Community 70|Community 70]]
- [[_COMMUNITY_Community 71|Community 71]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]
- [[_COMMUNITY_Community 85|Community 85]]
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 89|Community 89]]
- [[_COMMUNITY_Community 90|Community 90]]
- [[_COMMUNITY_Community 91|Community 91]]
- [[_COMMUNITY_Community 92|Community 92]]
- [[_COMMUNITY_Community 93|Community 93]]
- [[_COMMUNITY_Community 94|Community 94]]
- [[_COMMUNITY_Community 99|Community 99]]

## God Nodes (most connected - your core abstractions)
1. `OBDLivePayload` - 43 edges
2. `_healthy_pids()` - 30 edges
3. `_dna_view()` - 30 edges
4. `Domain reference — 28 live fault profiles (from `OBD Live PID Diagnostic Profiles.md`)` - 29 edges
5. `_canonical_kwargs()` - 27 edges
6. `_make_validator()` - 27 edges
7. `_pids()` - 27 edges
8. `_make_checker()` - 27 edges
9. `OBDLab Module Wiki` - 24 edges
10. `test_obd_lab.pyfrom obd_live_lab.core.pid_ingestion_validator import PIDIngestionValidatorfrom obd_live_lab.core.semantic_consistency_checker import SemanticConsistencyCheckerfrom obd_live_lab.core.sensor_signal_translator import SensorSignalTranslator` - 23 edges

## Surprising Connections (you probably didn't know these)
- `translator()` --calls--> `SensorSignalTranslator`  [INFERRED]
  tests/integration/test_pipeline_smoke.py → obdlab/core/sensor_signal_translator.py
- `translator()` --calls--> `SensorSignalTranslator`  [INFERRED]
  tests/regression/test_obdlab_regression.py → obdlab/core/sensor_signal_translator.py
- `normalizer()` --calls--> `O2Normalizer`  [INFERRED]
  tests/unit/test_o2_normalizer.py → obdlab/core/o2_normalizer.py
- `_make_validator()` --calls--> `PIDIngestionValidator`  [INFERRED]
  tests/unit/test_pid_ingestion_validator.py → obdlab/core/pid_ingestion_validator.py
- `_make_checker()` --calls--> `SemanticConsistencyChecker`  [INFERRED]
  tests/unit/test_semantic_consistency_checker.py → obdlab/core/semantic_consistency_checker.py

## Communities (103 total, 28 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (67): _EvidenceTier, MatchType, Specificity class for an OBDLab evidence signature., Internal corroboration tier derived from existing payload fields., OBDLivePayload, OBDLivePayload Pydantic model per OBDLab_KG_Wiki.md §5 / SEMANTIC_CONTRACT.md §4, OBDLab output payload — canonical fields per §5 / SEMANTIC_CONTRACT §4.4., O2FailureMode (+59 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (67): _dna_view(), _dual_pids(), _expected_ve(), Tests for VEEngine — 3-branch polymorphic routing per OBDLab_KG_Wiki.md §10., MAF_ONLY — back-calc MAP, bucket=REGULATORY_HIGH_IDLE., DUAL at STRESS_IDLE ~4000 RPM., DUAL at STABILIZED_IDLE ~650 RPM (low end of idle band)., DUAL with cold intake air (-10°C). (+59 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (55): BaseModel, dna_high(), Integration smoke test — exercises the full OBDLab pipeline end-to-end.  Covers:, STRESS_IDLE bucket with wideband O2 passthrough., engine_rpm > 8000 raises PIDValidationError., Cold engine (ECT=40°C) + dna_view=None → COLD_OPEN_LOOP_INVALID, analytics froze, Minimal valid input + dna_view=None → payload emitted, JSON round-trips., 2-bank V-engine: both bank-1 and bank-2 trims in payload. (+47 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (55): _make_checker(), _make_dna(), _pids(), Tests for SemanticConsistencyChecker — 4 Physics Gates, thermal gate, closed-lo, ECT=85, Open_Loop_Cold → SemanticConsistencyError., ECT=40, Open_Loop_Cold → no error (engine is genuinely cold)., VE=65%, NA, STABILIZED_IDLE → no error., VE=95% but TURBOCHARGED → no error (turbo can exceed 90%). (+47 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (43): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, emissions, engine_displacement_liters, induction_type (+35 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (40): _dna_view(), Tests for O2Normalizer — 2-branch O2 normalisation per OBDLab_KG_Wiki.md §11., Wideband equivalence ratio passes through unchanged., Wideband ratio outside [0.7, 1.3] returns O2_CHANNEL_FAULT with clamped lambda., Boundary values 0.7 and 1.3 are valid and pass through., Without DNA, narrowband is assumed and narrowband input is accepted., When DNA says NARROWBAND but pid_oxygen_sensor_volts is missing., When DNA says WIDEBAND but pid_wideband_equivalence_ratio is missing. (+32 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (39): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, emissions, engine_displacement_liters, induction_type (+31 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (39): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, emissions, engine_displacement_liters, induction_type (+31 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (39): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, emissions, engine_displacement_liters, induction_type (+31 more)

### Community 9 - "Community 9"
Cohesion: 0.11
Nodes (37): _candidate_evidence_tier(), _candidate_sort_key(), CandidateScore, _clamp_confidence(), classify_top3(), _evidence_tier(), _float_or_none(), _freeze_frame_o2_rail_agrees() (+29 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (37): 10. `core/semantic_consistency_checker.py` — `SemanticConsistencyChecker`, 11. `core/analytics_preconditions.py` — `AnalyticsPreconditions`, 12. `core/state_bucketing.py`, 13. Test Coverage, 1. Module Map, 2. `schemas/vocabulary.py` — Enums, 3. `schemas/dna_view.py`, 4. `schemas/payload.py` — `OBDLivePayload` (21 fields) (+29 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (34): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, emissions, engine_displacement_liters, induction_type (+26 more)

### Community 12 - "Community 12"
Cohesion: 0.06
Nodes (34): 1. Functional Architecture & Core Mandate, 1. The 3-Way Polymorphic Math Routing Matrix, 1. The Architectural Crisis: Narrowband vs. Wideband, 1. The Core Volumetric Efficiency Equation, 1. The OBD Lab Architectural Component Tree, 2. Complete Sequence Timeline within the OBD Lab Module, 2. Guarding Against Traversal Crashes, 2. High-Density Node Inventory (The 8-PID Minimalist Schema) (+26 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (30): _make_dna(), _make_validator(), Tests for PIDIngestionValidator — boundary checks, unit conversions, DNA-RPM th, When both canonical and alternate are present, keep canonical, drop alternate., DNA-HIGH with rated_rpm=None still gets static 0..8000 check., test_bank2_contract_one_bank_both_null_passes(), test_bank2_contract_one_bank_longft2_non_null_raises(), test_bank2_contract_one_bank_shrtft2_non_null_raises() (+22 more)

### Community 14 - "Community 14"
Cohesion: 0.07
Nodes (28): case_id, dna_view_json, expected_payload_subset, calculated_engine_load_pct, coolant_temp_c, engine_rpm, engine_warmed, longft2 (+20 more)

### Community 15 - "Community 15"
Cohesion: 0.07
Nodes (29): Domain reference — 28 live fault profiles (from `OBD Live PID Diagnostic Profiles.md`), Profile 10 — `CATALYST_OVERWHELMED`, Profile 11 — `SAMPLE_INVALID`, Profile 12 — `TIMING_OVER_ADVANCED`, Profile 13 — `TIMING_RETARDED`, Profile 14 — `O2_SENSOR_BIASED_LOW`, Profile 15 — `O2_SENSOR_BIASED_HIGH`, Profile 16 — `WORN_ENGINE` (+21 more)

### Community 16 - "Community 16"
Cohesion: 0.07
Nodes (27): 10. Analytics Preconditions — DTC Frozensets, 11. Cold-Engine Payload Defaults, 12. `freeze_frame_pids` Forwarding Contract, 13. Error Types and Codes, 14. Forbidden Patterns (OBDLab-specific), 1. Physical Constants (`core/ve_engine.py`), 2. Physical Sensor Bounds (`config/physical_sensor_bounds.json`), 3. Unit Conversion Factors (+19 more)

### Community 17 - "Community 17"
Cohesion: 0.13
Nodes (14): AssertionError, Raised when a Physics Gate (§4) fails.      Source: OBDLab_KG_Wiki.md §4., SemanticConsistencyError, Semantic consistency checker — 4 Physics Gates per OBDLab_KG_Wiki.md §4.  Appl, Gate 2: closed loop should be active at engine temperature — wiki: §4., Gate 3: VE > 90% on NA engine at STABILIZED_IDLE — wiki: §4.          Three-br, Gate 4: trim out of safety range — wiki: §4.          Redundant with §3.1 boun, Thermal gate — wiki: §4.1.          ECT < 75 °C → set rpm_state_bucket = COLD_ (+6 more)

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (11): _calc_ve_standard(), _expected_ve(), VE computation engine per OBDLab_KG_Wiki.md §10.  Implements the Speed-Density, Standard VE formula §10.1 — both MAF and MAP present., Emulate MAF from MAP+RPM+Displacement, then compute VE.          Emulated_MAF, Back-calculate MAP from MAF+RPM+Displacement, then compute VE.          Inferr, Classify VE result against fault triggers per §6.4 / §10.3.          FAULT_VE_, VE computation engine with 3-branch polymorphic routing per §10.2.      Public (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (14): _assert_field(), _load_fixture_files(), Regression test suite for OBDLab — parametrized over JSON fixture files.  Each f, At least 5 regression fixtures are present., Verify regression fixtures cover HIGH, None, and PARTIAL DNA confidence., Yield (case_id, fixture_dict) for every JSON file in fixtures/., Resolve an expected value, supporting the '_approx' suffix for float tolerance., Assert a single payload field against expected value. (+6 more)

### Community 20 - "Community 20"
Cohesion: 0.17
Nodes (15): NamedTuple, AirMeteringStrategy, EuroEmissionCategory, InductionType, O2SensorType, OBDLab DNA view — typed DNA-first input per NewArchProposal §4 Step 2 / §5.  Obd, European emission category per OBD_VOCABULARY.md §4.1.      Source: OBD_VOCABULA, Air metering strategy per OBD_VOCABULARY.md §4.2.      Source: OBD_VOCABULARY.md (+7 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (15): Tests for TrimVectorAggregator per OBDLab_KG_Wiki.md §12., shrtft1 + longft1 with number_of_banks == 1 returns (bank1, None)., All four trim fields summed per-bank when number_of_banks == 2., Bank-2 None fields are ignored when number_of_banks == 1., number_of_banks == 2 but shrtft2 is None raises PIDValidationError., number_of_banks == 2 but longft2 is None raises PIDValidationError., Missing shrtft1 raises PIDValidationError., Missing longft1 raises PIDValidationError. (+7 more)

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (15): 1. Responsibility, 2. Architecture Position, 3. Internal Pipeline (7 Steps), 4. VE Routing Architecture, 5. O2 Normalisation Architecture, 6. Trim Analytics Gate — 8-Gate Priority Chain, 7. COMLab Integration Points, 8. Non-Functional Requirements (+7 more)

### Community 23 - "Community 23"
Cohesion: 0.12
Nodes (15): Assumptions, Explicitly Deferred (v2), Key Features (all P0), PRD — OBDLab, Section 1 — Summary, Section 2 — Contacts, Section 3 — Background, Section 4 — Objective (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (8): PIDIngestionValidator, PID ingestion validator per OBDLab_KG_Wiki.md §3.  Source: OBDLab_KG_Wiki.md §3., DNA-relative RPM boundary per NewArchProposal §3.3.          HIGH:     strict —, Enforce bank-2 null contract per OBDLab_KG_Wiki.md §3.1.          shrtft2 and lo, Validates manually-entered OBD-II PIDs against physical sensor bounds.      Sour, Apply §3.2 unit conversions, validate against §3.1 bounds, return sanitised dict, Convert alternate-unit fields to canonical form per §3.2.          When both an, Validate each field against §3.1 bounds. Raise PIDValidationError on violation.

### Community 25 - "Community 25"
Cohesion: 0.13
Nodes (15): 6.1 RpmStateBucket — see `SEMANTIC_CONTRACT.md §8`, 6.2 VERoutingMode — OBDLab-internal, 6.3 O2NormalizationMode — OBDLab-internal, 6.4 VEValidity — OBDLab-internal, 6.5 TrimAnalyticsGate — OBDLab-internal, 6.6 NodeSensorStatus — OBDLab-internal, 6.7 O2FailureMode — OBDLab-internal, 6. OBDLab enum declarations (+7 more)

### Community 26 - "Community 26"
Cohesion: 0.18
Nodes (12): Map OBDLab evidence signatures to canonical diagnostic families.  This module is, Return the OBDLab-reachable family for a typed evidence signature.      Args:, signature_to_family(), Tests for OBDLab evidence-signature to canonical-family mapping., Every O2 failure maps to sensor_fault; healthy O2 maps to no_fault., Agreeing trim direction and lambda band map to lean/rich families., Every emitted family is canonical and OBDLab-reachable., Unknown or non-discriminating signatures fall back to no_fault. (+4 more)

### Community 27 - "Community 27"
Cohesion: 0.19
Nodes (8): O2Normalizer, O2 sensor normalisation layer per OBDLab_KG_Wiki.md §11.  Routes on dna_view.u, Direct wideband pass-through per §11.2.          Reads pid_wideband_equivalenc, 3-zone voltage → lambda mapping for WB sensor in NB simulation mode §11.3., Normalize O2 sensor input to a unified lambda scalar per §11.      Public entr, Route to the matching O2 normalisation branch and return (lambda, mode, failure), 3-zone narrowband voltage → lambda mapping per §11.1.          Reads pid_oxyge, normalizer()

### Community 28 - "Community 28"
Cohesion: 0.21
Nodes (12): NodeMAFStatus, NodeMAPStatus, O2NormalizationMode, OBDLab canonical vocabulary — 7 StrEnums from OBDLab_KG_Wiki.md §6.  All value, Engine RPM state bucket per OBDLab_KG_Wiki.md §6.1 / §8.      Source: OBDLab_K, VE-formula polymorphic routing per OBDLab_KG_Wiki.md §6.2 / §10.2.      Source, O2 sensor normalisation strategy per OBDLab_KG_Wiki.md §6.3 / §11.      Source, MAF sensor data provenance per OBDLab_KG_Wiki.md §6.6.      Source: OBDLab_KG_ (+4 more)

### Community 29 - "Community 29"
Cohesion: 0.15
Nodes (12): code:json ({), Coverage matrix — what the log set must span, Deliverable, Fault families to represent (within 1990–2010 petrol scope), Output format, Part A — raw PID dict (`raw_user_inputs`), Part B — vehicle DNA view (`ObdLabDnaView`), Research Prompt — Build a Test PID Log Set for OBDLab (+4 more)

### Community 31 - "Community 31"
Cohesion: 0.17
Nodes (11): Tests for AnalyticsPreconditions per OBDLab_KG_Wiki.md §9.  8 gates × (PASS + FA, throttle_pos == 90 → WOT_ACTIVE., Missing throttle_pos → gate passes (treat as not-WOT)., Healthy PID dict with semantic_gates_passed=True → VALID., Verify P0130 and P0161 are in O2_FAULT_DTCS (range endpoints)., Verify P0335 and P0340 are in CKP_CMP_FAULT_DTCS., test_all_gates_pass_returns_valid(), test_ckp_cmp_fault_dtcs_bounds() (+3 more)

### Community 32 - "Community 32"
Cohesion: 0.17
Nodes (12): _healthy_pids(), No O2 DTCs in active_dtcs → gate passes., P0130 (first O2 DTC) → O2_FAULT_ACTIVE., Return a PID dict where all 8 precondition gates should pass., dfco_active is False → gate passes., Missing coolant_temp_c → ENGINE_COLD., fuel_sys_status == Closed_Loop → gate passes., test_gate1_ect_missing() (+4 more)

### Community 33 - "Community 33"
Cohesion: 0.24
Nodes (9): PIDValidationError, OBDLab custom exception hierarchy., Raised when a PID violates physical_sensor_bounds.json (§3.1)., aggregate(), Trim vector aggregator per OBDLab_KG_Wiki.md §12.  Computes total_trim_correctio, Aggregate STFT + LTFT per bank into trim correction deltas.      Source: OBDLab_, Coerce value to float, raising PIDValidationError on None., _safe_float() (+1 more)

### Community 34 - "Community 34"
Cohesion: 0.20
Nodes (7): AnalyticsPreconditions, Analytics precondition gate per OBDLab_KG_Wiki.md §9.  Evaluates the 8 precondit, Evaluate the 8 analytics-precondition gates per §9.      Returns the first gate, SensorSignalTranslator — OBDLab pipeline orchestrator per §2.1.  Wires togethe, OBDLab pipeline orchestrator — wires §3–§12 into one OBDLivePayload.      Publ, SensorSignalTranslator, translator()

### Community 35 - "Community 35"
Cohesion: 0.18
Nodes (11): 10.1 Formula (Speed-Density Ideal Gas), 10.2 Polymorphic routing (by VERoutingMode), 10.3 VE validation triggers, 10.3a Target VE constants for emulation branches, 10.4 Sub-module YAML config, 10. VE computation, code:block15 (VE (%) = [MAF(g/s) × 8.314 × (IAT(°C) + 273.15)]), code:block16 (VinDNA: air_metering_strategy) (+3 more)

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (10): 1. Standards anchored, 3.1 Boundary rules (`config/physical_sensor_bounds.json`), 3.2 Unit normalisation, 3. Input validation — physical sensor bounds, 5. OBDLivePayload — canonical output schema, 7. Alias normalization table, 9. Analytics preconditions, code:jsonc ({) (+2 more)

### Community 37 - "Community 37"
Cohesion: 0.24
Nodes (8): Run the full OBDLab pipeline and return an OBDLivePayload.          Pipeline o, compute_bucket(), _condition_matches(), Engine state bucketing per OBDLab_KG_Wiki.md §8.2.  Loads obd_translation_rules., Determine engine state bucket from sanitized PIDs and optional DNA view.      Pr, Check whether all conditions in a bucketing rule match., Evaluate a single condition against pids + dna_view., _rule_matches()

### Community 38 - "Community 38"
Cohesion: 0.22
Nodes (8): Deliverables (authored by architect *after* research; coded after that), Not runnable until, Research gate (answer before runnable scope is authored), Scope gate, Scope (one paragraph — precise after research), Success criteria / signal-noise, T-OBDV2-BANK-ASYM-1 — per-bank trim emit for bank asymmetry, Why this exists (the re-home)

### Community 39 - "Community 39"
Cohesion: 0.22
Nodes (8): Deliverables (authored by architect *after* research; coded after that), Not runnable until, Research gate (answer before runnable scope is authored), Scope gate, Scope (one paragraph — to be made precise after research), Success criteria / signal-noise, T-OBDV2-ECU-PERCEPT-1 — OBD perception-delta channel for `ecu_fault`, Why this exists (the split)

### Community 40 - "Community 40"
Cohesion: 0.36
Nodes (7): _load_bounds(), Drift guard for physical_sensor_bounds.json against OBDLab_KG_Wiki.md §3.1.  E, test_bank2_contract_present(), test_bound_row_matches_wiki(), test_bounds_field_count(), test_no_extra_fields(), test_source_wiki_present()

### Community 41 - "Community 41"
Cohesion: 0.25
Nodes (7): Drift-guard tests for obdlab.schemas.vocabulary against OBDLab_KG_Wiki.md., Every enum value must appear verbatim in OBDLab_KG_Wiki.md §6., REGULATORY_HIGH_IDLE is canonical (§6.1)., HIGH_IDLE_LOAD is BP-era and forbidden anywhere in obdlab/., test_high_idle_load_is_forbidden(), test_rpm_bucket_names_canonical(), test_wiki_drift_guard()

### Community 42 - "Community 42"
Cohesion: 0.25
Nodes (8): 11.1 Narrowband → lambda (NARROWBAND_VOLTAGE_TO_LAMBDA), 11.2 Wideband passthrough (WIDEBAND_PASSTHROUGH), 11.3 Wideband-in-NB-simulation (WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA), 11.4 Sensor bias detection rule, 11. O₂ Normalisation, code:block20 (Input: pid_o2_sensor_voltage_b1s1 (0.1 – 0.9 V)), code:block21 (Input: pid_wideband_equivalence_ratio (direct lambda/AFR val), code:block22 (Input: pid_oxygen_sensor_volts (0–1 V simulated NB signal fr)

### Community 43 - "Community 43"
Cohesion: 0.29
Nodes (7): Adjacent cylinder misfire rule, code:block29 (Misfire (incomplete combustion)), Domain reference — Misfire diagnostics (from `RefDocs/misfires/`), DTC pairing rules, Misfire type classification, OBD-II misfire monitor operation, Three root causes

### Community 44 - "Community 44"
Cohesion: 0.29
Nodes (7): 2.1 Processing sequence, 2.2 Directory structure, 2.3 Python class API (key signatures), 2. Module architecture, code:block1 ([User UI / Form Input]), code:block2 (obd_live_lab/), code:python (class PIDIngestionValidator:)

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (7): Catalyst monitor enable conditions, code:block27 (Step 1  Confirm ECT ≥ 70 °C at DTC set time (freeze-frame EC), Domain reference — Catalyst diagnostics (from `master_catalyst_guide.md`), False P0420 cluster, P0420 diagnosis sequence, Physical inspection thresholds, TWC operating envelope

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (7): code:block28 (Step 1  Warm idle), Domain reference — Vacuum / MAP diagnostics (from `RefDocs/vacuum-systems/`), EGR strategy divergence (critical for OBDLab VIN DNA routing), IAC count as vacuum leak indicator, MAP kPa reference (sea-level, closed throttle, warm idle), Snap throttle test, Vacuum gauge patterns

### Community 47 - "Community 47"
Cohesion: 0.33
Nodes (5): bank_2_null_contract, rule, source_wiki, bounds, source_wiki

### Community 48 - "Community 48"
Cohesion: 0.33
Nodes (5): Drift classification guide, Inventory, OBDLab Drift Inventory — 2026-05-25, Sanity check rows, Summary

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (6): 13.1 Ceiling table, 13.2 MatchType definitions, 13.3 Evidence tiers, 13.4 Widening derivation, 13. Top-3 confidence ceiling (statistical exit), code:text (PARTIAL = round(HIGH / 1.30, 2))

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (6): Domain reference — DTC classification (from `master_obd_guide.md`), DTC source weighting, DTC type / MIL behaviour, Freeze-frame rules, OBDLab DTC portability rules, Sanity rails

### Community 51 - "Community 51"
Cohesion: 0.40
Nodes (5): longft1, max, min, note, unit

### Community 52 - "Community 52"
Cohesion: 0.40
Nodes (5): shrtft2, max, min, note, unit

### Community 53 - "Community 53"
Cohesion: 0.40
Nodes (5): longft2, max, min, note, unit

### Community 54 - "Community 54"
Cohesion: 0.40
Nodes (5): shrtft1, max, min, note, unit

### Community 55 - "Community 55"
Cohesion: 0.40
Nodes (4): North-star scope gate (blocks everything), OBDLabV2 — Progress Ledger, Task log, Workflow (owner) — research-first, same for every lab

### Community 56 - "Community 56"
Cohesion: 0.40
Nodes (5): 12.1 Total Fuel Trim (TFT), 12.2 STFT/LTFT delta rules, 12.3 Bank comparison (V engines), 12. Trim vector computation, code:block23 (total_trim_correction_delta    = shrtft1 + longft1    (Bank )

### Community 57 - "Community 57"
Cohesion: 0.40
Nodes (5): 4.1 Thermal gate, 4.2 Closed-loop sanity gate, 4. Semantic consistency rules (Physics Gates), code:block4 (gate_thermal_stabilization:), code:block5 (gate_closed_loop:)

### Community 58 - "Community 58"
Cohesion: 0.40
Nodes (5): 8.1 Bucket definitions, 8.2 YAML bucketing rules (`obd_translation_rules.yaml`), 8.3 `STRESS_IDLE` RPM per VIN, 8. Engine state bucketing, code:yaml (state_bucketing_rules:)

### Community 59 - "Community 59"
Cohesion: 0.40
Nodes (5): Cam vs ignition timing distinction, Domain reference — Ignition timing system (from `RefDocs/ignition-timing/`), Spark burn line analysis (oscilloscope), Spark plug condition diagnostics, Timing advance rationale

### Community 60 - "Community 60"
Cohesion: 0.40
Nodes (5): code:block26 (B1S1  =  Bank 1, upstream (pre-cat — primary feedback sensor), Domain reference — O₂ sensor diagnostics (from `master_o2_sensor_guide.md`), DTC families by sensor position, Pre-cat ↔ post-cat switching ratio (catalyst masking), Sensor position canonical names

### Community 61 - "Community 61"
Cohesion: 0.50
Nodes (4): coolant_temp_c, max, min, unit

### Community 62 - "Community 62"
Cohesion: 0.50
Nodes (4): engine_rpm, max, min, unit

### Community 63 - "Community 63"
Cohesion: 0.50
Nodes (4): intake_air_temp_c, max, min, unit

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (4): calculated_engine_load_pct, max, min, unit

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (4): manifold_vacuum_kpa, max, min, unit

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (4): mass_airflow_gps, max, min, unit

### Community 67 - "Community 67"
Cohesion: 0.50
Nodes (4): 5-gas / OBD correlation table, Domain reference — Advanced powertrain clusters (from `OBDadd1.md`), Ghost Misfire rule (from `OBD_VOCABULARY.md §18.4`), Powertrain cluster classification (fault family routing)

### Community 68 - "Community 68"
Cohesion: 0.50
Nodes (4): code:block25 (Measure TFT at STABILIZED_IDLE (SI) and STRESS_IDLE (StI).), Domain reference — Fuel trim diagnostics (from `master_fuel_trim_guide.md`), Supplementary trim techniques, Trim-pattern RPM-dependence decision tree

## Knowledge Gaps
- **451 isolated node(s):** `source_wiki`, `min`, `max`, `unit`, `min` (+446 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ObdLabDnaView` connect `Community 2` to `Community 1`, `Community 34`, `Community 5`, `Community 17`, `Community 18`, `Community 19`, `Community 20`, `Community 24`, `Community 27`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Why does `SemanticConsistencyChecker` connect `Community 17` to `Community 2`, `Community 3`, `Community 34`, `Community 20`, `Community 28`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Why does `_make_checker()` connect `Community 3` to `Community 17`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Are the 40 inferred relationships involving `OBDLivePayload` (e.g. with `MatchType` and `_EvidenceTier`) actually correct?**
  _`OBDLivePayload` has 40 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `_dna_view()` (e.g. with `ObdLabDnaView` and `ObdEmissionsView`) actually correct?**
  _`_dna_view()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Map OBDLab evidence signatures to canonical diagnostic families.  This module is`, `Return the OBDLab-reachable family for a typed evidence signature.      Args:`, `Rank OBDLab evidence signatures into internal candidate scores.  This module doe` to the rest of the system?**
  _724 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05328218243819267 - nodes in this community are weakly interconnected._