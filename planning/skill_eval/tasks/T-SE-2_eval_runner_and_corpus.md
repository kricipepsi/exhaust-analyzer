# T-SE-2 — Eval runner + matched coding-task corpus

**Status:** authored · impl blocked · **Blocked by:** T-SE-0 · **Pack:** `planning/skill_eval/`
**Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `codingskills/ecc-subset/eval-harness`.

## Goal

Build the harness that runs a fixed coding-task corpus under the CONTRACT arms
(A baseline / B skill / C no-gate) and records the metric schema from T-SE-0. Wraps
the `eval-harness` skill's EDD/pass@k machinery — do not reinvent it.

## Deliverables

1. `corpus/` — **N ≥ 5** matched, representative coding tasks (CONTRACT §5). Each
   task: a self-contained prompt + a hidden oracle (hidden tests / expected behaviour)
   the runner scores against. Mix real (reuse small OBD/GAS coder tasks) + synthetic
   (a known-API and a trap-API task to exercise hallucination metric). Pin each task's
   difficulty + the claim-axes it can exercise.
2. `runner.py` — given (task, arm, skill, seed) → executes the arm, captures the
   T-SE-0 metric record, writes one JSON-lines row per trial. Arm C disables the gate.
3. A smoke run: 1 task × arms A/B × K=2, emitting valid metric rows (no real verdict yet).

## Success criteria

- Runner emits the full T-SE-0 metric schema; first-pass counts captured **before**
  any fix; tokens recorded.
- Arm C path provably skips the inner-loop gate (asserted in a test).
- Corpus tasks carry hidden oracles; a deliberately wrong solution scores as failing.
- `ruff`/`pyright`/`pytest -x -q` clean on the runner itself.

## Out of scope

Running the full N×K×arms matrix (that is the cohort tasks). Judging skills.

## Signal/noise consumer

`runner.py` output is consumed by T-SE-3..6 (cohort A/B) and aggregated by T-SE-FINAL.
Every emitted field traces to a metric in T-SE-0's schema; unused fields do not ship.

## Verification

Smoke JSON-lines validate against the schema; arm-C-skips-gate test passes; a planted
wrong solution is scored failing.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-2.md`, opening with `## Plan`.)
