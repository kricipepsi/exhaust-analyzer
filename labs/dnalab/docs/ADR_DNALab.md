# Architecture Decision Records — DNALab (v2)

**Scope:** DNALab (umbrella composer of the DNA family).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-11; refreshed 2026-06-12 (schema bump landed, `SCHEMA_VERSION
= "1.2"`) — consolidates the lab-level decisions; granular records remain under
`docs/adr/` (0001–0004).

> These ADRs record decisions already implemented in `dnalab/`. Each captures *why*.
> Future changes supersede an ADR with a new one rather than editing it in place.

| ADR | Title | Status |
|-----|-------|--------|
| ADR-0001 | DNALab composes; it does not decode, validate, or route | Accepted |
| ADR-0002 | DNALab is the only in-family importer (`dnalab → vinlab + symptomlab`) | Accepted |
| ADR-0003 | Versioned envelope with a hard mismatch guard | Accepted |
| ADR-0004 | Delegate serialization to each producer model | Accepted |
| ADR-0005 | Validate triage-key presence before the VIN decode | Accepted |
| ADR-0006 | Auto-stamp session identity (`DNA_TX_…` + UTC timestamp) | Accepted |
| ADR-0007 | One coordinating schema-bump task, run last (T-DNA-7) | Accepted |

---

## ADR-0001: DNALab composes; it does not decode, validate, or route

**Status:** Accepted (architecture; `docs/adr/0002-dnalab-only-importer.md`)

### Context

The DNA prior has two halves — physical identity and operator symptom — produced by two
independent labs. Something must join them under the §4.3 contract. That joiner could
also try to decode, validate, or route, but each of those is another lab's job.

### Decision

DNALab is a **thin composer**: it calls `vinlab.decode` and `symptomlab.resolve`, stamps
session metadata, and packages `VehicleDNA`. It owns no decode logic, no symptom catalog,
no routing. Correctness of each half is the producer's responsibility.

### Consequences

- **Positive:** the umbrella stays small, deterministic, and easy to reason about; one
  place knows how to compose, nowhere else.
- **Positive:** producer changes don't ripple into DNALab beyond a version bump.
- **Negative:** DNALab depends on both producers being import-clean and API-stable.

### Alternatives Considered

1. **Compose in COMLab or the UI.** Rejected: scatters composition and the version
   contract across consumers.
2. **A fat umbrella that also validates/routes.** Rejected: duplicates VINLab/SymptomLab/
   COMLab responsibilities.

---

## ADR-0002: DNALab is the only in-family importer

**Status:** Accepted (`docs/adr/0002-dnalab-only-importer.md`)

### Context

The DNA family is three isolated codebases. But composition inherently needs to call
both producers — a pure no-import rule would make composition impossible.

### Decision

Permit exactly one in-family import direction: `dnalab → vinlab + symptomlab`. VINLab and
SymptomLab import no one; DNALab imports both and imports **no** COMLab. COMLab mirrors
`VehicleDNA`.

### Consequences

- **Positive:** composition is possible without breaking lab isolation; the dependency
  graph stays acyclic and one-directional.
- **Negative:** DNALab is coupled to both producers' public APIs (intended — that is its
  job).

### Alternatives Considered

1. **No imports at all (compose via JSON only).** Rejected: would force the UI to call
   both labs and hand DNALab raw dicts, scattering the orchestration.
2. **Bidirectional imports.** Rejected: reintroduces cycles.

---

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

## ADR-0004: Delegate serialization to each producer model

**Status:** Accepted (`docs/adr/0003`/`0004`; models API)

### Context

`VehicleDNA` nests `VinDNA` and `SymptomDNA`. The umbrella could re-enumerate their
fields when serializing, but that would duplicate field knowledge and drift the moment a
producer changes.

### Decision

`to_json_payload` calls `vin_dna.to_json()` / `symptom_dna.to_json()`;
`from_json_payload` calls `VinDNA.from_json` / `SymptomDNA.from_json`. DNALab knows only
the five top-level keys; the inner shapes belong to the producers.

### Consequences

- **Positive:** no duplicated field knowledge; producer field changes need no DNALab edit
  (only a version bump when the shape changes).
- **Neutral:** round-trip correctness depends on each producer's `to_json`/`from_json`
  being inverses.

### Alternatives Considered

1. **Flatten everything in the umbrella.** Rejected: duplicates and drifts field
   knowledge.
2. **A shared serializer utility.** Rejected: re-couples the labs.

---

## ADR-0005: Validate triage-key presence before the VIN decode

**Status:** Accepted (assembly API)

### Context

`build_vehicle_dna` does two pieces of work: a (heavier) VIN decode and a symptom
resolve. If the triage dict is incomplete, doing the decode first wastes work and reports
the wrong failure.

### Decision

Check the four required triage keys (`tier_1`, `tier_2`, `occurs_during`, `engine_state`)
**first**; raise `SymptomValidationError` immediately if any is missing, before calling
`vinlab.decode`.

### Consequences

- **Positive:** fail-fast on the cheap check; the error names the real problem (missing
  triage), not a downstream symptom.
- **Neutral:** the VIN is only decoded once the triage is structurally complete.

### Alternatives Considered

1. **Decode first, validate triage later.** Rejected: wastes the decode and obscures the
   real failure.
2. **Let `symptomlab.resolve` raise on the missing kwargs.** Rejected: the explicit
   pre-check gives a single, clear `build_vehicle_dna`-level error.

---

## ADR-0006: Auto-stamp session identity

**Status:** Accepted (models API)

### Context

COMLab's orchestrator correlates the DNA prior with the rest of the pipeline by session.
Requiring callers to supply a session id and timestamp invites omission and format drift.

### Decision

`VehicleDNA.new` auto-generates `session_id = DNA_TX_<10 hex upper>` and an ISO-8601 UTC
`timestamp` when not supplied, while still accepting caller-supplied values for testing
and replay.

### Consequences

- **Positive:** every payload is correlatable and consistently formatted with no caller
  effort.
- **Neutral:** the id is a UUID4 slice (10 hex) — collision-safe for session scope, not a
  cryptographic guarantee.

### Alternatives Considered

1. **Require callers to supply identity.** Rejected: invites omission/format drift.
2. **Full UUID string.** Rejected: the 10-hex `DNA_TX_` form is human-legible and
   sufficient for session correlation.

---

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

## References

- `SEMANTIC_CONTRACT.md §4.3` — `VehicleDNA` schema + `schema_version`.
- `docs/adr/0001`–`0004` — granular naming/import/enum decisions.
- `docs/audits/AUDIT_2026-06-11_dna_vin_rework_and_dna10_answerability.md` — rework audit.
- `tasks/PROGRESS.md` — DNA-family ledger (T-DNA-7 coordinating task).
- `HLD_DNALab.md` / `DLD_DNALab.md` / `LLD_DNALab.md` — current design surface.
