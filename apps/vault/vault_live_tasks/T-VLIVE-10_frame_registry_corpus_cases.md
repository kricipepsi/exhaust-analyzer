# T-VLIVE-10 — Frame registry on the live tree (part 2: case library + corpus audit)

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-9 (part 1 establishes the registry remap + first rows)
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Frame the remaining registry sections per `vault-map.registry.yaml` —
`case_library/` (~18) + `CORPUS_AUDIT/` (~10), ≈28 notes — completing the
registry's appearance in all three `.base` views on live.

## Context
Same registry-specific remap and note location as **T-VLIVE-9** (read its
`## Context`): notes under `labs/comlab/registry/docs/<section>/...`; map `code/`
tier drops to the registry root (`labs/comlab/registry/<X>`, plus `tools/`,
`shim/`). T-VLIVE-9 has already validated the remap and the root `_bases/`.

## Consumer (signal/noise)
`consumers` from the map, never empty, registry/COMLab-internal. **`grep`-confirm
each consumer + `test -f` each remapped `implements`/`drift_guards` before
writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Each note in the `case_library/` + `CORPUS_AUDIT/` `frame:` groups carries one
   valid `§4` block, paths remapped, `consumers` non-empty.
2. Idempotent: verify/merge, never duplicate.
3. If the combined set proves too large for one clean session, frame
   `case_library/` here and register `CORPUS_AUDIT/` as `T-VLIVE-10b` in
   `Unplanned follow-ups` — do not rush a partial, unverified pass.

## Files to touch
- edit (frontmatter only): `labs/comlab/registry/docs/case_library/**`, `.../CORPUS_AUDIT/**` as named in the map
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-10.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- The three groups in T-VLIVE-9; comlab proper; `.base` bodies; registry Python; doc **bodies**; any graph; `Vault/`.

## Verification
1. Each framed note: one valid `§4` block, no empty `consumers`, paths exist, consumers resolve. No duplicates.
2. Obsidian-on-root: the new registry notes show in `consumers.base` `ok (n≥1)`, `modules.base` (lab: registry), `drift-guards.base`. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/registry/tests` green.
4. `git status --porcelain -- labs/comlab/registry/graph/` clean.

## Success criteria
All registry framed notes (parts 1+2) render in the three views on live with zero `MISSING` consumers; registry tests green; no graph changed.
