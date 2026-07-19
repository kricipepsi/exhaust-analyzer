---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-lean_condition
implements:
- labs/comlab/registry/rules/lean_condition.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_lean_condition_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/lean_condition.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: lean_condition · Parent document: labs/comlab/registry/corpus_curated.csv
# lean_condition
53 cases

### Case: CASE-011
- **Description**: Lambda 1.25→1.02 at 2500RPM; STFT drops +20→+2; classic idle-only vacuum leak signature; PCV hose split
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.03%, CO₂: 11.5%, O₂: 4.5%, NOx: 280.0 ppm, λ Analyser: 1.25
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 18.0%, ECU λ: 1.18, MAF: 3.0 g/s
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_Clears_At_2500RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.03%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 280 ppm: moderate idle/light-load combustion temperature. λ 1.25: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CASE-012
- **Description**: Idle stoich; 2500RPM lean(1.18); STFT+22% at speed; failing fuel pump volume; worsens opposite to vacuum leak
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.06%, CO₂: 14.5%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 12.0%, ECU λ: 1.08, MAF: 3.8 g/s
- **DTCs**: P0171
- **Expected Fault**: Fuel_Delivery_Restriction_Lean_Under_Load
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03).

### Case: CASE-017
- **Description**: Unmetered air enters via split PCV hose; MAP=45kPa high; lambda 1.15→1.00 at 2500RPM as manifold vacuum drops
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.03%, CO₂: 11.5%, O₂: 4.5%, NOx: 300.0 ppm, λ Analyser: 1.15
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 15.0%, ECU λ: 1.12, MAF: 2.8 g/s
- **DTCs**: P0171
- **Expected Fault**: PCV_Hose_Split_Idle_Vacuum_Leak_Clears
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 80 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.03%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 300 ppm: moderate idle/light-load combustion temperature. λ 1.15: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CASE-019
- **Description**: MAF idle=2.2g/s (expected 3.5); fails double-displacement rule; lean worsens at 2500; LTFT+16% confirms persistent lean
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.1%, CO₂: 13.5%, O₂: 0.5%, NOx: 55.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 16.0%, ECU λ: 1.08, MAF: 2.2 g/s
- **DTCs**: P0171
- **Expected Fault**: MAF_Dirty_HotFilm_Lean_Under_Load
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 30 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 55 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03).

### Case: CASE-020
- **Description**: HC 1800→250 at 2500RPM; NOx=8ppm key discriminator (lean would be >300); EGR dilutes less at higher airflow; P0401 confirms
- **Gas Chemistry**: HC: 1800.0 ppm, CO: 1.8%, CO₂: 12.5%, O₂: 1.2%, NOx: 8.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): -2.0% / -2.0%, ECU λ: 0.99, MAF: 3.5 g/s
- **DTCs**: P0401
- **Expected Fault**: EGR_Stuck_Open_HC_Clears_2500RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1800 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 8 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: CASE-025
- **Description**: Idle normal; rich only at 2500RPM cruise; FF=2200RPM 55% LOAD; purge duty=95%; vapor floods intake under engine load
- **Gas Chemistry**: HC: 40.0 ppm, CO: 0.2%, CO₂: 14.0%, O₂: 0.4%, NOx: 45.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): -18.0% / -12.0%, ECU λ: 0.97, MAF: 3.5 g/s
- **DTCs**: P0172
- **Expected Fault**: EVAP_Purge_Valve_Stuck_Open_Cruise_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 40 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.2%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 45 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-027
- **Description**: Boot tears under torque at WOT; FF=100% LOAD 35km/h confirms load-dependent; lambda severely lean at 2500RPM from unmetered air ingestion
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 11.0%, O₂: 4.0%, NOx: 150.0 ppm, λ Analyser: 1.22
- **OBD / Air / Engine**: Trims B1 (ST/LT): 22.0% / 18.0%, ECU λ: 1.2, MAF: 3.0 g/s
- **DTCs**: P0101
- **Expected Fault**: Intake_Boot_Tear_WOT_Load_Lean_P0101
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 150 ppm: moderate idle/light-load combustion temperature. λ 1.22: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CASE-030
- **Description**: Carbon deposits form mechanical air bypass around closed throttle plate; idle high at 1100RPM; TPS=0%; slight lean trim
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.1%, CO₂: 14.0%, O₂: 0.8%, NOx: 50.0 ppm, λ Analyser: 1.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 8.0%, ECU λ: 1.03, MAF: 3.5 g/s
- **DTCs**: P0507
- **Expected Fault**: Throttle_Body_Carbon_Idle_Speed_High
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 1.05: lean (≥1.05) — Brettschneider chemistry.

