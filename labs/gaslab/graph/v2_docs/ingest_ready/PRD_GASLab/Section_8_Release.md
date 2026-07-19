
> **Context:** GASLab PRD v2.1 (2026-06-10) · Module: GASLab · Section: Section 8 — Release · Parent document: PRD_GASLab.md
## Section 8 — Release

### v2.1 Scope

All P0 features above. Bound matching scoped to `STABILIZED_IDLE`; the high-idle reading is an optional second input that unlocks RPM-differential separation.

### Shipped since v1.0

- Timing taxonomy 32 → 34 (`WRONG_VALVE_TIMING` retired; 3 `CAM_TIMING_*` added).
- Dual-RPM input and RPM-differential family separation.
- Per-vehicle CoC `target_lambda_v112` window, Euro-class CO/HC scaling, wideband O₂-bias calibration.
- `lambda_measured` payload field (T-FX-7 no-OBD fallback).

### Explicitly Deferred (v2+)

- Cross-lab enum mirror: `OBD_VOCABULARY.md §17` / COMLab schema still at 32 — the breaking change is intentionally divergent until coordinated.
- Full `differentiator_edges` resolution of the near-identical triplet at single-point idle (`FLAT_CAMSHAFT` ↔ `O2_SENSOR_BIASED_LOW` ↔ `WORN_PISTON_RINGS`).
- `REGULATORY_HIGH_IDLE` / `STRESS_IDLE` as first-class operating states.

### Success Criteria

1. KR1–KR4 all pass in CI.
2. `test_ontology.py` confirms 34 faults, 6 DNA-gated entries, 1 `requires_dtc`, 3 catch-alls.
3. `test_rule_engine_reachability.py` confirms all 34 signatures are reachable.
4. `test_validators.py` wiki-drift guard passes.


## Graph relations (explicit)

**Section 8 — Release** DESCRIBES **GASLab PRD v2.1**
**GASLab v2.1** SUPERSEDES **GASLab v1.0** -- 34 signatures, dual-RPM, CoC targets


