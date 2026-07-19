# Architecture Decision Records — GASLab
**Status:** Living index (individual records are immutable once Accepted)
**Version:** 1.0
**Date:** 2026-06-10
**Format:** Nygard template, per `_skills/doc/ADR.md`
**Code baseline:** GASLab v2.1 (34-value surface, dual-RPM input)

This file records the standing architectural decisions that shape GASLab. Records are numbered sequentially and, once **Accepted**, are not edited — a later decision supersedes an earlier one with a new record. Each captures *why*, not *how*; the *how* lives in HLD / LLD / DLD.


*(Table converted to entity blocks — 4dlab-doc-prep Step 2)*

### ADR-0001
- **#**: ADR-0001
- **Decision**: Brettschneider chemistry is ground truth over ECU perception
- **Status**: Accepted

### ADR-0002
- **#**: ADR-0002
- **Decision**: Signal/noise — every schema field needs a named, existing consumer
- **Status**: Accepted

### ADR-0003
- **#**: ADR-0003
- **Decision**: No cross-lab Python imports — mirror types locally
- **Status**: Accepted

### ADR-0004
- **#**: ADR-0004
- **Decision**: A declarative YAML ontology is the single source of fault signatures
- **Status**: Accepted

### ADR-0005
- **#**: ADR-0005
- **Decision**: DNA gates are strict and unconditional, not confidence-weighted
- **Status**: Accepted

### ADR-0006
- **#**: ADR-0006
- **Decision**: Deterministic specificity ranking with catch-alls last
- **Status**: Accepted

### ADR-0007
- **#**: ADR-0007
- **Decision**: Retire `WRONG_VALVE_TIMING`; adopt three `CAM_TIMING_*` states (32→34)
- **Status**: Accepted

### ADR-0008
- **#**: ADR-0008
- **Decision**: Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator
- **Status**: Accepted

### ADR-0009
- **#**: ADR-0009
- **Decision**: Optional high-idle (2500 RPM) reading drives RPM-differential separation
- **Status**: Accepted

### ADR-0010
- **#**: ADR-0010
- **Decision**: Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window
- **Status**: Accepted

### ADR-0011
- **#**: ADR-0011
- **Decision**: `confidence` is carried but gates only the `co_high_idle` override
- **Status**: Accepted


---


> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR_GASLab — Preamble · Parent document: ADR_GASLab.md

## Graph relations (explicit)

**ADR_GASLab — Preamble** DESCRIBES **GASLab ADR v2.1**

