# OBDLab REEXTRACTION_SPEC — v1 (2026-05-20)

**Module:** `OBDLab` | **Source wiki:** `OBDLab_KG_Wiki.md` (v5.0, 1290 lines)
**Cross-vocab:** `COMLab/docs/wiki/OBD_VOCABULARY.md`
**Pattern reference:** GASLab augmented pass (success) · DTCLab prompt (T-PREP-1 structure)

---

## §0 — Root cause (expected, not yet run)

The OBDLab wiki has the same structural class as GASLab and DTCLab at extraction time:

**Problem 1 — Tail truncation.** `graphify --wiki` stops reading the source file around §12. The wiki's "Domain reference" sections (28 fault profiles, powertrain clusters, ignition timing, vacuum/MAP, misfire) start after line ~530 and run to line 1289. A vanilla single-pass extraction will miss all 28 fault profiles, the full TrimAnalyticsGate enum, and all cross-domain reference sections. Canary: if profiles 15–28 (WORN_ENGINE through EVAP_CANISTER_SATURATED) produce zero nodes, truncation hit.

**Problem 2 — Table-skipping.** The 28 fault profile PID tables (each is a markdown table with PID / SI / StI / Reasoning columns) will not produce edges without an explicit table-row→edge prompt rule. Same failure mode as DTCLab routing-tag tables.

**Problem 3 — Cross-file references.** The wiki uses inline `OBD_VOCABULARY.md §N.M` citations throughout. Without an explicit cross-file edge extraction rule, these become dangling text rather than graph edges.

**Solution (proven on GASLab and DTCLab):** augmented chunked re-extraction with table-row→edge and cross-file citation rules, followed by Option 3 deterministic patch for any edges the LLM still misses.

---

## §1 — Source files for extraction

| File | Role | Key sections |
|---|---|---|
| `OBDLab_KG_Wiki.md` | Primary — module logic + 28 fault profiles | §2 pipeline, §4 physics gates, §6 enums, §10–12 computation, Domain references |
| `COMLab/docs/wiki/OBD_VOCABULARY.md` | Vocabulary reference — cross-file nodes | §2 PIDs, §3 RPM bands, §4 VIN switches, §5 derived nodes, §6 fault families, §17 ChemicalSignature, §18–21 domain rules |

**Do NOT extract from `RefDocs/` subdirectories** — these are raw source materials that were already synthesised into the two wiki files above. Extracting them would produce duplicate or conflicting nodes.

---

## §2 — Augmented extraction configuration

### §2.1 Chunking rules (anti-truncation)

The wiki is 1290 lines. Split into chunks with ≤ 400 lines each and merge results before community detection:

| Chunk | Lines | Content |
|---|---|---|
| `chunk_01` | 1–450 | §1 Standards → §12 Trim vector |
| `chunk_02` | 451–850 | Domain reference: Fuel trim → Profile 14 |
| `chunk_03` | 851–1289 | Profile 15 → Misfire diagnostics + Document index |

Truncation canary: `chunk_03` must produce at minimum the following nodes — `WORN_ENGINE`, `FLAT_CAMSHAFT`, `GDI_INTAKE_VALVE_CARBON`, `WORN_PISTON_RINGS`, `WORN_VALVE_SEALS`, `POA_SIGNATURE`, `WRONG_VALVE_TIMING`, `EGR_STUCK_CLOSED`, `EGR_STUCK_OPEN`, `VVT_FAILURE`, `EVAP_CANISTER_SATURATED`. If fewer than 8 of these appear in the graph post-merge, truncation recurred — investigate chunk-merge logic before proceeding.

### §2.2 Augmented prompt rules

Add these rules to the extractor prompt in addition to default graphify rules:

**Rule A — Enum value enumerates:**
> When an entity is declared as a `StrEnum` class with named members, emit one `enumerates` edge per member: `{ClassName} --enumerates--> {MemberName}`. Example: `RpmStateBucket --enumerates--> STABILIZED_IDLE`.

**Rule B — Table-row → edge (fault profile PIDs):**
> For each "### Profile N — `CHEMICAL_SIGNATURE`" section, emit the chemical signature name as a node and connect it to its associated PIDs with a `characterised_by` edge. Example: `RICH_MIXTURE --characterised_by--> longft1_negative`. Treat the SI column and the StI column as distinct operating contexts. Only emit edges for PID values with a clear direction (positive / negative / stuck / elevated / etc.) — do not emit edges for "Normal" or "N/A" entries.

**Rule C — Cross-file citation → edge:**
> When prose contains `OBD_VOCABULARY.md §N.M` or `SEMANTIC_CONTRACT.md §N.M`, emit a `cross_references` edge from the current entity to a node representing that section. Example: `VERoutingMode --cross_references--> AirMeteringStrategy_OBD_VOCAB_4.2`.

