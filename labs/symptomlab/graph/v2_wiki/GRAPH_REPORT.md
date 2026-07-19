# Graph Report - .  (2026-06-12)

## Corpus Check
- Corpus is ~4,808 words - fits in a single context window. You may not need a graph.

## Summary
- 109 nodes · 123 edges · 11 communities
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.75)
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

## God Nodes (most connected - your core abstractions)
1. `SymptomValidator.validate` - 15 edges
2. `OccursDuring (StrEnum)` - 11 edges
3. `LoadState (StrEnum)` - 10 edges
4. `SymptomDNA (Part-B payload)` - 10 edges
5. `revised 21-pair catalog` - 7 edges
6. `SymptomLab Wiki — Index` - 6 edges
7. `oil_consumption (Tier-1, seventh)` - 6 edges
8. `poor_economy_fuel_odor_sound (Tier-1)` - 5 edges
9. `EngineState (StrEnum)` - 5 edges
10. `EnvironmentalConditions (dataclass)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `LoadState (StrEnum)` --refines--> `legacy symptom catalog`  [EXTRACTED]
  wiki/02_environmental_axes.md → wiki/04_catalog_changelog.md
- `right_after_fillup (legacy, DROPPED)` --conceptually_related_to--> `poor_economy_fuel_odor_sound (Tier-1)`  [INFERRED]
  wiki/04_catalog_changelog.md → wiki/01_symptom_catalog.md
- `SymptomLab Wiki — Index` --documents--> `Two-Tier Symptom Catalog (note)`  [EXTRACTED]
  wiki/00_index.md → wiki/01_symptom_catalog.md
- `SymptomLab Wiki — Index` --documents--> `Three Environmental Context Axes (note)`  [EXTRACTED]
  wiki/00_index.md → wiki/02_environmental_axes.md
- `SymptomLab Wiki — Index` --documents--> `SymptomDNA Part-B Payload Contract (note)`  [EXTRACTED]
  wiki/00_index.md → wiki/03_symptom_dna_payload.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **21-pair catalog validation contract** — wiki_01_symptom_catalog_symptom_catalog, wiki_01_symptom_catalog_allowed_combinations_yaml, wiki_01_symptom_catalog_symptomvalidator_validate [EXTRACTED 1.00]
- **SymptomDNA four-field Part-B payload** — wiki_03_symptom_dna_payload_symptomdna, wiki_03_symptom_dna_payload_tier_1_primary_symptom, wiki_03_symptom_dna_payload_tier_2_subfield_filter, wiki_03_symptom_dna_payload_environmental_conditions, wiki_03_symptom_dna_payload_free_text_notes [EXTRACTED 1.00]
- **COMLab-owned routing/weighting proposals (signal/noise boundary)** — wiki_01_symptom_catalog_comlab_a, wiki_01_symptom_catalog_comlab_b, wiki_01_symptom_catalog_comlab_f, wiki_01_symptom_catalog_comlab_g [EXTRACTED 1.00]

## Communities (11 total, 0 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.15
Nodes (17): allowed_combinations.yaml, DNALab resolve entrypoint, SymptomValidator.__init__, SymptomValidator.validate, cranking, EngineState (StrEnum), EnvironmentalConditions (dataclass), running (+9 more)

### Community 1 - "Community 1"
Cohesion: 0.15
Nodes (13): SymptomLab Wiki — Index, Two-Tier Symptom Catalog (note), COMLab-A (routing weights proposal), COMLab-B (context modifiers + report-trust cap), COMLab-F (per-tier weighting bands), COMLab-G (exhaust-chemistry footprints), exhaust-chemistry footprints, FaultAtlasRouter (+5 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (13): blue_smoke_under_acceleration (Tier-2), COMLab-OIL-KG (oil_consumption routing proposal), Engine Mechanical (PCV/Crankcase), Engine Mechanical (Piston Rings), oil_consumption (Tier-1, seventh), oil_loss_no_visible_smoke (Tier-2), EPA light-duty driveability investigation, legacy symptom catalog (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.18
Nodes (11): coasting_deceleration, coil_dielectric_stress_regime, cold_only, idle, LoadState (StrEnum), manifold vacuum regime (vacuum ∝ 1/throttle), steady_cruise, transient_acceleration (+3 more)

### Community 4 - "Community 4"
Cohesion: 0.25
Nodes (8): backfire_loud_pop (Tier-2), Crank/Cam Position Sensors, engine_dies_or_stalls (Tier-1), Idle-Control (Carbon Restriction), Ignition-Coil / Valve-Timing, intermittent_random_cutout (Tier-2), when_coasting_to_stop (Tier-2), intermittent_random (legacy, reworded)

### Community 5 - "Community 5"
Cohesion: 0.29
Nodes (8): black_smoke (Tier-2), blue_oily_smell (Tier-2), blue_smoke_on_cold_start_clears (Tier-2), Engine Mechanical (Head Gasket), Engine Mechanical (Valve Stem Seals), Fuel-Delivery (Extreme Rich Mixture), visible_exhaust_smoke (Tier-1), white_sweet_smell (Tier-2)

### Community 6 - "Community 6"
Cohesion: 0.25
Nodes (8): constant_vibration_shudder (Tier-2), Coolant-Temp-Sensor / Vacuum Leak, Ignition-Coil / Spark Plug (Misfire), rough_idle_shudder (Tier-1), stalls_on_cold_start (Tier-2), surging_hunting_idle (Tier-2), Vacuum Leak / Idle-Control, constant_shudder (legacy, reworded)

### Community 7 - "Community 7"
Cohesion: 0.25
Nodes (8): EGR-System / Lean-Misfire, Fuel-Delivery (Leaking Injector), just_poor_mpg (Tier-2), knock_pinging_under_load (Tier-2), Oxygen-Sensor / Coolant-Temp-Sensor, poor_economy_fuel_odor_sound (Tier-1), strong_fuel_smell (Tier-2), right_after_fillup (legacy, DROPPED)

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (8): fast_crank_whining (Tier-2), Fuel-Delivery / Coolant-Temp-Sensor, Ignition Primary / Battery / Starter Circuit, no_crank_silent (Tier-2), prolonged_crank_hard_start (Tier-2), Valve-Timing / Mechanical Compression, vehicle_starting_issues (Tier-1), normal_crank_zero_rpm (legacy, reworded)

### Community 9 - "Community 9"
Cohesion: 0.25
Nodes (8): always, hot_only, ignition_sensor_regime, intermittent, OccursDuring (StrEnum), cold_engine_only (legacy, DROPPED), hot_engine_only (legacy, DROPPED), only_when_hot (legacy, DROPPED)

### Community 10 - "Community 10"
Cohesion: 0.29
Nodes (7): Catalyst / Air-Fuel Metering (MAF), flat_sluggish_always (Tier-2), hesitation_throttle_tip_in (Tier-2), Ignition-Coil (Dielectric Breakdown), lack_of_power_hesitation (Tier-1), sudden_jerk_stumble (Tier-2), Throttle Sensor / Transient Fueling

## Knowledge Gaps
- **56 isolated node(s):** `Two-Tier Symptom Catalog (note)`, `Three Environmental Context Axes (note)`, `SymptomDNA Part-B Payload Contract (note)`, `Catalog Changelog — Legacy to Revised (note)`, `Ignition Primary / Battery / Starter Circuit` (+51 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `OccursDuring (StrEnum)` connect `Community 9` to `Community 0`, `Community 1`, `Community 3`?**
  _High betweenness centrality (0.004) - this node is a cross-community bridge._
- **What connects `Two-Tier Symptom Catalog (note)`, `Three Environmental Context Axes (note)`, `SymptomDNA Part-B Payload Contract (note)` to the rest of the system?**
  _56 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.14705882352941177 - nodes in this community are weakly interconnected._