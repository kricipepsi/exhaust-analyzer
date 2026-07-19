# Graph Report - vinlab_v2docs  (2026-07-06)

## Corpus Check
- 68 files · ~12,400 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 396 nodes · 328 edges · 68 communities (26 shown, 42 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b7b2b9b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_4. `models.py` — `VinDNA` (frozen dataclass)|4. `models.py` — `VinDNA` (frozen dataclass)]]
- [[_COMMUNITY_Section 7 — Solution|Section 7 — Solution]]
- [[_COMMUNITY_7. `overlaycylinder_heuristic.py` — `infer_cylinder`|7. `overlay/cylinder_heuristic.py` — `infer_cylinder`]]
- [[_COMMUNITY_7. Downstream Integration Points (consumers)|7. Downstream Integration Points (consumers)]]
- [[_COMMUNITY_Architecture Decision Records — VINLab (v2)|Architecture Decision Records — VINLab (v2)]]
- [[_COMMUNITY_3. `models.py` — Nested dataclasses|3. `models.py` — Nested dataclasses]]
- [[_COMMUNITY_2. `models.py` — Enums (9 StrEnums)|2. `models.py` — Enums (9 StrEnums)]]
- [[_COMMUNITY_8. Non-Functional Requirements|8. Non-Functional Requirements]]
- [[_COMMUNITY_13. Forbidden Patterns (VINLab-specific)|13. Forbidden Patterns (VINLab-specific)]]
- [[_COMMUNITY_9. Known Gaps  Accepted Behaviour|9. Known Gaps / Accepted Behaviour]]
- [[_COMMUNITY_6. Engine Resolution & Overlays|6. Engine Resolution & Overlays]]
- [[_COMMUNITY_Section 2 — Contacts|Section 2 — Contacts]]
- [[_COMMUNITY_ADR-0001 Offline runtime — bake all reference data into `vinlabdata`|ADR-0001: Offline runtime — bake all reference data into `vinlab/data/`]]
- [[_COMMUNITY_ADR-0002 VINLab is a sibling module, not a sub-package of DNALab|ADR-0002: VINLab is a sibling module, not a sub-package of DNALab]]
- [[_COMMUNITY_ADR-0003 No cross-lab Python imports — COMLab mirrors `VinDNA`|ADR-0003: No cross-lab Python imports — COMLab mirrors `VinDNA`]]
- [[_COMMUNITY_ADR-0004 Enum-typed `VinDNA` fields replace bare `str`|ADR-0004: Enum-typed `VinDNA` fields replace bare `str`]]
- [[_COMMUNITY_ADR-0005 Single deep air-metering module replaces two parallel switches|ADR-0005: Single deep air-metering module replaces two parallel switches]]
- [[_COMMUNITY_ADR-0006 Data-driven checksum bypass for non-NHTSA markets|ADR-0006: Data-driven checksum bypass for non-NHTSA markets]]
- [[_COMMUNITY_ADR-0007 Cylinder-count heuristic is a gated last resort, never an override|ADR-0007: Cylinder-count heuristic is a gated last resort, never an override]]
- [[_COMMUNITY_ADR-0008 Confidence is graded, never fatal — degrade rather than crash|ADR-0008: Confidence is graded, never fatal — degrade rather than crash]]
- [[_COMMUNITY_ADR-0009 SQL isolation — all SQL lives in `dbtecdoc_query.py`|ADR-0009: SQL isolation — all SQL lives in `db/tecdoc_query.py`]]
- [[_COMMUNITY_ADR-0010 `ChassisNumberError` distinguishes wrong-length input from decode failure|ADR-0010: `ChassisNumberError` distinguishes wrong-length input from decode failure]]
- [[_COMMUNITY_Section 8 — Release|Section 8 — Release]]
- [[_COMMUNITY_11. Test Coverage (current)|11. Test Coverage (current)]]
- [[_COMMUNITY_4. Checksum Architecture (validate_vin_checksum)|4. Checksum Architecture (validate_vin_checksum)]]
- [[_COMMUNITY_10. Error Types|10. Error Types]]
- [[_COMMUNITY_References|References.md]]
- [[_COMMUNITY_BDD — VINLab (v2)|BDD — VINLab (v2)]]
- [[_COMMUNITY_Feature_Checksum_with_market-aware_bypass|Feature_Checksum_with_market-aware_bypass.md]]
- [[_COMMUNITY_Feature_Decode_happy_path|Feature_Decode_happy_path.md]]
- [[_COMMUNITY_Feature_Model-year_resolution_and_the_L_collision|Feature_Model-year_resolution_and_the_L_collision.md]]
- [[_COMMUNITY_Feature_Offline_+_isolation_guarantees_(CI-level_behaviour)|Feature_Offline_+_isolation_guarantees_(CI-level_behaviour).md]]
- [[_COMMUNITY_Feature_Overlay_derivations|Feature_Overlay_derivations.md]]
- [[_COMMUNITY_Feature_Petrol-only_scope_guard_(H1)|Feature_Petrol-only_scope_guard_(H1).md]]
- [[_COMMUNITY_Feature_Structural_validation|Feature_Structural_validation.md]]
- [[_COMMUNITY_Feature_Two-path_engine_resolution|Feature_Two-path_engine_resolution.md]]
- [[_COMMUNITY_Feature_WMI_and_low-volume_manufacturers|Feature_WMI_and_low-volume_manufacturers.md]]
- [[_COMMUNITY_Traceability_summary|Traceability_summary.md]]
- [[_COMMUNITY_DLD — VINLab (v2)|DLD — VINLab (v2)]]
- [[_COMMUNITY_1._Module_Map|1._Module_Map.md]]
- [[_COMMUNITY_5._decoder.py_—_RobustVINDecoder|5._decoder.py_—_RobustVINDecoder.md]]
- [[_COMMUNITY_6._Air-metering_derivation_(decoder.py_+_overlay_air_metering.py)|6._Air-metering_derivation_(decoder.py_+_overlay_air_metering.py).md]]
- [[_COMMUNITY_8._db_tecdoc_query.py_—_SQL_isolation_(H8)|8._db_tecdoc_query.py_—_SQL_isolation_(H8).md]]
- [[_COMMUNITY_9._Confidence_grading_(decoder.py)|9._Confidence_grading_(decoder.py).md]]
- [[_COMMUNITY_HLD — VINLab (v2)|HLD — VINLab (v2)]]
- [[_COMMUNITY_1._Responsibility|1._Responsibility.md]]
- [[_COMMUNITY_2._Architecture_Position|2._Architecture_Position.md]]
- [[_COMMUNITY_3._Internal_Pipeline_(decode_vin_payload)|3._Internal_Pipeline_(decode_vin_payload).md]]
- [[_COMMUNITY_5._WMI_&_Year_Resolution|5._WMI_&_Year_Resolution.md]]
- [[_COMMUNITY_LLD — VINLab (v2)|LLD — VINLab (v2)]]
- [[_COMMUNITY_10._Euro_→_Horizon_Map_(overlay_horizon.py)|10._Euro_→_Horizon_Map_(overlay_horizon.py).md]]
- [[_COMMUNITY_11._Upstream-O2_Derivation_(overlay_switches.py)|11._Upstream-O2_Derivation_(overlay_switches.py).md]]
- [[_COMMUNITY_12._Cylinder_Heuristic_Constants_(overlay_cylinder_heuristic.py)|12._Cylinder_Heuristic_Constants_(overlay_cylinder_heuristic.py).md]]
- [[_COMMUNITY_1._Checksum_Tables_(decoder.py)|1._Checksum_Tables_(decoder.py).md]]
- [[_COMMUNITY_2._Character_&_Charset_Constants_(decoder.py)|2._Character_&_Charset_Constants_(decoder.py).md]]
- [[_COMMUNITY_3._Checksum_Bypass_Sets_(decoder.py)|3._Checksum_Bypass_Sets_(decoder.py).md]]
- [[_COMMUNITY_4._Euro_Normalisation_(decoder.py)|4._Euro_Normalisation_(decoder.py).md]]
- [[_COMMUNITY_5._WMI_Low-Volume_Rule_(decoder.py_resolve_wmi)|5._WMI_Low-Volume_Rule_(decoder.py_resolve_wmi).md]]
- [[_COMMUNITY_6._Year_Disambiguation_(decoder.py_resolve_year)|6._Year_Disambiguation_(decoder.py_resolve_year).md]]
- [[_COMMUNITY_7._Engine_Resolution_Slices_(decoder.py_resolve_engine)|7._Engine_Resolution_Slices_(decoder.py_resolve_engine).md]]
- [[_COMMUNITY_8._Displacement_&_Tech-Mask_Conversion_(decoder.py)|8._Displacement_&_Tech-Mask_Conversion_(decoder.py).md]]
- [[_COMMUNITY_9._Stress-Idle_RPM_Table_(overlay_stress_rpm.py)|9._Stress-Idle_RPM_Table_(overlay_stress_rpm.py).md]]
- [[_COMMUNITY_PRD — VINLab|PRD — VINLab]]
- [[_COMMUNITY_Section_1_—_Summary|Section_1_—_Summary.md]]
- [[_COMMUNITY_Section_3_—_Background|Section_3_—_Background.md]]
- [[_COMMUNITY_Section_4_—_Objective|Section_4_—_Objective.md]]
- [[_COMMUNITY_Section_5_—_Market_Segment|Section_5_—_Market_Segment.md]]
- [[_COMMUNITY_Section_6_—_Value_Proposition|Section_6_—_Value_Proposition.md]]

