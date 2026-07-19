---
node_type: task
task_id: T-VAULT-DOCGRAPH-2
status: done
pack: VAULT · **Mode:** GRAPH-TOOLING lane
lab: obdlab
mode: graph-tooling lane
blocked_by:
- T-VAULT-DOCGRAPH-1
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_docs — docs graph
- /check-impact command
- /graph-find command
- design→code→test spine (.base views)
implements:
- graph/v2_docs/graph.json
- graph/v2_docs_llm/graph.json
- graph/v2_docs/PASS3_CROSSCHECK.md
tags:
- task
- vault
- obdlab
---

# T-VAULT-DOCGRAPH-2 — Pass-3 LLM **cross-check** of the deterministic docs graph (checker, not adder)

**Status:** `done` (cross-check run 2026-06-10 — **0 real GAPs**; deliverable `graph/v2_docs/PASS3_CROSSCHECK.md`) · **Pack:** VAULT · **Mode:** GRAPH-TOOLING lane (graphify run — no lab inner-loop/gate)
**Origin:** Owner request 2026-06-10 — DOCGRAPH-1 built `graph/v2_docs/` **deterministically** (claude-cli auth
failed, fell back to the chunks' explicit relation blocks). DeepSeek backend is now configured; run Pass 3 as a
**verification instrument** over that deterministic graph. · **Blocked by:** T-VAULT-DOCGRAPH-1 (its
`graph/v2_docs/graph.json` is the baseline this task checks against).
**Consumer (signal/noise):** **Adds no schema field and writes no edge into the canonical graph by default.** The
deliverable is a **diff report** (`graph/v2_docs/PASS3_CROSSCHECK.md`). Its job is to *confirm* the deterministic
docs graph is complete and surface any genuinely-missing **EXTRACTED** edge. The downstream consumers are unchanged
from DOCGRAPH-1 — the **vault build** (`build_lab_vault.py` reads `graph/v2_docs/graph.json`), the **design→code→test
spine** in the three `.base` views (`modules.base` / `consumers.base` / `drift-guards.base`), and `/check-impact` /
`/graph-find`. A confirmed edge feeds those consumers **only after** it is made explicit in a chunk and the
deterministic pass re-run (via `4dlab-doc-prep`); it is **never** patched into `graph.json` from the LLM graph.

### Role note (graph-tooling lane) ###

Running `4dlab-graphify-run` is graph tooling, not lab diagnostic code — no `obdlab/` inner-loop / 6-phase gate. The
skill (incl. the new **Step 5 — Pass 3 noise control**) is authored; this task **runs** it (resolve → run → relocate
→ verify → cross-check) and emits the diff report. It **never** edits source/docs and **never** post-patches
`graph.json`.

### Why this task exists (the noise risk, stated plainly) ###

Every 4DLab graph to date is built from deterministic sources only (AST + the chunks' explicit relation blocks). No
LLM-inferred edge has ever entered a graph. That is the **auditable-by-construction** position the signal/noise rule
wants. Pass 3 (an LLM reading prose) can *break* that by adding plausible-but-unsourced edges. So Pass 3 is run here
**as a checker, not an adder**: it answers one question — *"reading the same prose, does the model find an EXTRACTED
edge, between two existing nodes, that has a named consumer, which the hand-authored relation blocks missed?"* —
and rejects everything else as noise.

```text
ASCII — checker flow (mirrors Step 5 of 4dlab-graphify-run):

  graph/v2_docs/graph.json  (deterministic baseline, DOCGRAPH-1) ──┐
                                                                    ├─►  DIFF  ─►  PASS3_CROSSCHECK.md
  graph/v2_docs_llm/graph.json  (Pass 3, deepseek, DEFAULT mode) ──┘            { CONFIRMED | GAP | NOISE }
        per LLM edge:
          EXTRACTED + both nodes exist + present in baseline      → CONFIRMED  (no action; proves completeness)
          EXTRACTED + both nodes exist + MISSING + named consumer → GAP        (→ 4dlab-doc-prep, re-run det. pass)
          INFERRED / AMBIGUOUS / new node / no consumer           → NOISE      (rejected; proposal-or-drop)
```

### Goal ###

Run graphify Pass 3 over `labs/obdlab/graph/v2_docs/ingest_ready/` with `--backend deepseek` in **default mode**
(NOT `--deep`), relocate the result to a **separate scratch dir** `graph/v2_docs_llm/`, diff it against the canonical
`graph/v2_docs/graph.json`, and write a classification report. Route any `GAP` back to `4dlab-doc-prep`. Promote
nothing into the canonical graph in this task.

### Success criteria ###

1. **Separate-dir guard.** Pass 3 output lands in `graph/v2_docs_llm/` (graph.json + GRAPH_REPORT.md + graph.html);
   canonical `graph/v2_docs/graph.json` is **byte-unchanged** (`git status --porcelain` + mtime). No surviving root
   `graphify-out/` (`test -d graphify-out` false).
2. **Default mode confirmed.** The run used `--backend deepseek` and **no** `--deep` flag (record the exact command
   in the progress note). Rationale: deep mode is defined to emit more `INFERRED` edges — the opposite of the intent.
3. **Diff report exists** — `graph/v2_docs/PASS3_CROSSCHECK.md` — listing every LLM edge classified as exactly one of
   `CONFIRMED` / `GAP` / `NOISE`, with counts. Each `GAP` row names: the edge (src→tgt, relation), its source-chunk
   anchor, and **the named COMLab/fault-atlas consumer** that justifies it (no consumer ⇒ it is `NOISE`, not `GAP`).
4. **No silent promotion.** Zero edges written into `graph/v2_docs/graph.json` by this task. `GAP`s are listed for
   routing to `4dlab-doc-prep`; `NOISE` with a nameable consumer is recorded as a **proposal** candidate
   (`comlab/config/proposals/`), everything else is dropped.
5. **Health sanity** on the LLM graph: nodes/links > 0, confidence split reported (`EXTRACTED` vs `INFERRED` vs
   `AMBIGUOUS`). A high `INFERRED` share is expected and is precisely what the gate filters out — report it, do not
   act on it.
6. **No collateral:** `graph/v1_baseline/`, `graph/v2_code/`, `graph/v2_tests/`, `graph/v2_wiki/`, and the canonical
   `graph/v2_docs/graph.json` all byte-unchanged; `research/chunks/` and `graphify-out/manifest.json` untouched.

### Deliverables ###

1. `labs/obdlab/graph/v2_docs_llm/` — the Pass-3 LLM scratch graph (graph.json + GRAPH_REPORT.md + graph.html).
2. `labs/obdlab/graph/v2_docs/PASS3_CROSSCHECK.md` — the CONFIRMED/GAP/NOISE diff report (the real deliverable).
3. *(already authored by this work, not re-edited here)* `4dlab-graphify-run/SKILL.md` Step 5 "Pass 3 noise control"
   is the procedure this task executes. If the runner finds the procedure ambiguous, the fix is a skill edit, not a
   graph patch.

### Files to touch ###

- `labs/obdlab/graph/v2_docs_llm/` (new scratch graph)
- `labs/obdlab/graph/v2_docs/PASS3_CROSSCHECK.md` (new report)
- `Vault/tasks/progress_notes/T-VAULT-DOCGRAPH-2.md` (gate + review blocks)

### Out of scope ###

- Writing any edge into `graph/v2_docs/graph.json` — forbidden; route `GAP`s to `4dlab-doc-prep`.
- Editing source/docs/chunks — that is `4dlab-doc-prep`.
- `--deep` mode — explicitly excluded (it manufactures the noise this task suppresses).
- Re-running `v2_wiki|v2_code|v2_tests` extraction — canonical, do not rebuild (CLAUDE.md HARD RULE).
- Acting on any `proposal` candidate — recording it is in scope; specing/implementing it is a separate task.

### Verification (graph-tooling lane) ###

```bash
cd <repo>/labs/obdlab
# 1) LLM graph in its own dir; canonical docs graph untouched
test -f graph/v2_docs_llm/graph.json && echo "OK llm graph present" || echo "FAIL no llm graph"
git status --porcelain graph/v2_docs/graph.json | grep . \
  && echo "FAIL canonical v2_docs changed" || echo "OK canonical intact"
test -d graphify-out && echo "FAIL root graphify-out remains" || echo "OK relocated"
# 2) confidence split on the LLM graph
python3.14 - <<'PY'
import json,collections
g=json.load(open('graph/v2_docs_llm/graph.json'))
n,l=g.get('nodes',[]),g.get('links',[])
conf=collections.Counter((e.get('confidence') or e.get('confidence_tag') or '?') for e in l)
print('llm nodes',len(n),'links',len(l))
for k,c in conf.most_common(): print(f'  {c:4d} {k}')
PY
# 3) diff report exists and classifies every edge
test -f graph/v2_docs/PASS3_CROSSCHECK.md \
  && grep -qiE 'CONFIRMED|GAP|NOISE' graph/v2_docs/PASS3_CROSSCHECK.md \
  && echo "OK crosscheck report present" || echo "FAIL no/empty report"
# 4) no collateral on the other graph pieces
git status --porcelain graph/v1_baseline graph/v2_code graph/v2_tests graph/v2_wiki \
  research/chunks graphify-out/manifest.json | grep . \
  && echo "FAIL collateral changed" || echo "OK no collateral"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-DOCGRAPH-2.md` opens with the confirmed `## Plan`; the run session fills
`VERIFICATION GATE` (the four checks + LLM-graph confidence split + CONFIRMED/GAP/NOISE counts) + `CODE REVIEW`
(the PASS3_CROSSCHECK.md diff; confirmation that zero edges entered the canonical graph). The row flips to `done`
only when both blocks are clean, the LLM graph is built into `v2_docs_llm/` (deepseek, default mode), the report
classifies every edge, every `GAP` names a consumer + chunk anchor (or is demoted to `NOISE`), and the canonical
`graph/v2_docs/graph.json` plus all sibling graphs are byte-unchanged. **Anti-orphan note:** a `GAP` is only "real"
if its consumer is read in a live code path — otherwise it is `NOISE`, regardless of being EXTRACTED.
