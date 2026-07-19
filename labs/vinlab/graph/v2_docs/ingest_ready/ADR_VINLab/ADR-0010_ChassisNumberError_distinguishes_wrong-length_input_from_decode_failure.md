> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0010: ChassisNumberError distinguishes wrong-length input from decode failure | Parent document: ADR_VINLab.md

## ADR-0010: `ChassisNumberError` distinguishes wrong-length input from decode failure

**Status:** Accepted (decoder API)

### Context

Pre-standardisation vehicles use chassis/frame numbers that are not 17 characters.
Treating these as ordinary decode failures conflates "this isn't a VIN" with "this VIN
won't decode".

### Decision

A non-17-character input raises `ChassisNumberError`, a subclass of `VINDecodeError`.
Callers can catch the subclass to route legacy identifiers to a separate pipeline;
catching `VINDecodeError` still catches both.

### Consequences

- **Positive:** callers separate "not a VIN" from "bad VIN" without string-matching
  messages.
- **Neutral:** one extra exception type in the public surface.

### Alternatives Considered

1. **One generic `VINDecodeError` for everything.** Rejected: loses the routing
   distinction.
2. **Return a sentinel instead of raising.** Rejected: inconsistent with the rest of
   the validation path, which raises.

---

## Graph relations (explicit)

**ADR-0010: ChassisNumberError distinguishes wrong-length input from decode failure** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.decoder.ChassisNumberError** IMPLEMENTS **ADR-0010**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **vinlab.decoder.ChassisNumberError**
