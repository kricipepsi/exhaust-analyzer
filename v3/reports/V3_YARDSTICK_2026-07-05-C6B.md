# V3_YARDSTICK_2026-07-05-C6B — C6 signal-pack yardstick

**Task:** `T-V3-P4-C6B_c6_signal_commit`  
**Date:** 2026-07-05  
**Mode:** new yardstick for changed corpus schema (C6 Mode $06 + shared MAF columns landed after C3B)

---

## Yardstick rule

Per `v3/V3_START_HERE.md` and `FL_YARDSTICK_2026-06-30.md`: any corpus/oracle edit mints a **new** yardstick file.  
This file (`V3_YARDSTICK_2026-07-05-C6B.md`) is the active C6B-commit ruler.  
The frozen baseline `FL_YARDSTICK_2026-06-30.md` and prior V3 yardsticks remain immutable historical records.

---

## Frozen artefacts (post-C6B active V3 corpus/oracle)

| Artefact | Value |
|---|---|
| Workspace commit at original FL measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `bf7393688230caf7f15054cc2473343e26351aa72c4615ca83044c7eb12fc0de` |
| Oracle subset SHA-256 | `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127` |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json` |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows `accuracy_excluded=true` |

---

## Measured scoreboard state at mint

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
```

Observed:

- `top3_family` = **241/294 = 81.97%**
- `coverage` = **211/294 = 0.72**
- `top3_on_covered` = **177/211 = 83.89%**
- `total_abstained` = **83**
- `single_verdict family+state` = **146/294 = 49.66%**
- `Hash lock: ok`

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json
```

Observed movement against `POST_T_V3_P4_C3B`:

- `newly_pass` = **13**
- `newly_fail` = **0**
- `REGRESSIONS: (empty)`
- per-family net movement: `sensor_fault +13`, all other families `+0`

---

## C6B expectation delta surfaced

The task expected `top3_family 241/294` and `13 newly_pass / 0 newly_fail / REGRESSIONS: (empty)`; the live C6B run matched that exactly. Coverage moved from C3B's 209/294 to **211/294** with **83** total abstained. The C6A pre-flight had disclosed 13 WOULD_BANK with 8 covered / 5 still-abstained under `MARGIN=0.02`; the live corpus/scorer state preserves the `top3_family` movement while the abstain dial remains unchanged.

---

## Provenance

- C6 seed source: `v3/data/c6_synthetic_seed_2026-07-05.{csv,json}`
- C6 disclosure report: `v3/reports/V3_C6_SIGNAL_DRYRUN_2026-07-05.{md,json}` scenario `S-COMMIT`
- Minting task note: `v3/v3_tasks/progress_notes/T-V3-P4-C6B.md`
- Previous active yardstick: `V3_YARDSTICK_2026-07-05-C3B`
