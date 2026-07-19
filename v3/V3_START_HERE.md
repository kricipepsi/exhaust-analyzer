# 4DLab v3 — START HERE (top-3 differential rebuild bootstrap)

Paste this as message 1 of a fresh coder session. This file is a **procedure**, not
documentation — execute it before any other output.

## What this pack is
Rebuild the wired engine's verdict from a single forced guess into a **ranked top-3
differential + abstain**, and close the residual gap with new input signals, until the
correct fault family is in the top-3 **>= 95%** of cases. The full spec is
`v3/V3_PLAN.md`. The owner's direction (2026-06-30): top-3 + abstain, the ranker is the
known problem, new signals are in scope for the cases a single idle snapshot can't separate.

## Boot (every session)
1. Read `v3/V3_PROGRESS.md` (ledger) — take the **first `pending` row whose `Blocked by`
   are all `done`**. That is your task. One task per session.
2. Read the named task spec `v3/v3_tasks/T-V3-<n>_*.md` in full. **It is the spec** — read
   only what it pins (READ-NARROW; do not whole-read large reports/wikis/modules).
3. Read the mandatory skills from the existing wired bundle:
   `apps/wired/_wired_skills/_INDEX.md` -> wired-python, wired-verification-loop,
   wired-code-review (+ any on-demand skill the task's `Load skills:` line names).
4. Load-bearing context, opened **narrow** (by line range the task pins):
   - `v3/V3_PLAN.md` sections 1-4 (the failure-mode buckets and the phase the task serves).
   - `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md` (per-case mode + stage).
   - `apps/wired/fl_tasks/reports/FL_YARDSTICK_2026-06-30.md` (the frozen BEFORE + hashes).
   - The scoreboard `apps/wired/fl_tasks/score_v3_yardstick.py` and the scorer
     `apps/wired/v7/run_suite.py::score_case`.
5. Post a one-paragraph scope confirmation (which task, what you will touch, what you will
   NOT touch) **before** any code.

## Hard rules (this pack)
- **The frozen yardstick is immutable.** `FL_YARDSTICK_2026-06-30` (corpus + oracle + scorer
  hashes) is the historical BEFORE. Any oracle/corpus edit **mints a new yardstick file**
  (`V3_YARDSTICK`); it never overwrites the frozen one. The scoreboard refuses on hash
  mismatch — that is by design.
- **Top-3 reframe before rank-tuning.** Recover OUTRANKED cases by *surfacing* the runner-ups
  the ranker already computes (`fault_atlas_router.py` `runner_ups`/`differential_siblings`),
  **not** by re-weighting scores. Any rank-weight change must run the full corpus and show
  **no regressed family** (audit FT-8: tuning ties regresses neighbours).
- **No new signal without a producer AND a consumer.** A new field/state ships only with a
  named GASLab/OBDLab producer and a named rule consumer (signal/noise rule). Sensor values may be
  **synthesized provisionally** pre-launch — grounded in the case's oracle fault + research band,
  tolerance-wide, `synthetic=true`-flagged, calibrated on real data (`4DLab_CLAUDE.md` §Provisional
  synthetic signals). Cases the research cannot ground stay abstained.
- **No `Vault/` edits, no `graphify` / frozen-graph rebuild, no secrets.** Edit live
  `labs/<lab>/`. (Workspace canon — `/agent_workspace/4DLab_CLAUDE.md`.)
- Run/trace JSON stays untracked (git-excluded), like the v7/FL runs.
- **Disclosure-first pack (progressive disclosure).** Tasks are ordered so each
  *reveals* what the next decision needs before any task *commits* to it; a task
  that would both disclose and commit is split (the commit is a separate `Blocked
  by` task). The owner runs step-by-step: one live authored task at a time, the
  rest forward-registered. Surface shortfalls, don't hide them. (Authoring
  mechanics: `_skills/coding-bootstrap/SKILL.md`.)

## Pack map
| Task | Does | Blocked by |
|---|---|---|
| T-V3-0 | measure real correct-in-top-3 rate from the frozen trace; set target + abstain thresholds | — |
| T-V3-1 | top-3 + abstain scorer; mint V3_YARDSTICK; keep frozen BEFORE | T-V3-0 |
| T-V3-2 | re-pin oracle (Option B) — recovers 133 SURFACE_DEFECT, zero engine change | — |
| T-V3-3 | engine surfaces the ranked differential + `fault_family` on siblings (**disclosure step** — reveals true top3_family) | T-V3-1 |
| T-V3-D5 | tiered acceptance checkpoint / next-decision map | T-V3-3 |
| T-V3-3B | emit verdict abstain (floor/margin) — **deferred behind the T-V3-D5 disclosure** | T-V3-D5 |
| T-V3-4+ | rank-recovery (TUNABLE) + Phase-4 new-signal packs (research / owner-data-gated) | research answers / owner signal data |
| T-V3-P4-C*-PRE/SYNTH/A/B | per-cluster signal packs (C2 done; **C3 live now**; pinned order C3→C6→C5→C4→C9→C8→C1→C7). Load skills: **wired-signal-pack** | prior stage of the same pack |

## Definition of done (pack)
The acceptance command
`/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score`
reports, against the v3 yardstick: `top3_on_covered >= 95%` at the coverage floor T-V3-0
sets, **no family regressed** on the single-verdict number vs the frozen 45.24%, and the
residual misses are only PRODUCER_GAP/DATA_GAP — **abstained, not mis-answered**.

## Session-end gate (STRICT — both blocks clean before a task flips to `done`)
1. `VERIFICATION GATE` (from wired-verification-loop) — in `v3_tasks/progress_notes/<id>.md`.
2. `CODE REVIEW` (from wired-code-review, incl. the structural-craft WARNING axis) — same file.
Update the `V3_PROGRESS.md` row, then stop. The **owner** runs the final commit by explicit path.
