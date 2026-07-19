---
node_type: report
lab: apps/wired
module: v3/c5_signal_sim.py
implements: T-V3-P4-C5A
consumers: [owner acceptance read, next-decision C5B commit sizing]
tags: [v3, phase4, c5, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C5A_c5_signal_dryrun.md
---

# V3 C5 SIGNAL DRYRUN — Lean condition root cause (read-only sim)

**Task:** [[T-V3-P4-C5A_c5_signal_dryrun]] · **Date:** 2026-07-06 · **Mode:** STRICT (read-only sim)
**Baseline pin:** `POST_T_V3_P4_C6B` / `V3_YARDSTICK_2026-07-05-C6B` (csv `bf739368…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**C5 Seed:** `v3/data/c5_synthetic_seed_2026-07-06.json` (`synthetic=true`; 6 separable + 4 stay-abstained EGR lookalikes)

## 1. Headline yield (Scenario 3: full contract)

- **Simulated top3_family:** **246/294** (baseline 241/294, **+5** newly passes).
- **Coverage:** **207/294** (87 abstained; coverage 70.41%, top3_on_covered 85.02%).
- **FT-8 union regressions:** **0** regressions over 68 neighbours (0 no_fault regressions).
- **Stay-abstained validation:** 0 stay-abstained cases banked (should be 0; actual banked: []).

### Scoreboard Disclosure & Trade-offs (C5R Audit Requirement)
- **WOULD_BANK Masking:** All 5 newly-passing cases (EXP-N011, EXP-N022, EXP-N029, case_003, case_016) remain **abstained** (masked by the margin/floor dial).
- **Covered Pool Reduction:** The covered pool drops from **211 to 207** cases. The 4 cases that went from covered to abstained are: **EXP-N011, EXP-N022, EXP-N029, and era3_015**.
- **Passing Pool Drift:** Case **era3_015** was covered-as-passing in the baseline but becomes abstained here, leaving the active passing pool.
- **Net Metric Transitions:** `top3_family` moves **241 → 246**, coverage moves **71.8% → 70.4%** (211/294 to 207/294), and `top3_on_covered` rises **83.89% → 85.02%** (177/211 to 176/207).
## 2. Column-subset scenario ladder

| Metric | S1 trims only | S2 + WOT load/lambda | S3 full (+ WOT press) | S-COMMIT (WOT trims/press/load) |
| --- | ---: | ---: | ---: | ---: |
| top3_family | 246/294 | 246/294 | 246/294 | 246/294 |
| WOULD_BANK | **5** | **5** | **5** | **5** |
| coverage | 70.41% | 70.41% | 70.41% | 70.41% |
| top3_on_covered | 85.02% | 85.02% | 85.02% | 85.02% |
| abstained | 87 | 87 | 87 | 87 |
| regressions | 0 | 0 | 0 | 0 |

## 3. Precedence & collision checks

- **C3/C5 precedence assertion:** overlap = [] (should be empty).
- **C5/C6 MAF-collision assertion:** overlap = [] (should be empty).

## 4. Per-case yield breakdown (Scenario 3)

| Case ID | Oracle fault | Seed path | C5 State (S3) | Sub-gate | Outcome | Winner (sim) | Top-3 families | Reason if STILL_SHORT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CSV-113` | `egr_stuck_open` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `none` | **STILL_SHORT** | `MF-001` (`misfire`) | `[catalyst_failure, misfire, sensor_fault]` | seed stay-abstained: stuck open EGR lookalike is not true-lean separable |
| `CSV-114` | `egr_stuck_open` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `none` | **STILL_SHORT** | `MF-001` (`misfire`) | `[catalyst_failure, misfire, sensor_fault]` | seed stay-abstained: stuck open EGR lookalike is not true-lean separable |
| `EXP-N011` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **WOULD_BANK** | `LC-001` (`lean_condition`) | `[lean_condition, sensor_fault, vacuum_leak]` | — |
| `EXP-N022` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **WOULD_BANK** | `LC-001` (`lean_condition`) | `[catalyst_failure, lean_condition, vacuum_leak]` | — |
| `EXP-N029` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **WOULD_BANK** | `MW-002` (`mechanical_wear`) | `[lean_condition, mechanical_wear, vacuum_leak]` | — |
| `REAL-004` | `egr_stuck_open` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `none` | **STILL_SHORT** | `MF-001` (`misfire`) | `[catalyst_failure, misfire, sensor_fault]` | seed stay-abstained: stuck open EGR lookalike is not true-lean separable |
| `case_003` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **WOULD_BANK** | `CF-001` (`catalyst_failure`) | `[catalyst_failure, lean_condition, misfire]` | — |
| `case_016` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **WOULD_BANK** | `CF-001` (`catalyst_failure`) | `[catalyst_failure, lean_condition, sensor_fault]` | — |
| `era1_001` | `egr_stuck_open` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `none` | **STILL_SHORT** | `MF-001` (`misfire`) | `[catalyst_failure, misfire, sensor_fault]` | seed stay-abstained: stuck open EGR lookalike is not true-lean separable |
| `era3_015` | `vacuum_leak_post_maf` | `VACUUM_LEAK_TRIM_PATTERN` | `VACUUM_LEAK_TRIM_PATTERN` | `vacuum_leak_trim_pattern` | **ALREADY_PASS** | `LC-002` (`lean_condition`) | `[lean_condition, misfire]` | — |

## 5. FT-8 neighbour union audit

Union of passes_cases across `lean_condition.json` and `vacuum_leak.json` contains **68** cases.
- **Dual target+neighbour cases (2):** EXP-N011, case_003.
- **Regressions (0):** none.

## 6. Commit sizing for C5B

- **New columns load-bearing:** The trims-only Scenario 1 recovers the 6 vacuum leaks post-MAF.
- **Precedence implementation point:** `integration_shim.py::_score_rule`, after C3 and C6 branch checks.

> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 241/294 until C5B commits real columns and mints a new yardstick.
