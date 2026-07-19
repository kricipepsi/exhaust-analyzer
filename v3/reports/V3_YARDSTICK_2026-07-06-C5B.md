# V3_YARDSTICK_2026-07-06-C5B — C5 signal-pack yardstick

**Task:** `T-V3-P4-C5B_c5_signal_commit`  
**Date:** 2026-07-06  
**Mode:** new yardstick for changed corpus schema (C5 5 new schema columns + values into 6 shared columns)

---

## Yardstick rule

Per `v3/V3_START_HERE.md` and `FL_YARDSTICK_2026-06-30.md`: any corpus/oracle edit mints a **new** yardstick file.  
This file (`V3_YARDSTICK_2026-07-06-C5B.md`) is the active C5B-commit ruler.  
The frozen baseline `FL_YARDSTICK_2026-06-30.md` and prior V3 yardsticks remain immutable historical records.

---

## Frozen artefacts (post-C5B active V3 corpus/oracle)

| Artefact | Value |
|---|---|
| Workspace commit at original FL measurement | `fe3b827cfa4c80b099873a6c3c4b17833b50ae98` |
| Corpus + oracle CSV | `apps/wired/v7/data/cases_petrol_v7.csv` |
| CSV SHA-256 | `c49c17af1182a3eb07056a3fbf27c101378a32f35e375b18b3104d3928d8c7fd` |
| Oracle subset SHA-256 | `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127` |
| Scorer | `apps/wired/v7/run_suite.py` |
| Scorer SHA-256 | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |
| Source run JSON | `apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json` |
| Row count | 314 total = 294 accuracy (`tag=viable`) + 20 invalid; 20 rows `accuracy_excluded=true` |

---

## Measured scoreboard state at mint

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
```

Observed:

- `top3_family` = **250/294 = 85.03 %**
- `coverage` = **208/294 = 0.71**
- `top3_on_covered` = **179/208 = 86.06 %**
- `total_abstained` = **86**
- `single_verdict family+state` = **147/294 = 50.00 %**
- `Hash lock: ok`

Diff command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff --before apps/wired/v7/runs/POST_T_V3_P4_C6B/results.json --after apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json
```

Observed movement against `POST_T_V3_P4_C6B`:

- `newly_pass` = **9**
- `newly_fail` = **0**
- `REGRESSIONS: (empty)`
- per-family net movement: `lean_condition +9`, all other families `+0`

---

## C5B expectation delta surfaced (Scoreboard Disclosure)

The task expected `top3_family 246/294` and `5 newly_pass / 0 newly_fail / REGRESSIONS: (empty)`. The live run resulted in `top3_family 250/294` (9 newly_pass).

The delta is exactly +4 additional passes: `era1_001, CSV-113, CSV-114, REAL-004`. These are the 4 EGR stuck open lookalike cases. In the baseline `POST_T_V3_P4_C6B` (where C5 columns were empty/None), these 4 cases had empty trims, which allowed a false `CF-001` (catalyst failure) rule to outrank `lean_condition` in the top-3 window. Writing normal/healthy trims from the C5 seed (as required by the data gate) caused the catalyst check in `integration_shim.py::_score_rule` to prune the false `CF-001` rule, allowing their expected family `lean_condition` to enter the top-3 window and pass. This is chemically and diagnostically correct.

- **WOULD_BANK Masking:** All 5 newly-passing vacuum leak cases (`EXP-N011, EXP-N022, EXP-N029, case_003, case_016`) remain **abstained** (masked by the margin/floor dial).
- **Covered Pool Reduction:** The covered pool drops from **211 to 208** cases. The net metric transitions are: `top3_family` moves **241 → 250**, coverage moves **211/294 to 208/294**, and `top3_on_covered` rises **83.89% → 86.06%**.

---

## Provenance

- C5 seed source: `v3/data/c5_synthetic_seed_2026-07-06.{csv,json}`
- C5 disclosure report: `v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}` scenario `s_commit`
- Minting task note: `v3/v3_tasks/progress_notes/T-V3-P4-C5B.md`
- Previous active yardstick: `V3_YARDSTICK_2026-07-05-C6B`
