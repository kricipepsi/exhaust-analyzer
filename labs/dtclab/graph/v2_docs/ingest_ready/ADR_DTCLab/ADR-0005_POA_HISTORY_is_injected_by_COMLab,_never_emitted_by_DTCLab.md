
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0005: POA_HISTORY is injected by COMLab, never emitted by DTCLab · Parent document: ADR_DTCLab.md
## ADR-0005: `POA_HISTORY` is injected by COMLab, never emitted by DTCLab

**Status:** Accepted

**Context.** Piston/valve oil-aerosol burning (POA) produces a gas-chemistry fingerprint (HC high,
CO low, λ ≈ 1.00) but **no direct DTC**. Its truth source is GASLab chemistry, not the DTC list.

**Decision.** `POA_HISTORY` is a member of `DTCRoutingTag` (so the payload can carry it), but
`RoutingTagMapper` never produces it and it has no `routing_tag_map.yaml` entry. COMLab's
fault-atlas router injects it when `GASLab.chemical_state == POA_SIGNATURE` (T-FX-3).

**Consequences.**
- (+) Chemistry-truth ownership stays with GASLab; DTCLab does not fabricate a signal it cannot see.
- (+) `family_map.py` maps `POA_HISTORY → None` so the Phase-2 scorer never votes on it.
- (−) The "never emitted" guarantee is convention-enforced in v1 (no automated test) — tracked as
  an open gap; if it ever appears in mapper output, that is a DTCLab bug.

**Alternatives considered.** (1) DTCLab inferring POA from P0300 fallout — rejected: P0300 is
downstream noise, not a primary POA marker; the older "P250C + P0300" reading is superseded.

---


## Graph relations (explicit)

**ADR-0005** DESCRIBES **DTCLab ADR v1.0**
**routing_tag_mapper.RoutingTagMapper.map** IMPLEMENTS **ADR-0005** -- never emits POA_HISTORY
