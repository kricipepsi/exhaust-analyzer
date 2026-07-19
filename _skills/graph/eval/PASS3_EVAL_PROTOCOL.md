# Pass-3 graph evaluation protocol (code · wiki · document)

**Author:** architect (4DLab) · **Date:** 2026-06-10 · **Status:** spec (for a coder / graph-tooling session to run)
**Question this answers:** *Does graphify's Pass 3 (an LLM re-reading the same sources) ADD genuine missing edges to a graph, or only NOISE?*

> **Premise note (for the record).** The driving request named "GW-ENH-3", but that
> is GASLab vocab-path/citation housekeeping (done; its own rules forbid running
> graphify). The real Pass-3 task is **`T-VAULT-DOCGRAPH-2`** in `Vault/tasks/` —
> "run Pass 3 into a scratch dir, diff vs the deterministic graph, classify
> CONFIRMED/GAP/NOISE, promote nothing". This protocol generalises that single
> (document-only) task to all three graph types the owner asked for.

---

## The principle: checker, not adder

Every 4DLab graph is built **deterministically** (AST for code; the chunks'
explicit relation blocks for wiki/docs). No LLM-inferred edge has ever entered a
canonical graph — that is the *auditable-by-construction* position the signal/noise
rule wants. Pass 3 can break it by adding plausible-but-unsourced edges.

So Pass 3 is run **as a checker**. It earns its keep only if it finds an
`EXTRACTED` edge, between two **existing** nodes, with a **named consumer**, that
the deterministic pass missed. Everything else is noise. **Nothing is promoted
into a canonical graph by this evaluation** — a confirmed gap is fixed at source
(re-run the deterministic pass) and re-derived, never patched in from the LLM graph.

(Owner gloss: a "consumer" is the later piece of code that actually reads an edge.
An edge no code reads is noise, however plausible it looks.)

---

## The three-step flow (per graph type)

1. **Save the baseline.** The canonical `graph/<tier>/graph.json` is already the
   baseline — leave it byte-unchanged. (Optionally snapshot it first:
   `cp graph/<tier>/graph.json graph/<tier>/graph.baseline.json`.) The evaluator
   only ever *reads* it.
2. **Run Pass 3 into a separate scratch dir.** Use `4dlab-graphify-run` with
   `--backend deepseek` in **default mode** (never `--deep` — deep mode is defined
   to emit more INFERRED edges, the opposite of intent). Relocate the result to
   `graph/<tier>_llm/` so the canonical dir is never touched.
3. **Compare and classify.** Run the matching eval skill's script (below). It emits
   `graph/<tier>/PASS3_CROSSCHECK.md` with every LLM edge classified
   CONFIRMED / CANDIDATE_GAP / NOISE plus a health delta. The agent then names a
   consumer for each CANDIDATE_GAP or demotes it to NOISE.

---

## Per-type readiness — READ THIS BEFORE RUNNING

The three tiers are **not** symmetric. Pass 3 reads from an `ingest_ready/`
staging dir; only the docs tier has one, and CLAUDE.md forbids re-running
`v2_code`/`v2_wiki`/`v2_tests` extraction unless explicitly instructed.

| Tier | Baseline (measured 2026-06-10) | `ingest_ready/`? | Pass-3 producible today? | Eval skill |
|---|---|---|---|---|
| **document** (`v2_docs`) | 480 nodes / 1045 edges · 100% EXTRACTED · 0 dangling · 0 isolated | **yes** | **Yes** — DeepSeek configured; this is `T-VAULT-DOCGRAPH-2` | `eval-doc-graph` |
| **wiki** (`v2_wiki`) | 451 nodes / 494 edges · 408 EXTRACTED / 84 INFERRED / 2 AMBIGUOUS · 22 isolated | n/a (pre-chunked source) | **Gated** — source is `research/chunks/` (exists); running Pass 3 re-extracts a canonical graph → needs owner instruction | `eval-wiki-graph` |
| **code** (`v2_code`) | 188 nodes / 492 edges · 249 EXTRACTED / 243 INFERRED (~50%) | n/a (AST source) | **Gated + uncertain** — Pass 3 is for prose; confirm graphify even supports an LLM pass over `.py`. Highest noise risk (AST is already truth) | `eval-code-graph` |

**Consequence / tradeoff to surface to the owner:** the document graph can be
evaluated now end-to-end. The wiki graph's source (`research/chunks/`) exists, so
its Pass-3 graph is producible — but only with an explicit owner instruction,
since running it **re-extracts a canonical graph** (the HARD RULE). The code graph
is doubly gated: same re-extraction rule, **plus** it is unclear graphify even
supports an LLM pass over `.py` (Pass 3 is a prose instrument), and the code check
is normally just the always-on health-check anyway. The eval **skills** for all
three are ready and verified. Recommended sequencing: run docs first (cleanest
test — 100% EXTRACTED baseline), see whether Pass 3 yields any real GAP, and only
then decide whether re-extracting wiki — or attempting code — is worth the cost.

**Health-check is always available, ungated.** Every eval skill also runs in a
single-graph **health-only** mode (omit the second graph argument): it reads the
canonical `graph.json` and reports a GOOD/CHECK condition verdict with no LLM pass,
no re-extraction and no tokens. That is the "confirm the graph is in good
condition" test, and it is the default deliverable for the code tier.

