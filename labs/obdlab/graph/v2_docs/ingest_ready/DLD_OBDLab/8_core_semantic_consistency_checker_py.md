> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 8 core/semantic_consistency_checker.py · Parent document: DLD_OBDLab.md

## 8. `core/semantic_consistency_checker.py` — `SemanticConsistencyChecker`

`evaluate(sanitized_pids, dna_view) → dict` returns
`{rpm_state_bucket_override, engine_warmed, trim_analytics_suspect, gates_passed}`.

### Entity: Semantic consistency gates

- **Thermal** — `ECT < 75` · Effect: override bucket → `COLD_OPEN_LOOP_INVALID`; `engine_warmed=False`
- **Physics_Gate_1** — `VSS > 10 AND RPM < 400` · Effect: `SemanticConsistencyError`
- **Physics_Gate_2** — `ECT ≥ 80 AND fuel_status == OL` · Effect: `SemanticConsistencyError`
- **Physics_Gate_4** — trim outside `[-127, 127]` · Effect: `SemanticConsistencyError`
- **Closed-loop** — `ECT ≥ 75 AND fuel_status != CL` · Effect: `trim_analytics_suspect=True` (non-blocking)

`gates_passed` lists the 3 physics gates that passed; the orchestrator derives
`semantic_gates_passed = (len(gates_passed) == 3)`. **Physics_Gate_3 (the NA VE
ceiling) was removed (FIX-1 Option B)** — its intent is now carried by
`VEValidity.FAULT_VE_SENSOR_SKEW` in the VE engine.

## Graph relations (explicit)

**SemanticConsistencyChecker.evaluate** GATED_BY **Thermal gate** (ECT < 75 → COLD_OPEN_LOOP_INVALID)
**SemanticConsistencyChecker.evaluate** GATED_BY **Physics_Gate_1** (VSS > 10 AND RPM < 400)
**SemanticConsistencyChecker.evaluate** GATED_BY **Physics_Gate_2** (ECT ≥ 80 AND fuel_status == OL)
**SemanticConsistencyChecker.evaluate** GATED_BY **Physics_Gate_4** (trim outside [-127, 127])
**Physics_Gate_3** SUPERSEDES **FAULT_VE_SENSOR_SKEW** (FIX-1 Option B)
**test_semantic_consistency_checker.py** VERIFIES **SemanticConsistencyChecker** (unit tests)
