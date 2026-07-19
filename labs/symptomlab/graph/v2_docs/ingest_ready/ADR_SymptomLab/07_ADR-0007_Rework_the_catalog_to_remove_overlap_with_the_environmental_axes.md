> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0007: Rework the catalog to remove overlap with the environmental axes · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0007: Rework the catalog to remove overlap with the environmental axes

**Status:** Accepted (T-DNA-1 — research-revised catalog)

### Context

The legacy 18-pair catalog had tier_2 values that duplicated other axes:
`cold_engine_only` / `only_when_hot` duplicated `occurs_during`; `only_high_rpm_highway`
/ `right_after_fillup` duplicated the load axis (now shipped as `load_state`, T-DNA-2).
Duplicated dimensions inflate the routing surface and confuse the prior.

### Decision

Replace the overlapping tier_2 values with discriminating ones and fill gaps (surging
idle, prolonged crank, tip-in hesitation, knock, backfire), keeping the catalog at
exactly 18 pairs. Two tier_1 categories were renamed
(`vehicle_wont_start → vehicle_starting_issues`,
`poor_economy_fuel_odor → poor_economy_fuel_odor_sound`). The revised strings have no
live consumer yet, so the routing map ships as **proposal COMLab-A**.

### Consequences

- **Positive:** each tier_2 carries independent signal; the environmental axes own the
  thermal/load dimensions.
- **Negative:** the rename is a breaking vocabulary change COMLab-A must absorb. The
  catalog edit was completed by T-DNA-8 (now 18/18); the invariant passes.

### Alternatives Considered

1. **Keep the legacy catalog.** Rejected: dimensional overlap corrupts the prior.
2. **Expand beyond 18 pairs.** Rejected: breaks the fixed-surface invariant (ADR-0003).

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**allowed_combinations.yaml** SUPERSEDES **legacy 18-pair catalog** (dimensional overlap removed)
**tier_2 vocabulary** DERIVED_FROM **environmental-axis de-duplication rework** (T-DNA-1)
