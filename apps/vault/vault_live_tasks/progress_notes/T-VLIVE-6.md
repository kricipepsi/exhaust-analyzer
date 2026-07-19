# T-VLIVE-6 — Frame symptomlab on the live tree

## Plan

Scope: `T-VLIVE-6` frames `symptomlab` live notes from `labs/symptomlab/docs/` and wiki source `labs/symptomlab/wiki/`: 4 design docs plus 5 wiki notes from `vault-map.symptomlab.yaml` (9 notes total). I will confirm `labs/symptomlab/symptomlab/` and `labs/symptomlab/wiki/` exist, verify every named consumer file+symbol and every `implements` / `drift_guards` path resolves after live remap before writing, add exactly one `§4` frontmatter block per framed note, then run the task verification.

## Verification results

- Eligibility: `T-VLIVE-6` is the first runnable `pending` row after stale-ledger guard confirmed `T-VLIVE-1` and `T-VLIVE-2` gates/framed notes; later pending rows remain behind it.
- Framed notes: 9 symptomlab notes total (`PRD/HLD/LLD/DLD` + 5 `wiki/*.md` notes from `vault-map.symptomlab.yaml`).
- Existing wiki chunk frontmatter was merged into one top YAML block per wiki note; no duplicate `§4` blocks were added.
- `.base` mechanical row counts for symptomlab: `modules=9`, `consumers=9` with 0 `MISSING`, `drift-guards=6`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists; every consumer file resolves by live read/search. Search-confirmed consumer symbols include `build_vehicle_dna`, `resolve()`, `SymptomDNA.from_json`, `VehicleDNA.symptom_dna`, `route_symptom`, `environmental_conditions.engine_state`, `environmental_conditions.occurs_during`, and `SymptomValidator.validate`.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/symptomlab/tests` → 63 passed.
- Graph untouched: `git status --porcelain -- labs/symptomlab/graph/` produced no output.
- Desktop Obsidian render check not run in-session; the same frontmatter filters were mechanically asserted against `_bases/modules.base`, `_bases/consumers.base`, and `_bases/drift-guards.base` semantics.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-6` was first runnable `pending` row; blocker `T-VLIVE-1` is `done`.
- [x] Framed notes present with valid `§4` frontmatter: 9/9.
- [x] No empty `consumers`: 0 missing across 9 framed symptomlab notes.
- [x] Bases render mechanically: `modules=9`, `consumers=9`, `drift-guards=6` for symptomlab map corpus.
- [x] Tests green: 63 passed.
- [x] Graph untouched: clean `labs/symptomlab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: symptomlab map paths already target live `labs/symptomlab/symptomlab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.symptomlab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 5 wiki notes retained one merged chunk + `§4` block.
- [x] Scope guard: plain-map entries (`ADR_SymptomLab.md`, `BDD_SymptomLab.md`, `SYMPTOM_VOCABULARY.md`) remain unframed.
