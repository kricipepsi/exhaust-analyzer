> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 8 Non-Functional Requirements · Parent document: HLD_OBDLab.md

## 8. Non-Functional Requirements

### Entity: NFR targets

- **Pipeline latency** — < 50 ms warm idle, HIGH DNA
- **Sensor bounds drift** — 0 drift between `physical_sensor_bounds.json` and `OBDLab_KG_Wiki.md §3.1`
- **Import isolation** — 0 cross-lab Python imports
- **HIGH_IDLE_LOAD token** — 0 occurrences in `obdlab/` (superseded by `REGULATORY_HIGH_IDLE`/`STRESS_IDLE`)
- **Numeric literals** — every literal in `obdlab/` carries a `# wiki:` citation comment
- **Signal/noise** — every payload field has a named, existing-or-proposed consumer

## Graph relations (explicit)

**test_sensor_bounds.py** VERIFIES **physical_sensor_bounds.json ↔ OBDLab_KG_Wiki.md §3.1** (0 drift)
**test_dna_view.py** VERIFIES **import isolation** (0 cross-lab imports)
**test_vocabulary.py** VERIFIES **HIGH_IDLE_LOAD absent** (0 occurrences)
**code-review gate** VERIFIES **every numeric literal carries # wiki: citation**
**signal/noise rule** VERIFIES **every payload field has named consumer** (HLD §7)
