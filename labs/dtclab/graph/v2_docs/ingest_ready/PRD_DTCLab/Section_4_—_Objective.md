
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 4 — Objective · Parent document: PRD_DTCLab.md
## Section 4 — Objective

**Business benefit.** Translate raw DTC lists into structured, confidence-weighted routing tags
and ranked fault-family candidates that COMLab can dispatch and fuse, reducing manual
DTC-to-fault mapping from minutes to milliseconds.

**Customer benefit.** Technicians receive a clear historical fault context, a Mode $06 margin
table that surfaces impending failures before a full DTC sets, and a ranked candidate list.

**Key Results:**

- **KR1:** `DataFusionSanitizer.sanitize()` returns a valid `DTCLabPayload` for all named
  regression fixtures with zero structural failures.
- **KR2:** Zero cross-lab Python imports (import-isolation audit in `test_dna_view.py`).
- **KR3:** All **5** DNA-gated routing entries suppress correctly on non-equipped vehicles
  (verified in `test_routing_tag_mapper.py` + integration tests).
- **KR4:** `POA_HISTORY` is never emitted by `RoutingTagMapper` — COMLab's responsibility (T-FX-3).
- **KR5:** `classify_top3()` returns ≤ 3 deduplicated `(family, confidence∈[0,1])` candidates,
  sorted `(-confidence, family)`, with no sum-1 normalisation (left to COMLab `combine()`).

---


## Graph relations (explicit)

**Section 4 — Objective** DESCRIBES **DTCLab PRD v2.0**
**DataFusionSanitizer.sanitize** VERIFIES **KR1** -- returns valid DTCLabPayload
**test_dna_view.py** VERIFIES **KR2** -- zero cross-lab imports
**test_routing_tag_mapper.py** VERIFIES **KR3** -- DNA-gated routing suppression
**COMLab** VERIFIES **KR4** -- POA_HISTORY injection contract T-FX-3
**ranking.classify_top3** VERIFIES **KR5** -- returns top-3 candidates
