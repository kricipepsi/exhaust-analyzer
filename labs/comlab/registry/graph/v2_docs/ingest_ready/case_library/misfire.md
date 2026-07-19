---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-misfire
implements:
- labs/comlab/registry/rules/misfire.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_misfire_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/misfire.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: misfire · Parent document: labs/comlab/registry/corpus_curated.csv
# misfire
44 cases

### Case: CASE-021
- **Description**: FF ECT=35°C gates diagnosis to cold-start valve sticking; HC=1200 at idle; warm-up clears fault
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.8%, CO₂: 11.5%, O₂: 1.5%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 3.0%, ECU λ: 1.0, MAF: 3.0 g/s
- **DTCs**: P0300
- **Expected Fault**: Cold_Start_Misfire_Sticky_Valve_ECT35
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.8%: mild rich / pre-cat normal (0.5–1.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-024
- **Description**: Coil-4 breaks down at high load/temp; FF=4500RPM 85% LOAD confirms load-dependent fault; HC+O2 signature of dead cylinder
- **Gas Chemistry**: HC: 800.0 ppm, CO: 0.4%, CO₂: 12.0%, O₂: 4.0%, NOx: 35.0 ppm, λ Analyser: 1.17
- **OBD / Air / Engine**: Trims B1 (ST/LT): 12.0% / 8.0%, ECU λ: 1.15, MAF: 3.5 g/s
- **DTCs**: P0304
- **Expected Fault**: High_Load_Ignition_Coil_Breakdown_P0304
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 800 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.4%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1.17: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CASE-033
- **Description**: GDI injectors spray directly; no port wash; carbon on intake valves soaks cold-start fuel; FF ECT=25°C gates to cold mechanical fault
- **Gas Chemistry**: HC: 850.0 ppm, CO: 0.6%, CO₂: 12.0%, O₂: 1.5%, NOx: 40.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 3.0%, ECU λ: 1.0, MAF: 3.2 g/s
- **DTCs**: P0300
- **Expected Fault**: GDI_Intake_Valve_Carbon_Cold_Misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 850 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03).

### Case: CASE-038
- **Description**: GDI rail pressure=2MPa (target 5MPa); insufficient atomisation; lean misfire; HC=650 O2=3.8 = dead-cylinder signature; P0300
- **Gas Chemistry**: HC: 650.0 ppm, CO: 0.3%, CO₂: 11.5%, O₂: 3.8%, NOx: 25.0 ppm, λ Analyser: 1.22
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 15.0%, ECU λ: 1.18, MAF: 3.5 g/s
- **DTCs**: P0300
- **Expected Fault**: GDI_Fuel_Rail_Pressure_Drift_Lean_Misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 650 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.3%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1.22: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-022
- **Description**: HC>>1000 + O2 = misfire
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.5%, CO₂: 10.0%, O₂: 5.0%, NOx: 20.0 ppm, λ Analyser: 1.25
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 5.0%, ECU λ: 1.2
- **DTCs**: P0302
- **Expected Fault**: Mechanical_Misfire_Spark_Plug
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 5%: severe lean / large misfire / air leak (>4%). NOx 20 ppm: low — rich quench or idle without thermal load. λ 1.25: lean (≥1.05) — Brettschneider chemistry.

