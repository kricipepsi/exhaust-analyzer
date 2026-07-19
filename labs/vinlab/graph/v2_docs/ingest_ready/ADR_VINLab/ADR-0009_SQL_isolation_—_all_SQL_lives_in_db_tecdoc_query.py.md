> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0009: SQL isolation — all SQL lives in db/tecdoc_query.py | Parent document: ADR_VINLab.md

## ADR-0009: SQL isolation — all SQL lives in `db/tecdoc_query.py`

**Status:** Accepted (H8 constraint)

### Context

`vref.db` lookups need SQL, but SQL scattered across modules is hard to audit and to
keep read-only.

### Decision

Every SQL string lives in `db/tecdoc_query.py`. `lookup_engine_ref` opens `vref.db`
read-only via the SQLite `mode=ro` URI and returns rows as plain dicts. No other module
writes SQL (H8).

### Consequences

- **Positive:** one place to audit queries; read-only enforced at the connection.
- **Neutral:** the decoder depends on a thin query layer rather than touching SQLite
  directly.

### Alternatives Considered

1. **Inline SQL in the decoder.** Rejected: violates H8; harder to audit.
2. **An ORM.** Rejected: overkill for a single read query, and adds a dependency.

---

## Graph relations (explicit)

**ADR-0009: SQL isolation — all SQL lives in db/tecdoc_query.py** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.db.tecdoc_query.lookup_engine_ref** IMPLEMENTS **ADR-0009**
**labs/vinlab/tests/unit/test_build.py** VERIFIES **vinlab.db.tecdoc_query.lookup_engine_ref**
