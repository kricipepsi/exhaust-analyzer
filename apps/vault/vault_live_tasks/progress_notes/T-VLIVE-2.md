## Plan

Scope: `T-VLIVE-2` frames `gaslab` live notes; wiki source is `labs/gaslab/wiki/`, live package dir is `labs/gaslab/gaslab/`, and the map-authored corpus is 15 notes: 4 design docs in `labs/gaslab/docs/` plus 11 wiki notes in `labs/gaslab/wiki/`. I will add only one `§4` frontmatter block per mapped note, remap `labs/gaslab/code/...` to `labs/gaslab/gaslab/...`, keep `tests/` and `docs/` paths unchanged, and confirm every named consumer plus every `implements`/`drift_guards` path resolves before writing.

## Verification results

- Framed notes: 15 gaslab notes total (`PRD/HLD/LLD/DLD` + 11 `wiki/*.md` notes from `vault-map.gaslab.yaml`).
- Existing wiki chunk frontmatter was merged into one top YAML block per wiki note; no duplicate `§4` blocks were added.
- `.base` mechanical row counts for gaslab: `modules=15`, `consumers=15` with 0 `MISSING`, `drift-guards=13`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists after live remap; every consumer file exists and resolves by live read/search. Search-confirmed consumer symbols include `chemical_state`, `gas_co/gas_hc/gas_o2/lambda_chem`, `sample_validity`, `lambda_measured`, `ChemicalSignature`, `_coc_adjust_normal_bounds`, `_euro_thresholds`, `block_test_passed`, `reading_high`, and ranking top-3 confidence constants.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/gaslab/tests` → 208 passed, 2 skipped, 4 deselected.
- Graph untouched: `git status --porcelain -- labs/gaslab/graph/` produced no output.
- Desktop Obsidian render check not run in-session; the same frontmatter filters were mechanically asserted against `_bases/modules.base`, `_bases/consumers.base`, and `_bases/drift-guards.base` semantics.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-2` was first runnable `pending` row after `T-VLIVE-1` was `done`; stale-ledger guard checked `T-VLIVE-1` gates and framed notes.
- [x] Framed notes present with valid `§4` frontmatter: 15/15.
- [x] No empty `consumers`: 0 missing across 15 framed gaslab notes.
- [x] Bases render mechanically: `modules=15`, `consumers=15`, `drift-guards=13` for gaslab map corpus.
- [x] Tests green: 208 passed, 2 skipped, 4 deselected.
- [x] Graph untouched: clean `labs/gaslab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all remapped `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: `labs/gaslab/code/...` became `labs/gaslab/gaslab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.gaslab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 11 wiki notes retained one merged chunk + `§4` block.
- [x] Scope guard: plain-map entries (`ADR_GASLab.md`, `BDD_GASLab.md`, `GAS_VOCABULARY.md`, `00_index.md`, `11_sources_appendices.md`, `CHANGE_v2.1_timing_taxonomy.md`) remain unframed.
