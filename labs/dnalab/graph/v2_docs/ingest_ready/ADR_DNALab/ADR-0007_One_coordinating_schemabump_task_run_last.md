> **Context:** DNALab ADR_DNALab v2 (2026-06-12) · Module: DNALab · Section: ADR-0007: · Parent document: ADR_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## ADR-0007: One coordinating schema-bump task, run last (T-DNA-7)

**Status:** Accepted (DNA-family pack)

### Context

Several upstream tasks add fields across the producers (`load_state` in SymptomLab;
`rated_rpm` / CoC / `fuel_type` in VINLab). Bumping `schema_version` per task would churn
the contract repeatedly and risk partial-generation payloads.

### Decision

A single coordinating task (**T-DNA-7**, blocked by T-DNA-1/2/3/4/6) bumps
`SCHEMA_VERSION` `1.0 → 1.1` **once**, round-trips every field the upstream tasks actually
landed, and wires `load_state` through `build_vehicle_dna`. It runs last and includes only
landed fields (e.g. if `fuel_type` stayed a proposal, it is not in scope).

> **Outcome (landed):** T-DNA-7 shipped the `1.0 → 1.1` bump; the round-trip covers
> `load_state`, `rated_rpm`, and the formalized CoC fields. `fuel_type` stayed a proposal
> (COMLab-E), so it is **not** in the round-trip. A later, separate change (**T-DNA-10**,
> the `engine_state` wire-value rename) took the version `1.1 → 1.2` under the same
> lockstep rule.

### Consequences

- **Positive:** one clean version transition per shape change; no partial-generation
  payloads; COMLab sees a coherent version (now `1.2`).
- **Negative:** the bump is gated on all upstream tasks completing — intended, so the
  version never moves ahead of the shape.

### Alternatives Considered

1. **Bump per field-adding task.** Rejected: repeated contract churn, partial generations.
2. **Never version; add fields silently.** Rejected: breaks the mismatch guard (ADR-0003)
   and COMLab's generation detection.

---

## Graph relations (explicit)

**ADR-0007** DESCRIBES **one coordinating schema-bump task, run last**
**T-DNA-7** DESCRIBES **SCHEMA_VERSION 1.0→1.1 bump** (coordinated, done)
**T-DNA-10** DESCRIBES **SCHEMA_VERSION 1.1→1.2 bump** (engine_state wire-value rename, done)
**ADR-0007** GATED_BY **all upstream field tasks complete** (T-DNA-1/2/3/4/6 → T-DNA-7)
**fuel_type** DESCRIBES **stayed as proposal (COMLab-E)** (not in round-trip scope)
