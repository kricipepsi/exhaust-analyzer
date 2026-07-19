
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0008: Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator · Parent document: ADR_GASLab.md
## ADR-0008: Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator

**Status:** Accepted

**Context.** `CAM_TIMING_RETARDED_MAP` vs `CAM_TIMING_RETARDED_MAF` differ by the engine's air-metering system (Speed-Density/MAP vs MAF). The obvious implementation is a DNA field for the metering system used as a gate.

**Decision.** The cam-timing states carry **no DNA gate**. There is no DNA field for MAF-vs-MAP metering, and adding one purely to gate these faults would introduce a field with no other consumer — a signal/noise violation (ADR-0002). Instead the MAP/MAF distinction rides the **gas-direction discriminator** (Speed-Density tends rich; MAF tends lean), corroborated by OBD trims downstream and confirmed by the idle→2500 RPM behaviour (ADR-0009).

**Consequences.**
- Positive: no orphan DNA field; the split is carried by chemistry the engine already has.
- Positive: keeps the DNA view at 13 fields, all with consumers.
- Negative: the MAP/MAF call rests on gas direction plus the high-idle vector, so it needs `reading_high` to be confident; without it the call is weaker.
- Neutral: full phase confirmation still belongs downstream (CKP/CMP in OBDLab/DTCLab).

**Alternatives considered.**
1. *Add an `air_metering_type` DNA field and gate on it.* Rejected — a field whose only reader is this gate; violates signal/noise.
2. *Emit a generic `CAM_TIMING_RETARDED` and let COMLab split it.* Rejected — pushes the discriminable distinction across the boundary and loses the gas-direction signal GASLab uniquely holds.

**References.** `wiki/CHANGE_v2.1_timing_taxonomy.md`; `GAS_VOCABULARY §3.1`; `resolution.py` cam-timing gates.

---


## Graph relations (explicit)

**ADR-0008: Cam-timing states are not DNA-gated; the MAF/MAP split rides a gas discriminator** DESCRIBES **GASLab ADR v2.1**
**CAM_TIMING_RETARDED_MAP, CAM_TIMING_RETARDED_MAF** GATED_BY **gas-direction discriminator** -- no MAF/MAP DNA field (signal/noise)


