> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: Preamble | Parent document: ADR_VINLab.md

# Architecture Decision Records — VINLab (v2)

**Scope:** VINLab (vehicle-identity channel, Part A of the DNA family).
**Format:** Nygard template (one decision per record, immutable once Accepted).
**Date compiled:** 2026-06-11 — back-filled from the shipped sibling-split rework
(T-RM-2-DNA, T-FX-2, T-FX-5, T-VL-4, T-VL-7).

> These ADRs record decisions already implemented in `vinlab/`. Each captures *why* a
> choice was made, with the task ID that carried it. Future changes supersede an ADR
> with a new one rather than editing it in place.

### ADR: ADR-0001
- **Title**: Offline runtime — bake all reference data into `vinlab/data/`, zero MySQL/network
- **Status**: Accepted

### ADR: ADR-0002
- **Title**: VINLab is a sibling module, not a sub-package of DNALab
- **Status**: Accepted

### ADR: ADR-0003
- **Title**: No cross-lab Python imports — COMLab mirrors `VinDNA`
- **Status**: Accepted

### ADR: ADR-0004
- **Title**: Enum-typed `VinDNA` fields replace bare `str`
- **Status**: Accepted

### ADR: ADR-0005
- **Title**: Single deep air-metering module replaces two parallel switches
- **Status**: Accepted

### ADR: ADR-0006
- **Title**: Data-driven checksum bypass for non-NHTSA markets
- **Status**: Accepted

### ADR: ADR-0007
- **Title**: Cylinder-count heuristic is a gated last resort, never an override
- **Status**: Accepted

### ADR: ADR-0008
- **Title**: Confidence is graded, never fatal — degrade rather than crash
- **Status**: Accepted

### ADR: ADR-0009
- **Title**: SQL isolation — all SQL lives in `db/tecdoc_query.py` (H8)
- **Status**: Accepted

### ADR: ADR-0010
- **Title**: `ChassisNumberError` distinguishes wrong-length input from decode failure
- **Status**: Accepted

---

## Graph relations (explicit)

**ADR_VINLab.md** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
