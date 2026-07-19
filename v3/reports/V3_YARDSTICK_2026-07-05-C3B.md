# V3_YARDSTICK_2026-07-05-C3B — C3 signal-pack yardstick

**Task:** `T-V3-P4-C3B_c3_signal_commit`  
**Date:** 2026-07-05  
**Mode:** new yardstick for changed corpus schema (C3 electrical columns landed after C2B)

---

## Yardstick rule

Per `v3/V3_START_HERE.md` and `FL_YARDSTICK_2026-06-30.md`: any corpus/oracle edit mints a **new** yardstick file.  
This file (`V3_YARDSTICK_2026-07-05-C3B.md`) is the active C3B-commit ruler.  
The frozen baseline `FL_YARDSTICK_2026-06-30.md` and prior V3 yardsticks remain immutable historical records.

---

## Frozen artefacts (post-C3B active V3 corpus/oracle)

| Artefact | Value |
|---|---|
| Workspace commit at original FL measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `9f530695dc3cf5586c9248a2b9de2f474950170326dcf5f62c1aefc36683e283` |
| Oracle subset SHA-256 | `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127` |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json` |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows `accuracy_excluded=true` |

---

## Measured scoreboard state at mint

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json
```

Observed:

- `top3_family` = **228/294 = 77.55%**
- `coverage` = **209/294 = 0.71**
- `top3_on_covered` = **167/209 = 79.90%**
- `total_abstained` = **85**
- `single_verdict family+state` = **137/294 = 46.60%**
- `Hash lock: ok`

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C2B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json
```

Observed movement against `POST_T_V3_P4_C2B`:

- `newly_pass` = **16**
- `newly_fail` = **0**
- `REGRESSIONS: (empty)`
- per-family net movement: `ecu_fault +16`, all other families `+0`

---

## C3A expectation delta surfaced

The task expected `coverage 210/294`, `top3_on_covered 168/210 = 80.00%`, and `total_abstained 84`. The live C3B run instead produced `coverage 209/294`, `top3_on_covered 167/209 = 79.90%`, and `total_abstained 85`.

Observed abstain changes versus `POST_T_V3_P4_C2B`: five newly margin-abstained cases — `CSV-123`, `CSV-124`, `EXP-N002`, `EXP-N004`, `case_013`. The pack metric still lands exactly: `top3_family 212 → 228 (+16)` with `REGRESSIONS: (empty)`.

---

## Provenance

- C3 seed source: `v3/data/c3_synthetic_seed_2026-07-05.{csv,json}`
- C3 disclosure report: `v3/reports/V3_C3_SIGNAL_DRYRUN_2026-07-05.{md,json}`
- Minting task note: `v3/v3_tasks/progress_notes/T-V3-P4-C3B.md`
- Previous active yardstick: `V3_YARDSTICK_2026-07-05`
