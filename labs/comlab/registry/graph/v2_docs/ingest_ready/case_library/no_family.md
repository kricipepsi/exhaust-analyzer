---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-invalid_input
implements:
- labs/comlab/registry/rules/invalid_input.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_invalid_input_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/no_family.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: (no family) · Parent document: labs/comlab/registry/corpus_curated.csv
# (no family)
1 cases

### Case: case_011
- **Description**: Garbage DTC string (invalid input)
- **Gas Chemistry**: HC: 50.0 ppm, CO: 0.1%, CO₂: 14.0%, O₂: 1.5%, NOx: 100.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: GARBAGE
- **Expected Fault**: invalid_input
- **Expected State**: invalid_input
- **Reasoning**: HC 50 ppm: normal idle. CO 0.1%: normal. CO2 14.0%: healthy. O2 1.5%: at the upper edge of normal. NOx 100 ppm: typical. λ 1.01: stoich. Gases are clean; the test exists to verify the validator rejects an unrecognised DTC string before any inference runs.


## Graph relations (explicit)

**labs/comlab/registry/rules/invalid_input.json** VERIFIES **case_011**