### Case: CASE-032
- **Description**: Turbo seal allows oil into intercooler; HC spikes only under boost pressure (>2500RPM at load); idle clean; no DTC
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 14.8%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Turbo_Intercooler_Oil_Soak_HC_Under_Boost
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-034
- **Description**: Wastegate open; no boost builds; MAF_2500=8.0g/s (expected 14+); gas stays stoich (ECU adapts); VE<70%; P0299 underboost
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.08%, CO₂: 14.0%, O₂: 0.5%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: P0299
- **Expected Fault**: Turbo_Wastegate_Stuck_Open_Low_Boost
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-036
- **Description**: GDI injector tip deposits impair high-pressure atomisation under load; idle ok; lean at 2500RPM; LTFT+18% confirms
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 14.5%, O₂: 0.3%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 18.0%, ECU λ: 1.05, MAF: 3.5 g/s
- **DTCs**: P0171
- **Expected Fault**: GDI_Injector_Tip_Fouling_Lean_At_Speed
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-016
- **Description**: λ corrected 1.200→1.271
- **Gas Chemistry**: HC: 45.0 ppm, CO: 0.02%, CO₂: 11.5%, O₂: 4.5%, NOx: 120.0 ppm, λ Analyser: 1.271
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 12.0%, ECU λ: 1.18
- **DTCs**: P0171
- **Expected Fault**: Mechanical_Lean_Vacuum_Leak
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 45 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 120 ppm: moderate idle/light-load combustion temperature. λ 1.271: lean (≥1.05) — Brettschneider chemistry; OBD λ=1.18 (Δ=+0.09) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-068
- **Description**: Gas perfect; false lean DTC
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.08%, CO₂: 15.2%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / -2.0%, ECU λ: 1.0
- **DTCs**: P0171
- **Expected Fault**: Ghost_Lean_DTC_False_Trigger
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-100
- **Description**: λ corrected 0.700→0.750
- **Gas Chemistry**: HC: 400.0 ppm, CO: 8.0%, CO₂: 8.0%, O₂: 0.1%, NOx: 10.0 ppm, λ Analyser: 0.75
- **OBD / Air / Engine**: Trims B1 (ST/LT): -25.0% / -15.0%, ECU λ: 0.75
- **DTCs**: P0172
- **Expected Fault**: Severe_Intake_Restriction
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 400 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 8%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 8%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 10 ppm: low — rich quench or idle without thermal load. λ 0.75: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: CSV-109
- **Description**: Lean at idle only; trims clear at 2500rpm; PCV vacuum hose split
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.05%, CO₂: 12.0%, O₂: 3.5%, NOx: 250.0 ppm, λ Analyser: 1.18
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 12.0%, ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_Idle_Only
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 80 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 250 ppm: moderate idle/light-load combustion temperature. λ 1.18: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-110
- **Description**: Idle-only vacuum leak; intake manifold gasket; trims normal at speed
- **Gas Chemistry**: HC: 95.0 ppm, CO: 0.04%, CO₂: 11.8%, O₂: 4.0%, NOx: 280.0 ppm, λ Analyser: 1.2
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 14.0%, ECU λ: 1.17
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_Idle_Only
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 95 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.04%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 280 ppm: moderate idle/light-load combustion temperature. λ 1.2: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-111
- **Description**: Idle perfect; 2500rpm lean: failing fuel pump; high-load lean
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.1%, CO₂: 13.0%, O₂: 2.8%, NOx: 180.0 ppm, λ Analyser: 1.13
- **OBD / Air / Engine**: Trims B1 (ST/LT): 15.0% / 10.0%, ECU λ: 1.12
- **DTCs**: P0174
- **Expected Fault**: Fuel_Delivery_Lean_High_RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 2.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 180 ppm: moderate idle/light-load combustion temperature. λ 1.13: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-112
- **Description**: Restricted fuel filter; lean only under load; idle stoich ok
- **Gas Chemistry**: HC: 75.0 ppm, CO: 0.08%, CO₂: 12.8%, O₂: 3.0%, NOx: 220.0 ppm, λ Analyser: 1.14
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 12.0%, ECU λ: 1.13
- **DTCs**: P0171
- **Expected Fault**: Fuel_Delivery_Lean_High_RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 75 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 220 ppm: moderate idle/light-load combustion temperature. λ 1.14: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: CSV-113
- **Description**: EGR stuck open; HC>>1500; NOx<15ppm key discriminator; stoich λ
- **Gas Chemistry**: HC: 1700.0 ppm, CO: 2.3%, CO₂: 12.4%, O₂: 2.65%, NOx: 12.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): -2.0% / 0.0%, ECU λ: 0.99
- **DTCs**: P0401
- **Expected Fault**: EGR_Stuck_Open_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1700 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 2.3%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.4%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.65%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 12 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: CSV-114
- **Description**: EGR valve seized open; rough idle; NOx near zero
- **Gas Chemistry**: HC: 1850.0 ppm, CO: 2.5%, CO₂: 12.2%, O₂: 2.85%, NOx: 8.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): -3.0% / -1.0%, ECU λ: 0.99
- **DTCs**: P0401
- **Expected Fault**: EGR_Stuck_Open_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1850 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 2.5%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.2%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.85%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 8 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: EXP-N001
- **Description**: 1999 brake-booster diaphragm; lean only when brake pedal depressed
- **Gas Chemistry**: HC: 90.0 ppm, CO: 0.05%, CO₂: 12.5%, O₂: 3.0%, NOx: 230.0 ppm, λ Analyser: 1.14
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 6.0%, ECU λ: 1.1
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_Brake_Booster_Transient
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 90 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 230 ppm: moderate idle/light-load combustion temperature. λ 1.14: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXP-N009
- **Description**: 2006 dirty MAF; under-reports air; ECU under-fuels; physical lean
- **Gas Chemistry**: HC: 70.0 ppm, CO: 0.05%, CO₂: 12.0%, O₂: 2.5%, NOx: 240.0 ppm, λ Analyser: 1.13
- **OBD / Air / Engine**: Trims B1 (ST/LT): 14.0% / 16.0%, ECU λ: 1.1
- **DTCs**: P0171
- **Expected Fault**: MAF_Underreport_Dust
- **Expected State**: named_fault
- **Confidence Range**: 0.71 – 0.91
- **Reasoning**: HC 70 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 240 ppm: moderate idle/light-load combustion temperature. λ 1.13: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXP-N010
- **Description**: Purge valve flooding intake with vapor; trims neg; ECU EVAP fault DTC
- **Gas Chemistry**: HC: 280.0 ppm, CO: 1.8%, CO₂: 13.2%, O₂: 0.8%, NOx: 30.0 ppm, λ Analyser: 0.93
- **OBD / Air / Engine**: Trims B1 (ST/LT): -15.0% / -8.0%, ECU λ: 0.95
- **DTCs**: P0441
- **Expected Fault**: EVAP_Purge_Stuck_Open
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 280 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 13.2%: healthy without-cat reference (13–14.5%). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 30 ppm: low — rich quench or idle without thermal load. λ 0.93: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXP-N011
- **Description**: Cracked PCV hose intermittent; idle hunts; trims swing -10 to +10
- **Gas Chemistry**: HC: 180.0 ppm, CO: 0.15%, CO₂: 13.5%, O₂: 1.5%, NOx: 90.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: PCV_Hose_Cracked_Intermittent
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.15%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1.5%: typical pre-cat residual (0.5–1.5%). NOx 90 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03).

