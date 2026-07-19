# 4DLab Obsidian Vault — Implementation Plan

**Author:** architect session · **Date:** 2026-06-09
**Target vault root:** `Vault/`
**Driving skill:** `_skills/graph/4dlab-vault/` (authored alongside this plan)
**Scope this session:** plan + skill files. Populating the OBD vault is the
*next* step (running the skill), not this session.

> Governing rule (unchanged): every field added to any schema must have a
> **named, existing consumer**. That applies to the vault's own frontmatter
> too — see the consumer table in §4. A field no view or command reads does
> not ship.

---

## 1. What the inputs actually are

`ObsidianProp.md` is a **descriptive sample**, not a spec to copy. It sketches a
"graph-aware monorepo vault": a rigid frontmatter schema, two grep commands
(`/graph-find`, `/check-impact`), a `CLAUDE.md` manifest, and an operational
checklist. We adapt the *ideas*, not the text.

The four `Vault/Obsidian*.md` files are **generic upstream skills** — raw
material, not adapted to us:

| File | Surface | Disposition |
|---|---|---|
| `ObsidianBase.md` | Obsidian Bases (`.base` dynamic views) | **Adopt** — core of graph-aware views |
| `ObsidianMDS.md` | Obsidian-Flavored Markdown | **Adopt a trimmed subset** (frontmatter, wikilinks, embeds, callouts, tables, mermaid) |
| `ObsidianCLI.md` | Obsidian CLI v1.12 (needs desktop running) | **Optional appendix** — query-only, env-gated |
| `ObsidianSessions.md` | `sync-claude-sessions` | **Out of scope** — orthogonal to a code/wiki vault |

### Keep / drop from `ObsidianProp.md`

**Keep:** the frontmatter-node idea (`module / implements / consumers /
drift_guards / tags`); the two grep commands; a vault `CLAUDE.md` manifest; a
`System-Map.md` index; the "trace before you change" checklist.

**Drop:** its invented constraints (`2.5 MB` asset cap, `250 ms p95`) — not ours
and unverifiable here; its `Application/<module>` layout — replaced by our
`labs/<lab>/` layout; its `~/.claude/commands/` placement — our commands live in
the skill and (optionally) the vault `.claude/`.

---

## 2. The DLD / PRD / HLD / LLD / vocabulary question (answered)

The 4-tier vault model separates two distinct source folders that were previously
conflated under `wiki/`:

| Vault tier | Source folder | Graph piece | State |
|---|---|---|---|
| code | `labs/obdlab/obdlab/` | `graph/v2_code/` | finished |
| tests | `labs/obdlab/tests/` | `graph/v2_tests/` | finished |
| wiki | `labs/obdlab/research/chunks/` | `graph/v2_wiki/` (451 nodes) | finished |
| docs | `labs/obdlab/docs/` | `graph/v2_docs/` | **pending TODO-4 graphify** |

The `research/chunks/` corpus (wiki tier) is graphified; the design docs
(docs tier) are **not yet graphified** — the `graphify-out/manifest.json` ingest
set is `research/chunks/**` + `vocabulary.py`, not the design docs. The docs-tier
vault copy is gated on **TODO-4** (doc-prep skill → graphify → `graph/v2_docs/`).
DLD/HLD/LLD/PRD live *inside* `labs/obdlab/docs/`, and `vocabulary.py` is part of
the code.

The obsolete `OBDLab_KG_Wiki.md` (old v1 baseline, `graph/v1_baseline/`) was
archived 2026-06-10 to `ARCHIVE/2026-06-10_obsolete-wiki/`; the `v2_wiki` piece
(`research/chunks`) supersedes it.

**So:**

- **Do you need them for full understanding? Yes.** The HLD→LLD→DLD→code chain
  is exactly what turns a vault from "a pile of `.py`" into something navigable.
  They are the design context that makes the graph legible.
- **Do you need a separate graphify step for the docs tier? Yes — TODO-4.**
  The wiki tier (`research/chunks`) is already graphified; the docs tier
  (`docs/`) needs its own graphify run (gated by TODO-4) before it can carry
  graph-aware frontmatter.
