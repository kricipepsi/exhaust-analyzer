# SHIP AUDIT — 4DApp final pre-publish audit
**Authored:** 2026-07-07 (architect, Cowork). **Scope:** all `labs/*` ledgers, registry,
`apps/wired` (+v7/fl/test packs), `v3/` pack, `apps/ui`, root harness, working tree.
**Question answered:** are all tasks done, and is the app ready to publish?

---

## Verdict: NOT ready to publish — 4 blockers, 1 owner ritual

Engine work is genuinely complete (v3 pack closed under the owner stop ruling at
**top3_family 269/294 = 91.50%**, top3_on_covered 93.52%, 0 regressions, yardstick
`V3_YARDSTICK_2026-07-06-C9B`, commit `d2b7350`). What blocks publishing is not the
engine — it is the surface, the verification staleness, and two honesty/coverage debts.

| # | Blocker | Why it blocks | Resolution |
|---|---|---|---|
| B-1 | **No user-facing app exists.** `apps/ui` is design docs only; the old Streamlit app is archived (`ARCHIVE/4DLabWired/app.py`); vault-live notes confirm UI consumers point at deleted `apps/wiredV2/`. Wired exposes only `run_case.py` (a command-line runner). | Nothing for a user to open. Owner ruling 2026-07-07: publishing = end-user UI, same look as the old UI, populated with all fields. | `T-SHIP-UI-1` → `T-SHIP-UI-2` |
| B-2 | **Full-suite verification is stale.** Last full cross-lab green: 1991 tests, 2026-06-30. Since then 7 signal packs (C2B..C9B) edited `labs/comlab` schemas + registry shim + wired composition + corpus; each ran only its own gates + `apps/wired/v7/tests` (48). | Shipping on a 7-day-old full-suite result after schema-touching commits is unverified. | `T-SHIP-1` |
| B-3 | **Scoreboard has no synthetic-vs-real split.** Canon (`4DLab_CLAUDE.md`, Provisional synthetic signals, point 3) requires the scoreboard to keep the split so no metric is mistaken for field accuracy. ~90 corpus rows now carry `synthetic=true`-seeded columns (C2 22, C3 22, C6 14, C5 10, C4 11, C9 11); `score_v3_yardstick.py` reports one undifferentiated number. The published 91.50% is research-consistent-input performance, not field accuracy. | Publishing the headline number without the split violates the policy the seeding was allowed under. | `T-SHIP-1` (disclose) → `T-SHIP-2` (commit) |
| B-4 | **VIN brand join drops ~11.6% of petrol traffic.** `planning/AUDIT_2026-07-06_vin_engine_number.md` §6: blank-brand WMIs (TMB, VSS, TSM, UU1, TMA, NLH — Škoda also mojibake `�KODA` on the map side) are dead on both join sides; +1.1% WMIs absent entirely. ENG-1/ENG-2 fixed the engine map/join but not this. | 1 in 8 real VINs gets no brand → degraded DNA at first contact with real users. | `T-SHIP-3` |
| R-1 | **Owner commit ritual pending.** ~900 uncommitted paths (root doc deletions/moves, `docs/Vocabulary/` relocation, graph caches, ledger edits). Git is owner-run, by explicit path — flagged only. | A published app must build from a committed tree. | `T-SHIP-5` (owner-delegated 2026-07-07) |

## Ledger sweep result (all packs)

**Complete (all rows `done`):** gaslab T-GV2 (Stage 1) · obdlab T-OBDV2 (Stage 2) ·
dtclab T-DTCV2 (Stage 3) · comlab Stage-4 fusion consumers (all 20+ rows incl.
DELTA 1A-1D/2, LAMBDAPROJ-1, FATAL-1) · COMTST 1-4 · registry (REVIVE-1, AUTHOR-ignition_fault,
CHEMSIG-34 landed with T-GV2-2 2026-06-28) · semantic T-SEM-1..5 · dnalab/symptomlab/vinlab
T-DNA rows · wired T-WIRE-1..4 · wired-test T-WTEST-1..5 · wired-v7 T-V7-1..9 ·
wired-fl T-FL-1..4 · **v3 pack closed** (C8/C1/C7 tail CLOSED by owner stop ruling 2026-07-06) ·
vinlab ENG-1/ENG-2 (2026-07-06).

**Open, dispositioned in the ship pack (hygiene / owner decisions):**
- **Stale ledgers:** root `harness/` T-TH pack (blocked/pending since 06-05, superseded by the
  wired v7 harness) · gaslab `T-MIG-5`/F-9 · comlab `T-RMW-MIRROR` (stale: audit verified the
  COMLab mirror is 34-value and `WRONG_VALVE_TIMING` is gone from live code) → `T-SHIP-4` closes
  the rows with evidence instead of leaving lying ledgers.
- **Owner rulings queued:** rings/PCV HC-direction (two known-wrong routes ship otherwise:
  MW-001→CF-001, MW-008→SF-001, per `RINGS_PCV_TRIAGE_RULING.md`) → `D-SHIP-1`. Q-C5-EGR
  wiki-vs-cluster conflict (HOLD per DECISIONS 2026-07-06, needs authenticated firecrawl pass)
  → `D-SHIP-2`.
- **Post-launch backlog (registered, not specced):** registry coverage gaps (case_046 P0190,
  EXP-N023, charging P0620-P0626 wiki+rule, CS-002 router-assumption assert — folded into
  T-SHIP-1's verification), `T-COM-CAMTIMING-MAF-1`, FU-2 doc-sync (§17 32→34 — folded into
  T-SHIP-4), 4 deferred gas-delta columns, abstain-cal (parked, MARGIN=0.02), masked tally 19,
  CASE-022 covered-wrong (needs C6 sensor-dynamics data), graph-lane items (GRAPH-TRUST,
  T-VLIVE-3c — dev tooling, off the runtime path).

## Accepted-as-is at publish (owner rulings already on record)
- 89.72%→93.52% on covered accepted; no chasing/tightening (stop ruling 2026-07-06).
- Coverage 0.73 — 78 cases abstain by design; UI must render abstain honestly.
- Synthetic-seeded columns stay until real user data lands (correctable, flagged).

**Pack:** `apps/wired/ship_tasks/SHIP_START_HERE.md` · ledger `SHIP_PROGRESS.md`.
