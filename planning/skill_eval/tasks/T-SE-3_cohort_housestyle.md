# T-SE-3 — Cohort A/B: house-style & craft (worked example)

**Status:** authored · impl blocked · **Blocked by:** T-SE-0, T-SE-1, T-SE-2 ·
**Pack:** `planning/skill_eval/` · **Mode:** STRICT
**Load skills (session start):** read `SKILL_EVAL_START_HERE.md`; sandbox Python 3.14;
mandatory pair + `eval-harness`. **Do not hand-load the skills under test** — the
runner's arm logic loads them (CONTRACT §2 / START_HERE §0).

This is the **template** the other cohort tasks (T-SE-4/5/6) clone. It is fully
worked so the pattern is unambiguous.

## Cohort under test

`python`, `uncle-bob-craft`, `improve-codebase-architecture` (the codingskills copy;
the top-level duplicate is `DEAD` per T-SE-1). All three claim **gate-invisible**
quality (structure, naming, cohesion) ± anti-hallucination (`python`).

## Method (per skill in the cohort)

Run the T-SE-2 corpus, arms **A (baseline)** vs **B (skill)**, **K ≥ 3** trials each.
Primary metrics (CONTRACT §3): blinded rubric score (metric 5) + complexity proxy;
for `python` additionally first-pass counts (1) and hallucinated-API count (4).
Arm C is **not** used here (no gate overlap).

## Deliverables

1. `results/cohort_housestyle.jsonl` — every trial's metric record.
2. `cohort_housestyle_report.md` — per skill: mean±SD on each primary metric, the
   effect `mean(B)−mean(A)`, whether it clears the §5 bar, and the verdict
   (`KEEP`/`TRIM`/`CUT`) with the evidence line.

## Success criteria

- K ≥ 3 trials per arm per skill; rubric scoring blinded (arm labels stripped).
- Each verdict states the effect size **and** the variance it must beat; sub-variance
  effects are reported `null`, not rounded up to a win.
- Verdicts written back to the ledger's per-skill table.

## Out of scope

Other cohorts; deleting skills; changing the rubric (frozen in T-SE-0).

## Signal/noise consumer

Verdicts feed T-SE-FINAL's KEEP/TRIM/CUT table and the recommended default load-set.

## Verification

Re-score one artefact blind and reproduce its axis scores within the K-pass SD;
recompute one effect-vs-bar decision by hand.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-SE-3.md`, opening with `## Plan`.)
