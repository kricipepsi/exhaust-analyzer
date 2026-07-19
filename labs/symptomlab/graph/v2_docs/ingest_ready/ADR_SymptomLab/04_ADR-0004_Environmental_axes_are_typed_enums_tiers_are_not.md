> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0004: Environmental axes are typed enums; tiers are not · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0004: Environmental axes are typed enums; tiers are not

**Status:** Accepted (contract §4.2 / §8)

### Context

`occurs_during`, `engine_state`, and `load_state` are a small, closed, contract-fixed
vocabulary the diagnostic engine branches on directly. The tier vocabulary, by contrast,
is open and growing (ADR-0002).

### Decision

Model the environmental axes as `StrEnum`s (`OccursDuring`, `EngineState`, `LoadState`)
so an out-of-vocabulary value fails at the boundary; keep the tiers as YAML-validated
`str`.

### Consequences

- **Positive:** invalid environmental context is rejected immediately and precisely.
- **Neutral:** two different validation mechanisms in one lab (enum coercion for
  environment, set membership for tiers) — each matched to its vocabulary's nature.

### Alternatives Considered

1. **All strings, all YAML-validated.** Rejected: loses compile-time/type clarity for a
   genuinely fixed set.
2. **All enums.** Rejected: re-couples the open tier vocabulary to code.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**OccursDuring, EngineState, LoadState** GATED_BY **closed StrEnum vocabulary** (contract-fixed)
**tier_1, tier_2** GATED_BY **open YAML vocabulary** (not enum)
