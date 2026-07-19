## Plan

I am beginning task `T-VLIVE-4` to frame the `dnalab` live notes. The wiki-source folder is `labs/dnalab/wiki/` and the live package dir is `labs/dnalab/dnalab/`. I will frame 8 notes in total: 4 design docs (`PRD_DNALab.md`, `HLD_DNALab.md`, `LLD_DNALab.md`, `DLD_DNALab.md`) and 4 wiki notes (`10_vehicle_dna_envelope.md`, `11_schema_versioning.md`, `12_assembly_contract.md`, `13_session_identity.md`). I will verify that every named consumer (reconciled by `T-VLIVE-4b`) and all `implements` and `drift_guards` paths exist and resolve in the live tree before writing frontmatter, and then run pytest on `labs/dnalab/tests` to confirm everything is green.

## Verification results

- Eligibility: `T-VLIVE-4` was the first runnable `pending` row after blockers `T-VLIVE-1` and `T-VLIVE-4b` reached `done`.
- Framed notes: 8 dnalab notes total (`PRD/HLD/LLD/DLD` + 4 `wiki/*.md` notes from `vault-map.dnalab.yaml`).
- Existing wiki chunk frontmatter was merged into one top YAML block per wiki note; no duplicate `§4` blocks were added.
- `.base` mechanical row counts for dnalab: `modules=8`, `consumers=8` with 0 `MISSING`, `drift-guards=6`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists; every consumer file resolves by live read/search. Search-confirmed consumer symbols include `from_vehicle_dna`, `SessionMetadata.schema_version`, `project()`, `OrchestratorInboundRequest`, `route_symptom`, and `session_id`.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/dnalab/tests` → 27 passed.
- Graph untouched: `git status --porcelain -- labs/dnalab/graph/` produced no output.
- Desktop Obsidian render check not run in-session; the same frontmatter filters were mechanically asserted against `_bases/modules.base`, `_bases/consumers.base`, and `_bases/drift-guards.base` semantics.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-4` was first runnable `pending` row; blockers `T-VLIVE-1` and `T-VLIVE-4b` are `done`.
- [x] Framed notes present with valid `§4` frontmatter: 8/8.
- [x] No empty `consumers`: 0 missing across 8 framed dnalab notes.
- [x] Bases render mechanically: `modules=8`, `consumers=8`, `drift-guards=6` for dnalab map corpus.
- [x] Tests green: 27 passed.
- [x] Graph untouched: clean `labs/dnalab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: dnalab map paths already target live `labs/dnalab/dnalab/...` and `labs/comlab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.dnalab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 4 wiki notes retained one merged chunk + `§4` block.
- [x] Scope guard: plain-map entries (`ADR_DNALab.md`, `BDD_DNALab.md`, `DNA_VOCABULARY.md`, etc.) remain unframed.
