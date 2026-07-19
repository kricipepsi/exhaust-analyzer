---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-catalyst_failure
implements:
- labs/comlab/registry/rules/catalyst_failure.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_catalyst_failure_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/catalyst_failure.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: catalyst_failure · Parent document: labs/comlab/registry/corpus_curated.csv
# catalyst_failure
21 cases

### Case: CASE-013
- **Description**: CO2 14.5→8.5% at 2500RPM; O2 rises; NOx=800 from combustion temp spike; backpressure pumping loss; VE<60%
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.08%, CO₂: 14.5%, O₂: 0.4%, NOx: 40.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 6.0%, ECU λ: 1.1, MAF: 3.8 g/s
- **DTCs**: P0420
- **Expected Fault**: Clogged_Cat_CO2_Collapse_2500RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.75 – 0.95
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03); OBD λ=1.1 (Δ=-0.09) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: CASE-015
- **Description**: Gas clean (cat working); LTFT=+14% betrays upstream mechanical wear; downstream O2=0.65V steady (cat functional); silent decline
- **Gas Chemistry**: HC: 18.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 0.25%, NOx: 50.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 14.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_LTFT_Elevated_Pre_Cat_Wear
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 18 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.25%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-016
- **Description**: HC rises 180→380 at 2500; cat no longer oxidising; downstream O2 fluctuating (not stored); CO2 depressed
- **Gas Chemistry**: HC: 180.0 ppm, CO: 0.1%, CO₂: 14.5%, O₂: 0.3%, NOx: 50.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 3.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: P0420
- **Expected Fault**: Dead_Catalyst_HC_Breakthrough_At_Load
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CASE-026
- **Description**: Engine healthy; cat heater circuit failed; cat below 300°C light-off even at speed; downstream O2 fluctuating; P0420 set
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.1%, CO₂: 14.5%, O₂: 0.3%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: P0420
- **Expected Fault**: Catalyst_Below_Lightoff_Heater_Failure
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-121
- **Description**: Tailpipe clean (cat doing work) but LTFT>12% reveals upstream rich
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.1%, CO₂: 14.5%, O₂: 0.3%, NOx: 60.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 14.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_Mechanical_Wear
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 30 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 60 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-122
- **Description**: 3-way cat masking ring blow-by; gas perfect; trims betray engine wear
- **Gas Chemistry**: HC: 35.0 ppm, CO: 0.12%, CO₂: 14.3%, O₂: 0.35%, NOx: 55.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 6.0% / 16.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_Mechanical_Wear
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 35 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.12%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.3%: healthy without-cat reference (13–14.5%). O2 0.35%: low — rich consumed the oxygen, or perfect stoich. NOx 55 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N008
- **Description**: 1qt/500mi oil burn; cat masks pre-cat HC; LTFT rising = silent decline
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.2%, CO₂: 15.5%, O₂: 0.1%, NOx: 250.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 13.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_Oil_Burn
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.2%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 250 ppm: moderate idle/light-load combustion temperature. λ 1: in the catalyst window (0.97–1.03).

### Case: EXP-N012
- **Description**: Collapsed muffler baffle; CO2 drops at load; pumping loss; no DTC
- **Gas Chemistry**: HC: 150.0 ppm, CO: 1.1%, CO₂: 9.0%, O₂: 0.8%, NOx: 60.0 ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Exhaust_Restriction_Collapsed_Baffle
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 150 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.1%: mild rich / pre-cat normal (0.5–1.5%). CO2 9%: severely depressed (<11% — large rich/lean misfire or sample dilution). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 60 ppm: low — rich quench or idle without thermal load. λ 0.98: in the catalyst window (0.97–1.03).

