
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0006: Cross-field coolant/fluid signatures as a post-mapping step (5b) · Parent document: ADR_DTCLab.md
## ADR-0006: Cross-field coolant/fluid signatures as a post-mapping step (5b)

**Status:** Accepted

**Context.** Two fault signatures cannot be read from a DTC alone: coolant-system malfunction
(P0128/P0117 *while in* `OL_FAULT`) and fluid-quench misfire (P030x *while in* `CL`). Each needs
the DTC **and** the freeze-frame fuel-system status together.

**Decision.** `evaluate_coolant_dtc_context(dtc, fuel_status)` runs as pipeline **step 5b**, after
routing-tag mapping and after the freeze frame is extracted, appending
`COOLANT_SYSTEM_MALFUNCTION` / `CYLINDER_FLUID_MISFIRE` when both conditions hold. These two tags
have no YAML entry because they are not single-pattern matches.

**Consequences.**
- (+) Captures fluid-intrusion faults no single DTC names; both tags carry a named COMLab
  fault-atlas consumer (context-only in `family_map.py`).
- (−) The two tags can appear at the tail out of strict enum order (appended after the ordered
  mapper output) — documented in LLD §8, harmless to consumers.

**Alternatives considered.** (1) Encoding the cross-field rule in the YAML — rejected: the YAML
schema is single-axis (DTC pattern → tag) and cannot express a fuel-status precondition. (2) Doing
it inside the mapper — rejected: the mapper has no freeze-frame input by design (pure DTC→tag).

---


## Graph relations (explicit)

**ADR-0006** DESCRIBES **DTCLab ADR v1.0**
**data_fusion_sanitizer.DataFusionSanitizer.sanitize** IMPLEMENTS **ADR-0006** -- step 5b
**test_dtclab_pipeline.py** VERIFIES **ADR-0006**
