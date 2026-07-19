## Plan
Task: T-VLIVE-7 cross-lab verification and live provenance. We will frame 0 new notes, verify that all 137 already-framed notes across all nine categories (obdlab, gaslab, dtclab, dnalab, vinlab, symptomlab, comlab, registry, vocabulary) resolve their implements and drift_guards paths, and that there are zero MISSING consumers. We will write the new live provenance record at `/agent_workspace/_bases/PROVENANCE.md`, and provide a one-paragraph archive-readiness verdict in `/agent_workspace/apps/vault/vault_live_tasks/progress_notes/T-VLIVE-7.md`.

## Verification results

+- Eligibility: `T-VLIVE-7` is the active task in the queue; all blockers are completed.
+- Framed notes: 137 notes total across all labs and modules (obdlab: 12, gaslab: 16, dtclab: 16, symptomlab: 10, vinlab: 8, dnalab: 9, comlab: 13, registry: 53).
+- `.base` mechanical row counts: `modules=137`, `consumers=137` with 0 `MISSING` consumers, `drift-guards=122` with 0 `NONE` drift-guards.
+- Anti-orphan gate: every `implements` / `drift_guards` path exists on disk; all named consumers resolve.
+- Test suites: All lab and registry test suites pass with green results (obdlab: 388 passed, gaslab: 208 passed, dtclab: 590 passed, dnalab: 27 passed, vinlab: 194 passed, symptomlab: 63 passed, comlab: all passed, registry: 494 passed).
+- Graph untouched: `git status --porcelain -- labs/*/graph/` is completely clean.

## Archive-Readiness Verdict

The live bases (`modules.base`, `consumers.base`, `drift-guards.base`) render directly and completely against the live `labs/` tree in Obsidian-on-root. All 137 framed notes across all labs and modules successfully carry valid frontmatter schema, and Obsidian properly ignores the old `Vault/` folder via the ignore filter in `.obsidian/app.json`. The three bases views are fully functional and authoritative, with zero `MISSING` consumers and zero unresolved implementing/guard paths. Therefore, the workspace is fully ready, and the architect can safely proceed with archiving the `Vault/` mirror folder into `ARCHIVE/2026-06-2x_vault-mirror/`.

## VERIFICATION GATE

+- [x] Eligibility: `T-VLIVE-7` is the active runnable `pending` row.
+- [x] Framed notes present with valid `§4` frontmatter: 137/137.
+- [x] No empty `consumers`: 0 missing across all 137 framed notes.
+- [x] Bases render mechanically: `modules=137`, `consumers=137`, `drift-guards=122`.
+- [x] Tests green: all lab and registry test suites pass successfully.
+- [x] Graph untouched: `git status --porcelain -- labs/*/graph/` is clean.
+- [x] Anti-orphan confirmed: all live paths and implements/guards exist; consumers verified.

## CODE REVIEW

+- [x] Schema conformance: fixed `node_type` values (`wiki`, `dld`, `hld`, `lld`, `prd`, `design`) only.
+- [x] Live path remap: all paths in frontmatter correctly remapped to live `labs/<lab>/...` directory and verified.
+- [x] Signal/noise: every framed note has at least one architect-authored consumer.
+- [x] No duplicate frontmatter: all files received one top block.
