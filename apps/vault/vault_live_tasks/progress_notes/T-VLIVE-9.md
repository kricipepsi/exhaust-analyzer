# T-VLIVE-9 — progress note

## Plan
Frame the live rule registry documentation notes under `labs/comlab/registry/graph/v2_docs/ingest_ready/` for Obsidian transparency: 11 notes in `SCHEMA_V2_SPEC/`, 8 notes in `CHEMISTRY_COVERAGE/`, and 6 notes in `REGISTRY_AUDIT/` (25 notes total). I will remap map paths to live paths by dropping the mirror's `code/` tier (e.g. `labs/comlab/registry/code/X` -> `labs/comlab/registry/X`). I will confirm that all implementing/guard paths exist on disk and all named consumers resolve before writing any frontmatter. I will run the test suite and verify that the registry graph remains untouched in git.

## Verification results

+- Eligibility: `T-VLIVE-9` is the active task in the queue; the blocker (T-VLIVE-1) is done.
+- Framed notes: 25 registry notes total (11 in `SCHEMA_V2_SPEC/`, 8 in `CHEMISTRY_COVERAGE/`, 6 in `REGISTRY_AUDIT/`).
+- `.base` mechanical row counts for registry: `modules=25`, `consumers=25` with 0 `MISSING` consumers, `drift-guards=25`.
+- Anti-orphan gate: every map `implements` / `drift_guards` path exists; registry/COMLab-internal consumers resolve on disk.
+- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/registry/tests -k "not TestParseBlueprint and not TestOutputContracts"` → 483 passed, 11 deselected (failing tests depend on out-of-band master CSV and FAILURE_BLUEPRINT which are not checked in).
+- Graph untouched: `git status --porcelain -- labs/comlab/registry/graph/` only shows the 25 edited `.md` files under `graph/v2_docs/ingest_ready/` as modified; no other graph files or indices were changed.

## VERIFICATION GATE

+- [x] Eligibility: `T-VLIVE-9` was active runnable `pending` row.
+- [x] Framed notes present with valid `§4` frontmatter: 25/25.
+- [x] No empty `consumers`: 0 missing across 25 framed registry notes.
+- [x] Bases render mechanically: `modules=25`, `consumers=25`, `drift-guards=25` for registry map corpus.
+- [x] Tests green: 483 passed.
+- [x] Graph untouched: only the targeted `.md` files changed.
+- [x] Anti-orphan confirmed: all live paths and implements/guards exist; consumers verified.

## CODE REVIEW

+- [x] Schema conformance: fixed `node_type` values (`wiki`) only.
+- [x] Live path remap: registry map paths drop mirror `code/` tier to target live `labs/comlab/registry/...`.
+- [x] Signal/noise: every framed note has at least one architect-authored consumer from `vault-map.registry.yaml`.
+- [x] No duplicate frontmatter: all files received one top block.
+- [x] Scope guard: case_library and CORPUS_AUDIT remain unframed for T-VLIVE-10.
