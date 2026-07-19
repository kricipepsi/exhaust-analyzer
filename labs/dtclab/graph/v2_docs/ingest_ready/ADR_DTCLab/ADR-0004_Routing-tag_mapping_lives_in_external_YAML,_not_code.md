
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0004: Routing-tag mapping lives in external YAML, not code · Parent document: ADR_DTCLab.md
## ADR-0004: Routing-tag mapping lives in external YAML, not code

**Status:** Accepted

**Context.** The DTC-range → routing-tag relation is large (32 entries), churns as coverage grows,
and must be auditable against the wiki (`DTC_VOCABULARY.md §15`).

**Decision.** Mappings live in `dtclab/config/routing_tag_map.yaml`, each entry carrying
`patterns`, `tag`, `source_wiki` provenance, and optional `dna_gate`. `RoutingTagMapper` compiles
them at construction. Adding coverage is a data edit with a citation, not a code change.

**Consequences.**
- (+) Coverage changes are reviewable as data diffs with provenance; no recompile of logic.
- (+) The same YAML feeds both the mapper and the Phase-2 scorer's rule set.
- (−) A malformed YAML surfaces only at load time (`FileNotFoundError` / parse error at import) —
  accepted as fail-at-startup over fail-at-runtime.

**Alternatives considered.** (1) Hard-coded `if/elif` ladder — rejected: unreviewable, no
provenance. (2) A database — rejected: over-engineered for a static, version-controlled table.

---


## Graph relations (explicit)

**ADR-0004** DESCRIBES **DTCLab ADR v1.0**
**routing_tag_map.yaml** IMPLEMENTS **ADR-0004** -- mapping in YAML
