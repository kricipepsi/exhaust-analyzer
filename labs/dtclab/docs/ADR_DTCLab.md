# ADR — DTCLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-11
**Scope:** Architecture Decision Records for the DTCLab v2 module (`labs/dtclab/`)

Format: Nygard template (`_skills/doc/ADR.md`). Each record captures a decision that shipped in
the `dtclab/` package (AST ground truth, June 2026), its context, and its consequences. ADRs are
historical records; once accepted they are superseded, not edited. The signal/noise rule governs
every record: a field, tag, or enum value ships only with a named, existing consumer.

| ADR | Title | Status |
|---|---|---|
| ADR-0001 | Strict lab isolation via a locally-mirrored DNA view | Accepted |
| ADR-0002 | Typed `DTCLabPayload` as the single COMLab boundary contract | Accepted |
| ADR-0003 | DNA gate as a *filter*, not a *requirement* (three-branch confidence) | Accepted |
| ADR-0004 | Routing-tag mapping in external YAML, not code | Accepted |
| ADR-0005 | `POA_HISTORY` injected by COMLab, never emitted by DTCLab | Accepted |
| ADR-0006 | Cross-field coolant/fluid signatures as a post-mapping step (5b) | Accepted |
| ADR-0007 | Phase-2 scorer reuses §16 weights — no new numeric literal, no normalisation | Accepted |
| ADR-0008 | Drop `SAI_HISTORY` / secondary-air from the routing surface | Accepted |
| ADR-0009 | Surface Mode $06 monitor-aborted / no-start state (`EP-DTC-NOSTART-1`) | Proposed |

---

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

## ADR-0002: Typed `DTCLabPayload` as the single COMLab boundary contract

**Status:** Accepted

**Context.** DTCLab produces several heterogeneous outputs (three DTC lists, routing tags, Mode $06
results, historical context, freeze frame, MIL state). COMLab needs one stable, validated contract.

**Decision.** All output is assembled into a single Pydantic model, `DTCLabPayload` (9 fields),
validated at the boundary. Field validators enforce the DTC regex (`ERR-CONTRACT-001`), routing-tag
membership (`ERR-CONTRACT-002`), and the Mode $06 MID-key pattern. COMLab consumes it at the
`dtc_lab_output` key of its inbound request (vocab §17).

**Consequences.**
- (+) One typed seam; malformed data fails at DTCLab's edge, not deep in COMLab.
- (+) Error codes give COMLab a deterministic failure contract.
- (−) Every new payload field needs a named COMLab consumer or it does not ship — intentional friction.

**Alternatives considered.** (1) Returning a tuple/dict of parts — rejected: no single validation
point, no typed contract. (2) Multiple return surfaces — rejected: multiplies the integration
contract COMLab must track.

---

## ADR-0003: DNA gate as a *filter*, not a *requirement* (three-branch confidence)

**Status:** Accepted

**Context.** DNA-gated tags (`CATALYST_HISTORY`, `EGR_HISTORY`) should be suppressed
on vehicles that physically lack the hardware — but VIN decoding is not always confident, and a
missing/low-confidence VIN must not silently drop real DTC evidence.

**Decision.** The gate is keyed on `DtcLabDnaView.confidence` with three branches: `HIGH` →
strict hardware-presence check; `PARTIAL` → emit with a logged downgrade; `NONE` (or `dna_view is
None`) → emit unconditionally (pure DTC-pattern routing). The DNA gate filters false positives
*when it can be trusted* and otherwise yields to the DTC evidence.

**Consequences.**
- (+) No real fault is suppressed by an absent/weak VIN; false positives are removed only on HIGH.
- (+) Same pattern as GASLab/OBDLab — one mental model across labs.
- (−) On HIGH-but-wrong DNA, a real fault could be suppressed; mitigated by unknown-gate fail-open.

**Alternatives considered.** (1) Hard requirement (suppress unless hardware proven) — rejected:
drops evidence whenever VIN is missing. (2) No gating — rejected: floods COMLab with
hardware-impossible tags (e.g. catalyst codes on a pre-cat vehicle).

---

## ADR-0004: Routing-tag mapping lives in external YAML, not code

**Status:** Accepted

**Context.** The DTC-range → routing-tag relation is large (32 entries), churns as coverage grows,
and must be auditable against the wiki (`DTC_VOCABULARY.md §15`).