## God Nodes (most connected - your core abstractions)
1. `4. `models.py` — `VinDNA` (frozen dataclass)` - 32 edges
2. `Section 7 — Solution` - 26 edges
3. `7. `overlay/cylinder_heuristic.py` — `infer_cylinder`` - 15 edges
4. `Architecture Decision Records — VINLab (v2)` - 12 edges
5. `7. Downstream Integration Points (consumers)` - 12 edges
6. `3. `models.py` — Nested dataclasses` - 11 edges
7. `2. `models.py` — Enums (9 StrEnums)` - 10 edges
8. `8. Non-Functional Requirements` - 8 edges
9. `13. Forbidden Patterns (VINLab-specific)` - 8 edges
10. `9. Known Gaps / Accepted Behaviour` - 7 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (68 total, 42 thin omitted)

### Community 0 - "4. `models.py` — `VinDNA` (frozen dataclass)"
Cohesion: 0.06
Nodes (33): #: 1, #: 10, #: 11, #: 12, #: 13, #: 14, #: 15, #: 16 (+25 more)

### Community 1 - "Section 7 — Solution"
Cohesion: 0.07
Nodes (27): #: 1, #: 10, #: 11, #: 12, #: 13, #: 14, #: 15, #: 16 (+19 more)

### Community 2 - "7. `overlay/cylinder_heuristic.py` — `infer_cylinder`"
Cohesion: 0.12
Nodes (16): 7. `overlay/cylinder_heuristic.py` — `infer_cylinder`, Brand(s): BMW, Brand(s): Honda, Brand(s): Hyundai/Kia, Brand(s): Mazda, Brand(s): Mercedes, Brand(s): Mitsubishi, Brand(s): Nissan (+8 more)