### Case: EXP-N014
- **Description**: Carbon on intake valves soaks fuel cold; releases warm; HC spike on warm-up
- **Gas Chemistry**: HC: 800.0 ppm, CO: 1.2%, CO₂: 12.5%, O₂: 1.0%, NOx: 50.0 ppm, λ Analyser: 0.94
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 5.0%, ECU λ: 1.02
- **DTCs**: No DTCs stored
- **Expected Fault**: GDI_Intake_Carbon_Sequestration
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 800 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.2%: mild rich / pre-cat normal (0.5–1.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 0.94: rich (≤0.95) — chemistry says excess fuel; OBD λ=1.02 (Δ=-0.08) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: EXP-N017
- **Description**: Torn bypass diaphragm; air recirculates; rich at boost; idle ok
- **Gas Chemistry**: HC: 220.0 ppm, CO: 1.5%, CO₂: 13.0%, O₂: 0.6%, NOx: 40.0 ppm, λ Analyser: 0.92
- **OBD / Air / Engine**: Trims B1 (ST/LT): -12.0% / -8.0%, ECU λ: 0.95
- **DTCs**: P0299
- **Expected Fault**: Turbo_Bypass_Valve_Leak
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 220 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.6%: typical pre-cat residual (0.5–1.5%). NOx 40 ppm: low — rich quench or idle without thermal load. λ 0.92: rich (≤0.95) — chemistry says excess fuel.

### Case: EXT-201
- **Description**: PCV hose cracked; lean at idle clears at 2500 RPM. Trims drop from +20% to +3% at speed. FF confirms idle-speed fault
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.02%, CO₂: 12.0%, O₂: 4.5%, NOx: 280.0 ppm, λ Analyser: 1.22
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 18.0%, ECU λ: 1.18, MAF: 3.2 g/s
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_PCV_Hose_Idle_Only
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 60 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 280 ppm: moderate idle/light-load combustion temperature. λ 1.22: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXT-202
- **Description**: Idle-only lean; intake manifold gasket leak seals as manifold expands with heat. Trims normalise above 2000 RPM
- **Gas Chemistry**: HC: 55.0 ppm, CO: 0.03%, CO₂: 11.8%, O₂: 4.8%, NOx: 300.0 ppm, λ Analyser: 1.25
- **OBD / Air / Engine**: Trims B1 (ST/LT): 22.0% / 20.0%, ECU λ: 1.2, MAF: 2.8 g/s
- **DTCs**: P0171
- **Expected Fault**: Vacuum_Leak_Intake_Manifold_Gasket
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 55 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.03%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.8%: severe lean / large misfire / air leak (>4%). NOx 300 ppm: moderate idle/light-load combustion temperature. λ 1.25: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXT-204
- **Description**: Fuel filter partially clogged; idle fuel demand met, but at 2500 RPM flow restriction causes lean condition. LTFT rises with load
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.06%, CO₂: 14.5%, O₂: 0.3%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 12.0% / 14.0%, ECU λ: 1.08, MAF: 4.1 g/s
- **DTCs**: P0171
- **Expected Fault**: Fuel_Delivery_Restricted_Fuel_Filter_Lean_High_RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.06%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03); OBD λ=1.08 (Δ=-0.08) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: EXT-205
- **Description**: Fuel pump worn; idle pressure okay, but under sustained 2500 RPM load, rail pressure drops, causing progressive lean condition
- **Gas Chemistry**: HC: 18.0 ppm, CO: 0.05%, CO₂: 14.8%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 10.0%, ECU λ: 1.06, MAF: 3.8 g/s
- **DTCs**: P0171
- **Expected Fault**: Fuel_Delivery_Failing_Fuel_Pump_Voltage_Droop
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 18 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXT-206
- **Description**: EVAP purge valve stuck open; fuel vapours flood intake at cruise. Idle nearly normal due to lower purge flow. Rich only at 2500 RPM
- **Gas Chemistry**: HC: 50.0 ppm, CO: 0.15%, CO₂: 13.0%, O₂: 0.5%, NOx: 60.0 ppm, λ Analyser: 1.02
- **OBD / Air / Engine**: Trims B1 (ST/LT): -18.0% / -10.0%, ECU λ: 0.94, MAF: - g/s
- **DTCs**: P0172
- **Expected Fault**: EVAP_Purge_Valve_Stuck_Open_Load_Rich
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 50 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.15%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 60 ppm: low — rich quench or idle without thermal load. λ 1.02: in the catalyst window (0.97–1.03); OBD λ=0.94 (Δ=+0.08) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: EXT-211
- **Description**: EGR valve stuck wide open at idle; HC>1800, NOx<20 (key discriminator). At 2500 RPM EGR dilutes less relative to total charge, HC drops to 250, NOx rises to 150
- **Gas Chemistry**: HC: 1800.0 ppm, CO: 1.8%, CO₂: 12.5%, O₂: 1.2%, NOx: 15.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): -2.0% / -2.0%, ECU λ: 0.99, MAF: - g/s
- **DTCs**: P0401
- **Expected Fault**: EGR_Stuck_Open_Idle_Rough
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1800 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 1.8%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 15 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: EXT-212
- **Description**: EGR seized open; NOx near zero at idle. Cold-start stall tendency. At 2500 RPM idle smooths but HC remains elevated. EGR exhaust passage carbon-packed
- **Gas Chemistry**: HC: 1950.0 ppm, CO: 2.0%, CO₂: 12.2%, O₂: 1.4%, NOx: 12.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): -3.0% / -3.0%, ECU λ: 0.98, MAF: - g/s
- **DTCs**: P0401
- **Expected Fault**: EGR_Valve_Seized_Open_Cold_Start_Stall
- **Expected State**: named_fault
- **Confidence Range**: 0.8 – 0.99
- **Reasoning**: HC 1950 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 2%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.2%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.4%: typical pre-cat residual (0.5–1.5%). NOx 12 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: EXT-214
- **Description**: Brake booster diaphragm intermittent leak; vacuum leak only when brake pedal depressed. FF captured at idle, 0 km/h, low load. Trims spike on brake application
- **Gas Chemistry**: HC: 90.0 ppm, CO: 0.04%, CO₂: 11.5%, O₂: 4.5%, NOx: 300.0 ppm, λ Analyser: 1.22
- **OBD / Air / Engine**: Trims B1 (ST/LT): 16.0% / 14.0%, ECU λ: 1.18, MAF: - g/s
- **DTCs**: P0171
- **Expected Fault**: Intake_Vacuum_Leak_Brake_Booster_Diaphragm
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 90 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.04%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 300 ppm: moderate idle/light-load combustion temperature. λ 1.22: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXT-215
- **Description**: Throttle body gasket weeping; trims +18% idle, drop to +3% at 2500. FF=idle confirms idle-only leak. Carb cleaner test positive at TB flange
- **Gas Chemistry**: HC: 85.0 ppm, CO: 0.05%, CO₂: 11.0%, O₂: 5.0%, NOx: 310.0 ppm, λ Analyser: 1.26
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 15.0%, ECU λ: 1.2, MAF: - g/s
- **DTCs**: P0171
- **Expected Fault**: Intake_Vacuum_Leak_Throttle_Body_Gasket
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 85 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 5%: severe lean / large misfire / air leak (>4%). NOx 310 ppm: moderate idle/light-load combustion temperature. λ 1.26: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXT-218
- **Description**: Dirty MAF sensor under-reports airflow; ECU under-fuels. Physical lean (λ=1.15 gas). LTFT+16%. FF at 2200 RPM cruise. MAF=2.4 g/s at idle (expected ~3.5)
- **Gas Chemistry**: HC: 70.0 ppm, CO: 0.08%, CO₂: 13.0%, O₂: 2.5%, NOx: 250.0 ppm, λ Analyser: 1.15
- **OBD / Air / Engine**: Trims B1 (ST/LT): 14.0% / 16.0%, ECU λ: 1.12, MAF: 2.4 g/s
- **DTCs**: P0171
- **Expected Fault**: MAF_Underreport_Dirty_HotFilm
- **Expected State**: named_fault
- **Confidence Range**: 0.71 – 0.91
- **Reasoning**: HC 70 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 2.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 250 ppm: moderate idle/light-load combustion temperature. λ 1.15: lean (≥1.05) — Brettschneider chemistry. Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: EXT-240
- **Description**: Purge valve stuck open flooding intake with fuel vapour. FF: 2200 RPM cruise, 55% LOAD. Trims negative at -12%/-10%. Fuel smell at canister vent. P0441 confirms EVAP fault
- **Gas Chemistry**: HC: 280.0 ppm, CO: 1.5%, CO₂: 12.8%, O₂: 0.6%, NOx: 45.0 ppm, λ Analyser: 0.96
- **OBD / Air / Engine**: Trims B1 (ST/LT): -12.0% / -10.0%, ECU λ: 0.97, MAF: 3.9 g/s
- **DTCs**: P0441
- **Expected Fault**: EVAP_Purge_Stuck_Open_Rich_FF_Cruise
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 280 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 1.5%: mild rich / pre-cat normal (0.5–1.5%). CO2 12.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.6%: typical pre-cat residual (0.5–1.5%). NOx 45 ppm: low — rich quench or idle without thermal load. λ 0.96: borderline rich (0.95–0.97).

