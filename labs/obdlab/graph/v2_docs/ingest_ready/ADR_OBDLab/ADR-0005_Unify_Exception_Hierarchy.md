> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0005: Unify exception hierarchy under ObdLabError · Parent document: ADR_OBDLab.md

## ADR-0005: Unify the exception hierarchy under `ObdLabError`

**Status:** Accepted (2026-06-08 — T-OBDV2-FIX-5)

### Context

OBDLab exceptions inherited from stdlib bases: `PIDValidationError(ValueError)`
and `SemanticConsistencyError(AssertionError)`. COMLab's fusion error-handling
path could not catch "any OBDLab error" without catching unrelated `ValueError`s,
and `AssertionError` is semantically wrong for a validation failure.

### Decision

Introduce a single root `ObdLabError(Exception)` and reparent both subclasses
under it. Physics Gate 4 now raises `SemanticConsistencyError` (consistent with
the other gates) rather than a bare `ValueError`.

### Consequences

- **Positive:** COMLab catches the whole family with one `except ObdLabError`.
- **Positive:** exception semantics match intent (no `AssertionError` for
  validation).
- **Negative:** any caller that previously caught `ValueError`/`AssertionError`
  from OBDLab must update to `ObdLabError` — a breaking change for downstream
  error handling (in-repo callers updated in the same task).

### Alternatives Considered

1. **Leave stdlib bases in place.** Rejected: forces broad, imprecise `except`
   clauses in COMLab.
2. **Multiple unrelated roots** (one per module). Rejected: defeats the
   single-`except` goal.

## Graph relations (explicit)

**ADR-0005** DESCRIBES **Unify exception hierarchy under ObdLabError**
**T-OBDV2-FIX-5** DESCRIBES **ADR-0005** (task that carried it)
**ObdLabError** SUPERSEDES **ValueError / AssertionError** (v1.0 stdlib bases reparented)
**PIDValidationError** DERIVED_FROM **ObdLabError**
**SemanticConsistencyError** DERIVED_FROM **ObdLabError**
**COMLab except ObdLabError** CONSUMES **ObdLabError hierarchy** (single catch)
