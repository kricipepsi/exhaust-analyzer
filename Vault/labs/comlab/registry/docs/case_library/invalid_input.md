---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-invalid_input"
implements:
  - "labs/comlab/registry/code/rules/invalid_input.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_invalid_input_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/invalid_input.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: invalid_input · Parent document: labs/comlab/registry/corpus_curated.csv
# invalid_input
2 cases

### Case: CASE-046
- **Description**: CO2 exceeds physical maximum (~16%); analyzer calibration drift or NDIR saturation; recalibrate with reference gas; all readings suspect
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.5%, CO₂: 19.5%, O₂: 0.1%, NOx: 40.0 ppm, λ Analyser: 
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: INVALID_CO2_Over_Range_Analyzer_Calibration_Drift
- **Expected State**: invalid_input
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: CO2 reading exceeds the ~16% theoretical maximum for gasoline (master_gas_guide §6 sanity rail). NDIR bench calibration drift or analyser saturation; recalibrate against reference gas before any diagnosis. All gas channels are suspect until calibration is verified.

### Case: CSV-081
- **Description**: INTENTIONAL INVALID sentinel
- **Gas Chemistry**: HC: 0.0 ppm, CO: 0.01%, CO₂: 20.5%, O₂: 0.0%, NOx: 0.0 ppm, λ Analyser: 0.9998
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: INVALID_CO2_OVER_RANGE
- **Expected State**: invalid_input
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: CO2 reading exceeds the ~16% theoretical maximum for gasoline (master_gas_guide §6 sanity rail). NDIR bench calibration drift or analyser saturation; recalibrate against reference gas before any diagnosis. All gas channels are suspect until calibration is verified.


## Graph relations (explicit)

**labs/comlab/registry/rules/invalid_input.json** VERIFIES **CASE-046**
**labs/comlab/registry/rules/invalid_input.json** VERIFIES **CSV-081**
