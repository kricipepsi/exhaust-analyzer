# T-V3-D6 — progress note (abstain acceptance checkpoint)

**Task:** `T-V3-D6_abstain_acceptance_checkpoint.md` · **Status:** done · **Author:** Antigravity · **Date:** 2026-07-01
**Reports:** `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md`, `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.json`
**Script:** `v3/abstain_sweep.py`

## Plan

Perform measurement-only analysis of the T-V3-3C landing.
1. Run scoreboard diff and score commands to verify headline values (top3_family = 176, coverage = 0.37, total_abstained = 185, single_verdict = 81/294).
2. Confirm floor-inertness (no cases below 0.80 floor).
3. Compute family-aware abstain margin sweep for margins {0.05, 0.03, 0.02, 0.01, 0.00} and floor-only.
4. Construct Tier 1 (headline), Tier 2 (decision map), and Tier 3 (margin sweep table + JSON) and write to reports.

## Findings & Sweep Analysis

* **Floor-inertness:** The absolute confidence floor of 0.80 is 100% inert, firing on 0/294 cases. All engine verdicts have confidence >= 0.80.
* **Tension:** Margin-abstain conflicts directly with the top-3 verdict shape. At MARGIN=0.05, 88 of the 185 abstained cases are top-3 correct (hidden wins) and 97 are top-3 wrong (correct silences).
* **Sweep cliff:** A major cliff exists between 0.05 and 0.03/0.02. Relaxing the margin to 0.02 recovers 120 cases of coverage (raising coverage 0.37 -> 0.78), retrieving 61 hidden wins while only allowing 59 top-3 wrong cases.

## VERIFICATION GATE

```
VERIFICATION GATE — T-V3-D6
1. Compile : PASS  (v3/abstain_sweep.py)
2. Lint    : PASS  (ruff check -> OK)
3. Types   : PASS  (pyright -> 0 errors)
4. Tests   : PASS  (pytest -x -q apps/wired/tests/ -> 11 passed)
5. Contract: PASS  (rebound yardstick V3_YARDSTICK_2026-06-30 checked; headline top3_family 176/294, coverage 0.37, total_abstained 185, single_verdict 81/294 matched; floor-inertness confirmed; margin sweep completed and reports written)
6. Orphan  : N-A   (no new runtime fields or contracts introduced)
Result: CLEAN
```

## CODE REVIEW

```
CODE REVIEW — T-V3-D6
Scope         : PASS  (only created reports and read-only sweep script; no engine edits)
Composition   : PASS  (checkpoint-only, no cross-lab imports or legacy paths)
Consumers     : PASS  (consumed by owner decision and v3 acceptance gate)
Literals      : PASS  (margins and floor thresholds cited)
Docstrings    : PASS  (docstrings present in sweep script)
Craft (WARN)  : depth: sweep script is separate, clean, and read-only; deletion: no dead code; seam: no engine or scorer code touched; interface: reads public result files and expected families from petrol CSV
Result: CLEAN
```
