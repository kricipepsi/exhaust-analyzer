# Lab → Vault Pipeline — Execution Guide

**Scope:** how to take **one finished lab** (GASLab, DTCLab, COMLab, DNALab/VINLab — any lab
beyond OBDLab) from raw source all the way into the Obsidian vault, the same way OBDLab was
done. OBDLab is the worked example throughout.
**Audience:** the architect (who authors the task specs) and the coder/build sessions (who run
each step). Lane ownership is marked at every phase.
**Author:** architect session · **Date:** 2026-06-10

> **One rule above all (signal/noise):** nothing — no schema field, no graph edge, no vault
> frontmatter field (the small labelled header at the top of a note) — ships unless a **named,
> existing consumer** reads it on a real code path. "Future use" is not a consumer. This rule
> governs every phase below.

---

## 0. The pipeline at a glance

Four **corpora** (a corpus = one body of material of a single kind) per lab, carried through
four **phases**. Read top-to-bottom:

```
            CODE (.py pkg)     TEST CODE (.py)    WIKI (<wiki-dir> .md)        DOCS (HLD/DLD/LLD/ADR/BDD/PRD .md)
            ───────────────    ───────────────    ─────────────────────────   ─────────────────────────────────
PHASE 1     codingskills        codingskills        prose correct at source     author/reconcile to v2
prepare     audit + clean       (tests green)       (<wiki-dir>)                (the "PRD refresh" model)
the 4 sets  THEN graph-legible
            (coder lane)        (coder lane)        (architect/author lane)     (architect/author lane)
                │                   │                       │                           │
PHASE 2     4dlab-code-prep     4dlab-code-prep     4dlab-wiki-prep             4dlab-doc-prep
prep for    (probe/audit)       (on tests/)         (relations/labels/roster)   (explode/tables/anchor/relations)
ingestion       │                   │                       │                           │
                ▼                   ▼                       ▼                           ▼
PHASE 3     graphify Pass 1     graphify Pass 1     graphify Pass 3             graphify Pass 3
ingestion   (AST, offline)      (AST, offline)      (LLM, costs tokens)         (LLM, costs tokens)
  via           │                   │                       │                           │
4dlab-          ▼                   ▼                       ▼                           ▼
graphify-run  graph/v2_code/      graph/v2_tests/     graph/v2_wiki/              graph/v2_docs/
                └───────────────────┴───────────┬───────────┴───────────────────────────┘
                                                 ▼
PHASE 4                              4dlab-vault  →  build_lab_vault.py
copy to vault                        copies all four tiers into Vault/labs/<lab>/ and injects
                                     consumer-aware frontmatter; never re-extracts the graph
```

Two facts that explain the whole shape:

- **Code and tests are `.py`** → graphify reads them with **Pass 1** (tree-sitter AST — a static
  read of the code's structure with no language model, so it's offline and free). Their graph
  quality depends only on what's *statically visible* in the source.
- **Wiki and docs are `.md` prose** → graphify reads them with **Pass 3** (an LLM semantic pass —
  costs tokens). Their graph quality depends on how *explicit* the relationships are in the text.

That is why code is *cleaned/refactored* (restructured without changing behaviour) before prep,
while wiki/docs are *made explicit* before prep — different levers for different passes.

---

## 1. Lanes and the one-task rule (read before starting)

- **Architect lane** — authors the task spec (the file under `<pack>/tasks/`): pins the bounds,
  citations, the **named consumer**, success criteria, and the file list. The architect's "done"
  is an unambiguous spec, not green tests.
- **Coder / build lane** — executes one spec: edits code/wiki/docs, runs the inner loop
  (`ruff` → `pyright` → `pytest`; `ruff`/`pyright` are the linter and type-checker — automated
  code-quality checks), fills the `VERIFICATION GATE` + `CODE REVIEW` blocks in the progress note.
- **One task per session.** Finish exactly one task, update its ledger row, then stop and clear
  context. The next task starts fresh from the pack's `*_START_HERE.md`.
- **Atomic registration.** Writing a task file and adding its row to the ledger are one operation.

Each corpus-phase below is normally **one task** = **one session**. A full lab is therefore a
chain of tasks, run in dependency order (template in §7).

---

## 2. Phase 0 — Lab readiness gate

