
> **Context:** GASLab PRD v2.1 (2026-06-10) · Module: GASLab · Section: Section 1 — Summary · Parent document: PRD_GASLab.md
## Section 1 — Summary

GASLab is the exhaust gas chemistry analysis module of 4DApp. It accepts one or two 5-gas analyser readings (idle, plus an optional high-idle / 2500 RPM reading) of HC, CO, CO₂, O₂, and NOx, plus a typed vehicle DNA view, computes the Brettschneider lambda as ground truth, gates sample validity, and classifies the reading into one of **34** `ChemicalSignature` values. The output `GasLabPayload` is consumed by COMLab as the chemistry ground-truth layer (L1/L2) of the 4DApp diagnostic pipeline.

---


## Graph relations (explicit)

**Section 1 — Summary** DESCRIBES **GASLab PRD v2.1**
**GASLab** DESCRIBES **5-gas chemistry ground-truth module** -- L1/L2 of 4DApp pipeline
**GasLabPayload** CONSUMES **COMLab** -- chemistry ground-truth input


