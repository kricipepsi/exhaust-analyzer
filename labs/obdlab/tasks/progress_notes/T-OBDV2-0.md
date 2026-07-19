# T-OBDV2-0 — decision record (scope gate)

**Type:** scope-gate decision (no code; no VERIFICATION GATE / CODE REVIEW — those apply to build tasks).
**Decision:** `revive` — **emitter role**.
**Date / ratification:** 2026-06-08, owner-ratified in session (owner confirmed the emitter framing against
their own research `KGtopic.md`).

## Rationale (summary; full evidence in the task file)

1. **Quarantine cause = data, not code.** `wiki/PID_LOGSET_RESEARCH_PROMPT.md` L24-26 + audit Culprit 2: the
   >95% NO_FAULT came from a PID-less corpus, not a logic defect. `translate()` already emits a typed payload.
2. **Signatures now exist** to build PID-bearing fixtures — `research/chunks/*` + `formula-wiki/` + the J1979
   `research/obd2-pid-table-service-01.csv` (which also fixes Q3: STFT range −100…+99, ±127 = sentinel).
3. **Emitter is the architecture.** `KGtopic.md` division-of-labor: parsing labs emit "perceptions," COMLab
   judges. Inherited DEP-2/DEP-3 specs assume it.
4. **Standalone classification is conceded** — audit shows OBD-only family separation is data-limited and
   override is net-negative (App 4 −5). Validates T-OBDV2-PURGE-1.

## Consequences recorded in PROGRESS.md

- T-OBDV2-PURGE-1 / PURGE-2 → unblocked (`pending (runnable)`).
- T-OBDV2-ECU-PERCEPT-1 / BANK-ASYM-1 → no longer gated on T-OBDV2-0; remain research-gated on their Qs.
- Next runnable proof: **T-OBDV2-1 — PID-logset wiring gate** (to author next session).

## What revive does NOT yet prove

Revive is ratified **intent**. It becomes verified **capability** only when T-OBDV2-1 demonstrates the live
pipeline produces discriminating, non-`NO_FAULT` output on PID-bearing fixtures. Until then, no channel task
(ECU-PERCEPT, BANK-ASYM) should flip to `done`.
