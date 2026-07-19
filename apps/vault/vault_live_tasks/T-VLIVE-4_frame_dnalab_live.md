# T-VLIVE-4 — Frame dnalab on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to dnalab's live notes — design docs in `labs/dnalab/docs/`
+ wiki notes in `labs/dnalab/wiki/` — exactly the `frame:` entries in
`vault-map.dnalab.yaml`, so dnalab appears in all three `.base` views on live.

## Context
Root `_bases/` + `Vault/` exclusion already in place (T-VLIVE-1). **Wiki source =
`labs/dnalab/wiki/`.** Live package dir = `labs/dnalab/dnalab/`. Apply the
mirror→live remap from `VAULT_LIVE_START_HERE.md`. `source:` = each note's live path.

## Consumer (signal/noise)
`consumers` from `vault-map.dnalab.yaml`, never empty. **`grep`-confirm every named
consumer file+symbol resolves; `test -f` every `implements`/`drift_guards` path —
before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Every dnalab note in the map's `frame:` set carries one valid `§4` block, paths remapped to live, `consumers` non-empty.
2. Idempotent: verify, never duplicate.

## Files to touch
- edit (frontmatter only): the `labs/dnalab/docs/*.md` and `labs/dnalab/wiki/**` notes named in `vault-map.dnalab.yaml`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-4.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Any other lab; `.base` query bodies; lab Python; note/chunk **bodies**; any graph; `Vault/`.

## Verification
1. Each framed dnalab note: one valid `§4` block, no empty `consumers`, paths exist, consumers resolve. No duplicates.
2. Obsidian-on-root: `consumers.base` shows dnalab `ok (n≥1)`, zero `MISSING`; `modules.base` groups dnalab; `drift-guards.base` shows `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/dnalab/tests` green.
4. `git status --porcelain -- labs/dnalab/graph/` clean.

## Success criteria
dnalab renders in all three views on live with zero `MISSING` consumers; dnalab tests green; no graph changed.
