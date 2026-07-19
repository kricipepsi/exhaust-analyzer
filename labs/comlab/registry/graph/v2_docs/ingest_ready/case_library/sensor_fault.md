---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-sensor_fault
implements:
- labs/comlab/registry/rules/sensor_fault.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_sensor_fault_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/sensor_fault.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: sensor_fault · Parent document: labs/comlab/registry/corpus_curated.csv
# sensor_fault
20 cases

### Case: CASE-014
- **Description**: Target >8 switches/10s; 3 = sluggish; trims drift slowly; gas near stoich; replace sensor; no DTC yet
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.1%, CO₂: 14.8%, O₂: 0.3%, NOx: 60.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 12.0%, ECU λ: 1.0, MAF: 3.7 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_3_Switches_Per_10s
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 60 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: CSV-025
- **Description**: Oscillating trims; gas clean
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 15.0%, O₂: 0.2%, NOx: 50.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / -10.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_Aging
- **Expected State**: named_fault
- **Confidence Range**: 0.6 – 0.8
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N006
- **Description**: 1996 MAP drift; ECU thinks rich, trims neg; gas reality near stoich
- **Gas Chemistry**: HC: 90.0 ppm, CO: 0.7%, CO₂: 13.5%, O₂: 0.6%, NOx: 110.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): -5.0% / 0.0%, ECU λ: 0.95
- **DTCs**: No DTCs stored
- **Expected Fault**: MAP_Sensor_Drift_Speed_Density
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 90 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.7%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.6%: typical pre-cat residual (0.5–1.5%). NOx 110 ppm: moderate idle/light-load combustion temperature. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N015
- **Description**: Wideband ref-current drift; ECU sees stoich, truth lean; high NOx tell
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.08%, CO₂: 13.5%, O₂: 1.8%, NOx: 1100.0 ppm, λ Analyser: 1.15
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Wideband_O2_Reference_Drift
- **Expected State**: named_fault
- **Confidence Range**: 0.57 – 0.77
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 1100 ppm: elevated — hot lean burn or stuck-open EGR fingerprint. λ 1.15: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.15) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: EXP-N020
- **Description**: Vehicle at altitude; BARO calc stuck SL; over-fuelling; trims maxed neg
- **Gas Chemistry**: HC: 320.0 ppm, CO: 3.5%, CO₂: 12.5%, O₂: 0.3%, NOx: 25.0 ppm, λ Analyser: 0.85
- **OBD / Air / Engine**: Trims B1 (ST/LT): -20.0% / -18.0%, ECU λ: 0.86
- **DTCs**: No DTCs stored
- **Expected Fault**: BARO_Calculation_Stuck_Sea_Level
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 320 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 0.85: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N028
- **Description**: Heater under-performing; ECU on safe-map; gas oscillates uncontrolled
- **Gas Chemistry**: HC: 70.0 ppm, CO: 0.1%, CO₂: 13.0%, O₂: 1.5%, NOx: 240.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0053
- **Expected Fault**: Wideband_Heater_Cold_Safe_Map
- **Expected State**: named_fault
- **Confidence Range**: 0.59 – 0.79
- **Reasoning**: HC 70 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 240 ppm: moderate idle/light-load combustion temperature. λ 1.05: lean (≥1.05) — Brettschneider chemistry; OBD λ=1 (Δ=+0.05) — emerging perception gap.

