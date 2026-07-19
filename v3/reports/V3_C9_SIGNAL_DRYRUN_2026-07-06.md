---
node_type: report
lab: apps/wired
module: v3/c9_signal_sim.py
implements: T-V3-P4-C9A
consumers: [owner acceptance read, next-decision C9B commit sizing]
tags: [v3, phase4, c9, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C9A_c9_signal_dryrun.md
---

# V3 C9 SIGNAL DRYRUN — Independent healthy-confirm (read-only sim)

**Task:** [[T-V3-P4-C9A_c9_signal_dryrun]] · **Date:** 2026-07-06 · **Mode:** STRICT (read-only sim)
**Baseline pin:** `POST_T_V3_P4_C4B` / `V3_YARDSTICK_2026-07-06-C4B` (csv `1063be61…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**C9 Seed:** `v3/data/c9_synthetic_seed_2026-07-06.json` (`synthetic=true`; 10 separable + 1 stay-abstained misfire lookalike)

## 1. Headline yield (Scenario 2: full contract)

- **Simulated top3_family:** **269/294** (baseline 259/294, **+10** newly passes).
- **Coverage:** **215/294** (79 abstained; coverage 73.13%, top3_on_covered 93.49%).
- **FT-8 union regressions:** **0** regressions over 17 neighbours (0 no_fault regressions).
- **Stay-abstained validation:** 0 stay-abstained cases banked (should be 0; actual banked: []).

### Scoreboard Disclosure & Trade-offs
- **WOULD_BANK Masking:** Only 1 of the 10 newly-passing cases (EXT-216) remains **abstained** (masked by the margin/floor dial).
- **Covered Pool Expansion:** The covered pool increases from **214 to 215** cases (due to CSV-127 and CSV-128 moving from abstained to covered, while EXT-216 became abstained).
- **Passing Pool Drift:** No active passing pool cases were regressed.
- **Net Metric Transitions:** `top3_family` moves **259 → 269** (+10), coverage moves **72.79% → 73.13%** (214/294 to 215/294), and `top3_on_covered` moves **89.72% → 93.49%** (192/214 to 201/215).

## 2. Column-subset scenario ladder

| Metric | S1 OBD-only | S2 full contract | S-COMMIT |
| --- | ---: | ---: | ---: |
| top3_family | 269/294 | 269/294 | 269/294 |
| WOULD_BANK | **10** | **10** | **10** |
| coverage | 73.13% | 73.13% | 73.13% |
| top3_on_covered | 93.49% | 93.49% | 93.49% |
| abstained | 79 | 79 | 79 |
| regressions | 0 | 0 | 0 |

## 3. Precedence & collision checks

- **C3/C9 precedence assertion:** overlap = [] (should be empty).
- **C6/C9 precedence assertion:** overlap = [] (should be empty).
- **C4/C9 precedence assertion:** overlap = [] (should be empty).

## 4. Per-case yield breakdown (Scenario 2)

| Case ID | Oracle fault | Seed path | C9 State (S2) | Sub-gate | Outcome | Winner (sim) | Top-3 families | Reason if STILL_SHORT |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `CSV-127` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[catalyst_failure, lean_condition, no_fault]` | — |
| `CSV-128` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[catalyst_failure, misfire, no_fault]` | — |
| `EXT-216` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `RM-001` (`rich_mixture`) | `[catalyst_failure, no_fault, rich_mixture]` | — |
| `PDF-HI-005` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[ecu_fault, no_fault, sensor_fault]` | — |
| `PDF-HI-010` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[ecu_fault, no_fault, sensor_fault]` | — |
| `YAML-PDF_HI_005` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[ecu_fault, lean_condition, no_fault]` | — |
| `YAML-PDF_HI_010` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[cam_timing, catalyst_failure, no_fault]` | — |
| `YAML-TC1` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[ecu_fault, lean_condition, no_fault]` | — |
| `case_014` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[catalyst_failure, no_fault, sensor_fault]` | — |
| `era2_016` | `misfire_lookalike` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `dtc_present,mode06_margin_low,stft_idle_high,ltft_idle_high,trim_delta_high,gas_hc_out_of_bounds,gas_co_out_of_bounds,gas_co2_out_of_bounds,gas_o2_out_of_bounds` | **STILL_SHORT** | `NF-001` (`no_fault`) | `[ecu_fault, lean_condition, no_fault]` | seed stay-abstained: misfire lookalike is not healthy separable |
| `era3_014` | `no_fault` | `SYSTEM_HEALTH_CONFIRMED` | `SYSTEM_HEALTH_CONFIRMED` | `pass` | **WOULD_BANK** | `NF-002` (`no_fault`) | `[catalyst_failure, lean_condition, no_fault]` | — |

## 5. FT-8 neighbour union audit

Union of passes_cases across `no_fault.json` contains **17** cases.
- **Dual target+neighbour cases (5):** PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-TC1, era2_016.
- **Regressions (0):** none.

## 6. Commit sizing for C9B

- **New columns load-bearing:** The OBD-only Scenario 1 achieves the exact same yield as Scenario 2. The 5-gas deltas are NOT load-bearing.
- **Precedence implementation point:** `integration_shim.py::_score_rule`, checking C3, C6, and C4 states.

> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 259/294 until C9B commits real columns and mints a new yardstick.

## 7. Recommendation

**Recommendation:** **C9B-GO** (meaningful yield (+10 cases: CSV-127, CSV-128, EXT-216, PDF-HI-005, PDF-HI-010, YAML-PDF_HI_005, YAML-PDF_HI_010, YAML-TC1, case_014, era3_014), 0 regressions, and era2_016 correctly abstains)
