> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0006: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0006: Auto-stamp session identity

**Status:** Accepted (models API)

### Context

COMLab's orchestrator correlates the DNA prior with the rest of the pipeline by session.
Requiring callers to supply a session id and timestamp invites omission and format drift.

### Decision

`VehicleDNA.new` auto-generates `session_id = DNA_TX_<10 hex upper>` and an ISO-8601 UTC
`timestamp` when not supplied, while still accepting caller-supplied values for testing
and replay.

### Consequences

- **Positive:** every payload is correlatable and consistently formatted with no caller
  effort.
- **Neutral:** the id is a UUID4 slice (10 hex) — collision-safe for session scope, not a
  cryptographic guarantee.

### Alternatives Considered

1. **Require callers to supply identity.** Rejected: invites omission/format drift.
2. **Full UUID string.** Rejected: the 10-hex `DNA_TX_` form is human-legible and
   sufficient for session correlation.

---

## Graph relations (explicit)

**ADR-0006** DESCRIBES **auto-stamp session identity** (DNA_TX_ + UTC timestamp)
**VehicleDNA.new()** CONSUMES **uuid4 + datetime.now(timezone.utc)** (auto-generation)
**session_id** DESCRIBES **DNA_TX_<10 hex upper>** (collision-safe for session scope)
**timestamp** DESCRIBES **ISO-8601 UTC YYYY-MM-DDTHH:MM:SSZ**
**ADR-0006** VERIFIES **correlatable payload with no caller effort** (test_assembly.py)
