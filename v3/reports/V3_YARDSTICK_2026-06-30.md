# V3_YARDSTICK_2026-06-30 — v3 top-3 + abstain yardstick

**Task:** `T-V3-1_topk_abstain_scorer`  
**Date:** 2026-06-30  
**Mode:** new yardstick for changed metric set (extends frozen `FL_YARDSTICK_2026-06-30`)

---

## Yardstick rule

Per `FL_YARDSTICK_2026-06-30.md`: any change to the metric set mints a **new** yardstick file.  
This file (`V3_YARDSTICK_2026-06-30.md`) is the v3 ruler.  
The frozen baseline `FL_YARDSTICK_2026-06-30.md` remains the immutable historical BEFORE.

---

## Frozen artefacts (post-T-V3-2 active V3 corpus/oracle)

`V3_ORACLE_REPIN_2026-06-30.md` is the change-record for the Option-B oracle re-pin. It is also
known as the `V3_ORACLE_REPIN` yardstick note; the canonical active scoreboard yardstick name is
`V3_YARDSTICK_2026-06-30`.

| Artefact | Value |
|---|---|
| Workspace commit at original FL measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `47182b3d9c4d4cb9e08645746a07fbae0d09b5db3d913fe00e1567965dd86dc9` |
| Oracle subset SHA-256 | `192d7be1a339ce45afa7682d710ccfca7b1a0102bff447d037a63a64a73879f5` |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON (historical FL baseline) | `apps/wired/v7/runs/20260630_163900/results.json` |
| Run JSON SHA-256 | `d9069f8dea738de91654320b4f431b4345364ff27571f39cce2fd5b7fb210ee3` |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows `accuracy_excluded=true` |

---

## v3 metric definitions (V3_PLAN.md §3)

| Metric | Definition | Role |
|---|---|---|
| `single_verdict` (family+state) | winner family == expected **and** state correct | frozen BEFORE = **45.24%**; never deleted |
| **`top3_family`** | expected family in {winner} ∪ {top-2 differential siblings by score} | **v3 acceptance metric** |
| `coverage` | share of cases the engine did **not** abstain on | honesty dial — high accuracy on low coverage is not a win |
| `top3_on_covered` | `top3_family` restricted to non-abstained cases | the headline **"95%" target** |

---

## Abstain rule (calibrated from T-V3-0 report)

An abstain is triggered when **either** condition holds:

| Parameter | Value | Source |
|---|---|---|
| `abstain_floor` | **0.80** (winner_score < 0.80 → abstain) | T-V3-0 §6: "close-margin wrong top-1 cases (<0.03 gap): 64" |
| `abstain_margin` | **0.05** (top1 − top2 ≤ 0.05 → abstain) | T-V3-0 §6 |

An abstained case:
- counts **against** `coverage` (denominator = all 294 accuracy cases)
- is **excluded** from `top3_on_covered` denominator
- is **never** scored as a wrong family in primary metrics

---

## Fault_id → fault_family resolution for siblings

Until T-V3-3 ships `fault_family` on `DifferentialSiblingOut`, the scorer resolves sibling `fault_id` → family via the same registry/KG map the router uses:

```
rule_map = load_rule_family_map()  # labs/comlab/registry/rules/*.json → {rule_id: fault_family}
sibling_family = rule_map.get(sibling.fault_id, "unspecified")
```

This mirrors `fault_atlas_router.py` `_kg.resolve(fault_id).fault_family`.

---

## v3 scoreboard output (what `score_v3_yardstick.py score` prints)

```
WIRED-FL V3 SCOREBOARD — SCORE
Yardstick: FL_YARDSTICK_2026-06-30; localization: FL_LOCALIZATION_2026-06-30
Hash lock: ok
Result source: current installed wired engine
Build: git_sha=... env=(USE_V2_REGISTRY=..., WIRED_OTEL=...) label=...

OVERALL PRIMARY ROUTING (frozen single-verdict baseline)
  family+state: 133/294 = 45.24 %
  family only : 141/294 = 47.96 %
  state only  : 275/294 = 93.54 %
  adjudicated : 143/294 = 48.64 % (ORACLE_SUSPECT +10)

V3 TOP-3 + ABSTAIN METRICS
  top3_family       : X/294 = YY.YY %
  coverage          : Z.ZZ  (NNN/294 non-abstained)
  top3_on_covered   : M/N   = PP.PP %
  total_abstained   : K
  abstain_floor     : 0.80  (winner_score < floor -> abstain)
  abstain_margin    : 0.05  (top1 - top2 <= margin -> abstain)

PER-FAMILY PRIMARY ROUTING
  ... (unchanged)

PER-MODE COUNTS (frozen T-FL-3 buckets)
  ... (unchanged)

SURFACE DIMENSIONS
  ... (unchanged)
```

---

## Acceptance criteria (V3_PLAN.md §6)

v3 is accepted when the scoreboard reports, **against this V3_YARDSTICK**:

1. `single_verdict` family+state — reported, **no family regressed** vs frozen 45.24%
2. **`top3_on_covered >= 95%`** with `coverage` ≥ floor set by T-V3-0 (likely ≥ 80%)
3. Per-mode buckets show SURFACE_DEFECT and OUTRANKED drained to ~0 remaining-miss; residual misses are only PRODUCER_GAP/DATA_GAP that Phase 4 has not yet (or cannot) close, and those are **abstained**, not mis-answered.

---

## Verification command

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Must print both the frozen single-verdict block **and** the new V3 TOP-3 + ABSTAIN block, with the frozen 45.24% unchanged.

---

## Files created/modified by T-V3-1

- `apps/wired/fl_tasks/score_v3_yardstick.py` — added `top3_family`, `coverage`, `top3_on_covered`, abstain logic; updated `render_score`
- `apps/wired/v7/tests/test_topk_scorer.py` — unit tests pinning new metric math + abstain behavior
- `v3/reports/V3_YARDSTICK_2026-06-30.md` — this file