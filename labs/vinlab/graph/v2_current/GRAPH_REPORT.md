# Graph Report - 4DLabV2\labs\vinlab  (2026-06-06)

## Corpus Check
- 80 files · ~97,712 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1364 nodes · 1723 edges · 92 communities (80 shown, 12 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.67)
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
- [[_COMMUNITY_Community 86|Community 86]]
- [[_COMMUNITY_Community 87|Community 87]]
- [[_COMMUNITY_Community 88|Community 88]]
- [[_COMMUNITY_Community 90|Community 90]]

## God Nodes (most connected - your core abstractions)
1. `Detailed Listing` - 107 edges
2. `Cylinder Count — Resolved Engine Codes` - 103 edges
3. `infer_cylinder()` - 49 edges
4. `VINDecodeError` - 29 edges
5. `ChassisNumberError` - 26 edges
6. `_make_full_payload()` - 23 edges
7. `TestVinDNAFromJsonInvalidEnum` - 23 edges
8. `TestVinDNAFromJsonMissingRequired` - 22 edges
9. `RobustVINDecoder` - 21 edges
10. `UpstreamO2Type` - 20 edges

## Surprising Connections (you probably didn't know these)
- `infer_cylinder()` --calls--> `Handler`  [INFERRED]
  vinlab/overlay/cylinder_heuristic.py → mysql_bridge.py
- `decoder()` --calls--> `RobustVINDecoder`  [INFERRED]
  tests/conftest.py → vinlab/decoder.py
- `test_bmw_n52b25()` --calls--> `infer_cylinder()`  [INFERRED]
  tests/test_cylinder_heuristic.py → vinlab/overlay/cylinder_heuristic.py
- `test_hyundai_g4ke()` --calls--> `infer_cylinder()`  [INFERRED]
  tests/test_cylinder_heuristic.py → vinlab/overlay/cylinder_heuristic.py
- `test_honda_k20a()` --calls--> `infer_cylinder()`  [INFERRED]
  tests/test_cylinder_heuristic.py → vinlab/overlay/cylinder_heuristic.py

## Communities (92 total, 12 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.02
Nodes (107): A.C. CARS (2 rows, 2 unique codes), ALFA ROMEO (16 rows, 16 unique codes), ASIA (1 rows, 1 unique codes), ASTON MARTIN (5 rows, 5 unique codes), AUDI (32 rows, 32 unique codes), AUSTIN (6 rows, 6 unique codes), AUSTIN HEALEY (1 rows, 1 unique codes), AUSTIN MORIS (1 rows, 1 unique codes) (+99 more)

