# Graph Report - registry_code  (2026-07-06)

## Corpus Check
- 26 files · ~32,285 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 220 nodes · 419 edges · 29 communities (24 shown, 5 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 121 edges (avg confidence: 0.51)
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

## God Nodes (most connected - your core abstractions)
1. `_Observation` - 28 edges
2. `Rule` - 22 edges
3. `Any` - 20 edges
4. `RegistryV2Router` - 19 edges
5. `RuleSet` - 18 edges
6. `ChemistryState` - 17 edges
7. `OBDEvidence` - 17 edges
8. `EvidenceTier` - 16 edges
9. `FaultFamily` - 16 edges
10. `DTCRoutingTag` - 16 edges

## Surprising Connections (you probably didn't know these)
- `_Observation` --uses--> `ChemistryEvidence`  [INFERRED]
  integration_shim.py → schema_v2.py
- `_Observation` --uses--> `ChemistryState`  [INFERRED]
  integration_shim.py → schema_v2.py
- `_Observation` --uses--> `DTCEvidence`  [INFERRED]
  integration_shim.py → schema_v2.py
- `_Observation` --uses--> `DTCRoutingTag`  [INFERRED]
  integration_shim.py → schema_v2.py
- `_Observation` --uses--> `EvidenceTier`  [INFERRED]
  integration_shim.py → schema_v2.py

## Import Cycles
- None detected.

## Communities (29 total, 5 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.10
Nodes (42): _apply_competition(), _build_observation(), _check_chemistry_evidence(), _check_dtc_evidence(), _check_obd_evidence(), _coerce_dtc_routing_tags(), _control_plausibility_state(), _corroboration_count() (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.19
Nodes (34): BaseModel, ChemistryEvidence, DTCEvidence, DTCRoutingTag, FaultFamily, ControlPlausibilityState, LeanRootCauseState, Any (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (20): build_cvsgaps_map(), build_new_case(), build_new_metas(), CaseMeta, classify_case(), CorpusMeta, load_master_csv(), main() (+12 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (15): _audit_pid_coverage(), _load_all_rulesets(), Singleton-style router: loads + validates all 16 rule files at     construction;, Construct a router against ``rules_dir``.          ``expected_files`` defaults t, Read-only view of the loaded rules (used by tests)., Translate a COMLab post-rank winner through the canonical v2 renderer., Module-level entry point. Lazily constructs the default router on first     call, Route a case and return trace-only diagnostics for COMLab spans. (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.28
Nodes (8): _is_valid_uuid4(), Any, Output-contract mirrors for the v2 integration shim.  Why this module exists (RE, True iff ``value`` is a string parseable as a version-4 UUID., Return a UUID4 string for the output ``session_id``.      Reads ``payload["metad, Return a ``UserInputEchoAudit``-shaped dict for the output.      Passes through, resolve_session_id(), resolve_user_input_echo_audit()

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (7): cases, curated_count, dropped_count, generated_at, master_csv_total, new_count, relabel_count

### Community 6 - "Community 6"
Cohesion: 0.50
Nodes (4): Look up a v2 rule's PID in the sanitized payload. Returns ``None`` when     the, Resolve a single (source, field) pair to ``float | None``., _resolve_pid_from_payload(), _resolve_single_source()

### Community 7 - "Community 7"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 8 - "Community 8"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 9 - "Community 9"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 10 - "Community 10"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 11 - "Community 11"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 12 - "Community 12"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 13 - "Community 13"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 14 - "Community 14"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 15 - "Community 15"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 16 - "Community 16"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 17 - "Community 17"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 18 - "Community 18"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 19 - "Community 19"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 20 - "Community 20"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 21 - "Community 21"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 22 - "Community 22"
Cohesion: 0.50
Nodes (3): fault_family, rules, version

### Community 23 - "Community 23"
Cohesion: 0.67
Nodes (3): escape_html(), main(), Safely escape HTML special characters, returning empty string for None.

## Knowledge Gaps
- **56 isolated node(s):** `generated_at`, `master_csv_total`, `curated_count`, `dropped_count`, `relabel_count` (+51 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **5 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `_Observation` connect `Community 0` to `Community 1`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Why does `_translate_to_output()` connect `Community 0` to `Community 1`, `Community 3`, `Community 4`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `CaseMeta` connect `Community 2` to `Community 1`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `_Observation` (e.g. with `ChemistryEvidence` and `ChemistryState`) actually correct?**
  _`_Observation` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Rule` (e.g. with `ChemistryEvidence` and `ChemistryState`) actually correct?**
  _`Rule` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `Any` (e.g. with `ChemistryEvidence` and `ChemistryState`) actually correct?**
  _`Any` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `RegistryV2Router` (e.g. with `ChemistryEvidence` and `ChemistryState`) actually correct?**
  _`RegistryV2Router` has 9 INFERRED edges - model-reasoned connections that need verification._