
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0001: Strict lab isolation via a locally-mirrored DNA view · Parent document: ADR_DTCLab.md
## ADR-0001: Strict lab isolation via a locally-mirrored DNA view

**Status:** Accepted

**Context.** DTCLab needs vehicle context (catalyst/EGR presence, emissions horizon, VIN
confidence) to gate routing tags. That context originates in DNALab/VINLab and is projected by
COMLab. A direct import (`from comlab import VehicleDNA`) would couple DTCLab to COMLab's release
cycle and break the workspace's non-negotiable "no cross-lab Python imports" boundary.

**Decision.** DTCLab defines its **own** slim mirror, `DtcLabDnaView` (+ `DtcEmissionsView` and
the four mirror enums), in `dtclab/schemas/dna_view.py`. COMLab populates it via
`COMLab.project(..., target='dtc')` and passes it in through the `DataFusionSanitizer`
constructor. DTCLab imports nothing from any sibling lab; the mirror carries only the fields DTCLab
actually reads.

**Consequences.**
- (+) Labs stay independently testable; isolation is enforced by `test_dna_view.py`'s import audit.
- (+) The DNA view is exactly as wide as its consumers (signal/noise honoured).
- (−) Enum values can diverge from OBDLab (`HORIZON_CLASSIC` vs `HORIZON_ADAPTIVE`), so COMLab must
  maintain an explicit mapping (see LLD §13). This is accepted as the cost of isolation.

**Alternatives considered.** (1) Direct import of COMLab types — rejected: violates the isolation
rule and creates a build-time cycle. (2) Passing a loose `dict` — rejected: no type safety, no
Pydantic validation, was the prior shape replaced per `NewArchProposal_ImplementationPlan.md §4`.

---


## Graph relations (explicit)

**ADR-0001** DESCRIBES **DTCLab ADR v1.0**
**dna_view.DtcLabDnaView** IMPLEMENTS **ADR-0001** -- local mirror
**test_dna_view.py** VERIFIES **ADR-0001**
