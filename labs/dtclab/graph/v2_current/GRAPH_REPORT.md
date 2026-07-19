# Graph Report - 4DLabV2\labs\dtclab  (2026-06-06)

## Corpus Check
- 46 files · ~40,125 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1072 nodes · 1540 edges · 91 communities (79 shown, 12 thin omitted)
- Extraction: 83% EXTRACTED · 17% INFERRED · 0% AMBIGUOUS · INFERRED: 266 edges (avg confidence: 0.73)
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
- [[_COMMUNITY_Community 82|Community 82]]
- [[_COMMUNITY_Community 83|Community 83]]
- [[_COMMUNITY_Community 84|Community 84]]

## God Nodes (most connected - your core abstractions)
1. `extract_freeze_frame()` - 64 edges
2. `_valid_raw()` - 55 edges
3. `RoutingTagMapper` - 42 edges
4. `rank_candidates()` - 35 edges
5. `_payload()` - 31 edges
6. `_dna_view()` - 30 edges
7. `DataFusionSanitizer` - 29 edges
8. `FreezeFrameIncompleteError` - 21 edges
9. `FuelSystemStatus` - 21 edges
10. `_valid_payload_dict()` - 21 edges

## Surprising Connections (you probably didn't know these)
- `test_regression_case()` --calls--> `DataFusionSanitizer`  [INFERRED]
  tests/regression/test_dtclab_regression.py → dtclab/core/data_fusion_sanitizer.py
- `test_case04_mode06_critical_fail()` --calls--> `DataFusionSanitizer`  [INFERRED]
  tests/regression/test_dtclab_regression.py → dtclab/core/data_fusion_sanitizer.py
- `test_case05_trim_values_present()` --calls--> `DataFusionSanitizer`  [INFERRED]
  tests/regression/test_dtclab_regression.py → dtclab/core/data_fusion_sanitizer.py
- `test_dtc_format_error_str_contains_code_and_mode()` --calls--> `DTCFormatError`  [INFERRED]
  tests/unit/test_dtc_ingestion_gate.py → dtclab/core/dtc_ingestion_gate.py
- `test_valid_code_passes()` --calls--> `validate_dtc_list()`  [INFERRED]
  tests/unit/test_dtc_ingestion_gate.py → dtclab/core/dtc_ingestion_gate.py

