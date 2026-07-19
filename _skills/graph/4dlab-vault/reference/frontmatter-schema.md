# Frontmatter Node Schema (authoritative)

This is the contract for every `.md` note the vault adds frontmatter to. It is
adapted from `ObsidianProp.md` and bound to the 4DLab signal/noise rule: **every
field is read by a named consumer.** If you want a new field, add a row to the
consumer table first. No row → the field does not ship.

## Schema

```yaml
---
node_type: wiki        # wiki | dld | hld | lld | prd | lab-index | design
lab: obdlab            # lab slug; matches labs/<lab>/
module: obd_live_lab   # module name as used in the lab + graph
subsystem: trim-analytics   # finer grouping within the module
implements:            # code paths this note specifies (vault-relative)
  - "labs/obdlab/code/core/ve_engine.py"
consumers:             # downstream NAMED consumers — human-authored, never empty
  - "comlab: fault_atlas fusion (perception channel)"
drift_guards:          # tests guarding the implemented code (vault-relative)
  - "labs/obdlab/tests/unit/test_ve_engine.py"
tags: [obdlab, perception, finished]
source: "labs/obdlab/docs/DLD_OBDLab.md"   # provenance: original path in the lab
---
```

## Per-field consumer table

| Field | Type | Named consumer (the code path / view that reads it) |
|---|---|---|
| `node_type` | enum | filter key in all three `.base` views |
| `lab` | string | `modules.base` top-level `groupBy`; lab landing note links |
| `module` | string | `modules.base` grouping; `/graph-find <module>` command |
| `subsystem` | string | `modules.base` row order; module-group readability |
| `implements` | list[path] | `/check-impact` (note→code map); `drift-guards.base` join |
| `consumers` | list[string] | `consumers.base` (signal/noise audit view); `/check-impact` |
| `drift_guards` | list[path] | `drift-guards.base` (coverage map) |
| `tags` | list | Obsidian tag pane; `.base` `file.hasTag()` filters |
| `source` | path | `_meta/PROVENANCE.md`; reconcile vault note vs live lab |

## Rules

- **`consumers` is never empty and never auto-derived.** If you cannot name a
  consumer (a COMLab analytics path or a fault-atlas route), the note is not
  ready for the vault. This is the signal/noise principle applied to the vault's
  own metadata.
- **`node_type` is a closed vocabulary, but the `.base` views filter on its
  *presence* (`hasProperty("node_type")`), not on a specific value** — so a new
  value is a display/grouping label, not a filter break. Current values:
  `dld/hld/lld/prd` (design docs), `wiki` (KG/operational wiki + vocabulary
  notes), `lab-index` (per-lab landing note), `design` (the `apps/ui` design
  corpus — has no code/tests/graph). Add a value only when a real note needs it,
  and list it here.
- **Paths are vault-relative** (`labs/<lab>/...`), so wikilinks and Bases
  filters resolve inside the vault regardless of where the vault is mounted.
- **Mechanical vs semantic fields.** The build script injects only `node_type`,
  `lab`, `module`, `source`, and a `tags` skeleton. `subsystem`, `implements`,
  `consumers`, `drift_guards` come from `assets/vault-map.<lab>.yaml`, which a
  human authors.

## Adding a new field (proposal path)

Per the v2 forward-progress rule, a genuinely useful new field is welcome — but
it ships **with its consumer**. Add the consumer-table row (naming the `.base`
view or command that will read it), add the `.base` change that reads it, and
note it in the vault plan's follow-ups. A field with no reader is an orphan, not
a feature.

## Task-note frontmatter (the FX ledger)

`Vault/tasks/T-*.md` are not lab notes — they are the FX task ledger. They carry
a **separate** frontmatter shape under `node_type: task`, so the ledger is
machine-queryable (which task is next, what blocks what) without parsing prose.
The inline `**Status:** / **Blocked by:**` lines stay as the human-readable
narrative; **frontmatter is the authoritative source for queries.**

```yaml
---
node_type: task                 # fixed value 'task' — partitions tasks from lab notes
task_id: T-GAS-VAULT            # canonical id (matches the H1 and ledger row)
status: pending                 # pending | done | void
queue: next                     # OPTIONAL — only on the "pending (next)" front-of-queue task
pack: VAULT                     # ledger pack (VAULT, etc.)
lab: gaslab                     # gaslab | dtclab | obdlab
mode: architect/author + vault-tooling lane
blocked_by:                     # task_ids that must be done/void first; [] = ready
  - T-GAS-GRAPH-AST
  - T-GAS-PATHS-1
consumers:                      # named readers of the task's output (never empty)
  - "build_lab_vault.py — vault frontmatter derivation"
  - "consumers.base — signal/noise audit view"
implements:                     # OPTIONAL — produced artefacts the task contracts
  - "vault-map.gaslab.yaml"
tags: [task, vault, gaslab]
---
```

### Per-field consumer table (task notes)

| Field | Type | Named consumer (what reads it) |
|---|---|---|
| `node_type: task` | enum value | `tasks.base` filter (`node_type == "task"`); `vault_query.py tasks/next` |
| `task_id` | string | `tasks.base` row id; `blocked_by` cross-reference resolution in `vault_query.py next` |
| `status` | enum | `tasks.base` `groupBy`; `vault_query.py next` (only `pending` is selectable) |
| `queue` | enum | `tasks.base` row order — front-of-queue hint |
| `pack` | string | `tasks.base` column / future per-pack grouping |
| `lab` | string | `tasks.base` filtering; ties a task to its lab notes |
| `mode` | string | human lane label shown in `tasks.base` |
| `blocked_by` | list[task_id] | `vault_query.py next` unblocked-task computation (all blockers `done`/`void`) |
| `consumers` | list[string] | `consumers.base` audit (tasks are **excluded** there by `!file.inFolder("tasks")`, but the rule still holds: never empty) |
| `implements` | list[path] | informational; tasks are **excluded** from `drift-guards.base` so produced artefacts are not mistaken for untested code |

**Why tasks are excluded from `consumers.base` / `drift-guards.base`.** Those two
views audit *lab* notes. Task notes carry `node_type` and sometimes `implements`,
so without `!file.inFolder("tasks")` they would leak in — a task's produced
artefact (`graph/v2_*/graph.json`) would show as "untested" in the coverage map.
The exclusion keeps each view's semantics intact; tasks live in `tasks.base`.
