> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0009: Bank-2 trims are null, never 0.0 · Parent document: ADR_OBDLab.md

## ADR-0009: Bank-2 trims are `null`, never `0.0`, on single-bank engines

**Status:** Accepted (`OBDLab_KG_Wiki.md §3.1` contract; enforced in validator & aggregator)

### Context

Inline-engine (single-bank) vehicles have no bank-2 trims. Emitting `0.0` for an
absent bank is indistinguishable from a real zero trim and would corrupt
bank-asymmetry analytics (`per_bank_trim_delta`).

### Decision

When `number_of_banks == 1`, `shrtft2`/`longft2` (and the derived
`total_trim_correction_delta_b2`, `per_bank_trim_delta`) must be `null`.
Supplying a non-null bank-2 value on a single-bank engine raises
`PIDValidationError` (`SEMANTIC_CONTRACT §4.4` violation). The aggregator raises
if `number_of_banks == 2` but a bank-2 field is `None`.

### Consequences

- **Positive:** "absent bank" and "zero trim" are unambiguous; bank-asymmetry
  analytics stay sound.
- **Negative:** callers must pass `None` (not `0.0`) for absent banks — a
  contract they must observe.
- **Neutral:** bank-2 validation in bounds-checking is conditional on
  `number_of_banks == 2`.

### Alternatives Considered

1. **Default absent banks to `0.0`.** Rejected: conflates absence with a real
   zero and breaks `per_bank_trim_delta`.
2. **Omit bank-2 fields entirely from single-bank payloads.** Rejected: a
   variable field set complicates the fixed JSON contract; `null` is cleaner.

## Graph relations (explicit)

**ADR-0009** DESCRIBES **Bank-2 trims null, never 0.0, on single-bank engines**
**SEMANTIC_CONTRACT §4.4** DESCRIBES **ADR-0009** (contract enforced in validator & aggregator)
**PIDIngestionValidator._enforce_bank2_contract** VERIFIES **number_of_banks==1 → shrtft2/longft2 must be None**
**TrimVectorAggregator.aggregate** VERIFIES **number_of_banks==2 → bank-2 fields must not be None**
**shrtft2/longft2** GATED_BY **null contract for single-bank** (PIDValidationError on violation)
**per_bank_trim_delta** CONSUMES **bank1 − bank2** (null-safe: absent bank → None)
