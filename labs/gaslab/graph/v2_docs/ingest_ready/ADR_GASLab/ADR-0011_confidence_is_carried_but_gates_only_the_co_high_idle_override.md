
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0011: `confidence` is carried but gates only the `co_high_idle` override · Parent document: ADR_GASLab.md
## ADR-0011: `confidence` is carried but gates only the `co_high_idle` override

**Status:** Accepted

**Context.** `GasLabDnaView.confidence` (`HIGH` / `PARTIAL` / `NONE`) describes how trustworthy the DNA projection is. ADR-0005 rules out using it to weaken fault gates. The question remains whether it should be consumed anywhere in GASLab at all.

**Decision.** `confidence` is **carried and forwarded to COMLab** but has exactly one functional use inside GASLab: `_rich_co_ceiling` uses the per-vehicle `co_high_idle` as the rich-CO ceiling for the `CAM_TIMING_RETARDED_MAP` branch **only when `confidence == "HIGH"`**; otherwise the Euro-scaled default applies. There is no other branching on `confidence` in the canonical pipeline.

**Consequences.**
- Positive: a per-vehicle CoC limit is trusted only when the lookup is high-confidence; otherwise a safe class default is used.
- Positive: the field earns its place (it has a named reader) without becoming a broad heuristic.
- Negative: a subtle, easily overlooked coupling — documented here precisely so it is not mistaken for general confidence weighting.
- Neutral: COMLab may use `confidence` for its own purposes independently.

**Alternatives considered.**
1. *Ignore `confidence` entirely in GASLab.* Rejected — then `co_high_idle` would be trusted blindly even on a low-confidence lookup.
2. *Use `confidence` to weight all per-vehicle overrides.* Rejected — broadens into the heuristic ADR-0005 declines; one explicit gate is enough.

**References.** `LLD_GASLab §7, §9`; `DLD_GASLab §5`; `resolution._rich_co_ceiling`.

---


## Graph relations (explicit)

**ADR-0011: `confidence` is carried but gates only the `co_high_idle` override** DESCRIBES **GASLab ADR v2.1**
**GasLabDnaView.confidence** CONSUMES **resolution._rich_co_ceiling()** -- gates co_high_idle override; only GASLab consumer