**Rule D — Physics Gate → monitored PID:**
> For each `Physics_Gate_N` rule, emit a `monitors` edge to each PID or derived node named in the trigger condition. Example: `Physics_Gate_1 --monitors--> engine_rpm`.

**Rule E — VIN routing switch → internal mode:**
> When prose states "maps 1-to-1 to" or "driven by" between a cross-vocab enum and a wiki-internal enum, emit a `maps_to` edge. Example: `VERoutingMode --maps_to--> AirMeteringStrategy`.

**Rule F — Analytics gate → guard condition:**
> For each entry in the `TrimAnalyticsGate` enum, emit a `gated_by` edge from the analytics subject (trim analytics, normalized_obd_lambda, OBDLivePayload) to the gate condition node. Example: `trim_analytics --gated_by--> engine_warmed`.

**Rule G — Derived node → computation step:**
> When a derived node (total_trim_correction_delta, calculated_ve, normalized_obd_lambda, engine_warmed) is described as computed or produced by a processing class, emit a `computes` edge from the class to the derived node. Example: `SensorSignalTranslator --computes--> normalized_obd_lambda`.

**Rule H — Hex token / PID code → canonical node:**
> When a SAE J1979 PID code (`010C`, `0106`, etc.) appears adjacent to a PID name, emit a `has_pid_code` edge: `engine_rpm --has_pid_code--> PID_010C`.

---

## §3 — Relation vocabulary

| Relation | Direction | Meaning |
|---|---|---|
| `enumerates` | EnumNode → EnumValue | Enum class declares this value |
| `maps_to` | InternalEnum → CrossVocabEnum | 1-to-1 semantic equivalence across wiki boundary |
| `monitors` | PhysicsGate → PIDNode | Gate reads this sensor/field to evaluate |
| `gated_by` | AnalyticsNode → GateCondition | Analytics only valid when condition passes |
| `computes` | ProcessingClass → DerivedNode | Class produces this derived value |
| `validates` | ProcessingClass → BoundsNode | Class enforces these boundary rules |
| `cross_references` | WikiSection → VocabSection | Explicit wiki cross-citation |
| `characterised_by` | ChemicalSignature → PIDPattern | Fault shows this PID pattern |
| `routes_to` | RoutingModeValue → Formula | This mode triggers this computation path |
| `exposed_as` | InternalNode → PublicField | Internal computation exposed via this public field |
| `described_in` | Node → SourceDoc | Authoritative definition is in this file |

**Forbidden relations** (automatic extraction failure signal — must be zero):
- `semantically_similar_to` between any two ChemicalSignature values
- `conceptually_related_to` between any two domain nodes (enums, PIDs, gates, fault profiles)

---

## §4 — Proof-set (26 edges)

These edges are structurally guaranteed by the wiki's prose. ≥ 20/26 must be present after augmented extraction + any Option 3 patch. Use these as the deterministic patch list if the augmented pass misses them.

Node labels below are human-readable. After first extraction run, record the exact graphify-assigned node IDs in §4.1 below.

### §4.1 Proof-set table

