> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| DNALab Owner | Module Owner | `build_vehicle_dna` orchestration, `VehicleDNA` schema + versioning, JSON round-trip |
| VINLab Owner | In-family Producer | Supplies `VinDNA` (Part A) via `vinlab.decode()` |
| SymptomLab Owner | In-family Producer | Supplies `SymptomDNA` (Part B) via `symptomlab.resolve()` |
| COMLab Team | Integration Consumer | Ingests `VehicleDNA` as `OrchestratorInboundRequest.vehicle_dna`; mirrors the types |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; schema versioning; one-way in-family import boundary |

---

## Graph relations (explicit)

**DNALab Owner** DESCRIBES **build_vehicle_dna orchestration + VehicleDNA schema + versioning**
**VINLab Owner** DESCRIBES **VinDNA (Part A) via vinlab.decode()**
**SymptomLab Owner** DESCRIBES **SymptomDNA (Part B) via symptomlab.resolve()**
**COMLab Team** DESCRIBES **VehicleDNA ingestion as OrchestratorInboundRequest.vehicle_dna**
