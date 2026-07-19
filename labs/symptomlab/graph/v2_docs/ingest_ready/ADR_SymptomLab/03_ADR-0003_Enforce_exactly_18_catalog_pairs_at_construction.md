> **Context:** SymptomLab ADR v2.1 (2026-06-12) · Module: SymptomLab · ADR-0003: Enforce exactly 18 catalog pairs at construction · Parent document: ADR_SymptomLab.md · Boundary contract: SEMANTIC_CONTRACT §4.2

## ADR-0003: Enforce exactly 18 catalog pairs at construction

**Status:** Accepted (contract §4.2)

### Context

COMLab's symptom→family routing map is keyed by `(tier_1, tier_2)`. If the catalog could
be any size, the routing surface would be unbounded and untestable, and an accidental
drop/duplicate would silently change the diagnosis.

### Decision

`SymptomValidator.__init__` raises `ValueError` unless the catalog defines **exactly 18**
pairs (6 × 3). The check runs at construction, before any triage is validated.

### Consequences

- **Positive:** the routing surface is a fixed, fully-tested 18-key set; accidental
  drift fails fast and loudly.
- **Negative:** a partial catalog edit breaks construction entirely. This was seen
  mid-pack when the live file briefly sat at 17 pairs; T-DNA-8 reconciled it to 18 and the
  invariant now passes. This is the invariant working as designed — surfacing an
  incomplete edit rather than shipping it silently.

### Alternatives Considered

1. **Accept any catalog size.** Rejected: unbounded, untestable routing surface.
2. **Warn instead of raise.** Rejected: a wrong-size catalog would reach production.

---
---

## Graph relations (explicit)

**ADR_SymptomLab.md** DESCRIBES **SymptomLab** (operator-symptom channel, Part B of DNA family)
**SymptomDNA** GOVERNED_BY **SEMANTIC_CONTRACT §4.2**
**SymptomValidator** GATED_BY **18-pair construction invariant**
**allowed_combinations.yaml** GATED_BY **fixed-size invariant** (catalog drift → construction failure)
