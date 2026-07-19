# T-DCA-GAS — gaslab doc↔code conformance audit
**Owner:** deepseek · **Status:** `pending` (runnable) · **Mode:** STRICT, READ-ONLY · **Method:** `../T-DCA-METHOD.md`

### Goal ###
Audit gaslab's design/contract docs against code and produce `planning/doc_conformance/reports/gaslab__deepseek.md`,
classifying every checked claim MATCH / DRIFT / UNDOCUMENTED / SUPERSEDED / PENDING (+ DUP-DRIFT for vocabulary)
per `../T-DCA-METHOD.md`. Read-only: discover, do not fix.

### Success criteria ###
- `reports/gaslab__deepseek.md` exists with: a counts header, a `doc:line | claim | class | code evidence (file:line) | proposed fix` table, and a one-line per-class verdict.
- **Seeded case reproduced (MATCH):** `GAS_VOCABULARY` + `ADR-0007` state `ChemicalSignature` = **34** (WRONG_VALVE_TIMING retired, 3 `CAM_TIMING_*` added); code `labs/gaslab/gaslab/contracts.py` has exactly 34 enum members and live code has 0 `WRONG_VALVE_TIMING`. A run that cannot reproduce this MATCH is wrong — STOP and re-check the method.
- `git --no-pager diff --stat` shows only `reports/gaslab__deepseek.md` added.

### Context ###
Surfaced by the 2026-06-29 doc-drift review: T-GTA covers framed graph edges only; HLD/LLD/ADR/Vocabulary *content* is unaudited. gaslab doc set to check: `labs/gaslab/docs/GAS_VOCABULARY.md`, `labs/gaslab/docs/ADR_GASLab.md` (chunks under `labs/gaslab/graph/v2_docs/ingest_ready/ADR_GASLab/`), `labs/gaslab/docs/HLD_GASLab.md`, `labs/gaslab/docs/LLD_GASLab.md`. Code: `labs/gaslab/gaslab/` — `contracts.py` (the `ChemicalSignature` enum, line ~32), `resolution.py`, `rule_engine.py`. Vocabulary duplicate to cross-check: `labs/semantic/vocabul/GAS_VOCABULARY.md` (test-anchored canonical) — flag **DUP-DRIFT** if it disagrees with the gaslab copy. Prioritise LLD "exact" sections (Physical Constants, Brettschneider lambda, Exhaust-Gas-Triangle boundaries, Definitive-Override thresholds) — each stated literal must match the code literal.
Load skills: `planning/doc_conformance/T-DCA-METHOD.md` (procedure), `_skills/doc/ADR.md`.

### Consumer (signal/noise) ###
N/A — read-only audit, adds no field/enum/fault.

### Deliverables ###
1. `planning/doc_conformance/reports/gaslab__deepseek.md` — the classified audit report.

### Files to touch ###
- `planning/doc_conformance/reports/gaslab__deepseek.md` (CREATE)

### Out of scope ###
Fixing any drift (that is the later `T-DCA-RECONCILE` pass); editing docs / code / maps / graph; `Vault/`; `graphify`; the framed-edge checks (those are T-GTA). Every finding is reported, never patched in this task.

### Verification ###
1. Every gaslab doc class (Vocabulary, ADR, HLD/LLD) covered; every enumerated claim classified with `doc:line` + `code:line` evidence; zero unclassified.
2. Seeded case reproduced as MATCH (ChemicalSignature = 34; 0 live `WRONG_VALVE_TIMING`).
3. `git --no-pager diff --stat` shows only the report added.

### Progress hook ###
Fill `progress_notes/T-DCA-GAS.md` (Plan at top, then VERIFICATION GATE + CODE REVIEW). Flip `DOC_CONFORMANCE_PROGRESS.md` row `T-DCA-GAS` → done with Verification="N claims: a MATCH / b DRIFT / c SUPERSEDED / d DUP-DRIFT / e PENDING; seeded MATCH OK". Then STOP.
