
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0008: Drop SAI_HISTORY / secondary-air from the routing surface · Parent document: ADR_DTCLab.md
## ADR-0008: Drop `SAI_HISTORY` / secondary-air from the routing surface

**Status:** Accepted

**Context.** Earlier DTCLab design carried `SAI_HISTORY` (P0411) gated by a
`secondary_air_equipped` emissions flag. Secondary-air injection operates during cold-start
light-off (~260 °C), below 4DLab's ≥ 75 °C read-floor — so the SAI signal is unreadable in the idle
window 4DLab actually ingests.

**Decision.** `SAI_HISTORY`, the `secondary_air_equipped` flag, the P0411 YAML entry, and the
`secondary_air_equipped` gate branch are all removed from shipped code. `DTCRoutingTag` is 18
values; `DtcEmissionsView` is 3 flags; the routing map has 5 DNA-gated entries. The decision is
recorded in `wiki/11_proposals_register.md §11.4`.

**Consequences.**
- (+) No dead signal in the contract; every routing tag is something 4DLab can actually observe.
- (−) Vehicles that genuinely fail SAI get no DTCLab tag for it — accepted, as the data is outside
  4DLab's read window anyway.

**Alternatives considered.** Keep `SAI_HISTORY` as a pass-through — rejected: a tag with no readable
signal and no consumer violates signal/noise.

---


## Graph relations (explicit)

**ADR-0008** DESCRIBES **DTCLab ADR v1.0**
**DTCRoutingTag** SUPERSEDES **v1 secondary_air_equipped** -- secondary-air dropped
