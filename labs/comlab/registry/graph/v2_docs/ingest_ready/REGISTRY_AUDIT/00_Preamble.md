---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "rule-inventory-and-rebuild"
implements:
  - "labs/comlab/registry/rules/lean_condition.json"
  - "labs/comlab/registry/rules/rich_mixture.json"
  - "labs/comlab/registry/rules/misfire.json"
  - "labs/comlab/registry/integration_shim.py"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py loads rebuilt v2 rule data instead of v1 inventory"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py delegates v2 routing to registry.integration_shim"
drift_guards:
  - "labs/comlab/registry/tests/test_integration_shim.py"
  - "labs/comlab/registry/tests/test_lean_condition_rules.py"
  - "labs/comlab/registry/tests/test_rich_mixture_rules.py"
  - "labs/comlab/registry/tests/test_misfire_rules.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/REGISTRY_AUDIT/00_Preamble.md"
---
> **Context:** REGISTRY_AUDIT v2.0 · Module: Registry · Section: Preamble · Parent document: labs/comlab/registry/corpus_curated.csv
# REGISTRY AUDIT — v1 Rule Inventory and Patch-vs-Rebuild Decision

**Generated:** 2026-05-27
**Inputs:**
- `COMLab/comlab/config/global_fault_registry.json` (53 executable rule registrations)
- `COMLab/comlab/config/kg/*.json` (58 knowledge graph nodes across 12 families)
- `registry/corpus_curated.csv` (252 curated cases)
- `registry/CORPUS_AUDIT.md` (AUDIT-CORPUS deliverable)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md`
- `COMLab/comlab/core/fault_atlas_router.py` (routing/pruning/scoring logic)

---


## Graph relations (explicit)

**labs/comlab/registry/docs/REGISTRY_AUDIT.md** DESCRIBES **REGISTRY_AUDIT v2.0**
