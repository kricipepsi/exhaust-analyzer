# T-DCA-OBD — obdlab doc↔code conformance audit
**Owner:** deepseek · **Status:** `pending` (runnable) · **Mode:** STRICT, READ-ONLY · **Method:** `../T-DCA-METHOD.md`

### Goal ###
Audit obdlab's design/contract docs against code and produce `planning/doc_conformance/reports/obdlab__deepseek.md`,
classifying every checked claim MATCH / DRIFT / UNDOCUMENTED / SUPERSEDED / PENDING (+ DUP-DRIFT for vocabulary)
per `../T-DCA-METHOD.md`. Read-only: discover, do not fix.

### Success criteria ###
- `reports/obdlab__deepseek.md` exists with: a counts header, a `doc:line | claim | class | code evidence (file:line) | proposed fix` table, and a one-line per-class verdict.
- **Seeded case reproduced (DRIFT + DUP-DRIFT, the known FU-2):** `OBD_VOCABULARY.md`'s changelog/§17 does not reflect the 32→34 ChemicalSignature timing split (DRIFT); and `labs/semantic/vocabul/OBD_VOCABULARY.md` (test-anchored canonical, parsed by `labs/comlab/tests/unit/test_vocabulary_sae_iso_conformance.py`) **differs** from the byte-identical `labs/obdlab/docs/OBD_VOCABULARY.md` + `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md` copies (DUP-DRIFT). A run that reports obdlab "clean" is wrong — STOP and re-check.
- `git --no-pager diff --stat` shows only `reports/obdlab__deepseek.md` added.

### Context ###
Surfaced by the 2026-06-29 doc-drift review. obdlab doc set: `labs/obdlab/docs/OBD_VOCABULARY.md`, `labs/obdlab/docs/ADR_OBDLab.md` (chunks under `labs/obdlab/graph/v2_docs/ingest_ready/ADR_OBDLab/`), `labs/obdlab/docs/HLD_OBDLab.md`, `labs/obdlab/docs/LLD_OBDLab.md`. Code: `labs/obdlab/obdlab/schemas/vocabulary.py` + `labs/obdlab/obdlab/core/`. Cross-check the three OBD_VOCABULARY copies (obdlab / `labs/comlab/docs/Vocabulary/` / `labs/semantic/vocabul/`) and name the test-anchored canonical. Prioritise LLD "exact" sections (Physical Constants, Sensor Bounds, VE formula/constants, O2-normaliser boundaries, lambda_perception_delta guard) — each literal must match code.
Load skills: `planning/doc_conformance/T-DCA-METHOD.md` (procedure), `_skills/doc/ADR.md`.

### Consumer (signal/noise) ###
N/A — read-only audit, adds no field/enum/fault.

### Deliverables ###
1. `planning/doc_conformance/reports/obdlab__deepseek.md` — the classified audit report.

### Files to touch ###
- `planning/doc_conformance/reports/obdlab__deepseek.md` (CREATE)

### Out of scope ###
Fixing any drift (later `T-DCA-RECONCILE` pass, incl. deduping vocabulary to the canonical + closing FU-2); editing docs / code / maps / graph; `Vault/`; `graphify`; framed-edge checks (T-GTA).

### Verification ###
1. Every obdlab doc class (Vocabulary, ADR, HLD/LLD) covered; every enumerated claim classified with `doc:line` + `code:line` evidence; zero unclassified.
2. Seeded case reproduced: §17 staleness = DRIFT, semantic-vs-copies divergence = DUP-DRIFT.
3. `git --no-pager diff --stat` shows only the report added.

### Progress hook ###
Fill `progress_notes/T-DCA-OBD.md` (Plan at top, then gates). Flip `DOC_CONFORMANCE_PROGRESS.md` row `T-DCA-OBD` → done with the class counts. Then STOP.
