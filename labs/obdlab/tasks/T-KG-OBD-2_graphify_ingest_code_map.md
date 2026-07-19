# T-KG-OBD-2 — Graphify ingest of OBDLab source → separate code-map KG

**Status:** `blocked` — **awaiting the source-legibility prep** (`T-KG-OBD-2-PREP`) · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Lane:** dedicated **KG-lane** task (the permitted graphify exception, `OBDLAB_TASKS_START_HERE.md` §0 —
deliverable names `graph.json`).
**Blocked by:** `T-KG-OBD-2-PREP` (the final `4dlab-code-prep` legibility pass over `obdlab/obdlab`).
The audit-backlog source-mutating tasks (`T-OBDV2-FIX-1..7`, `T-OBDV2-ARCH-1`, `T-OBDV2-ARCH-2`) are now
all `done`, so the logic of the source is frozen — but the **last** source touch is the code-prep pass,
and the map must ingest that prepped source, not the pre-prep version. ⚠ Also re-check `T-OBDV2-9/-10` if
later authored and they land new code, and re-confirm no source change lands after `T-KG-OBD-2-PREP`.
**Consumer (signal/noise):** the produced `graph.json` is a **code-map artefact, not a schema field** —
the field-level rule does not bite. Named consumer = the **architect/coder repo-navigation workflow**
(`/graphify query "what calls translate()"`, "where is `o2_normalizer` consumed", import/call tracing).
This is **separate from** the diagnostic wiki KG (`T-KG-OBD-1` → `graph/v2_wiki/`) and must not be merged
into it.

> **Why this is its own task (and its own graph).** The old per-lab graphs mixed code AST + docs because
> the runs pointed at the whole lab dir. We are deliberately splitting: **diagnostic KG = wiki only**
> (`T-KG-OBD-1`); **code map = source only** (this task). The wiki already captures the one cross-link
> that matters — *which signal is consumed by which code* — via each chunk's `consumer:` line, so the
> code map is a navigation aid, not a diagnostic input.

## Scope decision

- **Source-only build.** INPUT = `obdlab/obdlab/` (the 17-module Python package: `core/`, `schemas/`).
  **Exclude** `tests/` (test scaffolding is not the architecture) and `research/` (that is the wiki KG's
  input, already built separately).
- **Output to a NEW location:** `graph/v2_code/` (recommended name — coder/owner may rename). Holds
  `graph.json`, `GRAPH_REPORT.md`, `graph.html`.
- **Do NOT touch** `graph/v1_baseline/`, `graph/v2_current/` (old whole-lab), or `graph/v2_wiki/`
  (diagnostic KG from `T-KG-OBD-1`).

## Procedure (the standard graphify pipeline)

```
cd <repo>/labs/obdlab
/graphify obdlab/obdlab
```

