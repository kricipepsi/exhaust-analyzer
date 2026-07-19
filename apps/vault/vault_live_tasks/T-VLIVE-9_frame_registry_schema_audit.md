# T-VLIVE-9 — Frame registry on the live tree (part 1: schema + chemistry + audit)

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to the **first three section groups** of the registry's
framed notes per `vault-map.registry.yaml` — `SCHEMA_V2_SPEC/` (~11),
`CHEMISTRY_COVERAGE/` (~8), `REGISTRY_AUDIT/` (~6), ≈25 notes — so the registry
begins appearing in the three `.base` views on live. Part 2 (`case_library/` +
`CORPUS_AUDIT/`) is **T-VLIVE-10**.

## Context
The registry is a sub-package consumed by COMLab; its framed notes live under
`labs/comlab/registry/docs/<section>/...` (the map's `frame:` keys are relative to
that docs root). The map's `lab:` is `registry`, `module:` `registry`.

**Registry-specific remap (NOT the lab rule):** the registry package root *is*
`labs/comlab/registry/` — there is **no `registry/registry/` dir**. So map paths
drop the mirror `code/` tier directly:
- `labs/comlab/registry/code/schema_v2.py` → `labs/comlab/registry/schema_v2.py`
- `labs/comlab/registry/code/tools/<X>.py` → `labs/comlab/registry/tools/<X>.py`
- `labs/comlab/registry/code/shim/<X>.py` → `labs/comlab/registry/shim/<X>.py`
- `labs/comlab/registry/tests/<X>` → unchanged
Confirm each remapped path with `test -f` (registry layout has `schema_v2.py`,
`integration_shim.py` at root + `tools/`, `shim/`, `tests/`).

## Consumer (signal/noise)
`consumers` from `vault-map.registry.yaml`, never empty — registry/COMLab-internal
readers. **`grep`-confirm every named consumer + `test -f` every
`implements`/`drift_guards` (remapped) before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Each note in the `SCHEMA_V2_SPEC/`, `CHEMISTRY_COVERAGE/`, `REGISTRY_AUDIT/`
   `frame:` groups carries one valid `§4` block, paths remapped per above, `consumers` non-empty.
2. Idempotent: verify, never duplicate. If any registry docs already carry prep
   frontmatter, **merge** the `§4` fields (single block) as in T-VLIVE-8.

## Files to touch
- edit (frontmatter only): `labs/comlab/registry/docs/SCHEMA_V2_SPEC/**`, `.../CHEMISTRY_COVERAGE/**`, `.../REGISTRY_AUDIT/**` as named in the map
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-9.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- `case_library/` + `CORPUS_AUDIT/` (T-VLIVE-10); comlab proper (T-VLIVE-8); `.base` bodies; registry Python; doc **bodies**; any graph; `Vault/`.

## Verification
1. Each framed note in the three groups: one valid `§4` block, no empty `consumers`, paths exist (remapped), consumers resolve. No duplicate blocks.
2. Obsidian-on-root: `consumers.base` shows the registry notes `ok (n≥1)`; `modules.base` groups `lab: registry`; `drift-guards.base` shows `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/registry/tests` green.
4. `git status --porcelain -- labs/comlab/registry/graph/` clean.

## Success criteria
The schema/chemistry/audit registry notes render in the three views on live with zero `MISSING` consumers; registry tests green; no graph changed. T-VLIVE-10 covers the rest.
