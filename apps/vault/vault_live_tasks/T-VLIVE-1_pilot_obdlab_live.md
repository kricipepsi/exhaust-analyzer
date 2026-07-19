# T-VLIVE-1 — Pilot: frame obdlab on the live tree + stand up root `_bases/`

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring (no lab inner-loop edit) · **Mode:** STRICT
**Blocked by:** — (runnable now)
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md` (the `§4` schema) + `bases-and-views.md` (what each view queries).

## Goal
Prove the live-tree approach end-to-end on **one** lab. Place the three `.base`
views at a root location Obsidian-on-root indexes, hide the soon-to-be-archived
`Vault/` mirror so the views reflect **live only**, and frame obdlab's live notes
(design docs + wiki tier) with `§4` frontmatter so all three views render obdlab
rows. When this task is `done`, the pattern is proven and T-VLIVE-2…6 fan it out.

## Context
The `.base` files are **frontmatter-keyed and folder-generic** (`modules.base`
filters `file.inFolder("labs")` + `hasProperty("module")`; `consumers.base`
filters `hasProperty("node_type")`; `drift-guards.base` filters non-empty
`implements`). They need **no path edits** — they only need (a) to live where
Obsidian-on-root indexes them, and (b) live `labs/` notes that carry the
frontmatter. The current copies in `_skills/graph/4dlab-vault/assets/` are inside
an **excluded** folder (`_skills/` is in `userIgnoreFilters`), so copy them out to
a root `_bases/`.

obdlab is the right pilot: its wiki tier (7 `research/chunks/*/README.md`) was
already framed on the live tree by `T-VAULT-WIKIFRAME-1` (done) — so this task
**verifies** those 7 (does not re-add) and **adds** frontmatter to the 7 live
design docs in `labs/obdlab/docs/` per `vault-map.obdlab.yaml`.

Two pre-existing facts confirmed at authoring: live package dir is
`labs/obdlab/obdlab/`; obdlab's wiki source is `labs/obdlab/research/chunks/`
(NOT `labs/obdlab/wiki/`). Live design docs are currently **bare** (no frontmatter).

## Consumer (signal/noise)
Every framed note's `consumers` come from `vault-map.obdlab.yaml` (architect-
authored). The named consumers feed the `.base` views: `consumers` → `consumers.base`
audit; `implements`/`drift_guards` → `drift-guards.base` coverage; `module`/`lab`
→ `modules.base`. **Confirm each consumer file+symbol resolves to a live read and
each `implements`/`drift_guards` path exists before writing.** Unresolvable → STOP,
route to architect.

## Deliverables
1. **Root `_bases/`** containing `modules.base`, `consumers.base`,
   `drift-guards.base` copied verbatim from `_skills/graph/4dlab-vault/assets/`.
   (Do not modify their query bodies.)
2. **`Vault/` excluded from the Obsidian view** — add `"Vault/"` to
   `userIgnoreFilters` in `.obsidian/app.json` so the views count live notes only
   (the mirror is double-counted otherwise; it is archived in T-VLIVE-7's
   architect follow-up). Reversible.
3. **obdlab design docs framed** — add the `§4` block (below) to the 7 live docs
   in `labs/obdlab/docs/` that `vault-map.obdlab.yaml` lists under `frame:`
   (PRD/HLD/LLD/DLD + the others present in the map), with all map paths remapped
   to live (`labs/obdlab/code/X` → `labs/obdlab/obdlab/X`; `tests/`,`docs/`
   unchanged). `source:` = the doc's own live path.
4. **obdlab wiki tier verified (not re-added)** — confirm the 7
   `research/chunks/*/README.md` already carry valid `§4` frontmatter from
   `T-VAULT-WIKIFRAME-1`; if any is missing/invalid, repair it from the map.

### `§4` frontmatter block (per the schema; values from `vault-map.obdlab.yaml`)
```yaml
---
node_type: <prd|hld|lld|dld|wiki>   # from the map's frame entry
lab: obdlab
module: <module from the map>
subsystem: <subsystem from the map>
implements:        # map paths REMAPPED to live; [] if the map lists none
  - "labs/obdlab/obdlab/<...>"
consumers:         # from the map; never empty; each must resolve to a live read
  - "<named COMLab consumer · behaviour>"
drift_guards:      # map test paths (already live form); [] if none
  - "labs/obdlab/tests/<...>"
tags: [obdlab, finished, <node_type>]
source: "labs/obdlab/docs/<thisdoc>.md"
---
```

## Files to touch
- create: `_bases/modules.base`, `_bases/consumers.base`, `_bases/drift-guards.base`
- edit: `.obsidian/app.json` (append `"Vault/"` to `userIgnoreFilters`)
- edit: the 7 `labs/obdlab/docs/*.md` named in the map's `frame:` (frontmatter only)
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-1.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md` (flip row, promote T-VLIVE-2…6 → pending)

## Out of scope
- Any other lab (T-VLIVE-2…6).
- Editing `.base` query bodies, lab Python, wiki/chunk/doc **bodies**, or any graph.
- Copying notes into `Vault/` or running `build_lab_vault.py` (mirror is retired).
- Archiving `Vault/` (architect follow-up, T-VLIVE-7).
- Re-framing obdlab's research/chunks READMEs (already done; verify only).

## Verification
1. `_bases/` holds the 3 `.base` files, byte-identical to the assets copies.
2. `.obsidian/app.json` `userIgnoreFilters` now includes `"Vault/"` and parses as
   valid JSON.
3. Each framed obdlab doc carries one valid `§4` block; **no empty `consumers`**;
   every `implements`/`drift_guards` path exists (`test -f`); every named consumer
   file+symbol resolves (`grep`). No duplicate frontmatter on the 7 wiki READMEs.
4. In Obsidian opened on `/agent_workspace`: `modules.base` shows obdlab grouped
   by subsystem; `consumers.base` shows the obdlab notes as `ok (n≥1)` (zero
   `MISSING`); `drift-guards.base` shows the design docs' `implements`→guards.
   (If Obsidian desktop is unavailable in-session, assert mechanically: every
   framed note matches the view filters and has the required non-empty fields;
   note the desktop render-check as an owner step.)
5. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/obdlab/tests` is
   green (frontmatter added to a note a test parses must not break it).
6. `git status --porcelain -- labs/obdlab/graph/` is clean.

## Success criteria
The three `.base` views render obdlab rows against the **live** tree with zero
`MISSING` consumers, obdlab tests are green, no graph changed, and the root
`_bases/` + `Vault/` exclusion make the live view authoritative. T-VLIVE-2…6 are
promoted to `pending`.