A lab is eligible for this pipeline only when **all four inputs exist and are finished**
(`4dlab-vault` enforces this before it will copy anything):

```
labs/<lab>/<lab>/            ← production source package   (code corpus)
labs/<lab>/tests/            ← test suite                  (test corpus)
labs/<lab>/<wiki-dir>/       ← wiki / domain prose         (wiki corpus)
labs/<lab>/docs/             ← HLD/DLD/LLD/ADR/BDD/PRD      (docs corpus)
```

> **`<wiki-dir>` is lab-specific** — the wiki corpus folder name varies by lab:
> OBDLab uses `research/chunks/`, **GASLab uses `wiki/`**. Take the literal value
> from the lab's pack `*_START_HERE.md`. Throughout this guide `<wiki-dir>` stands
> wherever OBDLab's worked example would otherwise hardcode `research/chunks/`.

If any is missing or still in flux, **stop** — do not half-populate. As of 2026-06-10 only
**OBDLab** qualifies; the other labs reach the gate as they finish.

**Architect action:** confirm the four inputs, then author the task chain (§7). **Do not** run a
prep skill on a lab that hasn't passed this gate.

---

## 3. Phase 1 — Prepare the four sets (source-level correctness)

Goal: get each corpus *correct and clean at the source* **before** any graph work, so the graph
is built once on good material and not churned by a later refactor.

### 1A · CODE — audit with `_skills/codingskills` FIRST, then confirm graph-legibility

This is the step the owner pinned: **code is audited and cleaned with the general
code-quality skills before the graphify-specific prep.** Order matters — refactoring after the
graph is built would force a re-extraction.

Run these from `_skills/codingskills/` (coder lane; each changes code and re-runs the inner loop):

| Skill | What it does for the code |
|---|---|
| `improve-codebase-architecture` | Finds **deepening opportunities** — turning shallow modules (interface nearly as complex as the implementation) into deep ones; cleaner module seams ⇒ cleaner graph communities. |
| `uncle-bob-craft` | Clean-Architecture / SOLID / dependency-rule review; boundaries and code smells. |
| `code-simplifier` | Reduces nesting/redundancy **without changing behaviour**; clearer names (the name *is* the future graph node label). |
| `code-review-excellence` | Systematic review pass; catches defects before they're frozen into the graph. |
| `pythonskill` (python-expert-coder) | PEP 8, modern 3.10+ patterns, security gating, the generate-validate-fix loop. |

Then make the package **AST-legible** for graphify (still coder lane) — the levers `4dlab-code-prep`
will audit in Phase 2: explicit named imports (no `from x import *`), a `__all__` public surface,
type hints on public signatures, domain states as real `Enum`/`StrEnum`s (a fixed set of named
values), and `# WHY:` rationale comments on non-obvious gates/formulas. Numeric literals in
`gaslab/`/`obdlab/` must carry their wiki-citation comment.

**Exit criterion:** tests green, inner loop clean, code reads cleanly. The graph isn't built yet.

### 1B · TEST CODE — green and meaningful

Tests are `.py`, so they become their own graph (`v2_tests`). Before that they must be green and
actually assert behaviour. The `_skills/codingskills/ecc-subset/` skills cover this lane:
`python-testing`, `verification-loop`, `ai-regression-testing`, `eval-harness`. **Exit criterion:**
`pytest` green; tests map to real schema/rules (these become the `VERIFIES` / `drift_guards` edges).

### 1C · WIKI — prose correct at source (`<wiki-dir>`)

The wiki tier is the already-chunked domain corpus under `<wiki-dir>`. Phase 1 here is just
confirming the prose is current and citation-backed; the explicit-relation work is Phase 2. **Do
not** move or rename `<wiki-dir>` — it is graph-canonical at its source.

### 1D · DOCS — author / reconcile each design doc to v2

The six design docs (`HLD / DLD / LLD / ADR / BDD / PRD`) must each describe the **shipped** code,
not a superseded version — exactly the OBDLab **PRD refresh** model (`T-VAULT-PRD-V2-1`): bump the
version, reconcile every field/bound/enum/exception to the AST ground-truth, drop pruned values,
keep numeric literals' wiki citations. This is **architect/author lane** (design-doc authoring, no
inner-loop). **Exit criterion:** all six docs are current v2 peers; superseded blueprints and
duplicates are excluded/archived.

