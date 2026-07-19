
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: Preamble · Parent document: ADR_DTCLab.md
# ADR — DTCLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-11
**Scope:** Architecture Decision Records for the DTCLab v2 module (`labs/dtclab/`)

Format: Nygard template (`_skills/doc/ADR.md`). Each record captures a decision that shipped in
the `dtclab/` package (AST ground truth, June 2026), its context, and its consequences. ADRs are
historical records; once accepted they are superseded, not edited. The signal/noise rule governs
every record: a field, tag, or enum value ships only with a named, existing consumer.

### ADR: ADR-0001
- **Title**: Strict lab isolation via a locally-mirrored DNA view
- **Status**: Accepted

### ADR: ADR-0002
- **Title**: Typed `DTCLabPayload` as the single COMLab boundary contract
- **Status**: Accepted

### ADR: ADR-0003
- **Title**: DNA gate as a *filter*, not a *requirement* (three-branch confidence)
- **Status**: Accepted

### ADR: ADR-0004
- **Title**: Routing-tag mapping in external YAML, not code
- **Status**: Accepted

### ADR: ADR-0005
- **Title**: `POA_HISTORY` injected by COMLab, never emitted by DTCLab
- **Status**: Accepted

### ADR: ADR-0006
- **Title**: Cross-field coolant/fluid signatures as a post-mapping step (5b)
- **Status**: Accepted

### ADR: ADR-0007
- **Title**: Phase-2 scorer reuses §16 weights — no new numeric literal, no normalisation
- **Status**: Accepted

### ADR: ADR-0008
- **Title**: Drop `SAI_HISTORY` / secondary-air from the routing surface
- **Status**: Accepted

### ADR: ADR-0009
- **Title**: Surface Mode $06 monitor-aborted / no-start state (`EP-DTC-NOSTART-1`)
- **Status**: Proposed

---


## Graph relations (explicit)

**ADR_DTCLab.md** DESCRIBES **DTCLab ADR v1.0**
