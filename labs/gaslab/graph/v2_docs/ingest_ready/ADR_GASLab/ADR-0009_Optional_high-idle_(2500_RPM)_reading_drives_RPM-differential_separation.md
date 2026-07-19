
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0009: Optional high-idle (2500 RPM) reading drives RPM-differential separation · Parent document: ADR_GASLab.md
## ADR-0009: Optional high-idle (2500 RPM) reading drives RPM-differential separation

**Status:** Accepted

**Context.** Several faults are indistinguishable from a single idle reading — cam timing vs vacuum lean, weak vs dead catalyst, and the mechanical-wear leaves all overlap at idle. The discriminating information is *how the chemistry changes between idle and ~2500 RPM*.

**Decision.** `GasLabContext` accepts an **optional** second reading at 2500 RPM (`reading_high`). When present it unlocks the RPM-differential discriminators in `resolution.apply_differentiators` (normalise / persist / NOx-rise patterns, catalyst dual-idle, mechanical-wear leaf routing). All fault bound-matching stays scoped to `operating_state: STABILIZED_IDLE`; the high-idle reading is a *discriminator input*, not a new operating-state bucket. When `reading_high` is absent the engine still classifies on the idle reading alone.

**Consequences.**
- Positive: resolves overlapping idle signatures using behaviour over RPM, the physically correct discriminator.
- Positive: backwards-compatible — single-reading callers keep working; the new branches are additive.
- Negative: the strongest separations require the technician to take a second reading; without it some pairs stay ambiguous.
- Neutral: the engine carries both single- and dual-reading code paths.

**Alternatives considered.**
1. *Promote `REGULATORY_HIGH_IDLE`/`STRESS_IDLE` to first-class operating states with their own fault tables.* Deferred to v2 — larger ontology change; the discriminator approach delivers the separation now without duplicating fault tables.
2. *Require two readings always.* Rejected — breaks single-reading callers and the common quick-check workflow.

**References.** `HLD_GASLab §6`; `LLD_GASLab §6`; `process.py` (`GasLabContext.reading_high`).

---


## Graph relations (explicit)

**ADR-0009: Optional high-idle (2500 RPM) reading drives RPM-differential separation** DESCRIBES **GASLab ADR v2.1**
**GasLabContext.reading_high** CONSUMES **resolution.apply_differentiators()** -- unlocks RPM-differential discriminators


