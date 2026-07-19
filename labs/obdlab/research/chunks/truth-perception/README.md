---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "truth-vs-perception"
implements:
  - "labs/obdlab/obdlab/core/sensor_signal_translator.py"
consumers:
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py — truth-vs-perception override core"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py RULE_SYMPTOM_PRIOR (capped 0.65)"
drift_guards:
  - "labs/obdlab/tests/unit/test_sensor_signal_translator.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/truth-perception/README.md"
---
# chunks/truth-perception/ — index & disposition ledger


**Date:** 2026-06-07 · **Step:** Phase 2 chunking, NEW topic pack created from the
`sources/various/` volume sweep (Vol1 primary). Topic = the L1–L5 truth-vs-perception
paradigm: λ_obd (ECU perception) vs λ_chem (gas truth) and the discrepancy logic.

## Why a new pack
Vol1 is explicitly the 5-tier truth-vs-perception case library. It extends — does not
duplicate — `o2-logic/05_bias-vs-real-truth-perception` (O₂-only) and is distinct from
the fuel-trim case matrix (trim cases) and ecu-diagnosis (ECU hardware modes).

## Chunk set

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `01_five-tier-l1-l5-architecture` | L1–L5 framing; L3 = perception_contradiction | COMLab perception_contradiction (method) | active framing |
| `02_lambda-delta-vector-and-scoring` | Δλ = λ_obd−λ_chem; L5 trust/consistency scores | perception_contradiction + proposed L5 scorer | MIXED (Δλ active, scores PROPOSAL) |
| `03_thirty-case-liar-library` | N-001..N-030 discrepancy cases | fault_atlas pattern set + test corpus | PROPOSAL (library) |
| `04_combustion-integrity-oxygen-usage` | CO2/(CO2+CO), O2/CO misfire-vs-rich | GASLab resolver → fault_atlas | PROPOSAL |

## Source disposition
`Vol1.md` — fully chunked into 01–04. Gate note: prose readable; inline λ/subscript
symbols stripped in export — **numbers recovered from the intact case tables**, which
survived. No formula fabricated; ratio forms flagged in the formula wiki pending list.

## Forward-progress proposals raised
L5 prognostic scoring fields (Perception_Reliability_Index, ECU_Consistency_Score,
Thermal_State_Confidence) + the combustion-integrity ratios. Each names a consumer;
cross-referenced to proposals/extracted (EP-COM-03, EP-COM-05, EP-GAS-02).


## Core Entities

- truth-perception (L1-L5 paradigm)
- Lambda_Delta_Vector, perception_contradiction, fault_atlas_router
- COMLab perception_contradiction (L3) + proposed L5 scorer

## Graph relations (explicit)

**truth-perception** FRAMES the engine as L1-L5 with **lambda_chem** as ground truth
**L3** IS the live **perception_contradiction** override

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
