---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-overheating"
implements:
  - "labs/comlab/registry/code/rules/overheating.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_overheating_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/overheating.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: overheating · Parent document: labs/comlab/registry/corpus_curated.csv
# overheating
4 cases

### Case: NEW-overheating-01
- **Description**: Thermostat stuck partially closed - moderate overheat, ECU has detected and elevated idle to ECU_COOLING_IDLE target; no DTC yet.
- **Gas Chemistry**: HC: 15 ppm, CO: 0.15%, CO₂: 14.8%, O₂: 0.4%, NOx: 550 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: MAP: 32 kPa, RPM: 1050, ECT: 112°C
- **DTCs**: No DTCs stored
- **Expected Fault**: overheating_thermostat_stuck
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: ECT 112C exceeds OVERHEATING_THRESHOLD (108C); RPM 1050 = ECU_COOLING_IDLE band. NOx 550 ppm below HIGH_COMBUSTION_TEMP (1500 ppm) - OBD-primary.

### Case: NEW-overheating-02
- **Description**: Thermostat failure - P0128 DTC stored but ECU has not (yet) elevated idle; ECT at OVERHEATING_THRESHOLD boundary.
- **Gas Chemistry**: HC: 10 ppm, CO: 0.10%, CO₂: 15.0%, O₂: 0.3%, NOx: 400 ppm, λ Analyser: 1.00
- **OBD / Air / Engine**: MAP: 30 kPa, RPM: 950, ECT: 108°C
- **DTCs**: P0128
- **Expected Fault**: overheating_thermostat_p0128
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: P0128 gating; ECT 108C = OVERHEATING_THRESHOLD. RPM 950 NORMAL_HOT_IDLE - DTC stored but no cooling-idle yet.

### Case: NEW-overheating-03
- **Description**: Head gasket failure - internal coolant leak; SEVERE_OVERHEAT ECT plus P0117 from sensor in steam pockets; gas shows steam-quench pattern.
- **Gas Chemistry**: HC: 30 ppm, CO: 0.25%, CO₂: 12.5%, O₂: 2.0%, NOx: 200 ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: MAP: 35 kPa, RPM: 1100, ECT: 120°C
- **DTCs**: P0117
- **Expected Fault**: overheating_head_gasket
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: ECT 120C = CRITICAL_OVERHEAT; P0117 suggestive of internal coolant loss. Gas: CO2 displaced, NOx suppressed, HC raised - COOLANT_LEAK_INTERNAL fingerprint per GAS_WIKI 7.32.

### Case: NEW-overheating-04
- **Description**: Electric radiator fan failure - ECT elevated above NORMAL_OPERATING but ECU has not detected (sensor misses radiator-side hot spot); no DTC, no idle elevation.
- **Gas Chemistry**: HC: 8 ppm, CO: 0.08%, CO₂: 15.1%, O₂: 0.2%, NOx: 380 ppm, λ Analyser: 1.00
- **OBD / Air / Engine**: MAP: 30 kPa, RPM: 850, ECT: 106°C
- **DTCs**: No DTCs stored
- **Expected Fault**: overheating_fan_failure
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: ECT 106C in ELEVATED_TEMP band; RPM 850 NORMAL_HOT_IDLE - undetected fan failure. RPM lt 1000 discriminates from OV-001.


## Graph relations (explicit)

**labs/comlab/registry/rules/overheating.json** VERIFIES **NEW-overheating-01**
**labs/comlab/registry/rules/overheating.json** VERIFIES **NEW-overheating-02**
**labs/comlab/registry/rules/overheating.json** VERIFIES **NEW-overheating-03**
**labs/comlab/registry/rules/overheating.json** VERIFIES **NEW-overheating-04**
