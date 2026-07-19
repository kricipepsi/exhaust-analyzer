> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0005: Single deep air-metering module replaces two parallel switches | Parent document: ADR_VINLab.md

## ADR-0005: Single deep air-metering module replaces two parallel switches

**Status:** Accepted (T-FX-2 — audit candidate #3, "two views of one fact")

### Context

`VinDNA` ships both `primary_load_calculation` (developer label) and
`air_metering_strategy` (OBDLab-canonical). Two separate switch statements computed
these from `(has_maf, has_map)`, so the same physical fact had two code paths that
could disagree.

### Decision

Introduce `overlay/air_metering.classify_air_metering(has_maf, has_map)`, a single deep
module returning a frozen `AirMeteringClassification` with **both** labels from one
classification. The decoder calls it once.

### Consequences

- **Positive:** one source of truth for the air-metering fact; the two labels can never
  disagree.
- **Neutral:** the mapping table is now centralised (both → DUAL/HYBRID, MAF → MAF_ONLY,
  MAP/neither → MAP_ONLY/SPEED_DENSITY).

### Alternatives Considered

1. **Keep two switches, add a consistency test.** Rejected: tests a defect that
   shouldn't be expressible.
2. **Drop one label.** Rejected: both are consumed (developer ergonomics vs OBDLab
   routing).

---

## Graph relations (explicit)

**ADR-0005: Single deep air-metering module replaces two parallel switches** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.overlay.air_metering.classify_air_metering** IMPLEMENTS **ADR-0005**
**labs/vinlab/tests/unit/test_air_metering.py** VERIFIES **vinlab.overlay.air_metering.classify_air_metering**
