# V3_YARDSTICK_2026-07-05 — C2 signal-pack yardstick

**Task:** `T-V3-P4-C2B_c2_signal_commit`  
**Date:** 2026-07-05  
**Mode:** new yardstick for changed corpus schema (C2 columns landed)

---

## Yardstick rule

Per `v3/V3_START_HERE.md` and `FL_YARDSTICK_2026-06-30.md`: any corpus/oracle edit mints a **new** yardstick file.  
This file (`V3_YARDSTICK_2026-07-05.md`) is the active C2-commit ruler.  
The frozen baseline `FL_YARDSTICK_2026-06-30.md` and prior `V3_YARDSTICK_2026-07-01` remain immutable historical records.

---

## Frozen artefacts (post-C2B active V3 corpus/oracle)

| Artefact | Value |
|---|---|
| Workspace commit at original FL measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `3df2e8cbd82a866c3b8f12a72fdee837ac35cc1f09a19db65a10baa499282ddc` |
| Oracle subset SHA-256 | `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127` |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json` |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows `accuracy_excluded=true` |

---

## Measured scoreboard state at mint

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Observed:

- `top3_family` = **212/294 = 72.11%**
- `coverage` = **214/294 = 0.73**
- `top3_on_covered` = **164/214 = 76.64%**
- `total_abstained` = **80**
- `single_verdict family+state` = **134/294 = 45.58%**
- `Hash lock: ok`

This mint records the first live signal-pack commit. `top3_family` rises **197 → 212** with `REGRESSIONS: (empty)` against `POST_T_V3_3D`.

---

## Provenance

- C2 seed source: `v3/data/c2_synthetic_seed_2026-07-01.json`
- C2 disclosure report: `v3/reports/V3_C2_SIGNAL_DRYRUN_2026-07-05.{md,json}`
- Minting task note: `v3/v3_tasks/progress_notes/T-V3-P4-C2B.md`
- Previous active yardstick: `V3_YARDSTICK_2026-07-01`
