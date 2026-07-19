
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0002: Signal/noise — every schema field needs a named, existing consumer · Parent document: ADR_GASLab.md
## ADR-0002: Signal/noise — every schema field needs a named, existing consumer

**Status:** Accepted

**Context.** Schemas accrete "might be useful later" fields. Each unused field is a maintenance and correctness liability: it must be populated, validated, kept in sync across the JSON boundary, and reasoned about, while delivering nothing.

**Decision.** Every field added to any GASLab schema (`GasLabPayload`, `GasLabDnaView`, `GasLabContext`) must have a **named consumer** in COMLab analytics or fault-atlas routing, plus the code path that reads it. "Future use" is not a consumer. The consumer may be added in the *same* change (a new field and the new reader ship together), but it must be named and real. If the consumer cannot be named, the field does not ship.

**Consequences.**
- Positive: the contract surface stays minimal and every field is traceable to a reader.
- Positive: review has an objective gate — grep for the consumer, or reject.
- Negative: genuinely forward-looking schema work must be staged as a proposal with a specced consumer, not merged speculatively.
- Neutral: drives an "anti-orphan" check before a task closes (a field read nowhere is a breach even with green tests).

**Alternatives considered.**
1. *Allow reserved fields for forward compatibility.* Rejected — this is exactly the accretion failure mode; reserved fields are never cleaned up.
2. *Gate only on the payload, not the inputs.* Rejected — DNA-view and context fields carry the same sync cost across the boundary.

**References.** Project `CLAUDE.md` "Signal/noise principle"; `GAS_VOCABULARY §12.2` (fields deliberately excluded).

---


## Graph relations (explicit)

**ADR-0002: Signal/noise — every schema field needs a named, existing consumer** DESCRIBES **GASLab ADR v2.1**
**GasLabPayload, GasLabDnaView, GasLabContext** GATED_BY **signal/noise rule** -- every field needs named COMLab consumer


