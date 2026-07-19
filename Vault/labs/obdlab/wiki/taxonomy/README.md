---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "emission-era-taxonomy"
implements:
  - "labs/obdlab/code/schemas/dna_view.py"
consumers:
  - "comlab: labs/comlab/comlab/core/symptom_router.py — era/emission symptom-prior routing"
  - "comlab: labs/comlab/comlab/core/fault_atlas_kg.py"
drift_guards:
  - "labs/obdlab/tests/unit/test_dna_view.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/taxonomy/README.md"
---
# chunks/taxonomy/ — index & disposition ledger


**Date:** 2026-06-07 · **Step:** Phase 2 chunking — pack populated from the
`sources/various/` volume sweep (was empty per SWEEP_MANIFEST §10). Topic = fault
classification backbone: Euro emission eras + era/make fault priors. Pairs with the
J2012 P-code family doc at `sources/taxonomy/faultatlas.md` (not yet chunked separately).

## Chunk set

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `01_euro-emission-standards-eras` | Euro 1–6 eras gate which sensors/aftertreatment/faults exist | DNALab tier resolution → fault_atlas era gating | PROPOSAL |
| `02_era-fault-case-catalogue` | era/make known-failure priors (Vol4/6/8) | fault_atlas make/era prior layer | PROPOSAL |

## Source disposition
`Vol6.md` → 01 (Euro standards + eras) + 02 (Era 1–3 case lists). `Vol4.md` → 02 (30
era/make cases; also feeds pids-protocol/01). `Vol8.md` → 02 (comparative misfire/DTC).
Gate: prose/case tables readable; some Vol6 g/km standard cells image-stripped (logged
in formula-wiki pending list, not reconstructed).

## Still open
`sources/taxonomy/faultatlas.md` + `faultlist.md` (J2012 8-family P-code backbone) not
yet chunked here — prior-pass item, independent of the volume sweep.


## Core Entities

- taxonomy (Euro eras + era/make priors)
- Euro_Era_1, Euro_Era_2, Euro_Era_3, J2012 families
- DNALab tier resolution -> fault_atlas era gating + prior layer

## Graph relations (explicit)

**taxonomy** GATES **fault_atlas** by Euro era and make/era priors

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
