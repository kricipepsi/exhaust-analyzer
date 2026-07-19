
> **Context:** ADR-0006 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0006: Separate the rule registry from the Fault-Atlas KG

**Status:** Accepted

**Context.** Two distinct kinds of knowledge meet at the verdict: *evaluation
rules* (which operators/thresholds/horizons make a fault fire) and *enrichment*
(what the fault means physically, what to repair). Conflating them in one file
makes both hard to edit and audit, and forces a code change to add a fault's
human-facing copy.

**Decision.** Keep two artefacts with a strict split. `global_fault_registry.json`
owns the **evaluation rules** consumed by `fault_atlas_router`. The **Fault-Atlas
Knowledge Graph** owns the **enrichment** and ships as a **directory of 13
per-family JSON files** under `comlab/config/kg/` (`lean_condition.json`,
`misfire.json`, …, `invalid_input.json`) plus `_kg_schema.json`, loaded once at
boot by `fault_atlas_kg.FaultAtlasKG` into one flat `dict[fault_id, KGNode]` for
O(1) lookup. The KG is **passive** — no graph database, no traversal at runtime;
the only edge type is `differential_siblings`, carried inside each node. A
**build-break consistency test** (`tests/e2e/test_kg_registry_consistency.py`,
mirrored in the build-validation script) enforces that every registry `fault_id`
has a KG node and vice versa.

**Consequences.**
- Positive: domain editors change enrichment as config-only PRs, per family,
  without touching Python or the rule rows.
- Positive: "rule fired" and "what it means" never silently diverge — a missing
  pair is a build failure, not a runtime "fault fires but cannot be enriched" gap.
- Negative: two files to keep in lockstep; the consistency gate is mandatory in CI.
- Neutral: per-family split (resolves the v1.0 "one file vs directory" question)
  keeps each family independently editable and diffable.

**Alternatives considered.**
1. *One combined registry+enrichment file.* Rejected — couples rule logic to UI
   copy and bloats every rule row.
2. *A single monolithic `fault_atlas_kg.json`.* Rejected — poor editor ergonomics
   and noisy diffs versus the per-family directory.
3. *A real graph database.* Rejected — the dataset is small, static, and
   version-controlled; a dict lookup beats infra.

**References.** `COMLab_HLD.md` §5; `COMLab_LLD.md` §3.4, §6.5, §8.2;
`comlab/core/fault_atlas_kg.py`; `comlab/schemas/kg.py`; `comlab/config/kg/`.


## Graph relations (explicit)

**ADR-0006** DESCRIBES **Separation of registry and KG**
**comlab/core/fault_atlas_router.py** IMPLEMENTS **ADR-0006**
