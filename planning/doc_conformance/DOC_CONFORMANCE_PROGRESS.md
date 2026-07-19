# Doc-Conformance Audit — Progress Ledger
**Method spec (all `T-DCA-*` rows):** `T-DCA-METHOD.md` · **Reports:** `reports/<lab>__<agent>.md`.
**Mode:** STRICT (read-only audit; no doc/code edits). **Last updated:** 2026-06-29 (architect, Cowork — pack authored).
**Why this pack exists:** T-GTA audits framed graph edges only; the **content** of HLD/LLD, ADRs, and
Vocabulary docs vs code was unaudited. The 2026-06-29 drift review found triplicated vocabulary copies
that have diverged (see seeded cases). This is the only file a `T-DCA` coder needs after `T-DCA-METHOD.md`.
Keep under ~120 lines. Gate blocks / evidence go in the report, not here.

## How to run
Non-coding lane → run on **deepseek** (`run-deepseek.sh`, Claude Code harness; export `DEEPSEEK_API_KEY` first).
Launch a session, paste the task file (`tasks/T-DCA-<LAB>_*.md`) — it pins the procedure (`T-DCA-METHOD.md`),
the doc set, and the seeded case. deepseek audits, writes `reports/<lab>__deepseek.md`, fills
`tasks/progress_notes/T-DCA-<LAB>.md`, flips the row, STOPs. **One lab per session.**

## Seeded validation cases (the audit MUST reproduce these)
1. **gaslab — MATCH:** `GAS_VOCABULARY` + `ADR-0007` state `ChemicalSignature` = **34** (WRONG_VALVE_TIMING
   retired, 3 `CAM_TIMING_*` added). Code `gaslab/contracts.py` has exactly 34 members; 0 `WRONG_VALVE_TIMING`
   in live code. The audit must classify these MATCH.
2. **obdlab — DRIFT + DUP-DRIFT (known FU-2):** `OBD_VOCABULARY.md` changelog stops at v1.1 and never records
   the 32→34 timing split; and `labs/semantic/vocabul/OBD_VOCABULARY.md` (test-anchored canonical, parsed by
   `comlab/tests/unit/test_vocabulary_sae_iso_conformance.py`) **differs** from the byte-identical
   `obdlab/docs/` + `comlab/docs/Vocabulary/` copies. The audit must catch both the stale §17 (DRIFT) and the
   copy divergence (DUP-DRIFT). A run that reports obdlab "clean" is wrong.

## Task log
| ID | Method | Owner | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|---|
| T-DCA-GAS | `tasks/T-DCA-GAS_gaslab_doc_conformance.md` | deepseek | done | — | 2026-06-29 | — | 30 claims: 29 MATCH / 0 DRIFT / 0 SUPERSEDED / 1 DUP-DRIFT / 0 PENDING; seeded MATCH OK | gaslab: `GAS_VOCABULARY` + `ADR_GASLab`/`adr` + `HLD/LLD_GASLab` vs `gaslab/contracts.py`,`gaslab/`. Seeded case 1. → `reports/gaslab__deepseek.md` |
| T-DCA-OBD | `tasks/T-DCA-OBD_obdlab_doc_conformance.md` | deepseek | done | — | 2026-06-29 | — | 20 claims: 16 MATCH / 3 DRIFT / 0 SUPERSEDED / 1 DUP-DRIFT / 0 PENDING; seeded case OK | obdlab: `OBD_VOCABULARY` (+ comlab/semantic copies) + ADRs + `HLD/LLD_OBDLab` vs `obdlab/schemas/vocabulary.py`. Seeded case 2 (FU-2). → `reports/obdlab__deepseek.md` |
**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`.
**Runnability:** `pending` = runnable now; each coder picks the first `pending` row whose Owner = its id.

## Deferred waves (promote one wave at a time, after the prior reports land)
Wave 1 (above): **gaslab**, **obdlab** — emitter labs the wiring composes; both carry vocabulary in the
divergence set. Promote the next waves by adding `T-DCA-<LAB>` rows in this order:
1. **dtclab**, **vinlab** — LLD "exact constant/regex/threshold" rich; dtclab is in the DTC_VOCABULARY
   tri-divergence (all three copies differ).
2. **comlab** — largest doc set (HLD+LLD+11 ADRs+Vocabulary dir); audit after its emitters.
3. **dnalab**, **symptomlab** — smaller; partition one coder each.
Final: `T-DCA-RECONCILE` — one architect-reviewed pass that applies every report's DRIFT/SUPERSEDED/
DUP-DRIFT fixes (incl. deduping vocabulary to the test-anchored canonical + closing FU-2). Author after the
wave reports exist. **Not a wiring gate** — doc conformance is a quality pass, not a `T-WIRE-1` blocker.

## Architect-level out-of-band patches
| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-29 | `planning/doc_conformance/**` | Authored the Doc-Conformance Audit pack (METHOD + ledger + reports/) and promoted wave-1 (gaslab, obdlab). | Owner doc-drift review: HLD/ADR/Vocabulary content was unaudited; found triplicated vocabulary divergence + open FU-2. |