### Case: EXT-207
- **Description**: Cat clogged; at idle low exhaust volume passes, CO2=14.5. At 2500 RPM backpressure rises, CO2 drops to 10.5, O2 rises to 5.5. Lambda drifts lean from pumping loss
- **Gas Chemistry**: HC: 35.0 ppm, CO: 0.1%, CO₂: 14.5%, O₂: 0.4%, NOx: 50.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 8.0%, ECU λ: 1.12, MAF: - g/s
- **DTCs**: P0420
- **Expected Fault**: Clogged_Catalytic_Converter_Flow_Restriction
- **Expected State**: named_fault
- **Confidence Range**: 0.73 – 0.93
- **Reasoning**: HC 35 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03); OBD λ=1.12 (Δ=-0.11) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: EXT-208
- **Description**: Melted cat core; flow restriction causes CO2 collapse at 2500 RPM (8.5%). NOx spike from elevated combustion temps. Backpressure >5 psi at 2500
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.08%, CO₂: 14.8%, O₂: 0.3%, NOx: 40.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 6.0%, ECU λ: 1.1, MAF: - g/s
- **DTCs**: P0420
- **Expected Fault**: Catalyst_Melted_Substrate_Exhaust_Restriction
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 40 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03); OBD λ=1.1 (Δ=-0.10) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: EXT-213
- **Description**: Cat working marginally at idle; at 2500 RPM NOx>1000 indicates catalyst incapable of reducing NOx under load. CO2 drop+O2 rise confirms flow restriction
- **Gas Chemistry**: HC: 40.0 ppm, CO: 0.08%, CO₂: 14.5%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 4.0%, ECU λ: 1.1, MAF: 4.0 g/s
- **DTCs**: P0420
- **Expected Fault**: Dead_Catalyst_NOx_Breakthrough_2500RPM
- **Expected State**: named_fault
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 40 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03); OBD λ=1.1 (Δ=-0.09) — ECU sees leaner than chemistry, perception-contradiction symptom (rule 7).

