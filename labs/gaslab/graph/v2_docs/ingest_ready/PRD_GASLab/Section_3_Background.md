
> **Context:** GASLab PRD v2.1 (2026-06-10) · Module: GASLab · Section: Section 3 — Background · Parent document: PRD_GASLab.md
## Section 3 — Background

**Context.** A 5-gas exhaust analyser measures CO, HC, CO₂, O₂, and NOx in the exhaust stream. These five gases encode the combustion event more completely than the ECU alone. The Brettschneider equation (1983) derives an air-fuel lambda value from this chemistry that is independent of the ECU's fuel-trim perception.

**Why now.** The 34-fault ontology (`gas_lab_ontology.yaml`, mirrored by the `ChemicalSignature` enum) is complete. The v2.1 timing-taxonomy revision retired the single `WRONG_VALVE_TIMING` value and replaced it with three system-specific cam-timing states (`CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED`), seating five timing states (two ignition + three cam) as first-class entries. A synthetic boundary-permutation grid plus a generative property suite (boundary / combinatorial / fuzz / noise / overlap) covers the fault signature space.

**What recently became possible.** Adding the optional **high-idle (2500 RPM) reading** unlocked RPM-differential discriminators that separate faults whose single-point idle signatures overlap — cam timing vs vacuum lean, weak vs dead catalyst, and the mechanical-wear family leaves — without inventing DNA fields that would have no consumer.

---


## Graph relations (explicit)

**Section 3 — Background** DESCRIBES **GASLab PRD v2.1**
**ChemicalSignature** SUPERSEDES **WRONG_VALVE_TIMING** -- v2.1 timing taxonomy, 32->34
**reading_high** CONSUMES **resolution.apply_differentiators()** -- RPM-differential discriminators


