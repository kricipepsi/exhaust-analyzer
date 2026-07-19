# T-FL-1 — Lock the true v2 baseline + freeze the v3 yardstick
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` (runnable now) · **Blocked by:** —
**Mode:** STRICT — measures + freezes a snapshot; **no engine/oracle/lab edits**. · **Scope owner:** wired-fl.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
"Did v3 improve for real?" is only answerable against a **trustworthy, frozen** current
number. The raw 48% is polluted by two surface defects (`fault_code` namespace,
`confidence` band — F-V7-CODE-NS/-CONF-SAT) and by oracle pins that may be wrong
(`mechanical_wear→misfire` etc.). This task produces the **honest current routing
accuracy** and **freezes the exact corpus+oracle** that v3 will be re-scored against, so
the before/after is apples-to-apples by construction.

## Signal/noise
Adds no domain field. The **named consumer** is T-FL-4 (the v3 scoreboard) and the v3
coders, who compare against this frozen yardstick. Nothing here is speculative — it is the
measurement anchor the rest of the pack and v3 depend on.

## Pinned facts (verified at authoring)
- v7 scorer `apps/wired/v7/run_suite.py` scores 6 dims; `fault_family` + `state` are the
  routing-truth dims and are **independent** of the two surface defects (V7_ACCURACY §4).
- Current v2 default run: `v7/runs/20260630_163900/` → family routing 141/294 = 48.0 %.
- Suspect oracle clusters (V7_ACCURACY §5): e.g. `mechanical_wear→misfire` (10), tagged
  *maybe oracle-correct, not engine-error* — must be adjudicated against the wiki, **read-only**.

## Success criteria (verify against these; loop until all hold)
1. Report a **primary metric = family+state routing accuracy** with the two surface dims
   (`fault_code` namespace, `confidence` band) **explicitly excluded and reported
   separately**, so routing signal is not masked. State the number and its denominator.
2. Adjudicate each **ORACLE_SUSPECT** cluster from V7_ACCURACY §5 against the lab wiki
   (read-only): for each, record *oracle-correct* (engine was right; oracle pin to be
   fixed in v3 corpus) or *engine-error* (genuine misroute). Produce both an **as-pinned**
   and an **adjudicated** routing number, with the delta and the per-cluster decisions.
3. **Freeze the yardstick:** copy the exact corpus + oracle + scorer version + run command
   into `apps/wired/fl_tasks/reports/FL_YARDSTICK_<date>.md` (content hash of the CSV, the
   scorer git sha / file hash, the env incl. `USE_V2_REGISTRY` default). v3 MUST be scored
   on this frozen artefact; any later corpus edit forks a new yardstick, never mutates this.
4. No engine, oracle CSV, wiki, or scorer file is modified (adjudication is recorded in the
   report only).

## Scope
**IN:** re-score the existing `20260630_163900` run (or re-run v2 for parity — state which)
on family+state; adjudicate ORACLE_SUSPECT clusters vs wiki; write
`FL_YARDSTICK_<date>.md` (frozen inputs + hashes + as-pinned vs adjudicated numbers + the
per-cluster decision table); log any oracle-pin corrections as `pending-for-v3` rows (not
applied).
**OUT:** editing the CSV/oracle/wiki/scorer/engine; tuning; `graphify`; `Vault/`; committing
run JSON.

## Gate (STRICT dual-gate → `progress_notes/T-FL-1.md`)
- **VERIFICATION GATE:** paste the as-pinned and adjudicated routing numbers, the ORACLE_SUSPECT
  decision table with wiki citations, and the yardstick hashes.
- **CODE REVIEW:** confirm zero source/oracle edits; the yardstick is a frozen copy, not a mutation.
