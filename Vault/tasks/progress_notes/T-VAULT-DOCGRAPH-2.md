# T-VAULT-DOCGRAPH-2 — progress note

## Plan

Run `4dlab-graphify-run` (resolve → run → relocate → verify → **Step 5 Pass-3 noise control**) over the prepared
`labs/obdlab/graph/v2_docs/ingest_ready/` chunks as a **checker**, not an adder. Command: `graphify extract
graph/v2_docs/ingest_ready --directed --backend deepseek` in **default mode** (NO `--deep`), scoped to that dir only
(never repo root — the 81.9k-node guard). Relocate the result to the **scratch** dir `graph/v2_docs_llm/` — never
over the canonical `graph/v2_docs/`. Diff the LLM graph against the deterministic `graph/v2_docs/graph.json` from
DOCGRAPH-1 and write `graph/v2_docs/PASS3_CROSSCHECK.md` classifying every LLM edge as `CONFIRMED` (EXTRACTED, both
nodes exist, already in baseline), `GAP` (EXTRACTED, both nodes exist, MISSING, **named** COMLab/fault-atlas
consumer → route to `4dlab-doc-prep`, re-run deterministic pass, never patch `graph.json`), or `NOISE`
(INFERRED/AMBIGUOUS/new-node/consumer-less → proposal-or-drop). Promote nothing into the canonical graph. Verify no
collateral on `v1_baseline`/`v2_code`/`v2_tests`/`v2_wiki`/canonical `v2_docs`, and no change to `research/chunks` or
`graphify-out/manifest.json`. Graph-tooling lane — no lab inner-loop/gate. Blocked by T-VAULT-DOCGRAPH-1.

Preflight: confirm `DEEPSEEK_API_KEY` is set and no stale `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` shadows it
(auto-detect order `gemini→kimi→claude→openai→deepseek`); name `--backend deepseek` explicitly regardless. Confirm
the runner's `graphifyy` is the intended version (DOCGRAPH-1 note recorded 0.8.36 in the run env, while
`.venv-wired` shows 0.8.35 — reconcile before spending tokens). DeepSeek backend works on either; default model
`deepseek-v4-flash`.


## VERIFICATION GATE

Completed 2026-06-10; gate block reconciled from `graph/v2_docs/PASS3_CROSSCHECK.md` on 2026-06-11 (run evidence
was written to the cross-check artefact but not transcribed here at run time).

- **Separate-dir guard:** LLM Pass-3 relocated to scratch `graph/v2_docs_llm/` (111 nodes / 84 edges), **never**
  over canonical `graph/v2_docs/`. Confirmed: `v2_docs/graph.json` mtime `2026-06-10 14:33` (DOCGRAPH-1 build)
  predates the cross-check run (`v2_docs_llm/` 18:04, `PASS3_CROSSCHECK.md` 18:12) → canonical graph untouched.
- **Default-mode command recorded:** `graphify extract graph\v2_docs\ingest_ready --backend deepseek --out .`
  with `GRAPHIFY_DEEPSEEK_MODEL=deepseek-v4-pro`, **NO `--deep`** (default mode). Cost 44,720 in / 62,621 out
  tokens, est. $0.0238, 22 min wall. Scoped to `ingest_ready/` only — no repo-root run (81.9k-node guard held).
- **LLM-graph confidence split:** EXTRACTED 81 · INFERRED 3 · AMBIGUOUS 0 (the nonzero INFERRED share is what
  the gate discards — reported, not acted on).
- **CONFIRMED / GAP / NOISE counts:** CONFIRMED 0 (vacuous — disjoint vocabulary, see methodology note) ·
  **real GAPs 0** · NOISE 84 (78 by the differ + 6 `unknown_rel` candidates demoted by adjudication) ·
  **0 promotions** into the canonical graph.
- **No collateral:** `git status --porcelain -- graph/v1_baseline graph/v2_code graph/v2_tests graph/v2_wiki
  research/chunks` clean; `graphify-out/manifest.json` unchanged.
- **Canonical `v2_docs` byte-unchanged:** the only new file under `graph/v2_docs/` is the report
  `PASS3_CROSSCHECK.md`; `graph.json` / `GRAPH_REPORT.md` / `graph.html` retain their 14:33 DOCGRAPH-1 bytes.

## CODE REVIEW

- **Diff walk:** the differ matched on exact `(source_id, target_id, relation)` tuples; that is near-vacuous
  here because the two graphs use disjoint vocabularies (baseline = controlled diagnostic relations; LLM =
  generic `references`/`implements`/`calls`), so `CONFIRMED 0` / `BASELINE_ONLY 1045` are vocabulary artefacts,
  not evidence of an incomplete baseline. The meaningful check was done by hand on the 6 signal-ish candidates.
- **Every candidate names a consumer or is demoted:** all 6 `unknown_rel` candidates demote to NOISE — each is
  a generic restatement of an edge the baseline already carries under a signal relation at the *same chunk
  anchor* (e.g. `OBDLivePayload→COMLab` echoes baseline `MIRRORS_CONTRACT_IN @ HLD/7:L48`). The
  `anti_orphan_s4→OBDLivePayload` row is the textbook anti-orphan case — its source chunk explicitly flags
  those fields as having no live COMLab reader, so promoting it would manufacture an orphan; correctly dropped.
- **Zero edges entered the canonical graph;** no `comlab/config/proposals/` entry created (none names a new
  diagnostic relationship with a nameable live consumer the baseline lacks). LLM graph stays scratch in
  `graph/v2_docs_llm/`.
- **Probe-coverage caveat (not a blocker):** the DeepSeek run covered 57/68 chunks (deepseek-v4-pro hit the
  16k output cap on the mega-chunk; some split halves failed to parse), so it is a sparse, conservative probe —
  it can surface a missed edge but cannot prove completeness by absence. Baseline completeness rests on
  DOCGRAPH-1's deterministic 100%-EXTRACTED build, which this run found nothing to add to.

> Both blocks clean · deliverable `PASS3_CROSSCHECK.md` complete · canonical graph unmodified → ledger row → `done`.
