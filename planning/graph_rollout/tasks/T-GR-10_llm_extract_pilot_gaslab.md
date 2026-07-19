### Goal ###
**LLM `extract` pilot — gaslab predicate layer, DISCLOSURE ONLY.** Build the LLM Pass-3 docs graph
into `labs/gaslab/graph/v2_docs_llm/` (a *separate* dir — NEVER over the canonical offline
`v2_docs/`) and produce the diff report that lets the owner decide the promotion path. Context: the
offline `graphify update` path on this host emits only structural `contains`; the architectural
predicates doc-prep wrote into the chunks (`SUPERSEDES` / `CONSUMES` / `VERIFIES` /
`MIRRORS_CONTRACT_IN`) are parsed only by the LLM `extract` pass (`llm.py`). Reference shape:
obdlab `v2_docs` (built where the pass ran) carries 93 VERIFIES / 76 CONSUMES / 16 SUPERSEDES /
9 MIRRORS_CONTRACT_IN alongside MENTIONS.
### Runner / backend ###
**Nemo lane.** Backend named explicitly, resolved in this order:
1. `--backend deepseek` if `DEEPSEEK_API_KEY` is set (workspace default; cheap, parallel).
2. `--backend claude-cli` otherwise — ONLY after verifying the CLI is authenticated
   (`claude` reports `loggedIn: true`; unauthenticated CLI fails the whole pass — the 2026-06-10
   DOCGRAPH-1 incident). Concurrency is forced to 1 → slow; acceptable for one lab.
Never let graphify auto-detect (a stale key silently shadows the intended backend). Record which
backend ran in the report. Keys come from the environment only — **never written to any file, note,
or report**. Default extraction mode — **never `--deep`** (deep mode manufactures INFERRED noise).
### Success criteria ###
1. **Run per `4dlab-graphify-run`** (resolve → run → relocate → verify): copy
   `labs/gaslab/graph/v2_docs/ingest_ready/` to `/tmp/gaslab_docs_llm/`, run
   `graphify extract /tmp/gaslab_docs_llm --directed --backend deepseek` (never repo root),
   relocate `graphify-out/{graph.json,GRAPH_REPORT.md,graph.html}` →
   `labs/gaslab/graph/v2_docs_llm/`; no root `graphify-out/` survives.
2. **Health:** 0 dangling; isolated low and explained; confidence split reported with
   **EXTRACTED dominant** (INFERRED/AMBIGUOUS counted, not hidden).
3. **Predicate layer present:** >0 edges for each of `SUPERSEDES`, `CONSUMES`, `VERIFIES` (accept
   lowercase); `MIRRORS_CONTRACT_IN` reported (may legitimately be 0 for gaslab — say so, don't pad).
   3 predicate spot-checks resolve to correct source chunk file+line via `graphify explain
   --graph labs/gaslab/graph/v2_docs_llm/graph.json`.
4. **Diff report vs canonical offline `v2_docs/`** per skill §5 (checker, not adder): classify LLM
   edges CONFIRMED / GAP (EXTRACTED + both nodes exist in v2_docs + named consumer) / NOISE
   (INFERRED/AMBIGUOUS/consumer-less). Write `REPORT_T-GR-10_llm_extract_pilot.md` in the pack dir
   with counts, spot-check transcript, token/cost figure, and a promotion recommendation.
5. **No collateral:** `labs/gaslab/graph/v2_docs/` and every other graph byte-identical
   (`git status --porcelain` + checksum recorded pre-run).
### Out of scope — the disclosure gate ###
**No promotion.** Do not touch canonical `v2_docs/`, do not patch `graph.json`, do not flip any
"predicate layer deferred" ledger wording, do not roll out to other labs (that is T-GR-11, owner-gated
on this report). Never `Vault/` writes, never repo root, no key in files. Owner decides after reading
the report: **(A)** adopt `v2_docs_llm/` as the queryable predicate tier per lab (symptomlab
precedent), **(B)** keep it supplementary/scratch, or **(C)** drop the predicate layer.
### Verification ###
```bash
cd /agent_workspace
python3 - <<'PY'
import json, collections
d=json.load(open("labs/gaslab/graph/v2_docs_llm/graph.json"))
ids={n["id"] for n in d["nodes"]}
rels=collections.Counter(l.get("relation","?") for l in d["links"])
conf=collections.Counter(l.get("confidence","?") for l in d["links"])
print(len(d["nodes"]),"nodes",len(d["links"]),"links",
      sum(1 for l in d["links"] if l["source"] not in ids or l["target"] not in ids),"dangling")
print("conf:",dict(conf))
for k in ("SUPERSEDES","CONSUMES","VERIFIES","MIRRORS_CONTRACT_IN"):
    print(f"  {k}: {rels.get(k,0)+rels.get(k.lower(),0)}")
PY
git status --porcelain labs/gaslab/graph/v2_docs | grep . && echo "FAIL: canonical v2_docs touched" || echo OK
test -d graphify-out && echo "FAIL: root graphify-out remains" || echo OK
```
### Progress hook ###
Ledger T-GR-10 → done; dual-gate note `../progress_notes/T-GR-10.md`; report
`REPORT_T-GR-10_llm_extract_pilot.md`. Promotion decision stays OPEN for the owner.
### Depends on ###
T-GR-3 done (canonical gaslab v2_docs is the diff baseline) · a working backend (DEEPSEEK_API_KEY in env, OR authenticated claude-cli) ·
owner go for token spend (this task file is the authorization to *run*, not to *promote*).
