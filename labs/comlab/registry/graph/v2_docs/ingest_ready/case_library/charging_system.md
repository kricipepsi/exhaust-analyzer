---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-charging_system
implements:
- labs/comlab/registry/rules/charging_system.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_charging_system_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/charging_system.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: charging_system · Parent document: labs/comlab/registry/corpus_curated.csv
# charging_system
3 cases

### Case: NEW-charging_system-01
- **Description**: Charging system: system voltage low (P0562). Battery 11.8 V at idle. Clean idle gas (NORMAL); DTC is the diagnostic signal. Battery voltage is not captured in schema.
- **Gas Chemistry**: HC: 8 ppm, CO: 0.08%, CO₂: 15.0%, O₂: 0.3%, NOx: 380 ppm, λ Analyser: 1.00
- **OBD / Air / Engine**: MAP: 32 kPa, RPM: 850, ECT: 88°C
- **DTCs**: P0562
- **Expected Fault**: 
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: 

### Case: NEW-charging_system-02
- **Description**: Charging system: system voltage high / overcharging (P0563). Battery 15.2 V at idle (voltage regulator failure). Clean idle gas (NORMAL); DTC is the diagnostic signal. Battery voltage is not captured in schema.
- **Gas Chemistry**: HC: 10 ppm, CO: 0.10%, CO₂: 14.9%, O₂: 0.4%, NOx: 350 ppm, λ Analyser: 1.00
- **OBD / Air / Engine**: MAP: 33 kPa, RPM: 880, ECT: 92°C
- **DTCs**: P0563
- **Expected Fault**: 
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: 

### Case: NEW-charging_system-03
- **Description**: Charging-induced ghost misfire: ECU reports P0300 but gas chemistry NORMAL. Battery 11.5 V bouncing 0.4 V. Charging DTC + clean chemistry is the discriminator from real misfire. Battery voltage is not captured in schema.
- **Gas Chemistry**: HC: 12 ppm, CO: 0.10%, CO₂: 14.8%, O₂: 0.4%, NOx: 320 ppm, λ Analyser: 1.00
- **OBD / Air / Engine**: MAP: 33 kPa, RPM: 830, ECT: 90°C
- **DTCs**: P0562; P0300
- **Expected Fault**: 
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.90
- **Reasoning**: 


## Graph relations (explicit)

**labs/comlab/registry/rules/charging_system.json** VERIFIES **NEW-charging_system-01**
**labs/comlab/registry/rules/charging_system.json** VERIFIES **NEW-charging_system-02**
**labs/comlab/registry/rules/charging_system.json** VERIFIES **NEW-charging_system-03**
