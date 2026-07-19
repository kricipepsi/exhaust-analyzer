# T-SHIP-4 — ledger hygiene: close stale rows with evidence (.md-only)
**Pack:** ship · **Blocked by:** — · **Lane:** coder (doc reconciliation; read-only on code)
**Write scope:** the ledger/wiki `.md` files named below. No code, data, or rule edits.

## Why (audit "Open, dispositioned" list)
Several ledgers assert states the audit disproved. A published repo must not carry
lying ledgers — the next session (or auditor) inherits them as truth.

## Rows to disposition (each flip carries a one-line evidence cite)
1. **Root harness pack** `harness/HARNESS_PROGRESS.md`: T-TH-0/3/5/6/7/8/10/11/12/13/14 +
   T-MASTER-RECON (pending/blocked since 2026-06-05). The wired v7 suite
   (`apps/wired/v7/`, 294-case corpus, hash-locked yardstick) is the live accuracy
   harness; the master-CSV track was superseded. Flip rows → `deferred (superseded by
   wired-v7 harness — reopen only by owner instruction)`; header note pointing at
   `apps/wired/v7_tasks/V7_PROGRESS.md`.
2. **gaslab** `labs/gaslab/tasks/PROGRESS.md`: `T-MIG-5` blocked/F-9 (TestSuite runner
   corpus refresh) — same supersession; annotate, do not delete.
3. **comlab** `labs/comlab/tasks/PROGRESS.md`: `T-RMW-MIRROR` (DEP-5) says wired is stuck
   at `ChemicalSignature==30`. Audit 2026-07-07 verified: the COMLab mirror enum is
   34-value (`labs/comlab/comlab/schemas/vocabulary.py:241`) and `WRONG_VALVE_TIMING`
   has no live reference (only an archived report). Re-verify with the same two greps,
   then flip → `void (stale — mirror reconciled via T-GV2-2 2026-06-28)`.
4. **FU-2 doc-sync** (gaslab follow-ups table): update the canonical mirror
   `OBD_VOCABULARY` §17 (now under `labs/comlab/docs/Vocabulary/`) from 32→34 chemistry
   values (drop `WRONG_VALVE_TIMING`, add the 3 `CAM_TIMING_*`), sync all live copies the
   semantic pack tracks (`labs/semantic/tasks/T-SEM-5` names them). Close FU-2.
5. **Post-launch backlog registration** (rows, `deferred`, one line each — no specs):
   registry `case_046-P0190` rule · `charging-system-alternator-gap` (needs DTC wiki task
   first) · `EXP-N023-uncoverable` (needs richer capture) · `T-COM-CAMTIMING-MAF-1`
   (already registered, cross-link) · 4 deferred gas-delta columns · abstain-cal (parked)
   · CASE-022 C6 sensor-dynamics data ask. Home: `apps/wired/ship_tasks/POST_LAUNCH_BACKLOG.md`,
   linked from `SHIP_PROGRESS.md`.

## Success criteria
- Every flipped row cites its evidence inline; zero rows deleted (archive, don't delete).
- `grep -rn "pending" harness/HARNESS_PROGRESS.md` returns no task rows.
- FU-2: §17 lists exactly the 34 live values (diff against
  `labs/comlab/comlab/schemas/vocabulary.py`); FU-2 row closed with date.
