> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: Preamble · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

# Architecture Decision Records — DNALab (v2)

**Scope:** DNALab (umbrella composer of the DNA family).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-11; refreshed 2026-06-12 (schema bump landed, `SCHEMA_VERSION
= "1.2"`) — consolidates the lab-level decisions; granular records remain under
`docs/adr/` (0001–0004).

> These ADRs record decisions already implemented in `dnalab/`. Each captures *why*.
> Future changes supersede an ADR with a new one rather than editing it in place.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | DNALab composes; it does not decode, validate, or route | Accepted |
| ADR-0002 | DNALab is the only in-family importer (`dnalab → vinlab + symptomlab`) | Accepted |
| ADR-0003 | Versioned envelope with a hard mismatch guard | Accepted |
| ADR-0004 | Delegate serialization to each producer model | Accepted |
| ADR-0005 | Validate triage-key presence before the VIN decode | Accepted |
| ADR-0006 | Auto-stamp session identity (`DNA_TX_…` + UTC timestamp) | Accepted |
| ADR-0007 | One coordinating schema-bump task, run last (T-DNA-7) | Accepted |

---

## Graph relations (explicit)

**ADR_DNALab v2** DESCRIBES **7 architecture decisions for dnalab** (Nygard template)
**ADR_DNALab v2** CONSOLIDATES **lab-level decisions** (granular records at docs/adr/0001–0004)
**ADR_DNALab v2** MIRRORS_CONTRACT_IN **HLD_DNALab v2.1 + DLD_DNALab v2.1**
