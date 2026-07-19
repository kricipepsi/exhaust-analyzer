> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 1 — Summary

DNALab is the **assembly** of the DNA family. It composes Part A (`VinDNA`, from VINLab)
and Part B (`SymptomDNA`, from SymptomLab) plus session metadata into one `VehicleDNA` —
the unified, contract-shaped payload COMLab ingests as its independent prior. The single
public entry point is `dnalab.build_vehicle_dna(vin, triage) → VehicleDNA`.

DNALab is the only lab in the DNA family that imports the others: the one allowed
in-family direction is `dnalab → vinlab + symptomlab`. It imports no COMLab. `VehicleDNA`'s
schema is governed by `SEMANTIC_CONTRACT.md §4.3`.

DNALab is a **composer, not a decoder and not a router.** It does not decode VINs (VINLab
does) or validate symptoms (SymptomLab does) or route faults (COMLab does). It orchestrates
the two producers, stamps session identity, and guarantees the combined payload
round-trips through JSON cleanly.

---

## Graph relations (explicit)

**dnalab.build_vehicle_dna()** DESCRIBES **the single public entry point**
**dnalab** DESCRIBES **composer, not decoder and not router**
**VehicleDNA** CONSUMED_BY **COMLab ingestion** (unified, contract-shaped payload)
**dnalab → vinlab + symptomlab** DESCRIBES **the only allowed in-family import direction**
