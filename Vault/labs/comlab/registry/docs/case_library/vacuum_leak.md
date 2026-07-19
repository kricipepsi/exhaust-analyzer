---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-vacuum_leak"
implements:
  - "labs/comlab/registry/code/rules/vacuum_leak.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_vacuum_leak_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/vacuum_leak.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: vacuum_leak · Parent document: labs/comlab/registry/corpus_curated.csv
# vacuum_leak
4 cases

### Case: NEW-vacuum_leak-01
- **Description**: Moderate vacuum leak -- lean trims at idle correct at 2500 RPM. No DTC yet.
- **Gas Chemistry**: HC: 25 ppm, CO: 0.05%, CO₂: 13.0%, O₂: 3.0%, NOx: ppm, λ Analyser: 1.08
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8% / 15%, ECU λ: 1.09, MAP: 48 kPa, RPM: 750, ECT: 90°C
- **DTCs**: No DTCs stored
- **Expected Fault**: Vacuum_Leak_Moderate
- **Expected State**: named_fault
- **Confidence Range**: 0.70 – 0.85
- **Reasoning**: HC 25 ppm: clean burn. CO 0.05 pct: near zero. CO2 13.0 pct: depressed by lean burn. O2 3.0 pct: elevated -- unmetered air entering through vacuum leak. lambda 1.08: lean at idle (Brettschneider). LTFT +15 pct STFT +8 pct: ECU adding fuel to compensate for unmetered air at idle. MAP 48 kPa: elevated vs normal 30-40 kPa at hot idle -- manifold can't pull deep vacuum due to leak. lambda_2500 1.01: near stoich at 2500 RPM -- fixed-size leak contributes proportionally less air at lower manifold vacuum. RPM-dependent trim pattern is the vacuum_leak differentiator vs persistent lean_condition.

### Case: NEW-vacuum_leak-02
- **Description**: Small vacuum leak with P0171 DTC triggered. Trims elevated at idle, DTC confirms lean.
- **Gas Chemistry**: HC: 15 ppm, CO: 0.02%, CO₂: 14.0%, O₂: 1.5%, NOx: ppm, λ Analyser: 1.04
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5% / 12%, ECU λ: 1.05, MAP: 44 kPa, RPM: 800, ECT: 95°C
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_DTC
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.80
- **Reasoning**: HC 15 ppm: clean burn. CO 0.02 pct: near zero. CO2 14.0 pct: slightly depressed. O2 1.5 pct: mildly elevated -- small vacuum leak. lambda 1.04: marginally lean at idle. LTFT +12 pct STFT +5 pct: moderate trim correction -- ECU compensating for small unmetered air source. MAP 44 kPa: slightly elevated (10 pct margin over 40 kPa normal ceiling). DTC P0171: ECU has logged system-too-lean, confirming the persistent lean condition. lambda_2500 1.00: fully corrected at 2500 RPM -- the leak is proportionally small enough that normal airflow at cruise overwhelms it.

### Case: NEW-vacuum_leak-03
- **Description**: Large-bore vacuum leak (brake booster / PCV disconnect). Very high MAP at idle, extreme trims.
- **Gas Chemistry**: HC: 35 ppm, CO: 0.08%, CO₂: 11.5%, O₂: 5.0%, NOx: ppm, λ Analyser: 1.15
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20% / 25%, ECU λ: 1.18, MAP: 60 kPa, RPM: 850, ECT: 88°C
- **DTCs**: No DTCs stored
- **Expected Fault**: Vacuum_Leak_Large_Bore
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.80
- **Reasoning**: HC 35 ppm: slightly elevated -- incipient lean misfire. CO 0.08 pct: still near zero. CO2 11.5 pct: substantially depressed -- severe lean combustion deficit. O2 5.0 pct: severely elevated -- massive unmetered air entry. lambda 1.15: grossly lean at idle. LTFT +25 pct STFT +20 pct: ECU at near-maximum fuel trim trying to compensate. MAP 60 kPa: near-atmospheric at idle (normal is 30-40 kPa) -- manifold vacuum near collapse, classic large-bore leak (brake booster hose disconnect / PCV valve stuck open). lambda_2500 1.03: still slightly lean at 2500 RPM -- leak is so large it still contributes even at lower manifold vacuum. The extreme MAP elevation at idle is the GATING differentiator for VL-003.

### Case: NEW-vacuum_leak-04
- **Description**: Moderate vacuum leak, V-engine bank 2 only. P0174 DTC (bank 2 lean), bank 1 trims normal.
- **Gas Chemistry**: HC: 20 ppm, CO: 0.03%, CO₂: 13.5%, O₂: 2.5%, NOx: ppm, λ Analyser: 1.06
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2% / 3%, Trims B2 (ST/LT): 10% / 18%, ECU λ: 1.07, MAP: 50 kPa, RPM: 700, ECT: 92°C
- **DTCs**: P0174
- **Expected Fault**: Vacuum_Leak_Bank2
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 20 ppm: clean burn. CO 0.03 pct: near zero. CO2 13.5 pct: depressed by lean burn on bank 2. O2 2.5 pct: elevated -- unmetered air on one bank. lambda 1.06: lean at idle. LTFT B2 +18 pct STFT B2 +10 pct: bank 2 trims elevated while bank 1 trims near zero (LTFT +3 pct STFT +2 pct) -- the asymmetry isolates the leak to bank 2. MAP 50 kPa: elevated at idle (25 pct margin over 40 kPa normal ceiling). DTC P0174: bank-2-only lean code confirms the asymmetry. lambda_2500 1.01: corrects at 2500 RPM. Single-bank trim elevation + RPM-dependent correction = intake manifold gasket leak at bank 2 runner.


## Graph relations (explicit)

**labs/comlab/registry/rules/vacuum_leak.json** VERIFIES **NEW-vacuum_leak-01**
**labs/comlab/registry/rules/vacuum_leak.json** VERIFIES **NEW-vacuum_leak-02**
**labs/comlab/registry/rules/vacuum_leak.json** VERIFIES **NEW-vacuum_leak-03**
**labs/comlab/registry/rules/vacuum_leak.json** VERIFIES **NEW-vacuum_leak-04**
