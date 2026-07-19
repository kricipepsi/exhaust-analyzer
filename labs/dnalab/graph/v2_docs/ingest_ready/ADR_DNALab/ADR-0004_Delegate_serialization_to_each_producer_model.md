> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0004: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0004: Delegate serialization to each producer model

**Status:** Accepted (`docs/adr/0003`/`0004`; models API)

### Context

`VehicleDNA` nests `VinDNA` and `SymptomDNA`. The umbrella could re-enumerate their
fields when serializing, but that would duplicate field knowledge and drift the moment a
producer changes.

### Decision

`to_json_payload` calls `vin_dna.to_json()` / `symptom_dna.to_json()`;
`from_json_payload` calls `VinDNA.from_json` / `SymptomDNA.from_json`. DNALab knows only
the five top-level keys; the inner shapes belong to the producers.

### Consequences

- **Positive:** no duplicated field knowledge; producer field changes need no DNALab edit
  (only a version bump when the shape changes).
- **Neutral:** round-trip correctness depends on each producer's `to_json`/`from_json`
  being inverses.

### Alternatives Considered

1. **Flatten everything in the umbrella.** Rejected: duplicates and drifts field
   knowledge.
2. **A shared serializer utility.** Rejected: re-couples the labs.

---

## Graph relations (explicit)

**ADR-0004** DESCRIBES **delegate serialization to each producer model**
**VehicleDNA.to_json_payload()** DELEGATES_TO **VinDNA.to_json()**
**VehicleDNA.to_json_payload()** DELEGATES_TO **SymptomDNA.to_json()**
**VehicleDNA.from_json_payload()** DELEGATES_TO **VinDNA.from_json() + SymptomDNA.from_json()**
**ADR-0004** VERIFIES **DNALab knows only the 5 top-level keys** (no inner field duplication)
