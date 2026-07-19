---
node_type: hld
lab: comlab
module: comlab
subsystem: architecture
implements: []
consumers:
- 'lld: labs/comlab/docs/COMLab_LLD.md'
- 'dld: labs/comlab/docs/COMLab_DLD.md'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py family-routing architecture'
drift_guards: []
tags:
- comlab
- architecture
- hld
source: labs/comlab/docs/COMLab_HLD.md
---

# COMLab High-Level Design (HLD)

**Document type:** HLD — architecture. Companion documents now all exist and are
binding: `COMLab_LLD.md` (file/class spec), `COMLab_DLD.md` (resource manifest +
ops), `COMLab_PRD.md` (wizard UX), `docs/adr/` (numbered decision records), and
`COMLab_BDD.md` (behavioural scenarios).

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_HLD_v1.0_2026-05-21.md`. The v1.0 "open questions for
sign-off" (§12) are all now resolved in code; §12 records the resolutions.

**What changed v1.0 → v2.0 (as-built reconciliation):**

- The Fault-Atlas KG ships as a **directory of 13 per-family JSON files** under
  `comlab/config/kg/` (plus `_kg_schema.json`), not a single file (resolves §12 Q2).
- Three modules the v1.0 draft did not name are now load-bearing:
  `core/perception_contradiction.py`, `core/ecu_hardware_checker.py`, and
  `analytics/delta_engine.py` (the two-operating-point Δ engine feeding the
  router's Phase 5).
- `execution_meta.lab_routing_directive` is **surfaced** in the outbound payload
  (resolves §12 Q6); `user_input_echo_audit` is **kept** COMLab-emitted
  (resolves §12 Q4).
- Observability is real: `comlab/observability/_tracer.py` provides an
  OpenTelemetry-or-no-op tracer; the router and aggregator open spans per stage.

**Authoritative inputs reconciled in this document:**

- `wiki/01_role_boundaries_fusion_spine.md` … `wiki/14_sources_appendices.md` —
  the COMLab domain wiki (canonical truth; code reconciles up to it).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — the binding JSON boundary protocol
  between the five labs.
- `docs/Vocabulary/OBD_VOCABULARY.md`, `docs/Vocabulary/DTC_VOCABULARY.md` —
  canonical identifiers, enums, ranges.
- `CROSS_LAB_DEPENDENCIES.md` — the forward registry of emitter→fusion pairs
  (DEP-1…DEP-10) that COMLab consumes in this final stage.
- The NewArch horizontal DNA-flow architecture (DNA reaches every lab on *input*,
  not after the fact) and its per-lab projection contract (`LabDnaView`).

**Non-goals of this HLD:**

- File-level class signatures and method bodies — `COMLab_LLD.md`.
- JSON schema files for `global_fault_registry.json` and the KG files — `COMLab_LLD.md` §8.
- Resource budgets, latency targets, deployment topology — `COMLab_DLD.md`.
- Wizard screen flow, plausibility error copy, UI gating decisions — `COMLab_PRD.md`.

---

## 1. What COMLab is, in one sentence

COMLab is the **read-only fusion gate** at the terminal end of the 4DLab
pipeline: it accepts pre-validated, DNA-aware JSON fragments from GASLab,
OBDLab, and DTCLab (each of which already saw the `VehicleDNA` on the way in),
runs a deterministic rule-engine triage scored against a flat fault registry,
decorates the winning verdict with structured component metadata from a
passive Fault-Atlas Knowledge Graph, and emits one
`OrchestratorFinalUIOutput` JSON payload to the UI.

**Scope (binding, per `wiki/04_horizon_eras.md`):** the engine targets **petrol
1990–2010, Euro 1–5**, across three horizon buckets (`HORIZON_LEGACY` Euro 1–2,
`HORIZON_ADAPTIVE` Euro 3–4, `HORIZON_MODERN` Euro 5). Post-2010 **Euro 6+**
technology — GPF/DPF inference, LSPI, secondary-air-injection (SAI) inference —
is **out of scope** and is not represented in any schema, registry rule, or KG
node. GDI and early turbocharging are in scope only for vehicles sold within the
1990–2010 window. `HORIZON_MODERN` remains a real era bucket (and the safe
default), capped at this window; it is not the "2010–2020 wideband/GPF" tier the
v1.0 draft described.

---

## 2. Where COMLab sits in 4DLab (post-horizontal-DNA flip)

The architecture changed when `NewArchProposal.md` was accepted: the
`VehicleDNA` payload now reaches every diagnostic lab on its *input* side, not
just COMLab. COMLab loses its monopoly on DNA awareness — and gains a
narrower, cleaner job.

```
                    ┌─────────────┐     ┌──────────────┐
                    │   VINLab    │     │  SymptomLab  │
                    │   VinDNA    │     │  SymptomDNA  │
                    └──────┬──────┘     └──────┬───────┘
                           │                   │
                           ▼                   ▼
                       ┌─────────────────────────────┐
                       │           DNALab            │   (umbrella; only
                       │   build_vehicle_dna()       │    lab allowed to
                       │       → VehicleDNA          │    import other labs)
                       └──────────────┬──────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │   project to per-lab views (done by the assembler /       │
        │   COMLab projector — see §6.1)                            │
        ▼                             ▼                             ▼
 ┌──────────────┐            ┌──────────────┐             ┌──────────────┐
 │   GASLab     │            │   OBDLab     │             │   DTCLab     │
 │  (sees       │            │  (sees       │             │  (sees       │
 │ GasLabDnaView│            │ ObdLabDnaView│             │ DtcLabDnaView│
 │  at INPUT)   │            │  at INPUT)   │             │  at INPUT)   │
 │  fails-fast  │            │  fails-fast  │             │  routing-aware│
 │  on DNA-     │            │  on DNA-     │             │  DTC pruning  │
 │  relative    │            │  relative    │             │               │
 │  plausibility│            │  bounds      │             │               │
 └──────┬───────┘            └──────┬───────┘             └──────┬───────┘
        │ GasLabPayload             │ OBDLivePayload             │ DTCLabPayload
        └─────────────────┬─────────┴─────────────┬──────────────┘
                          │                       │
                          ▼                       ▼
                ┌──────────────────────────────────────────────┐
                │                  COMLab                      │
                │                                              │
                │   ingests:                                   │
                │     OrchestratorInboundRequest               │
                │     = vehicle_dna                            │
                │     + gas_lab_output                         │
                │     + obd_live_data                          │
                │     + dtc_lab_output                         │
                │     + symptom_dna  (top-level, T-FX-5)       │
                │                                              │
                │   does:                                      │
                │     stage A — pydantic + fatal gates +       │
                │               DNA projection + routing       │
                │               directive + degradation mode   │
                │     stage B — fault atlas registry walk      │
                │               (horizon + hardware + symptom  │
                │                pruning, polymorphic O₂ math, │
                │                catalyst-damage override)     │
                │     stage C — fault-atlas KG enrichment      │
                │               (NEW — §5)                     │
                │     stage D — power-loss analytics           │
                │                                              │
                │   produces:                                  │
                │     OrchestratorFinalUIOutput JSON           │
                └────────────────────┬─────────────────────────┘
                                     │
                                     ▼
                                    UI
