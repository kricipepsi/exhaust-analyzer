> **Context:** DNALab HLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 1. · Parent document: HLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 1. Responsibility

DNALab is the **assembly** of the DNA family. It composes `VinDNA` (Part A, VINLab) and
`SymptomDNA` (Part B, SymptomLab) plus session metadata into one `VehicleDNA` — the
contract-shaped payload COMLab ingests. It is a **composer, not a decoder/validator/
router**: each producer owns its own correctness; DNALab orchestrates, stamps identity,
and guarantees the joined payload round-trips. `VehicleDNA`'s schema is governed by
`SEMANTIC_CONTRACT.md §4.3`.

DNALab is the **only** lab that imports siblings: `dnalab → vinlab + symptomlab` (the one
allowed in-family direction). It does not import COMLab; COMLab mirrors `VehicleDNA`.

---

## Graph relations (explicit)

**dnalab** DESCRIBES **DNA family assembly** (composer, not decoder/validator/router)
**dnalab.build_vehicle_dna()** CONSUMES **vinlab.decode()** (Part A, in-family import)
**dnalab.build_vehicle_dna()** CONSUMES **symptomlab.resolve()** (Part B, in-family import)
**VehicleDNA** OWNED_BY **DNALab**
**VehicleDNA** CONSUMED_BY **COMLab OrchestratorInboundRequest.vehicle_dna** (live mirror)
**dnalab → vinlab + symptomlab** DESCRIBES **the only allowed in-family import direction**
