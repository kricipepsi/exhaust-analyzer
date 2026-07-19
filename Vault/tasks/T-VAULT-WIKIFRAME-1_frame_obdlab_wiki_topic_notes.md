---
node_type: task
task_id: T-VAULT-WIKIFRAME-1
status: done
pack: VAULT
lab: obdlab
mode: strict
blocked_by:
- T-VAULT-BUILD-1
consumers:
- COMLab analytics / fault-atlas routing
tags:
- task
- vault
- obdlab
---

# T-VAULT-WIKIFRAME-1 — Frame the OBDLab wiki tier (7 topic READMEs, consumer-named)

**Status:** `done` · **Pack:** VAULT (OBDLab tier) · **Mode:** STRICT (vault-tooling / architect-authoring lane — no lab inner-loop/gate)
**Origin:** transparency gap surfaced 2026-06-11 (owner) — OBDLab frames only 5 notes (4 design docs + landing) vs DTCLab/GASLab 16 each; its entire wiki tier (63 `.md` across 7 topic folders) shipped into the vault with **no frontmatter**, so it is invisible to `consumers.base`, `drift-guards.base`, and `modules.base`. Authored 2026-06-11 (architect).
**Blocked by:** — (`T-VAULT-BUILD-1` is `done`; all four tier sources + graphs present on disk).
**Granularity (owner decision 2026-06-11):** **topic-level** — frame the **7 topic READMEs**, one named consumer each. Not per-chunk (all 63), not READMEs+curated picks. This matches DTCLab/GASLab's ~11 wiki-topic-note granularity and keeps every framed note consumer-honest.

## Consumer (signal/noise) — the gate this task exists to satisfy

Each of the 7 framed READMEs must name **≥1 existing COMLab consumer with a code path**. No "future use". The builder's own gate already refuses any framed note with an empty `consumers` list; this task makes that gate *pass with real entries* for the wiki tier. The proposed mapping below is pinned from `grep` over `labs/comlab/` (every cited file already references the topic's signals); the framing session **confirms each path + symbol resolves to a live read** before writing (anti-orphan check).

| # | Topic README (canonical source) | `subsystem` | **Named COMLab consumer (code path · behaviour)** |
|---|---|---|---|
| 1 | `research/chunks/o2-logic/README.md` | `o2-lambda-perception` | `comlab: labs/comlab/comlab/core/perception_contradiction.py` — O2/lambda bias-vs-truth comparison; **+** `comlab/analytics/power_loss_analytics.py` — mixture scoring |
| 2 | `research/chunks/fuel-trim/README.md` | `fuel-trim-reasoning` | `comlab: labs/comlab/comlab/core/perception_contradiction.py` — Total Fuel Trim evaluation; **+** `comlab/core/lab_pipeline_aggregator.py` — OBD payload intake |
| 3 | `research/chunks/delta-relations/README.md` | `delta-vector-scoring` | `comlab: labs/comlab/comlab/analytics/power_loss_analytics.py` — lambda-delta-vector scoring; **+** `comlab/core/perception_contradiction.py` |
| 4 | `research/chunks/ecu-diagnosis/README.md` | `ecu-hardware` | `comlab: labs/comlab/comlab/core/ecu_hardware_checker.py` — ECU driver/rail fault checks (dedicated consumer) |
| 5 | `research/chunks/pids-protocol/README.md` | `pid-mode06-readiness` | `comlab: labs/comlab/comlab/core/fault_atlas_kg.py` — PID/Mode06/readiness fault-atlas keys; **+** `comlab/core/lab_pipeline_aggregator.py` |
| 6 | `research/chunks/taxonomy/README.md` | `emission-era-taxonomy` | `comlab: labs/comlab/comlab/core/symptom_router.py` — era/emission symptom-prior routing; **+** `comlab/core/fault_atlas_kg.py` |
| 7 | `research/chunks/truth-perception/README.md` | `truth-vs-perception` | `comlab: labs/comlab/comlab/core/perception_contradiction.py` — truth-vs-perception override core; **+** `comlab/core/symptom_router.py` — symptom prior (stays a prior, not an override) |

If any path fails to resolve at framing time, **do not invent a substitute** — STOP and route the note back to the architect; an unframmable topic is a signal/noise finding, not a fill-in.

## Goal

Add `§4` frontmatter (the vault's framed-note schema) to the **7 canonical topic READMEs** under `labs/obdlab/research/chunks/<topic>/README.md`, then rebuild the OBDLab vault so the 7 notes appear framed in `Vault/labs/obdlab/wiki/<topic>/README.md`. Outcome: OBDLab wiki tier becomes visible to all three `.base` audit views, raising OBDLab from 5 framed notes to **12** (4 docs + 7 wiki + landing) — parity with DTC/GAS coverage.

## Frontmatter schema (match DTCLab wiki notes exactly)

Author this block at the top of each of the 7 canonical READMEs (values per the table above):

```yaml
---
node_type: "wiki"
lab: "obdlab"
module: "obdlab"
subsystem: "<from table>"
implements:
  - "<obdlab code path this topic documents — confirm exists>"
consumers:
  - "<named COMLab consumer from the table · behaviour>"
drift_guards:
  - "<guarding obdlab test — confirm exists>"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/<topic>/README.md"
---
```

`implements` and `drift_guards` are secondary (DTC wiki notes carry one of each); pin the best obdlab code/test target per topic and **confirm the path resolves** — leave the list to a single confirmed entry rather than padding. `consumers` is the gate and is fully pinned above.

## Success criteria

1. **7 canonical READMEs carry valid `§4` frontmatter** — `node_type: wiki`, `lab/module: obdlab`, the `subsystem` from the table, ≥1 `consumers` entry resolving to a live COMLab read, and a `source:` self-reference. No empty `consumers`.
2. **Rebuild propagates the frontmatter** — `build_lab_vault.py --lab obdlab` (apply) copies the 7 framed READMEs into `Vault/labs/obdlab/wiki/<topic>/README.md` with frontmatter intact. Confirm whether the builder copies source frontmatter through (DTC/GAS evidence says yes) or needs a manifest entry; if a manifest is required, that one-line wiki-tier registration is in scope, nothing else.
3. **`consumers.base` shows 7 new OBDLab wiki rows**, each `ok (n≥1)` — none `MISSING`.
4. **`drift-guards.base` and `modules.base` pick up the 7 notes** under `lab: obdlab`, grouped by `subsystem`.
5. **PROVENANCE refreshed** — `_meta/PROVENANCE.md` OBDLab `framed notes` count rises from 4 to **11** (7 wiki + 4 docs; landing note excluded as before).
6. **No re-extraction, no graph touch** — `graph/v2_wiki/` and `research/chunks/**` chunk bodies unchanged (only the 7 README frontmatter blocks added). Verify via `git status --porcelain -- labs/obdlab/graph/`.
7. **Anti-orphan** — for each of the 7, `grep` the named consumer file and confirm the OBD signal it claims to feed is actually read there.

## Out of scope (→ Unplanned follow-ups, not this diff)

- Framing the 56 individual chunk notes under each topic (owner chose topic-level; per-chunk is a separate decision).
- Any edit to chunk bodies, the `v2_wiki` graph, or COMLab code.
- `System-Map.md` wiki-tier wording (already a known §8 follow-up from T-VAULT-BUILD-1).

## VERIFICATION GATE

_(filled by the framing/build session — pending)_

## CODE REVIEW

_(filled by the framing/build session — pending)_