---

## Classification rubric (shared) and per-type signal/noise

Every LLM edge lands in exactly one class:

| Class | Rule (objective — the script decides) |
|---|---|
| **CONFIRMED** | edge already in baseline → proves completeness, no action |
| **CANDIDATE_GAP** | `EXTRACTED` + both nodes exist + missing from baseline + relation in the tier's **signal** set → agent must name a consumer or demote |
| **NOISE_inferred** | confidence ≠ `EXTRACTED` (INFERRED / AMBIGUOUS) |
| **NOISE_new_node** | an endpoint is absent from the baseline (LLM invented a node) |
| **NOISE_generic_rel** | `EXTRACTED` but the relation is in the tier's **generic** set (no consumer value) |
| **BASELINE_ONLY** | in baseline, the LLM did not find it — informational |

The **named-consumer** step is judgment the script cannot do; the agent fills it
from the report skeleton. No consumer ⇒ the row is NOISE (or, if a *new* consumer
can be specced, a **proposal** in `comlab/config/proposals/` — never the live graph).

**Signal vs generic relations per tier** (from the measured relation vocabularies):

- **document** — signal: `CONSUMES, GATED_BY, ROUTES_TO, VERIFIES, ENUMERATES, DERIVED_FROM, MIRRORS_CONTRACT_IN, SUPERSEDES, OWNED_BY`; generic (noise-prone): `MENTIONS, DESCRIBES`. Consumer anchor: **COMLab analytics / fault-atlas routing**.
- **wiki** — signal: `consumed_by, indicates, maps_to, routes_to, produces, produces_negative, raises, emits, requires, suppresses, refines, triggers`; generic (organizational): `documents, member_of, has_value`. Consumer anchor: **COMLab analytics / fault-atlas routing**.
- **code** — signal (AST-structural, ground truth): `calls, contains, inherits, method, uses, references, rationale_for`; no auto-generic class (the discriminator is confidence + AST-truth scrutiny). Consumer anchor: **graph navigation / drift-guards / design→code→test spine** (NOT COMLab analytics). A code CANDIDATE_GAP is a *candidate AST blind spot* and must be validated against the source before it counts.

---

## Success criteria (mirror `T-VAULT-DOCGRAPH-2`, per tier)

1. **Separate-dir guard.** Pass-3 output lands in `graph/<tier>_llm/`; canonical
   `graph/<tier>/graph.json` is byte-unchanged (`git status --porcelain` + mtime);
   no surviving root `graphify-out/`.
2. **Default mode confirmed.** Run used `--backend deepseek` and **no** `--deep`
   (record the exact command in the progress note).
3. **Report exists.** `graph/<tier>/PASS3_CROSSCHECK.md` classifies every LLM edge
   as exactly one class, with counts. Each surviving GAP names src→tgt, relation,
   source anchor, and the named consumer.
4. **No silent promotion.** Zero edges written into any canonical `graph.json`.
5. **Health sanity** on the LLM graph reported (nodes/links > 0, confidence split).
   A high INFERRED share is expected and is what the gate filters — report, don't act.
6. **No collateral.** All sibling graphs + `research/chunks/` + `graphify-out/manifest.json` byte-unchanged.

---

## Verdict template (what the coder writes back)

> **Tier:** `<document|wiki|code>` · **Run:** deepseek, default mode, `<date>`
> **Counts:** CONFIRMED N · CANDIDATE_GAP N (→ GAP N / demoted-NOISE N) · NOISE N · BASELINE_ONLY N
> **Verdict:** `BENEFICIAL` (≥1 real GAP with a named, live consumer) | `PURE NOISE — baseline complete` (the expected healthy result for a mature graph).
> **GAPs routed:** `<edge → 4dlab-doc-prep / extractor fix / proposal>` or `none`.

---

## Role / lane note

Authoring this protocol and the three eval skills is the **architect** deliverable.
**Running** Pass 3 and the comparison is a **coder / graph-tooling session** (no lab
inner-loop / 6-phase gate — graph tooling is not lab diagnostic code). The document
tier's run is already specced as `T-VAULT-DOCGRAPH-2`; this protocol extends the
same instrument to wiki and code once their `_llm` inputs can be produced.

---

## Unplanned follow-ups (off-scope discoveries — not actioned here)

| # | Finding | Suggested task |
|---|---|---|
| 1 | Wiki & code tiers have no `ingest_ready/`; Pass 3 cannot run on them without owner-instructed re-extraction (HARD RULE). | Owner decision + an ingest-path task per tier, **only if** the docs run shows Pass 3 finds real GAPs. |
| 2 | `build_lab_vault.py` reads a stale `graphify-out/graph.json`, not the canonical `graph/v2_docs/graph.json` (per the 2026-06-10 handoff). | Path-fix + consumer-wiring task (the handoff's recommended next task) — independent of this eval. |
| 3 | Only `CONSUMES` has a live reader; `GATED_BY/ROUTES_TO/VERIFIES` edges are built but unconsumed (per graph audit). | A GAP found by this eval is only "real" if its consumer is live — wiring those readers is its own task. |
