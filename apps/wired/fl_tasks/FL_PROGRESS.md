# wired-fl — Failure-Localization Pack (Progress Ledger)
**Pack goal:** build the instrument that **pinpoints the exact failure point of every
failing v7 case** — the pipeline stage where it first diverges and the failure *mode* —
and a **frozen before/after yardstick** so the planned **v3** rebuild can be judged on
*real* per-family / per-mode movement, not another incomparable headline number.
**Premise (proven, see `v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md`):** the
~50% ceiling is a **producer/discrimination** limit, not coverage. The dead families
(`mechanical_wear` 0/14, `exhaust_leak` 0/10, `non_starter` 0/5, `ecu_fault` 4/31) fail
because the upstream labs cannot emit a *distinct* state from a single warm-idle 5-gas
snapshot + sparse DTC, so the correct rule is pruned on GATING or outranked by a louder
family (e.g. misfire on `P0300`+high-HC). This pack makes that attribution **per case,
mechanically**, so v3 targets the right layer.
**Tasks dir:** `apps/wired/fl_tasks/` · **Reuses:** v7 corpus/oracle/driver
(`apps/wired/v7/`), the trace tooling (`apps/wired/trace/`, T-V7-6), and the v7 follow-up
dispositions (T-V7-7/8).
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW). **Read-only on engine** —
this pack measures and localizes; it does **not** fix the engine (that is v3).
**Reads on boot:** `apps/wired/fl_tasks/WIRED_FL_START_HERE.md`
**Last updated:** 2026-06-30 (Codex — T-FL-4 v3 scoreboard; pack complete)
Keep under ~120 lines; bulk gate notes go in `fl_tasks/progress_notes/<id>.md`.
---
## Pre-pack gate
| Item | State | Evidence |
|---|---|---|
| v7 suite runs full corpus, 0 crashes | **done** | `v7_tasks/reports/V7_ACCURACY_2026-06-30.md` (314/314) |
| failure mechanism root-caused at row level | **done** | `v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md` |
| trace pass authored (prune/rank spans) | **authored** | `v7_tasks/T-V7-6_jaeger_full_corpus_trace.md` |
| two P0 surface defects dispositioned | **investigating** | `v7_tasks/T-V7-7` (code-ns), `T-V7-8` (confidence) |
## Task log
| ID | Task file | Status | Blocked by | Date | Verification | Notes |
|---|---|---|---|---|---|---|
| T-FL-1 | `T-FL-1_lock_true_baseline.md` | done | — | 2026-06-30 | `reports/FL_YARDSTICK_2026-06-30.md`; `progress_notes/T-FL-1.md` | Frozen yardstick: as-pinned family+state 133/294 = 45.24%; adjudicated 143/294 = 48.64%; `mechanical_wear→misfire` 10 marked pending-for-v3 oracle correction. |
| T-FL-2 | `T-FL-2_capture_upstream_evidence.md` | done | — | 2026-06-30 | `reports/FL_UPSTREAM_2026-06-30.md`; `reports/FL_UPSTREAM_2026-06-30.json`; `progress_notes/T-FL-2.md` | Captured per-case GASLab chemistry + OBDLab O2 mode/status for 314/314 rows; live prune-span spot checks recorded for 3 dead-family cases; dead-family emitted-vs-required table ready for T-FL-3. |
| T-FL-3 | `T-FL-3_classify_failure_modes.md` | done | T-V7-6, T-FL-2 | 2026-06-30 | `reports/FL_LOCALIZATION_2026-06-30.md`; `progress_notes/T-FL-3.md` | Classified 294/294 accuracy cases with cited span/field evidence: SURFACE_DEFECT 133, OUTRANKED 107, PRODUCER_GAP 25, DATA_GAP 19, ORACLE_SUSPECT 10, PRUNED_OTHER 0. Dead-family calls: mechanical_wear oracle-suspect/product-definition, exhaust_leak outranked at rank, non_starter producer-gap dominant. |
| T-FL-4 | `T-FL-4_v3_scoreboard.md` | done | T-FL-1, T-FL-3 | 2026-06-30 | `score_v3_yardstick.py`; `reports/FL_SCOREBOARD_README_2026-06-30.md`; `progress_notes/T-FL-4.md` | One-command before/after harness bound to `FL_YARDSTICK`: live current engine reproduces 133/294 = 45.24%; self-compare all-zero; hash mismatch refuses. v3 entry point: build against `FL_LOCALIZATION`, judge against this scoreboard. |
**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Runnability:** guard takes the first `pending` row whose `Blocked by` are all `done`.
T-FL-1, T-FL-2, T-FL-3, and T-FL-4 are done. The failure-localization pack is complete:
v3 is built against `FL_LOCALIZATION` and judged by `score_v3_yardstick.py` against `FL_YARDSTICK`.
---
## Failure-mode taxonomy (the classification T-FL-3 assigns)
| Mode | Meaning | Fix layer (for v3) |
|---|---|---|
| `PRODUCER_GAP` | correct family's rule pruned because the upstream lab never emitted the GATING state it needs | GASLab/OBDLab classifier or the input signal |
| `PRUNED_OTHER` | correct rule pruned for a non-producer reason (bad gate, contract) | rule/contract |
| `OUTRANKED` | correct rule fired but lost the score; record the winner + deciding evidence | rank weights / evidence (audit: tuning ties regresses neighbours) |
| `DATA_GAP` | discriminating signal absent from the inputs entirely (e.g. OBDLab NO_FAULT) | data acquisition / scope |
| `ORACLE_SUSPECT` | engine's answer may be domain-correct; the oracle pin is questionable | oracle correction (not engine) |
| `SURFACE_DEFECT` | failed only on `fault_code` namespace or `confidence` band (F-V7-CODE-NS / -CONF-SAT) | engine surface (T-V7-7/8), not routing |
---
## Unplanned follow-ups
| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| FL-V3-ORACLE-MW-MISFIRE | T-FL-1 | Revisit 10 `mechanical_wear→misfire` rows: repin to misfire for single-snapshot yardstick or add mechanical discriminator before scoring as mechanical_wear. | pending-for-v3 |
---
## Architect-level out-of-band patches
| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-30 | `apps/wired/fl_tasks/**` | Authored the failure-localization pack (ledger + START_HERE + T-FL-1..4) after the rebuild-failure audit. | Owner directive: build a test pack that pinpoints exact failure points, to target a real v3 and measure honest before/after. |
