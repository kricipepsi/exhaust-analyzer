---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-no_fault
implements:
- labs/comlab/registry/rules/no_fault.json
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_no_fault_rules.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/no_fault.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: no_fault · Parent document: labs/comlab/registry/corpus_curated.csv
# no_fault
17 cases

### Case: CASE-009
- **Description**: Standard E10 petrol; Gas-Sum=15.5(CO2+O2); Ocv=0.054 applied; Hcv=1.84; stoichiometric reference
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.3%, NOx: 28.0 ppm, λ Analyser: 1.008
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 1.0%, ECU λ: 1.0, MAF: 3.5 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: E10_Healthy_Baseline_Gas_Sum_Check
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 28 ppm: low — rich quench or idle without thermal load. λ 1.008: in the catalyst window (0.97–1.03).

### Case: CSV-001
- **Description**: Perfect stoich with cat
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.3%, NOx: 25.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 2.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 25 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-005
- **Description**: Clean burn; slight lean trim
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 15.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): -1.0% / 0.0%, ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 15 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: CSV-127
- **Description**: Normal cold-start enrichment phase; expected ~30s after key-on
- **Gas Chemistry**: HC: 180.0 ppm, CO: 0.45%, CO₂: 13.8%, O₂: 0.55%, NOx: 45.0 ppm, λ Analyser: 0.99
- **OBD / Air / Engine**: Trims B1 (ST/LT): 8.0% / 0.0%, ECU λ: 0.99
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 180 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.45%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.8%: healthy without-cat reference (13–14.5%). O2 0.55%: typical pre-cat residual (0.5–1.5%). NOx 45 ppm: low — rich quench or idle without thermal load. λ 0.99: in the catalyst window (0.97–1.03).

### Case: CSV-128
- **Description**: Cold-start: rich enrichment + retarded timing for fast cat light-off
- **Gas Chemistry**: HC: 220.0 ppm, CO: 0.5%, CO₂: 13.5%, O₂: 0.6%, NOx: 50.0 ppm, λ Analyser: 0.98
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 0.0%, ECU λ: 0.98
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 220 ppm: minor inefficiency band (50–250 ppm — pre-cat normal or marginal misfire). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13.5%: healthy without-cat reference (13–14.5%). O2 0.6%: typical pre-cat residual (0.5–1.5%). NOx 50 ppm: low — rich quench or idle without thermal load. λ 0.98: in the catalyst window (0.97–1.03).

### Case: EXT-216
- **Description**: Cold start at ECT=45°C; open-loop enrichment. STFT and LTFT both -25% (normal cold-start fuel trim authority). Confirmed warm-up phase; not a fault
- **Gas Chemistry**: HC: 650.0 ppm, CO: 5.5%, CO₂: 11.0%, O₂: 0.2%, NOx: 15.0 ppm, λ Analyser: 0.82
- **OBD / Air / Engine**: Trims B1 (ST/LT): -25.0% / -25.0%, ECU λ: 0.78, MAF: - g/s
- **DTCs**: P0172
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 650 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 5.5%: very rich (>3% — expect concurrent HC rise once rich-misfire threshold is crossed). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 15 ppm: low — rich quench or idle without thermal load. λ 0.82: rich (≤0.95) — chemistry says excess fuel. Pattern: CO↑ + O2↓ → classic rich (rule 1).

### Case: EXT-220
- **Description**: Perfect baseline with freeze frame data. FF captured at hot idle: ECT=89°C, LOAD=15%, RPM=720. All PIDs nominal
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.2%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, MAF: 3.6 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.2%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: EXT-231
- **Description**: Benchmark healthy O2: cross-counts=22 per 10 sec. Fast, symmetric switching 0.2-0.8V. MAF 3.4 g/s idle, 10.2 g/s at 2500 RPM (2.0L engine)
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 20.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 1.0%, ECU λ: 1.0, MAF: 3.4 g/s
- **DTCs**: No DTCs stored
- **Expected Fault**: Healthy_O2_Fast_Switching_Benchmark
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: PDF-HI-005
- **Description**: High idle baseline; excellent combustion
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.3%, NOx: 30.0 ppm, λ Analyser: 1.001
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 30 ppm: low — rich quench or idle without thermal load. λ 1.001: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.00) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: PDF-HI-010
- **Description**: Reference baseline at high idle
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.08%, CO₂: 15.3%, O₂: 0.25%, NOx: 20.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 0.0
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.08%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.3%: at or near the efficient ceiling (≥14.5% with cat). O2 0.25%: low — rich consumed the oxygen, or perfect stoich. NOx 20 ppm: low — rich quench or idle without thermal load. λ 1.01: in the catalyst window (0.97–1.03); OBD λ=0 (Δ=+1.01) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7).