> **Exclusion discipline (learned on OBDLab):** the `docs/` folder can contain non-design-doc files —
> generic skill stubs (`ADR.md`, `BDD.md`), a vocabulary **duplicate** (`OBD_VOCABULARY.md`, which has
> its own `_vocabulary/` vault home), handoff/inventory notes, and superseded blueprints (`OBDlab.md`).
> Phase 2 doc-prep must ingest an **explicit file list**, never a `docs/*.md` glob.

---

## 4. Phase 2 — Prepare data for ingestion (the prep skills)

Each corpus has its **own** prep skill. Do not cross the streams (the single most common mistake).
These skills **never** write `graph.json` and **never** run graphify.

| Corpus | Prep skill | Operations | What it produces |
|---|---|---|---|
| code | `4dlab-code-prep` | `probe` → `audit` → `report` | a fix-plan against AST-legibility rules; the coder applies fixes (it does **not** auto-edit source) |
| test code | `4dlab-code-prep` | same, scoped to `tests/` | same, for the test package |
| wiki | `4dlab-wiki-prep` | `relations` → `labels` → `roster` → `verify` | append-only trailer blocks making implied links **explicit** + canonical entity labels |
| docs | `4dlab-doc-prep` | `explode` → `tables` → `anchor` → `relations` → `verify` | `graph/v2_docs/ingest_ready/<doc>/…` — monolith split by header, tables → entity blocks, lineage anchor + architectural relation lines |

Key distinctions:

- **Code/test prep is an *audit*, not a rewrite.** `4dlab-code-prep` probes what your local
  graphify build actually extracts, then reports violations as `file:line → rule → fix`. A blanket
  auto-rewrite is forbidden (unreviewable diff). Code-prep **excludes** `tests/` and `research/`
  when scoped to the production package — the test corpus is prepped as its own run.
- **Wiki/doc prep makes relations EXTRACTED.** graphify tags an edge `EXTRACTED` (full confidence)
  only when the text states it directly; otherwise `INFERRED`/`AMBIGUOUS`. The prep appends explicit
  `**SUBJECT** PREDICATE **OBJECT**` lines so the LLM extracts facts instead of guessing. **Every
  `CONSUMES`/`VERIFIES` line must name a real, existing code path or test** — orphans are flagged,
  proposals stay labelled as proposals (never promoted to live). This is signal/noise at the edge.
- **Docs are monolithic; wiki is pre-chunked.** That's why docs get the extra `explode`/`anchor`/
  `tables` steps and wiki goes straight to `relations`.

---

## 5. Phase 3 — Ingestion (run graphify) via `4dlab-graphify-run`

One skill builds **all** corpora; it auto-routes by file type. Flow per corpus:
`resolve → run → relocate → verify`.

| Corpus | Pass | Cost | Destination graph dir | Directed? |
|---|---|---|---|---|
| code | Pass 1 (AST) | free, no key | `graph/v2_code/` | usually undirected |
| test code | Pass 1 (AST) | free, no key | `graph/v2_tests/` | usually undirected |
| wiki | Pass 3 (LLM) | tokens + backend | `graph/v2_wiki/` | `--directed` |
| docs | Pass 3 (LLM) | tokens + backend | `graph/v2_docs/` | `--directed` |

> **Note for the docs corpus:** `4dlab-graphify-run` originally documented only **code** and
> **wiki** branches. The **docs branch** (dest `graph/v2_docs/`, prep skill `4dlab-doc-prep`,
> verify focus = the architectural-predicate proof-set) is being added under `T-VAULT-DOCGRAPH-1`.
> Confirm that branch is present in the skill before running the docs corpus on a new lab.

**Hard guards (these are the failure modes — never skip):**

- **Never `/graphify .` from a repo root.** Always scope to the specific package or chunks
  directory (this is the rule the 81.9k-node incident exists to enforce).
- **Never re-extract a canonical graph.** A verified `graph.json` is canonical; do not rebuild it
  unless explicitly instructed.
- **Relocate, then confirm no root `graphify-out/` survives.** Move `graph.json` + `GRAPH_REPORT.md`
  + `graph.html` into the destination dir.
