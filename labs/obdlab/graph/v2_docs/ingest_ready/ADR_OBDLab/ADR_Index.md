> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · Section: ADR Index · Parent document: ADR_OBDLab.md

# Architecture Decision Records — OBDLab (v2)

**Scope:** OBDLab (Stage 2, electronic-perception channel).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-10 — back-filled from the shipped revive-as-emitter
rework (T-OBDV2-0 … T-OBDV2-11, FIX-1…7, ARCH-1/2, PURGE-1…3).

> These ADRs record decisions already implemented in `obdlab/`. They are written
> as historical records: each captures *why* a choice was made, with the task ID
> that carried it. Future changes supersede an ADR with a new one rather than
> editing it in place.

### Entity: ADR index (9 decisions)

- **ADR-0001** — Revive OBDLab as a perception-channel emitter, not a fault classifier · Status: Accepted
- **ADR-0002** — Emit at Stage 2, consume at Stage 4 — forward-registered consumers & proposals · Status: Accepted
- **ADR-0003** — No cross-lab Python imports — OBDLab mirrors the types it needs · Status: Accepted
- **ADR-0004** — Remove Physics Gate 3; fold its intent into `FAULT_VE_SENSOR_SKEW` · Status: Accepted
- **ADR-0005** — Unify the exception hierarchy under `ObdLabError` · Status: Accepted
- **ADR-0006** — Widen fuel-trim bounds to the OBD rail `±127` and treat rails as signal · Status: Accepted
- **ADR-0007** — Prune the dead standalone classifier and orphan enums/fields · Status: Accepted
- **ADR-0008** — VE is evidence only under the dual-sensor gate; single-sensor → `UNKNOWN` · Status: Accepted
- **ADR-0009** — Bank-2 trims are `null`, never `0.0`, on single-bank engines · Status: Accepted

## Graph relations (explicit)

**ADR_OBDLab v2.0** SUPERSEDES **ADR_OBDLab v1.0**
**ADR-0001..0009** DESCRIBES **9 architecture decisions** (implemented in obdlab/, back-filled 2026-06-10)
**ADR_OBDLab** MIRRORS_CONTRACT_IN **HLD_OBDLab / DLD_OBDLab / LLD_OBDLab** (design surface)