- A pure-code corpus → graphify runs **AST extraction only** (Part A); semantic subagents (Part B) are
  skipped automatically (the skill's fast-path). Output is the module/class/function node set with
  import/call edges.
- Default **undirected** to match the existing lab graphs; `--directed` is available if a true call-
  direction graph is wanted — record which was used in the progress note.
- After `./graphify-out/` is written, **relocate** it:
  ```bash
  mkdir -p graph/v2_code
  mv graphify-out/graph.json    graph/v2_code/graph.json
  mv graphify-out/GRAPH_REPORT.md graph/v2_code/GRAPH_REPORT.md
  mv graphify-out/graph.html    graph/v2_code/graph.html
  ```

## Hard guards (the recurring failure mode)

- **NEVER run `graphify update .` from the repo root** (the prior 81.9k-node incident). Scope strictly to
  `obdlab/obdlab`, output to `graph/v2_code/` only.
- **No collateral on the other graphs.** `v1_baseline/`, `v2_current/`, `v2_wiki/` unchanged.
- **No surviving root-level `graphify-out/`** after the task.
- **Confirm the code-freeze gate first:** `T-OBDV2-8`, the audit-backlog source fixes
  (`T-OBDV2-FIX-1..7`, `T-OBDV2-ARCH-1/-2`), **and `T-KG-OBD-2-PREP`** must all be `done` in
  `PROGRESS.md` before running, and **no source edit may land after `T-KG-OBD-2-PREP`**. If any is
  still open, STOP — the map would be built against stale or un-prepped source.

## Success criteria

- `graph/v2_code/graph.json` exists, non-empty (`nodes > 0`, `edges > 0`); not the "empty graph" error.
- AST nodes cover the package — spot-check that key modules/symbols are present:
  `o2_normalizer`, `sensor_signal_translator` (`translate`), `payload` (`OBDLivePayload`),
  `vocabulary` (`O2FailureMode`, `TrimAnalyticsGate`, `DownstreamTrimRole`, `FuelSystemStatus`).
- `GRAPH_REPORT.md` generated with labelled communities.
- No collateral: other `graph/*` dirs unchanged; no root `graphify-out/`.

## Deliverables

1. `graph/v2_code/graph.json` — OBDLab source code map.
2. `graph/v2_code/GRAPH_REPORT.md`, `graph/v2_code/graph.html`.
3. `tasks/progress_notes/T-KG-OBD-2.md` — `## Plan` → `VERIFICATION GATE` → `CODE REVIEW` (node/edge
   counts, key-symbol spot-check, `--directed` y/n, other graphs untouched).

## Files to touch

- `graph/v2_code/` (new dir — outputs only)
- `tasks/progress_notes/T-KG-OBD-2.md` (new)
- `tasks/PROGRESS.md` (flip this row to `done`)

## Out of scope

No source edits. No merge with the wiki KG (`v2_wiki/`). No overwrite of any existing `graph/*`. No live
consumer wired to `v2_code/graph.json` in this task. Do not run while `T-OBDV2-8` is open.

## Verification

```bash
cd <repo>/labs/obdlab
# gate: code is frozen — T-OBDV2-8 AND all open audit-backlog source fixes must be done
grep -E "T-OBDV2-8\b" tasks/PROGRESS.md | grep -qi "done" || { echo "FAIL: T-OBDV2-8 not done — code not frozen"; exit 1; }
for t in T-OBDV2-FIX-1 T-OBDV2-FIX-2 T-OBDV2-FIX-3 T-OBDV2-FIX-4 T-OBDV2-FIX-5 T-OBDV2-FIX-6 T-OBDV2-FIX-7 T-OBDV2-ARCH-1 T-OBDV2-ARCH-2 T-KG-OBD-2-PREP; do
  grep -E "\b$t\b" tasks/PROGRESS.md | grep -qi "done" || { echo "FAIL: $t not done — source still in flux / not prepped"; exit 1; }
done
# non-empty code map
python3 -c "import json; d=json.load(open('graph/v2_code/graph.json')); \
  assert len(d['nodes'])>0 and len(d.get('links',d.get('edges',[])))>0; \
  print('nodes',len(d['nodes']),'links',len(d.get('links',d.get('edges',[]))))"
# key symbols present
python3 - <<'PY'
import json
labels=' '.join((n.get('label') or n.get('id') or '') for n in json.load(open('graph/v2_code/graph.json'))['nodes'])
for s in ['o2_normalizer','translate','OBDLivePayload','O2FailureMode','TrimAnalyticsGate']:
    print(s, s in labels)
PY
# no collateral
git status --porcelain graph/v1_baseline graph/v2_current graph/v2_wiki | grep . && echo "FAIL: other graphs changed" || echo "OK"
test -d ../../graphify-out && echo "FAIL: root graphify-out exists" || echo "OK no root graphify-out"
```

## Progress hook

`tasks/progress_notes/T-KG-OBD-2.md`: `## Plan` (input `obdlab/obdlab`, output `graph/v2_code`, directed
y/n, gate `T-OBDV2-8=done`), then `VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md row → `done` with
node/edge counts and "OBDLab source code map; AST-only; other graphs untouched."
