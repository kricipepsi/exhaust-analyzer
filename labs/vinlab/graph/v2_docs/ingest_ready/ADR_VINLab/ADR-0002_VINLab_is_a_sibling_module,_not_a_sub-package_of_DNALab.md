> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0002: VINLab is a sibling module, not a sub-package of DNALab | Parent document: ADR_VINLab.md

## ADR-0002: VINLab is a sibling module, not a sub-package of DNALab

**Status:** Accepted (2026-06-06 — T-RM-2-DNA)

### Context

In v1, VINLab lived inside `DNALab/VINLab/`. The v2 architecture treats the DNA family
as three independently-versioned codebases (`vinlab`, `symptomlab`, `dnalab`) connected
only through typed JSON.

### Decision

VINLab migrated to its own top-level folder with its own `pyproject.toml`. `dnalab`
imports `vinlab` (one-directional, allowed within the family); VINLab imports no other
lab. v1 process history stays in `DNALab/VINLab/` for the Phase-5 archive.

### Consequences

- **Positive:** VINLab builds, tests, and versions on its own.
- **Positive:** the DNA-family import direction is explicit and auditable.
- **Negative:** shared types (e.g. enums) are duplicated as local copies until the
  Phase 0b `comlab.schemas.vocabulary` import swap.

### Alternatives Considered

1. **Keep VINLab nested in DNALab.** Rejected: couples versioning and blurs the
   producer/composer boundary.
2. **One mega-package for the whole DNA family.** Rejected: defeats lab isolation.

---

## Graph relations (explicit)

**ADR-0002: VINLab is a sibling module, not a sub-package of DNALab** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab package boundary** IMPLEMENTS **ADR-0002**
**labs/vinlab/tests/unit/test_standalone.py** VERIFIES **vinlab package boundary**
