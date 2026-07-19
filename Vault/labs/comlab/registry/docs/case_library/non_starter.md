---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-non_starter"
implements:
  - "labs/comlab/registry/code/rules/non_starter.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_non_starter_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/non_starter.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: non_starter · Parent document: labs/comlab/registry/corpus_curated.csv
# non_starter
4 cases

### Case: REAL-001
- **Description**: Cranking only; near-zero combustion
- **Gas Chemistry**: HC: 20200.0 ppm, CO: 0.006%, CO₂: 0.16%, O₂: 19.73%, NOx: 14.0 ppm, λ Analyser: 1.14
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: No_Spark_Coil_Failure
- **Expected State**: warning
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 20200 ppm: extreme — almost always mechanical (rings, valve sealing) or hard ignition fault (>2000 ppm). CO 0.006%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 0.16%: atmospheric — no combustion product (cranking / probe in air). O2 19.73%: severe lean / large misfire / air leak (>4%). NOx 14 ppm: low — rich quench or idle without thermal load. λ 1.14: lean (≥1.05) — Brettschneider chemistry; OBD λ=0 (Δ=+1.14) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: REAL-003
- **Description**: Extreme cold enrichment; flood
- **Gas Chemistry**: HC: 26710.0 ppm, CO: 3.24%, CO₂: 1.16%, O₂: 14.54%, NOx: 30.0 ppm, λ Analyser: 0.63
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Rich_No_Start_ECT_Sensor
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 26710 ppm: extreme — almost always mechanical (rings, valve sealing) or hard ignition fault (>2000 ppm). CO 3.24%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 1.16%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 14.54%: severe lean / large misfire / air leak (>4%). NOx 30 ppm: low — rich quench or idle without thermal load. λ 0.63: rich (≤0.95) — chemistry says excess fuel; OBD λ=0 (Δ=+0.63) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: case_006
- **Description**: Non-starter with no fuel delivery (cranking)
- **Gas Chemistry**: HC: 0.0 ppm, CO: 0.0%, CO₂: 0.04%, O₂: 20.9%, NOx: 0.0 ppm, λ Analyser: 2.5
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 200.0
- **DTCs**: P0230
- **Expected Fault**: ns_no_fuel
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 0: no fuel reaching the chamber — nothing to leak as raw HC. CO 0%: no combustion, no partial-burn product. CO2 0.04%: atmospheric — nothing burned. O2 20.9%: ambient air, unconsumed because no spark/fuel reaction. NOx 0 ppm: no combustion temperature. λ >2: chemistry confirms zero combustion; routes to non-starter no-fuel pipeline (P0230 corroborates).

### Case: case_007
- **Description**: Non-starter lean no-start (spark, weak fuel)
- **Gas Chemistry**: HC: 300.0 ppm, CO: 0.02%, CO₂: 4.0%, O₂: 16.0%, NOx: 10.0 ppm, λ Analyser: 1.35
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 300.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ns_lean_no_start
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 300 ppm: some fuel reaches the chamber but barely lights. CO 0.02%: almost no rich product — combustion never sustains. CO2 4.0%: far below normal because most charges fail to ignite. O2 16.0%: most of the intake air comes straight through. NOx 10 ppm: too cold to form. λ 1.35: extremely lean — lean-misfire no-start; non-starter pipeline picks this up without a fuel-pump DTC.


## Graph relations (explicit)

**labs/comlab/registry/rules/non_starter.json** VERIFIES **REAL-001**
**labs/comlab/registry/rules/non_starter.json** VERIFIES **REAL-003**
**labs/comlab/registry/rules/non_starter.json** VERIFIES **case_006**
**labs/comlab/registry/rules/non_starter.json** VERIFIES **case_007**
