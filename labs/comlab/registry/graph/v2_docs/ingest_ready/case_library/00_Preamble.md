---
node_type: wiki
lab: registry
module: registry
subsystem: case-library-00_Preamble
implements:
- labs/comlab/registry/corpus_curated.csv
consumers:
- 'registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics
  loads and scores registry rules'
- 'comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim
  behind USE_V2_REGISTRY'
- 'registry: labs/comlab/registry/code/tools/render_case_library.py groups curated
  cases by fault family'
drift_guards:
- labs/comlab/registry/tests/test_render_case_library.py
tags:
- registry
- finished
- wiki
source: labs/comlab/registry/graph/v2_docs/ingest_ready/case_library/00_Preamble.md
---

> **Context:** case_library v2.0 · Module: Registry · Section: Preamble · Parent document: labs/comlab/registry/corpus_curated.csv
# 4DLab Curated Case Library

Static index of all reference cases used to validate the rule registry


## Graph relations (explicit)

**labs/comlab/registry/docs/case_library.html** DESCRIBES **case_library v2.0**
