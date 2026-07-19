# Graph Report - C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\vinlab\tests  (2026-06-13)

## Corpus Check
- Corpus is ~7,981 words - fits in a single context window. You may not need a graph.

## Summary
- 542 nodes · 567 edges · 27 communities (20 shown, 7 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 17 edges (avg confidence: 0.8)
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
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]

## God Nodes (most connected - your core abstractions)
1. `_make_full_payload()` - 21 edges
2. `TestVinDNAFromJsonInvalidEnum` - 11 edges
3. `_safe_decode()` - 10 edges
4. `TestPreCleanAndChassisNumberError` - 10 edges
5. `TestVinDNAFromJsonMissingRequired` - 10 edges
6. `make_stress_profile()` - 7 edges
7. `emissions` - 6 edges
8. `emissions` - 6 edges
9. `emissions` - 6 edges
10. `emissions` - 6 edges

## Surprising Connections (you probably didn't know these)
- `test_euro1_naturally_aspirated_uses_legacy_baseline()` --calls--> `make_stress_profile()`  [INFERRED]
  unit/test_stress_rpm.py → conftest.py
- `test_euro2_small_naturally_aspirated_uses_small_displacement_target()` --calls--> `make_stress_profile()`  [INFERRED]
  unit/test_stress_rpm.py → conftest.py
- `test_euro4_large_naturally_aspirated_uses_large_displacement_target()` --calls--> `make_stress_profile()`  [INFERRED]
  unit/test_stress_rpm.py → conftest.py
- `test_euro5_turbo_uses_boost_target()` --calls--> `make_stress_profile()`  [INFERRED]
  unit/test_stress_rpm.py → conftest.py
- `test_euro6_gdi_uses_high_pressure_fuel_target()` --calls--> `make_stress_profile()`  [INFERRED]
  unit/test_stress_rpm.py → conftest.py

## Communities (27 total, 7 thin omitted)

