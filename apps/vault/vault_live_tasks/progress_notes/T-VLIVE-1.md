## Plan

Scope: `T-VLIVE-1` pilot for `obdlab`; wiki source is `labs/obdlab/research/chunks/`. I will frame the map-authored corpus: 4 design docs in `labs/obdlab/docs/` (`PRD/HLD/LLD/DLD`) plus verify the 7 existing wiki README nodes, for 11 framed notes total. The docs folder also contains `ADR_OBDLab.md`, `BDD_OBDLab.md`, and `OBD_VOCABULARY.md`, but `vault-map.obdlab.yaml` provides no semantic fields for them, so they stay plain. I will create root `_bases/`, add `Vault/` to `.obsidian/app.json`, and confirm every named consumer plus every `implements`/`drift_guards` path resolves before writing frontmatter.

## Verification results

- `_bases/modules.base`, `_bases/consumers.base`, `_bases/drift-guards.base`: byte-identical to `_skills/graph/4dlab-vault/assets/` copies.
- `.obsidian/app.json`: valid JSON; `userIgnoreFilters` includes `Vault/`.
- Framed notes: 11 obdlab notes total (`PRD/HLD/LLD/DLD` + 7 `research/chunks/*/README.md`).
- `.base` mechanical row counts for obdlab: `modules` 11, `consumers` 11 with 0 `MISSING`, `drift-guards` 9.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists after live remap; every consumer path resolves. Pathless `comlab: fault_atlas fusion (perception channel)` resolved to live COMLab fault-atlas router / aggregator reads (`labs/comlab/comlab/core/fault_atlas_router.py`, `labs/comlab/comlab/core/lab_pipeline_aggregator.py`).
- Wiki frontmatter repair: existing 7 README blocks were single blocks; repaired `module` to `obd_live_lab` and `implements` to live `labs/obdlab/obdlab/...` paths.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/obdlab/tests` → 388 passed, 2 skipped.
- Graph untouched: `git status --porcelain -- labs/obdlab/graph/` produced no output.
- Test-path maintenance: `labs/obdlab/tests/unit/test_dna_view.py` now resolves current live COMLab vocabulary at `labs/comlab/docs/Vocabulary/` before legacy `docs/wiki` fallbacks; this unblocked the task-required suite and does not change lab runtime code.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-1` was first runnable `pending` row; blockers `—`.
- [x] Root bases present and byte-identical to assets: 3/3.
- [x] `Vault/` excluded in Obsidian app config; JSON parses.
- [x] Framed notes present with valid `§4` frontmatter: 11/11.
- [x] No empty `consumers`: 0 missing across 11 framed obdlab notes.
- [x] Bases render mechanically: `modules=11`, `consumers=11`, `drift-guards=9` for obdlab map corpus.
- [x] Tests green: 388 passed, 2 skipped.
- [x] Graph untouched: clean `labs/obdlab/graph/` status.
- [x] Anti-orphan confirmed: all named consumer paths and all remapped `implements` / `drift_guards` paths resolve.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: `labs/obdlab/code/...` became `labs/obdlab/obdlab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored named consumer from `vault-map.obdlab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 7 wiki READMEs retained one repaired block.
- [x] Scope guard: non-map docs (`ADR_OBDLab.md`, `BDD_OBDLab.md`, `OBD_VOCABULARY.md`) remain plain because the map provides no semantic fields for them.
