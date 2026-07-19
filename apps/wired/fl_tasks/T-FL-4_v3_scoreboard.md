# T-FL-4 — v3 scoreboard: one-command before/after on the frozen yardstick
**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` · **Blocked by:** T-FL-1, T-FL-3
**Mode:** STRICT — adds a repeatable harness; **no engine/oracle edits**. · **Scope owner:** wired-fl.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Why this task exists
The owner's end goal: when v3 is built, know **for real** whether accuracy improved or hit
the same wall — per family and per failure mode, not as another incomparable headline. This
task delivers the **single command** that re-scores any engine build against the **frozen
T-FL-1 yardstick** and prints the delta, classified by the T-FL-3 modes. Without it, "v3 is
better" is an assertion; with it, it is a diff.

## Signal/noise
Adds no domain field. The **named consumer** is the owner / v3 reviewer at v3 acceptance
time. The harness exists to make the v2→v3 comparison mechanical and honest — and to make a
**null result legible** ("v3 moved PRODUCER_GAP by +X, OUTRANKED by 0" tells you exactly
whether the rebuild touched the real constraint).

## Pinned facts (verified at authoring)
- Yardstick (corpus+oracle+scorer+env, hashed) is frozen by T-FL-1 (`FL_YARDSTICK_<date>.md`).
- Failure modes + per-case attribution come from T-FL-3 (`FL_LOCALIZATION_<date>.md`).
- The engine under test is selected by env (`USE_V2_REGISTRY`) / the installed `wired`
  package — the harness must record exactly which build it scored (git sha + env).

## Success criteria (verify against these; loop until all hold)
1. One command runs the frozen yardstick against the **current** engine and prints:
   overall family+state routing %, **per-family** %, and **per-failure-mode** counts —
   reproducing the T-FL-1 baseline numbers exactly (proves the harness is faithful before
   it is ever used on v3).
2. The same command takes a **second** result set (a future v3 run) and prints a **delta
   table**: per-family Δ and per-mode Δ (e.g. `PRODUCER_GAP 70→40`, `OUTRANKED 60→58`),
   plus overall Δ — with the build identity (git sha + env) of each side recorded.
3. The comparison is **locked to the frozen yardstick** — the harness refuses to score if
   the corpus/oracle/scorer hash differs from the T-FL-1 freeze (guards against moving the
   goalposts mid-comparison). Document the override path (a new yardstick, explicitly named).
4. A short `apps/wired/fl_tasks/reports/FL_SCOREBOARD_README_<date>.md` documents the
   command, the yardstick it is bound to, and how to read a null result honestly.
5. Self-comparison sanity: scoring the baseline against itself yields all-zero deltas.

## Scope
**IN:** the scoreboard harness under `apps/wired/fl_tasks/` (re-uses the v7 scorer + T-FL-3
classifier, does not reimplement them); the README; the hash-lock guard.
**OUT:** building v3; editing engine/oracle/scorer; tuning; `graphify`; `Vault/`; committing
run JSON. **The harness must not embed any v3 expectation** — it scores whatever engine is
installed, neutrally.

## Gate (STRICT dual-gate → `progress_notes/T-FL-4.md`)
- **VERIFICATION GATE:** paste the baseline-reproduction output (matches T-FL-1), a
  self-comparison all-zero-delta run, and a hash-lock-refusal demonstration.
- **CODE REVIEW:** confirm zero source edits; harness reuses (not forks) the scorer/classifier;
  no v3 assumption baked in.

## Pack close-out (this task also)
On accept, update `FL_PROGRESS.md` (mark the pack `done`), cross-link the four FL reports
from `V7_PROGRESS.md`, and record the SUGGESTED v3 entry point: **v3 is built against
`FL_LOCALIZATION` (target list) and judged by this scoreboard against `FL_YARDSTICK`.**
