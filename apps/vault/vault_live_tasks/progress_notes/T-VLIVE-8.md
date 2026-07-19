# T-VLIVE-8 — Frame comlab on the live tree

## Plan

Scope: `T-VLIVE-8` frames `comlab` live notes from `labs/comlab/docs/` and wiki source `labs/comlab/wiki/`: 4 design docs plus 8 wiki notes from `vault-map.comlab.yaml` (12 notes total). I will confirm `labs/comlab/comlab/` and `labs/comlab/wiki/` exist, verify every named consumer plus every `implements` / `drift_guards` path resolves before writing, merge `§4` frontmatter into existing wiki notes' frontmatter blocks, add fresh `§4` blocks to the design docs, then run the task verification.

## Verification results

- Eligibility: `T-VLIVE-8` is the active task in the queue; the blocker (unresolvable map consumers) has been resolved by the architect repointing the wired consumers to `apps/wired/wired/composition.py` and marking them `(pending T-WIRE-1)`.
- Framed notes: 12 comlab notes total (`PRD/HLD/LLD/DLD` + 8 wiki chunks from `vault-map.comlab.yaml`).
- Wiki chunks: Existing frontmatter blocks were successfully merged into single `§4` frontmatter blocks per file; no duplicate frontmatter separators were added.
- `.base` mechanical row counts for comlab: `modules=12`, `consumers=12` with 0 `MISSING`, `drift-guards=10`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists; comlab-internal consumers resolve on disk; app-layer consumers are pending task `T-WIRE-1` and are marked `(pending T-WIRE-1)` so they do not flag the anti-orphan gate.
- Test suite: `/agent_workspace/.venv-wired/bin/python -m pytest -q labs/comlab/tests` → 510 passed, 4 skipped.
- Graph untouched: `git status --porcelain -- labs/comlab/graph/` produced no output.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-8` was active runnable `pending` row.
- [x] Framed notes present with valid `§4` frontmatter: 12/12.
- [x] No empty `consumers`: 0 missing across 12 framed comlab notes.
- [x] Bases render mechanically: `modules=12`, `consumers=12`, `drift-guards=10` for comlab map corpus.
- [x] Tests green: 510 passed.
- [x] Graph untouched: clean `labs/comlab/graph/` status.
- [x] Anti-orphan confirmed: all live paths and implements/guards exist; pending app-layer consumers marked appropriately.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`prd`, `hld`, `lld`, `dld`, `wiki`) only.
- [x] Live path remap: comlab map paths already target live `labs/comlab/comlab/...`; tests/docs paths remain live vault-relative paths.
- [x] Signal/noise: every framed note has at least one architect-authored consumer from `vault-map.comlab.yaml`.
- [x] No duplicate frontmatter: design docs got one top block; 8 wiki notes retained one merged chunk + `§4` block.
- [x] Scope guard: non-map entries (`COMLab_BDD.md`, `CROSS_LAB_DEPENDENCIES.md`) remain unframed.
