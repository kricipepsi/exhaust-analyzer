# BDD — GASLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-10
**Authored from:** `_skills/doc/BDD.md` (Gherkin Given/When/Then, declarative, one behaviour per scenario)
**Code baseline:** GASLab v2.1 (34-value surface, dual-RPM input)

These are **executable specifications** for GASLab's observable behaviour at the `gaslab.process.process()` boundary. Each scenario is declarative — it states what the system does for a given exhaust reading and DNA view, never how. Every feature names the test module that exercises it, so the scenarios stay honest against `pytest`. Numeric values are illustrative of the documented bands (see LLD §4, §6); they are not new thresholds.

A shared vocabulary used throughout:

- **A reading** = the five analyser inputs (HC ppm, CO/CO₂/O₂ vol%, NOx ppm).
- **A high-idle reading** = an optional second reading taken at 2500 RPM (`reading_high`).
- **A DNA view** = the 13-field `GasLabDnaView` slice for the vehicle.
- **The verdict** = `(chemical_state, sample_validity)` carried in `GasLabPayload`.

---


> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: BDD_GASLab — Preamble · Parent document: BDD_GASLab.md

## Graph relations (explicit)

**BDD_GASLab — Preamble** DESCRIBES **GASLab BDD v2.1**

