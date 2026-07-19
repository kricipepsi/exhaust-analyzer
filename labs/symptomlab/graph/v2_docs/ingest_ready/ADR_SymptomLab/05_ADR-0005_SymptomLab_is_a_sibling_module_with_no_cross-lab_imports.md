> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0005: SymptomLab is a sibling module with no cross-lab imports · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0005: SymptomLab is a sibling module with no cross-lab imports

**Status:** Accepted (2026-06-06 — T-RM-2-DNA)

### Context

In v1, SymptomLab lived inside `DNALab/SymptomLab/`. The v2 DNA family is three
independently-versioned codebases connected only through typed JSON.

### Decision

SymptomLab migrated to its own folder + `pyproject.toml`. `dnalab` imports `symptomlab`
(the one allowed in-family direction); SymptomLab imports no other lab. COMLab mirrors
`SymptomDNA` locally.

### Consequences

- **Positive:** independent build/test/version; explicit, auditable boundary.
- **Negative:** the `SymptomDNA` type is duplicated in COMLab's mirror — sync is a
  documented responsibility.

### Alternatives Considered

1. **Keep it nested in DNALab.** Rejected: couples versioning, blurs the boundary.
2. **Import COMLab's mirror type.** Rejected: violates isolation.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomLab** GATED_BY **zero cross-lab imports** (DNA-family boundary)
**COMLab** MIRRORS_CONTRACT_IN **SymptomDNA** (typed mirror, sync responsibility)