### Case: MECH-003
- **Description**: Lean; high NOx from combustion temp
- **Gas Chemistry**: HC: 180.0 ppm, CO: 0.1%, CO₂: 13.2%, O₂: 3.8%, NOx: 200.0 ppm, λ Analyser: 1.18
- **OBD / Air / Engine**: Trims B1 (ST/LT): 18.0% / 12.0%, ECU λ: 1.15
- **DTCs**: P0171
- **Expected Fault**: Intake_Vacuum_Leak
- **Expected State**: named_fault
- **Confidence Range**: 0.77 – 0.97
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.2%: healthy without-cat reference (13–14.5%). O2 3.8%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 200 ppm: moderate idle/light-load combustion temperature. λ 1.18: lean (≥1.05) — Brettschneider chemistry.

### Case: MECH-005
- **Description**: GDI deposits; HC spikes cold-start
- **Gas Chemistry**: HC: 850.0 ppm, CO: 0.4%, CO₂: 13.5%, O₂: 1.0%, NOx: 65.0 ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): -3.0% / -2.0%, ECU λ: 0.99
- **DTCs**: No DTCs stored
- **Expected Fault**: GDI_Carbon_Intake_Buildup
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 850 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 0.4%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 1%: typical pre-cat residual (0.5–1.5%). NOx 65 ppm: low — rich quench or idle without thermal load. λ 0.98: in the catalyst window (0.97–1.03).

