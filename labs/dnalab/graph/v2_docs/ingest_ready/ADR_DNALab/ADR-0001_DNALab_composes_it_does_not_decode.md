> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0001: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0001: DNALab composes; it does not decode, validate, or route

**Status:** Accepted (architecture; `docs/adr/0002-dnalab-only-importer.md`)

### Context

The DNA prior has two halves — physical identity and operator symptom — produced by two
independent labs. Something must join them under the §4.3 contract. That joiner could
also try to decode, validate, or route, but each of those is another lab's job.

### Decision

DNALab is a **thin composer**: it calls `vinlab.decode` and `symptomlab.resolve`, stamps
session metadata, and packages `VehicleDNA`. It owns no decode logic, no symptom catalog,
no routing. Correctness of each half is the producer's responsibility.

### Consequences

- **Positive:** the umbrella stays small, deterministic, and easy to reason about; one
  place knows how to compose, nowhere else.
- **Positive:** producer changes don't ripple into DNALab beyond a version bump.
- **Negative:** DNALab depends on both producers being import-clean and API-stable.

### Alternatives Considered

1. **Compose in COMLab or the UI.** Rejected: scatters composition and the version
   contract across consumers.
2. **A fat umbrella that also validates/routes.** Rejected: duplicates VINLab/SymptomLab/
   COMLab responsibilities.

---

## Graph relations (explicit)

**ADR-0001** DESCRIBES **DNALab as thin composer** (not decoder, validator, or router)
**build_vehicle_dna()** CONSUMES **vinlab.decode() + symptomlab.resolve()** (composition only)
**dnalab** VERIFIES **owns no decode logic, no symptom catalog, no routing**
**ADR-0001** SUPERSEDES **any fat-umbrella design** (rejected alternatives)