**Decision.** Mappings live in `dtclab/config/routing_tag_map.yaml`, each entry carrying
`patterns`, `tag`, `source_wiki` provenance, and optional `dna_gate`. `RoutingTagMapper` compiles
them at construction. Adding coverage is a data edit with a citation, not a code change.

**Consequences.**
- (+) Coverage changes are reviewable as data diffs with provenance; no recompile of logic.
- (+) The same YAML feeds both the mapper and the Phase-2 scorer's rule set.
- (−) A malformed YAML surfaces only at load time (`FileNotFoundError` / parse error at import) —
  accepted as fail-at-startup over fail-at-runtime.

**Alternatives considered.** (1) Hard-coded `if/elif` ladder — rejected: unreviewable, no
provenance. (2) A database — rejected: over-engineered for a static, version-controlled table.

---

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

## ADR-0007: Phase-2 scorer reuses §16 weights — no new literal, no normalisation

**Status:** Accepted

**Context.** COMLab's Bayesian fusion (`combine()`, FU-1) wants ranked `(fault_family, confidence)`
candidates, not raw tags. DTCLab is the natural place to rank DTC evidence, but must not invent a
parallel scoring scheme or pre-empt COMLab's normalisation.

**Decision.** `ranking.py` computes per-family confidence purely from the existing
`DTC_CONFIDENCE_WEIGHTS` (§16) and the §14.2 DNA factors (1.0/0.7/0.5). `rank_candidates` takes the
max contributing weight per family and tags evidence strength via `MatchType`. `classify_top3`
clamps to the unit interval, dedups, and returns the top 3 — with **no sum-1 normalisation** and
**no `LabResult` construction** (those belong to COMLab `combine()` and the Wired adapter `T-DTW-1`).

**Consequences.**
- (+) Single source of truth for weights; no drift between the payload weights and the scorer.
- (+) Clear ownership: DTCLab ranks, COMLab fuses/normalises, Wired adapts.
- (−) The scorer's consumer is the Wired adapter, which must exist for the surface to be live —
  acceptable, it is a named, specced consumer (`T-DTW-1`), not "future use".

**Alternatives considered.** (1) Normalising to sum-1 in DTCLab — rejected: double-normalisation
corrupts the Bayesian fusion. (2) Introducing family/tier confidence ceilings — rejected: adds
unsourced numeric literals (DESIGN §6 forbids it).

---

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

## ADR-0009: Surface Mode $06 monitor-aborted / no-start state (`EP-DTC-NOSTART-1`)

**Status:** Proposed

**Context.** A non-starting engine often leaves Mode $06 monitors in a *monitor-aborted /
Incomplete* state (e.g. MID $A1 / TID $53) rather than pass/fail, and the freeze frame may show
fuel/spark-cut. Today `classify_margin` only resolves the three margin tri-states, so the no-start
signal is invisible to COMLab.

**Decision (proposed, not shipped).** Extend `mode06_evaluator.py` and the Mode-06 schemas to
surface a monitor-aborted/Incomplete state plus a freeze-frame fuel/spark-cut indicator, CAN-era
gated. This ships **with** its consumer — COMLab `T-COMV2-NOSTART-1` — as a co-shipped proposal,
not as a speculative field. Registered by `T-OBDV2-5`; tracked as `T-DTCV2-NOSTART-1`.

**Consequences (anticipated).**
- (+) Enables no-start diagnosis, a high-leverage gap (DTC-absent cases dominate the audit backlog).
- (+) Stays within signal/noise: the new state's consumer is named and specced before code lands.
- (−) Adds a fourth Mode $06 state and a freeze-frame field — both must be drift-guarded and
  CAN-era gated to avoid false positives on pre-CAN vehicles.

**Alternatives considered.** (1) Inferring no-start from the absence of DTCs — rejected: ambiguous,
no positive evidence. (2) Deferring with no consumer — rejected: a consumer *can* be named
(`T-COMV2-NOSTART-1`), so the forward-progress rule makes this a proposal, not a deferral.

> This record is **Proposed** — it does not describe shipped code. It ships only when
> `T-DTCV2-NOSTART-1` and its COMLab consumer are authored and land together, and it is registered
> in `comlab/config/proposals/`.
