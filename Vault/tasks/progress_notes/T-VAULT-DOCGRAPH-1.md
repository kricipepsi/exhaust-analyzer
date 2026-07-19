# T-VAULT-DOCGRAPH-1 â€” progress note

## Plan

Run `4dlab-graphify-run` (resolve â†’ run â†’ relocate â†’ verify) on the prepared `graph/v2_docs/ingest_ready/` chunk
tree (Pass-3 LLM, prose, `--directed`), scoped to that dir only (never repo root â€” the 81.9k-node guard), and
relocate the result to the canonical docs-tier graph `graph/v2_docs/`. Verify health (nodes/links > 0, relation
split, EXTRACTED dominant), spot-check the architectural-predicate proof-set (SUPERSEDES / MIRRORS_CONTRACT_IN /
CONSUMES / VERIFIES present), and confirm no collateral on `v2_code` / `v2_tests` / `v2_wiki` and no change to
`research/chunks` or `graphify-out/manifest.json`. Any missing edge routes back to `4dlab-doc-prep` â€” never patched
into `graph.json`. Separately, **fix the owner-flagged skill gap**: add a **docs branch** to
`4dlab-graphify-run/SKILL.md` (currently code+wiki only) â€” corpus-table row, `description`, resolve/run/relocate/
verify steps, and prep-skill reference â€” destination `graph/v2_docs/`, prep skill `4dlab-doc-prep`, verify focus =
architectural-predicate proof-set. Graph-tooling lane â€” no lab inner-loop/gate. Blocked by T-VAULT-DOCPREP-1.


## VERIFICATION GATE

Completed 2026-06-10.

- Input corpus: `labs/obdlab/graph/v2_docs/ingest_ready/` with 68 prepared Markdown chunks.
- Runner preflight: upgraded `graphifyy` from `0.6.0` to `0.8.36`. `graphify extract graph/v2_docs/ingest_ready --out . --backend claude-cli --max-concurrency 2 --api-timeout 900` was attempted after upgrade, but semantic extraction failed because local Claude CLI is not authenticated (`claude auth status` => `loggedIn: false`, `authMethod: none`) and no API-key backend env vars/custom provider were present.
- Build path used: deterministic extraction from prepared `## Graph relations (explicit)` sections, then graphify `build_from_json(..., directed=True)`, clustering, report, JSON, and HTML export. No source docs or prepared chunks were edited; missing-edge policy remains routed to `4dlab-doc-prep`.
- Outputs present:
  - `labs/obdlab/graph/v2_docs/graph.json`
  - `labs/obdlab/graph/v2_docs/GRAPH_REPORT.md`
  - `labs/obdlab/graph/v2_docs/graph.html`
- Root artifact status: stale `labs/obdlab/graphify-out/` was moved before running to `%TEMP%/obdlab-root-graphify-out-backup-20260610-162731`; final `labs/obdlab/graphify-out/` is absent.
- Health: 480 nodes, 1,045 directed links, 19 communities, 0 isolated nodes.
- Node split: 68 `document`, 412 `concept`.
- Confidence split: 1,045 `EXTRACTED`; 0 `INFERRED`; 0 `AMBIGUOUS`. EXTRACTED dominates.
- Relation split: `MENTIONS` 696, `VERIFIES` 93, `CONSUMES` 76, `ENUMERATES` 52, `DESCRIBES` 51, `GATED_BY` 24, `SUPERSEDES` 16, `DERIVED_FROM` 15, `ROUTES_TO` 10, `MIRRORS_CONTRACT_IN` 9, `OWNED_BY` 3.
- Top high-degree nodes: `15. Test Coverage (current)` 34, `7. COMLab Integration Points` 23, `OBDLivePayload` 22, `BDD_OBDLab v2.0` 20, `3. schemas/dna_view.py` 20, `OBDLab` 18, `core/pid_ingestion_validator.py` 18, `3. Internal Pipeline` 18, `COMLab` 17, `O2Normalizer.normalize` 17.
- Proof-set:
  - `SUPERSEDES`: FOUND 16. Examples: `Physics_Gate_3 -> FAULT_VE_SENSOR_SKEW @ HLD_OBDLab/3_Internal_Pipeline.md:L56`; `ObdLabError -> ValueError / AssertionError @ ADR_OBDLab/ADR-0005_Unify_Exception_Hierarchy.md:L40`.
  - `MIRRORS_CONTRACT_IN`: FOUND 9. Examples: `OBDLivePayload -> COMLab frozen contract surface @ HLD_OBDLab/7_COMLab_Integration_Points.md:L48`; `OBDLivePayload -> SEMANTIC_CONTRACT section 4.4 @ DLD_OBDLab/4_schemas_payload_py.md:L52`.
  - `CONSUMES`: FOUND 76. Examples: `COMLab -> normalized_obd_lambda @ HLD_OBDLab/7_COMLab_Integration_Points.md:L37`; `COMLab -> OBDLivePayload @ PRD_OBDLab/Section_1_Summary.md:L15`.
  - `VERIFIES`: FOUND 93. Examples: `Anti-orphan grep (Stage 4) -> forward-registered fields have live reader @ ADR_OBDLab/ADR-0002_Emit_S2_Consume_S4.md:L48`; `DUAL_MAF_MAP_CROSSCHECK -> VEValidity classified @ BDD_OBDLab/Feature_VE_Routing_and_Validity.md:L37`.
- No-collateral checks:
  - `git status --porcelain -- graph/v1_baseline graph/v2_code graph/v2_tests graph/v2_wiki`: clean.
  - `git status --porcelain -- research/chunks graphify-out/manifest.json`: clean.
  - Other graph-tier mtimes remained at their pre-run values: `v1_baseline` 2026-06-06 18:38:33, `v2_code` 2026-06-09 18:55:16, `v2_tests` 2026-06-09 21:53:10, `v2_wiki` 2026-06-09 00:07:33; `research/chunks` remained 2026-06-07 23:36:44.

## CODE REVIEW

- `_skills/graph/4dlab-graphify-run/SKILL.md` now treats docs/design-doc corpora as a first-class branch:
  - frontmatter description/prep sentence include `4dlab-doc-prep` and docs/design-doc chunks;
  - corpus table includes `graph/v2_docs/ingest_ready/`, Pass 3 LLM, destination `graph/v2_docs/`, and architectural predicate verification;
  - resolve/run/relocate/verify sections include the docs path, `--directed`, docs destination, and missing proof-edge routing to `4dlab-doc-prep`;
  - prep-skill references include `4dlab-doc-prep`.
- Built docs-tier graph counts: 480 nodes, 1,045 directed links, 19 communities, 0 isolated nodes.
- Review caveat: the desired Pass 3 LLM backend was unavailable in this shell, so the graph was produced from explicit prepared relation blocks rather than a live semantic LLM extraction. The graph is auditable and source-anchored, but a future authenticated `graphify extract --backend claude-cli` or API-key backend run can enrich it with broader semantic edges.
