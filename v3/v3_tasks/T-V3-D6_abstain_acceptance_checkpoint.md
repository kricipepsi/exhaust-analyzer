### Goal ###
Turn the T-V3-3C landing into the abstain pack's **disclosure keystone**: a tiered report that (a)
confirms the family-aware margin recovered coverage without moving `top3_family`, and (b) lays out the
**next-decision map** for the abstain dial so the owner picks the commit from evidence.
Measurement-only — no engine/schema/oracle/CSV edits. Uses `score_v3_yardstick.py score`/`diff` and a
read-only threshold sweep over existing run results.

> **Bound to the T-V3-3C disclosure (2026-07-01).** Headline numbers below are measured
> (`progress_notes/T-V3-3C.md`). Reproduce them, then write them up in tiers + produce the sweep.

### Progressive-disclosure role — the keystone ###
Essential-first, three tiers, so the owner reads one line and drills only if a number surprises.
- **Tier 1 — headline (<=3 lines).** `coverage 0.10 -> 0.37` (109/294 covered), `total_abstained
  264 -> 185`, `top3_family` **176/294 unchanged**, `63` unnecessary abstentions recovered. One-word
  verdict: **improved, not settled** — the dial still hides top3-correct answers.
- **Tier 2 — decision map (the menu).** One row per option with gate/risk:

  | Option | What it buys | Gate / Risk |
  |---|---|---|
  | Retune margin down (T-V3-3D-ABSTAIN-CAL) | sweep shows a **cliff**: relaxing MARGIN 0.05->~0.02 roughly doubles coverage. Pick the point that keeps abstentions mostly-wrong. | owner picks operating point from the sweep; changes the honesty dial's aggressiveness (not the acceptance metric). |
  | Redefine abstain for a top-3 product | margin-abstain **fights the top-3 reframe**: it silences cases where the correct family is already in the shown differential. Option: abstain on floor only / on genuine cross-family low-confidence only; let the differential communicate ties. | owner **definition** decision — what "decline to answer" means when the UI already shows 3 ranked causes. |
  | Fix floor inertness | **floor never fires (0/297 < 0.80).** The engine is ≥0.80 confident even when wrong, so absolute-confidence abstain is inert; only margin works. Recalibrating confidence would make floor meaningful. | larger change, likely score-calibration/research-adjacent; do not fold into a threshold tweak. |
  | Genuine exact ties -> T-V3-4 | ~67 cases tie exactly across families even after family-aware margin — the true ranker ambiguity. | research-gated (cluster answers) + FT-8 risk. |
  | Same-family residual / dedupe | residual same-family sibling artifacts (cf. SCORER_WINDOW `EXP-N010`,`era3_008`). | owner decision; small; merges with T-V3-D6-SCORERWIN. |

- **Tier 3 — per-case + sweep (JSON + table).** The `diff` movement table, the per-abstained-case
  right/wrong split, and the **margin sweep** (below) live in `.json`; Tier 1/2 stay scannable.

### Success criteria ###
- Score POST_T_V3_3C against the rebound `V3_YARDSTICK_2026-06-30` guard (`Hash lock: ok`, no
  `--allow-new-yardstick`). Confirm the bound headline: `top3_family` **176/294**, `coverage` **0.37**
  (109/294), `total_abstained` **185**, `single_verdict` **81/294**.
- **Floor-inertness stated:** report explicitly that floor fires on **0** cases (all abstention is
  margin-driven) — this is the finding that kills the absolute-confidence lever.
- **Margin sweep (the decision input):** recompute, **on the scorer's 294 denominator**, the
  family-aware abstain outcome at MARGIN ∈ {0.05, 0.03, 0.02, 0.01, 0.00} and floor-only. For each:
  `coverage`, `total_abstained`, and — crucially — how many abstained cases are **top3-correct**
  (hidden wins) vs **top3-wrong** (correct silence). This is what tells the owner whether relaxing
  the margin recovers wins or just leaks wrong answers. (A read-only recompute from the run's verdict
  scores + the corpus expected families; no engine change, no re-run needed.)
