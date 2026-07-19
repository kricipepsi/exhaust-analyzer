> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0003: No cross-lab Python imports — COMLab mirrors VinDNA | Parent document: ADR_VINLab.md

## ADR-0003: No cross-lab Python imports — COMLab mirrors `VinDNA`

**Status:** Accepted (architecture constraint)

### Context

The 4D architecture keeps each lab a fully isolated codebase connected only through
typed JSON boundaries. COMLab, OBDLab, DTCLab, and GASLab all need data that originates
in `VinDNA`.

### Decision

VINLab **never imports** from another lab, and no other lab imports VINLab — except
`dnalab`, which imports `vinlab` (the one allowed in-family direction). COMLab mirrors
`VinDNA`'s types locally and projects them into per-lab DNA views.

### Consequences

- **Positive:** no import cycles; labs version independently.
- **Negative:** mirrored types can drift from `VinDNA` (e.g. the `UpstreamO2Type`
  member-name divergence reconciled by COMLab-D; the CoC/emissions nesting drift, whose
  VINLab-side shape is now formalized by T-DNA-4 with the projector path fix paired as
  COMLab-C). Sync is a documented manual responsibility.

### Alternatives Considered

1. **Shared `common` enum package.** Rejected: reintroduces the coupling isolation
   exists to remove.
2. **Direct import of COMLab projector types.** Rejected: violates the boundary.

---

## Graph relations (explicit)

**ADR-0003: No cross-lab Python imports — COMLab mirrors VinDNA** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**comlab.projection.project** IMPLEMENTS **ADR-0003**
**labs/comlab/tests/unit/test_projection.py** VERIFIES **comlab.projection.project**
