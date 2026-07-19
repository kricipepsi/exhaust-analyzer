> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0005: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0005: Validate triage-key presence before the VIN decode

**Status:** Accepted (assembly API)

### Context

`build_vehicle_dna` does two pieces of work: a (heavier) VIN decode and a symptom
resolve. If the triage dict is incomplete, doing the decode first wastes work and reports
the wrong failure.

### Decision

Check the four required triage keys (`tier_1`, `tier_2`, `occurs_during`, `engine_state`)
**first**; raise `SymptomValidationError` immediately if any is missing, before calling
`vinlab.decode`.

### Consequences

- **Positive:** fail-fast on the cheap check; the error names the real problem (missing
  triage), not a downstream symptom.
- **Neutral:** the VIN is only decoded once the triage is structurally complete.

### Alternatives Considered

1. **Decode first, validate triage later.** Rejected: wastes the decode and obscures the
   real failure.
2. **Let `symptomlab.resolve` raise on the missing kwargs.** Rejected: the explicit
   pre-check gives a single, clear `build_vehicle_dna`-level error.

---

## Graph relations (explicit)

**ADR-0005** DESCRIBES **validate triage-key presence before VIN decode**
**build_vehicle_dna()** GATED_BY **triage pre-check** (before vinlab.decode)
**SymptomValidationError** GATED_BY **missing triage key** (fail-fast)
**ADR-0005** VERIFIES **cheap check first, heavy decode only if triage complete** (test_assembly.py)