| # | Source | Relation | Target | Wiki §location | Required for criterion |
|---|---|---|---|---|---|
| 1 | `RpmStateBucket` | `enumerates` | `STABILIZED_IDLE` | §6.1 | C1 |
| 2 | `RpmStateBucket` | `enumerates` | `STRESS_IDLE` | §6.1 | C1 |
| 3 | `RpmStateBucket` | `enumerates` | `REGULATORY_HIGH_IDLE` | §6.1 | C1 |
| 4 | `RpmStateBucket` | `enumerates` | `COLD_OPEN_LOOP_INVALID` | §6.1 | C1 |
| 5 | `VERoutingMode` | `enumerates` | `DUAL_MAF_MAP_CROSSCHECK` | §6.2 | C1 |
| 6 | `VERoutingMode` | `enumerates` | `MAP_ONLY_SPEED_DENSITY` | §6.2 | C1 |
| 7 | `VERoutingMode` | `enumerates` | `MAF_ONLY` | §6.2 | C1 |
| 8 | `VEValidity` | `enumerates` | `FAULT_MAF_CONTAMINATION` | §6.4 | C1 |
| 9 | `TrimAnalyticsGate` | `enumerates` | `ENGINE_COLD` | §6.5 | C1 |
| 10 | `TrimAnalyticsGate` | `enumerates` | `O2_FAULT_ACTIVE` | §6.5 | C1 |
| 11 | `O2FailureMode` | `enumerates` | `SLUGGISH` | §6.7 | C1 |
| 12 | `O2FailureMode` | `enumerates` | `WRONG_CENTERLINE` | §6.7 | C1 |
| 13 | `VERoutingMode` | `maps_to` | `AirMeteringStrategy` | §6.2 — "maps 1-to-1" | C5 |
| 14 | `O2NormalizationMode` | `maps_to` | `upstream_o2_sensor_type` | §6.3 — "Driven by VinDNA" | C5 |
| 15 | `PIDIngestionValidator` | `validates` | `physical_sensor_bounds` | §2.3, §3.1 | C3 |
| 16 | `SensorSignalTranslator` | `computes` | `normalized_obd_lambda` | §2.3, §11 | C3 |
| 17 | `SensorSignalTranslator` | `computes` | `total_trim_correction_delta` | §2.3, §12.1 | C3 |
| 18 | `SensorSignalTranslator` | `computes` | `calculated_ve` | §2.3, §10 | C3 |
| 19 | `Physics_Gate_1` | `monitors` | `engine_rpm` | §4 table | C4 |
| 20 | `Physics_Gate_2` | `monitors` | `coolant_temp_c` | §4 table | C4 |
| 21 | `Physics_Gate_3` | `monitors` | `calculated_ve` | §4 table | C4 |
| 22 | `WORN_PISTON_RINGS` | `characterised_by` | `shrtft1_near_zero_at_SI` | Profile 22 — truncation canary | C2 |
| 23 | `EVAP_CANISTER_SATURATED` | `characterised_by` | `EVAP_purge_duty_cycle` | Profile 28 — truncation canary | C2 |
| 24 | `VVT_FAILURE` | `characterised_by` | `cam_position_desired_vs_actual` | Profile 27 — truncation canary | C2 |
| 25 | `OBDLivePayload` | `cross_references` | `SEMANTIC_CONTRACT_4_4` | §5 — "Defined authoritatively in SEMANTIC_CONTRACT §4.4" | C6 |
| 26 | `GDI_INTAKE_VALVE_CARBON` | `characterised_by` | `shrtft1_positive_at_idle` | Profile 18 | C2 |

> **After first extraction:** populate §4.2 below with the actual graphify node IDs so the Option 3 patch script has exact keys.

### §4.2 Actual node IDs (populated 2026-05-20 after augmented chunked extraction + Option 3 patch)

```
# Format: human_label = graphify_node_id
RpmStateBucket           = out1a::chunk_01a_obdlab_kg_wiki_rpmstatebucket
STABILIZED_IDLE          = out1a::chunk_01a_obdlab_kg_wiki_stabilized_idle
STRESS_IDLE              = out1a::chunk_01a_obdlab_kg_wiki_stress_idle
REGULATORY_HIGH_IDLE     = out1a::chunk_01a_obdlab_kg_wiki_regulatory_high_idle
COLD_OPEN_LOOP_INVALID   = out1a::chunk_01a_obdlab_kg_wiki_cold_open_loop_invalid
VERoutingMode            = out1a::chunk_01a_obdlab_kg_wiki_veroutingmode
DUAL_MAF_MAP_CROSSCHECK  = out1a::chunk_01a_obdlab_kg_wiki_dual_maf_map_crosscheck
MAP_ONLY_SPEED_DENSITY   = out1a::chunk_01a_obdlab_kg_wiki_map_only_speed_density
MAF_ONLY                 = out1a::chunk_01a_obdlab_kg_wiki_maf_only
VEValidity               = out1b::obdlab_kg_wiki_vevalidity
FAULT_MAF_CONTAMINATION  = out1b::obdlab_kg_wiki_vevalidity_fault_maf_contamination
TrimAnalyticsGate        = out1b::obdlab_kg_wiki_trimanalyticsgate
ENGINE_COLD              = out1b::obdlab_kg_wiki_trimanalyticsgate_engine_cold
O2_FAULT_ACTIVE          = out1b::obdlab_kg_wiki_trimanalyticsgate_o2_fault_active
O2FailureMode            = out1b::obdlab_kg_wiki_o2failuremode
SLUGGISH                 = out1b::obdlab_kg_wiki_o2failuremode_sluggish
WRONG_CENTERLINE         = out1b::obdlab_kg_wiki_o2failuremode_wrong_centerline
AirMeteringStrategy      = out1a::airmeteringstrategy
O2NormalizationMode      = out1a::chunk_01a_obdlab_kg_wiki_o2normalizationmode
upstream_o2_sensor_type  = out1b::obdlab_kg_wiki_upstream_o2_sensor_type
PIDIngestionValidator    = out1a::chunk_01a_obdlab_kg_wiki_pidingestionvalidator
SemanticConsistencyChecker = out1a::chunk_01a_obdlab_kg_wiki_semanticconsistencychecker
SensorSignalTranslator   = out1a::chunk_01a_obdlab_kg_wiki_sensorsignaltranslator
physical_sensor_bounds   = out1a::chunk_01a_obdlab_kg_wiki_physical_sensor_bounds_json
normalized_obd_lambda    = out1a::chunk_01a_obdlab_kg_wiki_normalized_obd_lambda
total_trim_correction_delta = out1a::chunk_01a_obdlab_kg_wiki_total_trim_correction_delta
calculated_ve            = out1a::chunk_01a_obdlab_kg_wiki_calculated_ve
Physics_Gate_1           = out1a::chunk_01a_obdlab_kg_wiki_physics_gate_1
Physics_Gate_2           = patch_physics_gate_2         (Option 3 patch)
Physics_Gate_3           = patch_physics_gate_3         (Option 3 patch)
Physics_Gate_4           = patch_physics_gate_4         (Option 3 patch)
engine_rpm               = out1a::chunk_01a_obdlab_kg_wiki_engine_rpm
coolant_temp_c           = out1a::chunk_01a_obdlab_kg_wiki_coolant_temp_c
OBDLivePayload           = out1a::chunk_01a_obdlab_kg_wiki_section_5_obdlivepayload
SEMANTIC_CONTRACT_4_4    = patch_semantic_contract_4_4  (Option 3 patch)
WORN_PISTON_RINGS        = out3a::chunk_03a_obdlab_kg_wiki_profile_22
VVT_FAILURE              = out3a::chunk_03a_obdlab_kg_wiki_profile_27
GDI_INTAKE_VALVE_CARBON  = out3a::chunk_03a_obdlab_kg_wiki_profile_18
EVAP_CANISTER_SATURATED  = patch_evap_canister_saturated (Option 3 patch)
```

