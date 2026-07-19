# HANDOFF — wired accuracy / failure-localization → v3 (next session)
**Date:** 2026-06-30 · **Author:** architect (Cowork) · **For:** the next architect session (and coder packs it dispatches)
**One-line state:** the v2 rebuild did **not** move accuracy (~48%); root cause is **proven** to be a
producer/discrimination limit, not code; the **failure-localization (FL) pack** is authored to
pinpoint every failure point and freeze a yardstick before any **v3** build begins.

---

## 1. Why we are here (the finding that drives everything)
The ~50% ceiling is **not** a coverage or code problem — it is a **producer/discrimination** limit.
The dead families fail because the upstream labs can't emit a *distinct* state from a single
warm-idle 5-gas snapshot + sparse DTC, so the correct rule is **pruned on GATING** or **outranked**
by a louder family (misfire wins on `P0300`+high-HC). New rules/wikis/oracle/scope work can't move a
limit that lives in the **measurement**. Full evidence (row-level, verified vs inferred):
`apps/wired/v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md`.
This reproduces the June-3 audit `…/migration/docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT…md`
("next gains are a research/data problem"), now confirmed on the rows.

## 2. The honest current number (frozen yardstick)
From **T-FL-1** (`apps/wired/fl_tasks/reports/FL_YARDSTICK_2026-06-30.md`):
- family+state routing **as-pinned: 133/294 = 45.24%**; **adjudicated: 143/294 = 48.64%**.
- 10 `mechanical_wear→misfire` rows flagged **pending-for-v3** oracle correction
  (`FL-V3-ORACLE-MW-MISFIRE`) — do not score them as engine error.
- The corpus+oracle+scorer are **hash-frozen**; v3 is measured against this exact artefact.
This (not 48.0% conjunctive, not the incomparable v1 "51%") is the v3 before-number.

## 3. State by pack
**wired-test** (`apps/wired/test_tasks/`) — **DONE & verified.** T-WTEST-1..5 all done; the Jaeger
trace path really ran (trace JSON on disk, `trace/runs/WTEST5_20260630/`). No action.

**wired-v7** (`apps/wired/v7_tasks/`) — T-V7-1..5 **done**. Open (all **pending/runnable**):
- **T-V7-6** full-corpus Jaeger `--trace` (needs the T-WTEST-3 collector up). *Unblocks T-FL-3.*
- **T-V7-7** READ-ONLY: decide canonical `fault_code` (engine ERR- vs oracle short). Memo only.
- **T-V7-8** READ-ONLY: decide `confidence_score` semantics (engine recalibrate vs oracle reband).
- **T-V7-9** v1 baseline via `USE_V2_REGISTRY=0` + fidelity diff vs `/home/m/Desktop/4dV1/registry/`.

**wired-fl** (`apps/wired/fl_tasks/`) — the instrument for v3:
- **T-FL-1 DONE** (yardstick frozen, §2).
- **T-FL-2 pending/runnable** — capture per-case GASLab chemistry + OBDLab mode (read-only). *Unblocks T-FL-3.*
- **T-FL-3 blocked** by T-V7-6 + T-FL-2 — the headline: classify every failing case into a mode
  (`PRODUCER_GAP`/`PRUNED_OTHER`/`OUTRANKED`/`DATA_GAP`/`ORACLE_SUSPECT`/`SURFACE_DEFECT`) + stage of
  first divergence; per-family×per-mode matrix = **the v3 target list**.
- **T-FL-4 blocked** by T-FL-1 + T-FL-3 — one-command before/after scoreboard on the frozen yardstick.

## 4. Do next session (exact, ordered)
Two are runnable immediately and **independent — split across the two coders, no edit race**:
1. **T-FL-2** (coder A) — `apps/wired/fl_tasks/`, capture upstream states. Critical path.
2. **T-V7-6** (coder B) — bring up the native Jaeger collector, trace the full corpus. Critical path.
Then, once both are `done`:
3. **T-FL-3** — produce the per-case failure-point map + per-mode matrix (the deliverable the owner asked for).
4. **T-FL-4** — wire the scoreboard.
Fill spare coder slots with the read-only memos **T-V7-7** and **T-V7-8** (they de-pollute the
routing number and feed the `SURFACE_DEFECT` bucket). **T-V7-9** when owner wants the v1 delta.

Bootstrap each coder session with the matching START_HERE as message 1:
`apps/wired/fl_tasks/WIRED_FL_START_HERE.md` or `apps/wired/v7_tasks/WIRED_V7_START_HERE.md`.
Assignments (SUGGESTED blocks, owner activates): `.agent/assignments.md`.

## 5. The hard rule
**Do not start v3 until T-FL-3 lands the target list.** v3 is then BUILT against
`FL_LOCALIZATION_<date>.md` (which modes dominate decides what v3 touches — GASLab classifier,
rank weights, corpus, or input modality) and JUDGED by the T-FL-4 scoreboard against the frozen
yardstick. No engine edits in any v7/FL task — those packs measure only.

## 6. Owner decisions still open
- **v3 direction** (from the audit §7): **B** narrow scope + abstain on indistinguishable families ·
  **C** add a discriminating signal (snap-throttle/transient gas, real trims — data/protocol, not code) ·
  **D** ship a ranked top-3 differential. Pick after T-FL-3 shows the mode mix. Engine tuning is **not**
  an option (FT-8: tuning ties regresses neighbours).
- **T-V7-7 / T-V7-8** P0 dispositions (owner chose *investigate first* — memos pending).
- **T-V7-9** v1-baseline path (toggle proxy authored; "build true-v1 harness over 4dV1" held in reserve
  if the Step-0 fidelity diff comes back low).

## 7. Artefact index
- Failure mechanism: `v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md`
- Accuracy + taxonomy: `v7_tasks/reports/V7_ACCURACY_2026-06-30.md`
- Frozen yardstick: `fl_tasks/reports/FL_YARDSTICK_2026-06-30.md`
- Ledgers: `fl_tasks/FL_PROGRESS.md`, `v7_tasks/V7_PROGRESS.md`, `test_tasks/TEST_PROGRESS.md`
- Full v1 system (read-only): `/home/m/Desktop/4dV1/` · June-3 audit: `…/migration/docs/reference/audit_2026-06-03/`
