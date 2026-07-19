> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0004: Enum-typed VinDNA fields replace bare str | Parent document: ADR_VINLab.md

## ADR-0004: Enum-typed `VinDNA` fields replace bare `str`

**Status:** Accepted (T-FX-5)

### Context

Early `VinDNA` annotated vocabulary fields as bare `str`. Typos and out-of-vocabulary
values were not caught until far downstream, and the contract §8 vocabulary was not
enforced at the type level.

### Decision

Replace bare `str` annotations with local `StrEnum` types whose members carry the exact
`SEMANTIC_CONTRACT §8` strings (`InductionType`, `FuelDeliveryType`, `AirMeteringStrategy`,
`EuroEmissionCategory`, etc.). `to_json()` coerces members to `.value`, so the wire form
is unchanged; `from_json()` raises on an unknown string.

### Consequences

- **Positive:** invalid vocabulary fails at construction, not downstream.
- **Positive:** the future cut-over to `comlab.schemas.vocabulary` is a one-line import
  swap.
- **Negative:** the enums are presently duplicated in `models.py` rather than imported.

### Alternatives Considered

1. **Keep bare `str` + runtime validators.** Rejected: validation scattered, types
   uninformative.
2. **Import enums from COMLab now.** Rejected: would break the no-cross-lab-import rule
   before Phase 0b.

---

## Graph relations (explicit)

**ADR-0004: Enum-typed VinDNA fields replace bare str** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.models.VinDNA** IMPLEMENTS **ADR-0004**
**labs/vinlab/tests/unit/test_models.py** VERIFIES **vinlab.models.VinDNA**
