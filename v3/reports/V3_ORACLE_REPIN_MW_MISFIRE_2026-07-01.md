# V3_ORACLE_REPIN_MW_MISFIRE_2026-07-01 — mechanical_wear → misfire oracle re-pin

**Task:** `FL-V3-ORACLE-MW-MISFIRE_oracle_repin`  
**Date:** 2026-07-01  
**Mode:** Oracle-data + yardstick rebind only — zero engine/router/run-suite change. This changes the acceptance answer key for the 10 signed-off ORACLE_SUSPECT rows.

---

## Summary

Re-pinned the v7 oracle (`apps/wired/v7/data/cases_petrol_v7.csv`) for the 10 signed-off ORACLE_SUSPECT rows where the current single-snapshot engine emits `MF-001`/`misfire`.

This is a product-definition call, not an engine improvement: the single-snapshot yardstick now accepts the defensible misfire read. True mechanical-wear separation remains Phase-4 discriminator work.

**Result against `V3_YARDSTICK_2026-07-01`:**

| Metric | Before T-V3-4B | After re-pin | Delta |
|---|---:|---:|---:|
| `top3_family` | 184/294 = 62.59% | 193/294 = 65.65% | +9 |
| scoreboard `family+state` | 80/294 = 27.21% | 85/294 = 28.91% | +5 |
| raw target primary dimensions | 0/10 | 10/10 | +10 |
| `top3_on_covered` | 87/107 = 81.31% | 92/107 = 85.98% | +5 |
| `total_abstained` | 187 | 187 | 0 |

Why +9 rather than +10 top-3: `CSV-120` already had `mechanical_wear` in its old top-3 sibling set before the re-pin, so the answer-key change improves its primary dimensions but not the aggregate top-3 counter. Why +5 rather than +10 scoreboard `family+state`: 5 of the 10 target cases are still abstained under the current 0.05 margin dial, so they pass raw dimensions but are masked from the non-abstained primary summary.

---

## Rows changed

Exactly these 10 rows were re-pinned:

| Case ID | Old expected family/code | New expected family/code | State | Confidence band | Engine verdict |
|---|---|---|---|---|---|
| `CSV-118` | `mechanical_wear` / `ERR-MW-004` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `CSV-119` | `mechanical_wear` / `ERR-MW-002` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `CSV-120` | `mechanical_wear` / `ERR-MW-002` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `EXT-222` | `mechanical_wear` / `ERR-MW-005` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `EXT-223` | `mechanical_wear` / `ERR-MW-003` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `EXT-224` | `mechanical_wear` / `ERR-MW-002` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `MECH-002` | `mechanical_wear` / `ERR-MW-002` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `MECH-006` | `mechanical_wear` / `ERR-MW-005` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `era1_002` | `mechanical_wear` / `ERR-MW-002` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |
| `era1_015` | `mechanical_wear` / `ERR-MW-003` | `misfire` / `MF-001` | `named_fault` | `[0.80, 1.00]` | `misfire` / `MF-001` |

The 4 explicitly excluded mechanical-wear rows remain `mechanical_wear`: `CSV-117`, `EXP-N030`, `MECH-001`, `case_044`.

---

## New yardstick

| Artefact | SHA-256 |
|---|---|
| Corpus CSV (`cases_petrol_v7.csv`) | `5e41bafe85f634f07050627661d411df20c71bdb0e4390b54d6b9787c108a809` |
| Oracle subset | `3088a7c3d0c4b643e1dbf47b0ee05740a7d28416f08fe26a251cc3740948d127` |
| Hash-locked scorer (`apps/wired/v7/run_suite.py`) | `dc47eb4fc7701ae6e5b942c369411af51dca54c5aea4890f2bd401935cc75966` |

`apps/wired/fl_tasks/score_v3_yardstick.py` now binds the active yardstick to `V3_YARDSTICK_2026-07-01`. Historical `FL_YARDSTICK_2026-06-30` and `V3_YARDSTICK_2026-06-30` hashes remain present and unchanged. `apps/wired/v7/run_suite.py` was not touched.

---

## Verification results

### Scoreboard

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --write-results apps/wired/v7/runs/POST_ORACLE_MW/results.json
```

Observed:

- `Yardstick: V3_YARDSTICK_2026-07-01`
- `Hash lock: ok`
- `top3_family: 193/294 = 65.65%`
- `family+state: 85/294 = 28.91%`
- `ORACLE_SUSPECT`: 5 primary pass, 0 remaining miss in the non-abstained summary
- result set written to `apps/wired/v7/runs/POST_ORACLE_MW/results.json`

### Diff guard

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py diff \
  --before apps/wired/v7/runs/POST_T_V3_4B/results.json \
  --after  apps/wired/v7/runs/POST_ORACLE_MW/results.json
```

Observed:

- `Hash lock: ok`
- `REGRESSIONS: (empty)`
- No per-family newly-fail movement.

Note: the scoreboard `diff` command reports `newly_pass: 0` because its movement definition is v3-pass (`single_verdict OR top3_family`), and these cases were already v3-pass after loading the current oracle/result combination. A targeted raw primary-dimension check showed exactly the 10 intended rows flipped from primary fail to primary pass, with `primary_new_fail = 0`.

### Guard tests

```bash
/agent_workspace/.venv-wired/bin/python -m pytest \
  apps/wired/v7/tests/test_oracle_repin.py \
  apps/wired/v7/tests/test_yardstick_rebind.py \
  apps/wired/v7/tests/test_topk_scorer.py -q
```

Observed: `12 passed`.

### CSV target guard

Observed by direct CSV parse:

- `repinned_count = 10`
- target rows: `CSV-118`, `CSV-119`, `CSV-120`, `EXT-222`, `EXT-223`, `EXT-224`, `MECH-002`, `MECH-006`, `era1_002`, `era1_015`
- remaining `expected_fault_family == mechanical_wear` rows: `CSV-117`, `EXP-N030`, `MECH-001`, `case_044`

---

## Files modified / created

1. **Modified:** `apps/wired/v7/data/cases_petrol_v7.csv` — 10 oracle rows re-pinned.
2. **Modified:** `apps/wired/fl_tasks/score_v3_yardstick.py` — active yardstick name and hashes updated.
3. **Modified:** `apps/wired/v7/tests/test_oracle_repin.py` — MW misfire re-pin guard and excluded-row guard.
4. **Modified:** `apps/wired/v7/tests/test_topk_scorer.py` — test helper now places `abstained` inside `verdict`, matching the live scorer read-site.
5. **Created:** `apps/wired/v7/runs/POST_ORACLE_MW/results.json` — AFTER result set.
6. **Created:** `v3/reports/V3_ORACLE_REPIN_MW_MISFIRE_2026-07-01.md` — this change record.

---

## Scope caveat

`apps/wired/tests/test_oil_cases.py::test_oil_cases_route_to_expected_faults` currently expects the `MW-003` fixture to route to `MW-003`, but the live engine routes it to `MF-001`. This was observed while running the broader `apps/wired/tests/` suite and is outside this oracle-data task: no engine, oil fixture, or run-suite code was changed here.