### Case: EXT-219
- **Description**: MAF over-reporting (7.2 g/s at hot idle vs expected 3.5). ECU adds excess fuel; gas confirms rich (λ=0.91). Trims maxed negative. MAF replaced, problem resolved
- **Gas Chemistry**: HC: 150.0 ppm, CO: 2.8%, CO₂: 14.0%, O₂: 0.2%, NOx: 25.0 ppm, λ Analyser: 0.91
- **OBD / Air / Engine**: Trims B1 (ST/LT): -20.0% / -15.0%, ECU λ: 0.85, MAF: 7.2 g/s
- **DTCs**: P0172
- **Expected Fault**: MAF_Overreport_Faulty_Sensor_Element
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 2.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 0.91: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXT-229
- **Description**: O2 cross-counts=4 per 10 seconds (expected >8). Sensor aged; switching still occurs but too slow. Trims drift slowly. Gas nearly stoich. O2 sensor replacement recommended
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.1%, CO₂: 14.8%, O₂: 0.3%, NOx: 60.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 12.0%, ECU λ: 1.0, MAF: 3.8 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_Sluggish_CrossCounts
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 30 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 60 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: EXT-230
- **Description**: O2 cross-counts=2 per 10 seconds; sensor essentially dead. Trims flat. Gas borderline stoich but sensor cannot detect mixture swings. Replace immediately
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.08%, CO₂: 15.0%, O₂: 0.25%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 1.0% / 2.0%, ECU λ: 1.0, MAF: 3.6 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_Failing_CrossCounts
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.7
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.25%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: TC-046
- **Description**: TC46: no lambda reported; gas pattern only
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 15.0%, O₂: 0.2%, NOx: 50.0 ppm, λ Analyser: 1.0072
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / -10.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_Aging_TC
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1.0072: in the catalyst window (0.97–1.03).

### Case: YAML-CSV25
- **Description**: Lazy_O2_Sensor_Aging
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 15.0%, O₂: 0.2%, NOx: 50.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Lazy_O2_Sensor_Aging
- **Expected State**: named_fault
- **Confidence Range**: 0.6 – 0.8
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-TC46
- **Description**: Sensor Aging (70%)
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 0.2%, NOx: 0.0 ppm, λ Analyser: 1.0056
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.0056: in the catalyst window (0.97–1.03).

### Case: case_004
- **Description**: P0420 with normal post-cat O2 and clean gases (false catalyst DTC)
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.01%, CO₂: 14.8%, O₂: 0.3%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 3.0% / 2.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0420
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 10 ppm: near zero — meets the post-cat ≤50 ppm reference (lambda.pdf §6.1). CO 0.01%: essentially zero, well inside the ≤0.5% post-cat window. CO2 14.8%: at the efficient ceiling. O2 0.3%: minimal residual oxygen, stoichiometric. NOx 20 ppm: low at idle as expected. λ 1.00: dead-centre of the 0.97–1.03 catalyst window; chemistry contradicts the P0420 DTC, pointing at a faulty post-cat O2 sensor rather than a real catalyst failure.

### Case: case_009
- **Description**: Wideband sensor drift (false lean) covered by P0053
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.2%, CO₂: 14.5%, O₂: 0.8%, NOx: 80.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.96, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0053
- **Expected Fault**: Wideband_Heater_Cold_Safe_Map
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 30 ppm: clean burn, no combustion problem. CO 0.2%: slightly elevated — possibly residual from open-loop fallback map. CO2 14.5%: at the healthy ceiling. O2 0.8%: below 1.5%, normal post-burn residue. NOx 80 ppm: typical idle. λ 1.01: chemistry says stoich; ECU λ=0.96 plus flat trims (sensor in open-loop due to P0053) is the wideband-heater-fault contradiction.

### Case: case_025
- **Description**: STFT=-127% (O2 sensor short-to-ground)
- **Gas Chemistry**: HC: 100.0 ppm, CO: 0.8%, CO₂: 13.0%, O₂: 1.0%, NOx: ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): -127.0% / -100.0%, ECU λ: 0.75, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0131
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.8
- **Reasoning**: HC 100 ppm: slightly elevated, mild rich offset. CO 0.8%: modestly elevated, mild rich. CO2 13.0%: slightly depressed. O2 1.0%: typical. NOx unmeasured. λ 0.98: only mildly rich; the railed STFT=-127% and OBD λ=0.75 are clearly an O2-sensor short-to-ground (P0131), not a real combustion event of that magnitude.