---

## §5 — Success criteria (all 8 must pass)

| # | Criterion | Minimum pass threshold | Notes |
|---|---|---|---|
| C1 | All 7 OBDLab enum types present as nodes | 7/7 enum class nodes in graph | RpmStateBucket, VERoutingMode, O2NormalizationMode, VEValidity, TrimAnalyticsGate, NodeSensorStatus/NodeMAFStatus/NodeMAPStatus, O2FailureMode |
| C2 | Fault profile nodes ≥ 20/28 | ≥ 20 ChemicalSignature-linked nodes | Profiles 1–14 should be easy; 15–28 require chunk_02/chunk_03 to land |
| C3 | Processing pipeline classes all 3 present | 3/3 nodes | PIDIngestionValidator, SemanticConsistencyChecker, SensorSignalTranslator |
| C4 | Physics Gates ≥ 2/4 present with monitor edges | 2 gates with ≥ 1 `monitors` edge each | Physics_Gate_1 through Physics_Gate_4 (§4 table) |
| C5 | Cross-file mapping edges ≥ 2 | ≥ 2 `maps_to` edges to OBD_VOCABULARY nodes | VERoutingMode→AirMeteringStrategy + O2NormalizationMode→upstream_o2_type |
| C6 | OBDLivePayload node present with cross-ref to SEMANTIC_CONTRACT | 1 node + 1 cross_references edge | Payload schema lives in SEMANTIC_CONTRACT §4.4 |
| C7 | Zero forbidden relations between domain nodes | 0 `semantically_similar_to` or `conceptually_related_to` between ChemicalSignature values | Any presence = extraction quality failure |
| C8 | Proof-set recovery | ≥ 20/26 edges | After augmented pass + Option 3 patch |

---

## §6 — Escalation rule

If C2 still shows fewer than 20/28 fault profile nodes **AND** C4/C5 fail AFTER both the augmented+chunked extraction (step 2) AND the deterministic patch (step 4), **STOP**. That is a graphify chunk-merge failure, not a wiki problem. Surface the failing chunk cache files. Do not run a third same-shape extraction.

---

## §7 — On completion

1. Write `graphify-out/STEP1_VERIFICATION_LOG.md` with:
   - Run date + pass number
   - Per-criterion results (C1–C8)
   - Proof-set recovery count (N/26)
   - Root-cause recap: what the augmented pass caught vs what Option 3 patched
   - Spot-check: 5 random non-proof-set edges verified against source wiki citations

2. Create `OBDLAB_PROGRESS.md` at OBDLab root (if not present); mark T-PREP-1 done.

3. Commit as one change: `REEXTRACTION_SPEC.md` + graphify artifacts + verification log + progress file.
