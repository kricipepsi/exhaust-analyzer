> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 13 core/analytics_preconditions.py · Parent document: DLD_OBDLab.md

## 13. `core/analytics_preconditions.py` — `AnalyticsPreconditions`

`evaluate(sanitized_pids, semantic_gates_passed) → TrimAnalyticsGate`. 8 gates,
priority order (HLD §6). Constants: `O2_FAULT_DTCS` (32 codes, P0130–P0161),
`CKP_CMP_FAULT_DTCS` ({P0335, P0340}), `ECT_WARM_THRESHOLD = 70`,
`WOT_THROTTLE_THRESHOLD = 90`. DTC checks are opaque set intersection — no regex.

## Graph relations (explicit)

**AnalyticsPreconditions.evaluate** ENUMERATES **TrimAnalyticsGate** (9 values, priority order)
**AnalyticsPreconditions.evaluate** CONSUMES **O2_FAULT_DTCS** (32 codes, P0130–P0161, local frozenset)
**AnalyticsPreconditions.evaluate** CONSUMES **CKP_CMP_FAULT_DTCS** ({P0335, P0340}, local frozenset)
**AnalyticsPreconditions.evaluate** CONSUMES **ECT_WARM_THRESHOLD = 70** / **WOT_THROTTLE_THRESHOLD = 90** (local constants)
**AnalyticsPreconditions.evaluate** CONSUMES **semantic_gates_passed** (from orchestrator)
**COMLab** CONSUMES **trim_analytics_gate** (confidence path — suppress trim findings unless VALID)
**test_analytics_preconditions.py** VERIFIES **AnalyticsPreconditions** (unit tests)
