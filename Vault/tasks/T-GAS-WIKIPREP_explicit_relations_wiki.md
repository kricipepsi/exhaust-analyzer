---
node_type: task
task_id: T-GAS-WIKIPREP
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling / author lane
blocked_by: []
consumers:
- graph/v2_wiki — wiki graph
tags:
- task
- vault
- gaslab
---


# T-GAS-WIKIPREP — Make wiki relations explicit (`4dlab-wiki-prep` on `labs/gaslab/wiki/`)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING / author lane (prep skill — no lab inner-loop/gate)
**Origin:** pipeline guide §4 (wiki prep) · **Blocked by:** — (precondition: wiki prose current — see below)
**Consumer (signal/noise):** **Adds no schema field.** Appends explicit relation trailer blocks so
graphify's Pass-3 LLM (T-GAS-GRAPH-LLM) tags edges `EXTRACTED` (full confidence) instead of guessing
`INFERRED`/`AMBIGUOUS`. The resulting `graph/v2_wiki/` graph informs the vault build's `consumers` /
`implements` frontmatter (plan §4). **Every appended `CONSUMES` / `VERIFIES` line must name a real,
existing code path or test** (grep-checked) — orphans are flagged, proposals stay labelled as
proposals (never promoted to live). That is signal/noise enforced at the edge.

### ⚠ GASLab path — NOT `research/chunks/` ###

The pipeline guide says wiki = `research/chunks/`; **that is OBDLab's layout.** GASLab's wiki is the
already-chunked corpus at **`labs/gaslab/wiki/`**:
`00_index.md`, `01_role_boundaries_dna_ingestion.md` … `11_sources_appendices.md`, plus
`CHANGE_v2.1_timing_taxonomy.md`. Run the skill against `labs/gaslab/wiki/`. **Do not** move or rename
it — it is graph-canonical at that source, and `PROGRESS.md` names it the v2 canonical wiki.

### Precondition — wiki currency ###

Phase-1C is "prose current + citation-backed." GASLab has open wiki-enhancement tasks in
`labs/gaslab/tasks/wiki_enhancements/` (`GW-ENH-1/2/3`). If any materially change the chunk prose the
relations depend on, let them land first (they are the gaslab wiki pack, not this pack). If they are
cosmetic/citation-only, proceed and note it. **Confirm currency in the Plan before appending relations.**

### Skill operations (guide §4) ###

`relations → labels → roster → verify` — append-only trailer blocks making implied links explicit
(`**SUBJECT** PREDICATE **OBJECT**`) + canonical entity labels. The skill never edits sourced prose
beyond appending its blocks, never writes `graph.json`, never runs graphify.

### Success criteria ###

1. Every chunk under `labs/gaslab/wiki/` carries exactly one explicit relations trailer; zero empty
   blocks.
2. Every `CONSUMES` / `VERIFIES` object resolves to a real GASLab field/enum/code path or test
   (grep-checked against `labs/gaslab/gaslab/` and `labs/gaslab/tests/`); orphans flagged, proposals
   labelled as proposals (route to `comlab/config/proposals/` if a consumer can be named).
3. Canonical entity labels match the code's names (e.g. `ChemicalSignature` values, `CAM_TIMING_*`,
   `target_lambda_v112`) so wiki nodes merge cleanly with code nodes at graph time.
4. `verify` op reports: relation-line counts by predicate, zero orphan edges, labels consistent,
   citations intact. **No prose rewrite; no graphify; no move of `wiki/`.**

### Out of scope ###

- Graphifying the wiki (→ T-GAS-GRAPH-LLM) · editing diagnostic prose content (→ GW-ENH-* pack).
- The docs corpus (→ T-GAS-DOCPREP) — **do not cross the streams** (wiki ≠ docs).

### Files to touch ###

- `labs/gaslab/wiki/*.md` — append-only relation/label trailer blocks.

### Verification ###

```bash
cd <repo>/labs/gaslab
# one relations block per chunk, none empty
grep -rL 'Graph relations' wiki/*.md ; echo "^ chunks missing a relations block (expect none)"
# spot every CONSUMES/VERIFIES object back to live code/test:
grep -rhoE 'CONSUMES \*\*[^*]+\*\*|VERIFIES \*\*[^*]+\*\*' wiki/ | sort -u | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-WIKIPREP.md` opens with the confirmed `## Plan` (currency confirmation
+ which chunks); the run session fills `VERIFICATION GATE` (one block/chunk, zero orphan edges, labels
consistent) + `CODE REVIEW` (relation counts, orphans flagged). Ledger row flips to `done` only when clean.