### Case: CSV-052
- **Description**: Gas misfire; OBD count=0
- **Gas Chemistry**: HC: 500.0 ppm, CO: 0.02%, CO₂: 15.5%, O₂: 4.5%, NOx: 10.0 ppm, λ Analyser: 1.2
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ECU_Misfire_Blindness
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 500 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 10 ppm: low — rich quench or idle without thermal load. λ 1.2: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.20) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-066
- **Description**: Perfect gas; P0300 ECU hallucination
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Electrical_Noise
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-101
- **Description**: One-cylinder dead; HC>400 O2>3 P0301; trims slightly long correction
- **Gas Chemistry**: HC: 650.0 ppm, CO: 0.3%, CO₂: 12.5%, O₂: 3.5%, NOx: 30.0 ppm, λ Analyser: 1.1
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 4.0%, ECU λ: 1.1
- **DTCs**: P0301
- **Expected Fault**: Misfire_Physical_Single_Cylinder
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 650 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.3%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1.1: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-102
- **Description**: Cyl-3 misfire; ignition coil fail; classic single-cyl signature
- **Gas Chemistry**: HC: 800.0 ppm, CO: 0.4%, CO₂: 12.0%, O₂: 3.8%, NOx: 25.0 ppm, λ Analyser: 1.12
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 6.0%, ECU λ: 1.12
- **DTCs**: P0303
- **Expected Fault**: Misfire_Physical_Single_Cylinder
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 800 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.4%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1.12: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-103
- **Description**: Random multi-cyl misfire; HC>1k + O2>5 = severe ignition fault
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.5%, CO₂: 10.5%, O₂: 5.5%, NOx: 18.0 ppm, λ Analyser: 1.22
- **OBD / Air / Engine**: Trims B1 (ST/LT): 15.0% / 8.0%, ECU λ: 1.2
- **DTCs**: P0300
- **Expected Fault**: Misfire_Physical_Multi_Cylinder
- **Expected State**: named_fault
- **Confidence Range**: 0.78 – 0.98
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10.5%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 5.5%: severe lean / large misfire / air leak (>4%). NOx 18 ppm: low — rich quench or idle without thermal load. λ 1.22: lean (≥1.05) — Brettschneider chemistry.

### Case: CSV-104
- **Description**: Multi-cyl misfire under load; coil pack failure
- **Gas Chemistry**: HC: 1500.0 ppm, CO: 0.6%, CO₂: 9.8%, O₂: 6.0%, NOx: 12.0 ppm, λ Analyser: 1.27
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 10.0%, ECU λ: 1.25
- **DTCs**: P0300
- **Expected Fault**: Misfire_Physical_Multi_Cylinder
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1500 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 9.8%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 6%: severe lean / large misfire / air leak (>4%). NOx 12 ppm: low — rich quench or idle without thermal load. λ 1.27: lean (≥1.05) — Brettschneider chemistry.

### Case: CSV-105
- **Description**: Misfire visible in gas (HC+O2) but ECU misfire counter=0; CKP tooth wear
- **Gas Chemistry**: HC: 450.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 3.2%, NOx: 22.0 ppm, λ Analyser: 1.12
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Misfire_ECU_Blind
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 450 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 3.2%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 22 ppm: low — rich quench or idle without thermal load. λ 1.12: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.12) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-106
- **Description**: Gas-evident misfire; ECU blind; reluctor-ring corrosion suspected
- **Gas Chemistry**: HC: 380.0 ppm, CO: 0.08%, CO₂: 13.0%, O₂: 3.5%, NOx: 18.0 ppm, λ Analyser: 1.13
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Misfire_ECU_Blind
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 380 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 18 ppm: low — rich quench or idle without thermal load. λ 1.13: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.13) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: CSV-107
- **Description**: Perfect gas; P0300 + 70 misfire counts = alternator ripple ghost
- **Gas Chemistry**: HC: 8.0 ppm, CO: 0.06%, CO₂: 15.4%, O₂: 0.15%, NOx: 25.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 1.0%, ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: Misfire_Ghost
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 8 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.4%: at or near the efficient ceiling (≥14.5% with cat). O2 0.15%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-108
- **Description**: Pristine combustion; ECU hallucinating misfires; loose engine ground
- **Gas Chemistry**: HC: 6.0 ppm, CO: 0.04%, CO₂: 15.5%, O₂: 0.1%, NOx: 22.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): -1.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: Misfire_Ghost
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 6 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.04%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 22 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: ECU-007
- **Description**: Perfect gas; alternator ripple
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: ECU_Ghost_Misfire_Hallucination
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: ECU-008
- **Description**: Misfire in gas; ECU 0 misfires
- **Gas Chemistry**: HC: 500.0 ppm, CO: 0.02%, CO₂: 15.5%, O₂: 4.5%, NOx: 10.0 ppm, λ Analyser: 1.2
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ECU_Misfire_Blindness_CKP
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 500 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 10 ppm: low — rich quench or idle without thermal load. λ 1.2: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.20) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: EXP-N016
- **Description**: Dual-mass flywheel play; CKP sees speed jitter; P0300 hallucination
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.06%, CO₂: 15.4%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: Misfire_Ghost_Loose_Flywheel
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.4%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N021
- **Description**: Severe vac leak triggers misfire; truth=rich (0.95); ECU sees lean (1.25)
- **Gas Chemistry**: HC: 1400.0 ppm, CO: 2.5%, CO₂: 11.0%, O₂: 2.5%, NOx: 40.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 15.0%, ECU λ: 1.25
- **DTCs**: P0171
- **Expected Fault**: Lean_Misfire_Feedback_Death_Spiral
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 1400 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 2.5%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.5%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.95: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.25 (Δ=-0.30) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: EXT-225
- **Description**: P0300 set at cold start (FF: ECT=20°C, RPM=800). Engine stumble during cold enrichment. Gas perfect once warm. FF cold-ECT gates diagnosis away from mechanical misfire
- **Gas Chemistry**: HC: 120.0 ppm, CO: 0.5%, CO₂: 13.5%, O₂: 0.8%, NOx: 80.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 1.0%, ECU λ: 1.0, MAF: - g/s
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Cold_ECT_FF
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 120 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 80 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03).

