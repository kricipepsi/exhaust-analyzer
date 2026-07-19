# T-VLIVE-11 — Frame the shared `_vocabulary/` notes on the live tree

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-1
**Load skills:** `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`.

## Goal
Add `§4` frontmatter to the **7 canonical vocabulary notes** named in
`vault-map.vocabulary.yaml` so the cross-lab semantic vocabulary appears in the
three `.base` views on live. These are shared notes, not a single lab.

## Context
**The map shape differs from the per-lab tasks:** `vault-map.vocabulary.yaml`
uses a top-level **`vocabulary:`** key (not `frame:`), and each entry carries its
own `lab`, `module`, `node_type` (all `wiki`), `subsystem`, `implements`,
`consumers`, `drift_guards`, and a **`canonical:`** path — the live note to frame.
Frame the note at each entry's `canonical:` path (confirmed present on disk):

- `labs/semantic/vocabul/OBD_VOCABULARY.md`
- `labs/gaslab/docs/GAS_VOCABULARY.md`
- `labs/dtclab/docs/DTC_VOCABULARY.md`
- `labs/symptomlab/docs/SYMPTOM_VOCABULARY.md`
- `labs/vinlab/docs/VIN_VOCABULARY.md`
- `labs/dnalab/docs/DNA_VOCABULARY.md`
- `labs/semantic/vocabul/SEMANTIC_CONTRACT.md`

All sit under `labs/...`, so they match `modules.base`'s `inFolder("labs")`.
**Remap:** some entries' `implements` use the mirror `code/` tier (e.g.
`labs/obdlab/code/schemas/vocabulary.py`, `labs/gaslab/code/contracts.py`) →
live `labs/<lab>/<lab>/...`; others are already live-form. Apply the
`code/`→`<lab>/` remap per entry and `test -f` each path. `source:` = the entry's
`source`/`canonical` path (its own live location).

## Consumer (signal/noise)
`consumers` come from the map, never empty, and are live COMLab/lab reads.
**`grep`-confirm each named consumer file+symbol resolves; `test -f` each remapped
`implements`/`drift_guards` before writing.** Unresolvable → STOP, route to architect.

## Deliverables
1. Each of the 7 canonical notes carries one valid `§4` block, `node_type: wiki`,
   the entry's `lab`/`module`/`subsystem`, `implements` remapped to live,
   `consumers` non-empty, `source` self-reference.
2. Idempotent: verify, never duplicate.

## Files to touch
- edit (frontmatter only): the 7 `canonical:` notes listed above
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-11.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Any lab's design-doc/wiki framing (those are T-VLIVE-2…6/8); the `apps/ui` corpus (deferred — see ledger); `.base` query bodies; note **bodies**; any graph; `Vault/`.

## Verification
1. Each of the 7 notes: one valid `§4` block, `node_type: wiki`, no empty `consumers`, every remapped `implements`/`drift_guards` path exists, every consumer resolves (`grep`). No duplicate blocks.
2. Obsidian-on-root: `consumers.base` shows the 7 vocab notes `ok (n≥1)`, zero `MISSING`; `modules.base` groups them under their `lab` with `module: semantic-vocabulary`; `drift-guards.base` shows their `implements`→guards. (No desktop → assert mechanically; flag owner render-check.)
3. The vocab notes' owning-lab test suites stay green where a test parses the note: run the affected labs' `tests` (obdlab, gaslab, dtclab, symptomlab, vinlab, dnalab, comlab) via `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/<lab>/tests` for each lab whose vocab note you edited.
4. `git status --porcelain -- labs/*/graph/` clean.

## Success criteria
All 7 vocabulary notes render in the three views on live with zero `MISSING` consumers; affected lab tests green; no graph changed.