### Community 3 - "7. Downstream Integration Points (consumers)"
Cohesion: 0.14
Nodes (13): 7. Downstream Integration Points (consumers), Graph relations (explicit), `VinDNA` field: `air_metering_strategy`, `VinDNA` field: CoC targets (`target_lambda_v112`, `co_low_idle`, `co_high_idle`, …), `VinDNA` field: `confidence`, `VinDNA` field: `engine_displacement_liters`, `VinDNA` field: `euro_emission_category` / `resolved_horizon`, `VinDNA` field: `induction_type` (+5 more)

### Community 4 - "Architecture Decision Records — VINLab (v2)"
Cohesion: 0.15
Nodes (12): ADR: ADR-0001, ADR: ADR-0002, ADR: ADR-0003, ADR: ADR-0004, ADR: ADR-0005, ADR: ADR-0006, ADR: ADR-0007, ADR: ADR-0008 (+4 more)

### Community 5 - "3. `models.py` — Nested dataclasses"
Cohesion: 0.15
Nodes (12): 3. `models.py` — Nested dataclasses, `AirMeteringArchitecture` (frozen), `Emissions` (frozen), Field: `downstream_o2_present`, Field: `downstream_trim_role`, Field: `egr_equipped`, Field: `has_catalyst`, Field: `has_maf_sensor` (+4 more)

### Community 6 - "2. `models.py` — Enums (9 StrEnums)"
Cohesion: 0.17
Nodes (11): 2. `models.py` — Enums (9 StrEnums), Enum: `AirMeteringStrategy`, Enum: `DownstreamTrimRole`, Enum: `EuroEmissionCategory`, Enum: `FuelDeliveryType`, Enum: `Horizon`, Enum: `InductionType`, Enum: `PrimaryLoadCalculation` (+3 more)

### Community 7 - "8. Non-Functional Requirements"
Cohesion: 0.20
Nodes (9): 8. Non-Functional Requirements, Graph relations (explicit), Requirement: Decode determinism, Requirement: Import isolation, Requirement: Numeric literals, Requirement: Runtime MySQL calls, Requirement: Runtime network calls, Requirement: Signal/noise (+1 more)

### Community 8 - "13. Forbidden Patterns (VINLab-specific)"
Cohesion: 0.20
Nodes (9): 13. Forbidden Patterns (VINLab-specific), Graph relations (explicit), Pattern: Expanding `_BRAND_DISPATCH`/`_MERCEDES_TABLE` without a follow-up task, Pattern: `from gaslab/obdlab/dtclab/comlab/symptomlab import …`, Pattern: Network or MySQL call at runtime, Pattern: New `VinDNA` field without a named consumer, Pattern: Numeric literal without a `# source:`/`# wiki:` comment, Pattern: Re-running graphify against `graph/` (+1 more)

### Community 9 - "9. Known Gaps / Accepted Behaviour"
Cohesion: 0.22
Nodes (8): 9. Known Gaps / Accepted Behaviour, Graph relations (explicit), ID: CoC-null check, ID: `mysql_data/`, ID: `secondary_air_equipped`, ID: T-DNA-3, ID: T-DNA-4, ID: T-DNA-5

