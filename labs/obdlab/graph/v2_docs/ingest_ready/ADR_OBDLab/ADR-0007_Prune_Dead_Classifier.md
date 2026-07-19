> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0007: Prune dead standalone classifier and orphan enums/fields · Parent document: ADR_OBDLab.md

## ADR-0007: Prune the dead standalone classifier and orphan enums/fields

**Status:** Accepted (2026-06-08 — T-OBDV2-PURGE-1/2/3, ARCH-1/2)

### Context

Post-revive (ADR-0001), several constructs had no consumer: the standalone
ranking/classification path (`ranking.py`, `family_map.py`), the
`VERoutingMode` enum (a duplicate of `AirMeteringStrategy`), several
`O2FailureMode` members (`SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`),
the `ObdLabDnaView` fields `cylinder_count`/`emissions`/`resolved_horizon`, and
the `EuroEmissionCategory`/`ResolvedHorizon` enums. The signal/noise rule says a
field read nowhere is an orphan.

### Decision

Excise all of the above. Keep `O2FailureMode` at four members
(`NO_FAULT`, `STUCK_LEAN`, `STUCK_RICH`, `WIDEBAND_OFFSET_CANDIDATE`) and
`ObdLabDnaView` at seven fields. COMLab fusion consumes the full payload, not a
top-3 ranking, so the classifier is genuinely dead.

### Consequences

- **Positive:** the surface matches what is actually consumed; no orphan fields;
  smaller, clearer schemas.
- **Negative:** removing required DNA fields forced edits across the tests that
  build `ObdLabDnaView` (8 files in PURGE-2) — a one-time cost.
- **Neutral:** any future need for a pruned member returns via the proposal path
  (ADR-0002), not by un-deleting.

### Alternatives Considered

1. **Keep orphans "for future use".** Rejected: direct signal/noise breach.
2. **Mark them deprecated but retained.** Rejected: dead surface still has to be
   maintained and drift-guarded.

## Graph relations (explicit)

**ADR-0007** DESCRIBES **Prune dead classifier and orphan enums/fields** (signal/noise enforcement)
**T-OBDV2-PURGE-1/2/3, ARCH-1/2** DESCRIBES **ADR-0007** (tasks that carried it)
**O2FailureMode v2** SUPERSEDES **v1 members: SLUGGISH, DEAD, WRONG_CENTERLINE, HEATER_FAULT** (no consumer, pruned)
**ObdLabDnaView v2** SUPERSEDES **v1 fields: cylinder_count, emissions, resolved_horizon** (no consumer, pruned)
**VERoutingMode** SUPERSEDES **AirMeteringStrategy** (duplicate removed, ARCH-2)
**EuroEmissionCategory, ResolvedHorizon** SUPERSEDES **(removed)** (no live consumer, PURGE-2)
