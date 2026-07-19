# Graph Report - registry_tests  (2026-07-06)

## Corpus Check
- 27 files · ~23,299 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 824 nodes · 1258 edges · 52 communities (29 shown, 23 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
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

## God Nodes (most connected - your core abstractions)
1. `_load_ruleset()` - 32 edges
2. `_load_ruleset()` - 31 edges
3. `_load_ruleset()` - 31 edges
4. `_load_ruleset()` - 29 edges
5. `_load_ruleset()` - 29 edges
6. `_load_ruleset()` - 28 edges
7. `_load_ruleset()` - 28 edges
8. `_write_ruleset()` - 26 edges
9. `_minimal_rule()` - 25 edges
10. `_load_ruleset()` - 24 edges

## Surprising Connections (you probably didn't know these)
- `test_missing_high_idle_safely_prunes()` --calls--> `_write_ruleset()`  [INFERRED]
  test_shim_high_idle_pids.py → test_integration_shim.py
- `test_rule_with_high_idle_gate_fires()` --calls--> `_write_ruleset()`  [INFERRED]
  test_shim_high_idle_pids.py → test_integration_shim.py
- `test_missing_high_idle_safely_prunes()` --calls--> `_minimal_rule()`  [INFERRED]
  test_shim_high_idle_pids.py → test_integration_shim.py
- `test_rule_with_high_idle_gate_fires()` --calls--> `_minimal_rule()`  [INFERRED]
  test_shim_high_idle_pids.py → test_integration_shim.py

## Import Cycles
- None detected.

## Communities (52 total, 23 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (63): _minimal_rule(), Any, Path, Tests for ``registry.integration_shim``.  The 11 tests below cover the shim's tw, Real-registry test. Constructing against the production rules dir     loads exac, Sanity check: the default rules dir constant resolves to the     ``registry/rule, When obd_live_data carries shrtft1/longft1, the shim resolves from live     OBD,, When obd_live_data is absent, the shim falls back to freeze-frame.     Uses long (+55 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (54): _load_ruleset(), Targeted tests for registry/rules/sensor_fault.json — v2 sensor_fault rule file., SF-005 and SF-006 use TIMING_RETARDED as SUGGESTIVE evidence., SF-001, SF-002, SF-003, SF-007 must use o2_voltage OBD evidence., SF-004 must use maf OBD evidence., SF-005 must use map_kpa OBD evidence., SF-006 must use ect_c OBD evidence., SF-006 must use o2_downstream OBD evidence. (+46 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (52): _load_ruleset(), Targeted tests for registry/rules/cam_timing.json — v2 cam_timing rule file., CT-005 must have empty chemistry_evidence — DTC-primary rule with no chemistry g, CT-001 must have empty dtc_evidence — mechanical timing on non-VVT engines     p, CT-002 must use stft_b1 OBD evidence as SUGGESTIVE for phaser lag trim     compe, CT-004 must use stft_b1 and ltft_b1 with negative thresholds as SUGGESTIVE     —, CT-005 must use stft_b1 and ltft_b1 in_range for near-zero trim detection —, CT-002 and CT-004 use P0011/P0012 DTC as SUGGESTIVE evidence. (+44 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (52): _load_corpus_case_ids(), _load_ruleset(), Targeted tests for registry/rules/non_starter.json — v2 non_starter rule file., NS-002 must use RICH_MISFIRE chemistry as GATING., NS-003 must use INCOMPLETE_COMBUSTION chemistry as GATING., NS-004 must accept LEAN_MISFIRE chemistry as SUGGESTIVE evidence., NS-001 must carry rpm < 600 as SUGGESTIVE OBD evidence., NS-001 must carry co2 < 5.0 as SUGGESTIVE OBD evidence. (+44 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (47): _load_ruleset(), Targeted tests for registry/rules/ecu_fault.json — v2 ecu_fault rule file., EF-003 must use in_range operator for frozen-trim detection., EF-001 must use P0171 DTC SUGGESTIVE evidence., EF-002 must use P0172 DTC SUGGESTIVE evidence., EF-003 must cover P0113, P0201, P0606, P0128 in DTC evidence., EF-004 must use P0606 DTC at DEFINITIVE tier., EF-005 must cover P0171, P0172, P0606 in DTC evidence. (+39 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (35): _load_ruleset(), Targeted tests for registry/rules/catalyst_failure.json — v2 catalyst_failure ru, At least one rule must use CATALYST_HISTORY DTC codes (P0420, P0430)., At least one rule must carry a perception_flag — OBD λ contradiction override., Helper: load and validate the catalyst_failure rule file., At least one rule must use OBD CO2 + O2 evidence for flow restriction., At least one rule must use LTFT >= 10%% OBD evidence for catalyst masking., At least one rule must use obd_lambda evidence — OBD λ contradiction path. (+27 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (33): _load_corpus_case_ids(), _load_ruleset(), RuleSet, Targeted tests for registry/rules/overheating.json — v2 overheating rule file., _rule_by_id(), test_all_case_ids_resolve(), test_all_overheating_cases_covered(), test_all_rules_have_confidence_ceiling() (+25 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (32): _load_ruleset(), Targeted tests for registry/rules/misfire.json — v2 misfire rule file., TIMING_RETARDED must appear as SUGGESTIVE — closes TIMING_RETARDED gap for misfi, At least one rule must use MISFIRE_HISTORY DTC codes (P0300-P0312)., At least one rule must use MISFIRE_HISTORY with strategy none_present — ECU blin, Helper: load and validate the misfire rule file., At least one rule must carry a perception_flag — truth-vs-perception override., Every numeric threshold in OBD evidence must carry a wiki_ref. (+24 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (30): _load_corpus_case_ids(), _load_ruleset(), Targeted tests for registry/rules/vacuum_leak.json — v2 vacuum_leak rule file., test_all_case_ids_resolve(), test_all_rules_have_confidence_ceiling(), test_all_vacuum_leak_cases_covered(), test_base_weights_in_range(), test_competition_group_vacuum_leak() (+22 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (29): _get_rule(), _load_corpus_case_ids(), _load_ruleset(), RuleSet, Targeted tests for registry/rules/charging_system.json — v2 charging_system rule, CS-001 ceiling = 0.85 matches OV-002 (single-specific-DTC pathognomonic rule)., The novel pattern: NORMAL_OPERATION at tier GATING.      This is the first rule, CS-002 must strictly outscore MF-004 on the ghost-misfire ambiguity.      Reads (+21 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (29): _load_ruleset(), Targeted tests for registry/rules/exhaust_leak.json — v2 exhaust_leak rule file., At least one rule must use HC + O2 OBD evidence — probe-tip/manifold dilution si, At least one rule must use P0171/P0174 DTC evidence — pre-cat lean DTC signal., At least one rule must use P2096/P2098 DTC evidence — post-cat trim DTC signal., Every numeric threshold in OBD evidence must carry a wiki_ref., Rules with base_weight <= 0.65 must carry a confidence_ceiling., NORMAL_OPERATION must not appear — ERR-EL-004 false-positive path removed in v2. (+21 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (28): _load_ruleset(), Targeted tests for registry/rules/ignition_fault.json — the v2 ignition_fault ru, Every numeric threshold in OBD evidence must carry a wiki_ref., Helper: load and validate the ignition_fault rule file., EXP-N026 must appear in passes_cases of the rule that targets it (IF-002)., CASE-035 must appear in passes_cases of the rule that targets it (IF-002)., case_036 must appear in passes_cases of the rule that targets it (IF-003)., IGNITION_MISFIRE must appear as DEFINITIVE in at least one rule — IF-001 anchor. (+20 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (27): _load_ruleset(), _payload(), Any, RuleSet, Targeted tests for registry/rules/invalid_input.json., _route(), test_all_rules_have_confidence_ceiling(), test_base_weights_in_range() (+19 more)

### Community 13 - "Community 13"
Cohesion: 0.07
Nodes (7): Minimal validation tests for registry.schema_v2., Mirror must have all 34 GASLab ChemicalSignature values., Must have 16 families (13 existing + 3 new per cvsgaps.md)., Must have 20 values (19 DTCLab + CYLINDER_FLUID_MISFIRE + UNKNOWN_FORMAT)., test_chemistry_state_count(), test_dtc_routing_tag_count(), test_fault_family_count()

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (22): _load_ruleset(), Targeted tests for registry/rules/rich_mixture.json — v2 rich_mixture rule file., Every numeric threshold in OBD evidence must carry a wiki_ref., Helper: load and validate the rich_mixture rule file., RICH_MIXTURE must appear as DEFINITIVE in at least one rule., POA_SIGNATURE must appear as SUGGESTIVE in at least one rule., SAMPLE_INVALID must appear as GATING in at least one rule — closes SAMPLE_INVALI, At least one rule must use P0172/P0175 DTC evidence — v1 had zero DTC-aware rich (+14 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (11): Any, Verify the produced corpus_curated.csv and corpus_meta.json., Every curated CSV row has a meta entry and vice versa., Curated CSV has the same columns as master., CorpusMeta counts match the actual data., No curated CSV row has an empty case_id., All NEW cases use the NEW- prefix., KEEP rows in curated CSV are verbatim copies from master. (+3 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (18): _load_ruleset(), Targeted tests for registry/rules/lean_condition.json — the first v2 rule file., Helper: load and validate the lean_condition rule file., LEAN_MIXTURE must appear as DEFINITIVE in at least one rule., TIMING_RETARDED must appear as SUGGESTIVE in at least one rule — closes #1 v1 ga, Every numeric threshold in OBD evidence must carry a wiki_ref., test_all_rules_in_same_competition_group(), test_at_least_three_rules() (+10 more)

### Community 17 - "Community 17"
Cohesion: 0.11
Nodes (17): Tests for ``registry.shim.payload_mirrors``.  These cover the output-contract de, A valid UUID4 in metadata.session_id is preserved verbatim — this is     the tra, Missing metadata → the fixed sentinel UUID, NOT a freshly-generated one     (a f, A non-UUID string (or a non-v4 UUID) falls back to the sentinel., The sentinel must be identical across calls — deterministic traceability., The sentinel itself must satisfy the UUID4 contract COMLab enforces., A present echo-audit dict is carried through verbatim (COMLab does not     gener, Missing echo-audit → sentinel with groups=[] and a parseable     submitted_at ti (+9 more)

### Community 18 - "Community 18"
Cohesion: 0.25
Nodes (14): _load_ruleset(), _payload(), Any, RuleSet, Targeted tests for registry/rules/no_fault.json., _route(), test_clean_false_lean_dtc_payload_routes_to_no_fault(), test_clean_no_dtc_payload_routes_to_no_fault() (+6 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (8): Decision logic for individual cases., Sentinel cases in CVSGAPS_KEEP_SENTINELS are kept., Sentinel cases not in keep list are dropped., Obsolete hardware cases are dropped., Contrived multi-fault cases are dropped even with pipeline bugs., Pipeline-bug cases without cvsgaps drop proposal are kept., Core diagnostic cases with no cvsgaps proposal are kept., TestClassifyCase

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (5): Tests for build_corpus.py — CorpusMeta schema validation + contract checks., FAILURE_BLUEPRINT.md parsing., Top-level CorpusMeta model., TestCorpusMeta, TestParseBlueprint

### Community 22 - "Community 22"
Cohesion: 0.22
Nodes (7): _load_corpus_case_ids(), Targeted tests for registry/rules/mechanical_wear.json — v2 mechanical_wear rule, MW-006 must use TIMING_RETARDED chemistry as SUGGESTIVE evidence., All rules must belong to mechanical_wear competition group., test_all_case_ids_resolve(), test_competition_group_mechanical_wear(), test_mw006_timing_retarded_suggestive()

### Community 23 - "Community 23"
Cohesion: 0.20
Nodes (9): Unit tests for tools/render_case_library.py., emits the HTML deterministically on re-run., Every row in corpus_curated.csv appears exactly once., Family counts rendered on the page match corpus_meta.json curation counts., All text fields from the CSV are properly HTML escaped in the output., test_every_csv_row_rendered_once(), test_family_counts_match_meta(), test_no_unescaped_user_text() (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.22
Nodes (9): _load_ruleset(), Every mechanical_wear case in corpus_curated.csv must appear in ≥1 rule., MW-001 must use WORN_PISTON_RINGS chemistry as GATING., test_all_mechanical_wear_cases_covered(), test_every_rule_has_passes_cases(), test_exactly_nine_rules(), test_mw001_worn_piston_rings_gating(), test_no_duplicate_rule_ids() (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (6): Valve seals low-idle transient HC signature routes to MW-002., Head-gasket coolant leak signature routes to MW-003., Worn rings low-idle gas signature routes to MW-001., test_head_gasket_routes_to_mw003(), test_rings_routes_to_mw001(), test_valve_seals_routes_to_mw002()

### Community 26 - "Community 26"
Cohesion: 0.43
Nodes (6): _future_consumer_mentions_task(), _loads_yaml(), Any, Path, test_live_route_does_not_load_comlab_kg(), test_oil_proposals_have_future_consumer()

### Community 27 - "Community 27"
Cohesion: 0.29
Nodes (6): The R2 rings payload still routes to MW-001, not MW-008., A legacy payload without high_idle_hc does not fire MW-008., PCV-shaped payload routes to MW-008., test_pcv_needs_high_idle(), test_pcv_routes_to_mw008(), test_rings_not_stolen_by_pcv()

### Community 28 - "Community 28"
Cohesion: 0.29
Nodes (6): The R4 PCV payload (lambda_chem=0.93) still routes to MW-008, not MW-009., Legacy payload without high_idle_hc does not fire MW-009., Turbo-shaped payload routes to MW-009., test_pcv_not_stolen_by_turbo(), test_turbo_needs_high_idle(), test_turbo_routes_to_mw009()

### Community 29 - "Community 29"
Cohesion: 0.40
Nodes (3): cvsgaps.md proposal mapping., Keep lists and drop proposals must not overlap., TestCvsgapsMap

## Knowledge Gaps
- **5 isolated node(s):** `Any`, `RuleSet`, `RuleSet`, `Path`, `RuleSet`
  These have ≤1 connection - possible missing edges or undocumented components.
- **23 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TestOutputContracts` connect `Community 15` to `Community 20`?**
  _High betweenness centrality (0.003) - this node is a cross-community bridge._
- **Why does `_load_ruleset()` connect `Community 24` to `Community 22`, `Community 31`, `Community 32`, `Community 33`, `Community 34`, `Community 35`, `Community 36`, `Community 37`, `Community 38`, `Community 39`, `Community 40`, `Community 41`, `Community 42`, `Community 43`, `Community 44`, `Community 45`, `Community 46`, `Community 47`, `Community 48`, `Community 49`, `Community 50`, `Community 51`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `TestClassifyCase` connect `Community 19` to `Community 20`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `registry tests package (wiki: labs/comlab/registry/docs/REGISTRY_START_HERE.md).`, `Any`, `Tests for build_corpus.py — CorpusMeta schema validation + contract checks.` to the rest of the system?**
  _257 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.061072261072261075 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.05451127819548872 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.05656565656565657 - nodes in this community are weakly interconnected._