### Case: case_026
- **Description**: STFT=+127% (O2 sensor open / high voltage)
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.1%, CO₂: 14.0%, O₂: 2.0%, NOx: ppm, λ Analyser: 1.04
- **OBD / Air / Engine**: Trims B1 (ST/LT): 127.0% / 100.0%, ECU λ: 1.5, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0132
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.8
- **Reasoning**: HC 60 ppm: slightly elevated. CO 0.1%: low. CO2 14.0%: near ideal. O2 2.0%: slightly elevated, mild lean. NOx unmeasured. λ 1.04: mild lean; railed +127% trim and OBD λ=1.50 are an open-circuit O2 signal, not a true λ=1.50 combustion.

### Case: case_037
- **Description**: Wideband heater fault during cold start (perception + cold gate)
- **Gas Chemistry**: HC: 350.0 ppm, CO: 1.5%, CO₂: 12.5%, O₂: 1.0%, NOx: ppm, λ Analyser: 0.96
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.98, RPM: 1100.0, ECT: 10.0°C
- **DTCs**: P0053
- **Expected Fault**: Wideband_Heater_Cold_Safe_Map
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.65
- **Reasoning**: HC 350 ppm: elevated — cold-start enrichment plus poor vaporisation. CO 1.5%: moderate, normal cold richness. CO2 12.5%: depressed by cold inefficient burn. O2 1.0%: normal. NOx unmeasured. λ 0.96: mildly rich, exactly what cold-start commands; P0053 says the heater faulted, ECU stayed on open-loop safe map — cold-start gate must not nuke the wideband-heater diagnosis.

### Case: case_039
- **Description**: Upstream O2 stuck at 0.45 V (no switching)
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.1%, CO₂: 14.0%, O₂: 2.0%, NOx: ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0134
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 80 ppm: slightly elevated, mild lean inefficiency. CO 0.1%: low. CO2 14.0%: only mildly depressed. O2 2.0%: slightly elevated, mild lean. NOx unmeasured. λ 1.03: mild lean; the steady 0.45 V upstream O2 plus flat trims plus P0134 prove the sensor is non-switching, not the engine.

### Case: case_041
- **Description**: MAP sensor stuck at barometric pressure (idle MAP=100 kPa)
- **Gas Chemistry**: HC: 150.0 ppm, CO: 1.0%, CO₂: 13.0%, O₂: 1.5%, NOx: ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -8.0%, ECU λ: 0.96, MAP: 100.0 kPa, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0106
- **Expected Fault**: MAP_sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 150 ppm: slightly elevated from a mild rich offset. CO 1.0%: modestly rich. CO2 13.0%: modestly depressed. O2 1.5%: borderline. NOx unmeasured. λ 0.98: mildly rich; the giveaway is MAP=100 kPa at idle (engine should pull ~30 kPa) — the sensor has died and speed-density is dumping extra fuel.

### Case: case_046
- **Description**: Fuel-pressure sensor implausible (P0190) but engine fine
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 14.6%, O₂: 0.5%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0190
- **Expected Fault**: sensor_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.6
- **Reasoning**: HC 20 ppm: clean. CO 0.05%: clean. CO2 14.6%: ideal. O2 0.5%: minimal. NOx 30 ppm: low. λ 1.00: perfect stoich. Gases prove combustion is normal so fuel pressure is actually fine; FRP=0 with P0190 is a sensor fault, not a fuel-pressure fault.


## Graph relations (explicit)

**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **CASE-014**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **CSV-025**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXP-N006**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXP-N015**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXP-N020**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXP-N028**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXT-219**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXT-229**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **EXT-230**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **TC-046**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **YAML-CSV25**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **YAML-TC46**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_004**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_009**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_025**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_026**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_037**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_039**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_041**
**labs/comlab/registry/rules/sensor_fault.json** VERIFIES **case_046**
