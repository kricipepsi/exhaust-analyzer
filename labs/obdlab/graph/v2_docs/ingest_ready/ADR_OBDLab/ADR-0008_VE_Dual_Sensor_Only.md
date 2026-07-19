> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0008: VE evidence only under dual-sensor gate · Parent document: ADR_OBDLab.md

## ADR-0008: VE is evidence only under the dual-sensor gate; single-sensor → `UNKNOWN`

**Status:** Accepted (2026-06-08 — T-OBDV2-2, Q5)

### Context

VE can be computed three ways depending on the air-metering hardware. But in the
`MAP_ONLY` and `MAF_ONLY` branches the missing sensor is emulated/back-calculated
from the very quantity VE would cross-check, so the value algebraically cancels —
there is no independent corroboration.

### Decision

Only `DUAL_MAF_MAP_CROSSCHECK` yields a classified `ve_validity` (VALID or one of
the three fault modes). `MAP_ONLY` and `MAF_ONLY` always return
`VEValidity.UNKNOWN`. COMLab treats VE as evidence **only** when validity is not
`UNKNOWN`; single-sensor rationality is left to P0068-style checks.

### Consequences

- **Positive:** OBDLab never overstates VE confidence it cannot justify.
- **Positive:** the `0.0` sentinel + `UNKNOWN` pair cleanly suppresses VE-based
  router decisions.
- **Negative:** single-sensor vehicles get no VE-fault evidence from OBDLab;
  that diagnosis must come from elsewhere.

### Alternatives Considered

1. **Classify validity in all three branches.** Rejected: would assert
   cross-checks that do not exist.
2. **Emit no VE for single-sensor configs.** Rejected: `ve_pct` is still useful
   context; only its *validity* is unknown.

## Graph relations (explicit)

**ADR-0008** DESCRIBES **VE evidence only under dual-sensor gate** (single-sensor → UNKNOWN)
**T-OBDV2-2 (Q5)** DESCRIBES **ADR-0008** (task that carried it)
**DUAL_MAF_MAP_CROSSCHECK** CONSUMES **VEValidity classification** (VALID or fault mode)
**MAP_ONLY / MAF_ONLY** CONSUMES **VEValidity.UNKNOWN** (always, no cross-check possible)
**COMLab T-COMV2-VE-GATE-1** CONSUMES **ve_validity** (evidence only when not UNKNOWN)
