---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "chemistry-coverage-matrix"
implements:
  - "labs/comlab/registry/code/schema_v2.py"
  - "labs/comlab/registry/code/rules/lean_condition.json"
  - "labs/comlab/registry/code/rules/rich_mixture.json"
  - "labs/comlab/registry/code/rules/misfire.json"
  - "labs/comlab/registry/code/rules/catalyst_failure.json"
  - "labs/comlab/registry/code/rules/sensor_fault.json"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
drift_guards:
  - "labs/comlab/registry/tests/test_schema_v2.py"
  - "labs/comlab/registry/tests/test_lean_condition_rules.py"
  - "labs/comlab/registry/tests/test_rich_mixture_rules.py"
  - "labs/comlab/registry/tests/test_misfire_rules.py"
  - "labs/comlab/registry/tests/test_catalyst_failure_rules.py"
  - "labs/comlab/registry/tests/test_sensor_fault_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/CHEMISTRY_COVERAGE/00_Preamble.md"
---

> **Context:** CHEMISTRY_COVERAGE v2.0 · Module: Registry · Section: Preamble · Parent document: labs/comlab/registry/corpus_curated.csv
# CHEMISTRY COVERAGE — GASLab State × Fault Family Matrix

**Generated:** 2026-05-27
**Inputs:**
- `registry/corpus_curated.csv` (252 cases, 16 fault families)
- `registry/CORPUS_AUDIT.md` (AUDIT-CORPUS deliverable — per-family case counts)
- `registry/REGISTRY_AUDIT.md` (AUDIT-REG deliverable — v1 rule inventory, chemistry states)
- `GASLab/gaslab/contracts.py` (34-value `ChemicalSignature` enum)
- `COMLab/comlab/config/global_fault_registry.json` (53 v1 rules, chemistry-gated)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md` (per-phase chemistry distribution in 239 failing traces)

**Methodology note:** The curated corpus (`corpus_meta.json`) stores per-case fault-family labels but not per-case GASLab chemistry states — those are emitted at runtime. Cell counts in this matrix are **inferred** from three sources: (a) Jaeger trace data for the 239 failing cases (aggregate chemistry distributions from the capability analysis), (b) v1 rule `gas_lab_state` gating — each rule's chemistry→family intent, and (c) domain knowledge of which chemistry signatures correspond to which fault families per GAS_VOCABULARY.md. Cells marked **[J]** are trace-confirmed from Jaeger representative cases; cells marked **[R]** are mapped from v1 rule registrations; cells marked **[D]** are domain-inferred from the GASLab vocabulary. Exact per-case chemistry-state data requires running GASLab against all 252 curated cases (out of scope for this read-only audit).

---


## Graph relations (explicit)

**labs/comlab/registry/docs/CHEMISTRY_COVERAGE.md** DESCRIBES **CHEMISTRY_COVERAGE v2.0**