### Case: EXT-226
- **Description**: P0300 set at highway cruise (FF: 3200 RPM, 55% LOAD, 80 km/h). Gas perfect. FF highway-speed gates diagnosis toward electrical noise, away from mechanical
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.05%, CO₂: 15.4%, O₂: 0.2%, NOx: 25.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: - g/s
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Highway_FF
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.4%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXT-228
- **Description**: P0300 from loose engine ground strap causing CKP signal noise. FF voltage=13.5V (normal), but oscilloscope confirms CKP jitter. Gas perfect. O2 cross-counts healthy at 18/10s
- **Gas Chemistry**: HC: 8.0 ppm, CO: 0.06%, CO₂: 15.5%, O₂: 0.15%, NOx: 22.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Loose_Engine_Ground_Voltage_Droop
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 8 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.15%: low — rich consumed the oxygen, or perfect stoich. NOx 22 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXT-234
- **Description**: Cyl-1 misfire at idle; P0301 specific. MAF slightly low from uneven intake pulses. O2 cross-counts elevated (false lean pulses from misfire). At 2500 RPM smooths partially
- **Gas Chemistry**: HC: 150.0 ppm, CO: 0.3%, CO₂: 13.5%, O₂: 0.8%, NOx: 55.0 ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 6.0%, ECU λ: 1.03, MAF: 3.3 g/s
- **DTCs**: P0301
- **Expected Fault**: Misfire_Single_Cylinder_P0301_Idle_PID
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.3%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 55 ppm: low — rich quench or idle without thermal load. λ 1.03: in the catalyst window (0.97–1.03).

