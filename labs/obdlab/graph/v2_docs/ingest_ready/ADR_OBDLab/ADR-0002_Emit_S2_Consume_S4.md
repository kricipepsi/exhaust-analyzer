> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0002: Emit at Stage 2, consume at Stage 4 · Parent document: ADR_OBDLab.md

## ADR-0002: Emit at Stage 2, consume at Stage 4 — forward-registered consumers & proposals

**Status:** Accepted (2026-06-08 — T-OBDV2-ECU-PERCEPT-1 and the T-OBDV2-2…11 pack)

### Context

The signal/noise rule is non-negotiable: every schema field must have a named,
existing consumer in COMLab analytics or fault-atlas routing — "future use" is
not a consumer. But OBDLab (Stage 2) is built **before** the COMLab fusion tasks
(Stage 4) that will read several of its channels. A strict reading would block
useful channels until COMLab is rebuilt.

### Decision

Allow a field to ship at Stage 2 when its consumer is **named and specced as a
forward-registered COMLab task** (e.g. `T-COMV2-VE-GATE-1`,
`T-COMV2-ECU-FUSE-1`), recorded in the proposals registry with the consumer and
code path. New diagnostic content defaults to a **proposal** (e.g. `EP-OBD-11`,
`EP-OBD-12`, `EP-OBD-17`) rather than to "defer/PENDING". The proposal and its
consumer are tracked together; the Stage-4 anti-orphan grep closes the loop when
the COMLab reader lands.

### Consequences

- **Positive:** OBDLab makes forward progress without waiting on COMLab; the
  signal/noise discipline is preserved (every field has a *named* consumer).
- **Positive:** the emit-S2/consume-S4 fields are an explicit frozen contract,
  so COMLab reconciles **up to** OBDLab, not the reverse.
- **Negative:** between Stage 2 and Stage 4 these fields are read by no *live*
  COMLab path — an accepted, tracked divergence (HLD §9), not an orphan.
- **Negative:** requires discipline — a forward-registered task that never lands
  would turn its field into a real orphan.

### Alternatives Considered

1. **Defer every cross-stage field to PENDING** until COMLab exists. Rejected:
   this is the "v1-stuck" failure mode; it defers nameable consumers.
2. **Ship fields with no consumer ("future use")** and wire them later.
   Rejected: a direct signal/noise breach.

## Graph relations (explicit)

**ADR-0002** DESCRIBES **emit-S2 / consume-S4 pattern** (forward-registered consumers, proposals registry)
**T-OBDV2-ECU-PERCEPT-1, T-OBDV2-2..11** DESCRIBES **ADR-0002** (tasks that carried it)
**OBDLivePayload** MIRRORS_CONTRACT_IN **COMLab frozen contract surface** (emit-S2 / consume-S4)
**Anti-orphan grep (Stage 4)** VERIFIES **forward-registered fields have live reader** (closes loop)
**Proposals: EP-OBD-11, EP-OBD-12, EP-OBD-17** DESCRIBES **forward-registered proposals** (comlab/config/proposals/)
