---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-ecu_fault"
implements:
  - "labs/comlab/registry/code/rules/ecu_fault.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_ecu_fault_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/ecu_fault.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: ecu_fault · Parent document: labs/comlab/registry/corpus_curated.csv
# ecu_fault
28 cases

### Case: CSV-041
- **Description**: Physical rich; ECU sees lean
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 15.0%, ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: ECU_Logic_Inversion_False_Lean
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.15 (Δ=-0.27) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: CSV-043
- **Description**: Gas clean; sensor PIDs impossible
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0113
- **Expected Fault**: ECU_Input_Error_Ref_Volt_Drift
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-045
- **Description**: Rich gas; trims flat
- **Gas Chemistry**: HC: 80.0 ppm, CO: 1.5%, CO₂: 13.5%, O₂: 1.5%, NOx: 40.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0201
- **Expected Fault**: ECU_Output_Driver_Hardware_Fail
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 80 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.05: lean (≥1.05) — Brettschneider chemistry.

### Case: CSV-072
- **Description**: Gas perfect; P0606 ROM failure
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 0.2%, NOx: 25.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0606
- **Expected Fault**: ECU_Internal_Checksum_Error
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-123
- **Description**: Physical lean; ECU sees rich (P0172) and pulls fuel; biased O2 sensor
- **Gas Chemistry**: HC: 70.0 ppm, CO: 0.04%, CO₂: 11.8%, O₂: 4.2%, NOx: 320.0 ppm, λ Analyser: 1.18
- **OBD / Air / Engine**: Trims B1 (ST/LT): -18.0% / -12.0%, ECU λ: 0.85
- **DTCs**: P0172
- **Expected Fault**: ECU_Logic_Inversion_False_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 70 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.04%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.2%: severe lean / large misfire / air leak (>4%). NOx 320 ppm: moderate idle/light-load combustion temperature. λ 1.18: lean (≥1.05) — Brettschneider chemistry; OBD λ=0.85 (Δ=+0.33) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-124
- **Description**: False-rich logic inversion; coolant-poisoned upstream O2 stuck high V
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.05%, CO₂: 12.0%, O₂: 3.8%, NOx: 290.0 ppm, λ Analyser: 1.16
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -10.0%, ECU λ: 0.86
- **DTCs**: P0172
- **Expected Fault**: ECU_Logic_Inversion_False_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 290 ppm: moderate idle/light-load combustion temperature. λ 1.16: lean (≥1.05) — Brettschneider chemistry; OBD λ=0.86 (Δ=+0.30) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-125
- **Description**: Stuck-open injector driver; cyl floods rich; neg trims try to compensate
- **Gas Chemistry**: HC: 420.0 ppm, CO: 1.8%, CO₂: 13.2%, O₂: 1.3%, NOx: 38.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): -8.0% / -5.0%, ECU λ: 0.96
- **DTCs**: P0201
- **Expected Fault**: ECU_Injector_Driver_Fail
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 420 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 13.2%: healthy without-cat reference (13–14.5%). O2 1.3%: typical pre-cat residual (0.5–1.5%). NOx 38 ppm: low — rich quench or idle without thermal load. λ 0.95: rich (≤0.95) — chemistry says excess fuel.

### Case: CSV-126
- **Description**: Driver MOSFET shorted; persistent rich on cyl-1; HC up
- **Gas Chemistry**: HC: 450.0 ppm, CO: 2.0%, CO₂: 13.0%, O₂: 1.5%, NOx: 35.0 ppm, λ Analyser: 0.94
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -7.0%, ECU λ: 0.95
- **DTCs**: P0201
- **Expected Fault**: ECU_Injector_Driver_Fail
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 450 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 2%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 13%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 35 ppm: low — rich quench or idle without thermal load. λ 0.94: rich (≤0.95) — chemistry says excess fuel.

### Case: ECU-001
- **Description**: Physical rich; ECU perceives lean
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 15.0%, ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: ECU_False_Lean_Logic_Inversion
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.15 (Δ=-0.27) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: ECU-002
- **Description**: Gas clean; ECT/MAP/TPS impossible
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.2%, CO₂: 14.8%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0113
- **Expected Fault**: ECU_5V_Reference_Drift
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.2%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: ECU-003
- **Description**: One cylinder dead; HC+O2 elevation
- **Gas Chemistry**: HC: 120.0 ppm, CO: 1.8%, CO₂: 13.5%, O₂: 1.2%, NOx: 45.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0201
- **Expected Fault**: ECU_Injector_Driver_Fail
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 120 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 45 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03).