- **No collateral.** The other `graph/*` dirs must be byte-unchanged (`git status --porcelain` +
  mtime).
- **Verify:** node/edge counts > 0; relation distribution; isolated-node count; for Pass-3 corpora
  confirm **EXTRACTED dominates**; spot-check the key symbols / proof-set. A missing edge is a
  **prep gap routed back to the prep skill** — never patched into `graph.json`.

---

## 5.5 Phase 3 verify — confirm each graph is in good condition (eval skills)

Once a graph is built, prove it is sound **before** it feeds the vault. The eval
skills under `_skills/graph/eval/` (`eval-code-graph`, `eval-wiki-graph`,
`eval-doc-graph`) provide one runnable test per tier, plus the shared procedure
`_skills/graph/eval/PASS3_EVAL_PROTOCOL.md`. There are two levels — run the first
always, the second only when you deliberately want to test an LLM pass.

### A. Health-check (always run — confirms the graph is in good condition)

Single-graph, reads the canonical `graph.json` only — **no LLM pass, no
re-extraction, no tokens, no owner gate.** It reports nodes, edges, density,
dangling edges, isolated nodes, the confidence split and the top hubs, then a
**GOOD / CHECK** verdict.

```bash
# one line per tier; omit the second graph arg ⇒ health-only mode
python _skills/graph/eval/eval-code-graph/scripts/eval_code_graph.py labs/<lab>/graph/v2_code/graph.json
python _skills/graph/eval/eval-wiki-graph/scripts/eval_wiki_graph.py labs/<lab>/graph/v2_wiki/graph.json
python _skills/graph/eval/eval-doc-graph/scripts/eval_doc_graph.py  labs/<lab>/graph/v2_docs/graph.json
```

Read the verdict like this:

