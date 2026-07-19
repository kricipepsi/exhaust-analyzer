# Graph Report - tests  (2026-06-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 699 nodes · 915 edges · 39 communities (28 shown, 11 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `16705b61`
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

## God Nodes (most connected - your core abstractions)
1. `_valid_raw()` - 55 edges
2. `_payload()` - 25 edges
3. `_dna_view()` - 23 edges
4. `_valid_payload_dict()` - 20 edges
5. `run_sanitize()` - 18 edges
6. `raw_freeze_frame` - 13 edges
7. `raw_freeze_frame` - 13 edges
8. `raw_freeze_frame` - 13 edges
9. `raw_freeze_frame` - 13 edges
10. `raw_freeze_frame` - 13 edges

## Surprising Connections (you probably didn't know these)
- `_build_ff_from_row()` --calls--> `map_fuel_status()`  [INFERRED]
  test_cases.py → conftest.py
- `test_csv_cases_dtclab()` --calls--> `is_fail_closed()`  [INFERRED]
  test_cases.py → conftest.py
- `test_dna_gate()` --calls--> `is_fail_closed()`  [INFERRED]
  generative/test_combinatorial.py → conftest.py
- `test_garbage_freeze_frame_types()` --calls--> `is_fail_closed()`  [INFERRED]
  generative/test_fuzz.py → conftest.py
- `test_randomized_fuzz_batch()` --calls--> `is_fail_closed()`  [INFERRED]
  generative/test_fuzz.py → conftest.py

## Communities (39 total, 11 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (59): _dna_view(), _monitor(), _payload(), Tests for dtclab.ranking — per-family confidence from §16 weights + §14.2 DNA ga, A single CONFIRMED DTC contributes weight 1.0 from §16., A PERMANENT DTC contributes weight 1.0 from §16., A PENDING DTC contributes weight 0.5 from §16., A Mode $06 CRITICAL_FAIL contributes weight 0.7 from §16 on an active family. (+51 more)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (45): _description, dna_view_json, air_metering_strategy, confidence, emissions, euro_emission_category, make, model (+37 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (39): Unit tests for DTCLabPayload Pydantic constraint enforcement.  Covers: valid rou, A DTC string not matching DTC_REGEX in confirmed_dtcs raises     ValidationError, A malformed DTC in pending_dtcs is also caught., A malformed DTC in permanent_dtcs is also caught., The BP-form character class B-D,P,U is rejected by the canonical regex.      P01, Lowercase DTC codes do not match the canonical regex (case-sensitive)., A 4-character DTC does not match the 5-character canonical form., Passing a raw string not in DTCRoutingTag raises ValidationError     carrying ER (+31 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (35): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (35): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+27 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (34): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+26 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (34): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+26 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (31): _dna_view(), End-to-end integration tests for the full DTCLab pipeline.  Covers: HIGH-confide, Full pipeline: HIGH-confidence DNA with catalyst-equipped car.      P0171 → LEAN, CATALYST_HISTORY is suppressed when has_catalyst=False with HIGH confidence., CATALYST_HISTORY is emitted when has_catalyst=True with HIGH confidence., EGR_HISTORY is suppressed when egr_equipped=False with HIGH confidence.      Tes, With dna_view=None, all tags emit unconditionally on DTC pattern match     (the, The output of sanitize() passes DTCLabPayload.model_validate. (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (30): _bogus_gate_yaml(), _dna_view(), Unit tests for RoutingTagMapper — DNA-gated DTC→tag fan-out.  Covers: basic fa, P0430 also routes to CATALYST_HISTORY with same gate logic., POA_HISTORY has no DTC-pattern mapping — it is injected by COMLab., Transmission DTCs (P0700) are recognised by regex but not mapped., Return a routing YAML string with an unrecognised dna_gate name., An unknown dna_gate name triggers the fail-open branch.      Under HIGH-confid (+22 more)