### Case: EXT-235
- **Description**: Cyl-3 ignition coil failed; dead hole. HC=750, O2=3.5 at idle. O2 cross-counts elevated (16/10s). Spark advance pulled to 6° (knock prevention). MAF=3.1 g/s low from pumping loss
- **Gas Chemistry**: HC: 750.0 ppm, CO: 0.4%, CO₂: 12.0%, O₂: 3.5%, NOx: 22.0 ppm, λ Analyser: 1.14
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 6.0%, ECU λ: 1.12, MAF: 3.1 g/s
- **DTCs**: P0303
- **Expected Fault**: Misfire_Single_Cylinder_P0303_Ignition_Coil
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 750 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.4%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 22 ppm: low — rich quench or idle without thermal load. λ 1.14: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: EXT-236
- **Description**: Multi-cyl misfire from failing coil pack; HC=1200, O2=5.0. O2 counts=18 (false lean spikes). Spark advance pulled to 4° (severe knock retard). MAF low at 2.8 g/s from pumping losses
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.5%, CO₂: 10.0%, O₂: 5.0%, NOx: 18.0 ppm, λ Analyser: 1.28
- **OBD / Air / Engine**: Trims B1 (ST/LT): 15.0% / 10.0%, ECU λ: 1.25, MAF: 2.8 g/s
- **DTCs**: P0300
- **Expected Fault**: Misfire_Multi_Cylinder_P0300_Coil_Pack
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 5%: severe lean / large misfire / air leak (>4%). NOx 18 ppm: low — rich quench or idle without thermal load. λ 1.28: lean (≥1.05) — Brettschneider chemistry.

### Case: EXT-237
- **Description**: CKP reluctor ring cracked; gas misfire visible but ECU misfire counter=0. O2 cross-counts=0 (ECU in open-loop fail-safe). MAF normal. ECU blindness confirmed
- **Gas Chemistry**: HC: 6.0 ppm, CO: 0.04%, CO₂: 15.5%, O₂: 0.1%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.6 g/s
- **DTCs**: P0300
- **Expected Fault**: ECU_Misfire_Blindness_CKP_Reluctor_Ring
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 6 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.04%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: PDF-4G-02
- **Description**: Rich + misfire warm idle; calc λ=0.920
- **Gas Chemistry**: HC: 400.0 ppm, CO: 2.5%, CO₂: 12.5%, O₂: 0.8%, NOx: 0.0 ppm, λ Analyser: 0.9474
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: High_CO_HC_Regular_Misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 400 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 2.5%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.9474: rich (≤0.95) — chemistry says excess fuel; OBD λ=0 (Δ=+0.95) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: PDF-4G-04
- **Description**: Dead cylinder from ignition wire; calc λ=1.133
- **Gas Chemistry**: HC: 450.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 2.5%, NOx: 0.0 ppm, λ Analyser: 1.106
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: 4Gas_Dead_Hole_Ignition_Wire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 450 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 2.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.106: lean (≥1.05) — Brettschneider chemistry; OBD λ=0 (Δ=+1.11) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: PDF-4G-05
- **Description**: Dead injector with catalyst lit; calc λ=0.997
- **Gas Chemistry**: HC: 120.0 ppm, CO: 0.3%, CO₂: 14.2%, O₂: 0.5%, NOx: 0.0 ppm, λ Analyser: 1.0101
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Dead_Hole_Injector_Catalyst_Lit
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 120 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.3%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.2%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.0101: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.01) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: PDF-HI-002
- **Description**: No lambda; lean misfire at high idle
- **Gas Chemistry**: HC: 1800.0 ppm, CO: 0.05%, CO₂: 11.5%, O₂: 4.5%, NOx: 0.0 ppm, λ Analyser: 1.1632
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Lean_Misfire_HighIdle
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 1800 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.1632: lean (≥1.05) — Brettschneider chemistry; OBD λ=0 (Δ=+1.16) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: PDF-HI-008
- **Description**: λ corrected 1.04→1.238; misfire at high RPM
- **Gas Chemistry**: HC: 600.0 ppm, CO: 0.15%, CO₂: 9.5%, O₂: 4.0%, NOx: 0.0 ppm, λ Analyser: 1.238
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.04
- **DTCs**: No DTCs stored
- **Expected Fault**: Ignition_Misfire_HighRPM
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 600 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.15%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 9.5%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 4%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.238: lean (≥1.05) — Brettschneider chemistry; OBD λ=1.04 (Δ=+0.20) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: YAML-CSV22
- **Description**: Mechanical_Misfire_Spark_Plug
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.5%, CO₂: 10.0%, O₂: 5.0%, NOx: 20.0 ppm, λ Analyser: 1.25
- **OBD / Air / Engine**: ECU λ: 1.2
- **DTCs**: P0302
- **Expected Fault**: Mechanical_Misfire_Spark_Plug
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 5%: severe lean / large misfire / air leak (>4%). NOx 20 ppm: low — rich quench or idle without thermal load. λ 1.25: lean (≥1.05) — Brettschneider chemistry.

