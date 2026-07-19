
> **Context:** COMLab LLD v2.0 · Module: COMLab · Section: Preamble · Parent document: COMLab DLD v2.0 / COMLab HLD v2.0
# COMLab Low-Level Design (LLD)

**Document type:** LLD — directory blueprint, per-module class/method
signatures, Pydantic schemas, JSON schemas for config artefacts, error-code
taxonomy, and test layout. Implementation-ready spec for the coder.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_LLD_v1.0_2026-05-21.md`.

> **Authority note (read first).** The shipped Python in `comlab/schemas/*.py`,
> `comlab/core/*.py`, and `comlab/analytics/*.py` is the **single source of
> truth** for exact field sets, types, and signatures. The snippets in this LLD
> are *representative* — they name the load-bearing types and contracts and call
> out where the code has grown past the v1.0 draft, but they do not re-list every
> field (that would re-introduce drift). Where this doc and the code disagree,
> the code wins; open an issue to correct the doc.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**. Post-2010 Euro 6+ technology — GPF/DPF inference, LSPI, secondary-air
injection — is out of scope and absent from every schema. The v1.0
`secondary_air_equipped` field has been **removed** from `EmissionsConfiguration`
accordingly.

**Companion to:** `COMLab_HLD.md` (architecture), `COMLab_PRD.md` (user-facing
behaviour), `COMLab_DLD.md` (resource/ops), `docs/adr/` (decisions),
`COMLab_BDD.md` (behaviour). This LLD inherits every decision from them.

**Out of scope:**

- Resource budgets, latency allocation, CI/build script — `COMLab_DLD.md`.
- Actual rule rows / KG node entries — config data, not code; this LLD specifies
  their *schema*, not their *content*.
- Method bodies. Method *signatures* and *contracts* are in scope.

**Authoritative inputs:**

- `COMLab_HLD.md` §3–§8 — module responsibilities and pipeline stages.
- `COMLab_PRD.md` §4–§6 — gates, error UX, what Screen 6 must consume.
- The six v1.0 rulings, now settled in code and recorded in `docs/adr/` and
  HLD §12: KG as a per-family **directory** (13 files), `user_input_echo_audit`
  COMLab-emitted, `lab_routing_directive` in `execution_meta`,
  `horizon_context_injector.py` filename kept, differential siblings capped at 5.
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` §4, §5, §8 — JSON shapes and enum
  vocabulary.
- `wiki/` — domain truth (esp. `04_horizon_eras`, `07_pipeline_stages`,
  `08_scoring_to_fusion_rework`, `11_two_point_delta`).
- The shipped `comlab/` package — this doc reconciles up to it.

---


## Graph relations (explicit)

**COMLab_LLD.md** DESCRIBES **COMLab LLD v2.0**
**COMLab LLD v2.0** MIRRORS_CONTRACT_IN **COMLab DLD v2.0**