### Case: REAL-002
- **Description**: No-start lean; fuel starvation
- **Gas Chemistry**: HC: 2937.0 ppm, CO: 0.025%, CO₂: 2.98%, O₂: 16.75%, NOx: 141.0 ppm, λ Analyser: 3.05
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Lean_No_Start_Fuel_Pump
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 2937 ppm: extreme — almost always mechanical (rings, valve sealing) or hard ignition fault (>2000 ppm). CO 0.025%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 2.98%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 16.75%: severe lean / large misfire / air leak (>4%). NOx 141 ppm: moderate idle/light-load combustion temperature. λ 3.05: cranking / no-combustion shape (master_gas_guide §3 rule 8 — route to non-starter pipeline); OBD λ=0 (Δ=+3.05) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO≈0 → lean misfire (rule 2): the fuel never lit.

### Case: REAL-004
- **Description**: NOx=13ppm key EGR discriminator
- **Gas Chemistry**: HC: 1663.0 ppm, CO: 2.27%, CO₂: 12.52%, O₂: 2.71%, NOx: 13.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: P0401
- **Expected Fault**: EGR_Stuck_Open_Idle
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 1663 ppm: severe misfire / oil burn / catalyst failure band (>800 ppm). CO 2.27%: clear rich (1.5–3% — combustion ran out of oxygen). CO2 12.52%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 2.71%: elevated alongside high CO — rich-misfire fingerprint (fuel dumped, never lit). NOx 13 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+0.99) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: HC↑ + O2↑ + CO↑ → rich misfire (rule 3): fuel dumped, partial burn.