## Communities (91 total, 12 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (74): _build_family_index(), _dna_factor_for_family(), _load_routing_rules(), _match_type_for_weight(), rank_candidates(), DTCLab Phase 2 scorer — per-family confidence from §16 weights + §14.2 DNA gatin, Build family → tags and family → dna_gate_names indices.      Returns:         (, Return the DNA confidence multiplier for *family*.      Ungated families always (+66 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (51): _matches_any(), DNA-gated routing-tag engine.  map() — pure DTC-to-tag function. No external inp, Evaluate the strict hardware-presence check for HIGH confidence., True if *dtc* matches at least one compiled regex in *patterns*., Maps confirmed DTC codes to DTCRoutingTag values with DNA-gate filtering.      C, Return the deduplicated routing tags for *confirmed_dtcs*.          Args:, Return True if *tag* is allowed through its DNA gate.          No gate → always, RoutingTagMapper (+43 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (47): DataFusionSanitizer, DataFusionSanitizer — public surface that wires the full DTCLab pipeline.  Inges, Wires the full DTCLab compilation pipeline into a single public surface.      Co, _dna_view(), End-to-end integration tests for the full DTCLab pipeline.  Covers: HIGH-confide, Full pipeline: HIGH-confidence DNA with catalyst-equipped non-GPF car.      P017, CATALYST_HISTORY is suppressed when has_catalyst=False with HIGH confidence., CATALYST_HISTORY is emitted when has_catalyst=True with HIGH confidence. (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.04
Nodes (48): 10. Fuel Pressure Regulator Diaphragm Rupture, 11. GM Passkey III / Transponder Key Recognition Failure, 12. Ford Fuel Pump Driver Module (FPDM) Corrosion Failure, 13. Mazda PCV Hose Collapse (Massive Unmetered Vacuum Leak), 14. Chrysler Totally Integrated Power Module (TIPM) Internal Relay Failure, 15. Volvo Electronic Throttle Module (ETM) Magneti-Marelli Failure, 16. BMW Direct-Injection High-Pressure Fuel Pump (HPFP) Failure (N54 Engine), 17. Nissan Crankshaft Position (CKP) / Camshaft Position (CMP) Sensor Solder Defect (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.04
Nodes (46): _description, dna_view_json, air_metering_strategy, confidence, emissions, euro_emission_category, make, model (+38 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (46): _description, dna_view_json, air_metering_strategy, confidence, emissions, euro_emission_category, make, model (+38 more)

### Community 6 - "Community 6"
Cohesion: 0.04
Nodes (46): 0. Module purpose & data-isolation invariant, 10.1 Lean signatures, 10.2 Rich signatures, 10.3 Misfire signatures, 10.4 Catalyst and EGR signatures, 10.5 Stoichiometric reference (healthy engine), 10. Domain reference — Gas Lab signature → DTC reverse-lookup, 11.1 Vocabulary (+38 more)

### Community 7 - "Community 7"
Cohesion: 0.07
Nodes (39): Unit tests for DTCLabPayload Pydantic constraint enforcement.  Covers: valid rou, A DTC string not matching DTC_REGEX in confirmed_dtcs raises     ValidationError, A malformed DTC in pending_dtcs is also caught., A malformed DTC in permanent_dtcs is also caught., The BP-form character class B-D,P,U is rejected by the canonical regex.      P01, Lowercase DTC codes do not match the canonical regex (case-sensitive)., A 4-character DTC does not match the 5-character canonical form., Passing a raw string not in DTCRoutingTag raises ValidationError     carrying ER (+31 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (35): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.06
Nodes (35): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+27 more)

### Community 10 - "Community 10"
Cohesion: 0.06
Nodes (34): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+26 more)

### Community 11 - "Community 11"
Cohesion: 0.06
Nodes (34): _description, dna_view_json, expected_flags, ff_codes_cleared_invalidated, ff_ect_warmup, ff_load_high_at_low_rpm, ff_open_loop_at_fault, ff_timing_retard_severe (+26 more)

### Community 12 - "Community 12"
Cohesion: 0.10
Nodes (30): classify_margin(), evaluate_monitor(), _load_dictionary(), _lookup_component(), Mode $06 on-board monitor evaluator — margin tri-state classifier.  Source: DTC_, Classify a Mode $06 margin percentage into its tri-state.      Source: DTC_VOCAB, Return the target component name for *mid_hex* from the dictionary.      Returns, Return the parsed Mode $06 hex dictionary at *path*.      Cached per distinct *p (+22 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (27): classify_historical_context(), Historical fault context classifier.  Derives a HistoricalFaultContext enum valu, Classify the historical context at the moment a DTC was stored.      Priority or, Tests for historical_context_classifier per DTC_VOCABULARY.md §9., RPM < 1000 alone is not enough; load must also be < 25., Load < 25 alone is not enough; RPM must also be < 1000., RPM > 2000 alone is not enough; load must also be > 45., Load > 45 alone is not enough; RPM must also be > 2000. (+19 more)

### Community 14 - "Community 14"
Cohesion: 0.11
Nodes (22): Compile raw OBD-II inputs into a validated ``DTCLabPayload``.          Args:, DTCFormatError, DTC ingestion gate — validates raw DTC strings against the canonical regex.  Sou, Raised when a DTC string does not match the canonical regex.      Source: DTC_VO, Validate every code in *codes* against the canonical DTC regex.      Args:, validate_dtc_list(), evaluate_coolant_dtc_context(), Evaluate cross-field DTC + fuel status for fluid intrusion signatures.      Retu (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.12
Nodes (13): FreezeFrameIncompleteError, Raised when one or more mandatory freeze-frame PIDs are missing., FuelSystemStatus, Fuel system loop status at freeze-frame capture.      Source: DTC_VOCABULARY.md, Unit tests for freeze_frame_extractor — FreezeFrameRecord + derived flags.  Cove, Cold start, open-loop fault, high-load low-rpm stall, IAT/ECT         biased, se, Replicate the exact structural smoke test from the task file., TestAllFlags (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (23): classify_top3(), Top-3 (family, confidence∈[0,1]) candidates for Bayesian fusion (FU-1).      Cal, _empty_payload(), _freeze_frame(), _payload_with_dtcs(), _payload_with_tags(), Tests for classify_top3 — DTCLab Phase 2 top-3 emission.  Verifies: ≤3 output, c, Every confidence must be in [0.0, 1.0]. (+15 more)

### Community 17 - "Community 17"
Cohesion: 0.08
Nodes (23): DNA view schema drift guard (T-P0-2).  Verifies DtcLabDnaView, DtcEmissionsView,, Every DNA-view enum value must appear verbatim in DTC_VOCABULARY.md., DtcLabDnaView must round-trip through model_validate with all fields., DtcLabDnaView must accept confidence=NONE (no-DNA fallback)., DtcLabDnaView must be importable from dtclab.schemas.dna_view only., DtcLabDnaView must have all 8 canonical fields from DTC_VOCABULARY.md §14., DtcEmissionsView must have the 4 bool flags from DTC_VOCABULARY.md §14., EuroEmissionCategory must have 8 values per DTC_VOCABULARY.md §14.1. (+15 more)

### Community 18 - "Community 18"
Cohesion: 0.09
Nodes (22): families_for_tags(), Canonical family mapping for DTCLab routing tags.  Maps each DTCRoutingTag (19-v, Return deduplicated, ordered canonical families for active routing tags.      St, Tests for dtclab.family_map — routing-tag → canonical-family map.  Covers: every, Context-only tags (None) are excluded from output., First occurrence determines position in output., Every one of the 18 DTCRoutingTag values is a key in the map., POA_HISTORY maps to None — COMLab injects it from GASLab. (+14 more)

### Community 19 - "Community 19"
Cohesion: 0.18
Nodes (5): Return a valid 12-mandatory-PID raw dict, with optional overrides., §12.1 explicitly permits negative coolant_temp_c., TestFieldConstraints, TestFlagIATEctBiased, _valid_raw()

### Community 20 - "Community 20"
Cohesion: 0.12
Nodes (16): 1. The DTC Lab Architectural Component Tree, 2. Complete Data Flow Timeline inside the DTC Lab Module, 2. Module System Architecture, 3.2 Script 2: data_fusion_sanitizer.py, 3. Step-by-Step Developer Implementation Guide for the DTC Lab## Step 3.1: Create Module Directory Structure, 3. Structural Component Breakdown## 3.1 Script 1: diagnostic_trouble_compiler.py, 4. Decoupled Configuration Specifications## 4.1 Hexadecimal Test Directory Layout (mode_06_hex_dictionary.json), 4. Verification Check Script for the DTC Lab Module (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.21
Nodes (4): extract_freeze_frame(), Validate mandatory PIDs and derive 6 symptom flags from *raw*.      Args:, TestFlagLoadHighLowRpm, TestFlagTimingRetard

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (8): T-FU-4: None-valued PIDs, non-numeric strings, coercible strings., A present-but-None mandatory PID is treated as missing., A non-numeric PID string (e.g. 'abc') raises ValidationError., Pydantic coerces '800' → 800 and flags derive correctly., Derived flags must be correct when PIDs are supplied as strings., Pydantic coerces StrEnum from string via the record-first path., None in extended PID is passthrough (not mandatory)., TestInputRobustness

### Community 23 - "Community 23"
Cohesion: 0.18
Nodes (15): _discover_fixture_paths(), _load_fixture(), Regression tests wired to the DTCLab case corpus.  Each case is a standalone JSO, Every JSON fixture file is valid JSON and has required keys., At least one fixture uses a HIGH-confidence DNA view and at least     one uses d, Case 04 (non-start) specifically asserts MID_21_TID_81 is CRITICAL_FAIL., Case 05 (self-healing delta) asserts STFT +22 and LTFT +11 are     present in th, Return all case_*.json fixture files sorted by name. (+7 more)

### Community 24 - "Community 24"
Cohesion: 0.20
Nodes (12): Single DTC-pattern → tag mapping with optional DNA gate., _RoutingRule, CandidateScore, MatchType, Evidence-strength tier derived from the strongest contributing source.      Sour, Single fault-family candidate with raw confidence and evidence tier.      Fields, DtcLabDnaView, Confidence tier of the VIN-to-DNA resolution.      Source: DTC_VOCABULARY.md §14 (+4 more)

### Community 25 - "Community 25"
Cohesion: 0.14
Nodes (13): 11. `DTCLabPayload` — top-level JSON contract, 15. DTC → routing-tag mapping table, 16. Confidence weights per DTC state, 18. What this vocab explicitly does NOT define, 19. Standards references (sources), 1. Standards anchored, 3. OBD-II service modes consumed, 5. `DTCSeverityClass` — 4 values (+5 more)

### Community 26 - "Community 26"
Cohesion: 0.24
Nodes (10): DTCSeverityClass, DTCState, HistoricalFaultContext, Mode06MonitorState, DTCLab canonical vocabulary — StrEnums, DTC_REGEX, and confidence weights.  All, DTC severity tier per SAE J2012 §6.      Source: DTC_VOCABULARY.md §5., OBD-II DTC confirmation state — reserved contract surface.      Not consumed by, Mode $06 on-board monitor test result tri-state.      Source: DTC_VOCABULARY.md (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.25
Nodes (8): BaseModel, DtcEmissionsView, Emissions-equipment flags that gate DNA-screened routing tags.      Source: DTC_, FreezeFrameRecord, FreezeFrameRecord — Mode $02 snapshot at fault confirmation.  Every field name i, Mode $02 freeze-frame snapshot captured at DTC confirmation.      Source: DTC_VO, DTCLabPayload, Top-level DTCLab output — the single JSON payload at the COMLab boundary.      S

### Community 28 - "Community 28"
Cohesion: 0.25
Nodes (7): _derive_iat_ect_bias(), _derive_load_high_low_rpm(), _derive_open_loop(), Freeze-frame extractor — validates Mode $02 data and derives symptom flags.  Sou, ff_open_loop_at_fault: loop status is open-loop, open-loop drive, or     open-lo, ff_load_high_at_low_rpm: high load at low RPM.      wiki: DTC_VOCABULARY.md §12., ff_iat_ect_biased: IAT/ECT delta > 30 °C at zero RPM.      wiki: DTC_VOCABULARY.

### Community 29 - "Community 29"
Cohesion: 0.25
Nodes (7): AirMeteringStrategy, EuroEmissionCategory, DTCLab-owned DNA view schema — typed replacement for the loose dict form.  Every, Euro emissions standard tier for the identified vehicle.      Source: DTC_VOCABU, Primary air-metering strategy of the identified vehicle.      Source: DTC_VOCABU, Vehicle technology horizon resolved from VIN decoding.      Source: DTC_VOCABULA, ResolvedHorizon

### Community 30 - "Community 30"
Cohesion: 0.25
Nodes (7): Vocabulary drift guard.  Verifies every enum value in dtclab/schemas/vocabulary., Every enum value must appear verbatim in DTC_VOCABULARY.md., DTC_REGEX must match DTC_VOCABULARY.md §10 canonical form., The BP regex form must not appear in any Python source under dtclab/., test_bp_regex_is_forbidden(), test_dtc_regex_matches_vocab(), test_wiki_drift_guard()

### Community 31 - "Community 31"
Cohesion: 0.29
Nodes (7): 14.1 Enums referenced by the view, 14.2 Confidence-gated behaviour, 14.3 Where the view comes from, 14. `DtcLabDnaView` — DNA-first input contract (NEW), code:python (class DtcLabDnaView(BaseModel):), code:python (class EuroEmissionCategory(StrEnum):), code:block15 (UI → DNALab.build_vehicle_dna(vin, triage) → VehicleDNA)

### Community 32 - "Community 32"
Cohesion: 0.33
Nodes (5): A1, name, source_wiki, _description, _source_wiki

### Community 33 - "Community 33"
Cohesion: 0.33
Nodes (6): 2.1 System class characters, 2.2 Subgroup digit, 2.3 Canonical regex, 2. DTC code structure (per SAE J2012), code:block1 (P  0  1  7  1), code:python (DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$")

### Community 34 - "Community 34"
Cohesion: 0.33
Nodes (6): 13.1 MID/TID key form, 13.2 Universal MID inventory (CAN-equipped vehicles, 2008+), 13.3 Universal MID range reference (prose form), 13. `Mode06MonitorResult` schema, code:python (class Mode06MonitorResult(BaseModel):), code:block12 ("MID_<HEX>_TID_<HEX>")

### Community 39 - "Community 39"
Cohesion: 0.50
Nodes (4): 12.1 Mandatory PIDs — 12 fields, 12.2 Extended PIDs — optional, 12.3 Derived symptom flags — 6 bool fields, 12. `FreezeFrameRecord` schema (§10 of predecessor wiki)

### Community 40 - "Community 40"
Cohesion: 0.50
Nodes (4): 17.1 Wire entry point, 17.2 Cross-boundary field ownership, 17.3 Ingestion failure routing, 17. COMLab integration contract (§24 of predecessor wiki)

### Community 41 - "Community 41"
Cohesion: 0.50
Nodes (4): 4.1 Per-value DNA gate summary, 4.2 DTC-to-routing-tag fan-out (prose anchor), 4. `DTCRoutingTag` — 19-value enum, code:python (from enum import StrEnum)

### Community 42 - "Community 42"
Cohesion: 0.67
Nodes (3): 01, name, source_wiki

### Community 43 - "Community 43"
Cohesion: 0.67
Nodes (3): 02, name, source_wiki

### Community 44 - "Community 44"
Cohesion: 0.67
Nodes (3): 05, name, source_wiki

### Community 45 - "Community 45"
Cohesion: 0.67
Nodes (3): 06, name, source_wiki

### Community 46 - "Community 46"
Cohesion: 0.67
Nodes (3): 13, name, source_wiki

### Community 47 - "Community 47"
Cohesion: 0.67
Nodes (3): 21, name, source_wiki

### Community 48 - "Community 48"
Cohesion: 0.67
Nodes (3): 22, name, source_wiki

### Community 49 - "Community 49"
Cohesion: 0.67
Nodes (3): 31, name, source_wiki

### Community 50 - "Community 50"
Cohesion: 0.67
Nodes (3): 32, name, source_wiki

### Community 51 - "Community 51"
Cohesion: 0.67
Nodes (3): 33, name, source_wiki

### Community 52 - "Community 52"
Cohesion: 0.67
Nodes (3): 34, name, source_wiki

### Community 53 - "Community 53"
Cohesion: 0.67
Nodes (3): 35, name, source_wiki

### Community 54 - "Community 54"
Cohesion: 0.67
Nodes (3): 36, name, source_wiki

### Community 55 - "Community 55"
Cohesion: 0.67
Nodes (3): 37, name, source_wiki

### Community 56 - "Community 56"
Cohesion: 0.67
Nodes (3): 38, name, source_wiki

### Community 57 - "Community 57"
Cohesion: 0.67
Nodes (3): 39, name, source_wiki

### Community 58 - "Community 58"
Cohesion: 0.67
Nodes (3): 3A, name, source_wiki

### Community 59 - "Community 59"
Cohesion: 0.67
Nodes (3): 3B, name, source_wiki

### Community 60 - "Community 60"
Cohesion: 0.67
Nodes (3): 3C, name, source_wiki

### Community 61 - "Community 61"
Cohesion: 0.67
Nodes (3): 3D, name, source_wiki

### Community 62 - "Community 62"
Cohesion: 0.67
Nodes (3): 71, name, source_wiki

### Community 63 - "Community 63"
Cohesion: 0.67
Nodes (3): 81, name, source_wiki

### Community 64 - "Community 64"
Cohesion: 0.67
Nodes (3): 82, name, source_wiki

### Community 65 - "Community 65"
Cohesion: 0.67
Nodes (3): A2, name, source_wiki

### Community 66 - "Community 66"
Cohesion: 0.67
Nodes (3): A3, name, source_wiki

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (3): A4, name, source_wiki

### Community 68 - "Community 68"
Cohesion: 0.67
Nodes (3): A5, name, source_wiki

### Community 69 - "Community 69"
Cohesion: 0.67
Nodes (3): A6, name, source_wiki

### Community 70 - "Community 70"
Cohesion: 0.67
Nodes (3): A7, name, source_wiki

### Community 71 - "Community 71"
Cohesion: 0.67
Nodes (3): A8, name, source_wiki

### Community 72 - "Community 72"
Cohesion: 0.67
Nodes (3): A9, name, source_wiki

### Community 73 - "Community 73"
Cohesion: 0.67
Nodes (3): E1, name, source_wiki

### Community 74 - "Community 74"
Cohesion: 0.67
Nodes (3): 7.1 Universal MID groups (prose anchor), 7. `Mode06MonitorState` — 3 values, code:python (class Mode06MonitorState(StrEnum):)

## Knowledge Gaps
- **394 isolated node(s):** `_source_wiki`, `_description`, `name`, `source_wiki`, `name` (+389 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Mode06MonitorResult` connect `Community 12` to `Community 0`, `Community 26`, `Community 27`, `Community 7`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `DataFusionSanitizer` connect `Community 2` to `Community 1`, `Community 14`, `Community 23`, `Community 24`, `Community 27`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `extract_freeze_frame()` connect `Community 21` to `Community 35`, `Community 36`, `Community 38`, `Community 75`, `Community 14`, `Community 15`, `Community 19`, `Community 22`, `Community 27`, `Community 28`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Are the 58 inferred relationships involving `extract_freeze_frame()` (e.g. with `.sanitize()` and `FreezeFrameRecord`) actually correct?**
  _`extract_freeze_frame()` has 58 INFERRED edges - model-reasoned connections that need verification._
- **Are the 35 inferred relationships involving `RoutingTagMapper` (e.g. with `DataFusionSanitizer` and `DtcLabDnaView`) actually correct?**
  _`RoutingTagMapper` has 35 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `rank_candidates()` (e.g. with `test_state_weight_sourced_from_s16_confirmed()` and `test_state_weight_sourced_from_s16_permanent()`) actually correct?**
  _`rank_candidates()` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 2 inferred relationships involving `_payload()` (e.g. with `DTCLabPayload` and `FreezeFrameRecord`) actually correct?**
  _`_payload()` has 2 INFERRED edges - model-reasoned connections that need verification._