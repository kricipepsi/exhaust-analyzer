---
chunk_id: COMWIKI-01
title: Role, Boundaries & the Fusion Spine
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: COMLab is the only module that consumes all four lab channels and emits a
  verdict; the isolation invariants that keep it a fusion spine, not a re-implementation
  of the emitters.
entities_defined:
- CONCEPT_FUSION_SPINE
- CONCEPT_ISOLATION
- CONCEPT_CHANNELS
- CONCEPT_EMIT_BOUNDARY
related_chunks:
- COMWIKI-02
- COMWIKI-03
- COMWIKI-07
- COMWIKI-08
sources:
- COMLab_HLD.md §3–§4
- AGENTS.md
- README.md
- REWORK_PLAN_COMLab.md §1
node_type: wiki
lab: comlab
module: comlab
subsystem: fusion-spine
implements:
- labs/comlab/comlab/core/fault_atlas_router.py
- labs/comlab/comlab/schemas/ingestion.py
consumers:
- 'comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py .process fusion-spine
  orchestration'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py family-map verdict'
- 'wired (pending T-WIRE-1): apps/wired/wired/composition.py LabPipelineAggregator
  import'
drift_guards:
- labs/comlab/tests/unit/test_fault_atlas_router.py
- labs/comlab/tests/unit/test_lab_pipeline_aggregator.py
tags:
- comlab
- fusion-spine
- wiki
source: labs/comlab/wiki/01_role_boundaries_fusion_spine.md
---

# Role, Boundaries & the Fusion Spine

## COMLab is the decision spine {#CONCEPT_FUSION_SPINE}

COMLab is the **prune→rank→fuse** module: the only part of 4DLab that reads every upstream
channel and turns them into one diagnostic output. Each emitter lab produces a single validated
payload over a JSON boundary:

- **GASLab** → `GasLabPayload` — tailpipe 5-gas chemistry collapsed to one `chemical_state`.
- **OBDLab** → `OBDLiveDataPayload` — live-PID trims, VE, lambda perception, sensor health.
- **DTCLab** → `DTCLabPayload` — confirmed/pending/permanent DTCs, freeze frame, Mode `$06`.
- **DNALab/VINLab** → `VehicleDNA` (+ top-level `SymptomDNA`) — hardware architecture + symptom.

COMLab consumes those four channels (`→ CONCEPT_CHANNELS`), prunes the candidate fault set by
era and hardware, scores the survivors, **fuses** the channels into a calibrated verdict, and
emits a ranked differential to the UI. The full operational walk is `COMWIKI-07`; the reworked
fusion stage is `COMWIKI-08`.

## The emit boundary: emitters emit channels, COMLab fuses verdicts {#CONCEPT_EMIT_BOUNDARY}

The single most load-bearing boundary in 4DLab: **emitter labs emit signals/channels, never
cross-lab fault verdicts.** GASLab says "the chemistry is `LEAN_MIXTURE`"; OBDLab says "trim is
+18 % and the O₂ sensor looks lazy"; DTCLab says "P0171 is confirmed." None of them says
"vacuum leak." The **fault verdict is COMLab fusion** — it is the only place a cross-domain
conclusion is allowed to form.

This is why, e.g., the `ecu_fault` decision (does the ECU's perception contradict gas reality?)
is a **COMLab** consumer (`T-COMV2-ECU-FUSE-1`) that reads OBD's `lambda_perception_delta` and
GAS's `lambda_chem` — OBDLab and GASLab each emit a *half*, COMLab judges (`COMWIKI-08`,
`COMWIKI-13`).

## Data-isolation invariant {#CONCEPT_ISOLATION}

COMLab mirrors the types it needs from each lab **locally**; it does **not** import emitter
packages. The JSON payloads are the only contact surface.

