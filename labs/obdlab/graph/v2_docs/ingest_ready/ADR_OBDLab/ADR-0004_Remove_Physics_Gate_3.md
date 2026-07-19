> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0004: Remove Physics Gate 3 · Parent document: ADR_OBDLab.md

## ADR-0004: Remove Physics Gate 3; fold its intent into `FAULT_VE_SENSOR_SKEW`

**Status:** Accepted (2026-06-08 — T-OBDV2-FIX-1, Option B)

### Context

Physics Gate 3 raised on "VE > 90% on a naturally-aspirated engine at stabilized
idle". The same physical condition is also expressible as a VE-validity
classification, creating two code paths for one fact — and the gate raised
(hard-stopping the pipeline) for what is really an evidence signal.

### Decision

Remove Physics Gate 3 from `SemanticConsistencyChecker`. Carry its intent as
`VEValidity.FAULT_VE_SENSOR_SKEW` in the VE engine (VE > 90 AND
`STABILIZED_IDLE` AND `NATURALLY_ASPIRATED`). The semantic checker now runs gates
**1, 2, 4** only; `gates_passed` collects three.

### Consequences

- **Positive:** one code path for the NA-VE-ceiling condition; it becomes
  emitted evidence (`ve_validity`) rather than a pipeline-aborting raise.
- **Positive:** removes a `dead_read` of `calculated_ve` flagged in the audit.
- **Negative:** downstream readers must treat `FAULT_VE_SENSOR_SKEW` as a
  validity value, not an exception — a contract change COMLab must honour.
- **Neutral:** `semantic_gates_passed` is now `len(gates_passed) == 3`.

### Alternatives Considered

1. **Keep Gate 3 as a raise** (Option A). Rejected: hard-stops on an evidence
   signal and duplicates the VE classifier.
2. **Keep both** the gate and the validity value. Rejected: two sources of truth
   for one condition.

## Graph relations (explicit)

**ADR-0004** DESCRIBES **Remove Physics Gate 3** (fold intent into FAULT_VE_SENSOR_SKEW)
**T-OBDV2-FIX-1 (Option B)** DESCRIBES **ADR-0004** (task that carried it)
**Physics_Gate_3** SUPERSEDES **FAULT_VE_SENSOR_SKEW** (VE validity classifier replaces gate)
**SemanticConsistencyChecker** GATED_BY **gates 1, 2, 4 only** (gates_passed == 3)
**COMLab** CONSUMES **ve_validity.FAULT_VE_SENSOR_SKEW** (evidence signal, not exception)
