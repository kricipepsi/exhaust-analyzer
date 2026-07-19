---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-rich_mixture
implements:
- labs/comlab/registry/rules/rich_mixture.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_rich_mixture_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/rich_mixture.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: rich_mixture · Parent document: labs/comlab/registry/corpus_curated.csv
# rich_mixture
23 cases

### Case: CASE-023
- **Description**: FF ECT=68°C after 20min drive; ECU stays in warm-up enrichment map; P0128 set at cruise; CO and HC elevated from rich map
- **Gas Chemistry**: HC: 220.0 ppm, CO: 0.6%, CO₂: 13.0%, O₂: 0.5%, NOx: 50.0 ppm, λ Analyser: 0.92
- **OBD / Air / Engine**: Trims B1 (ST/LT): -8.0% / -5.0%, ECU λ: 0.96, MAF: 3.5 g/s
- **DTCs**: P0128
- **Expected Fault**: Thermostat_Stuck_Open_ECT68_Enrichment
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 220 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 0.92: rich (≤0.95) — chemistry says excess fuel.

### Case: CASE-031
- **Description**: HPFP seal leak; fuel contaminates oil; PCV reintroduces via crankcase; rich at idle; trims maxed neg; P0087 low rail pressure
- **Gas Chemistry**: HC: 300.0 ppm, CO: 2.6%, CO₂: 12.5%, O₂: 0.4%, NOx: 35.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): -20.0% / -22.0%, ECU λ: 0.9, MAF: 3.5 g/s
- **DTCs**: P0087
- **Expected Fault**: GDI_HPFP_Internal_Seal_Leak_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 300 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 2.6%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: CASE-037
- **Description**: Intercooler pipe split post-turbo; pressurised air bypasses MAF; ECU adds excess fuel; physical rich; MAF vs MAP mismatch
- **Gas Chemistry**: HC: 200.0 ppm, CO: 1.8%, CO₂: 12.5%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -8.0%, ECU λ: 0.9, MAF: 3.5 g/s
- **DTCs**: P0234
- **Expected Fault**: Turbo_Boost_Leak_Post_Turbo_Rich_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 200 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: CASE-040
- **Description**: BOV diaphragm torn; rich spike only during gear shift pressure release; gas at idle and 2500 both normal; FF needed at shift moment
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.06%, CO₂: 15.2%, O₂: 0.2%, NOx: 22.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: P0234
- **Expected Fault**: Turbo_BOV_Tear_Rich_Spike_Gear_Change_Only
- **Expected State**: named_fault
- **Confidence Range**: 0.57 – 0.77
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 22 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-018
- **Description**: Rich CO; ECU correcting negatively
- **Gas Chemistry**: HC: 180.0 ppm, CO: 4.5%, CO₂: 12.5%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 0.85
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -10.0%, ECU λ: 0.86
- **DTCs**: P0172
- **Expected Fault**: Mechanical_Rich_Leaking_Injector
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 4.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 0.85: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N003
- **Description**: 1997 FPR return restricted; rail 80psi; trims maxed neg; rich won't clear
- **Gas Chemistry**: HC: 380.0 ppm, CO: 7.5%, CO₂: 9.0%, O₂: 0.2%, NOx: 12.0 ppm, λ Analyser: 0.75
- **OBD / Air / Engine**: Trims B1 (ST/LT): -25.0% / -25.0%, ECU λ: 0.78
- **DTCs**: P0172
- **Expected Fault**: Fuel_Pressure_Regulator_Return_Blocked
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 380 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 7.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 9%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 12 ppm: low — rich quench or idle without thermal load. λ 0.75: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N013
- **Description**: HPFP leak into oil; PCV reintroduces fuel; ECU pulls but stays rich
- **Gas Chemistry**: HC: 300.0 ppm, CO: 2.6%, CO₂: 12.5%, O₂: 0.4%, NOx: 28.0 ppm, λ Analyser: 0.88
- **OBD / Air / Engine**: Trims B1 (ST/LT): -30.0% / -20.0%, ECU λ: 0.85
- **DTCs**: P0172
- **Expected Fault**: GDI_HPFP_Internal_Seal_Failure
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 300 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 2.6%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 28 ppm: low — rich quench or idle without thermal load. λ 0.88: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXT-203
- **Description**: Rich at 2500 RPM only; injector O-ring leaks under fuel-rail pressure pulsation at higher flow. Idle trims near zero
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.08%, CO₂: 14.0%, O₂: 0.4%, NOx: 55.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -12.0%, ECU λ: 0.95, MAF: - g/s
- **DTCs**: P0172
- **Expected Fault**: Fuel_Delivery_Rich_Leaking_Injector_O_Ring
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 30 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 55 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: EXT-217
- **Description**: Thermostat stuck open; ECT=62°C after 20-minute drive. ECU remains in warm-up enrichment. P0128 set at steady 45 km/h cruise. HC up from persistent enrichment
- **Gas Chemistry**: HC: 220.0 ppm, CO: 0.6%, CO₂: 13.0%, O₂: 0.5%, NOx: 50.0 ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -8.0%, ECU λ: 0.96, MAF: - g/s
- **DTCs**: P0128
- **Expected Fault**: Thermostat_Stuck_Open_ECT_62C_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 220 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 0.98: in the catalyst window (0.97–1.03).

