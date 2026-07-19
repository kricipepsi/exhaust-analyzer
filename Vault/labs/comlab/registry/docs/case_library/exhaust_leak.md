---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-exhaust_leak"
implements:
  - "labs/comlab/registry/code/rules/exhaust_leak.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_exhaust_leak_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/exhaust_leak.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: exhaust_leak · Parent document: labs/comlab/registry/corpus_curated.csv
# exhaust_leak
5 cases

### Case: CSV-095
- **Description**: High O2 + lean = air ingress
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 6.0%, NOx: 20.0 ppm, λ Analyser: 1.3
- **OBD / Air / Engine**: Trims B1 (ST/LT): 20.0% / 10.0%, ECU λ: 1.0
- **DTCs**: P0171
- **Expected Fault**: Exhaust_Air_Leak_Pre_Cat
- **Expected State**: warning
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 6%: severe lean / large misfire / air leak (>4%). NOx 20 ppm: low — rich quench or idle without thermal load. λ 1.3: cranking / no-combustion shape (master_gas_guide §3 rule 8 — route to non-starter pipeline); OBD λ=1 (Δ=+0.30) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: PDF-HI-007
- **Description**: λ corrected 1.052→1.221; O2 high from exhaust leak
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.02%, CO₂: 11.0%, O₂: 3.5%, NOx: 0.0 ppm, λ Analyser: 1.221
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.05
- **DTCs**: No DTCs stored
- **Expected Fault**: Exhaust_Leak_False_Air
- **Expected State**: named_fault
- **Confidence Range**: 0.65 – 0.85
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.02%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 11%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 3.5%: clearly elevated (1.5–4%) — lean tail or misfire. NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.221: lean (≥1.05) — Brettschneider chemistry; OBD λ=1.05 (Δ=+0.17) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: TC-048
- **Description**: TC48: λ_gas corrected to Brettschneider 1.344; OBD λ=1.0 in OBD_Lambda
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 12.0%, O₂: 6.0%, NOx: 0.0 ppm, λ Analyser: 1.344
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0
- **DTCs**: P0171
- **Expected Fault**: Air_Intrusion_Exhaust_Leak_TC
- **Expected State**: named_fault
- **Confidence Range**: 0.55 – 0.75
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 6%: severe lean / large misfire / air leak (>4%). NOx 0: 4-gas analyser unmeasured channel (master_gas_guide §8.5: not low-NOx evidence). λ 1.344: cranking / no-combustion shape (master_gas_guide §3 rule 8 — route to non-starter pipeline); OBD λ=1 (Δ=+0.34) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: YAML-CSV95
- **Description**: Exhaust_Air_Leak_Pre_Cat
- **Gas Chemistry**: HC: 20.0 ppm, CO: 0.1%, CO₂: 15.0%, O₂: 6.0%, NOx: 20.0 ppm, λ Analyser: 1.3
- **OBD / Air / Engine**: ECU λ: 1.0
- **DTCs**: P0171
- **Expected Fault**: Exhaust_Air_Leak_Pre_Cat
- **Expected State**: warning
- **Confidence Range**: 0.7 – 0.9
- **Reasoning**: HC 20 ppm: clean burn (≤50 ppm post-cat ceiling per master_gas_guide §2). CO 0.1%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 15%: at or near the efficient ceiling (≥14.5% with cat). O2 6%: severe lean / large misfire / air leak (>4%). NOx 20 ppm: low — rich quench or idle without thermal load. λ 1.3: cranking / no-combustion shape (master_gas_guide §3 rule 8 — route to non-starter pipeline); OBD λ=1 (Δ=+0.30) — ECU sees richer than chemistry, perception-contradiction symptom (rule 7). Pattern: CO≈0 + O2↑ + HC normal → exhaust/sample air leak (master_gas_guide §8.1 row 2), not true lean.

### Case: case_045
- **Description**: P2096 post-cat lean DTC with downstream exhaust leak
- **Gas Chemistry**: HC: 100.0 ppm, CO: 1.8%, CO₂: 12.8%, O₂: 0.8%, NOx: ppm, λ Analyser: 0.94
- **OBD / Air / Engine**: Trims B1 (ST/LT): 10.0% / 8.0%, ECU λ: 1.02, RPM: 850.0, ECT: 90.0°C
- **DTCs**: P2096
- **Expected Fault**: exhaust_leak_post_cat
- **Expected State**: named_fault
- **Confidence Range**: 0.35 – 0.65
- **Reasoning**: HC 100 ppm: slightly elevated. CO 1.8%: clearly rich. CO2 12.8%: depressed. O2 0.8%: low. NOx unmeasured. λ 0.94: chemistry says rich; ECU sees post-cat lean (P2096) and is adding fuel — the post-cat sensor is being fed false air from a downstream leak.


## Graph relations (explicit)

**labs/comlab/registry/rules/exhaust_leak.json** VERIFIES **CSV-095**
**labs/comlab/registry/rules/exhaust_leak.json** VERIFIES **PDF-HI-007**
**labs/comlab/registry/rules/exhaust_leak.json** VERIFIES **TC-048**
**labs/comlab/registry/rules/exhaust_leak.json** VERIFIES **YAML-CSV95**
**labs/comlab/registry/rules/exhaust_leak.json** VERIFIES **case_045**
