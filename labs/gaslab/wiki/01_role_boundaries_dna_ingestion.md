---
chunk_id: GASWIKI-01
title: "Role, Boundaries & DNA-Gated Ingestion"
doc: GAS_WIKI
version: v2.0
summary: "Where GASLab sits in 4DLab, what it sees and emits (GasLabPayload), the slim GasLabDnaView it consumes, and the DNA-gated ingestion model that pushes per-vehicle input bounds to the UI."
covers_v1_sections: [1, 2, 3]
entities_defined: [CONCEPT_ROLE, CONCEPT_GASLAB_INPUTS, CONCEPT_GASLABPAYLOAD, CONCEPT_GASLABDNAVIEW, CONCEPT_DNA_GATED_INGESTION]
related_chunks: [GASWIKI-02, GASWIKI-04, GASWIKI-10, GASWIKI-11]
sources: ["GAS_WIKI.md v1.0 §1–3", "SEMANTIC_CONTRACT.md §4.4", "GAS_VOCABULARY.md §12"]
node_type: "wiki"
lab: "gaslab"
module: "gaslab"
subsystem: "payload-boundary"
implements:
  - "labs/gaslab/gaslab/contracts.py"
  - "labs/gaslab/gaslab/dna_view.py"
  - "labs/gaslab/gaslab/process.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py GasLabPayload ingestion"
  - "comlab: labs/comlab/comlab/schemas/vocabulary.py sample_validity/ChemicalSignature mirror"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py chemical_state routing"
drift_guards:
  - "labs/gaslab/tests/unit/test_contracts.py"
  - "labs/gaslab/tests/unit/test_dna_view.py"
  - "labs/gaslab/tests/unit/test_process.py"
tags: ["gaslab", "payload-boundary", "wiki"]
source: "labs/gaslab/wiki/01_role_boundaries_dna_ingestion.md"
---

# 1. Role, Boundaries & DNA-Gated Ingestion

> **Chunk summary.** This chunk covers the physical role of GASLab, its input/output boundaries, the slim DNA projection it consumes, and the DNA-gated ingestion model in which the UI (not GASLab) enforces per-vehicle input bounds.

## 1.1 Role and boundaries {#CONCEPT_ROLE}

GASLab is one of four leaves of the 4DLab fan-in. It converts a technician-entered 5-gas reading plus a slim DNA slice into one canonical `chemical_state`.

```
       DNALab.VehicleDNA  ──► GasLabDnaView (slim projection)
                                     │
   technician-entered 5-gas reading ─┤
                                     ▼
                              ┌─────────────┐
                              │   GASLab    │
                              │  process()  │
                              └──────┬──────┘
                                     ▼
                            GasLabPayload (JSON)
                                     ▼
                             COMLab aggregator
```

GASLab is a **separate codebase** and a **separate cowork account** from COMLab. The only allowed cross-lab import is DNALab → VINLab + SymptomLab. **GASLab never imports COMLab.**

**Operating envelope.** Petrol vehicles 1990–2010 (Euro 1 – Euro 5); manually-entered analyser readings (no live CAN streaming); 5-gas analysers only (no 4-gas fallback — NOₓ channel required); warm-engine samples only (cold open-loop is rejected, see → CONCEPT_RPM_BUCKET in GASWIKI-02). Post-2010 "modern" chemistry (Euro 6/7, 2010–2020 patterns) is out of scope.

## 1.2 What GASLab sees {#CONCEPT_GASLAB_INPUTS}

| Input | Source | Notes |
|---|---|---|
| HC (ppm) | technician form | NDIR channel reading |
| CO (vol %) | technician form | NDIR channel reading |
| CO₂ (vol %) | technician form | NDIR channel reading |
| O₂ (vol %) | technician form | electrochemical or paramagnetic |
| NOₓ (ppm) | technician form | electrochemical; 5-gas only — required |
| `engine_state_bucket` | UI form | `STABILIZED_IDLE` \| `REGULATORY_HIGH_IDLE` \| `STRESS_IDLE` |
| `GasLabDnaView` | COMLab projector | slim DNA slice (→ CONCEPT_GASLABDNAVIEW) |