### Case: EXT-232
- **Description**: Cat masking oil burn: gas perfect (λ=1.0, HC=25ppm), but LTFT=+12% reveals persistent lean correction. O2 cross-counts normal. LTFT>+10% is the tell for upstream mechanical wear
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.12%, CO₂: 15.0%, O₂: 0.25%, NOx: 50.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 4.0% / 12.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_LTFT_Elevated_Gas_Clean
- **Expected State**: named_fault
- **Confidence Range**: 0.63 – 0.83
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.12%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 0.25%: low — rich consumed the oxygen, or perfect stoich. NOx 50 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXT-233
- **Description**: Severe oil burn (1qt/500mi); cat completely masks tailpipe. LTFT=+15% is extreme. FF confirms idle-speed operation. Pre-cat gas would show HC>800. Cat doing dangerous work
- **Gas Chemistry**: HC: 18.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.3%, NOx: 35.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 15.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Catalyst_Masking_LTFT_Severe_Oil_Burn
- **Expected State**: named_fault
- **Confidence Range**: 0.6 – 0.8
- **Reasoning**: HC 18 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 35 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: PDF-4G-01
- **Description**: Pre-cat readings; NOx high before cat
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 14.8%, O₂: 0.4%, NOx: 850.0 ppm, λ Analyser: 1.009
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Preconditioning_Catalyst_Out
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 850 ppm: elevated — hot lean burn or stuck-open EGR fingerprint. λ 1.009: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.01) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: PDF-HI-006
- **Description**: Engine healthy; cat not processing
- **Gas Chemistry**: HC: 25.0 ppm, CO: 0.05%, CO₂: 14.5%, O₂: 0.4%, NOx: 80.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: Faulty_Catalyst_Engine_Healthy
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 25 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.4%: low — rich consumed the oxygen, or perfect stoich. NOx 80 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.00) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: REAL-005
- **Description**: Cat failing; NOx>>1000
- **Gas Chemistry**: HC: 166.0 ppm, CO: 1.26%, CO₂: 13.81%, O₂: 0.43%, NOx: 1183.0 ppm, λ Analyser: 0.979
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: P0420
- **Expected Fault**: Dead_Catalyst_NOx_Breakthrough
- **Expected State**: named_fault
- **Confidence Range**: 0.85 – 0.99
- **Reasoning**: HC 166 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 1.26%: mild rich / pre-cat normal (0.5–1.5%). CO2 13.81%: healthy without-cat reference (13–14.5%). O2 0.43%: low — rich consumed the oxygen, or perfect stoich. NOx 1183 ppm: elevated — hot lean burn or stuck-open EGR fingerprint. λ 0.979: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+0.98) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: YAML-PDF_4G_01
- **Description**: Preconditioning - Catalyst Out
- **Gas Chemistry**: HC: 82.0 ppm, CO: 0.6%, CO₂: 15.2%, O₂: 0.5%, NOx: 0.0 ppm, λ Analyser: 1.008843537414966
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: catalyst_failure
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 82 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.6%: mild rich / pre-cat normal (0.5–1.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.00884: in the catalyst window (0.97–1.03).

### Case: YAML-PDF_HI_006
- **Description**: Faulty Catalytic Converter (Engine Healthy)
- **Gas Chemistry**: HC: 110.0 ppm, CO: 0.45%, CO₂: 12.5%, O₂: 1.2%, NOx: 0.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: catalyst_failure
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 110 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.45%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.5%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 1.2%: typical pre-cat residual (0.5–1.5%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1: in the catalyst window (0.97–1.03).

### Case: case_010
- **Description**: P0420 with oil-burning catalyst poisoning (oil_consumption=high)
- **Gas Chemistry**: HC: 180.0 ppm, CO: 0.3%, CO₂: 13.8%, O₂: 1.0%, NOx: 400.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 4.0%, ECU λ: 1.0, RPM: 2500.0, ECT: 95.0°C
- **DTCs**: P0420
- **Expected Fault**: Catalyst_Inefficiency
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.65
- **Reasoning**: HC 180 ppm: moderately elevated; cat is failing to scrub, with oil-vapour HC slipping through. CO 0.3%: low — mixture itself is fine. CO2 13.8%: slightly depressed as the cat is no longer fully oxidising leftovers. O2 1.0%: normal stoich tail. NOx 400 ppm: modestly elevated, the rear cat's reduction stage no longer strips N. λ 1.01: feed gas is balanced — issue is downstream cat efficiency, very plausibly poisoned by oil consumption.

### Case: case_024
- **Description**: Normal idle gases, P0420 set on drive cycle (use freeze frame)
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.01%, CO₂: 15.0%, O₂: 0.2%, NOx: ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0420
- **Expected Fault**: catalyst_failure
- **Expected State**: named_fault
- **Confidence Range**: 0.35 – 0.65
- **Reasoning**: HC 5 ppm: extremely clean idle. CO 0.01%: perfect. CO2 15.0%: near the theoretical ceiling. O2 0.2%: minimal residual. NOx unmeasured at idle. λ 1.00: chemistry says combustion is perfect at idle; the freeze-frame from a 45%-load drive cycle is the only evidence of cat failure — L4 must elevate catalyst_failure despite clean L1 idle gases.

### Case: case_034
- **Description**: Aftermarket catalyst inefficient — high HC, normal CO
- **Gas Chemistry**: HC: 220.0 ppm, CO: 0.3%, CO₂: 13.8%, O₂: 0.8%, NOx: 250.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 5.0% / 4.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0420
- **Expected Fault**: aftermarket_catalyst_inefficient
- **Expected State**: named_fault
- **Confidence Range**: 0.4 – 0.7
- **Reasoning**: HC 220 ppm: elevated — cat is failing to oxidise HC effectively. CO 0.3%: normal — oxidation step is partly working. CO2 13.8%: slightly depressed. O2 0.8%: typical. NOx 250 ppm: moderate, reduction stage marginal. λ 1.01: chemistry says feed gas is fine; the high HC with normal CO is the tired-aftermarket-cat fingerprint.


## Graph relations (explicit)

**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CASE-013**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CASE-015**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CASE-016**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CASE-026**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CSV-121**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **CSV-122**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXP-N008**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXP-N012**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXT-207**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXT-208**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXT-213**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXT-232**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **EXT-233**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **PDF-4G-01**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **PDF-HI-006**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **REAL-005**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **YAML-PDF_4G_01**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **YAML-PDF_HI_006**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **case_010**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **case_024**
**labs/comlab/registry/rules/catalyst_failure.json** VERIFIES **case_034**
