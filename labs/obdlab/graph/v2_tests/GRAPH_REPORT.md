# Graph Report - obdlab_tests  (2026-07-06)

## Corpus Check
- 41 files · ~22,895 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 878 nodes · 1196 edges · 61 communities (37 shown, 24 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 48 edges (avg confidence: 0.78)
- Token cost: 0 input · 0 output

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

## God Nodes (most connected - your core abstractions)
1. `_make_validator()` - 39 edges
2. `OBDLivePayload` - 32 edges
3. `_canonical_kwargs()` - 32 edges
4. `_healthy_pids()` - 30 edges
5. `_dna_view()` - 28 edges
6. `_dna_view()` - 26 edges
7. `_dual_pids()` - 22 edges
8. `_warm_idle_input()` - 21 edges
9. `_pids()` - 20 edges
10. `_make_checker()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `_build_dna_view()` --calls--> `AirMeteringStrategy`  [INFERRED]
  fixtures/descriptor.py → conftest.py
- `_build_dna_view()` --calls--> `O2SensorType`  [INFERRED]
  fixtures/descriptor.py → conftest.py
- `test_csv_bounce_rate()` --calls--> `is_signal_bearing()`  [INFERRED]
  test_cases.py → conftest.py
- `test_csv_bounce_rate()` --calls--> `build_inputs_from_csv_row()`  [INFERRED]
  test_cases.py → conftest.py
- `test_boundary_channel_move_rate()` --calls--> `point_in_box()`  [INFERRED]
  generative/test_boundary.py → conftest.py

## Import Cycles
- None detected.

## Communities (61 total, 24 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (67): _dna_view(), _dual_pids(), _expected_ve(), Tests for VEEngine — 3-branch polymorphic routing per OBDLab_KG_Wiki.md §10., MAF_ONLY — back-calc MAP, bucket=REGULATORY_HIGH_IDLE., DUAL at STRESS_IDLE ~4000 RPM., DUAL at STABILIZED_IDLE ~650 RPM (low end of idle band)., DUAL with cold intake air (-10°C). (+59 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (65): OBDLivePayload, _canonical_kwargs(), Tests for OBDLivePayload Pydantic model per OBDLab_KG_Wiki.md §5., coolant_temp_c at min (-40) and max (140) accepted., calculated_engine_load_pct at 0 and 100 accepted., shrtft1 at min (-127) and max (127) accepted (widened OBD-rail bounds)., normalized_obd_lambda at 0.7 and 1.3 accepted., mass_airflow_gps null (None) is accepted (MAP_ONLY routing). (+57 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (54): _dna_view(), Tests for O2Normalizer — 2-branch O2 normalisation per OBDLab_KG_Wiki.md §11., Wideband equivalence ratio passes through unchanged., Wideband ratio outside [0.7, 1.3] returns O2_CHANNEL_FAULT with clamped lambda., Boundary values 0.7 and 1.3 are valid and pass through., Without DNA, narrowband is assumed and narrowband input is accepted., When DNA says NARROWBAND but pid_oxygen_sensor_volts is missing., When DNA says WIDEBAND but pid_wideband_equivalence_ratio is missing. (+46 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (48): _dna_high(), ObdLabDnaView, End-to-end tests for SensorSignalTranslator per T-P0-8.  Covers:   - HIGH-confid, Payload model_dump_json round-trips cleanly., dna_view=None: pipeline uses DUAL_MAF_MAP + NARROWBAND defaults., dna_view=None → narrowband O2 path (pid_oxygen_sensor_volts used)., ECT < 75 → COLD_OPEN_LOOP_INVALID, analytics frozen, payload emitted., ECT = 74.0 (just below 75 threshold) triggers cold override. (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (45): PIDIngestionValidator, _make_dna(), _make_validator(), ObdLabDnaView, Tests for PIDIngestionValidator — boundary checks, unit conversions, DNA-RPM thr, When both canonical and alternate are present, keep canonical, drop alternate., DNA-HIGH with rated_rpm=None still gets static 0..8000 check., test_bank2_contract_one_bank_both_null_passes() (+37 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (43): SemanticConsistencyChecker, _make_checker(), _make_dna(), _pids(), ObdLabDnaView, Tests for SemanticConsistencyChecker — 3 Physics Gates, thermal gate, closed-loo, ECT=40, Open_Loop_Cold → no error (engine is genuinely cold)., shrtft1=-5, longft1=-10 → no error (within safety range). (+35 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (40): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+32 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (39): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+31 more)

### Community 8 - "Community 8"
Cohesion: 0.05
Nodes (36): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+28 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (36): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+28 more)

### Community 10 - "Community 10"
Cohesion: 0.05
Nodes (36): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+28 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (31): case_id, dna_view_json, air_metering_strategy, confidence, cylinder_count, engine_displacement_liters, induction_type, rated_rpm (+23 more)

### Community 12 - "Community 12"
Cohesion: 0.07
Nodes (28): case_id, dna_view_json, expected_payload_subset, calculated_engine_load_pct, coolant_temp_c, engine_rpm, engine_warmed, longft2 (+20 more)

### Community 13 - "Community 13"
Cohesion: 0.09
Nodes (12): NamedTuple, Path, EnumAnchor, _find_comlab_vocab(), Drift-guard tests for obdlab.schemas.dna_view against canonical wiki sources.  O, Drift-guard tests for obdlab.schemas.vocabulary against OBDLab_KG_Wiki.md., Every enum value must appear verbatim in OBDLab_KG_Wiki.md §6., REGULATORY_HIGH_IDLE is canonical (§6.1). (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (19): _dna_view(), Unit tests for MAF linearity calculations and translator integration., Verify that fields are None when dna_view is None (no displacement)., Verify that fields are None when strategy is not DUAL_MAF_MAP_CROSSCHECK., Verify emitter discipline: no diagnostic verdicts are emitted in payload., Verify state isolation and order independence of the translator., Test W_theo calculation with standard parameters., Test delta calculation for clean MAF sensor. (+11 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (18): AirMeteringStrategy, build_air_metering_strategy(), build_inputs_from_csv_row(), build_o2_sensor_type(), is_signal_bearing(), _lambda_to_nb_voltage(), _parse_float(), _parse_int() (+10 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (16): _dna_narrowband(), _dna_wideband(), ObdLabDnaView, Tests for OBD perception-delta channel for ecu_fault (T-OBDV2-ECU-PERCEPT-1)., Wideband upstream O2 + commanded_equivalence_ratio calculates lambda_perception_, Non-numeric commanded_equivalence_ratio raises a PIDValidationError., Verify OBDLab stays an emitter and does not construct fault-family verdicts., Even if commanded_equivalence_ratio is present, narrowband upstream O2 defaults (+8 more)

### Community 17 - "Community 17"
Cohesion: 0.14
Nodes (13): _assert_field(), _load_fixture_files(), Regression test suite for OBDLab — parametrized over JSON fixture files.  Each f, At least 5 regression fixtures are present., Verify regression fixtures cover HIGH, None, and PARTIAL DNA confidence., Yield (case_id, fixture_dict) for every JSON file in fixtures/., Resolve an expected value, supporting the '_approx' suffix for float tolerance., Assert a single payload field against expected value. (+5 more)

### Community 18 - "Community 18"
Cohesion: 0.20
Nodes (15): _build_args(), _build_dna_view(), _coerce_float(), _coerce_int(), _diff(), _extract_expected(), Any, ObdLabDnaView (+7 more)

### Community 19 - "Community 19"
Cohesion: 0.12
Nodes (15): Tests for TrimVectorAggregator per OBDLab_KG_Wiki.md §12., shrtft1 + longft1 with number_of_banks == 1 returns (bank1, None, None)., All four trim fields summed per-bank when number_of_banks == 2., Bank-2 None fields are ignored when number_of_banks == 1., number_of_banks == 2 but shrtft2 is None raises PIDValidationError., number_of_banks == 2 but longft2 is None raises PIDValidationError., Missing shrtft1 raises PIDValidationError., Missing longft1 raises PIDValidationError. (+7 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (11): Integration smoke test — exercises the full OBDLab pipeline end-to-end.  Covers:, STRESS_IDLE bucket with wideband O2 passthrough., engine_rpm > 8000 raises PIDValidationError., Cold engine (ECT=40°C) + dna_view=None → COLD_OPEN_LOOP_INVALID, analytics froze, Minimal valid input + dna_view=None → payload emitted, JSON round-trips., 2-bank V-engine: both bank-1 and bank-2 trims in payload., test_smoke_2_bank_v_engine(), test_smoke_bounds_violation() (+3 more)

### Community 21 - "Community 21"
Cohesion: 0.17
Nodes (11): Tests for AnalyticsPreconditions per OBDLab_KG_Wiki.md §9.  8 gates × (PASS + FA, throttle_pos == 90 → WOT_ACTIVE., Missing throttle_pos → gate passes (treat as not-WOT)., Healthy PID dict with semantic_gates_passed=True → VALID., Verify P0130 and P0161 are in O2_FAULT_DTCS (range endpoints)., Verify P0335 and P0340 are in CKP_CMP_FAULT_DTCS., test_all_gates_pass_returns_valid(), test_ckp_cmp_fault_dtcs_bounds() (+3 more)

### Community 22 - "Community 22"
Cohesion: 0.17
Nodes (12): _healthy_pids(), No O2 DTCs in active_dtcs → gate passes., P0130 (first O2 DTC) → O2_FAULT_ACTIVE., Return a PID dict where all 8 precondition gates should pass., dfco_active is False → gate passes., Missing coolant_temp_c → ENGINE_COLD., fuel_sys_status == Closed_Loop → gate passes., test_gate1_ect_missing() (+4 more)

### Community 23 - "Community 23"
Cohesion: 0.25
Nodes (10): build_gt_source(), derive_has_maf(), derive_has_map(), derive_number_of_banks(), main(), T-TST-6: Project obdlab_cases.csv from the reconciled master CSV.  Reads the rec, Derive number_of_banks from bank_config field., Derive has_maf from MAF column presence. (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (9): channel_moved_for_box(), point_in_box(), Any, Return True if *point* lies geometrically inside *box_dims*.      Each dimension, Return True if the payload's discriminating channel moved for *box_sig*.      Ea, _centroid(), A2 — Combinatorial generator: pairwise corner sweep over fault boxes.  For each, A2 combinatorial: pairwise corners, ≥95% channel-move on interior. (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.27
Nodes (9): _centroid(), _eps_for(), _is_continuous_dim(), A2 — Boundary generator: per-dimension edge-point sweep over fault boxes.  For e, Enum/equality dimensions have lo == hi; continuous have lo < hi., Pick epsilon based on dimension type., Compute the centroid of a box., A2 boundary: ≥ 95% channel-move rate on interior points. (+1 more)

### Community 26 - "Community 26"
Cohesion: 0.24
Nodes (9): Unit tests for T-OBDV2-BANK-ASYM-1 (per-bank trim delta and emitter discipline)., Single-bank engines must emit None for per_bank_trim_delta., V-engines (2-bank) must compute B1 - B2 as a signed float., OBDLab must not emit any bank-asymmetry verdict or fault labels., Return a valid raw user input dict for warm steady idle tests., test_emitter_only_discipline(), test_single_bank_trim_delta_is_none(), test_v_engine_trim_delta_is_float() (+1 more)

### Community 27 - "Community 27"
Cohesion: 0.28
Nodes (8): _load_sourced_cases(), parse_comparison(), Verify the 8-cell coverage matrix and that all-default shape is < 5% of non-reje, Load sourced cases from logset.json., Helper to parse threshold-string comparison rules (e.g. '>+15', '<50')., Run SensorSignalTranslator.translate on each case and assert expected results., test_coverage_matrix_and_aggregate_rate(), test_pid_logset_case()

### Community 28 - "Community 28"
Cohesion: 0.36
Nodes (7): _load_bounds(), Drift guard for physical_sensor_bounds.json against OBDLab_KG_Wiki.md §3.1.  Ens, test_bank2_contract_present(), test_bound_row_matches_wiki(), test_bounds_field_count(), test_no_extra_fields(), test_source_wiki_present()

### Community 29 - "Community 29"
Cohesion: 0.33
Nodes (6): build_obdlab_descriptor(), Build the OBDLab ModuleDescriptor for the decision-rate harness.      Fault boxe, A2 — Fuzz generator: random envelope sampling, no-crash + round-trip gate.  Samp, Fuzz: random envelope points must not crash and must round-trip., test_fuzz_no_crash(), ModuleDescriptor

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (5): is_default_shape(), Return True when every discriminating channel is at its default/sentinel value., A1 — CSV-driven bounce-rate gate over obdlab_cases.csv.  Parametrises over the m, A1: bounce rate over obdlab_cases.csv must be < FLOOR_STANDALONE., test_csv_bounce_rate()

## Knowledge Gaps
- **234 isolated node(s):** `ObdLabDnaView`, `case_id`, `notes`, `engine_rpm`, `coolant_temp_c` (+229 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OBDLivePayload` connect `Community 1` to `Community 30`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `is_default_shape()` connect `Community 30` to `Community 1`, `Community 15`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Why does `build_obdlab_descriptor()` connect `Community 29` to `Community 24`, `Community 25`, `Community 18`, `Community 30`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Are the 31 inferred relationships involving `OBDLivePayload` (e.g. with `test_2_bank_payload()` and `test_calculated_engine_load_above_100_rejected()`) actually correct?**
  _`OBDLivePayload` has 31 INFERRED edges - model-reasoned connections that need verification._
- **What connects `ObdLabDnaView`, `Pytest configuration and shared fixtures for obdlab tests.  Provides the default`, `Return True when every discriminating channel is at its default/sentinel value.` to the rest of the system?**
  _494 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.052429667519181586 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05874125874125874 - nodes in this community are weakly interconnected._