### Case: TC-011
- **Description**: TC11 from diag.md; λ corrected 1.18→1.271
- **Gas Chemistry**: HC: 45.0 ppm, CO: 0.02%, CO₂: 11.5%, O₂: 4.5%, NOx: 120.0 ppm, λ Analyser: 1.271
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.18
- **DTCs**: P0171
- **Expected Fault**: Mechanical_Lean_Vacuum_Leak_TC
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 45 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 4.5%: severe lean / large misfire / air leak (>4%). NOx 120 ppm: moderate idle/light-load combustion temperature. λ 1.271: lean (≥1.05) — Brettschneider chemistry; OBD λ=1.18 (Δ=+0.09) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: YAML-CSV68
- **Description**: Ghost_Lean_DTC_False_Trigger
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.08%, CO₂: 15.2%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0171
- **Expected Fault**: Ghost_Lean_DTC_False_Trigger
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 10 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: case_003
- **Description**: Borderline lean with slight vacuum leak (L1 only)
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 2.8%, NOx: 350.0 ppm, λ Analyser: 1.06
- **OBD / Air / Engine**: RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: lean_condition
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.55
- **Reasoning**: HC 80 ppm: slightly elevated from incipient lean-misfire pulses. CO 0.05%: near zero — lean burn has surplus oxygen so no rich CO. CO2 13.5%: depressed because the lean burn loses efficiency. O2 2.8%: well above the 1.5% ceiling, classic lean tail. NOx 350 ppm: mildly elevated — lean chamber runs hotter (HC↔NOx anti-correlation). λ 1.06: chemistry says lean (>1.05), consistent with a small vacuum leak; L1-only must still return lean_condition.

