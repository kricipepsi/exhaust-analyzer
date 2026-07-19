---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "schema-v2-contract"
implements:
  - "labs/comlab/registry/code/schema_v2.py"
  - "labs/comlab/registry/code/integration_shim.py"
consumers:
  - "registry: labs/comlab/registry/code/integration_shim.py validates rule JSON through schema_v2 models"
  - "registry: labs/comlab/registry/code/tools/build_corpus.py and render_case_library.py consume curated schema/corpus contracts"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py consumes rendered v2 registry output"
drift_guards:
  - "labs/comlab/registry/tests/test_schema_v2.py"
  - "labs/comlab/registry/tests/test_integration_shim.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/SCHEMA_V2_SPEC/00_Preamble.md"
---

> **Context:** SCHEMA_V2_SPEC v2.0 · Module: Registry · Section: Preamble · Parent document: labs/comlab/registry/schema_v2.py
# SCHEMA V2 SPEC — 4DLab Registry Rule Schema

**Generated:** 2026-05-27
**Source task:** REG-V2-SCHEMA
**Authoritative model:** `registry/schema_v2.py`
**Audience:** Rule authors (REG-V2-AUTHOR-{family}) and integration engineer (REG-V2-INTEGRATE)

---


## Graph relations (explicit)

**labs/comlab/registry/docs/SCHEMA_V2_SPEC.md** DESCRIBES **SCHEMA_V2_SPEC v2.0**
**labs/comlab/registry/schema_v2.py** IMPLEMENTS **SCHEMA_V2_SPEC v2.0**
