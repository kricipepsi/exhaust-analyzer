# Graph Report - dnalab_docs  (2026-07-06)

## Corpus Check
- 51 files · ~8,091 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 215 nodes · 164 edges · 51 communities (12 shown, 39 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b7b2b9b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_`VehicleDNA` fields (5, contract §4.3)|`VehicleDNA` fields (5, contract §4.3)]]
- [[_COMMUNITY_2. `models.py` — `VehicleDNA` (frozen dataclass)|2. `models.py` — `VehicleDNA` (frozen dataclass)]]
- [[_COMMUNITY_Section 8 — Release|Section 8 — Release]]
- [[_COMMUNITY_ADR-0001 DNALab composes; it does not decode, validate, or route|ADR-0001: DNALab composes; it does not decode, validate, or route]]
- [[_COMMUNITY_ADR-0002 DNALab is the only in-family importer|ADR-0002: DNALab is the only in-family importer]]
- [[_COMMUNITY_ADR-0003 Versioned envelope with a hard mismatch guard|ADR-0003: Versioned envelope with a hard mismatch guard]]
- [[_COMMUNITY_ADR-0004 Delegate serialization to each producer model|ADR-0004: Delegate serialization to each producer model]]
- [[_COMMUNITY_ADR-0005 Validate triage-key presence before the VIN decode|ADR-0005: Validate triage-key presence before the VIN decode]]
- [[_COMMUNITY_ADR-0006 Auto-stamp session identity|ADR-0006: Auto-stamp session identity]]
- [[_COMMUNITY_ADR-0007 One coordinating schema-bump task, run last (T-DNA-7)|ADR-0007: One coordinating schema-bump task, run last (T-DNA-7)]]
- [[_COMMUNITY_5. Exceptions (propagated, not defined here)|5. Exceptions (propagated, not defined here)]]
- [[_COMMUNITY_3. `models.py` — `from_json_payload` contract|3. `models.py` — `from_json_payload` contract]]
- [[_COMMUNITY_Architecture Decision Records — DNALab (v2)|Architecture Decision Records — DNALab (v2)]]
- [[_COMMUNITY_References|References.md]]
- [[_COMMUNITY_BDD — DNALab (v2)|BDD — DNALab (v2)]]
- [[_COMMUNITY_Feature_Composition_happy_path|Feature_Composition_happy_path.md]]
- [[_COMMUNITY_Feature_Contract_surface|Feature_Contract_surface.md]]
- [[_COMMUNITY_Feature_Failfast_and_exception_propagation|Feature_Failfast_and_exception_propagation.md]]
- [[_COMMUNITY_Feature_Isolation_CIlevel_behaviour|Feature_Isolation_CIlevel_behaviour.md]]
- [[_COMMUNITY_Feature_JSON_roundtrip|Feature_JSON_roundtrip.md]]
- [[_COMMUNITY_Feature_Version_guard|Feature_Version_guard.md]]
- [[_COMMUNITY_Traceability_summary|Traceability_summary.md]]
- [[_COMMUNITY_DLD — DNALab (v2)|DLD — DNALab (v2)]]
- [[_COMMUNITY_1_Module_Map|1_Module_Map.md]]
- [[_COMMUNITY_4_assemblypy_buildvehicledna|4_assemblypy_buildvehicledna.md]]
- [[_COMMUNITY_6_Test_Coverage_current|6_Test_Coverage_current.md]]
- [[_COMMUNITY_7_Related_docs_granular_ADRs|7_Related_docs_granular_ADRs.md]]
- [[_COMMUNITY_HLD — DNALab (v2)|HLD — DNALab (v2)]]
- [[_COMMUNITY_1_Responsibility|1_Responsibility.md]]
- [[_COMMUNITY_2_Architecture_Position|2_Architecture_Position.md]]
- [[_COMMUNITY_3_Composition_Flow_buildvehicledna|3_Composition_Flow_buildvehicledna.md]]
- [[_COMMUNITY_4_VehicleDNA_Envelope_VehicleDNAnew|4_VehicleDNA_Envelope_VehicleDNAnew.md]]
- [[_COMMUNITY_5_Serialization_Version_Guard|5_Serialization_Version_Guard.md]]
- [[_COMMUNITY_6_Downstream_Integration_Point_consumer|6_Downstream_Integration_Point_consumer.md]]
- [[_COMMUNITY_7_NonFunctional_Requirements|7_NonFunctional_Requirements.md]]
- [[_COMMUNITY_8_Known_Gaps_Accepted_Behaviour|8_Known_Gaps_Accepted_Behaviour.md]]
- [[_COMMUNITY_LLD — DNALab (v2)|LLD — DNALab (v2)]]
- [[_COMMUNITY_1_Schema_Version_modelspy|1_Schema_Version_modelspy.md]]
- [[_COMMUNITY_2_SessionID_Format_modelspyVehicleDNAnew|2_SessionID_Format_modelspyVehicleDNAnew.md]]
- [[_COMMUNITY_3_Timestamp_Format_modelspyVehicleDNAnew|3_Timestamp_Format_modelspyVehicleDNAnew.md]]
- [[_COMMUNITY_4_TopLevel_Key_Set_modelspytojsonpayload|4_TopLevel_Key_Set_modelspytojsonpayload.md]]
- [[_COMMUNITY_5_Required_Triage_Keys_assemblypy|5_Required_Triage_Keys_assemblypy.md]]
- [[_COMMUNITY_6_EnumCoercion_Path_delegated|6_EnumCoercion_Path_delegated.md]]
- [[_COMMUNITY_7_Forbidden_Patterns_DNALabspecific|7_Forbidden_Patterns_DNALabspecific.md]]
- [[_COMMUNITY_PRD — DNALab|PRD — DNALab]]
- [[_COMMUNITY_Section_1_Summary|Section_1_Summary.md]]
- [[_COMMUNITY_Section_2_Contacts|Section_2_Contacts.md]]
- [[_COMMUNITY_Section_3_Background|Section_3_Background.md]]
- [[_COMMUNITY_Section_4_Objective|Section_4_Objective.md]]
- [[_COMMUNITY_Section_5_Market_Segment|Section_5_Market_Segment.md]]
- [[_COMMUNITY_Section_6_Value_Proposition|Section_6_Value_Proposition.md]]

