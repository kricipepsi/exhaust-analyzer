# Graph Report - dtclab  (2026-06-11)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 186 nodes · 308 edges · 17 communities (14 shown, 3 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 39 edges (avg confidence: 0.58)
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

## God Nodes (most connected - your core abstractions)
1. `_source_wiki` - 34 edges
2. `DTC to Routing Tag Map` - 15 edges
3. `DTCRoutingTag` - 12 edges
4. `DTCLabPayload` - 10 edges
5. `MatchType` - 8 edges
6. `CandidateScore` - 8 edges
7. `rank_candidates()` - 8 edges
8. `extract_freeze_frame()` - 8 edges
9. `DtcLabDnaView` - 8 edges
10. `FreezeFrameIncompleteError` - 7 edges

## Surprising Connections (you probably didn't know these)
- `MatchType` --uses--> `VinConfidence`  [INFERRED]
  ranking.py → schemas/dna_view.py
- `MatchType` --uses--> `DTCLabPayload`  [INFERRED]
  ranking.py → schemas/payload.py
- `MatchType` --uses--> `DTCRoutingTag`  [INFERRED]
  ranking.py → schemas/vocabulary.py
- `CandidateScore` --uses--> `VinConfidence`  [INFERRED]
  ranking.py → schemas/dna_view.py
- `CandidateScore` --uses--> `DTCLabPayload`  [INFERRED]
  ranking.py → schemas/payload.py

## Communities (17 total, 3 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (36): 01, name, 02, 05, 06, 13, 21, 22 (+28 more)

