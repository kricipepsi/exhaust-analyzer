## Plan

I am beginning task `T-VLIVE-5` to frame the `vinlab` live notes. The wiki-source folder is `labs/vinlab/wiki/` and the live package dir is `labs/vinlab/vinlab/`. I will frame 7 notes in total: 4 design docs (`PRD_VINLab.md`, `HLD_VINLab.md`, `LLD_VINLab.md`, `DLD_VINLab.md`) and 3 wiki notes (`10_decode_scope_rules.md`, `11_engine_resolution.md`, `12_brand_cylinder_rules.md`). I will verify that every named consumer (reconciled by `T-VLIVE-5b`) and all `implements` and `drift_guards` paths exist and resolve in the live tree before writing frontmatter, and then run pytest on `labs/vinlab/tests` to confirm everything is green.

## Verification results

- Eligibility: `T-VLIVE-5` was the first runnable `pending` row after blockers `T-VLIVE-1` and `T-VLIVE-5b` reached `done`.
- Framed notes: 7 vinlab notes total (`PRD/HLD/LLD/DLD` + 3 `wiki/*.md` notes from `vault-map.vinlab.yaml`).
- Existing wiki chunk frontmatter was merged into one top YAML block per wiki note; no duplicate `§4` blocks were added.
- `.base` mechanical row counts for vinlab: `modules=7`, `consumers=7` with 0 `MISSING`, `drift-guards=5`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists; every consumer file resolves by live read/search. Search-confirmed consumer symbols include `build_vehicle_dna`, `RobustVINDecoder.decode_vin_payload`, `_is_non_petrol`, `validate_vin_checksum`, `_resolve_wmi`, `_resolve_year`, `_resolve_engine`, `euro_to_horizon`, `infer_cylinder`, `project()`, and `FuelSystemStatus.CL`.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/vinlab/tests` → 194 passed, 8 skipped.
- Graph untouched: `git status --porcelain -- labs/vinlab/graph/` produced no output.
- Desktop Obsidian render check not run in-session; the same frontmatter filters were mechanically asserted against `_bases/modules.base`, `_bases/consumers.base`, and `_bases/drift-guards.base` semantics.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-5` was first runnable `pending` row; blockers `T-VLIVE-1` and `T-VLIVE-5b` are `done`.
- [x] Framed notes present with valid `§4` frontmatter: 7/7.
- [x] No empty `consumers`: 0 missing across 7 framed vinlab notes.
- [x] Bases render mechanically: `modules=7`, `consumers=7`, `drift-guards=5` for vinlab map corpus.
- [x] Tests green: 194 passed, 8 skipped.
- [x] Graph untouched: clean `labs/vinlab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: vinlab map paths already target live `labs/vinlab/vinlab/...` and `labs/comlab/...` / `labs/dnalab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.vinlab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 3 wiki notes retained one merged chunk + `§4` block.
- [x] Scope guard: plain-map entries (`ADR_VINLab.md`, `BDD_VINLab.md`, `VIN_VOCABULARY.md`, etc.) remain unframed.
