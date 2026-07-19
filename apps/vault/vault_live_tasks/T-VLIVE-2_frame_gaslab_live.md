# T-VLIVE-2 — Frame gaslab on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1 (pilot proves the bases render on live)
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to gaslab's live notes — the design docs in
`labs/gaslab/docs/` + the wiki notes in `labs/gaslab/wiki/` — exactly the entries
`vault-map.gaslab.yaml` lists under `frame:`, so gaslab appears in all three
`.base` views on the live tree.

## Context
The root `_bases/` and the `Vault/` exclusion are already in place (T-VLIVE-1).
This task only adds frontmatter to gaslab live notes. **Wiki source = `labs/gaslab/wiki/`.**
Live package dir = `labs/gaslab/gaslab/`. Apply the mirror→live remap from
`VAULT_LIVE_START_HERE.md` (`labs/gaslab/code/X` → `labs/gaslab/gaslab/X`;
`tests/`,`docs/` unchanged). `source:` = each note's own live path. Use the exact
`§4` block shape from the schema; values come from the map.

## Consumer (signal/noise)
`consumers` come from `vault-map.gaslab.yaml`, never empty. **Before writing each
note: `grep`-confirm every named consumer file+symbol resolves to a live read, and
`test -f` every `implements`/`drift_guards` path.** Unresolvable → STOP, route to
architect (do not invent substitutes).

## Deliverables
1. Every gaslab note in the map's `frame:` set carries one valid `§4` block,
   paths remapped to live, `consumers` non-empty.
2. Idempotent: if a note already has valid frontmatter, verify — never duplicate.

## Files to touch
- edit (frontmatter only): the `labs/gaslab/docs/*.md` and `labs/gaslab/wiki/**` notes named in `vault-map.gaslab.yaml`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-2.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Any other lab; `.base` query bodies; lab Python; note/chunk **bodies**; any graph; `Vault/`.

## Verification
1. Each framed gaslab note: one valid `§4` block, no empty `consumers`, every path exists, every consumer resolves (`grep`). No duplicate blocks.
2. Obsidian-on-root: `consumers.base` shows the gaslab notes `ok (n≥1)`, zero `MISSING`; `modules.base` groups gaslab by subsystem; `drift-guards.base` shows their `implements`→guards. (No desktop in-session → assert filter-match + non-empty fields mechanically; flag the render-check as an owner step.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/gaslab/tests` green.
4. `git status --porcelain -- labs/gaslab/graph/` clean.

## Success criteria
gaslab renders in all three views on the live tree with zero `MISSING` consumers; gaslab tests green; no graph changed.