## 1.3 What GASLab emits — GasLabPayload {#CONCEPT_GASLABPAYLOAD}

The contract surface, governed by `SEMANTIC_CONTRACT.md` §4.4 (with the v1.1 widening that put all five measured gases on the wire):

```jsonc
{
  "chemical_state": "RICH_MIXTURE",       // 34-value enum, see GAS_VOCABULARY §3
  "gas_co": 4.5,                          // vol %
  "gas_hc": 650,                          // ppm
  "gas_co2": 9.5,                         // vol %
  "gas_o2": 0.1,                          // vol %
  "gas_nox": 15,                          // ppm
  "lambda_chem": 0.82,                    // Brettschneider
  "lambda_measured": 1.02,                // optional directly-measured analyser λ (no-OBD path)
  "sample_validity": "VALID"              // VALID | BORDERLINE | INVALID | EXTERNAL_O2_SUSPECT
}
```

The contract widening (`gas_co2`, `gas_nox`) requires a matching update to `COMLab/comlab/schemas/ingestion.py::GasLabPayload` and to `SEMANTIC_CONTRACT.md` itself before GASLab is wired to COMLab — see `GAS_VOCABULARY.md` §12.1.

GASLab returns **exactly one** `chemical_state`; ambiguity is collapsed by rule priority (→ GASWIKI-04 named overrides).

## 1.4 The GasLabDnaView — the slim DNA slice {#CONCEPT_GASLABDNAVIEW}

GASLab does not consume the full `VehicleDNA`. COMLab's projector hands it a typed slice:

| Field | From `VinDNA` path | Used for |
|---|---|---|
| `engine_displacement_liters` | `vin_dna.engine_displacement_liters` | dilution math sanity, future VE checks |
| `cylinder_count` | `vin_dna.cylinder_count` | per-cylinder misfire math (`ΔO₂ ≈ 21 / N`) |
| `number_of_banks` | `vin_dna.number_of_banks` | future bank-asymmetry signatures |
| `euro_emission_category` | `vin_dna.euro_emission_category` | scales healthy/fault thresholds (→ CONCEPT_EURO_SCALING) |
| `fuel_delivery_type` | `vin_dna.fuel_delivery_type` | enables `GDI_*` fault classes |
| `induction_type` | `vin_dna.induction_type` | unlocks forced-induction NOₓ signatures; turbo-seal oil sub-mode |
| `emissions.upstream_o2_type` | `vin_dna.emissions.upstream_o2_type` | calibrates sensor-bias signatures |
| `emissions.has_catalyst` (from `downstream_o2_present`) | `vin_dna.emissions.downstream_o2_present` | switches "with cat" / "no cat" threshold tables |
| `emissions.egr_equipped` | `vin_dna.emissions.egr_equipped` | enables `EGR_STUCK_*` fault classes |
| `target_lambda_v112` | `vin_dna.target_lambda_v112` | per-vehicle CoC empirical target |
| `co_low_idle`, `co_high_idle` | `vin_dna.co_low_idle/high_idle` | per-vehicle CoC empirical bounds |
| `fuel_type` *(proposed v2)* | `vin_dna.fuel_type` | E5/E10/winter-blend correction context `[v2: q9]` |
| `altitude_band` *(proposed v2)* | session/context | informational only — λ math is altitude-invariant `[v2: q9]` |
| `confidence` | `vin_dna.confidence` | gates limited-scope fallback (→ GASWIKI-10) |

Code-side type lives in `COMLab/comlab/schemas/lab_dna_views.py`. The two proposed v2 fields (`fuel_type`, `altitude_band`) are context-only — see GASWIKI-02 §2.8 for why neither relaxes any gate.

## 1.5 DNA-gated ingestion model {#CONCEPT_DNA_GATED_INGESTION}

**Principle.** The UI is responsible for constraining technician input to physically plausible ranges for the specific vehicle. When DNALab decodes the VIN + triage it emits a `ui_input_bounds` block (one entry per editable field) that the UI uses to bound numeric inputs, reject out-of-range entries inline, and never let raw out-of-range values reach GASLab.

