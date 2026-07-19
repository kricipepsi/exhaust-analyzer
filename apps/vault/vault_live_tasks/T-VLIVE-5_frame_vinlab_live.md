# T-VLIVE-5 — Frame vinlab on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to vinlab's live notes — design docs in `labs/vinlab/docs/`
+ wiki notes in `labs/vinlab/wiki/` — exactly the `frame:` entries in
`vault-map.vinlab.yaml`, so vinlab appears in all three `.base` views on live.

## Context
Root `_bases/` + `Vault/` exclusion already in place (T-VLIVE-1). **Wiki source =
`labs/vinlab/wiki/`.** Live package dir = `labs/vinlab/vinlab/`. Apply the
mirror→live remap from `VAULT_LIVE_START_HERE.md`. `source:` = each note's live path.

## Consumer (signal/noise)
`consumers` from `vault-map.vinlab.yaml`, never empty. **`grep`-confirm every named
consumer file+symbol resolves; `test -f` every `implements`/`drift_guards` path —
before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Every vinlab note in the map's `frame:` set carries one valid `§4` block, paths remapped to live, `consumers` non-empty.
2. Idempotent: verify, never duplicate.

## Files to touch
- edit (frontmatter only): the `labs/vinlab/docs/*.md` and `labs/vinlab/wiki/**` notes named in `vault-map.vinlab.yaml`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-5.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Any other lab; `.base` query bodies; lab Python; note/chunk **bodies**; any graph; `Vault/`.

## Verification
1. Each framed vinlab note: one valid `§4` block, no empty `consumers`, paths exist, consumers resolve. No duplicates.
2. Obsidian-on-root: `consumers.base` shows vinlab `ok (n≥1)`, zero `MISSING`; `modules.base` groups vinlab; `drift-guards.base` shows `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/vinlab/tests` green.
4. `git status --porcelain -- labs/vinlab/graph/` clean.

## Success criteria
vinlab renders in all three views on live with zero `MISSING` consumers; vinlab tests green; no graph changed.