- **No cross-lab Python imports.** `comlab/` never does `from gaslab import …`. The contract
  types are re-declared as local mirrors (`schemas/ingestion.py`). This keeps the labs
  independently buildable and is the reason the emitter halves could ship at earlier stages
  while their COMLab consumers stayed "divergent until Stage 4" (`tasks/PROGRESS.md`).
- **COMLab does not recompute emitter math.** It does not compute lambda from raw gases
  (GASLab's Brettschneider), does not derive a DTC routing tag from a raw code (DTCLab), and
  does not re-derive the horizon from the VIN string (DNALab — forbidden per HLD §3). It reads
  the *resolved* tokens and fuses them.
- **One verdict surface.** The reworked fusion stage (`COMWIKI-08`) is the single place the
  cross-domain conclusion forms; analytics (`COMWIKI`-Stage D) only quantify severity of an
  already-decided verdict.

If a task tempts the coder to compute a lambda, a CO threshold, a DTC tag, or a horizon inside
COMLab, the task is wrong-module — surface and stop.

## The four channels at a glance {#CONCEPT_CHANNELS}

| Channel | Payload | Primary signal | Failure-to-supply behaviour |
|---|---|---|---|
| GAS | `GasLabPayload` | `chemical_state` (primary route key) | suppressed on `will_not_start`; else Stage-A abort if sample invalid |
| OBD | `OBDLiveDataPayload` | `total_trim_correction_delta`, VE, lambda perception | suppressed on `cranking`/`will_not_start` → `degradation_mode = GAS_DOMINANT` |
| DTC | `DTCLabPayload` | confirmed DTCs + routing tags; freeze frame | starved on this corpus (64/90 OUTRANKED have no DTC — `COMWIKI-08`) |
| DNA | `VehicleDNA` + `SymptomDNA` | horizon + hardware flags; symptom prior | `confidence == NONE` → Stage-A abort |

The field-by-field inventory of each channel is `COMWIKI-02`. How DNA prunes the candidate set
before any scoring is `COMWIKI-03`/`COMWIKI-04`.

## Build position

COMLab is **Stage 4, reworked last** (`ROADMAP.md`). Its `tasks/PROGRESS.md` rows are mostly
**forward-registered consumers** of emitter halves already shipped by GASLab (S1), OBDLab (S2),
and DTCLab (S3). Registering them keeps those emitted fields un-loseable and satisfies the
anti-orphan gate (every emitted field must be grep-confirmed read by its named fusion consumer
at Stage-4 close). Those consumers are enumerated in `COMWIKI-08` and `COMWIKI-13`.

## Graph relations (explicit)

**COMLab** CONSUMES **GASLabPayload, OBDLiveDataPayload, DTCLabPayload, VehicleDNA**
**COMLab** EMITS **OrchestratorFinalUIOutput** (ranked differential verdict)
**Emitter labs** EMIT_CHANNELS_NOT **fault verdicts**
**COMLab** MIRRORS_LOCALLY **emitter contract types** (no cross-lab import)
**CONCEPT_FUSION_SPINE** REALISED_BY **COMWIKI-07 pipeline + COMWIKI-08 fusion stage**

## Core Entities

- **CONCEPT_FUSION_SPINE** — COMLab as the prune→rank→fuse module, the sole cross-domain fault verdict engine. Consumer: `comlab/core/fault_atlas_router.py (via family map)`.
- **CONCEPT_ISOLATION** — The data-isolation invariant prohibiting cross-lab Python imports and keeping emitter packages independent. Consumer: `comlab/schemas/ingestion.py`.
- **CONCEPT_CHANNELS** — The four input channels (GAS, OBD, DTC, DNA) consumed over stable JSON boundaries. Consumer: `comlab/schemas/ingestion.py (OrchestratorInboundRequest)`.
- **CONCEPT_EMIT_BOUNDARY** — The boundary separating signals emitted by upstream labs from fusion verdicts formed in COMLab. Consumer: `comlab/core/fault_atlas_router.py`.
