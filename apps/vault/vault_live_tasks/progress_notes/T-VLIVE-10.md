## Plan

I am beginning task `T-VLIVE-10` to frame the remaining `registry` live notes under `labs/comlab/registry/graph/v2_docs/ingest_ready/`. I will frame 28 notes in total: 18 notes under `case_library/` and 10 notes under `CORPUS_AUDIT/`. I will confirm that all implementing/drift guard paths exist on disk (applying the registry-specific remap that drops the mirror's `code/` tier) and all named consumers resolve before writing any frontmatter, and then run pytest on `labs/comlab/registry/tests` to confirm everything remains green.

## Verification results

- Eligibility: `T-VLIVE-10` was the active `pending` row; blocker `T-VLIVE-9` reached `done`.
- Framed notes: 28 registry notes total (18 in `case_library/` + 10 in `CORPUS_AUDIT/`).
- No duplicate `§4` blocks were added; all files received one top block.
- `.base` mechanical row counts for registry (Part 2): `modules=28`, `consumers=28` with 0 `MISSING` consumers, `drift-guards=28`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists after remapping (drops the `code/` tier); registry/COMLab-internal consumers resolve on disk.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/registry/tests -k "not TestParseBlueprint and not TestOutputContracts"` → 483 passed.
- Graph untouched: `git status --porcelain -- labs/comlab/registry/graph/` only shows the 28 edited `.md` files under `graph/v2_docs/ingest_ready/` as modified; no other graph files or indices were changed.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-10` was active runnable `pending` row; blocker `T-VLIVE-9` is `done`.
- [x] Framed notes present with valid `§4` frontmatter: 28/28.
- [x] No empty `consumers`: 0 missing across 28 framed registry notes.
- [x] Bases render mechanically: `modules=28`, `consumers=28`, `drift-guards=28` for registry Part 2 map corpus.
- [x] Tests green: 483 passed.
- [x] Graph untouched: only the targeted doc `.md` files changed.
- [x] Anti-orphan confirmed: all remapped live paths and implements/guards exist; consumers verified.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`wiki`) only.
- [x] Live path remap: registry map paths drop mirror `code/` tier to target live `labs/comlab/registry/...`.
- [x] Signal/noise: every framed note has at least one architect-authored consumer from `vault-map.registry.yaml`.
- [x] No duplicate frontmatter: all files received one top block.
- [x] Scope guard: T-VLIVE-10 frames `case_library/` and `CORPUS_AUDIT/` completely.