### Community 1 - "Community 1"
Cohesion: 0.14
Nodes (16): _derive_iat_ect_bias(), _derive_load_high_low_rpm(), _derive_open_loop(), extract_freeze_frame(), FreezeFrameIncompleteError, Freeze-frame extractor — validates Mode $02 data and derives symptom flags.  Sou, ff_open_loop_at_fault: loop status is open-loop, open-loop drive, or     open-lo, ff_load_high_at_low_rpm: high load at low RPM.      wiki: DTC_VOCABULARY.md §12. (+8 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (18): DTC Vocabulary Document, Boost History, Catalyst History, ECU Internal History, EGR Equipped, EGR History, EVAP History, Has Catalyst (+10 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (12): Compile raw OBD-II inputs into a validated ``DTCLabPayload``.          Args:, DTCFormatError, DTC ingestion gate — validates raw DTC strings against the canonical regex.  Sou, Raised when a DTC string does not match the canonical regex.      Source: DTC_VO, Validate every code in *codes* against the canonical DTC regex.      Args:, validate_dtc_list(), evaluate_coolant_dtc_context(), Evaluate cross-field DTC + fuel status for fluid intrusion signatures.      Retu (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.21
Nodes (13): _build_family_index(), classify_top3(), _dna_factor_for_family(), _load_routing_rules(), _match_type_for_weight(), rank_candidates(), DTCLab Phase 2 scorer — per-family confidence from §16 weights + §14.2 DNA gatin, Build family → tags and family → dna_gate_names indices.      Returns:         ( (+5 more)

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (8): DataFusionSanitizer — public surface that wires the full DTCLab pipeline.  Inges, Wires the full DTCLab compilation pipeline into a single public surface.      Co, DNA-gated routing-tag engine.  map() — pure DTC-to-tag function. No external inp, Single DTC-pattern → tag mapping with optional DNA gate., Maps confirmed DTC codes to DTCRoutingTag values with DNA-gate filtering.      C, _RoutingRule, DTCRoutingTag, Fault-family routing hint derived from confirmed DTCs.      Source: DTC_VOCABULA

### Community 6 - "Community 6"
Cohesion: 0.24
Nodes (10): AirMeteringStrategy, EuroEmissionCategory, DTCLab-owned DNA view schema — typed replacement for the loose dict form.  Every, Euro emissions standard tier for the identified vehicle.      Source: DTC_VOCABU, Primary air-metering strategy of the identified vehicle.      Source: DTC_VOCABU, Vehicle technology horizon resolved from VIN decoding.      Source: DTC_VOCABULA, Confidence tier of the VIN-to-DNA resolution.      Source: DTC_VOCABULARY.md §14, ResolvedHorizon (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.27
Nodes (9): classify_margin(), evaluate_monitor(), _load_dictionary(), _lookup_component(), Mode $06 on-board monitor evaluator — margin tri-state classifier.  Source: DTC_, Classify a Mode $06 margin percentage into its tri-state.      Source: DTC_VOCAB, Return the target component name for *mid_hex* from the dictionary.      Returns, Return the parsed Mode $06 hex dictionary at *path*.      Cached per distinct *p (+1 more)

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (8): BaseModel, DtcEmissionsView, Emissions-equipment flags that gate DNA-screened routing tags.      Source: DTC_, Mode06MonitorResult, Mode06MonitorResult — Mode $06 on-board monitor test result.  Every field source, Single Mode $06 monitor test result.      Source: DTC_VOCABULARY.md §13., DTCLabPayload, Top-level DTCLab output — the single JSON payload at the COMLab boundary.      S

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (8): CandidateScore, MatchType, Evidence-strength tier derived from the strongest contributing source.      Sour, Single fault-family candidate with raw confidence and evidence tier.      Fields, DtcLabDnaView, Slim VehicleDNA projection consumed by DTCLab.      Source: DTC_VOCABULARY.md §1, Mode06MonitorState, Mode $06 on-board monitor test result tri-state.      Source: DTC_VOCABULARY.md

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (7): DTCSeverityClass, DTCState, HistoricalFaultContext, DTCLab canonical vocabulary — StrEnums, DTC_REGEX, and confidence weights.  All, DTC severity tier per SAE J2012 §6.      Source: DTC_VOCABULARY.md §5., OBD-II DTC confirmation state — reserved contract surface.      Not consumed by, Load / thermal context at the moment the DTC was stored.      Source: DTC_VOCABU

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (5): _matches_any(), Evaluate the strict hardware-presence check for HIGH confidence., True if *dtc* matches at least one compiled regex in *patterns*., Return the deduplicated routing tags for *confirmed_dtcs*.          Args:, Return True if *tag* is allowed through its DNA gate.          No gate → always

### Community 12 - "Community 12"
Cohesion: 0.40
Nodes (3): DTCLabPayload — top-level JSON contract emitted to COMLab.  Every field and cons, Validate monitor keys., Validate routing tags.

### Community 13 - "Community 13"
Cohesion: 0.50
Nodes (3): families_for_tags(), Canonical family mapping for DTCLab routing tags.  Maps each DTCRoutingTag (18-v, Return deduplicated, ordered canonical families for active routing tags.      St

## Knowledge Gaps
- **15 isolated node(s):** `_description`, `VVT History`, `Lean History`, `Thermal History`, `O2 History` (+10 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DTCRoutingTag` connect `Community 5` to `Community 3`, `Community 4`, `Community 6`, `Community 8`, `Community 9`, `Community 10`?**
  _High betweenness centrality (0.125) - this node is a cross-community bridge._
- **Why does `DTCLabPayload` connect `Community 8` to `Community 1`, `Community 5`, `Community 9`, `Community 10`, `Community 12`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `evaluate_monitor()` connect `Community 7` to `Community 8`, `Community 3`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DTCRoutingTag` (e.g. with `MatchType` and `CandidateScore`) actually correct?**
  _`DTCRoutingTag` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Canonical family mapping for DTCLab routing tags.  Maps each DTCRoutingTag (18-v`, `Return deduplicated, ordered canonical families for active routing tags.      St`, `DTCLab Phase 2 scorer — per-family confidence from §16 weights + §14.2 DNA gatin` to the rest of the system?**
  _78 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.14035087719298245 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._