### Case: case_008
- **Description**: Dual-bank lean on Bank 2 only (V-engine intake leak)
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.1%, CO₂: 14.2%, O₂: 1.8%, NOx: 250.0 ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, Trims B2 (ST/LT): 28.0% / 26.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0174
- **Expected Fault**: bank_specific_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.3 – 0.65
- **Reasoning**: HC 60 ppm: low at the common tailpipe because half the cylinders burn cleanly. CO 0.1%: minimal, no rich offset. CO2 14.2%: only mildly depressed since most cylinders combust normally. O2 1.8%: slightly elevated from bank 2's lean air slipping through. NOx 250 ppm: moderately elevated, hot lean burn on the affected bank. λ 1.03: only mildly lean overall because bank 1 dilutes bank 2's signature; bank-specific trims (B2 +28%) reveal the isolated leak.

### Case: case_016
- **Description**: NOx-only lean condition (5-gas analyser)
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.05%, CO₂: 14.0%, O₂: 0.8%, NOx: 1200.0 ppm, λ Analyser: 1.03
- **OBD / Air / Engine**: RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: lean_condition
- **Expected State**: named_fault
- **Confidence Range**: 0.45 – 0.75
- **Reasoning**: HC 30 ppm: low — combustion is mostly complete. CO 0.05%: essentially zero, not rich. CO2 14.0%: near ideal. O2 0.8%: only slightly elevated. NOx 1200 ppm: very high — when other gases look clean, only a hot lean burn produces this signature. λ 1.03: slightly lean confirms the diagnosis; NOx is the dominant diagnostic clue.

### Case: case_018
- **Description**: Lean misfire with both P0171 and P0300
- **Gas Chemistry**: HC: 900.0 ppm, CO: 0.1%, CO₂: 13.0%, O₂: 2.5%, NOx: 600.0 ppm, λ Analyser: 1.07
- **OBD / Air / Engine**: Trims B1 (ST/LT): 22.0% / 20.0%, ECU λ: 1.12, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171|P0300
- **Expected Fault**: lean_condition
- **Expected State**: named_fault
- **Confidence Range**: 0.5 – 0.8
- **Reasoning**: HC 900 ppm: very high — lean misfire dumps unburned fuel. CO 0.1%: near zero, no rich. CO2 13.0%: clearly depressed by lean misfire. O2 2.5%: elevated, classic lean-misfire signature. NOx 600 ppm: elevated from hot lean combustion outside misfire pulses. λ 1.07: clearly lean — ECU and chemistry agree, lean is the likely root cause of the random misfire.

### Case: case_019
- **Description**: Stuck-open EGR causing lean idle and high NOx
- **Gas Chemistry**: HC: 150.0 ppm, CO: 0.05%, CO₂: 12.5%, O₂: 3.0%, NOx: 1500.0 ppm, λ Analyser: 1.1
- **OBD / Air / Engine**: Trims B1 (ST/LT): 15.0% / 12.0%, ECU λ: 1.08, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0401
- **Expected Fault**: egr_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 150 ppm: moderately elevated — EGR-induced flame-front instability lets some HC slip. CO 0.05%: near zero, no rich. CO2 12.5%: depressed because EGR dilutes the charge and lean burn is inefficient. O2 3.0%: clearly elevated, lean tail. NOx 1500 ppm: extreme — without EGR closing properly, peak temperature rises uncontrolled. λ 1.10: strongly lean; the very-high NOx + lean + idle pattern is the classic stuck-open EGR fingerprint.

