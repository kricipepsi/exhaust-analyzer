---
node_type: "wiki"
lab: "registry"
module: "registry"
subsystem: "curated-corpus"
implements:
  - "labs/comlab/registry/code/corpus_curated.csv"
  - "labs/comlab/registry/code/corpus_meta.json"
  - "labs/comlab/registry/code/tools/build_corpus.py"
consumers:
  - "registry: labs/comlab/registry/code/tools/build_corpus.py produces corpus_curated.csv and corpus_meta.json"
  - "registry: labs/comlab/registry/code/tools/render_case_library.py reads corpus_curated.csv for case-library docs"
  - "registry: labs/comlab/registry/code/integration_shim.py route_case_with_diagnostics loads and scores registry rules"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py v2 path imports registry.integration_shim behind USE_V2_REGISTRY"
drift_guards:
  - "labs/comlab/registry/tests/test_build_corpus.py"
  - "labs/comlab/registry/tests/test_render_case_library.py"
tags: [registry, finished, wiki]
source: "labs/comlab/registry/graph/v2_docs/ingest_ready/CORPUS_AUDIT/00_Preamble.md"
---

> **Context:** CORPUS_AUDIT v2.0 · Module: Registry · Section: Preamble · Parent document: labs/comlab/registry/corpus_curated.csv
# CORPUS AUDIT — v2 Ground-Truth Corpus Curation

**Generated:** 2026-05-27
**Input:** `TestSuite/cases_petrol_master_v6.csv` (281 cases)
**Proposal source:** `registry/cvsgaps.md` (46 proposed dispositions)
**Jaeger evidence:** `4DLabWired/_jaeger/runs/20260527-044325/FAILURE_BLUEPRINT.md` (239 unique failing case IDs)
**Tooling:** `registry/tools/build_corpus.py` (idempotent; re-run produces identical output)

---


## Graph relations (explicit)

**labs/comlab/registry/docs/CORPUS_AUDIT.md** DESCRIBES **CORPUS_AUDIT v2.0**
**labs/comlab/registry/tools/build_corpus.py** IMPLEMENTS **CORPUS_AUDIT v2.0**
