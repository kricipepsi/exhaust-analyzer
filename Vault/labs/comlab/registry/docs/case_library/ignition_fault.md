---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "case-library-ignition_fault"
implements:
  - "labs/comlab/registry/code/rules/ignition_fault.json"
  - "labs/comlab/registry/code/corpus_curated.csv"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py groups curated cases by fault family"
drift_guards:
  - "labs/comlab/registry/tests/test_ignition_fault_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/ignition_fault.md"
---

> **Context:** case_library v2.0 · Module: Registry · Section: ignition_fault · Parent document: labs/comlab/registry/corpus_curated.csv
# ignition_fault
3 cases

### Case: CASE-035
- **Description**: Low-speed pre-ignition (LSPI) at high load low RPM; timing retarded to -12° to prevent engine damage; brief HC spike; warm engine required
- **Gas Chemistry**: HC: 600.0 ppm, CO: 0.5%, CO₂: 13.0%, O₂: 0.3%, NOx: 55.0 ppm, λ Analyser: 0.95
- **OBD / Air / Engine**: Trims B1 (ST/LT): -5.0% / -3.0%, ECU λ: 0.97, MAF: 3.5 g/s
- **DTCs**: P0324
- **Expected Fault**: GDI_LSPI_PreIgnition_Knock_Retard
- **Expected State**: named_fault
- **Confidence Range**: 0.67 – 0.87
- **Reasoning**: HC 600 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 13%: healthy without-cat reference (13–14.5%). O2 0.3%: low — rich consumed the oxygen, or perfect stoich. NOx 55 ppm: low — rich quench or idle without thermal load. λ 0.95: rich (≤0.95) — chemistry says excess fuel.

### Case: EXP-N026
- **Description**: Turbo-GDI low-speed pre-ignition event; HC spike; knock-retard
- **Gas Chemistry**: HC: 600.0 ppm, CO: 0.5%, CO₂: 12.8%, O₂: 0.8%, NOx: 45.0 ppm, λ Analyser: 0.93
- **OBD / Air / Engine**: Trims B1 (ST/LT): -3.0% / 0.0%, ECU λ: 0.97
- **DTCs**: P0324
- **Expected Fault**: GDI_LSPI_PreIgnition
- **Expected State**: named_fault
- **Confidence Range**: 0.57 – 0.77
- **Reasoning**: HC 600 ppm: real combustion problem (250–800 ppm = lean misfire, vacuum leak, or ignition fault). CO 0.5%: consistent with stoich or post-cat clean-up (≤0.5%). CO2 12.8%: depressed — real combustion deficit (rich, lean-misfire, or dilution). O2 0.8%: typical pre-cat residual (0.5–1.5%). NOx 45 ppm: low — rich quench or idle without thermal load. λ 0.93: rich (≤0.95) — chemistry says excess fuel.

### Case: case_036
- **Description**: Late ignition timing (knock-sensor fault) — moderate HC and CO
- **Gas Chemistry**: HC: 2200.0 ppm, CO: 1.2%, CO₂: 13.0%, O₂: 1.2%, NOx: ppm, λ Analyser: 0.97
- **OBD / Air / Engine**: Trims B1 (ST/LT): 0.0% / 0.0%, ECU λ: 1.0, RPM: 850.0, ECT: 90.0°C
- **DTCs**: No DTCs stored
- **Expected Fault**: late_ignition_timing
- **Expected State**: named_fault
- **Confidence Range**: 0.35 – 0.65
- **Reasoning**: HC 2200 ppm: very high — combustion runs into the exhaust stroke before the flame front completes. CO 1.2%: modestly elevated, partial combustion. CO2 13.0%: depressed by truncated burn. O2 1.2%: slightly elevated but below the >5% wrong-valve-timing threshold (richmixture.pdf), so this is timing-retard, not a mechanical valve problem. NOx unmeasured. λ 0.97: mildly rich because each pulse delivers fuel that does not fully burn; HC magnitude with mild CO and only slightly elevated O2 is the late-timing signature, not the wrong-valve-timing pattern (which would need O2 > 5%).


## Graph relations (explicit)

**labs/comlab/registry/rules/ignition_fault.json** VERIFIES **CASE-035**
**labs/comlab/registry/rules/ignition_fault.json** VERIFIES **EXP-N026**
**labs/comlab/registry/rules/ignition_fault.json** VERIFIES **case_036**
