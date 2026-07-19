# T-VLIVE-3 — Frame dtclab on the live tree

## Plan

Scope: `T-VLIVE-3` frames the live notes of `dtclab`. The wiki source is `labs/dtclab/wiki/` and the design docs live in `labs/dtclab/docs/`. I will frame 15 notes total (4 design docs and 11 wiki notes) as defined in `vault-map.dtclab.yaml`. I will confirm that every consumer and implements/drift_guards path resolves on disk before prepending the `§4` frontmatter block to each note, running the test suites, and confirming that no graph files were touched.

## Verification results

- Eligibility: `T-VLIVE-3` was the first runnable `pending` row after blocker `T-VLIVE-3b` was completed.
- Framed notes: 15 notes total (4 design docs in `labs/dtclab/docs/` and 11 wiki notes in `labs/dtclab/wiki/` as defined in `vault-map.dtclab.yaml`).
- Existing wiki chunk frontmatter: none existed; brand new `§4` frontmatter blocks prepended.
- `.base` mechanical row counts for dtclab: `modules=15`, `consumers=15` with 0 `MISSING` consumers, `drift rows=13` (13 notes with non-empty `implements`).
- Anti-orphan gate: every `implements` and `drift_guards` path exists; every consumer resolves to a live file on disk. Symbol verification confirms `_load_discriminator_table` and `routing_tag` exist in `labs/comlab/comlab/core/fault_atlas_router.py`.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/dtclab/tests` -> 590 passed.
- Graph untouched: `git status --porcelain -- labs/dtclab/graph/` produced no output.
- Desktop Obsidian render check: not run in-session; bases query semantics verified mechanically.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-3` was first runnable `pending` row; blocker `T-VLIVE-3b` is `done`.
- [x] Framed notes present with valid `§4` frontmatter: 15/15.
- [x] No empty `consumers`: 0 missing across 15 framed dtclab notes.
- [x] Bases render mechanically: `modules=15`, `consumers=15`, `drift-guards=13` for dtclab map corpus.
- [x] Tests green: 590 passed.
- [x] Graph untouched: clean `labs/dtclab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: dtclab map paths already target live `labs/dtclab/dtclab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.dtclab.yaml`.
- [x] No duplicate frontmatter: all notes got exactly one `§4` frontmatter block at the top.
- [x] Scope guard: plain-map entries (`ADR_DTCLab.md`, `BDD_DTCLab.md`, `DTC_VOCABULARY.md`, `00_INDEX.md`, `11_proposals_register.md`) remain unframed.