### Case: ECU-009
- **Description**: Rich gas; STFT=0 = open loop
- **Gas Chemistry**: HC: 120.0 ppm, CO: 2.5%, CO₂: 13.0%, O₂: 0.3%, NOx: 30.0 ppm, λ Analyser: 0.91
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ECU_Corrupted_Adaptive_Open_Loop
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 120 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 2.5%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 0.91: rich (≤0.95) — chemistry says excess fuel; OBD λ=1 (Δ=-0.09) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N002
- **Description**: RTV silicone poisoned upstream O2; ECU sees lean adds fuel; truth=rich
- **Gas Chemistry**: HC: 450.0 ppm, CO: 5.5%, CO₂: 12.0%, O₂: 0.3%, NOx: 18.0 ppm, λ Analyser: 0.84
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 25.0%, ECU λ: 1.05
- **DTCs**: P0171
- **Expected Fault**: ECU_Logic_Inversion_O2_Silicone
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 450 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 5.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 18 ppm: low — rich quench or idle without thermal load. λ 0.84: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.05 (Δ=-0.21) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N004
- **Description**: Manifold crack draws air; O2 sees lean adds fuel; truth=rich (0.92)
- **Gas Chemistry**: HC: 280.0 ppm, CO: 2.4%, CO₂: 11.0%, O₂: 1.6%, NOx: 35.0 ppm, λ Analyser: 0.92
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 15.0%, ECU λ: 1.12
- **DTCs**: P0171
- **Expected Fault**: Exhaust_Leak_PreCat_Logic_Inversion
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 280 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 2.4%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.6%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 35 ppm: low — rich quench or idle without thermal load. λ 0.92: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.12 (Δ=-0.20) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: EXP-N005
- **Description**: Frayed ground; alternator ripple mimics healthy O2 switching; truth lean
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.1%, CO₂: 13.5%, O₂: 1.6%, NOx: 280.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: ECU_Ground_Ripple_O2_Blindness
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.6%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 280 ppm: moderate idle/light-load combustion temperature. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N027
- **Description**: ECT 65°C never closes; ECU stays in warm-up enrichment; rich + HC
- **Gas Chemistry**: HC: 220.0 ppm, CO: 1.5%, CO₂: 12.0%, O₂: 1.5%, NOx: 50.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -5.0%, ECU λ: 0.96
- **DTCs**: P0128
- **Expected Fault**: Electric_Thermostat_Stuck_Open
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 220 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 0.95: rich (≤0.95) — chemistry says excess fuel.

### Case: EXT-221
- **Description**: Truth-vs-Perception override: physical rich (λ=0.88 gas), ECU perceives lean (λ=1.15 OBD). FF confirms idle-speed fault (RPM=800, LOAD=22%)
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 15.0%, ECU λ: 1.15, MAF: - g/s
- **DTCs**: P0171
- **Expected Fault**: ECU_Logic_Inversion_False_Lean_FF_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.15 (Δ=-0.27) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: TC-021
- **Description**: TC21: λ_gas corrected to Brettschneider 0.916; OBD λ=1.15 in OBD_Lambda
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 0.916
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: ECU_Liar_False_Lean_TC
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.916: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.15 (Δ=-0.23) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: YAML-CSV41
- **Description**: ECU_Logic_Inversion_False_Lean
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: ECU_Logic_Inversion_False_Lean
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.15 (Δ=-0.27) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: YAML-CSV43
- **Description**: ECU_Input_Error_Ref_Volt_Drift
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0113
- **Expected Fault**: ECU_Input_Error_Ref_Volt_Drift
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-CSV45
- **Description**: ECU_Output_Driver_Hardware_Fail
- **Gas Chemistry**: HC: 80.0 ppm, CO: 1.5%, CO₂: 13.5%, O₂: 1.5%, NOx: 40.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0201
- **Expected Fault**: ECU_Output_Driver_Hardware_Fail
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 80 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.05: lean (≥1.05) — Brettschneider chemistry.

### Case: YAML-CSV72
- **Description**: ECU_Internal_Checksum_Error
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 0.2%, NOx: 25.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0606
- **Expected Fault**: ECU_Internal_Checksum_Error
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-TC22
- **Description**: ECU FAULT: Ref Volt (40%)
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.2%, NOx: 0.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: P0113
- **Expected Fault**: ecu_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-TC47
- **Description**: ECU FAULT: Driver (30%)
- **Gas Chemistry**: HC: 80.0 ppm, CO: 1.5%, CO₂: 13.5%, O₂: 1.5%, NOx: 0.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: P0201
- **Expected Fault**: ecu_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 80 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1: in the catalyst window (0.97–1.03).

