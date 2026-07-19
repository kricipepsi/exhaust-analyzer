> **Context:** SymptomLab PRD v2.1 (2026-06-12) · Module: SymptomLab · Section 2 — Contacts · Parent document: PRD_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| SymptomLab Owner | Module Owner | Catalog curation, the 18-pair invariant, environmental enums, validation |
| COMLab Team | Integration Consumer | Mirrors `SymptomDNA`; routes tier_1/tier_2 to fault families in `fault_atlas_router` (the symptom prior); applies context modifiers; enforces the 65% trust ceiling |
| DNALab (assembly) | In-family Consumer | Calls `resolve()` with the triage dict; embeds `SymptomDNA` into `VehicleDNA` |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; "prior, not override"; open-vocabulary-via-YAML decision |

---
---

## Graph relations (explicit)

**PRD_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**COMLab Team** CONSUMES **SymptomDNA** (mirrors type; routes to fault_atlas_router)
**DNALab** CONSUMES **symptomlab.resolve** (in-family assembly)
