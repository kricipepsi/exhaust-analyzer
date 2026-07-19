## Plan

I am beginning task `T-VLIVE-11` to frame the 7 canonical shared vocabulary notes (`OBD_VOCABULARY.md`, `GAS_VOCABULARY.md`, `DTC_VOCABULARY.md`, `SYMPTOM_VOCABULARY.md`, `VIN_VOCABULARY.md`, `DNA_VOCABULARY.md`, `SEMANTIC_CONTRACT.md`) under `labs/...`. I will frame 7 notes in total, all as `node_type: wiki`. I will confirm that all implements/drift guard paths exist on disk (applying the `code/` to `<lab>/` remap for the mirror paths) and all named consumers resolve via `grep` before writing any frontmatter, and then run pytest on all affected labs' test suites to confirm everything remains green.

## Verification results

- Eligibility: `T-VLIVE-11` was the active `pending` row; blocker `T-VLIVE-1` reached `done`.
- Framed notes: 7 shared vocabulary notes total (`OBD_VOCABULARY.md`, `GAS_VOCABULARY.md`, `DTC_VOCABULARY.md`, `SYMPTOM_VOCABULARY.md`, `VIN_VOCABULARY.md`, `DNA_VOCABULARY.md`, `SEMANTIC_CONTRACT.md`).
- No duplicate `§4` blocks were added; all files received one top block.
- `.base` mechanical row counts for vocabulary notes: `modules=7`, `consumers=7` with 0 `MISSING` consumers, `drift-guards=7`.
- Anti-orphan gate: every map `implements` / `drift_guards` path exists after remapping (mirror `code/` tier remapped to live `labs/<lab>/<lab>/...`); all named consumers resolve on disk.
- Test suites:
  - `obdlab` tests: 388 passed, 2 skipped
  - `gaslab` tests: 208 passed, 2 skipped, 4 deselected
  - `dtclab` tests: 590 passed
  - `symptomlab` tests: 63 passed
  - `vinlab` tests: 194 passed, 8 skipped
  - `dnalab` tests: 27 passed
  - `comlab` tests: 510 passed, 4 skipped
- Graph untouched: `git status --porcelain -- labs/*/graph/` is clean; no other graph files or indices were changed.

## VERIFICATION GATE

- [x] Eligibility: `T-VLIVE-11` was active runnable `pending` row; blocker `T-VLIVE-1` is `done`.
- [x] Framed notes present with valid `§4` frontmatter: 7/7.
- [x] No empty `consumers`: 0 missing across 7 framed vocabulary notes.
- [x] Bases render mechanically: `modules=7`, `consumers=7`, `drift-guards=7` for vocabulary map corpus.
- [x] Tests green: all affected lab tests passed.
- [x] Graph untouched: only the targeted doc `.md` files changed.
- [x] Anti-orphan confirmed: all remapped live paths and implements/guards exist; consumers verified.

## CODE REVIEW

- [x] Schema conformance: fixed `node_type` values (`wiki`) only.
- [x] Live path remap: vocabulary map paths remapped to drop mirror `code/` tier to target live `labs/<lab>/<lab>/...`.
- [x] Signal/noise: every framed note has at least one architect-authored consumer from `vault-map.vocabulary.yaml`.
- [x] No duplicate frontmatter: all files received one top block.
- [x] Scope guard: T-VLIVE-11 frames the 7 shared vocabulary notes completely.