### Community 9 - "Community 9"
Cohesion: 0.08
Nodes (23): DNA view schema drift guard (T-P0-2).  Verifies DtcLabDnaView, DtcEmissionsView,, Every DNA-view enum value must appear verbatim in DTC_VOCABULARY.md., DtcLabDnaView must round-trip through model_validate with all fields., DtcLabDnaView must accept confidence=NONE (no-DNA fallback)., DtcLabDnaView must be importable from dtclab.schemas.dna_view only., DtcLabDnaView must have all 8 canonical fields from DTC_VOCABULARY.md §14., DtcEmissionsView must have the 2 bool flags from DTC_VOCABULARY.md §14., EuroEmissionCategory must have 8 values per DTC_VOCABULARY.md §14.1. (+15 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (18): Freeze-frame context PIDs classify to the correct HistoricalFaultContext.      g, Tests for historical_context_classifier per DTC_VOCABULARY.md §9., RPM < 1000 alone is not enough; load must also be < 25., Load < 25 alone is not enough; RPM must also be < 1000., Idle is checked before load in priority order., ECT < 60 must return COLD_START_TRANSIT_FAULT even when RPM/load match idle., ECT < 60 always wins regardless of RPM/load values., Wiki says ECT < 60 (strict); ECT=60 is not cold start. (+10 more)

### Community 11 - "Community 11"
Cohesion: 0.16
Nodes (21): _empty_payload(), _freeze_frame(), _payload_with_dtcs(), _payload_with_tags(), Tests for classify_top3 — DTCLab Phase 2 top-3 emission.  Verifies: ≤3 output, c, Every confidence must be in [0.0, 1.0]., Clamp is min(max(x,0),1) — no family-keyed or tier-keyed constant., No duplicate families in output; first occurrence carries max confidence. (+13 more)

### Community 12 - "Community 12"
Cohesion: 0.16
Nodes (5): Return a valid 12-mandatory-PID raw dict, with optional overrides., §12.1 explicitly permits negative coolant_temp_c., TestFieldConstraints, TestFlagLoadHighLowRpm, _valid_raw()

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (19): Tests for dtclab.family_map — routing-tag → canonical-family map.  Covers: every, Context-only tags (None) are excluded from output., First occurrence determines position in output., Every one of the 17 DTCRoutingTag values is a key in the map., POA_HISTORY maps to None — COMLab injects it from GASLab., DESIGN §2 direct mappings match., Every non-None value in ROUTING_TAG_TO_FAMILY is in CANONICAL_FAMILIES., CANONICAL_FAMILIES must have 16 entries (COMLab FaultFamilyLit). (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (17): _build_dna_view_for_case(), Discrete combinatorial suite for DTCLab (T-TST-9).  Lab-local generator — the sh, Build the appropriate dna_view (or None) for a DNA-gate test case., DNA-gated tags emit/drop per confidence and hardware presence.      gt_source: D, dna_view=None ≡ VinConfidence.NONE — emit gated tag unconditionally., VinConfidence.PARTIAL — emit gated tag (advisory)., VinConfidence.HIGH without hardware → gated tag DROPPED., Temporarily force RoutingTagMapper.map to return [] → suite MUST fail.      This (+9 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (14): _make_dict(), Tests for dtclab.core.mode06_evaluator — margin tri-state classifier.  Covers: m, Direct port of the verification block structural checks., Mode06MonitorResult Pydantic model enforces the MID key regex., N ≥ 5 monitors against the same dictionary path open the file ≤ 1 time., Write a minimal MID dictionary into *tmp_path* and return the path., test_component_lookup_known_mid(), test_dictionary_loaded_at_most_once() (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.14
Nodes (15): _build_args(), build_dtclab_descriptor(), _diff(), _entry_point(), _extract_expected(), _map_fuel_status(), _parse_dtc_cell(), DTCLab ModuleDescriptor for the generative test harness.  Discrete lab — no cont (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (15): _discover_fixture_paths(), _load_fixture(), Regression tests wired to the DTCLab case corpus.  Each case is a standalone JSO, Every JSON fixture file is valid JSON and has required keys., At least one fixture uses a HIGH-confidence DNA view and at least     one uses d, Case 04 (non-start) specifically asserts MID_21_TID_81 is CRITICAL_FAIL., Case 05 (self-healing delta) asserts STFT +22 and LTFT +11 are     present in th, Return all case_*.json fixture files sorted by name. (+7 more)

### Community 18 - "Community 18"
Cohesion: 0.12
Nodes (7): Unit tests for freeze_frame_extractor — FreezeFrameRecord + derived flags.  Cove, Cold start, open-loop fault, high-load low-rpm stall, IAT/ECT         biased, se, Replicate the exact structural smoke test from the task file., TestAllFlags, TestExtendedPIDs, TestFlagOpenLoop, TestStructuralSmoke

### Community 19 - "Community 19"
Cohesion: 0.12
Nodes (8): T-FU-4: None-valued PIDs, non-numeric strings, coercible strings., A present-but-None mandatory PID is treated as missing., A non-numeric PID string (e.g. 'abc') raises ValidationError., Pydantic coerces '800' → 800 and flags derive correctly., Derived flags must be correct when PIDs are supplied as strings., Pydantic coerces StrEnum from string via the record-first path., None in extended PID is passthrough (not mandatory)., TestInputRobustness

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (14): build_gt_source(), main(), parse_dtc_cell(), project_row(), T-TST-7: Project dtclab_cases.csv from the reconciled master CSV.  Reads the rec, Write projected rows to the DTCLab fixture CSV., Generate the DTCLab projected fixture from the reconciled master., Split a master DTC cell into tokens without validating DTC syntax. (+6 more)

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (5): Tests for dtclab.core.dtc_ingestion_gate — DTC format validation.  Covers: valid, BP-form DTC 'B-D001' must raise DTCFormatError (wiki §2.3 note)., Validation stops at the first malformed code., test_bp_form_explicitly_rejected(), test_fails_on_first_invalid()

### Community 22 - "Community 22"
Cohesion: 0.15
Nodes (13): _mutate_dtc(), Fail-closed input-contract fuzz suite for DTCLab (T-TST-9).  Lab-local fuzz gene, Malformed OBD mode keys raise ValueError.      gt_source: DTC_VOCABULARY.md §3 (, Missing mandatory PIDs raise FreezeFrameIncompleteError.      gt_source: DTC_VOC, Malformed Mode $06 inputs are fail-closed.      gt_source: DTC_VOCABULARY.md §13, Apply one random mutation to a DTC code., Seeded randomized fuzz — 50 mutated inputs, all fail-closed.      gt_source: DTC, Print the fuzz seed so failures are reproducible. (+5 more)

### Community 23 - "Community 23"
Cohesion: 0.20
Nodes (14): Cold-start (ECT < 60) dominates idle conditions per §9 priority rule., P0128 in OL_FAULT → COOLANT_SYSTEM_MALFUNCTION.      gt_source: CoolantLeakSig.m, P0302 in CL → CYLINDER_FLUID_MISFIRE.      gt_source: CoolantLeakSig.md §4; DTC_, test_cold_start_priority_over_idle(), test_coolant_system_malfunction_cross_field(), test_cylinder_fluid_misfire_cross_field(), Garbage types in freeze-frame fields raise ValidationError or ValueError.      g, test_garbage_freeze_frame_types() (+6 more)

### Community 24 - "Community 24"
Cohesion: 0.17
Nodes (11): classify_context_oracle(), dtclab_csv_path(), dtclab_csv_rows(), map_fuel_status(), parse_dtc_cell(), Pytest configuration and shared fixtures for dtclab tests.  Shared oracle helper, Mirror of classify_historical_context per DTC_VOCABULARY.md §9., Path to the dtclab_cases.csv fixture (T-TST-7 output). (+3 more)

### Community 25 - "Community 25"
Cohesion: 0.23
Nodes (11): _build_ff_from_row(), _has_ff_core(), _load_csv_rows(), _make_row_id(), pytest_generate_tests(), Parametrized characterization net over dtclab_cases.csv (T-TST-9).  All 194 rows, Load all rows from dtclab_cases.csv., True if the row has ect, rpm, and load values. (+3 more)

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (8): Every exemplar DTC routes to exactly its declared tag.      gt_source: DTC_VOCAB, MIL flags and fuel_status round-trip through the pipeline.      gt_source: DTC_V, test_mil_fuel_roundtrip(), test_routing_tag_exact_match(), Every DTC string mutation is fail-closed.      gt_source: DTC_VOCABULARY.md §2.3, test_dtc_string_fuzz(), is_fail_closed(), True if the outcome is fail-closed: typed error or schema-valid payload.      Fa

### Community 27 - "Community 27"
Cohesion: 0.25
Nodes (7): Vocabulary drift guard.  Verifies every enum value in dtclab/schemas/vocabulary., Every enum value must appear verbatim in DTC_VOCABULARY.md., DTC_REGEX must match DTC_VOCABULARY.md §10 canonical form., The BP regex form must not appear in any Python source under dtclab/., test_bp_regex_is_forbidden(), test_dtc_regex_matches_vocab(), test_wiki_drift_guard()

## Knowledge Gaps
- **158 isolated node(s):** `_description`, `_source_case`, `$03`, `$07`, `$0A` (+153 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_valid_raw()` connect `Community 12` to `Community 32`, `Community 33`, `Community 34`, `Community 18`, `Community 19`, `Community 28`, `Community 29`, `Community 30`, `Community 31`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `run_sanitize()` connect `Community 23` to `Community 10`, `Community 14`, `Community 22`, `Community 24`, `Community 26`?**
  _High betweenness centrality (0.007) - this node is a cross-community bridge._
- **Why does `test_csv_cases_dtclab()` connect `Community 23` to `Community 25`, `Community 26`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **Are the 15 inferred relationships involving `run_sanitize()` (e.g. with `test_csv_cases_dtclab()` and `test_routing_tag_exact_match()`) actually correct?**
  _`run_sanitize()` has 15 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Pytest configuration and shared fixtures for dtclab tests.  Shared oracle helper`, `Split a DTC cell on comma or pipe, strip whitespace, drop empties.`, `Map a CSV fuel_status value to the enum; None if empty/unrecognised.` to the rest of the system?**
  _360 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.05310734463276836 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.043478260869565216 - nodes in this community are weakly interconnected._