- **How they enter the vault:** copying `docs/` brings DLD/HLD/LLD/PRD as plain
  markdown; `vocabulary.py` rides along with the code copy. They become
  *navigable nodes* by getting vault frontmatter (§4), not by re-extraction.
  Wiki notes enter from `research/chunks/` → vault `wiki/`.

**Net recommendation:** four tiers, separate sources; copy, don't re-graphify;
give the design docs (DLD/HLD/LLD/PRD) their own `node_type` so Bases can show
the design→code→test spine. The `wiki/` folder is **retired** — it is no longer
a source for the vault.

---

## 3. Vault layout

Obsidian renders and graphs **`.md` notes**. Copied `.py`/test files are
*browsable link targets*, not graph nodes — the graph-awareness lives in the
`.md` frontmatter (§4), derived from `graph.json` but authored, not auto-dumped.

```
Vault/
├── CLAUDE.md                 # vault manifest: layout, rules, how to navigate
├── System-Map.md             # index of finished labs + entry points + base links
├── _bases/
│   ├── modules.base          # every note grouped by lab → module
│   ├── consumers.base        # SIGNAL/NOISE audit: note → named consumer(s)
│   └── drift-guards.base     # design/code → guarding tests (coverage map)
├── _meta/
│   └── PROVENANCE.md         # what was copied, when, from which source paths
├── _vocabulary/             # standalone cross-lab vocab notes (T-VAULT-VOCAB-1)
│   └── OBD_VOCABULARY.md     # sourced from labs/semantic/vocabul/ (canonical); node_type: wiki
└── labs/
    └── obdlab/               # ONLY finished labs (OBD is the only one now)
        ├── _OBDLab.md        # lab landing note (node_type: lab-index)
        ├── code/             # raw copy of labs/obdlab/obdlab/ (graphified source)
        ├── tests/            # raw copy of labs/obdlab/tests/
        ├── wiki/             # copy of labs/obdlab/research/chunks/ + injected frontmatter
        └── docs/             # copy of labs/obdlab/docs/ + injected frontmatter
```

**Not copied:** `graph.json` / `graphify-out/`. It stays canonical at its source
and is *read* during the build to inform frontmatter. (If you later want the
graph artefact in-vault for offline reference, that's a one-line add — flagged
in follow-ups, not done by default, to honor "only code/test/wiki/docs copied".)

**Existing `Vault/Obsidian*.md` files:** left in place (not my mess to move).
Recommendation — relocate them into `_skills/` since the adapted skill supersedes
them. Flagged in follow-ups; not done this session.

---

## 4. Frontmatter node schema (with named consumers)

Applied to **wiki `.md` notes** (design docs + KG wiki), lab landing notes, and
**`_vocabulary/` notes** (which reuse `node_type: wiki` — no new enum value
invented). Adapted from `ObsidianProp.md` and bound to our consumer model.

```yaml
---
node_type: wiki        # wiki | dld | hld | lld | prd | lab-index
lab: obdlab
module: obd_live_lab
subsystem: trim-analytics
implements:            # code paths this note specifies
  - "labs/obdlab/code/core/ve_engine.py"
consumers:             # downstream NAMED consumers — architect-authored
  - "comlab: fault_atlas fusion (perception channel)"
drift_guards:          # tests guarding the implemented code
  - "labs/obdlab/tests/unit/test_ve_engine.py"
tags: [obdlab, perception, finished]
source: "labs/obdlab/docs/DLD_OBDLab.md"   # provenance
---
```

**Signal/noise consumer table — every field is read by a named consumer:**

| Field | Named consumer (code path / view) |
|---|---|
| `node_type` | filter key in all three `.base` views |
| `lab` | `modules.base` top-level `groupBy`; lab landing note |
| `module` | `modules.base` grouping; `/graph-find <module>` |
| `subsystem` | `modules.base` row order; readability of the module group |
| `implements` | `/check-impact` (note→code map); `drift-guards.base` join |
| `consumers` | `consumers.base` (the signal/noise audit view); `/check-impact` |
| `drift_guards` | `drift-guards.base` (coverage map) |
| `tags` | Obsidian tag pane; `.base` `file.hasTag()` filters |
| `source` | `_meta/PROVENANCE.md`; rebuild/reconcile against the live lab |