### Case: YAML-CSV52
- **Description**: ECU_Misfire_Blindness
- **Gas Chemistry**: HC: 500.0 ppm, CO: 0.02%, CO₂: 15.5%, O₂: 4.5%, NOx: 10.0 ppm, λ Analyser: 1.2
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ECU_Misfire_Blindness
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 500 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 10 ppm: low — rich quench or idle without thermal load. λ 1.2: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.20) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: YAML-CSV66
- **Description**: Ghost_Misfire_Electrical_Noise
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Electrical_Noise
- **Expected State**: named_fault
- **Confidence Range**: 0.83 – 0.99
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-PDF_4G_02
- **Description**: High CO and HC with Regular Misfire (Warm Idle)
- **Gas Chemistry**: HC: 425.0 ppm, CO: 5.63%, CO₂: 10.0%, O₂: 2.3%, NOx: 0.0 ppm, λ Analyser: 0.9198
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 425 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 5.63%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 2.3%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.9198: rich (≤0.95) — chemistry says excess fuel. Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: YAML-PDF_4G_04
- **Description**: 4-Gas Dead Hole - Ignition Wire Failure
- **Gas Chemistry**: HC: 1257.0 ppm, CO: 0.49%, CO₂: 10.0%, O₂: 3.5%, NOx: 0.0 ppm, λ Analyser: 1.1325
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 1257 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.49%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.1325: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: YAML-PDF_4G_05
- **Description**: Dead Hole / Dead Injector / Catalyst Lit
- **Gas Chemistry**: HC: 55.0 ppm, CO: 0.02%, CO₂: 15.8%, O₂: 0.0%, NOx: 0.0 ppm, λ Analyser: 0.9974
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 55 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.9974: in the catalyst window (0.97–1.03).