### Case: case_001
- **Description**: Classic false-lean DTC (P0171) with rich tailpipe gas
- **Gas Chemistry**: HC: 220.0 ppm, CO: 3.5%, CO₂: 11.8%, O₂: 0.5%, NOx: 120.0 ppm, λ Analyser: 0.92
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 22.0%, ECU λ: 1.12, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171
- **Expected Fault**: ECU_Logic_Inversion_False_Lean
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.85
- **Reasoning**: HC 220 ppm: modest rise from rich incomplete burn (excess fuel exits as raw HC). CO 3.5%: clear rich signature, oxygen-starved combustion (richmixture.pdf row 1). CO2 11.8%: depressed below 14.5+ ceiling because rich burn is inefficient. O2 0.5%: low, the excess fuel consumed almost all available oxygen. NOx 120 ppm: low, rich quenches peak combustion temperature. λ 0.92: Brettschneider chemistry says rich (and is misfire-immune, lambda.pdf), contradicting ECU λ=1.12 with +25% trims — canonical false-lean perception inversion.

### Case: case_013
- **Description**: P0172 (rich DTC) with lean gases (false-rich perception)
- **Gas Chemistry**: HC: 40.0 ppm, CO: 0.02%, CO₂: 14.0%, O₂: 3.0%, NOx: 500.0 ppm, λ Analyser: 1.08
- **OBD / Air / Engine**: Trims B1 (ST/LT): -20.0% / -18.0%, ECU λ: 0.92, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0172
- **Expected Fault**: ECU_Logic_Inversion_False_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.85
- **Reasoning**: HC 40 ppm: normal/low — no rich misfire happening. CO 0.02%: near zero, nothing rich is happening. CO2 14.0%: slightly depressed because mixture is actually lean. O2 3.0%: clearly elevated, lean tail. NOx 500 ppm: elevated from hotter lean combustion. λ 1.08: chemistry says lean; ECU sees rich (OBD λ=0.92, trims -20%) and is pulling fuel — the false-rich mirror of Case 1.

### Case: case_027
- **Description**: P0606 ECU internal fault with normal gases (magnet test)
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.01%, CO₂: 14.7%, O₂: 0.4%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0606
- **Expected Fault**: ECU_Internal_Checksum_Error
- **Expected State**: named_fault
- **Confidence Range**: 0.35 – 0.7
- **Reasoning**: HC 15 ppm: clean. CO 0.01%: clean. CO2 14.7%: ideal. O2 0.4%: minimal residual. NOx 30 ppm: low idle. λ 1.00: perfect stoich. All gases healthy; diagnosis comes solely from the P0606 ECU-internal-checksum DTC, which the magnet edge legitimately promotes when the prerequisite DTC is present.

### Case: case_033
- **Description**: Pre-cat exhaust air leak (false-lean ECU, rich tailpipe)
- **Gas Chemistry**: HC: 200.0 ppm, CO: 3.0%, CO₂: 11.0%, O₂: 1.0%, NOx: ppm, λ Analyser: 0.91
- **OBD / Air / Engine**: Trims B1 (ST/LT): 22.0% / 20.0%, ECU λ: 1.1, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171
- **Expected Fault**: Exhaust_Air_Leak_Pre_Cat
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 200 ppm: elevated from rich incomplete burn. CO 3.0%: clearly rich. CO2 11.0%: strongly depressed. O2 1.0%: low (gas sample is post-leak so true rich shows). NOx unmeasured. λ 0.91: chemistry says rich; ECU sees lean because air is drawn in upstream of the O2 sensor — a pre-cat exhaust air leak (lambda.pdf §8.5: a 5% air leak shifts lambda 5% lean) inverting perception.


## Graph relations (explicit)

**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-041**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-043**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-045**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-072**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-123**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-124**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-125**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **CSV-126**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **ECU-001**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **ECU-002**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **ECU-003**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **ECU-009**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **EXP-N002**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **EXP-N004**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **EXP-N005**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **EXP-N027**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **EXT-221**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **TC-021**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-CSV41**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-CSV43**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-CSV45**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-CSV72**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-TC22**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **YAML-TC47**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **case_001**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **case_013**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **case_027**
**labs/comlab/registry/rules/ecu_fault.json** VERIFIES **case_033**
