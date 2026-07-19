---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-mechanical_wear"
implements:
  - "labs/comlab/registry/code/rules/mechanical_wear.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_mechanical_wear_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/mechanical_wear.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: mechanical_wear · Parent document: labs/comlab/registry/corpus_curated.csv
# mechanical_wear
11 cases

### Case: CSV-117
- **Description**: Snap-throttle required: HC spikes to ~950 on snap; idle=normal; oil burn-off
- **Gas Chemistry**: HC: 950.0 ppm, CO: 0.6%, CO₂: 12.5%, O₂: 1.4%, NOx: 70.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Valve_Stem_Seals_SnapThrottle
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 950 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.4%: typical pre-cat residual (0.5–1.5%). NOx 70 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-118
- **Description**: Worn valve stem seals; HC plume on snap-throttle; bluish smoke
- **Gas Chemistry**: HC: 1100.0 ppm, CO: 0.7%, CO₂: 12.2%, O₂: 1.5%, NOx: 65.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Valve_Stem_Seals_SnapThrottle
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 1100 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.7%: mild rich / pre-cat normal (0.5–1.5%). CO2 12.2%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 65 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: CSV-119
- **Description**: Coolant in combustion; HC>900 + O2>3 + white sweet smoke; CO2 depressed
- **Gas Chemistry**: HC: 950.0 ppm, CO: 0.7%, CO₂: 11.0%, O₂: 3.2%, NOx: 35.0 ppm, λ Analyser: 1.1
- **OBD / Air / Engine**: Trims B1 (ST/LT): 6.0% / 4.0%, ECU λ: 1.08
- **DTCs**: No DTCs stored
- **Expected Fault**: Head_Gasket_Failure_V2
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 950 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.7%: mild rich / pre-cat normal (0.5–1.5%). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.2%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1.1: lean (≥1.05) — Brettschneider chemistry.

### Case: CSV-120
- **Description**: Severe HG breach; coolant burning in chamber; cyl-pressure cross-talk
- **Gas Chemistry**: HC: 1100.0 ppm, CO: 0.9%, CO₂: 10.8%, O₂: 3.5%, NOx: 28.0 ppm, λ Analyser: 1.12
- **OBD / Air / Engine**: Trims B1 (ST/LT): 7.0% / 5.0%, ECU λ: 1.1
- **DTCs**: No DTCs stored
- **Expected Fault**: Head_Gasket_Failure_V2
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 1100 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.9%: mild rich / pre-cat normal (0.5–1.5%). CO2 10.8%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 28 ppm: low — rich quench or idle without thermal load. λ 1.12: lean (≥1.05) — Brettschneider chemistry.

### Case: EXT-222
- **Description**: Low compression on 3 cylinders; acceptable idle, but under load (FF: 3100 RPM, 78% LOAD) CO2 drops, HC rises. FF confirms load-dependent fault
- **Gas Chemistry**: HC: 450.0 ppm, CO: 0.5%, CO₂: 12.5%, O₂: 1.5%, NOx: 45.0 ppm, λ Analyser: 1.04
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 3.0%, ECU λ: 1.05, MAF: - g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Mechanical_Wear_Low_Compression_Multi_Cylinder_FF_HighLoad
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 450 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 45 ppm: low — rich quench or idle without thermal load. λ 1.04: borderline lean (1.03–1.05).

### Case: EXT-223
- **Description**: Worn rings; HC elevated at idle. FF=idle (850 RPM, 22% LOAD). At 2500 RPM HC drops as ring seal improves with higher cylinder pressure. Oil consumption confirmed
- **Gas Chemistry**: HC: 800.0 ppm, CO: 0.8%, CO₂: 12.0%, O₂: 1.8%, NOx: 35.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0, MAF: - g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Mechanical_Wear_Worn_Piston_Rings_FF_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 800 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.8%: mild rich / pre-cat normal (0.5–1.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1.05: lean (≥1.05) — Brettschneider chemistry.

### Case: EXT-224
- **Description**: Head gasket breach between cylinders 3-4; combustion pressure cross-talk. FF captured at 2200 RPM cruise. Coolant consumption + white smoke on cold start
- **Gas Chemistry**: HC: 950.0 ppm, CO: 1.2%, CO₂: 10.5%, O₂: 3.2%, NOx: 30.0 ppm, λ Analyser: 1.17
- **OBD / Air / Engine**: Trims B1 (ST/LT): 7.0% / 4.0%, ECU λ: 1.1, MAF: - g/s
- **DTCs**: P0300
- **Expected Fault**: Head_Gasket_Failure_FF_Cruise
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 950 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 1.2%: mild rich / pre-cat normal (0.5–1.5%). CO2 10.5%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 3.2%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1.17: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: MECH-001
- **Description**: HC persists at 2500rpm; oil burn
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.8%, CO₂: 13.5%, O₂: 1.2%, NOx: 80.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Worn_Piston_Rings_Valve_Seals
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.8%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 80 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: MECH-002
- **Description**: Coolant in combustion; CO2 depressed
- **Gas Chemistry**: HC: 800.0 ppm, CO: 0.9%, CO₂: 11.5%, O₂: 2.8%, NOx: 40.0 ppm, λ Analyser: 1.04
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 3.0%, ECU λ: 1.05
- **DTCs**: No DTCs stored
- **Expected Fault**: Head_Gasket_Failure
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 800 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.9%: mild rich / pre-cat normal (0.5–1.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.04: borderline lean (1.03–1.05).

### Case: MECH-006
- **Description**: Weak cylinders; CO2<12%
- **Gas Chemistry**: HC: 550.0 ppm, CO: 0.8%, CO₂: 11.8%, O₂: 3.2%, NOx: 25.0 ppm, λ Analyser: 1.09
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 6.0%, ECU λ: 1.08
- **DTCs**: No DTCs stored
- **Expected Fault**: Low_Compression_Multi_Cylinder
- **Expected State**: named_fault
- **Confidence Range**: 0.72 – 0.92
- **Reasoning**: HC 550 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.8%: mild rich / pre-cat normal (0.5–1.5%). CO2 11.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.2%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1.09: lean (≥1.05) — Brettschneider chemistry.

### Case: case_044
- **Description**: High HC with normal CO and λ≈1.0 (oil consumption / rings)
- **Gas Chemistry**: HC: 2500.0 ppm, CO: 0.2%, CO₂: 13.5%, O₂: 1.0%, NOx: 150.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: oil_burning
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.65
- **Reasoning**: HC 2500 ppm: extremely high — raw oil hydrocarbons enter the chamber and exit unburned. CO 0.2%: low — mixture itself is correct. CO2 13.5%: modestly depressed by the parasitic HC load. O2 1.0%: typical. NOx 150 ppm: moderate. λ 1.00: chemistry stoich because oil HC is small versus air mass; high HC + normal CO + λ≈1 is the rings/valve-seal oil-burn signature.


## Graph relations (explicit)

**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **CSV-117**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **CSV-118**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **CSV-119**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **CSV-120**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **EXT-222**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **EXT-223**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **EXT-224**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **MECH-001**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **MECH-002**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **MECH-006**
**labs/comlab/registry/rules/mechanical_wear.json** VERIFIES **case_044**