### Case: EXT-227
- **Description**: FPR diaphragm ruptured; fuel drawn into intake via vacuum line. FF=idle confirms worst at idle. Battery voltage 11.2V at FF suggests alternator contributing to sensor drift
- **Gas Chemistry**: HC: 550.0 ppm, CO: 4.0%, CO₂: 11.0%, O₂: 0.3%, NOx: 18.0 ppm, λ Analyser: 0.86
- **OBD / Air / Engine**: Trims B1 (ST/LT): -30.0% / -20.0%, ECU λ: 0.82, MAF: 4.8 g/s
- **DTCs**: P0172
- **Expected Fault**: Rich_Fuel_Pressure_Regulator_Diaphragm_Leak_FF
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 550 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 4%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 18 ppm: low — rich quench or idle without thermal load. λ 0.86: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: PDF-4G-03
- **Description**: Rich; not quite misfire; calc λ=0.945
- **Gas Chemistry**: HC: 150.0 ppm, CO: 3.5%, CO₂: 13.0%, O₂: 0.3%, NOx: 0.0 ppm, λ Analyser: 0.9116
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Rich_Mixture_High_CO
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 3.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.9116: rich (≤0.95) — chemistry says excess fuel; OBD λ=0 (Δ=+0.91) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: PDF-HI-001
- **Description**: No lambda; rich/over-fueling at high idle
- **Gas Chemistry**: HC: 650.0 ppm, CO: 4.0%, CO₂: 11.0%, O₂: 0.3%, NOx: 0.0 ppm, λ Analyser: 0.8692
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Rich_Over_Fueling_HighIdle
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 650 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 4%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.8692: rich (≤0.95) — chemistry says excess fuel; OBD λ=0 (Δ=+0.87) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: RULE-CO-1
- **Description**: Rule: CO>0.5% AND λ<0.98 = rich mixture
- **Gas Chemistry**: HC: 100.0 ppm, CO: 1.0%, CO₂: 13.0%, O₂: 1.0%, NOx: 500.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: CO_Rule_Rich_Threshold_Example
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 100 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1%: mild rich / pre-cat normal (0.5–1.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 1%: typical pre-cat residual (0.5–1.5%). NOx 500 ppm: moderate idle/light-load combustion temperature. λ 1: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.00) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: YAML-CSV18
- **Description**: Mechanical_Rich_Leaking_Injector
- **Gas Chemistry**: HC: 180.0 ppm, CO: 4.5%, CO₂: 12.5%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 0.85
- **OBD / Air / Engine**: ECU λ: 0.86
- **DTCs**: P0172
- **Expected Fault**: Mechanical_Rich_Leaking_Injector
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 4.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 0.85: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: YAML-PDF_4G_03
- **Description**: Rich Mixture - High CO (Not Quite Misfire)
- **Gas Chemistry**: HC: 85.0 ppm, CO: 2.9%, CO₂: 11.5%, O₂: 0.8%, NOx: 0.0 ppm, λ Analyser: 0.9445
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 85 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 2.9%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.9445: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: YAML-PDF_HI_001
- **Description**: High CO & High HC (Rich Mixture / Over-fueling)
- **Gas Chemistry**: HC: 650.0 ppm, CO: 4.0%, CO₂: 11.0%, O₂: 0.3%, NOx: 0.0 ppm, λ Analyser: 0.8692
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 650 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 4%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.8692: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: YAML-TC12
- **Description**: Mechanical Rich (85%)
- **Gas Chemistry**: HC: 180.0 ppm, CO: 4.5%, CO₂: 12.5%, O₂: 0.2%, NOx: 0.0 ppm, λ Analyser: 0.86
- **OBD / Air / Engine**: 
- **DTCs**: P0172
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 4.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 0.86: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: case_002
- **Description**: Cold-start enrichment without DTC mimicking rich fault
- **Gas Chemistry**: HC: 450.0 ppm, CO: 2.1%, CO₂: 10.5%, O₂: 1.2%, NOx: 80.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.98, RPM: 1200.0, ECT: 5.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.2 – 0.45
- **Reasoning**: HC 450 ppm: elevated but consistent with cold-start open-loop enrichment, fuel droplets not fully vaporised. CO 2.1%: typical cold-enrichment richness rather than a mechanical fault at ECT=5°C. CO2 10.5%: depressed because cold-chamber combustion is inefficient. O2 1.2%: slightly elevated — cold burn leaves residual air. NOx 80 ppm: low, cold chamber never reaches NOx-forming temperature. λ 0.95: mildly rich, exactly what the ECU commands during warm-up — the cold-start gate must demote mechanical-rich faults.

