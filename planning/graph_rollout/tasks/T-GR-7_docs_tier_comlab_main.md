### Goal ###
Build the missing **offline docs tier** for **comlab_main** — `labs/comlab/graph/v2_docs/` — closing its row in
assessment gap G2. Offline structure extraction only (`graphify update`): free, no key, no LLM.
### Success criteria ###
1. **Prep check first (read-only):** confirm prepared docs exist (doc-prep progress note done and/or
   `labs/comlab/graph/v2_docs/ingest_ready/` populated). If prep is missing or the docs corpus is raw
   prose, STOP and report — do NOT improvise prep (that is `4dlab-doc-prep`, a separate task).
2. Build per `4dlab-graphify-run` (resolve → run → relocate → verify): scoped input path (never
   repo root), output relocated to `labs/comlab/graph/v2_docs/`.
3. Health: 0 dangling; isolated nodes low and explained; **EXTRACTED-dominant** (INFERRED = 0 —
   offline build); spot-check 3 doc symbols (e.g. an ADR decision, an LLD module, a vocabulary
   term) resolve to correct file+line via `graphify explain --graph labs/comlab/graph/v2_docs/graph.json`.
4. Bookkeeping: `Vault/_meta/PROVENANCE.md` is Vault-owned — do NOT edit; instead record the new
   tier in `GRAPH_AUDIT_2026-06-28.md` inventory (append a dated row) and the pack ledger.
### Out of scope ###
No LLM (`extract`)/wiki tier. No rebuild of existing tiers (v2_code/v2_tests/v2_current untouched).
Never `graphify-out/`, never repo root, never `Vault/` writes. One lab per session.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/graphify explain "<spot-symbol>" --graph labs/comlab/graph/v2_docs/graph.json | head
python3 - <<'PY'
import json; d=json.load(open("labs/comlab/graph/v2_docs/graph.json"))
ids={n["id"] for n in d["nodes"]}
print(len(d["nodes"]),"nodes",len(d["links"]),"links",
      sum(1 for l in d["links"] if l["source"] not in ids or l["target"] not in ids),"dangling")
PY
git status --porcelain | grep -vE '^\?\? (labs/comlab/graph/v2_docs/|planning/graph_rollout/)' | grep -E 'graph' && echo "FAIL: touched other graphs" || echo OK
```
### Progress hook ###
Ledger T-GR-7 → done; note in `../progress_notes/T-GR-7.md` with counts + spot-check transcript.
### Depends on ###
T-GR-2 done (build on 0.9.7). Doc-prep for comlab_main done (verify, step 1).