- **Disclosure honesty:** Tier 1 must not present 0.37 coverage as "fixed" — 185 still abstained, of
  which **88 are top3-correct** (the dial hides them) and 97 top3-wrong. State the hidden-win count
  and that margin-abstain conflicts with the top-3 verdict shape.
- Inner loop clean on any helper touched (`py_compile`, `ruff`, `pyright`); a small read-only sweep
  script is fine (place under `v3/`, not the hash-locked `run_suite.py`); no new test required if no
  engine code changes.

### Disclosure (what this task must surface, not hide) ###
(1) `top3_family` is unchanged (176) — abstain never was an accuracy lever; say so plainly.
(2) The floor is inert; the only working lever (margin) fights the top-3 reframe — name that tension
so the "retune margin" option isn't mistaken for a free win. (3) The sweep must show wins-hidden vs
wrong-silenced per threshold, so no operating point looks cheaper than it is.

### Context ###
Reads `apps/wired/v7/runs/POST_T_V3_3C/results.json` (AFTER = family-aware margin; written by T-V3-3C)
and, for movement, `apps/wired/v7/runs/POST_T_V3_3B/results.json` (BEFORE = raw margin). Expected
families for the sweep's right/wrong split come from the corpus the scorer already loads
(`cases_petrol_v7.csv`, via `score_v3_yardstick.py`). Disclosed baselines from
`progress_notes/T-V3-3C.md`: coverage 0.37, total_abstained 185, recovered 63, hidden wins 52
(single-verdict) / 88 (top3), top3_family 176.

### Consumer (signal/noise) ###
- **Consumer:** the owner's abstain-commit decision (T-V3-3D-ABSTAIN-CAL vs redefine vs T-V3-4) and
  the v3 acceptance gate.
- **Code path:** `score_v3_yardstick.py score`/`diff` + a read-only sweep helper. No engine edit.

### Deliverables ###
1. `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.{md,json}` — CREATE. Tiered report (md) + per-case +
   margin sweep (json).
2. (optional) `v3/abstain_sweep.py` — CREATE, read-only recompute helper (no engine/run_suite touch).

### Files to touch ###
- `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md` (CREATE)
- `v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.json` (CREATE)
- `v3/abstain_sweep.py` (CREATE, optional)

### Out of scope ###
No engine/schema/scorer-threshold edits (retune is the deferred commit T-V3-3D-ABSTAIN-CAL, decided
FROM this report). **Do NOT edit `run_suite.py`** (hash-locked) or re-hash any yardstick. No oracle/CSV
edits. No `Vault/` edits. GRAPH GUARDRAIL: no `graphify`/graph rebuild.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --results apps/wired/v7/runs/POST_T_V3_3C/results.json | sed -n '1,16p'
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/POST_T_V3_3B/results.json \
  --after  apps/wired/v7/runs/POST_T_V3_3C/results.json \
  --write-md v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.md \
  --write-json v3/reports/V3_ABSTAIN_CHECKPOINT_2026-07-01.json | grep -iE 'REGRESSIONS|newly_pass'
# then hand-author Tier 1/2 + the margin sweep table into the .md/.json.
```
Gate: `Hash lock: ok`; `top3_family` 176/294; Tier-1 headline + Tier-2 decision map written; floor=0
stated; margin sweep (coverage + hidden-wins vs wrong-silenced per threshold) present on the 294
denominator.

### Progress hook ###
PROGRESS.md `T-V3-D6`: Status=done, Files changed=2-3, Verification="abstain checkpoint: coverage
0.10->0.37, top3_family 176 unchanged, 63 recovered; floor inert (0/297), all abstain margin-driven;
88 top3-correct still hidden; margin sweep shows cliff 0.05->0.02 ~doubles coverage; Tier-2 menu =
retune(T-V3-3D)/redefine/floor-calib/T-V3-4/dedupe".

### Depends on ###
T-V3-3C (family-aware margin) done — AFTER run `POST_T_V3_3C/results.json` present.
