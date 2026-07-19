---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-cam_timing
implements:
- labs/comlab/registry/rules/cam_timing.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_cam_timing_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/cam_timing.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: cam_timing · Parent document: labs/comlab/registry/corpus_curated.csv
# cam_timing
9 cases

### Case: CASE-018
- **Description**: HC delta 250→850ppm at 2500RPM from sluggish VVT phaser; spark advance fluctuating mid-load; CO2 drops under load
- **Gas Chemistry**: HC: 250.0 ppm, CO: 0.5%, CO₂: 12.5%, O₂: 0.5%, NOx: 55.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 3.0%, ECU λ: 1.0, MAF: 3.2 g/s
- **DTCs**: P0011
- **Expected Fault**: VVT_Phaser_Lag_HC_Rises_Under_Load
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 250 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 55 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: CSV-115
- **Description**: Retarded intake cam; HC up CO2 down NOx<80 (vs lean: NOx>800)
- **Gas Chemistry**: HC: 320.0 ppm, CO: 1.1%, CO₂: 11.8%, O₂: 1.6%, NOx: 60.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 2.0%, ECU λ: 1.0
- **DTCs**: P0011
- **Expected Fault**: Cam_Timing_Retard
- **Expected State**: named_fault
- **Confidence Range**: 0.72 – 0.92
- **Reasoning**: HC 320 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.1%: mild rich / pre-cat normal (0.5–1.5%). CO2 11.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.6%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 60 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: CSV-116
- **Description**: VVT phaser sluggish; late combustion; LOW NOx is the key tell
- **Gas Chemistry**: HC: 350.0 ppm, CO: 1.2%, CO₂: 11.5%, O₂: 1.8%, NOx: 45.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 3.0%, ECU λ: 1.0
- **DTCs**: P0011
- **Expected Fault**: Cam_Timing_Retard
- **Expected State**: named_fault
- **Confidence Range**: 0.72 – 0.92
- **Reasoning**: HC 350 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.2%: mild rich / pre-cat normal (0.5–1.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 45 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: EXP-N007
- **Description**: Oil sludge restricts cam phaser; valve overlap excess; HC up + low CO2
- **Gas Chemistry**: HC: 400.0 ppm, CO: 0.8%, CO₂: 13.5%, O₂: 0.45%, NOx: 70.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 1.0%, ECU λ: 1.0
- **DTCs**: P0011
- **Expected Fault**: VVT_Phaser_Sludge_Lag
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 400 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.8%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.45%: low — rich consumed the oxygen, or perfect stoich. NOx 70 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: EXP-N023
- **Description**: Solenoid coil R drifted 8→40Ω; phaser sluggish; HC up at 2500
- **Gas Chemistry**: HC: 420.0 ppm, CO: 0.4%, CO₂: 13.0%, O₂: 0.4%, NOx: 75.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: VVT_Solenoid_Resistance_Drift
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 420 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.4%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 75 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: EXT-209
- **Description**: Retarded cam at idle: HC=350, CO2 depressed. Trims mildly negative. At 2500 RPM phaser catches up, emissions nearly normalise. VVT solenoid resistance drifted
- **Gas Chemistry**: HC: 350.0 ppm, CO: 0.5%, CO₂: 12.5%, O₂: 1.0%, NOx: 55.0 ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: Trims B1 (ST/LT): -5.0% / -8.0%, ECU λ: 0.97, MAF: - g/s
- **DTCs**: P0011
- **Expected Fault**: Cam_Timing_Retard_VVT_Phaser_Lag
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 350 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1%: typical pre-cat residual (0.5–1.5%). NOx 55 ppm: low — rich quench or idle without thermal load. λ 1.03: in the catalyst window (0.97–1.03).

### Case: EXT-210
- **Description**: Over-advanced cam at idle: HC elevated, CO2 depressed. Trims negative. At 2500 RPM, cam returns to normal range. Cold rattle on start
- **Gas Chemistry**: HC: 400.0 ppm, CO: 0.6%, CO₂: 12.0%, O₂: 1.2%, NOx: 48.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): -3.0% / -5.0%, ECU λ: 0.98, MAF: - g/s
- **DTCs**: P0012
- **Expected Fault**: Cam_Timing_Advance_VVT_Phaser_Stuck
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 400 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 48 ppm: low — rich quench or idle without thermal load. λ 1.05: lean (≥1.05) — Brettschneider chemistry.

### Case: MECH-004
- **Description**: Retarded timing; HC/CO high
- **Gas Chemistry**: HC: 280.0 ppm, CO: 1.2%, CO₂: 12.8%, O₂: 1.8%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Cam_Timing_Retard_Late
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 280 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.2%: mild rich / pre-cat normal (0.5–1.5%). CO2 12.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: case_042
- **Description**: VVT phaser stuck advanced (P0011) — knock and rich
- **Gas Chemistry**: HC: 180.0 ppm, CO: 1.5%, CO₂: 12.5%, O₂: 1.2%, NOx: ppm, λ Analyser: 0.94
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -12.0%, ECU λ: 0.96, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0011
- **Expected Fault**: vvt_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.35 – 0.65
- **Reasoning**: HC 180 ppm: moderately elevated — knock or incomplete burn from over-advanced cam. CO 1.5%: clearly rich. CO2 12.5%: depressed. O2 1.2%: typical. NOx unmeasured. λ 0.94: clearly rich; with P0011 the cam phaser is stuck advanced, valve overlap pushes raw mixture through and lifts CO.


## Graph relations (explicit)

**labs/comlab/registry/rules/cam_timing.json** VERIFIES **CASE-018**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **CSV-115**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **CSV-116**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **EXP-N007**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **EXP-N023**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **EXT-209**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **EXT-210**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **MECH-004**
**labs/comlab/registry/rules/cam_timing.json** VERIFIES **case_042**
