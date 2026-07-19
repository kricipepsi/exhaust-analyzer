
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0003: DNA gate as a *filter*, not a *requirement* (three-branch confidence) · Parent document: ADR_DTCLab.md
## ADR-0003: DNA gate as a *filter*, not a *requirement* (three-branch confidence)

**Status:** Accepted

**Context.** DNA-gated tags (`CATALYST_HISTORY`, `EGR_HISTORY`) should be suppressed
on vehicles that physically lack the hardware — but VIN decoding is not always confident, and a
missing/low-confidence VIN must not silently drop real DTC evidence.

**Decision.** The gate is keyed on `DtcLabDnaView.confidence` with three branches: `HIGH` →
strict hardware-presence check; `PARTIAL` → emit with a logged downgrade; `NONE` (or `dna_view is
None`) → emit unconditionally (pure DTC-pattern routing). The DNA gate filters false positives
*when it can be trusted* and otherwise yields to the DTC evidence.

**Consequences.**
- (+) No real fault is suppressed by an absent/weak VIN; false positives are removed only on HIGH.
- (+) Same pattern as GASLab/OBDLab — one mental model across labs.
- (−) On HIGH-but-wrong DNA, a real fault could be suppressed; mitigated by unknown-gate fail-open.

**Alternatives considered.** (1) Hard requirement (suppress unless hardware proven) — rejected:
drops evidence whenever VIN is missing. (2) No gating — rejected: floods COMLab with
hardware-impossible tags (e.g. catalyst codes on a pre-cat vehicle).

---


## Graph relations (explicit)

**ADR-0003** DESCRIBES **DTCLab ADR v1.0**
**routing_tag_mapper.RoutingTagMapper** IMPLEMENTS **ADR-0003** -- three-branch gate
**test_routing_tag_mapper.py** VERIFIES **ADR-0003**