### Case: case_015
- **Description**: Marginal lambda mismatch (Brett vs analyser ~0.07)
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.5%, CO₂: 13.5%, O₂: 1.0%, NOx: 300.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.98, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.2 – 0.5
- **Reasoning**: HC 80 ppm: slightly elevated, mild combustion inefficiency. CO 0.5%: borderline — no clear rich call. CO2 13.5%: modestly low, marginal efficiency. O2 1.0%: normal-ish. NOx 300 ppm: slightly elevated, hot light-load burn near stoich. λ 1.05 vs OBD 0.98 → 0.07 gap, just below the mismatch warning threshold; engine must avoid firing the warning at the boundary.

### Case: case_017
- **Description**: 4-gas analyser with NOx=0 (must not fire nox_low)
- **Gas Chemistry**: HC: 200.0 ppm, CO: 1.5%, CO₂: 12.0%, O₂: 1.0%, NOx: 0.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.98, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.45 – 0.75
- **Reasoning**: HC 200 ppm: modestly elevated from rich incomplete burn. CO 1.5%: clearly rich (richmixture.pdf row 1). CO2 12.0%: depressed by inefficient rich combustion. O2 1.0%: low because excess fuel consumed the available oxygen. NOx 0: analyser is 4-gas — lambda.pdf §8.5 confirms a 4-gas analyser is adequate for lambda; NOx contributes only 0.05% O2 per 1000 ppm so omission is fine, and the engine must NOT read NOx=0 as 'nox_low' evidence. λ 0.95: mild rich, consistent with the CO/HC pattern.

### Case: case_023
- **Description**: Catalyst masking: P0420 with rich gases overwhelming cat
- **Gas Chemistry**: HC: 300.0 ppm, CO: 2.0%, CO₂: 12.0%, O₂: 1.0%, NOx: 100.0 ppm, λ Analyser: 0.93
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -10.0%, ECU λ: 0.96, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0420
- **Expected Fault**: rich_mixture
- **Expected State**: named_fault
- **Confidence Range**: 0.45 – 0.75
- **Reasoning**: HC 300 ppm: elevated — cat overwhelmed by rich feed gas. CO 2.0%: clearly rich. CO2 12.0%: depressed by inefficient rich burn. O2 1.0%: low — fuel consumed the air. NOx 100 ppm: quenched by rich. λ 0.93: chemistry says rich; the P0420 is masking — the cat is being fed bad exhaust, not failing in itself, so rich_mixture must outrank catalyst_failure.

### Case: case_029
- **Description**: High fuel pressure (specific child) — even rich pulse
- **Gas Chemistry**: HC: 180.0 ppm, CO: 2.5%, CO₂: 12.0%, O₂: 0.6%, NOx: ppm, λ Analyser: 0.92
- **OBD / Air / Engine**: Trims B1 (ST/LT): -20.0% / -18.0%, ECU λ: 0.94, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: high_fuel_pressure
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 180 ppm: moderately elevated from rich incomplete burn. CO 2.5%: clearly rich. CO2 12.0%: depressed. O2 0.6%: low — oxygen consumed by excess fuel. NOx unmeasured. λ 0.92: clearly rich and even (no pulse pattern), pointing at globally elevated fuel pressure rather than a single leaking injector.

### Case: case_030
- **Description**: Leaking injector — rhythmic exhaust pulse signature
- **Gas Chemistry**: HC: 400.0 ppm, CO: 1.8%, CO₂: 13.0%, O₂: 1.0%, NOx: ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): -10.0% / -8.0%, ECU λ: 0.97, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: leaking_injector
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 400 ppm: high — periodic raw-fuel pulses. CO 1.8%: rich. CO2 13.0%: depressed. O2 1.0%: low. NOx unmeasured. λ 0.95: mildly rich; high HC for the modest CO and the rhythmic exhaust pulse signature point to one cylinder receiving extra fuel — a leaking injector, not high global pressure.


## Graph relations (explicit)

**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **CASE-023**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **CASE-031**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **CASE-037**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **CASE-040**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **CSV-018**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **EXP-N003**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **EXP-N013**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **EXT-203**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **EXT-217**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **EXT-227**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **PDF-4G-03**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **PDF-HI-001**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **RULE-CO-1**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **YAML-CSV18**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **YAML-PDF_4G_03**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **YAML-PDF_HI_001**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **YAML-TC12**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_002**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_015**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_017**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_023**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_029**
**labs/comlab/registry/rules/rich_mixture.json** VERIFIES **case_030**
