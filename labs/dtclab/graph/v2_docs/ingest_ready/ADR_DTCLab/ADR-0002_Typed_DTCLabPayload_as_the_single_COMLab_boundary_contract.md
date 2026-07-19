
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0002: Typed DTCLabPayload as the single COMLab boundary contract · Parent document: ADR_DTCLab.md
## ADR-0002: Typed `DTCLabPayload` as the single COMLab boundary contract

**Status:** Accepted

**Context.** DTCLab produces several heterogeneous outputs (three DTC lists, routing tags, Mode $06
results, historical context, freeze frame, MIL state). COMLab needs one stable, validated contract.

**Decision.** All output is assembled into a single Pydantic model, `DTCLabPayload` (9 fields),
validated at the boundary. Field validators enforce the DTC regex (`ERR-CONTRACT-001`), routing-tag
membership (`ERR-CONTRACT-002`), and the Mode $06 MID-key pattern. COMLab consumes it at the
`dtc_lab_output` key of its inbound request (vocab §17).

**Consequences.**
- (+) One typed seam; malformed data fails at DTCLab's edge, not deep in COMLab.
- (+) Error codes give COMLab a deterministic failure contract.
- (−) Every new payload field needs a named COMLab consumer or it does not ship — intentional friction.

**Alternatives considered.** (1) Returning a tuple/dict of parts — rejected: no single validation
point, no typed contract. (2) Multiple return surfaces — rejected: multiplies the integration
contract COMLab must track.

---


## Graph relations (explicit)

**ADR-0002** DESCRIBES **DTCLab ADR v1.0**
**payload.DTCLabPayload** IMPLEMENTS **ADR-0002** -- single boundary contract
**test_payload.py** VERIFIES **ADR-0002**
