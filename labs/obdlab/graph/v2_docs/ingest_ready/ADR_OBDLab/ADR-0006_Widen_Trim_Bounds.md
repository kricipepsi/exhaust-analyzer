> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0006: Widen fuel-trim bounds to ±127 · Parent document: ADR_OBDLab.md

## ADR-0006: Widen fuel-trim bounds to the OBD rail `±127` and treat rails as signal

**Status:** Accepted (T-W-6)

### Context

The OBD-nominal trim range is roughly `[-100, 99.22]%`. Real ECUs report
**railed** values (`±127`) when a trim saturates — and a railed trim is itself a
diagnostic signal (the fuel system has run out of correction authority).
Rejecting `±127` as out-of-bounds would discard that signal.

### Decision

Widen the `shrtft*`/`longft*` bounds (in `physical_sensor_bounds.json` and the
Physics Gate 4 rails) to `[-127, 127]`. Document the rail value as a
sensor-fault signal consumed by COMLab trim-evidence scoring.

### Consequences

- **Positive:** railed trims survive validation and reach COMLab as evidence.
- **Negative:** the validator no longer rejects physically implausible mid-range
  values that happen to fall inside `±127`; semantic plausibility moves
  downstream.
- **Neutral:** bounds, Physics Gate 4 rails, and the JSON note are kept in sync.

### Alternatives Considered

1. **Keep nominal bounds and reject `±127`.** Rejected: loses the saturation
   signal.
2. **Clamp `±127` to nominal.** Rejected: fabricates a value and still loses the
   "railed" fact.

## Graph relations (explicit)

**ADR-0006** DESCRIBES **Widen trim bounds to OBD rail ±127** (treat rails as sensor-fault signal)
**T-W-6** DESCRIBES **ADR-0006** (task that carried it)
**shrtft1/longft1/shrtft2/longft2** GATED_BY **[-127, 127]** (widened from OBD-nominal [-100, 99.22])
**Physics_Gate_4** GATED_BY **[-127, 127]** (rails in sync with bounds)
**COMLab trim-evidence scoring** CONSUMES **railed trim signal** (±127 saturation as evidence)