No field is "future use." If a future field can't be placed in this table, it
doesn't ship — it goes to a proposal.

**`consumers` is architect-named, never auto-derived from `graph.json`.**
Auto-deriving would fabricate consumers and breach signal/noise. The build
script injects only the *mechanical* fields (`node_type`, `lab`, `module`,
`source`, `tags` skeleton); `implements` / `consumers` / `drift_guards` come
from the human-authored per-lab map (`assets/vault-map.<lab>.yaml`).

---

## 5. The skill: `_skills/graph/4dlab-vault/`

Single consolidated skill (sits in the existing `graph/` category beside
`4dlab-graphify-run`). Bundles only what our case needs.

```
4dlab-vault/
├── SKILL.md                          # when/how to build or update the vault
├── reference/
│   ├── frontmatter-schema.md         # §4 schema + consumer table (authoritative)
│   ├── bases-and-views.md            # the 3 .base views: what each answers, how to extend
│   ├── obsidian-md-conventions.md    # trimmed OFM subset we actually use
│   └── obsidian-cli-optional.md      # OPTIONAL, env-gated: query a running vault
├── assets/
│   ├── modules.base
│   ├── consumers.base
│   ├── drift-guards.base
│   ├── lab-landing.md.tmpl
│   └── vault-map.obdlab.yaml         # OBD's architect-named consumer map
└── scripts/
    └── build_lab_vault.py            # copy + frontmatter-skeleton inject; dry-run default
```

**Excluded by design:** session-sync (not a code/wiki concern). **Optional:** CLI
appendix — only useful if you run Obsidian desktop v1.12+ with the Windows
`.com` redirector; the vault is *built* by file tools, so CLI is query-only.

**Architect-role note:** `build_lab_vault.py` is *vault tooling*, not lab
diagnostic code, and is not subject to the lab inner-loop/gates. It is authored
as part of the skill deliverable and is **not executed against the labs this
session**.

---

## 6. Build procedure (what running the skill does)

1. Confirm the lab is **finished + graphified** (code, tests, wiki, and a
   `graphify-out/graph.json` all present). OBD qualifies; no other lab does yet.
2. `build_lab_vault.py --lab obdlab --dry-run` → review the copy/inject plan.
3. Drop it without `--dry-run` → copies `code/`, `tests/`, `wiki/` into
   `Vault/labs/obdlab/`, injects frontmatter skeletons, fills semantic fields
   from `vault-map.obdlab.yaml`, writes the lab landing note.
4. Copy the three `.base` files into `Vault/_bases/`, refresh `System-Map.md`
   and `_meta/PROVENANCE.md`.
5. Open `Vault/` in Obsidian; confirm the three Bases render and
   `orphans`/`unresolved` are empty (or explained).

Idempotent: re-running updates in place, never duplicates.

---

## 7. Success criteria

- Opening `Vault/` in Obsidian shows OBD's `code/`, `tests/`, `wiki/` and a
  working graph view.
- All three `.base` views render with rows (modules grouped; every wiki note has
  ≥1 named consumer; every `implements` target has ≥1 `drift_guard` or is
  explicitly marked untested).
- **Consumer completeness:** no wiki note ships with an empty `consumers` list.
- No `graph.json` re-extraction was run.
- `build_lab_vault.py` is idempotent and dry-run-safe.

---

## 8. Unplanned follow-ups (not in this diff)

