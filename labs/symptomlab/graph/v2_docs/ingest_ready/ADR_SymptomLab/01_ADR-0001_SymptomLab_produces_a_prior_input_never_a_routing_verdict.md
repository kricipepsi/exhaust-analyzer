> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0001: SymptomLab produces a prior input, never a routing verdict · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0001: SymptomLab produces a prior input, never a routing verdict

**Status:** Accepted (architecture constraint; `DNALab_TO_COMLab_FLOW.md §4`)

### Context

The operator's symptom is a cheap, independent signal — but a self-reported symptom is
fallible (research bounds the misleading-report rate near 35%). If SymptomLab emitted
routing (suppress modes, target equation, a fault verdict), the symptom signal would
become an override of the physical evidence.

### Decision

`SymptomDNA` carries **only** the four contract §4.2 fields and **no** routing. All
routing — the symptom→family prior, mode suppression, the context modifiers — lives in
COMLab, where the signal is applied as a **prior** under a trust ceiling (COMLab-B, 65%).

### Consequences

- **Positive:** the symptom channel cannot override physical evidence; the
  truth-vs-perception discipline holds.
- **Positive:** SymptomLab stays a small, pure validator/packager.
- **Negative:** SymptomLab alone produces no diagnosis — its value is realised only when
  COMLab consumes it.

### Alternatives Considered

1. **Emit routing/suppression hints with the symptom.** Rejected: couples the lab to
   COMLab's job and risks the symptom becoming an override.
2. **Emit a tentative fault verdict.** Rejected: that is COMLab's verdict surface.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomDNA** GATED_BY **prior-only rule** (no routing fields, no verdict)
**COMLab** CONSUMES **SymptomDNA** as a prior under trust ceiling (65%, COMLab-B)
