# T-VLIVE-8 — Frame comlab on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md` **and** `labs/comlab/_comlab_skills/comlab-vault-prep/SKILL.md` (COMLab is the terminal fusion spine — its consumers are COMLab-internal `core/`/`analytics/`/`schemas/` or the app layer, **never another lab**; proposals stay proposals).

## Goal
Add `§4` frontmatter to comlab's live notes — design docs in `labs/comlab/docs/`
+ wiki notes in `labs/comlab/wiki/` — exactly the ~12 `frame:` entries in
`vault-map.comlab.yaml`, so comlab appears in all three `.base` views on live.

## Context
Root `_bases/` + `Vault/` exclusion already in place (T-VLIVE-1). Live package dir =
`labs/comlab/comlab/`; standard remap `labs/comlab/code/X` → `labs/comlab/comlab/X`
(`tests/`,`docs/` unchanged). **Wiki source = `labs/comlab/wiki/`.**

**The comlab wrinkle (do not get this wrong):** comlab's live wiki notes
(`labs/comlab/wiki/*.md`) **already carry frontmatter** — the graphify *chunk*
schema (`chunk_id`, `title`, `doc`, `version`, …). You must **merge** the `§4`
fields (`node_type`, `lab`, `module`, `subsystem`, `implements`, `consumers`,
`drift_guards`, `tags`, `source`) **into that existing block** — never add a
second `---` block (two frontmatter blocks corrupt the note). Design docs in
`labs/comlab/docs/` are bare → add a fresh `§4` block there.

## Consumer (signal/noise)
`consumers` from `vault-map.comlab.yaml`, never empty, and per `comlab-vault-prep`:
they are COMLab-internal (`labs/comlab/comlab/core|analytics|schemas/...`) or the
app layer — **never GAS/OBD/DTC/DNA** (those are inputs, not consumers).
**`grep`-confirm every named consumer file+symbol resolves; `test -f` every
`implements`/`drift_guards` path — before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Every comlab note in the map's `frame:` set carries the `§4` fields, paths remapped to live, `consumers` non-empty.
2. Wiki notes: `§4` fields **merged into** the existing chunk frontmatter (single block). Design docs: fresh `§4` block.
3. Idempotent: if `§4` fields are already present/merged, verify — never duplicate.

## Files to touch
- edit (frontmatter only): the `labs/comlab/docs/*.md` and `labs/comlab/wiki/*.md` notes named in `vault-map.comlab.yaml`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-8.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- registry (T-VLIVE-9/10); any other lab; `.base` query bodies; lab Python; note/chunk **bodies** (only the frontmatter block); any graph; `Vault/`; comlab proposals (`comlab/config/proposals/`, EP-*, default-off capabilities — copied plain, not framed).

## Verification
1. Each framed comlab note: `§4` fields present (merged into the single existing block for wiki notes), no empty `consumers`, paths exist, consumers resolve. **No second frontmatter block on any wiki note** (`grep -c '^---$'` ≤ 2 per note).
2. Obsidian-on-root: `consumers.base` shows comlab `ok (n≥1)`, zero `MISSING`; `modules.base` groups comlab; `drift-guards.base` shows `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/tests` green.
4. `git status --porcelain -- labs/comlab/graph/` clean.

## Success criteria
comlab renders in all three views on live with zero `MISSING` consumers, every wiki note has exactly one (merged) frontmatter block, comlab tests green, no graph changed.