| Item | Why deferred / status |
|---|---|
| **`T-VAULT-VOCAB-1` — standalone `_vocabulary/OBD_VOCABULARY.md`** (`tasks/T-VAULT-VOCAB-1_standalone_obd_vocabulary_note.md`) | **DONE 2026-06-10.** `Vault/_vocabulary/OBD_VOCABULARY.md` built from canonical (body md5 `B14AFE09…` match); §4 frontmatter with 3 named consumers; `--vocab` build path idempotent; landing-note template updated with `[[OBD_VOCABULARY]]` wikilink; provenance recorded. Progress note at `tasks/progress_notes/T-VAULT-VOCAB-1.md`. |
| **`T-VAULT-PATHS-1` — docs/wiki convention + path refactor** (`tasks/T-VAULT-PATHS-1_docs_wiki_convention_paths.md`) | **DONE 2026-06-10.** 4-tier source mapping wired (code/tests/wiki=research-chunks/docs); all design-doc refs repointed wiki→docs; KG-wiki + OBDlab frames dropped; build dry-run resolves, no missing-note warning; graph/corpus untouched. Progress note at `tasks/progress_notes/T-VAULT-PATHS-1.md`. |
| `OBDLab_KG_Wiki.md` (obsolete v1 baseline) archived | **DONE 2026-06-10** → `ARCHIVE/2026-06-10_obsolete-wiki/obdlab/wiki/`. Superseded by the `v2_wiki` (`research/chunks`) piece. Frame-drop handled by T-VAULT-PATHS-1. |
| **`T-VAULT-PRD-V2-1` — refresh `PRD_OBDLab.md` v1→v2** (`tasks/T-VAULT-PRD-V2-1_refresh_prd_obdlab_v2.md`) | **DONE 2026-06-10.** TODO-4 precursor: PRD is still v1.0 (2026-05-22) while HLD/DLD/LLD/ADR/BDD are v2; reconcile to AST ground-truth so it can join the doc-prep set without seeding stale v1 fields. Architect-authoring lane. **Blocks T-VAULT-DOCPREP-1.** |
| **`T-VAULT-DOCPREP-1` — doc-prep the OBDLab design docs (TODO-4 pt 1)** (`tasks/T-VAULT-DOCPREP-1_doc_prep_design_docs.md`) | **DONE 2026-06-10.** Ran `4dlab-doc-prep` on the six v2 docs → `graph/v2_docs/ingest_ready/`; explicit ingest set excludes the generic `ADR.md`/`BDD.md` skill stubs + vocab duplicate. **Unblocks T-VAULT-DOCGRAPH-1.** |
| **`T-VAULT-DOCGRAPH-1` — graphify the docs tier → `graph/v2_docs/` (TODO-4 pt 2)** (`tasks/T-VAULT-DOCGRAPH-1_graphify_docs_tier.md`) | **DONE 2026-06-10** (ledger reconciled 2026-06-11). Docs-tier graph built → `graph/v2_docs/graph.json` (480 nodes / 1045 directed links, **100% EXTRACTED**, 0 isolated) + GRAPH_REPORT + html; proof-set spot-checked (SUPERSEDES 16, MIRRORS_CONTRACT_IN 9, CONSUMES 76, VERIFIES 93); `4dlab-graphify-run/SKILL.md` docs branch added; no collateral (other tiers + `research/chunks` + manifest clean). Built **deterministically** from the prepared explicit-relation blocks (live LLM backend was unauthenticated at run time) — source-anchored and auditable; the LLM-enrichment caveat is **closed by T-VAULT-DOCGRAPH-2** (0 real gaps). Both gate blocks clean in the note. Closes TODO-4; unblocks `T-VAULT-BUILD-1`. |
| **`T-VAULT-DOCGRAPH-2` — Pass-3 LLM cross-check of the docs graph (checker, not adder)** (`tasks/T-VAULT-DOCGRAPH-2_pass3_llm_crosscheck.md`) | **DONE 2026-06-10** (gate block transcribed from the cross-check artefact + ledger reconciled 2026-06-11). Ran `4dlab-graphify-run` Pass 3 (`--backend deepseek`, `deepseek-v4-pro`, default mode, est. $0.0238) over `ingest_ready/` → scratch `graph/v2_docs_llm/` (111 nodes / 84 edges); wrote `graph/v2_docs/PASS3_CROSSCHECK.md`. **Verdict: 0 real GAPs · 84 NOISE · 0 promotions** — all 6 signal-ish candidates were generic restatements of existing baseline edges at the same anchor. Canonical `v2_docs/graph.json` byte-unchanged; no edge entered any 4DLab graph. Probe was sparse (57/68 chunks) — completeness rests on DOCGRAPH-1's deterministic build, which it found nothing to add to. Both gate blocks now clean. |
| **`T-VAULT-WIKIGRAPH-1` — Pass-3 LLM cross-check of the wiki graph (checker, not adder)** (`tasks/T-VAULT-WIKIGRAPH-1_pass3_llm_crosscheck.md`) | **AUTHORED 2026-06-10, `pending`.** Pre-step health-check runnable now (`eval-wiki-graph --health-only`). Gated half runs Pass 3 over `research/chunks/` → scratch `graph/v2_wiki_llm/`, classifies → `graph/v2_wiki/PASS3_CROSSCHECK.md`. Eval skill: `_skills/graph/eval/eval-wiki-graph`. **Blocked by T-VAULT-DOCGRAPH-2 + explicit owner instruction to re-extract canonical `v2_wiki` (HARD RULE).** |
| **`T-VAULT-CODEGRAPH-1` — cross-check of the (AST) code graph (checker, not adder)** (`tasks/T-VAULT-CODEGRAPH-1_llm_crosscheck.md`) | **AUTHORED 2026-06-10, `pending`.** Part A = health-check (`eval-code-graph --health-only` → `graph/v2_code/GRAPH_HEALTH.md`), runnable now, satisfies "check the code graph". Part B = optional, gated LLM Pass-3 cross-check (expected near-pure-noise; AST is ground truth; precondition: confirm graphify supports an LLM pass over `.py`). Eval skill: `_skills/graph/eval/eval-code-graph`. **Part B blocked by T-VAULT-DOCGRAPH-2 + owner instruction.** |
| Relocate `Vault/Obsidian*.md` into `_skills/` | Pre-existing files; not this task's mess to move |
| Optionally copy `graph.json` into `Vault/labs/<lab>/graph/` | Conflicts with "only code/test/wiki"; decide explicitly |
| **`T-VAULT-BUILD-1` — populate the OBDLab vault (run `build_lab_vault.py`, 4 tiers)** (`tasks/T-VAULT-BUILD-1_populate_obdlab_vault.md`) | **DONE 2026-06-11** (ledger reconciled 2026-06-11 — row was stale at `pending` while the task file + progress note both read `done` and the vault is populated on disk: code 18 / tests 42 / wiki 63 / docs 10 files + `_obdlab.md` landing). Builder eligibility gate corrected to the four-tier model; build ran end-to-end → `Vault/labs/obdlab/` (code/tests/wiki/docs) + framed frontmatter on the 4 design docs + the 3 `.base` views + `PROVENANCE.md`; idempotent; no graphify re-extraction. **Gate 6/7 PASS, 2 residuals:** (5) `System-Map.md` auto-generation is outside the builder (no template/logic) — logged as §8 follow-up; the file exists, written separately. Owner-side **manual Obsidian render check still PENDING** (confirm the 3 Bases render with rows). Progress note: `tasks/progress_notes/T-VAULT-BUILD-1.md`. **Blocked by:** — (tiers present). |
| **`T-VAULT-WIKIFRAME-1` — frame the OBDLab wiki tier (7 topic READMEs, consumer-named)** (`tasks/T-VAULT-WIKIFRAME-1_frame_obdlab_wiki_topic_notes.md`) | **DONE 2026-06-11.** Added `§4` frontmatter to the 7 canonical `research/chunks/<topic>/README.md` files (each with grep-pinned COMLab consumers, implements, and drift guards) and added them to `vault-map.obdlab.yaml`. Rebuilt vault successfully, raising framed notes from 4 to 11. Restored and verified the `labs/obdlab` test suite (388 tests green). Progress note at `tasks/progress_notes/T-VAULT-WIKIFRAME-1.md`. |

| Add COMLab/GASLab/DTCLab/DNA labs to the vault | Not finished/graphified yet — copy only finished labs |
| Wire `/graph-find` `/check-impact` as vault `.claude/commands/` | Optional; skill documents them first |