```

The four upstream lab packages **do not import each other** and **do not
import COMLab**. The only Python import that crosses labs is DNALab importing
VINLab and SymptomLab (the umbrella exception). Every other boundary is JSON
governed by `SEMANTIC_CONTRACT.md`.

The single architectural shift COMLab is reacting to:

> **DNA reaches the labs on input.** COMLab is no longer the only point in the
> system that knows the vehicle's hardware profile. Each lab can fail-fast on
> DNA-relative inputs before its data ever crosses the COMLab boundary, which
> means COMLab's old `Fallback_Error_Execution_Tree` shrinks dramatically:
> "wrong RPM for engine" and "out-of-range trim for sensor type" die upstream,
> not here.

---

## 3. The four core responsibilities

COMLab has four jobs in v1. Anything outside these four is out of scope for
COMLab and belongs in a sibling lab or in DNALab.

1. **Validate** — `OrchestratorInboundRequest` is enforced through one
   Pydantic gate. Any schema drift from a producer is rejected here with a
   stable `ERR-CONTRACT-*` or `ERR-ABORT-*` code that the UI can render as an
   actionable next step. This is the only place in 4DLab where the *combined*
   payload shape is policed.

2. **Project** — the inbound `VehicleDNA` is projected into three slim,
   read-only `LabDnaView` shapes (Gas / OBD / DTC). In production these
   projections are built upstream by the assembler before each lab is called;
   COMLab's projector is the **single source of truth for the projection
   logic**, mirrored by the assembler. (See §6.1 for the projection-ownership
   split.)

3. **Triage** — the flat `global_fault_registry.json` is walked, pruned by
   horizon + hardware + symptom, scored, and one winning fault is selected.
   This is the rule engine. It is deterministic, has no graph traversal at
   runtime, and never modifies any input.

4. **Enrich and serialize** — the winning `fault_id` is looked up in the new
   Fault-Atlas Knowledge Graph (§5) to attach structured repair metadata;
   power-loss analytics are computed; the assembled
   `OrchestratorFinalUIOutput` JSON is returned. This is the only outbound
   side of the COMLab boundary.

Things COMLab explicitly **does not** do:

- Parse the VIN. Horizon is read from `vehicle_dna.vin_dna.euro_emission_category`,
  cylinder count from `vehicle_dna.vin_dna.cylinder_count`. The operational
  checklist in `DNALab_TO_COMLab_FLOW.md` §8 explicitly forbids
  string-slicing the VIN inside COMLab.
- Recompute anything the producer labs already computed. OBDLab owns
  `total_trim_correction_delta`; COMLab consumes it. GASLab owns
  `lambda_chem`; COMLab consumes it. DTCLab owns `routing_tags`; COMLab
  consumes them (and adds the synthetic `POA_HISTORY` injection — §4.4).
- Mutate `VehicleDNA`. COMLab is read-only over every input field.
- Import from any other lab's Python package. Mirror types via the JSON
  contract; never `from gaslab import ...`.

---

## 4. The processing pipeline (HLD-level sequence)

This pipeline is the HLD-level expansion of
`DNALab_TO_COMLab_FLOW.md` §4. File names below refer to the existing
`comlab/` package; the LLD will refine method signatures.

### 4.1 Stage A — `lab_pipeline_aggregator.py`

1. **Pydantic gate.** `OrchestratorInboundRequest(**raw_dict)`. Schema
   violation → reject with `ERR-CONTRACT-001` (regex/range fail) or
   `ERR-CONTRACT-002` (cross-field inconsistency like
   `air_metering_strategy` not matching the air-metering booleans).
2. **Schema-version gate.** If `vehicle_dna.schema_version` is older than
   COMLab's `MIN_SUPPORTED_SCHEMA_VERSION` constant → `ERR-ABORT-005`.
3. **Fatal validity gates (ordered).**
   - `gas_lab_output.sample_validity == "VALID"` else `ERR-ABORT-001`.
     If `symptom_router.route_symptom()` set `suppress_gaslab=True` (e.g.
     `engine_state == will_not_start`), this gate is skipped — absent
     GASLab data is expected, not fatal.
   - `obd_live_data.engine_warmed == true` else `ERR-ABORT-002`. Same
     suppression rule applies when `suppress_obd_live_pids=True`.
   - `vehicle_dna.vin_dna.confidence != "NONE"` else `ERR-ABORT-004`.
4. **Routing directive.** `symptom_router.route_symptom(symptom_dna)` →
   `LabRoutingDirective(suppress_gaslab, suppress_obd_live_pids,
   suppress_mode06_ui, cold_start_mode)`. This is the only piece of
   SymptomDNA that has a current COMLab consumer; the rest
   (`tier_1_primary_symptom`, `tier_2_subfield_filter`,
   `free_text_notes`) are *not* routed yet and the HLD does not invent
   consumers for them.
5. **Degradation classification.**
   - All four producers reported and required fields present →
     `FULL_FUSION`.
   - VinConfidence == `PARTIAL` OR scanner without freeze-frame /
     non-starter scenario → `GAS_DOMINANT`.
6. **DNA projection.** Build the three `LabDnaView` instances (see §6).
   At runtime COMLab does not call back into the labs with them — the
   assembler already did — but COMLab uses them internally for the
   polymorphic O₂ and air-metering math in Stage B.
7. **Perception-contradiction detector.** The ECU's `normalized_obd_lambda`
   is cross-checked against GASLab's `lambda_chem` in
   `comlab/core/perception_contradiction.py` (T-FX-6). Divergence beyond
   the active era's `lambda_tolerance`, with near-normal gas chemistry
   (Lambda Truth filter: 0.90 ≤ `lambda_chem` ≤ 1.10), surfaces an
   `O2_SENSOR_BIASED_LOW` or `O2_SENSOR_BIASED_HIGH` verdict. The signed
   delta and bias verdict populate `PerformanceAnalytics.lambda_perception_delta`
   and `o2_sensor_bias_verdict`. Inert when no OBD lambda is present (no-OBD
   sessions fall back to GASLab measured λ per T-FX-7).
8. **Sanitized payload assembly.** Add `resolved_horizon`,
   `degradation_mode`, `routing_directive`, and the three projected
   views into a working dict that flows into Stage B. The Pydantic
   models from steps 1-3 are preserved by reference; no values are
   re-typed or re-validated.

### 4.2 Stage B — `fault_atlas_router.py` (the rule engine)

1. **Load registry.** `global_fault_registry.json` parsed once at boot;
   the hot path uses the cached list.
2. **Prune by horizon.** Drop rows where
   `target_horizons` does not include the resolved horizon
   (LEGACY / ADAPTIVE / MODERN).
3. **Prune by hardware.** Drop rows whose preconditions contradict
   `VinDNA.emissions.*`, `vin_dna.induction_type`,
   `vin_dna.air_metering_strategy`. A GPF rule on a non-GPF car never
   evaluates; an EGR rule on `egr_equipped == false` never evaluates.
4. **POA synthetic tag.** If
   `gas_lab_output.chemical_state == "POA_SIGNATURE"`, append
   `DTCRoutingTag.POA_HISTORY` to the working routing_tags list. This
   replaces the old cross-lab `GASLab → DTCLab` parameter passing
   (resolved by T-FX-3); see `data_flow_report.md` §6.
5. **Walk remaining rows.** For each candidate fault: chemistry match
   → OBD operator checks (`GREATER_THAN`, `IN_RANGE`,
   `DEVIATES_FROM_TARGET`, etc.) → DTC presence / routing-tag check
   per the fault's `fallback_strategy` → confidence score
   (`base_weight + bonus_on_dtc_match`, capped at 1.0).
6. **Polymorphic O₂ math** via `vin_dna.emissions.upstream_o2_type`
   (4-value enum incl. `WIDEBAND_NB_SIM` per T-FX-4); polymorphic VE
   math via `vin_dna.air_metering_strategy` per the canonical mapping
   in `SEMANTIC_CONTRACT.md` §6.2 / §6.3.
7. **Catalyst-damage-imminent override.** If
   `dtc_lab_output.mil_flashing == true` AND any `confirmed_dtcs`
   matches `^P030[0-9]$`, force `severity_level =
   CRITICAL_IMMEDIATE_STOP` regardless of confidence ranking.
8. **Two-operating-point Δ (optional).** When the request carries a
   `second_operating_point` frame, `analytics/delta_engine.py` differences it
   against the primary (low-idle) channels and emits a typed `DeltaSignature`
   that Phase 5 reads as a **primary** rank term (the Δ-matched fault family is
   promoted above base-weighted static signatures). Absent → the byte-identical
   single-point path and the `SINGLE_POINT` degradation mode. The router exposes
   per-evidence `enable_*` flags (delta, bank-fuse, ECU-fuse, VE-gate,
   fuelsys-gate, ECU-hw, O2-offset, no-start, …) wiring the DEP-2…DEP-10 fusion
   consumers.
9. **Differential siblings (§5.3).** From the highest-scoring non-winning rows,
   take their `fault_id`s, union with editor-curated KG siblings, dedupe, cap at
   5. They feed the runner-up panel in the UI.

### 4.3 Stage C — `fault_atlas_kg.py` (NEW — Fault-Atlas Knowledge Graph)

1. **Lookup.** `fault_atlas_kg.resolve(winning_fault_id)` returns a
   `FaultEnrichment` dict (§5.2). The KG is loaded once at boot from
   `comlab/config/kg/` directory; the hot path is an O(1) dict
   read.
2. **Differential resolution.** For each of the top-3 sibling fault_ids
   from Stage B step 8, attach a slim `{fault_id, fault_name,
   confidence_score}` summary (no full enrichment for runner-ups —
   keeps payload small).

### 4.4 Stage D — `power_loss_analytics.py`

1. **Kinetic power loss %.** Computed from the gas-chemistry deltas and
   `vehicle_dna.vin_dna.cylinder_count`.
2. **Catalyst efficiency index %.** Computed from upstream-vs-downstream
   O₂ ratios when `vin_dna.emissions.downstream_o2_present == true`;
   bypassed otherwise.
3. **Severity level.** `CRITICAL_IMMEDIATE_STOP` /
   `WARNING_DEGRADED_PERFORMANCE` / `OPTIMAL_HEALTH`. Override from
   §4.2 step 7 wins.
4. **Perception-contradiction fields** (`lambda_perception_delta`,
   `o2_sensor_bias_verdict`) are populated earlier by the Stage A
   perception-contradiction detector (§4.1 step 7) and passed through
   unchanged by Stage D.

### 4.5 Stage E — `response.py` (serializer)

Pack the `OrchestratorFinalUIOutput` per §7.4. `session_id` and
`schema_version` echo back from the input verbatim.

---

## 5. The Fault-Atlas Knowledge Graph (KG) — the new piece

This section is the architectural change `COMLabDesign.md` exists to
introduce, distilled to what actually ships.

### 5.1 What it is and what it is not

**It is:** a passive, JSON-only catalog at
`comlab/config/kg/` (one file per fault family + `_kg_schema.json`) that maps every `fault_id` in
`global_fault_registry.json` to a `FaultEnrichment` record (§5.2). Loaded
once at boot, read-only, no graph traversal at runtime. The "graph"
shape is on disk and in the schema (nodes-and-edges JSON, §5.4) so it
can be linted, diffed, and visualised; the runtime hot path is a single
dict lookup by `fault_id`. Edits go through a config-only PR — no
Python is touched when adding a fault.

**It is not:** a new dependency on a graph database. There is no Neo4j,
no networkx at runtime, no SPARQL. The proposal's name "Static Knowledge
Graph" stays for continuity with `COMLabDesign.md`; the
implementation is a versioned JSON file plus a thin loader.

**It is not** a fault registry replacement. `global_fault_registry.json`
keeps owning the *evaluation rules* (operators, thresholds, target
horizons). The KG owns the *enrichment* (what hardware, what zone, what
to do). Strict separation: one file says "this rule fired", the other
says "and here is what that means physically".

**It is not** a runtime cross-lab dependency. The KG file lives entirely
inside `comlab/`. It is not consumed by GASLab, OBDLab, or DTCLab and
will never be imported by them. Per-lab wiki cross-references (e.g.
"see `GAS_WIKI.md` §6 for the chemistry context of `WORN_VALVE_SEALS`")
exist as developer documentation, not as runtime data dependencies.

### 5.2 What a node carries — the consumer-justified field set

Every field is bound to a named consumer in COMLab analytics, the
fault-atlas serializer, or the response payload. The signal/noise rule
strikes any field without one.

| Field | Type | Named consumer (code path) | Justification |
|---|---|---|---|
| `fault_id` | str | `fault_atlas_router.execute_triage_loop` (join key into KG) | Already exists in `global_fault_registry.json`; the join is the KG's purpose. |
| `fault_name` | str | `response.diagnostic_verdict.fault_name` | Already in `OrchestratorFinalUIOutput`. KG is the authoritative source so registry rows do not duplicate the string. |
| `fault_family` | enum (`FaultFamily`) | `response.diagnostic_verdict.fault_family` | Already in the response shape per `DNALab_TO_COMLab_FLOW.md` §5. KG owns the grouping. |
| `component_group` | str | `response.fault_enrichment.component_group` → UI grouping chip | Lets UI group runner-up faults by physical assembly without parsing fault names. |
| `impacted_subsystems` | list[str] | `response.fault_enrichment.impacted_subsystems` → UI badge list | Lets UI render "this fault touches X, Y, Z" badges. |
| `mechanical_failure_mode` | str (≤ 280 chars) | `response.fault_enrichment.mechanical_failure_mode` → UI "what is happening" line | Replaces the unstructured `display_headline` for the "explanation" slot specifically. |
| `ui_remediation_steps` | list[str] (1..8) | `response.fault_enrichment.ui_remediation_steps` → UI numbered steps | Replaces the single `actionable_remediation: str` field with a structured list the UI can render as numbered steps. |
| `differential_siblings` | list[fault_id] (0..5) | `fault_atlas_router` Stage B step 8 + `response.diagnostic_verdict.differential_siblings[]` → UI runner-up panel | Curated runner-ups per fault (editor-maintained), supplements the runtime-derived top-3. |

**Fields explicitly rejected during this design pass** (no consumer
identified, per the signal/noise rule):

- `wiki_refs` — "this fault is described in GAS_WIKI §X" pointers.
  Useful for the editor; no runtime consumer in COMLab. Goes in
  developer comments inside the JSON, not in the typed payload. Drop.
- `severity` — already computed at runtime by `power_loss_analytics`,
  and the override path in §4.2 step 7 can change it. A static
  severity in the KG would lie. Drop.
- `expected_dtcs` — pure documentation; the registry rule already
  encodes the DTC patterns it accepts. Drop.
- `tools_required`, `estimated_repair_hours`, `parts_cost_band` — no
  current UI consumer in v1; can be added in a future bump if and
  when the UI builds a "estimate cost" view. Drop until then.

### 5.3 Differential siblings — runtime top-3 vs editor-curated

Two sources contribute to the runner-up panel:

1. **Runtime top-3** (Stage B step 8). These are the next-highest
   scoring rules from the actual rule-engine walk in this session.
   They reflect "given these readings, here is what nearly fired".
2. **Editor-curated `differential_siblings`** (KG field).
   The editor knows that fault X is commonly confused with fault Y
   even when Y did not score this session. These are the
   "ask the technician to consider" set.

The serializer unions the two sources, deduplicates by `fault_id`, and
caps the total at 5. Each entry in the response is `{fault_id,
fault_name, confidence_score | null}` — `null` for editor-curated
siblings that did not fire this session.

### 5.4 The on-disk shape (HLD-level — LLD will finalise the JSON schema)

```jsonc
{
  "schema_version": "1.0",
  "$schema": "https://json-schema.org/draft-07/schema",
  "title": "COMLab Fault-Atlas Knowledge Graph",
  "nodes": {
    "ERR-E2-MECH-082": {
      "fault_name": "worn_valve_stem_seals",
      "fault_family": "rich_mixture",
      "component_group": "Engine Cylinder Head Assembly",
      "impacted_subsystems": ["Valve Guide Seals", "Combustion Ports"],
      "mechanical_failure_mode":
        "High intake manifold vacuum draws engine oil down worn valve guides into the ports at idle.",
      "ui_remediation_steps": [
        "Run a wet/dry compression test to rule out ring wear.",
        "Inspect valve cover gasket for oil leakage signature.",
        "Replace valve stem seals; verify valve-to-guide oil clearance."
      ],
      "differential_siblings": ["ERR-E3-MECH-085"]
    }
    /* ... one entry per fault_id in global_fault_registry.json ... */
  }
}
```

No top-level `edges` list. The "graph" is implicit:
`(node) -[differential_to]-> (node)` is the only edge type, and it lives
inside each node's `differential_siblings` field. If the v2 design ever
needs richer edges (e.g. `(fault) -[caused_by]-> (root_cause)`), the
field set will grow under §10's change protocol — not before there is a
consumer for it.

### 5.5 Consistency contract with the rule registry

Every `fault_id` that appears in `global_fault_registry.json` MUST have
a corresponding node in the `comlab/config/kg/` directory. Every `fault_id` in the
KG MUST appear in the registry. The check runs as
`tests/e2e/test_kg_registry_consistency.py`. A missing-pair failure is a build
break, not a runtime warning — there is no acceptable "fault fires but cannot be
enriched" path.

---

## 6. DNA projection — who owns what

The horizontal-DNA flip means `VehicleDNA` is no longer a COMLab-private
shape. Three labs need slim views of it, and the projection logic is
shared infrastructure. The split:

### 6.1 Projection ownership

- **COMLab owns the projection logic.** `comlab/projection.py` (new in
  LLD) defines `project(vehicle_dna_json: dict, *, target: Literal["obd",
  "gas", "dtc"]) -> LabDnaView`. The three `LabDnaView` classes are
  Pydantic frozen models with the exact field lists in `data_flow_report.md`
  §1, §2, §3 (15 / 10 / 11 fields respectively; counts verified against live `lab_dna_views.py`).
- **The assembler calls the projector.** In production the assembler is
  the UI layer; in tests/regression it is the test harness; in
  `scripts/run_pipeline_demo.py` it is the demo CLI. The assembler
  projects once, passes the right view to each lab on input, collects
  the lab outputs, and assembles `OrchestratorInboundRequest`.
- **Sibling labs do not import the COMLab projector.** Per project rule
  "no cross-lab Python imports", each lab mirrors its own `LabDnaView`
  shape as a tiny dataclass inside its own package (per `NewArchProposal_
  ImplementationPlan.md` §3 tradeoff 2). The COMLab projector and the
  per-lab mirror must agree on field names and types; a contract test
  in COMLab feeds a known `VehicleDNA` to the projector and asserts the
  shape matches each lab's published JSON schema.

### 6.2 Why COMLab still re-projects internally

Even though the assembler already projected the DNA before calling each
lab, COMLab needs the projected views again to drive its own polymorphic
math in Stage B (O₂ normalisation, VE formula choice). Rather than fish
those fields out of `vehicle_dna.vin_dna.*` ad-hoc throughout the
router code, the router asks the projector for the right view and reads
named fields. This keeps the router decoupled from the deep VehicleDNA
shape and gives one place to enforce projection rules.

### 6.3 What lives in each view

The field lists are authoritative in `data_flow_report.md` §1–§3. They
are not duplicated here — the data flow report is the canonical
specification. The HLD's only addition: each view ships
`resolved_horizon` and `confidence` as required fields, because the
router consumes both unconditionally.

---

## 7. JSON contracts — inbound and outbound

### 7.1 Inbound: `OrchestratorInboundRequest`

The shape comes from `SEMANTIC_CONTRACT.md` §4.5 with one delta
introduced by T-FX-5: `symptom_dna` is a **top-level** field, not nested
under `vehicle_dna`, because `symptom_router.route_symptom()` consumes
it for lab suppression.

```jsonc
{
  "vehicle_dna":      { /* VehicleDNA — SEMANTIC_CONTRACT §4.3 */ },
  "gas_lab_output":   { /* GasLabPayload — §4.4 */ },
  "obd_live_data":    { /* OBDLivePayload — §4.4 + data_flow_report §2 OUT additions */ },
  "dtc_lab_output":   { /* DTCLabPayload — §4.4 + data_flow_report §3 OUT additions */ },
  "symptom_dna":      { /* SymptomDNA — §4.2 (top-level, T-FX-5) */ }
}
```

The exact field set of each producer payload is owned by the producer
lab and locked by `SEMANTIC_CONTRACT.md` §4.4 + the §1–§3 OUT
additions in `data_flow_report.md`. COMLab does not redefine them; it
mirrors them as Pydantic models in `comlab/schemas/ingestion.py`.

### 7.2 What COMLab reads from where

The complete lookup table is `SEMANTIC_CONTRACT.md` §5 — verbatim. The
new HLD does not duplicate it. The only addition is `symptom_dna` at
the top level (consumed by `symptom_router.route_symptom`).

### 7.3 Routing directive (internal)

Produced by `symptom_router.route_symptom(symptom_dna)`, consumed by
`lab_pipeline_aggregator.run_fallback_tree` and `fault_atlas_router`.
Four bools: `suppress_gaslab`, `suppress_obd_live_pids`,
`suppress_mode06_ui`, `cold_start_mode`. This is internal COMLab state;
it does not appear in the inbound or outbound JSON.

### 7.4 Outbound: `OrchestratorFinalUIOutput` (NEW shape)

The v0.1 response in `comlab/schemas/response.py` is augmented for the
KG. The Signal/Noise Matrix in §5.2 above is the gate: every new field
has a named consumer.

```jsonc
{
  "session_id": "DNA_TX_8849201",
  "schema_version": "1.0",

  "execution_meta": {
    "resolved_horizon":            "HORIZON_MODERN",
    "degradation_mode":            "FULL_FUSION",
    "processing_confidence_rating":"HIGH_ASSURANCE",
    "vin_confidence":              "HIGH"
  },

  "diagnostic_verdict": {
    "is_fault_detected":  true,
    "fault_code":         "ERR-E2-MECH-082",
    "fault_name":         "worn_valve_stem_seals",
    "fault_family":       "rich_mixture",
    "display_headline":   "Worn valve stem seals — oil entering combustion at idle.",
    "confidence_score":   0.92,
    "differential_siblings": [
      { "fault_id": "ERR-E3-MECH-085", "fault_name": "worn_piston_rings", "confidence_score": 0.71 }
    ]
  },

  "fault_enrichment": {
    "component_group":        "Engine Cylinder Head Assembly",
    "impacted_subsystems":    ["Valve Guide Seals", "Combustion Ports"],
    "mechanical_failure_mode":"High intake manifold vacuum draws engine oil down worn valve guides into the ports at idle.",
    "ui_remediation_steps": [
      "Run a wet/dry compression test to rule out ring wear.",
      "Inspect valve cover gasket for oil leakage signature.",
      "Replace valve stem seals; verify valve-to-guide oil clearance."
    ]
  },

  "performance_analytics": {
    "kinetic_power_loss_pct":          12.4,
    "catalyst_efficiency_index_pct":   88.1,
    "severity_level":                  "WARNING_DEGRADED_PERFORMANCE"
  }
}
```

**Deletions from the COMLabDesign.md proposal:**

- `user_input_echo_audit` is **kept** in COMLab's outbound contract
  (see ADR-0011: the mobile wizard wipes per-screen state on view switch
  and cannot reliably re-emit typed values from local cache). The field
  is present in `response.py` and `ingestion.py` and
  is surfaced on Screen 6 per PRD §5.5.
- `static_knowledge_graph_enrichment` from the proposal becomes
  `fault_enrichment` — the name overpromised; the shape is what
  matters and is unchanged in content.
- `kinetic_performance_analytics.combustion_inefficiency_index` from
  the proposal is not surfaced separately — the user-facing metric is
  `kinetic_power_loss_pct`, which the existing v0.1 schema already
  exposes.

### 7.5 Error shapes

When Stage A aborts, COMLab returns a discriminated-union response:

```jsonc
{
  "session_id":             "<echoed>",
  "schema_version":         "1.0",
  "execution_meta": {
    "degradation_mode":     "FATAL_INCOMPLETE"
  },
  "error": {
    "error_code":           "ERR-ABORT-001",
    "ui_remediation_message":"Gas sample failed validity check (CO+CO₂+O₂ outside 14-18%). Re-seat probe and re-sample."
  }
}
```

`error_code` taxonomy is inherited from
`DNALab_TO_COMLab_FLOW.md` §6 (ERR-ABORT-001..005, ERR-CONTRACT-001/002,
ERR-VIN-400). No new codes introduced in this HLD.

---

## 8. Module layout (HLD-level — LLD finalises file boundaries)

This is the **as-built** layout of the shipped `comlab/` package (LLD §2 has
the exhaustive blueprint):

```
labs/comlab/
├── docs/
│   ├── COMLab_HLD.md      ← this document
│   ├── COMLab_LLD.md  COMLab_DLD.md  COMLab_PRD.md  COMLab_BDD.md
│   ├── adr/              numbered Architecture Decision Records
│   ├── Vocabulary/      OBD_/DTC_VOCABULARY.md, SEMANTIC_CONTRACT.md
│   └── ARCHIVE/         superseded doc snapshots (read-only history)
├── wiki/                domain truth (00_index … 14_sources_appendices)
├── comlab/
│   ├── schemas/
│   │   ├── ingestion.py        OrchestratorInboundRequest + producer mirrors
│   │   ├── response.py         OrchestratorFinalUIOutput (§7.4)
│   │   ├── vocabulary.py       locked enums (single cross-lab source of truth)
│   │   ├── lab_dna_views.py    Gas/Obd/Dtc LabDnaView frozen models (§6)
│   │   └── kg.py               KGNode / KGFile types
│   ├── projection.py           VehicleDNA dict → LabDnaView (§6)
│   ├── core/
│   │   ├── horizon_context_injector.py   reads resolved_horizon; no VIN parsing (§3)
│   │   ├── symptom_router.py             SymptomDNA → LabRoutingDirective
│   │   ├── lab_pipeline_aggregator.py    Stage A + pipeline entry (§4.1)
│   │   ├── perception_contradiction.py   λ-truth vs λ-perception (§4.1 step 7)
│   │   ├── ecu_hardware_checker.py        ECU digital-lie detector (DEP-9)
│   │   ├── fault_atlas_router.py         Stage B 5-phase triage (§4.2)
│   │   └── fault_atlas_kg.py             Stage C — KG loader + resolver (§5)
│   ├── analytics/
│   │   ├── power_loss_analytics.py       Stage D (§4.4)
│   │   └── delta_engine.py               two-operating-point Δ engine → router Phase 5
│   ├── observability/
│   │   └── _tracer.py                    OpenTelemetry-or-no-op span tracer
│   └── config/
│       ├── global_fault_registry.json    rule rows (registry-only after KG split)
│       ├── eras_sensitivity_masks.yaml   per-horizon threshold masks
│       ├── symptom_prior.yaml  tag_discriminator.yaml  proposals/
│       └── kg/                            13 per-family JSON files + _kg_schema.json (§5)
└── tests/                unit / e2e / integration / regression / generative
```

`horizon_context_injector.py` keeps its name for continuity but is a thin
reader over the inbound `VehicleDNA` plus the `eras_sensitivity_masks.yaml`
lookup — it does not parse the VIN or re-derive the horizon (the v1.0 rename to
`horizon_resolver.py` was not taken; the name stays). The one sanctioned
non-lab Python import is `registry.integration_shim` (`fault_atlas_router.py`
~L1845), a one-way dependency on the repo-root `registry/`, not a cross-lab
import.

---

## 9. Cross-cutting rules COMLab must honour

These come from the project instructions and the existing 4DLab
contracts. Listed explicitly so the LLD inherits them without
ambiguity.

1. **Signal/Noise.** Every new field in any schema this HLD introduces
   has a named consumer in §5.2 / §7.4. "Future use" is not a
   consumer. The KG editor cannot add a field without identifying the
   consumer; the consumer cannot land without the field. (Project rule
   verbatim.)
2. **JSON-only lab boundaries.** No `from gaslab import ...`,
   `from obdlab import ...`, `from dtclab import ...` anywhere in
   `comlab/`. Mirror types in `comlab/schemas/ingestion.py`. (Project
   rule + `SEMANTIC_CONTRACT.md` §1.)
3. **Numeric literals carry wiki citations.** Every threshold that
   the rule engine, the catalyst calculation, or the KG node count
   bands depend on must have a comment citing the source wiki
   (`GAS_WIKI.md §X`, `OBD_VOCABULARY.md §Y`, etc.). The LLD will
   enforce this in `global_fault_registry.json` rows and inside
   `power_loss_analytics.py`.
4. **No re-extraction of the canonical graph.** Each sibling lab's
   `graphify-out/graph.json` is authoritative and read-only. COMLab
   does not consume those graphs at runtime and does not re-run
   graphify.
5. **No ARCHIVE / v2 / v6 imports.** `docs/ARCHIVE/` (and any legacy v2/v6
   trees) exist for historical reading only; no Python under `comlab/` may
   import from them or open files inside them at runtime.
6. **Read-only over inputs.** COMLab never mutates a `VehicleDNA`,
   `GasLabPayload`, `OBDLivePayload`, or `DTCLabPayload`. Sanitization
   produces a derived working dict; the originals are immutable.
7. **`schema_version` echo.** The inbound `vehicle_dna.schema_version`
   appears verbatim in the outbound payload (already in the v0.1
   response shape).

---

## 10. Change protocol — how this HLD evolves

The HLD inherits the change protocol from `SEMANTIC_CONTRACT.md` §10
because every JSON change here is a contract change. To summarise:

- **Patch (clarification, typo, example):** one reviewer, one-line PR.
- **Minor (new optional field with a named consumer, new growing-enum
  value, tightened range that does not break existing producers):**
  two reviewers (COMLab owner + at least one producer lab).
- **Major (rename, remove, restrict previously-allowed value, change
  JSON shape):** RFC document required, 7-day comment window, all
  producer labs sign off.

The KG file (`fault_atlas_kg.json`) carries its own `schema_version`
(starts at "1.0"). KG **content** edits (adding a node, fixing a
remediation step, adjusting a `differential_siblings` list) are minor
bumps to the KG file, not to the contract. KG **schema** edits
(adding/removing a field) are contract-major.

---

## 11. What was kept, what was rejected from `COMLabDesign.md`

For traceability — the COMLabDesign proposal was a substantial
document. This HLD adopts only the parts that survive reconciliation
with the rest of 4DLab.

| From the proposal | Disposition | Why |
|---|---|---|
| Passive Static Knowledge Graph, decoupled from rule engine | **Kept** as the Fault-Atlas KG (§5). | Genuine architectural addition; cleanly separates "rule fired" from "what to fix". |
| `global_fault_registry.json` as flat rule registry | **Kept** (already in v0.1). | Matches existing OrchestratorLabBP and the §4.2 walk. |
| `orchestrator_skg_map.json` JSON shape | **Kept in spirit** as `fault_atlas_kg.json`. | Renamed to "KG" honestly; same on-disk pattern. |
| `fault_enrichment` block in the outbound payload | **Kept** (§7.4). | Each field has a named UI consumer. |
| `user_input_echo_audit` block | **Rejected from COMLab's contract.** | No consumer in COMLab analytics or routing. UI layer's responsibility. Open question §12 Q4. |
| Plausibility / decimal-misplacement sentinels in `lab_pipeline_aggregator` | **Moved upstream.** | Belongs at per-lab DNA-aware ingestion (post-horizontal-DNA flip). COMLab sees pre-validated data. |
| `idle_baseline` / `raised_2500_rpm` two-RPM matrix as the inbound shape | **Rejected.** | Contradicts `SEMANTIC_CONTRACT.md`. The two-RPM bucketing is internal to GASLab/OBDLab; COMLab sees one already-bucketed payload per lab. |
| VIN parsing inside `horizon_context_injector.py` | **Rejected.** | DNALab pre-computes `resolved_horizon` and ships it. `DNALab_TO_COMLab_FLOW.md` §8 explicitly forbids COMLab-side VIN string-slicing. |
| 4-script module count (drops `symptom_router.py`) | **Rejected.** | `symptom_router` produces the `LabRoutingDirective` consumed by Stage A and Stage B. Required. |
| Stub-grade `OBDLiveDataPayload` (only shrtft1/longft1/engine_warmed) | **Rejected.** | `data_flow_report.md` §2 already flagged the gap; the full computed-analytics surface (`ve_pct`, `total_trim_correction_delta`, `normalized_obd_lambda`, etc.) is required for the router to function. |
| Absence of `SymptomDNA` in the inbound payload | **Rejected.** | T-FX-5 elevates `symptom_dna` to top-level; the four routing-directive flags depend on it. |
| Hard-coded `0.0` injection for missing trims on legacy cars | **Rejected for non-legacy paths.** | `null`-vs-`0.0` distinction is correct in the proposal but per-lab DNA-aware ingestion is the right enforcement point. COMLab keeps the `GAS_DOMINANT` degradation mode for the legacy-no-scanner case but does not silently substitute zeros into trim fields. |
| `WORN_VALVE_SEALS` as the fault key | **Renamed.** | Use `fault_id` (e.g. `ERR-E2-MECH-082`) per the existing registry convention, not free-form `SCREAMING_SNAKE` strings. The KG's `fault_name` field carries the snake_case human-readable form (`worn_valve_stem_seals`). |
| 2.5 MB total config size envelope | **Deferred to DLD.** | Resource budget belongs in DLD; flagged here so the LLD is built with it in mind. |
| 250 ms latency target | **Deferred to DLD.** | Same. |
| Two parallel "HLD: Run-time State" + "HLD: Manual User Input Matrix" sections in the proposal | **Collapsed into one HLD here.** | The manual-input dimension belongs in the PRD; this HLD covers architecture. |

---

## 12. Open questions — resolved in code (v1.0 → v2.0)

The v1.0 draft's six sign-off questions are all now settled in the shipped
package. Recorded here for traceability; the binding rationale for the
architecturally significant ones lives in `docs/adr/`.

1. **Differential siblings — runtime top-N / total cap.** Resolved: total cap
   **5** (`DiagnosticVerdict.differential_siblings` is `max_length=5`, KGNode
   `differential_siblings` `max_length=5`); runtime siblings unioned with
   editor-curated, deduped by `fault_id`.
2. **KG file location.** Resolved: **directory** of 13 per-family JSON files
   under `comlab/config/kg/` + `_kg_schema.json` — not a single file. Loaded by
   `fault_atlas_kg.FaultAtlasKG`.
3. **KG editorship.** Resolved operationally: per-family files keep each domain
   editable independently; the registry⇆KG consistency test
   (`tests/e2e/test_kg_registry_consistency.py`) is the build-break gate.
4. **`user_input_echo_audit`.** Resolved: **kept**, COMLab-emitted pass-through
   (the mobile wizard wipes per-screen state). Present in `ingestion.py` and
   `response.py`; Stage D emits a sentinel when absent. See PRD §5.5.
5. **Rename `horizon_context_injector.py`.** Resolved: **not renamed** — name
   retained, behaviour is read-only horizon lookup.
6. **Serialising `LabRoutingDirective`.** Resolved: **surfaced** as
   `execution_meta.lab_routing_directive` (`LabRoutingDirectiveOut`, with
   `reasons[]`) so the UI can grey out suppressed sections. See PRD §5.6.

---

## 13. References

- `wiki/00_index.md` … `wiki/14_sources_appendices.md` — COMLab domain truth
  (code reconciles up to the wiki). Notable: `01_role_boundaries_fusion_spine`,
  `04_horizon_eras` (scope reminder: **petrol 1990–2010, Euro 1–5**;
  post-2010 Euro 6+ tech — GPF/LSPI/secondary-air — out of scope),
  `07_pipeline_stages`, `08_scoring_to_fusion_rework`, `11_two_point_delta`.
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — binding cross-lab JSON boundary
  protocol; this HLD operates inside it.
- `docs/Vocabulary/OBD_VOCABULARY.md`, `docs/Vocabulary/DTC_VOCABULARY.md` —
  canonical identifiers, enums, ranges.
- `CROSS_LAB_DEPENDENCIES.md` — forward registry of emitter→fusion pairs
  (DEP-1…DEP-10) consumed at this final stage.
- `COMLab_LLD.md` / `COMLab_DLD.md` / `COMLab_PRD.md` / `COMLab_BDD.md` /
  `docs/adr/` — companion design records.
- `docs/ARCHIVE/COMLab_HLD_v1.0_2026-05-21.md` — superseded draft (history).