- **dangling > 0** is always a defect (an edge points to a node that isn't there) → fix the prep/extraction.
- **isolated > 0** is a defect for **code** and **docs** (every node should be wired) but **expected for wiki**
  (fault/enum stubs await their relations) — the wiki skill knows this and does not flag it.
- **EXTRACTED should dominate** on Pass-3 (wiki/docs) graphs. Code/test (Pass-1 AST) graphs carry a higher INFERRED
  share by nature; that is a baseline property, not a fault.

Reference result on OBDLab (2026-06-10, all **GOOD**): docs 480/1045, 100% EXTRACTED, 0 isolated · wiki 451/494,
EXTRACTED-dominant, 22 isolated (expected) · code 188/492, ~50% INFERRED, 0 isolated.

### B. Pass-3 cross-check (checker, not adder — optional, gated)

The deeper test: did an LLM re-reading the same source find a real edge the
deterministic pass missed, or only noise? Run an LLM Pass 3 into a **separate
scratch dir** (`graph/<tier>_llm/`), then give both graphs to the eval skill,
which classifies every LLM edge CONFIRMED / CANDIDATE_GAP / NOISE and writes
`graph/<tier>/PASS3_CROSSCHECK.md`. **It promotes nothing** — a confirmed gap is
made explicit at source and the deterministic pass re-run, never patched into
`graph.json`. The agent names a live consumer for each CANDIDATE_GAP or demotes it.

This is gated, because producing the LLM graph **re-extracts a canonical graph**
(HARD RULE → needs explicit owner instruction) and costs tokens. Run order:
**docs first** (cheapest, 100%-EXTRACTED baseline — the cleanest test), then decide
whether wiki/code are worth it. On the **code** tier the AST is already ground
truth and the graph is already ~50% INFERRED, so Pass 3 there is expected to be
almost pure noise — the code check is normally just the Part-A health-check.

Tasks: `T-VAULT-DOCGRAPH-2` (docs), `T-VAULT-WIKIGRAPH-1` (wiki), `T-VAULT-CODEGRAPH-1` (code).
Full rubric, signal/noise relation sets per tier, and success criteria: `_skills/graph/eval/PASS3_EVAL_PROTOCOL.md`.

---

## 6. Phase 4 — Copy to the vault via `4dlab-vault`

The vault is a **read-mostly window** onto finished labs — it never re-extracts the graph; it
*reads* the existing `graph.json` to inform frontmatter. Build with
`scripts/build_lab_vault.py` (idempotent — re-running updates in place, never duplicates; always
`--dry-run` first).

What it copies into `Vault/labs/<lab>/`:

| Vault tier | Source folder | In vault as |
|---|---|---|
| `code/` | `labs/<lab>/<lab>/` | raw `.py` (browsable link targets, not graph nodes) |
| `tests/` | `labs/<lab>/tests/` | raw test files (link targets) |
| `wiki/` | `labs/<lab>/<wiki-dir>/` | `.md` notes **+ injected frontmatter** |
| `docs/` | `labs/<lab>/docs/` | `.md` design docs **+ injected frontmatter** |

Plus the shared, cross-lab `Vault/_vocabulary/` area (built once via `--vocab`).

Steps: (0) build `_vocabulary/` if not already; (1) verify eligibility — Phase 0; (2) author/confirm
`assets/vault-map.<lab>.yaml` — the **architect-named** consumer map (module / subsystem /
implements / consumers / drift_guards per note); (3) `--dry-run`; (4) build; (5) copy the three
`.base` views (the saved queries that make the vault graph-aware) into `Vault/_bases/`, refresh
`System-Map.md` + `_meta/PROVENANCE.md`; (6) open in Obsidian — confirm the three Bases render and
`orphans`/`unresolved` are empty or explained.

**`consumers` is human-authored, never auto-derived from the graph** — auto-deriving fabricates
consumers and breaks signal/noise. An empty `consumers` list = that note is not ready to ship.

**Not copied:** `graph.json` / `graphify-out/`, caches, `tasks/`. Graph-awareness comes from the
injected frontmatter, not from dumping the graph file into the vault.

---

## 7. Per-lab task pack — sizing and the chain

### 7.1 The sizing rule

One session = one task (the hard rule never changes). The lever is **how big each task is drawn**,
not how many run per session. Size each task at **~⅓–½ of a fresh context**, and let the seam fall
where a *decision gets frozen*. Three cost signals decide the split:

- **Input load** — how much source must be read in.
- **Decision density** — irreversible judgment calls (a refactor — restructuring code without
  changing behaviour; naming a consumer; reconciling a doc to code). The expensive ones.
- **Tool churn** — edit→inner-loop cycles; each refactor pass burns context.

**Split fine** the high-decision work (code-clean, doc authoring, each prep skill, the vault
consumer-map). **Batch** the mechanical, verifiable work (the graphify runs). Batching is done by
*drawing one larger task*, not by running two tasks in a session.

### 7.2 The batched chain (what the architect authors)

IDs use `<LAB>` (e.g. `GAS`); model contents on the OBDLab vault tasks. "≈n" = how many sessions
that row typically expands to.

```
Phase 1   T-<LAB>-CODE-CLEAN     codingskills audit + AST-legible   (coder)   ≈1–3  split per module if large
          T-<LAB>-TESTS-GREEN    suite green + meaningful           (coder)   ≈0–1  folds into CODE-CLEAN if light
          T-<LAB>-DOCS-V2-a/b/c  6 design docs → v2, in 2–3 groups  (author)  ≈2–3  e.g. HLD+DLD+LLD / ADR+BDD / PRD
                                 (wiki: confirm <wiki-dir> current — usually no task)
                │ (Phase-1 done per corpus)
Phase 2   T-<LAB>-CODEPREP       4dlab-code-prep on package         (coder)   ≈1
          T-<LAB>-TESTPREP       4dlab-code-prep on tests/          (coder)   ≈0–1  may fold into CODEPREP
          T-<LAB>-WIKIPREP       4dlab-wiki-prep on <wiki-dir>      (author)  ≈1
          T-<LAB>-DOCPREP        4dlab-doc-prep on the 6 docs       (author)  ≈1
                │ (prep done per corpus)
Phase 3   T-<LAB>-GRAPH-AST      graphify code + tests (Pass 1, offline, free)  ≈1   batched: same cost profile
          T-<LAB>-GRAPH-LLM      graphify wiki + docs (Pass 3, token cost)      ≈1   batched, but separate from AST
                │ (all four graphs built + verified)
Phase 4   T-<LAB>-VAULT          author vault-map.<lab>.yaml + dry-run + build + bases   ≈1
```

Dependencies: each Phase-2 prep is blocked by its matching Phase-1 task; each graph by its prep;
the vault by all four graphs. The four corpora are independent until they converge at the vault, so
within a phase the sessions run in any order.

### 7.3 How many tasks for the whole process

**Budget ≈ 10–12 execution sessions for a typical single-package lab** (baseline 11):

| Phase | Sessions |
|---|---|
| 1 — prepare sources (code-clean, tests, docs ×2–3) | ≈ 4 |
| 2 — ingestion prep (4 prep skills) | ≈ 4 |
| 3 — graphify (AST batch + LLM batch) | ≈ 2 |
| 4 — vault (map + build) | ≈ 1 |
| **Total** | **≈ 11** |

Swing factors: a large multi-module package pushes code-clean to 2–3 sessions (→ ~13); folding
tests-green into code-clean and test-prep into code-prep pulls it to ~9. Plus **one architect
session up front** to author the whole pack (the task files + ledger rows) — separate from the
execution count. So: **1 authoring session + ≈10–12 execution sessions per lab.**

> **OBDLab is the cheap case** — code, tests, and wiki are already done through Phase 3, so its
> remaining pack is just the docs track: `T-VAULT-DOCPREP-1` → `T-VAULT-DOCGRAPH-1` → docs-tier
> vault copy ≈ **3 sessions**. A fresh lab (GAS/DTC/COM/DNA) is the full ≈10–12.

Each task file states: **Status / Pack / Mode / Blocked-by**, the **named signal/noise consumer**,
goal, success criteria, files-to-touch, out-of-scope, a verification block, and a progress hook.
The graph-tier graph's consumer is the **vault build's frontmatter derivation** + the
**design→code→test spine** in the three `.base` views — both real and existing once the vault is wired.

---

## 8. Worked example — OBDLab (the reference run)

OBDLab is the only lab through the pipeline so far. State as of 2026-06-10:

| Corpus | Phase 1 | Phase 2 prep | Phase 3 graph | Phase 4 vault |
|---|---|---|---|---|
| code | done (v2 rework) | done | `graph/v2_code/` ✓ | wired (build maps the tier) |
| tests | done (878-node corpus) | done | `graph/v2_tests/` ✓ | wired |
| wiki | done | done (`CHUNK_ENHANCEMENT_PREP_REPORT`) | `graph/v2_wiki/` ✓ (451 nodes, EXTRACTED-dominant) | wired |
| docs | PRD refreshed to v2 ✓ (`T-VAULT-PRD-V2-1`) | **done `T-VAULT-DOCPREP-1`** | **pending `T-VAULT-DOCGRAPH-1`** | unblocks after docs graph |

The docs tier is the live front: `T-VAULT-DOCPREP-1` (doc-prep the six v2 docs) → `T-VAULT-DOCGRAPH-1`
(graphify → `graph/v2_docs/`, **and** add the docs branch to `4dlab-graphify-run`). Once those land,
the docs-tier vault copy unblocks and OBDLab is fully populated — the template every other lab follows.

---

## 9. Quick reference (pin this)

| Corpus | Source | Phase 1 quality skill(s) | Phase 2 prep skill | graphify pass | Graph dir | Vault tier |
|---|---|---|---|---|---|---|
| code | `labs/<lab>/<lab>/` | `codingskills` (architecture, uncle-bob, simplifier, review, python) | `4dlab-code-prep` | Pass 1 AST | `graph/v2_code/` | `code/` |
| test code | `labs/<lab>/tests/` | `codingskills/ecc-subset` (testing, verification) | `4dlab-code-prep` | Pass 1 AST | `graph/v2_tests/` | `tests/` |
| wiki | `labs/<lab>/<wiki-dir>/` | prose currency check | `4dlab-wiki-prep` | Pass 3 LLM | `graph/v2_wiki/` | `wiki/` |
| docs | `labs/<lab>/docs/` (6 design docs) | author/reconcile to v2 | `4dlab-doc-prep` | Pass 3 LLM | `graph/v2_docs/` | `docs/` |
| — | build | — | `4dlab-vault` / `build_lab_vault.py` | reads graph, no extraction | — | all four + `_vocabulary/` |

**Never:** run graphify from a repo root · re-extract a canonical graph · auto-fill `consumers` ·
ship a field/edge/frontmatter key with no named consumer · cross the prep streams (code↔wiki↔doc).
