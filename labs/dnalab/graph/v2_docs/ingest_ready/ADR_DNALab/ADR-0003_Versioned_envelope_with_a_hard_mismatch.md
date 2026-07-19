> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0003: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0003: Versioned envelope with a hard mismatch guard

**Status:** Accepted (contract §4.3)

### Context

`VehicleDNA` will gain fields as the producers evolve (T-DNA-2/3/4/6). COMLab must be
able to tell a new-generation payload from a legacy one, and must never silently load a
payload whose shape it does not expect.

### Decision

`VehicleDNA` carries `schema_version` (currently `"1.2"`). `from_json_payload` raises
`ValueError` on any mismatch — no silent cross-version coercion. The version is bumped in
lockstep with producer shape changes (ADR-0007): T-DNA-7 took it `1.0 → 1.1`, T-DNA-10
took it `1.1 → 1.2`.

### Consequences

- **Positive:** payload generations are self-describing; cross-version loads fail loudly.
- **Negative:** any shape change requires a coordinated version bump or deserialization
  breaks — by design (the guard exists to force that coordination).

### Alternatives Considered

1. **No version field.** Rejected: COMLab cannot distinguish generations.
2. **Best-effort load across versions.** Rejected: silent shape mismatches corrupt the
   prior.

---

## Graph relations (explicit)

**ADR-0003** DESCRIBES **versioned envelope with hard mismatch guard**
**SCHEMA_VERSION** CONSUMED_BY **VehicleDNA.from_json_payload()** (ValueError on mismatch)
**SCHEMA_VERSION** CONSUMED_BY **COMLab generation detection** (distinguishes 1.2 from legacy)
**ADR-0003** GATED_BY **ADR-0007** (coordinated schema bump)
