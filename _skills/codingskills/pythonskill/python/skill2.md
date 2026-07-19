# skill2.md — superseded 2026-05-07

This file's content has been merged into the canonical Python skill at
`SKILL.md` in this same directory.

**Do not load this file as a skill.** Open `SKILL.md` instead.

## What was merged in

- §1 "Strategic Planning — Contract-First" (signatures-first, library existence
  verification via `uv pip show` / `pip index versions`).
- §2 "Deterministic Validation Loop — Cheap-First" (syntax → ruff → bandit →
  type check, in that token-economical order).
- §3 "Iterative Refinement — Bounded" (5-iteration cap, 3–5 error messages per
  attempt, context isolation pattern).
- Bandit security gating note in §11 ("Security Essentials").
- `uv` preference and reproduce-first bug-fix rule in §13–§14.
- Research-cited framing throughout (20% library hallucination rate, 15–20×
  resolution-rate uplift from validation loops, 23–45% complex-task baseline,
  40%→13% bandit-gated CWE reduction).

The original prose of this file is preserved in git history; if you need to
review it, `git log -p` this path.