### Community 1 - "Community 1"
Cohesion: 0.02
Nodes (103): ALFA ROMEO (3 codes), ASIA (1 codes), ASTON MARTIN (4 codes), AUDI (31 codes), AUSTIN (6 codes), AUSTIN HEALEY (1 codes), AUSTIN MORIS (1 codes), BENTLEY (4 codes) (+95 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (48): infer_cylinder(), Infer cylinder_count, engine_configuration, induction from engine code.      Ret, Unit tests for vinlab.overlay.cylinder_heuristic — T-VL-7., test_audi_as_vw_group(), test_bmw_b48(), test_bmw_m62_v8(), test_bmw_n20_turbo(), test_bmw_n52b25() (+40 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (34): AirMeteringClassification, classify_air_metering(), Air metering classification — single deep module replacing two parallel switches, One classification for the (has_maf, has_map) fact.      Contract §8:       prim, Return both air-metering labels from a single classification of (has_maf, has_ma, Tests for air_metering classification module — all 4 (has_maf, has_map) combinat, TestClassifyAirMetering, TestDecoderIntegration (+26 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (37): CylinderHint, _displacement_fallback(), _induction(), _infer_bmw(), _infer_honda(), _infer_hyundai_kia(), _infer_mazda(), _infer_mercedes() (+29 more)

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
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 9 - "Community 9"
Cohesion: 0.05
Nodes (37): air_metering_architecture, has_maf_sensor, has_map_sensor, primary_load_calculation, air_metering_strategy, co2_type_approval, co_high_idle, co_low_idle (+29 more)

### Community 10 - "Community 10"
Cohesion: 0.08
Nodes (23): Decoder tests — exercises RobustVINDecoder against the actual vinlab/data/ artef, Year character mapping to pre-1990 raises VINDecodeError., VF1CB05CF25935016 — Renault Clio 1.2, 2002, Port Injection., T-FX-2: VINs with pos[9] in {0, U, Z} decode with model_year=None., Regression guard: standard VIN must still resolve to concrete int., BMW VIN with engine_code in both CSV and vref.db hits db_row path., Most sample VINs from specimens CSV decode without error.          Some VINs may, At least one sample VIN should have non-NONE confidence. (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.07
Nodes (21): euro_to_horizon(), euro_emission_category -> Horizon enum mapping per SEMANTIC_CONTRACT §6.4., Map a calendar year to its architecture horizon.      Used only when euro_emissi, Map EuroEmissionCategory to architecture horizon per contract §6.4.      EURO_1,, _year_to_horizon(), VF1357K0F17697151 — Renault Clio 1.2, model year 2001., VIN with vin[9]='L' and legacy WMI → resolves to 1990., VIN with vin[9]='L' and modern WMI → resolves to 2020. (+13 more)

### Community 12 - "Community 12"
Cohesion: 0.09
Nodes (22): NamedTuple, Every enum-shaped field must carry its StrEnum instance, not a bare str., test_enum_fields_are_str_enum_instances(), Regression test: patched RobustVINDecoder pass rate on OPSI petrol M1 CSV.  Samp, Sampled pass rate must be >= 99.5% (chassis numbers excluded)., _Result, _run_sample(), StrEnum (+14 more)

### Community 13 - "Community 13"
Cohesion: 0.10
Nodes (9): _make_full_payload(), Tests for VinDNA.from_json deserialization., CoC fields not in payload should remain None., Legacy payloads without resolved_horizon derive it from euro_emission_category., EURO_1 without resolved_horizon derives HORIZON_LEGACY., Nested fields should use defaults when keys are absent., from_json must reject payloads with invalid enum strings (T-FX-5)., TestVinDNAFromJsonInvalidEnum (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.06
Nodes (30): source, effortLevel, enabledPlugins, superpowers@claude-plugins-official, ALLOW_DELETE_OPERATION, ALLOW_INSERT_OPERATION, ALLOW_UPDATE_OPERATION, MYSQL_DB (+22 more)

### Community 15 - "Community 15"
Cohesion: 0.09
Nodes (29): SEMANTIC_CONTRACT.md §9 conformance tests., §9.2: induction_type is always a contract enum value., §9.2: confidence is always a contract enum value., §9.2: euro_emission_category is always a contract enum value., §9.2: air_metering_strategy is always a contract enum value., §9.2: primary_load_calculation is always a contract enum value., §9.3: has_maf/has_map, strategy, and load_calculation are consistent., §9.3: downstream_o2_present is True for model year >= 1996 (OBD-II mandate). (+21 more)

### Community 16 - "Community 16"
Cohesion: 0.10
Nodes (27): _bool_to_int(), _derive_era(), ec_for_entry(), _extract_tecdoc(), _load_overrides(), _load_yaml_entries(), main(), _merge_tecdoc_into_yaml() (+19 more)

### Community 17 - "Community 17"
Cohesion: 0.07
Nodes (26): A.1 Top-level scalar fields, A.2 Air metering architecture (nested), A.3 Emissions (nested), A.4 Derived / polymorphic switch fields, B.1 Columns persisted into `vref.db`, B.2 Columns explicitly excluded, BUILD_DATA_SOURCES.md — VinDNA Field-to-Source Contract, C.1 Fields sourced from TecDoc (+18 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (26): StrEnum, TestVinDNAFromJsonRoundTrip, AirMeteringStrategy, _derive_horizon_from_euro(), DownstreamTrimRole, Emissions, EuroEmissionCategory, from_json() (+18 more)

### Community 19 - "Community 19"
Cohesion: 0.08
Nodes (25): car_119512, mixture_rows, prd_rows, car_120080, mixture_rows, prd_rows, car_126961, mixture_rows (+17 more)

### Community 20 - "Community 20"
Cohesion: 0.08
Nodes (23): Sanity tests for VinDNA instantiation and enum values., PFI' must not appear — only PORT_INJECTION is valid per contract §8., Default-constructed VinDNA fields must still be StrEnum instances., Emissions.downstream_trim_role defaults to NONE., Emissions can be constructed with each DownstreamTrimRole value., VinDNA.resolved_horizon defaults to HORIZON_MODERN., to_json() emits resolved_horizon as its string value., _derive_horizon_from_euro maps all 7 euro categories per contract §6.4. (+15 more)

### Community 21 - "Community 21"
Cohesion: 0.12
Nodes (23): assert_no_diesel(), _build_layer_query(), _connect(), _displacement_clause(), extract_uncovered(), _get_cylinder_count(), load_covered_vds(), main() (+15 more)

### Community 22 - "Community 22"
Cohesion: 0.13
Nodes (21): Exception, build(), _extract_era_hints(), _load_vpic_wmis(), Build wmi.csv from vPIC WMI data + petrol CSV era hints.  Emits vinlab/data/wmi., Return {wmi: {brand, country}} from vPIC for passenger-car WMIs., Scan petrol CSV and return {wmi: era_hint} based on B_first_reg_date.      era_h, Build wmi.csv. Returns row count written. (+13 more)

### Community 23 - "Community 23"
Cohesion: 0.09
Nodes (21): BMW, Chrysler / Dodge / Jeep, code:python (def decode_engine(engine_code, displacement, sample_vin, bra), code:python (#!/usr/bin/env python3), Decoding Formula for Missing Engine Fields, Final Output Example for a Few Codes, Ford, General Motors (Chevrolet, Opel, Daewoo, etc.) (+13 more)

### Community 24 - "Community 24"
Cohesion: 0.09
Nodes (21): all_groups_top100, assembly_groups, prd_mixture, prd_pressure, sample_car_prd, term_search, воздух, давлен (+13 more)

### Community 25 - "Community 25"
Cohesion: 0.12
Nodes (12): T-FX-4: pre_clean_vin() + ChassisNumberError for wrong-length inputs., I characters → 1 substitution., O characters → 0 substitution., Multiple I and O characters all substituted., Already-clean VIN is uppercased and stripped but not otherwise changed., len != 17 raises ChassisNumberError, not generic VINDecodeError., ChassisNumberError is catchable as VINDecodeError., 16-char input with pre_clean still raises ChassisNumberError. (+4 more)

### Community 26 - "Community 26"
Cohesion: 0.11
Nodes (18): eng_id_matches_car_id, model_3890, model_3891, model_3892, model_3893, model_3894, model_3895, model_3896 (+10 more)

### Community 27 - "Community 27"
Cohesion: 0.14
Nodes (14): str, vref.db engine_ref table contains rows (68 as of T-VL-3 build)., engine_ref has the required schema columns., TestVrefDb, test_io_vin_not_blocked_by_invalid_chars(), _enrich_from_csv(), _norm_euro_csv(), Normalize CSV V9_euro_class_full or euro_label to 'euroN' format. (+6 more)

### Community 28 - "Community 28"
Cohesion: 0.16
Nodes (17): append_to_csv(), build_output_row(), deduplicate(), format_displacement(), get_connection(), load_bridge_map(), load_existing_vds_keys(), main() (+9 more)

### Community 29 - "Community 29"
Cohesion: 0.12
Nodes (15): code:block1 (passanger_cars.id ← passanger_car_engines.id), code:block2 (passanger_cars.id ← passanger_car_pds.passangercarid), code:sql (SELECT COUNT(*) > 0 AS has_egr), code:sql (SELECT), Key Linkage Tables, MCP Server Status (BUILD-TIME ONLY), Query example: Does vehicle X have EGR?, Query example: Get all VIN parameters for a passenger car (+7 more)

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (15): detect_vvt(), get_connection(), get_existing_engine_codes(), insert_engine_row(), is_gdi(), is_turbo(), main(), map_valvetrain() (+7 more)

### Community 31 - "Community 31"
Cohesion: 0.19
Nodes (14): build_lookup(), _calc_coverage(), is_diesel(), main(), parse_resolved_md(), tools/backfill_cylinder_count.py  Reads docs/cylinder_count_resolved.md, filters, Build a case-insensitive lookup keyed by stripped engine_code.     If duplicate, Return True if the fuel_system_type string indicates diesel. (+6 more)

### Community 32 - "Community 32"
Cohesion: 0.14
Nodes (8): Build artifact sanity checks — skipped if vinlab/data/ is empty., wmi.csv first row is a header with required columns., wmi.csv contains thousands of WMI entries., Year code 'L' has exactly two rows (1990 ERA_1, 2020 ERA_3)., At least some vds_engine_map.csv engine codes exist in vref.db.          Full co, TestEngineCodeCoverage, TestWmiCsv, TestYearsCsv

### Community 33 - "Community 33"
Cohesion: 0.16
Nodes (13): _build_vds_engine_code_index(), _load_vref_coc_index(), Data-driven test suite for cases_petrol_master_v6.csv.  T1 — Decode passrate >=, Build {brand_vds_full: engine_code} and {brand_pos8: engine_code} indexes., Load vref.db engine_ref rows indexed by engine_code., VinDNA CoC fields match their authoritative source (vref.db)., >= 85 % of all 281 CSV VINs must decode without VINDecodeError., Every decoded VinDNA serializes to JSON matching DNALab/COMLab handoff contract. (+5 more)

### Community 34 - "Community 34"
Cohesion: 0.23
Nodes (13): get_connection(), is_diesel_code(), load_ktype_bridge(), main(), query_cylinder_by_displacement(), query_cylinder_by_engine_code(), query_cylinder_by_ktype(), tools/tecdoc_cylinder_enricher.py  Queries TecDoc MySQL for cylinder_count by en (+5 more)

### Community 35 - "Community 35"
Cohesion: 0.15
Nodes (12): **Architectural Analysis and Database Naming Conventions**, **Aston Martin VH Powertrain Evolution and Motorsports Utility**, **Conclusions and Database Auditing Guidelines**, **Deconstruction of Database Naming Suffixes and Prefixes**, **Executive Summary of Diagnostic Powertrain Auditing**, **Mazdean Utility Engines in Emerging Markets**, **Mechanical Profile of Validated Petrol Engines (1990–2020)**, **Powertrain Forensic Report: Cylinder Count and Architectural Analysis of Petrol Engines (Model Years 1990–2020)** (+4 more)

### Community 36 - "Community 36"
Cohesion: 0.18
Nodes (11): csv_cases(), _data_available(), data_dir(), decoder(), Shared fixtures for VINLab tests., Check that all required data files exist., Path to vinlab/data/. Skip all tests if data files are missing., Module-scoped decoder instance loaded once per test session. (+3 more)

### Community 37 - "Community 37"
Cohesion: 0.23
Nodes (11): build(), _get_vpic_db(), _pass_a_vpic(), _pass_b_petrol_csv(), _pass_c_pos8_legacy(), Build vds_engine_map.csv from vPIC + petrol CSV.  Three-pass builder:   Pass A (, Extract VDS engine profiles from petrol CSV.      CSV rows overwrite vPIC rows o, Extract position-8-only fallback patterns for legacy-era WMIs. (+3 more)

### Community 38 - "Community 38"
Cohesion: 0.25
Nodes (10): derive_cylinder_count(), extract(), is_diesel(), main(), Extract engine codes from OPSI DMV CSV files for 7 WMI groups.  Reads three Nio_, Write rows to output_path in vds_engine_map.csv column order., Derive cylinder count from displacement (safe default only)., Check if an engine code is a known diesel code. (+2 more)

### Community 39 - "Community 39"
Cohesion: 0.31
Nodes (10): build_cylinder_lookup(), build_suffix_lookup(), get_connection(), is_diesel_code(), main(), normalize_code(), tools/tecdoc_cyl_from_attributes.py  Queries TecDoc MySQL engine_attributes for, Match CSV codes that appear as a suffix of a TecDoc normalized code.      Handle (+2 more)

### Community 40 - "Community 40"
Cohesion: 0.18
Nodes (6): North American VIN with bad checksum digit raises VINDecodeError., VIN with vin[8]='Z' skips checksum and proceeds to decode., VIN shorter than 17 chars raises ChassisNumberError (subclass of VINDecodeError), VIN with I/O chars gets cleaned first; with pre_clean=False it still raises., VIN with unresolvable WMI raises VINDecodeError., TestValidation

### Community 41 - "Community 41"
Cohesion: 0.20
Nodes (8): Keyword detection is case-insensitive., Direct test of the H1 fuel keyword guard., TestH1PetrolOnly, _is_non_petrol(), _normalise_euro(), RobustVINDecoder — per VINlookup.md (patched) with overlay rules.  Adaptive VI, Normalise a raw euro_norm string to the contract enum form., Check any value for non-petrol fuel keywords (H1 guard).

### Community 42 - "Community 42"
Cohesion: 0.29
Nodes (3): is_diesel_code(), main(), tools/tecdoc_cyl_from_codes.py  Derives cylinder_count from manufacturer engine-

### Community 43 - "Community 43"
Cohesion: 0.25
Nodes (7): 2. False Logic Prevention, 3. Targeted OBD Request Routing, Complete Universal Triage & Diagnostic Mapping Diagram, How the Code Processes the Diagram Inputs (JSON Rule Payload), Step-by-Step App Workflow for the User, The Combined Vehicle DNA Diagnostic Payload, Three Ways This Data Streamlines Your Backend App Logic## 1. Smart UI Optimization (Dynamic Form Fields)

### Community 44 - "Community 44"
Cohesion: 0.25
Nodes (5): T-FX-1: European-market VINs skip NHTSA checksum (data-driven WMI→country)., _EUROPEAN_COUNTRIES frozenset has at least 20 member states., North American VIN with correct checksum still validates (no false bypass)., North American VIN with wrong checksum still raises (bypass only for EU)., TestEuropeanChecksumBypass

### Community 45 - "Community 45"
Cohesion: 0.29
Nodes (6): By brand, code:block1 (HJY683411   FKA44621    0526/AS     00526A88079   AK00515), Possible next steps, Top 30 unresolved engine codes, Unresolved Cylinder Count Report — 2026-05-20, Why these remain unresolved

### Community 46 - "Community 46"
Cohesion: 0.29
Nodes (6): first_maf_car_engine, maf_cars, map_cars, model_prd_mixture_count, unique_engines_with_maf, unique_engines_with_map

### Community 47 - "Community 47"
Cohesion: 0.29
Nodes (6): engine_prd, engines, passanger_car_engines, passanger_car_prd, passanger_cars, prd

### Community 48 - "Community 48"
Cohesion: 0.29
Nodes (6): 1. The Redesigned Relational CSV Layout, 2. Implementation: The Robust Adaptive VIN Decoder, 3. Verification Test Code Trace, diagnostic_mvp/core/vin_decoder.pyimport reimport csvfrom typing import Dict, Any, test_legacy_vin.pyfrom diagnostic_mvp.core.vin_decoder import RobustVINDecoderimport json, Updated File: vds_engine_map.csv

### Community 49 - "Community 49"
Cohesion: 0.33
Nodes (5): lookup_engine_ref(), open_vref_readonly(), SQL isolation layer for vref.db — all SQL strings live here (H8).  The decoder c, Query vref.db engine_ref for tech-mask and CoC measurements.      Args:, Open vref.db in read-only mode via URI.      The decoder calls this once in __in

### Community 50 - "Community 50"
Cohesion: 0.33
Nodes (4): derive_upstream_o2_type(), Derived field computation for upstream O2 sensor type., Return the upstream O2 sensor type per contract §8 UpstreamO2Type enum.      Arg, vref.db o2_type=NB hint honoured even for year>=2001 fuel-injected.

### Community 51 - "Community 51"
Cohesion: 0.33
Nodes (3): BaseHTTPRequestHandler, Handler, mysql_bridge.py — local HTTP bridge so the Claude sandbox can query TecDoc. Run

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (4): T-FX-7: heuristic config wires into number_of_banks., SCFDAM2S1A1234567 — Aston Martin, heuristic → V12 → 2 banks., Subaru EE20 Boxer engine → engine_config BOXER_4 → 2 banks., TestHeuristicBanks

### Community 53 - "Community 53"
Cohesion: 0.40
Nodes (4): load_table(), main(), Create tecdoc tables and load CSV data. One-shot setup., total_columns includes row_id auto-increment. CSV has total_columns-1 cols.

### Community 54 - "Community 54"
Cohesion: 0.50
Nodes (3): engine class -> stress_idle_rpm_target mapping.  Per OBD_VOCABULARY.md §3.2: the, Return the stress-idle RPM target for a given vehicle profile.      Args:, stress_idle_rpm()

### Community 55 - "Community 55"
Cohesion: 0.50
Nodes (4): car_10_model_187, map_rows, mixture_rows, prd_rows

### Community 56 - "Community 56"
Cohesion: 0.50
Nodes (4): car_1_model_5598, map_rows, mixture_rows, prd_rows

### Community 57 - "Community 57"
Cohesion: 0.50
Nodes (4): car_2_model_164, map_rows, mixture_rows, prd_rows

### Community 58 - "Community 58"
Cohesion: 0.50
Nodes (4): car_3_model_7867, map_rows, mixture_rows, prd_rows

### Community 59 - "Community 59"
Cohesion: 0.50
Nodes (4): car_4_model_164, map_rows, mixture_rows, prd_rows

### Community 60 - "Community 60"
Cohesion: 0.50
Nodes (4): car_5_model_164, map_rows, mixture_rows, prd_rows

### Community 61 - "Community 61"
Cohesion: 0.50
Nodes (4): car_6_model_164, map_rows, mixture_rows, prd_rows

### Community 62 - "Community 62"
Cohesion: 0.50
Nodes (4): car_7_model_1608, map_rows, mixture_rows, prd_rows

### Community 63 - "Community 63"
Cohesion: 0.50
Nodes (4): car_8_model_164, map_rows, mixture_rows, prd_rows

### Community 64 - "Community 64"
Cohesion: 0.50
Nodes (4): car_9_model_164, map_rows, mixture_rows, prd_rows

### Community 65 - "Community 65"
Cohesion: 0.50
Nodes (3): manufacturers, manufacturers_sample, models

### Community 66 - "Community 66"
Cohesion: 0.50
Nodes (3): _coerce_enum_values(), Serialize to a JSON-safe dict matching SEMANTIC_CONTRACT.md §4.1.          Uses, Recursively convert Enum members to their .value form.

### Community 67 - "Community 67"
Cohesion: 0.67
Nodes (3): load_table(), main(), Load TecDoc CSV data into MySQL for VINLab.

## Knowledge Gaps
- **576 isolated node(s):** `defaultMode`, `model`, `type`, `command`, `superpowers@claude-plugins-official` (+571 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `infer_cylinder()` connect `Community 2` to `Community 51`, `Community 4`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `Handler` connect `Community 51` to `Community 2`, `Community 27`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `StrEnum` connect `Community 12` to `Community 10`, `Community 27`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 46 inferred relationships involving `infer_cylinder()` (e.g. with `test_bmw_n52b25()` and `test_hyundai_g4ke()`) actually correct?**
  _`infer_cylinder()` has 46 INFERRED edges - model-reasoned connections that need verification._
- **Are the 45 inferred relationships involving `str` (e.g. with `main()` and `run_query()`) actually correct?**
  _`str` has 45 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `VINDecodeError` (e.g. with `TestValidDecodes` and `TestLYearDisambiguation`) actually correct?**
  _`VINDecodeError` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `dump_schema.py — run once on Windows to expose TecDoc schema to Claude. Usage:`, `Load TecDoc CSV data into MySQL for VINLab.`, `mysql_bridge.py — local HTTP bridge so the Claude sandbox can query TecDoc. Run` to the rest of the system?**
  _846 weakly-connected nodes found - possible documentation gaps or missing edges._