### Community 1 - "Community 1"
Cohesion: 0.04
Nodes (28): Decoder tests — exercises RobustVINDecoder against the actual vinlab/data/ artef, Keyword detection is case-insensitive., Year character mapping to pre-1990 raises VINDecodeError., North American VIN with bad checksum digit raises VINDecodeError., VIN with vin[8]='Z' skips checksum and proceeds to decode., VIN shorter than 17 chars raises ChassisNumberError (subclass of VINDecodeError), VIN with I/O chars gets cleaned first; with pre_clean=False it still raises., VIN with unresolvable WMI raises VINDecodeError. (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (33): NamedTuple, str, Build artifact sanity checks — skipped if vinlab/data/ is empty., vref.db engine_ref table contains rows (68 as of T-VL-3 build)., engine_ref has the required schema columns., wmi.csv first row is a header with required columns., wmi.csv contains thousands of WMI entries., Year code 'L' has exactly two rows (1990 ERA_1, 2020 ERA_3). (+25 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 6 - "Community 6"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 7 - "Community 7"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 8 - "Community 8"
Cohesion: 0.06
Nodes (33): Sanity tests for VinDNA instantiation and enum values., rated_rpm serializes and deserializes with VinDNA., B58B30 fixture reads P14_rated_rpm median from the vref baseline., No resolved engine code means no rated_rpm overlay., All enums must use exact contract §8 strings., PFI' must not appear — only PORT_INJECTION is valid per contract §8., Every enum-shaped field must carry its StrEnum instance, not a bare str., Default-constructed VinDNA fields must still be StrEnum instances. (+25 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (11): _make_full_payload(), Tests for VinDNA.from_json deserialization., Legacy payloads without resolved_horizon derive it from euro_emission_category., EURO_1 without resolved_horizon derives HORIZON_LEGACY., Nested fields should use defaults when keys are absent., from_json must reject payloads with invalid enum strings (T-FX-5)., Minimal VinDNA with only vin should round-trip through from_json., CoC fields not in payload should remain None. (+3 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (29): SEMANTIC_CONTRACT.md §9 conformance tests., §9.2: induction_type is always a contract enum value., §9.2: confidence is always a contract enum value., §9.2: euro_emission_category is always a contract enum value., §9.2: air_metering_strategy is always a contract enum value., §9.2: primary_load_calculation is always a contract enum value., §9.3: has_maf/has_map, strategy, and load_calculation are consistent., §9.3: downstream_o2_present is True for model year >= 1996 (OBD-II mandate). (+21 more)

### Community 11 - "Community 11"
Cohesion: 0.08
Nodes (23): _build_mini_data_dir(), csv_cases(), _data_available(), data_dir(), decoder(), make_mini_data_dir(), make_switch_profile(), mini_data_dir() (+15 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (10): T-FX-4: pre_clean_vin() + ChassisNumberError for wrong-length inputs., I characters → 1 substitution., O characters → 0 substitution., Multiple I and O characters all substituted., Already-clean VIN is uppercased and stripped but not otherwise changed., len != 17 raises ChassisNumberError, not generic VINDecodeError., ChassisNumberError is catchable as VINDecodeError., 16-char input with pre_clean still raises ChassisNumberError. (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.20
Nodes (3): Tests for air_metering classification module — all 4 (has_maf, has_map) combinat, TestClassifyAirMetering, TestDecoderIntegration

### Community 14 - "Community 14"
Cohesion: 0.20
Nodes (9): Standalone verification — vinlab imports without MySQL or requests., vinlab imports cleanly when mysql.connector is absent., vinlab imports cleanly when requests is absent., vinlab imports cleanly with both mysql.connector and requests absent., decode() works with mysql and requests mocked absent., test_decode_without_network_dependencies(), test_import_without_both(), test_import_without_mysql() (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.36
Nodes (8): make_stress_profile(), Isolation tests for vinlab.overlay.stress_rpm., test_euro1_naturally_aspirated_uses_legacy_baseline(), test_euro2_small_naturally_aspirated_uses_small_displacement_target(), test_euro4_large_naturally_aspirated_uses_large_displacement_target(), test_euro5_turbo_uses_boost_target(), test_euro6_gdi_uses_high_pressure_fuel_target(), test_unrecognised_euro_falls_back_to_horizon()

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (5): T-FX-1: European-market VINs skip NHTSA checksum (data-driven WMI→country)., _EUROPEAN_COUNTRIES frozenset has at least 20 member states., North American VIN with correct checksum still validates (no false bypass)., North American VIN with wrong checksum still raises (bypass only for EU)., TestEuropeanChecksumBypass

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (4): VIN with vin[9]='L' and legacy WMI → resolves to 1990., VIN with vin[9]='L' and modern WMI → resolves to 2020., Unrecognised era_hint triggers flag, not silent fallback.          Strategy (b):, TestLYearDisambiguation

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (4): VF1CB05CF25935016 — Renault Clio 1.2, 2002, Port Injection., VF1357K0F17697151 — Renault Clio 1.2, model year 2001., SALLN12P0YAXXXXXX — Land Rover, no engine in CSV or vref.db → NONE., TestValidDecodes

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (5): Isolation tests for vinlab.overlay.horizon., All EuroEmissionCategory values map per SEMANTIC_CONTRACT.md section 6.4., Year bands follow VINlookup.md's 1990-2000, 2001-2010, 2011+ split., test_euro_to_horizon_matches_contract(), test_year_to_horizon_matches_vinlookup_bands()

## Knowledge Gaps
- **175 isolated node(s):** `has_maf_sensor`, `has_map_sensor`, `primary_load_calculation`, `air_metering_strategy`, `co2_type_approval` (+170 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `test_io_vin_not_blocked_by_invalid_chars()` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Why does `TestPreCleanAndChassisNumberError` connect `Community 12` to `Community 1`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **What connects `Shared fixtures for VINLab tests.`, `Check that all required data files exist.`, `Path to vinlab/data/. Skip all tests if data files are missing.` to the rest of the system?**
  _294 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.0425531914893617 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.0425531914893617 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05537098560354374 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.05263157894736842 - nodes in this community are weakly interconnected._