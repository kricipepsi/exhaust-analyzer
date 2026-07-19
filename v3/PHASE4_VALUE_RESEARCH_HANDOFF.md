# v3 Phase-4 — Continue-After-Value-Research Handoff (start here in the fresh session)
**Date:** 2026-07-01 · **Author:** architect (Cowork) · **Owner:** Mutolovsky
**Read order:** `v3/V3_START_HERE.md` → `v3/CLAUDE.md` → `v3/PHASE4_HANDOFF.md` → **this file**.
One job this session: **land the value-confirmation research, reconcile the synthetic bands, then run the C2 signal pack.**

## 1. Where we are (measured)
- `top3_family` **197/294** (post `T-V3-D6-SCORERWIN` distinct-family fix). Yardstick `V3_YARDSTICK_2026-07-01`; latest run `POST_T_V3_3D`; `run_suite.py` frozen.
- **Canon reversed (owner):** synthetic sensor values are now **allowed pre-launch** — grounded in each case's oracle fault + research band, **web/authoritative-corroborated**, **tolerance-wide**, `synthetic=true`-flagged, calibrated on real data later. Full policy: `4DLab_CLAUDE.md` §Provisional synthetic signals. State tolerance width on every task.
- **Done:** P4-1 (acquisition spec) · P4-2 (min-signal-set, corrected order C2 22 / C3 21 / C6 14 / C9 11 / C4 11 / C5 10 / C8 6 / C1 5 / C7 3) · C2-PRE (reveal contract) · C2-SYNTH (C2 seed drafted from quick web). D6-SCORERWIN done.

## 2. What is out for research (the thing this session waits on)
9 per-cluster **value-confirmation prompts**: `v3/research/value_prompts/CLUSTER{1..9}_value_prompt.md` (+ README). Each asks values-only (range · fleet spread · distribution · CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT), grounded in `research_answers/clusterN.md`. Hand each separately; **do NOT** attach `00_4DLAB_CONTEXT.md` (that's for the discriminating-measurement research, not value confirmation).
**Answers land as:** `v3/research/research_answers/clusterN_values.md`.

## 3. Continue here (runnable order once C2 answers land)
1. **Reconcile C2 bands.** Diff `research_answers/cluster2_values.md` verdicts against the drafted bands in `v3/reports/V3_C2_SYNTH_BANDS_2026-07-01.md`. Apply WIDEN/SHIFT/TIGHTEN/REJECT; re-run `v3/gen_c2_synth_seed.py` → updated `v3/data/c2_synthetic_seed_2026-07-01.*`. (Keep `synthetic=true`; no back-solve.)
2. **`T-V3-P4-C2A`** (authored, runnable) — read-only dry-run: simulate C2 producer+consumer on the reconciled seed; predict which of the 22 flip to top-3 + FT-8 (33-neighbour) regressions. No live edit, no mint.
3. **`T-V3-P4-C2B`** (forward-registered; author in full after C2A) — COMMIT: write the C2 column into the live corpus, wire producer into live GASLab/OBDLab, adjust RM/CF consumer rules, re-score, **mint a new yardstick** (corpus changed; mint pattern = `T-V3-2R`/oracle-repin; `run_suite.py` untouched). Gate: C2A + owner sign-off + FT-8 clean. Report synthetic-driven passes in the **synthetic-vs-real split** (CODE_LANDED ≠ SCORE_MOVED).
4. **Then other clusters** in P4-2 order (C3→C6→C9→…): each is SYNTH(seed from its `clusterN_values.md`) → C*A dry-run → C*B commit. `CASE-039` rides with C3.

## 4. Guardrails (unchanged, still binding)
`run_suite.py` frozen (never edit); any corpus/oracle change mints a new yardstick, never overwrite a frozen one. Never `Vault/`. No `graphify`/frozen-graph rebuild. No secrets. Git = owner's final commit by explicit path only. Cases the research can't ground stay **abstained**, never guessed.

## 5. Pointers
- Ledger (status + forward-registered): `v3/V3_PROGRESS.md` (runnable-guard = first `pending` row whose blockers are all `done`).
- Reveal contract (how a pack discloses): `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md`.
- Acquisition + ordering: `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.*`, `V3_MIN_SIGNAL_SET_2026-07-01.*`.
- Scoreboard: `apps/wired/fl_tasks/score_v3_yardstick.py` (`score`/`diff`; denom 294). Engine: `labs/comlab/comlab/core/fault_atlas_router.py`; rules `labs/comlab/registry/rules/*.json`.
**Bottom line:** research confirms the numbers → reconcile C2 bands → C2A → C2B (first real signal pack, mints a yardstick) → repeat per cluster. Everything is grounded + tolerance-wide + labelled; calibrate on real user data after launch.
