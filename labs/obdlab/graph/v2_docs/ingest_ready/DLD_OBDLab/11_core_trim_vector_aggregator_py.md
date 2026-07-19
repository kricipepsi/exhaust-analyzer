> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 11 core/trim_vector_aggregator.py · Parent document: DLD_OBDLab.md

## 11. `core/trim_vector_aggregator.py` — `TrimVectorAggregator`

`aggregate(sanitized_pids) → (bank1_tft, bank2_tft|None, per_bank_trim_delta|None)`.

```
bank1 = shrtft1 + longft1                    (always; None → PIDValidationError)
if number_of_banks != 2: return (bank1, None, None)
shrtft2/longft2 None when banks==2 → PIDValidationError
bank2 = shrtft2 + longft2
per_bank_trim_delta = bank1 − bank2
```

Bank-2 contract and `per_bank_trim_delta` are the bank-asymmetry channel
(T-OBDV2-BANK-ASYM-1).

## Graph relations (explicit)

**TrimVectorAggregator.aggregate** CONSUMES **shrtft1 / longft1 / shrtft2 / longft2** (trim inputs)
**TrimVectorAggregator.aggregate** DERIVED_FROM **total_trim_correction_delta = shrtft1 + longft1**
**TrimVectorAggregator.aggregate** DERIVED_FROM **total_trim_correction_delta_b2 = shrtft2 + longft2**
**TrimVectorAggregator.aggregate** DERIVED_FROM **per_bank_trim_delta = bank1 − bank2**
**TrimVectorAggregator** GATED_BY **SEMANTIC_CONTRACT §4.4** (bank-2 null contract)
**COMLab T-COMV2-BANK-FUSE-1** CONSUMES **per_bank_trim_delta** (S4 forward-reg, T-OBDV2-BANK-ASYM-1)
**test_trim_vector_aggregator.py** VERIFIES **TrimVectorAggregator** (unit tests)
