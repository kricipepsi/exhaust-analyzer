# ADR-0003: Signal/noise — every schema field needs a named, existing consumer

**Status:** Accepted

**Context.** As a fusion point, COMLab's schemas attract "might be useful later"
fields from every producer. Each unused field is a liability: it must be
populated, validated, kept in sync across the JSON boundary, and reasoned about,
while delivering nothing. With ten cross-lab dependencies in flight (DEP-1…DEP-10)
the accretion risk is high.

**Decision.** Every field on any COMLab schema (`ingestion.py`, `response.py`,
`lab_dna_views.py`, `kg.py`) must have a **named consumer** in a live code path,
and the field's comment names it (the codebase does this literally — e.g.
`control_module_voltage_v … # consumer: perception_contradiction.detect`,
`ff_fuel_spark_cut_at_crank … # consumer: fault_atlas_router no-start branch`).
"Future use" is not a consumer. A field and its reader may ship in the same
change, but the reader must be real. **A new improvement defaults to a proposal
that ships its consumer in the same change** — "not in v1" is not by itself a
reason to defer.

**Consequences.**
- Positive: the contract surface stays minimal and every field is grep-traceable
  to a reader (the anti-orphan check: at stage close every emitted field must be
  grep-confirmed read by its named fusion consumer — green tests alone are not
  "done").
- Positive: review has an objective gate — find the consumer or reject.
- Negative: genuinely forward-looking schema work must be staged as a proposal
  with a specced consumer, not merged speculatively (`config/proposals/`).
- Neutral: drove the removal of fields whose only "consumer" was documentation
  (e.g. KG `wiki_refs`, static `severity`).

**Alternatives considered.**
1. *Reserved fields for forward compatibility.* Rejected — exactly the accretion
   failure mode; reserved fields are never cleaned up.
2. *Gate only the outbound payload, not the inbound mirrors.* Rejected — mirror
   and view fields carry the same cross-boundary sync cost.

**References.** `CROSS_LAB_DEPENDENCIES.md` (anti-orphan gate); `wiki/08_scoring_to_fusion_rework.md`;
project `CLAUDE.md` signal/noise rule; field-level `# consumer:` comments throughout
`comlab/schemas/ingestion.py`.