### Case: case_031
- **Description**: PCV valve stuck open — lean idle, normal off-idle
- **Gas Chemistry**: HC: 90.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 3.0%, NOx: ppm, λ Analyser: 1.07
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 22.0%, ECU λ: 1.1, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171
- **Expected Fault**: pcv_fault
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 90 ppm: slightly elevated. CO 0.05%: near zero, not rich. CO2 13.5%: depressed by lean burn. O2 3.0%: clearly elevated, lean. NOx unmeasured. λ 1.07: clearly lean; combined with idle-only +25% trims the unmetered air enters via PCV — the leak goes away off-idle as manifold vacuum drops.

### Case: case_032
- **Description**: MAF underreporting (false-lean DTC, real lean condition)
- **Gas Chemistry**: HC: 50.0 ppm, CO: 0.02%, CO₂: 14.0%, O₂: 3.5%, NOx: ppm, λ Analyser: 1.09
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 18.0%, ECU λ: 1.12, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171
- **Expected Fault**: contaminated_maf
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 50 ppm: low — lean condition is steady, not misfiring. CO 0.02%: near zero, not rich. CO2 14.0%: slightly depressed. O2 3.5%: clearly elevated, lean. NOx unmeasured. λ 1.09: clearly lean; ECU and chemistry agree, but the under-reading MAF means trims chase a phantom — the fault is the sensor, not a vacuum leak.

### Case: case_047
- **Description**: P0455 large EVAP leak with stuck-open purge (lean idle)
- **Gas Chemistry**: HC: 80.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 3.0%, NOx: ppm, λ Analyser: 1.07
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 18.0%, ECU λ: 1.1, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0455|P0171
- **Expected Fault**: evap_leak
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 80 ppm: slightly elevated. CO 0.05%: near zero. CO2 13.5%: depressed. O2 3.0%: clearly elevated, lean. NOx unmeasured. λ 1.07: clearly lean; with P0455 (large evap leak) plus P0171, the purge valve is bleeding unmetered air into the manifold.

### Case: case_048
- **Description**: P0171 + P0174 — common vacuum leak after MAF (both banks lean)
- **Gas Chemistry**: HC: 60.0 ppm, CO: 0.05%, CO₂: 13.5%, O₂: 3.0%, NOx: ppm, λ Analyser: 1.07
- **OBD / Air / Engine**: Trims B1 (ST/LT): 25.0% / 22.0%, Trims B2 (ST/LT): 24.0% / 21.0%, ECU λ: 1.12, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171|P0174
- **Expected Fault**: vacuum_leak
- **Expected State**: named_fault
- **Confidence Range**: 0.45 – 0.75
- **Reasoning**: HC 60 ppm: slightly elevated. CO 0.05%: near zero. CO2 13.5%: depressed by lean burn. O2 3.0%: clearly elevated. NOx unmeasured. λ 1.07: clearly lean on both banks; symmetric +25%/+24% trims and matching B1+B2 lean DTCs point to a common downstream-of-MAF vacuum leak feeding both intakes.

### Case: case_050
- **Description**: Rotated/dirty MAF — under-reads airflow (lean DTCs)
- **Gas Chemistry**: HC: 50.0 ppm, CO: 0.02%, CO₂: 14.0%, O₂: 3.2%, NOx: ppm, λ Analyser: 1.09
- **OBD / Air / Engine**: Trims B1 (ST/LT): 26.0% / 24.0%, ECU λ: 1.13, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171|P0102
- **Expected Fault**: contaminated_maf
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 50 ppm: low — no misfire. CO 0.02%: near zero. CO2 14.0%: slightly depressed. O2 3.2%: clearly elevated, lean. NOx unmeasured. λ 1.09: clearly lean and ECU agrees; combined with P0102 (MAF low input) the MAF is the under-reporting source of the lean condition, not a vacuum leak.


## Graph relations (explicit)

**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-011**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-012**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-017**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-019**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-020**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-025**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-027**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-030**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-032**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-034**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CASE-036**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-016**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-068**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-100**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-109**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-110**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-111**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-112**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-113**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **CSV-114**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N001**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N009**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N010**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N011**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N014**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXP-N017**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-201**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-202**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-204**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-205**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-206**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-211**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-212**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-214**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-215**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-218**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **EXT-240**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **MECH-003**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **MECH-005**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **REAL-002**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **REAL-004**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **TC-011**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **YAML-CSV68**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_003**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_008**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_016**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_018**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_019**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_031**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_032**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_047**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_048**
**labs/comlab/registry/rules/lean_condition.json** VERIFIES **case_050**
