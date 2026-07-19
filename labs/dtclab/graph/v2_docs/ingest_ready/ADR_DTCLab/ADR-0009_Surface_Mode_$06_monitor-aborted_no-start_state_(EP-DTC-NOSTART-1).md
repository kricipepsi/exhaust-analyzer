
> **Context:** DTCLab ADR v1.0 (2026-06-11) · Module: DTCLab · Section: ADR-0009: Surface Mode $06 monitor-aborted / no-start state (EP-DTC-NOSTART-1) · Parent document: ADR_DTCLab.md
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


## Graph relations (explicit)

**ADR-0009** DESCRIBES **DTCLab ADR v1.0**
**EP-DTC-NOSTART-1** PROPOSAL **T-COMV2-NOSTART-1** -- proposed monitor-aborted state