### Community 10 - "6. Engine Resolution & Overlays"
Cohesion: 0.25
Nodes (7): 6. Engine Resolution & Overlays, Graph relations (explicit), Overlay: Air metering, Overlay: Cylinder fallback, Overlay: Horizon, Overlay: Stress RPM, Overlay: Upstream O2

### Community 11 - "Section 2 — Contacts"
Cohesion: 0.25
Nodes (7): Graph relations (explicit), Name: 4DApp Engineering Lead, Name: COMLab Team, Name: GASLab Owner, Name: OBDLab Owner, Name: VINLab Owner, Section 2 — Contacts

### Community 12 - "ADR-0001: Offline runtime — bake all reference data into `vinlab/data/`"
Cohesion: 0.29
Nodes (6): ADR-0001: Offline runtime — bake all reference data into `vinlab/data/`, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 13 - "ADR-0002: VINLab is a sibling module, not a sub-package of DNALab"
Cohesion: 0.29
Nodes (6): ADR-0002: VINLab is a sibling module, not a sub-package of DNALab, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 14 - "ADR-0003: No cross-lab Python imports — COMLab mirrors `VinDNA`"
Cohesion: 0.29
Nodes (6): ADR-0003: No cross-lab Python imports — COMLab mirrors `VinDNA`, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 15 - "ADR-0004: Enum-typed `VinDNA` fields replace bare `str`"
Cohesion: 0.29
Nodes (6): ADR-0004: Enum-typed `VinDNA` fields replace bare `str`, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 16 - "ADR-0005: Single deep air-metering module replaces two parallel switches"
Cohesion: 0.29
Nodes (6): ADR-0005: Single deep air-metering module replaces two parallel switches, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 17 - "ADR-0006: Data-driven checksum bypass for non-NHTSA markets"
Cohesion: 0.29
Nodes (6): ADR-0006: Data-driven checksum bypass for non-NHTSA markets, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 18 - "ADR-0007: Cylinder-count heuristic is a gated last resort, never an override"
Cohesion: 0.29
Nodes (6): ADR-0007: Cylinder-count heuristic is a gated last resort, never an override, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 19 - "ADR-0008: Confidence is graded, never fatal — degrade rather than crash"
Cohesion: 0.29
Nodes (6): ADR-0008: Confidence is graded, never fatal — degrade rather than crash, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 20 - "ADR-0009: SQL isolation — all SQL lives in `db/tecdoc_query.py`"
Cohesion: 0.29
Nodes (6): ADR-0009: SQL isolation — all SQL lives in `db/tecdoc_query.py`, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 21 - "ADR-0010: `ChassisNumberError` distinguishes wrong-length input from decode failure"
Cohesion: 0.29
Nodes (6): ADR-0010: `ChassisNumberError` distinguishes wrong-length input from decode failure, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 22 - "Section 8 — Release"
Cohesion: 0.29
Nodes (6): Explicitly Deferred, Graph relations (explicit), Landed (DNA-family pack — see `labs/dnalab/tasks/PROGRESS.md`), Section 8 — Release, Success Criteria, v2 Scope

### Community 23 - "11. Test Coverage (current)"
Cohesion: 0.33
Nodes (5): 11. Test Coverage (current), Area: Decoder + resolvers, Area: Graph artefacts, Area: Tooling / build data, Graph relations (explicit)

### Community 24 - "4. Checksum Architecture (validate_vin_checksum)"
Cohesion: 0.33
Nodes (5): 4. Checksum Architecture (validate_vin_checksum), Bypass: Non-NHTSA WMI, Bypass: Non-standard pos-9, Bypass: OPSI corrupt prefix, Graph relations (explicit)

### Community 25 - "10. Error Types"
Cohesion: 0.40
Nodes (4): 10. Error Types, Error: `ChassisNumberError`, Error: `VINDecodeError`, Graph relations (explicit)

## Knowledge Gaps
- **297 isolated node(s):** `ADR: ADR-0001`, `ADR: ADR-0002`, `ADR: ADR-0003`, `ADR: ADR-0004`, `ADR: ADR-0005` (+292 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **42 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `ADR: ADR-0001`, `ADR: ADR-0002`, `ADR: ADR-0003` to the rest of the system?**
  _297 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `4. `models.py` — `VinDNA` (frozen dataclass)` be split into smaller, more focused modules?**
  _Cohesion score 0.058823529411764705 - nodes in this community are weakly interconnected._
- **Should `Section 7 — Solution` be split into smaller, more focused modules?**
  _Cohesion score 0.07142857142857142 - nodes in this community are weakly interconnected._
- **Should `7. `overlay/cylinder_heuristic.py` — `infer_cylinder`` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `7. Downstream Integration Points (consumers)` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._