**Consequence for GASLab.** GASLab does **not** maintain its own per-vehicle physical-bound table. It assumes incoming readings sit within the analyser measurement envelope (HC 0–20 000 ppm, CO 0–15 %, CO₂ 0–22 %, O₂ 0–22 %, NOₓ 0–5 000 ppm). What GASLab still owns:

- **chemistry-level validity gates** — the Exhaust Gas Triangle and dilution screen (→ GATE_TRIANGLE, GATE_DILUTION in GASWIKI-04). These are physics, not vehicle-specific.
- **internal sanity rails** — values that pass the UI bound but are chemically impossible (e.g. CO > 12 % at idle with valid CO₂) raise `SAMPLE_INVALID`.

**What it replaces.** The old static `physical_sensor_bounds.json` pattern (no DNA awareness) is gone; the blindspot it caused (e.g. RPM allowed 0–8000 regardless of redline) is resolved at the UI before any value reaches GASLab.

**Tradeoff.** The UI must call DNALab synchronously before the technician types a gas reading. If DNALab fails or returns `confidence = NONE`, inputs cannot be bounded precisely — see GASWIKI-10 for the limited-scope behaviour that follows.

## Graph relations (explicit)

**GASLab** ROUTES_TO **COMLab** aggregator
**GASLab.process()** EMITS **GasLabPayload**
**GasLabPayload** CONSUMED_BY **COMLab.comlab.schemas.ingestion**
**GasLabDnaView** CONSUMED_BY **gaslab.dna_view.GasLabDnaView**
**GasLabDnaView** PROJECTED_FROM **DNALab.VehicleDNA**
**CONCEPT_GASLAB_INPUTS** ENUMERATES **HC**, **CO**, **CO₂**, **O₂**, **NOₓ**, **engine_state_bucket**, **GasLabDnaView**
**engine_state_bucket** GATED_BY **STABILIZED_IDLE**, **REGULATORY_HIGH_IDLE**, **STRESS_IDLE**
**CONCEPT_DNA_GATED_INGESTION** REPLACES **physical_sensor_bounds.json**
**ui_input_bounds** CONSUMED_BY **UI input validation** (not GASLab)
**GATE_TRIANGLE** VALIDATES **sample_validity** at chemistry level
**GATE_DILUTION** VALIDATES **sample_validity** at chemistry level
**target_lambda_v112** CONSUMED_BY **brettschneider** mixture evaluation
**co_low_idle**, **co_high_idle** CONSUMED_BY **per-vehicle CoC threshold tables**
**fuel_type** (proposed v2) CARRIED_AS **context only** — CONSUMED_BY **COMLab.comlab.schemas.lab_dna_views**
**altitude_band** (proposed v2) CARRIED_AS **context only** — CONSUMED_BY **COMLab.comlab.schemas.lab_dna_views**
**confidence** GATED_BY **CONCEPT_SCOPE_SHRINKAGE** (GASWIKI-10)
**CONCEPT_ROLE** DESCRIBES **GASLab as 4DLab chemistry leaf**
**operating_envelope** GATED_BY **petrol 1990–2010**, **warm engine only**, **5-gas analyser required**
**GASLab** NEVER_IMPORTS **COMLab** (cross-lab import boundary)

## Core Entities

- **CONCEPT_ROLE** — GASLab position in 4DLab fan-in architecture: chemistry leaf, emits `GasLabPayload` to COMLab. Consumer: architecture spec.
- **CONCEPT_GASLAB_INPUTS** — five gas channels + `engine_state_bucket` + `GasLabDnaView`. Consumer: `gaslab/process()` entry point.
- **CONCEPT_GASLABPAYLOAD** — JSON contract surface: `chemical_state`, five gases, `lambda_chem`, `lambda_measured`, `sample_validity`. Consumer: `gaslab.contracts.GasLabPayload`.
- **CONCEPT_GASLABDNAVIEW** — slim DNA projection (14 fields from `VehicleDNA`). Consumer: `gaslab.dna_view.GasLabDnaView`.
- **CONCEPT_DNA_GATED_INGESTION** — UI enforces per-vehicle input bounds before GASLab sees any value. Consumer: UI layer (not GASLab code).
