
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0006: Deterministic specificity ranking with catch-alls last · Parent document: ADR_GASLab.md
## ADR-0006: Deterministic specificity ranking with catch-alls last

**Status:** Accepted

**Context.** Multiple fault signatures can match one reading. The engine must pick exactly one verdict, and the same input must always yield the same output (frozen models, CI grids, reproducible diagnoses).

**Decision.** Surviving candidates are ordered by `_candidate_rank = (is_catch_all, signature_width)`: catch-all faults (`VVT_FAILURE`, `EVAP_CANISTER_SATURATED`, `POA_SIGNATURE`) sort last, then the **narrowest** total signature width wins (more specific = preferred). On an exact tie the winner is the first in ontology declaration order. `min()` over this key is deterministic across process restarts.

**Consequences.**
- Positive: a single, reproducible verdict; specific faults beat broad ones.
- Positive: ties resolve by a stable, declared order — no hidden nondeterminism.
- Negative: declaration order becomes semantically meaningful for tied faults, so the ontology order is part of the contract.
- Neutral: catch-alls remain reachable when nothing more specific matches.

**Alternatives considered.**
1. *Emit all matches and let COMLab choose.* Rejected — pushes the disambiguation cost across the boundary and breaks the "single chemical state" invariant.
2. *Score by a weighted prior.* Rejected — reintroduces a tuning surface; the project flags weight-nudging as a smell.

**References.** `LLD_GASLab §5`; `GAS_VOCABULARY §13` invariant 3; `rule_engine.py`.

---


## Graph relations (explicit)

**ADR-0006: Deterministic specificity ranking with catch-alls last** DESCRIBES **GASLab ADR v2.1**
**rule_engine._candidate_rank** GATED_BY **is_catch_all, specificity** -- deterministic tie-breaking


