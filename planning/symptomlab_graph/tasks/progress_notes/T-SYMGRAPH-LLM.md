# T-SYMGRAPH-LLM — progress note

## Plan

**Task picked:** `T-SYMGRAPH-LLM` (build Pass-3 LLM tiers `v2_wiki/` + `v2_docs/`) — first
unblocked pending row; both blockers (WIKIPREP, DOCPREP) `done`. **Files to touch (CREATE):**
`labs/symptomlab/graph/v2_wiki/` (graph.json + GRAPH_REPORT.md + graph.html),
`labs/symptomlab/graph/v2_docs/` (same three), this progress note, and the PROGRESS ledger row.
**Two scoped Pass-3 runs** (`resolve→run→relocate→verify`, `--directed`) via
`_skills/graph/4dlab-graphify-run`: run 1 scope `labs/symptomlab/wiki/` → relocate to
`graph/v2_wiki/`; run 2 scope `labs/symptomlab/graph/v2_docs/ingest_ready/` → relocate to
`graph/v2_docs/`. **Backend (owner-confirmed):** host model **Opus 4.8** via Claude Code
subagent dispatch (global graphify skill path when GEMINI_API_KEY unset) — no external API
backend, no model-config change. **Verification commands:**
`eval_wiki_graph.py v2_wiki/graph.json`, `eval_doc_graph.py v2_docs/graph.json`,
`git status --porcelain labs/symptomlab/graph` (only the two new tiers may show),
`Test-Path graphify-out\graph.json` must be False. **Guards at risk:** never `/graphify .`
from a repo root (81.9k-node rule); never touch `graphify-out/`, `v2_current/`, `v1_baseline/`,
`v2_code/`, `v2_tests/`; a missing edge is a prep gap routed back, never hand-patched into
`graph.json`. **Both verdicts must read GOOD or hand back blocked.**

---

## Execution & verification (LITE)

**Backend:** host model **Opus 4.8** via Claude Code general-purpose subagent dispatch — the
global `graphify` skill's prescribed Pass-3 path when `GEMINI_API_KEY` is unset ("the host
session itself is the LLM"; graphify does not read `ANTHROPIC_API_KEY`/`DEEPSEEK_API_KEY` on
this path). No external API backend named, no model-config change. Owner-authorised the spend.

**Run mechanics:** each run executed from `cwd=labs/symptomlab` so graphify output landed at
`labs/symptomlab/graphify-out/` — the FROZEN root `graphify-out/` (58 MB, 4DLabV2 root) was
never the working dir and is byte-unchanged. graphify binary: `.venv-wired\Scripts\graphify.exe`.
Build = doc-only corpus → semantic subagent extraction → `build_from_json(directed=True)` →
cluster → `to_json` → `graphify export html` → relocate → remove spent local `graphify-out/`.

### Run 1 — wiki  (`labs/symptomlab/wiki/` → `graph/v2_wiki/`)
- Detect: 5 docs, ~4.8k words. 1 chunk (1 subagent): **96 nodes, 105 edges, 102 EXTRACTED /
  3 INFERRED / 0 AMBIGUOUS**, 3 hyperedges.
- Built graph (directed): **109 nodes, 123 links, 11 communities**.
- **eval-wiki-graph health verdict: GOOD** — nodes 109, links 123, density 0.0104,
  **dangling 0, isolated 0**, confidence split **{EXTRACTED 120, INFERRED 3}** (EXTRACTED
  dominant). Top hub: `wiki_01_symptom_catalog_symptomvalidator_validate` (deg 15).
  *(isolated is informational for wiki; here it landed at 0.)*

### Run 2 — docs  (`labs/symptomlab/graph/v2_docs/ingest_ready/` → `graph/v2_docs/`)
- Detect: 47 docs, ~7.9k words. 3 chunks by doc family (ADR+BDD / DLD+LLD / HLD+PRD), 3
  subagents in parallel:
  - C1 ADR+BDD: 33 nodes, 50 edges (48 EXTRACTED / 2 INFERRED), predicates supersedes 1,
    mirrors_contract_in 1, consumes 2, verifies 11.
  - C2 DLD+LLD: 30 nodes, 64 edges (57 EXTRACTED / 7 INFERRED), predicates mirrors_contract_in
    16, consumes 3, verifies 9, supersedes 0.
  - C3 HLD+PRD: 33 nodes, 53 edges (49 EXTRACTED / 4 INFERRED), predicates consumes 8,
    mirrors_contract_in 4, verifies 5, supersedes 1.
- Built graph (directed): **78 nodes, 169 links, 7 communities**.
- **eval-doc-graph health verdict: GOOD** — nodes 78, links 169, density 0.0281,
  **dangling 0, isolated 0** (docs fully wired, as required), confidence split
  **{EXTRACTED 157, INFERRED 12}** (EXTRACTED dominant). Top hubs: `concept_symptomlab` (43),
  `concept_symptomdna` (18), `concept_allowed_combinations_yaml` (18).
- **All four architectural predicates present** across the merged graph: `SUPERSEDES`,
  `MIRRORS_CONTRACT_IN`, `CONSUMES`, `VERIFIES` (the docs-prep proof-set).

### Collateral proof — `git status --porcelain 4DLab/4DLabV2/labs/symptomlab/graph`
```
?? 4DLab/4DLabV2/labs/symptomlab/graph/v2_docs/GRAPH_REPORT.md
?? 4DLab/4DLabV2/labs/symptomlab/graph/v2_docs/graph.html
?? 4DLab/4DLabV2/labs/symptomlab/graph/v2_docs/graph.json
?? 4DLab/4DLabV2/labs/symptomlab/graph/v2_wiki/
```
Only the two new tiers changed. Explicit re-check of `v2_code`, `v2_tests`, `v2_current`,
`v1_baseline`, `DIFF_REPORT.md` → **empty** (byte-unchanged). `ingest_ready/` survived the
relocate (already tracked from DOCPREP, so it does not appear as changed).

### No-surviving-root-output check
`Test-Path labs\symptomlab\graphify-out` → **False** (spent local output removed).
`Test-Path graphify-out\graph.json` (frozen root) → **True** (present & untouched, not staged).

**Result: both tiers built, both health verdicts GOOD, EXTRACTED-dominant, 0 collateral.**
Status → done.
