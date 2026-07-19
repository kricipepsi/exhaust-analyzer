> **Context:** DNALab PRD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: Section · Parent document: PRD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## Section 6 — Value Proposition

- **Jobs addressed:** producer orchestration, session stamping, schema versioning, JSON
  round-trip.
- **Gains created:** one `build_vehicle_dna()` call; fail-fast on incomplete triage
  before the (heavier) VIN decode; a self-describing versioned envelope.
- **Pains relieved:** no composition logic duplicated in the UI or COMLab; serialization
  is delegated to each model, so field changes in VINLab/SymptomLab don't require DNALab
  edits (only a version bump when the shape changes).
- **Competitive advantage:** the umbrella stays thin and deterministic; the contract
  surface (`§4.3`) is exactly five top-level keys, and the version field lets COMLab
  distinguish payload generations cleanly.

---

## Graph relations (explicit)

**build_vehicle_dna()** DESCRIBES **one call → complete, versioned prior**
**VehicleDNA.from_json_payload()** DESCRIBES **self-describing versioned envelope**
**dnalab** DESCRIBES **five top-level keys (§4.3) + thin deterministic umbrella**