### Case: YAML-CSV5
- **Description**: insufficient_evidence
- **Gas Chemistry**: HC: 5.0 ppm, CO: 0.05%, CO₂: 15.5%, O₂: 0.1%, NOx: 15.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 5 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.05%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.5%: at or near the efficient ceiling (≥14.5% with cat). O2 0.1%: low — rich consumed the oxygen, or perfect stoich. NOx 15 ppm: low — rich quench or idle without thermal load. λ 1: in the catalyst window (0.97–1.03).

### Case: YAML-PDF_HI_005
- **Description**: The Perfect Modern Pass (High Idle)
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.01%, CO₂: 14.8%, O₂: 0.3%, NOx: 0.0 ppm, λ Analyser: 1.001
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 15 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.01%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14.8%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.001: in the catalyst window (0.97–1.03).

### Case: YAML-PDF_HI_010
- **Description**: Good Baseline Reference
- **Gas Chemistry**: HC: 30.0 ppm, CO: 0.12%, CO₂: 14.0%, O₂: 0.5%, NOx: 300.0 ppm, λ Analyser: 1.01
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 30 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.12%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 14%: healthy without-cat reference (13–14.5%). O2 0.5%: typical pre-cat residual (0.5–1.5%). NOx 300 ppm: moderate idle/light-load combustion temperature. λ 1.01: in the catalyst window (0.97–1.03).

### Case: YAML-TC1
- **Description**: 100% Health
- **Gas Chemistry**: HC: 12.0 ppm, CO: 0.1%, CO₂: 15.2%, O₂: 0.3%, NOx: 0.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: 
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 12 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15.2%: at or near the efficient ceiling (≥14.5% with cat). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1: in the catalyst window (0.97–1.03).

### Case: case_012
- **Description**: Freeze-frame from past P0303 misfire, current idle clean
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.05%, CO₂: 14.6%, O₂: 0.5%, NOx: ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.1 – 0.45
- **Reasoning**: HC 20 ppm: clean idle, current combustion is healthy. CO 0.05%: near zero. CO2 14.6%: at the efficient ceiling. O2 0.5%: minimal residual, perfect stoich. NOx unmeasured at idle (cold-channel reading is non-diagnostic). λ 1.00: chemistry confirms a clean current burn; the historical freeze-frame P0303 from highway load should raise the ignition prior, not override the clean L1 result.

### Case: case_028
- **Description**: P0606 absent, normal gases (anti-magnet test)
- **Gas Chemistry**: HC: 15.0 ppm, CO: 0.01%, CO₂: 14.7%, O₂: 0.4%, NOx: 30.0 ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.3
- **Reasoning**: HC 15 ppm: clean. CO 0.01%: clean. CO2 14.7%: ideal. O2 0.4%: minimal residual. NOx 30 ppm: low idle. λ 1.00: perfect stoich. With no DTC, the magnet to ECU_Internal must NOT pull it into the top three; the ranker should report no_fault or insufficient_evidence.

### Case: case_049
- **Description**: Pending P0171, idle gases pristine (false-lean DTC, no consequence)
- **Gas Chemistry**: HC: 10.0 ppm, CO: 0.01%, CO₂: 14.8%, O₂: 0.3%, NOx: ppm, λ Analyser: 1.0
- **OBD / Air / Engine**: Trims B1 (ST/LT): 2.0% / 1.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P0171
- **Expected Fault**: no_fault
- **Expected State**: insufficient_evidence
- **Confidence Range**: 0.0 – 0.35
- **Reasoning**: HC 10 ppm: pristine. CO 0.01%: pristine. CO2 14.8%: at ceiling. O2 0.3%: minimal. NOx unmeasured. λ 1.00: perfect stoich. A pending P0171 with normal trims and no λ/chemistry contradiction is not enough evidence to assert any fault — perception detector must not over-fire.


## Graph relations (explicit)

**labs/comlab/registry/rules/no_fault.json** VERIFIES **CASE-009**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **CSV-001**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **CSV-005**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **CSV-127**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **CSV-128**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **EXT-216**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **EXT-220**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **EXT-231**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **PDF-HI-005**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **PDF-HI-010**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **YAML-CSV5**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **YAML-PDF_HI_005**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **YAML-PDF_HI_010**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **YAML-TC1**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **case_012**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **case_028**
**labs/comlab/registry/rules/no_fault.json** VERIFIES **case_049**
