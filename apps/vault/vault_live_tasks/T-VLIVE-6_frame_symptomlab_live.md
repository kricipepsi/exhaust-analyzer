# T-VLIVE-6 — Frame symptomlab on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to symptomlab's live notes — design docs in
`labs/symptomlab/docs/` + wiki notes in `labs/symptomlab/wiki/` — exactly the
`frame:` entries in `vault-map.symptomlab.yaml`, so symptomlab appears in all
three `.base` views on live.

## Context
Root `_bases/` + `Vault/` exclusion already in place (T-VLIVE-1). **Wiki source =
`labs/symptomlab/wiki/`.** Live package dir = `labs/symptomlab/symptomlab/`. Apply
the mirror→live remap from `VAULT_LIVE_START_HERE.md`. `source:` = each note's live path.

## Consumer (signal/noise)
`consumers` from `vault-map.symptomlab.yaml`, never empty. **`grep`-confirm every
named consumer file+symbol resolves; `test -f` every `implements`/`drift_guards`
path — before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Every symptomlab note in the map's `frame:` set carries one valid `§4` block, paths remapped to live, `consumers` non-empty.
2. Idempotent: verify, never duplicate.

## Files to touch
- edit (frontmatter only): the `labs/symptomlab/docs/*.md` and `labs/symptomlab/wiki/**` notes named in `vault-map.symptomlab.yaml`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-6.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Any other lab; `.base` query bodies; lab Python; note/chunk **bodies**; any graph; `Vault/`.

## Verification
1. Each framed symptomlab note: one valid `§4` block, no empty `consumers`, paths exist, consumers resolve. No duplicates.
2. Obsidian-on-root: `consumers.base` shows symptomlab `ok (n≥1)`, zero `MISSING`; `modules.base` groups symptomlab; `drift-guards.base` shows `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/symptomlab/tests` green.
4. `git status --porcelain -- labs/symptomlab/graph/` clean.

## Success criteria
symptomlab renders in all three views on live with zero `MISSING` consumers; symptomlab tests green; no graph changed.