### Case: YAML-PDF_HI_002
- **Description**: High HC & High O2 (Lean Misfire)
- **Gas Chemistry**: HC: 1000.0 ppm, CO: 0.3%, CO₂: 11.0%, O₂: 4.0%, NOx: 0.0 ppm, λ Analyser: 1.1748
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 1000 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.3%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.1748: lean (≥1.05) — Brettschneider chemistry. Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: YAML-RULE_CO_1
- **Description**: CO Rule: IF CO > 0.5% AND λ < 0.98 THEN "Rich mixture — check fuel delivery (injectors, p
- **Gas Chemistry**: HC: 100.0 ppm, CO: 1.0%, CO₂: 13.0%, O₂: 1.0%, NOx: 500.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 100 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1%: mild rich / pre-cat normal (0.5–1.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 1%: typical pre-cat residual (0.5–1.5%). NOx 500 ppm: moderate idle/light-load combustion temperature. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-TC36
- **Description**: Ghost Misfire (45%)
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 0.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: P0300
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-TC37
- **Description**: Mechanical Misfire (75%)
- **Gas Chemistry**: HC: 1200.0 ppm, CO: 0.5%, CO₂: 10.0%, O₂: 5.0%, NOx: 0.0 ppm, λ Analyser: 1.2
- **OBD / Air / Engine**: 
- **DTCs**: P0302
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 1200 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 10%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 5%: severe lean / large misfire / air leak (>4%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.2: lean (≥1.05) — Brettschneider chemistry.

### Case: case_005
- **Description**: P0301 misfire cylinder 1 with high HC and normal CO
- **Gas Chemistry**: HC: 1500.0 ppm, CO: 0.8%, CO₂: 12.0%, O₂: 1.5%, NOx: 200.0 ppm, λ Analyser: 1.04
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 4.0%, ECU λ: 1.0, RPM: 800.0, ECT: 90.0°C
- **DTCs**: P0301
- **Expected Fault**: misfire
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.85
- **Reasoning**: HC 1500 ppm: huge spike — raw fuel from cylinder 1 exits unburned. CO 0.8%: moderate; the dead cylinder dumps fuel without completing combustion. CO2 12.0%: depressed because one cylinder contributes nothing. O2 1.5%: slightly elevated — the dead cylinder's air escapes unused. NOx 200 ppm: moderate — the working cylinders still burn hot. λ 1.04: mildly lean overall because the dead cylinder's air passes through unreacted — a single-cylinder misfire fingerprint.

### Case: case_022
- **Description**: Dual-bank misfire on Bank 1 only (P0301), balanced tailpipe
- **Gas Chemistry**: HC: 250.0 ppm, CO: 0.3%, CO₂: 14.0%, O₂: 1.2%, NOx: 200.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 12.0% / 10.0%, Trims B2 (ST/LT): -2.0% / 0.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0301
- **Expected Fault**: misfire_cylinder_1
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.85
- **Reasoning**: HC 250 ppm: moderate — single-cylinder misfire on a six-cylinder dilutes HC at the common tailpipe. CO 0.3%: slightly elevated, partial burn from the affected cylinder. CO2 14.0%: only mildly depressed because five cylinders burn well. O2 1.2%: minor lean offset from the dead cylinder's air. NOx 200 ppm: moderate. λ 1.01: overall stoich because the misfire averages out; bank-1 trim of +12% versus bank-2 −2% pinpoints which bank holds the missing cylinder.

### Case: case_035
- **Description**: Ghost misfire from electrical noise (engine actually fine)
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 14.6%, O₂: 0.5%, NOx: ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0300
- **Expected Fault**: Ghost_Misfire_Electrical_Noise
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.65
- **Reasoning**: HC 20 ppm: clean — zero combustion deficit. CO 0.05%: clean. CO2 14.6%: ideal. O2 0.5%: minimal. NOx unmeasured. λ 1.00: perfect stoich. Gases prove combustion is healthy on every cylinder, so the P0300 is electrical noise, not a real misfire.


## Graph relations (explicit)

**labs/comlab/registry/rules/misfire.json** VERIFIES **CASE-021**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CASE-024**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CASE-033**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CASE-038**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-022**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-052**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-066**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-101**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-102**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-103**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-104**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-105**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-106**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-107**
**labs/comlab/registry/rules/misfire.json** VERIFIES **CSV-108**
**labs/comlab/registry/rules/misfire.json** VERIFIES **ECU-007**
**labs/comlab/registry/rules/misfire.json** VERIFIES **ECU-008**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXP-N016**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXP-N021**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-225**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-226**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-228**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-234**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-235**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-236**
**labs/comlab/registry/rules/misfire.json** VERIFIES **EXT-237**
**labs/comlab/registry/rules/misfire.json** VERIFIES **PDF-4G-02**
**labs/comlab/registry/rules/misfire.json** VERIFIES **PDF-4G-04**
**labs/comlab/registry/rules/misfire.json** VERIFIES **PDF-4G-05**
**labs/comlab/registry/rules/misfire.json** VERIFIES **PDF-HI-002**
**labs/comlab/registry/rules/misfire.json** VERIFIES **PDF-HI-008**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-CSV22**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-CSV52**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-CSV66**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-PDF_4G_02**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-PDF_4G_04**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-PDF_4G_05**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-PDF_HI_002**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-RULE_CO_1**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-TC36**
**labs/comlab/registry/rules/misfire.json** VERIFIES **YAML-TC37**
**labs/comlab/registry/rules/misfire.json** VERIFIES **case_005**
**labs/comlab/registry/rules/misfire.json** VERIFIES **case_022**
**labs/comlab/registry/rules/misfire.json** VERIFIES **case_035**