## God Nodes (most connected - your core abstractions)
1. `2. `models.py` — `VehicleDNA` (frozen dataclass)` - 7 edges
2. ``VehicleDNA` fields (5, contract §4.3)` - 6 edges
3. `Section 8 — Release` - 6 edges
4. `ADR-0001: DNALab composes; it does not decode, validate, or route` - 5 edges
5. `ADR-0002: DNALab is the only in-family importer` - 5 edges
6. `ADR-0003: Versioned envelope with a hard mismatch guard` - 5 edges
7. `ADR-0004: Delegate serialization to each producer model` - 5 edges
8. `ADR-0005: Validate triage-key presence before the VIN decode` - 5 edges
9. `ADR-0006: Auto-stamp session identity` - 5 edges
10. `ADR-0007: One coordinating schema-bump task, run last (T-DNA-7)` - 5 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (51 total, 39 thin omitted)

### Community 0 - "`VehicleDNA` fields (5, contract §4.3)"
Cohesion: 0.13
Nodes (14): Assumption: Producers own their own validation, Assumption: VehicleDNA shape is contract-owned, Assumption: Version moves in lockstep with producer field changes, Assumptions, Field: `schema_version`, Field: `session_id`, Field: `symptom_dna`, Field: `timestamp` (+6 more)

### Community 1 - "2. `models.py` — `VehicleDNA` (frozen dataclass)"
Cohesion: 0.15
Nodes (12): 2. `models.py` — `VehicleDNA` (frozen dataclass), Classmethods / methods, Field: `schema_version`, Field: `session_id`, Field: `symptom_dna`, Field: `timestamp`, Field: `vin_dna`, Graph relations (explicit) (+4 more)

### Community 2 - "Section 8 — Release"
Cohesion: 0.25
Nodes (7): Decided, Dependency note (transitive — resolved), Graph relations (explicit), Landed (DNA-family pack — see `tasks/PROGRESS.md`), Section 8 — Release, Success Criteria, v2 Scope

### Community 3 - "ADR-0001: DNALab composes; it does not decode, validate, or route"
Cohesion: 0.29
Nodes (6): ADR-0001: DNALab composes; it does not decode, validate, or route, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 4 - "ADR-0002: DNALab is the only in-family importer"
Cohesion: 0.29
Nodes (6): ADR-0002: DNALab is the only in-family importer, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 5 - "ADR-0003: Versioned envelope with a hard mismatch guard"
Cohesion: 0.29
Nodes (6): ADR-0003: Versioned envelope with a hard mismatch guard, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 6 - "ADR-0004: Delegate serialization to each producer model"
Cohesion: 0.29
Nodes (6): ADR-0004: Delegate serialization to each producer model, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 7 - "ADR-0005: Validate triage-key presence before the VIN decode"
Cohesion: 0.29
Nodes (6): ADR-0005: Validate triage-key presence before the VIN decode, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 8 - "ADR-0006: Auto-stamp session identity"
Cohesion: 0.29
Nodes (6): ADR-0006: Auto-stamp session identity, Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 9 - "ADR-0007: One coordinating schema-bump task, run last (T-DNA-7)"
Cohesion: 0.29
Nodes (6): ADR-0007: One coordinating schema-bump task, run last (T-DNA-7), Alternatives Considered, Consequences, Context, Decision, Graph relations (explicit)

### Community 10 - "5. Exceptions (propagated, not defined here)"
Cohesion: 0.29
Nodes (6): 5. Exceptions (propagated, not defined here), Exception: `KeyError`, Exception: `SymptomValidationError`, Exception: `ValueError`, Exception: `VINDecodeError` (+ `ChassisNumberError`), Graph relations (explicit)

### Community 11 - "3. `models.py` — `from_json_payload` contract"
Cohesion: 0.33
Nodes (5): 3. `models.py` — `from_json_payload` contract, Failure: invalid `vin_dna` / `symptom_dna` shape, Failure: missing required top-level key, Failure: `schema_version` ≠ `SCHEMA_VERSION`, Graph relations (explicit)

## Knowledge Gaps
- **143 isolated node(s):** `Graph relations (explicit)`, `Context`, `Decision`, `Consequences`, `Alternatives Considered` (+138 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `Graph relations (explicit)`, `Context`, `Decision` to the rest of the system?**
  _143 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should ``VehicleDNA` fields (5, contract §4.3)` be split into smaller, more focused modules?**
  _Cohesion score 0.13333333333333333 - nodes in this community are weakly interconnected._