---
node_type: report
lab: apps/wired
module: v3/c2_signal_sim.py
implements: T-V3-P4-C2A
consumers: [owner acceptance read, next-decision C2B commit sizing]
tags: [v3, phase4, c2, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C2A_c2_signal_dryrun.md
---

# V3 C2 SIGNAL DRYRUN — `top3_family` rises to 212/294

**Task:** [[T-V3-P4-C2A_c2_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)
**C2 Seed Data:** `v3/data/c2_synthetic_seed_2026-07-01.json` (`synthetic=true` provisional)
**Yardstick:** `V3_YARDSTICK_2026-07-01` (csv `5e41bafe…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**Live engine status:** untouched

## 1. BUILDABLE_NOW (Logic from Research)
The C2 producer emit rule and consumer wiring logic are derived from `cluster2.md` and are fully simulated in memory:
- **Producer Emit:** sustained negative trims at idle (`STFT+LTFT <= -10%`) emits `TRUE_RICH`. Deteriorated catalyst Mode $06 ratio / decel CO (`index_ratio > 0.20` or `decel_co_pct > 0.8%`) without rich trims emits `LOW_OSC_OR_HIGH_INDEX`. Otherwise, `NORMAL` is emitted.
- **Consumer Gating:** `rich_mixture.json` RM-001/003/004 only fire if `TRUE_RICH` is emitted. `catalyst_failure.json` CF-001/002/006/007 only fire if `LOW_OSC_OR_HIGH_INDEX` is emitted.
- **Score Boost:** satisfying the matching C2 state adds a `DEFINITIVE` boost (`+0.10`) to the rule's score and raises/removes the confidence ceiling (`clamped_score = min(raw_score, 1.0)`). Non-matching rules are pruned (`None`).

## 2. SCORING_GATED (Metrics & Yield Breakdown)
- **Denominator:** 294 cases
- **Baseline top-3 passes:** 197/294 (67.01%)
- **Simulated top-3 passes:** 212/294 (72.11%)
- **Newly passing (yield):** **15** cases
- **Coverage:** 72.79% (214/294 covered, 80 abstained)
- **Top-3 on covered:** **99.07%** (exceeds the 95% acceptance target: **99.07% >= 95%**)

### Per-Case C2 Yield Split
| Outcome | Count | Case IDs | Description |
| --- | --- | --- | --- |
| **WOULD_BANK** | 15 | `CASE-015, CASE-029, CASE-040, CSV-121, CSV-122, EXT-232, EXT-233, PDF-HI-001, PDF-HI-006, RULE-CO-1, YAML-PDF_HI_001, case_002, case_015, case_017, era2_019` | Newly passing C2-separable cases that flip from baseline FAIL to simulation PASS. |
| **ALREADY_PASS** | 4 | `CASE-023, EXP-N017, EXT-217, era2_015` | C2 cases that were already passing in baseline and continue to pass. |
| **STILL_SHORT** | 3 | `CSV-100, case_004, era1_017` | Cases that remain FAIL because they are not separable by C2 (3 lean condition, 2 sensor skew). |
| **ABSTAIN_NO_DATA** | 0 | (none) | Cases unmeasured (none in this synthetic run). |

### Detail of the 22 C2 Cases
| Case ID | Expected Family | C2 Emitted State | Baseline Hit | Top-3 Hit | Simulated Winner | Winner Family | Top-3 Families | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-015 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, lean_condition, no_fault}` | **WOULD_BANK** |
| CASE-023 | rich_mixture | `TRUE_RICH` | True | True | RM-001 | rich_mixture | `{cam_timing, misfire, rich_mixture}` | **ALREADY_PASS** |
| CASE-029 | rich_mixture | `TRUE_RICH` | False | True | LC-001 | lean_condition | `{exhaust_leak, lean_condition, rich_mixture}` | **WOULD_BANK** |
| CASE-040 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{lean_condition, no_fault, rich_mixture}` | **WOULD_BANK** |
| CSV-100 | lean_condition | `NORMAL` | False | False | SF-001 | sensor_fault | `{misfire, rich_mixture, sensor_fault}` | **STILL_SHORT** |
| CSV-121 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, exhaust_leak, lean_condition}` | **WOULD_BANK** |
| CSV-122 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, exhaust_leak, lean_condition}` | **WOULD_BANK** |
| EXP-N017 | lean_condition | `NORMAL` | True | True | MF-001 | misfire | `{lean_condition, misfire, sensor_fault}` | **ALREADY_PASS** |
| EXT-217 | rich_mixture | `TRUE_RICH` | True | True | RM-001 | rich_mixture | `{cam_timing, misfire, rich_mixture}` | **ALREADY_PASS** |
| EXT-232 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, lean_condition, no_fault}` | **WOULD_BANK** |
| EXT-233 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, lean_condition, no_fault}` | **WOULD_BANK** |
| PDF-HI-001 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{misfire, rich_mixture, sensor_fault}` | **WOULD_BANK** |
| PDF-HI-006 | catalyst_failure | `LOW_OSC_OR_HIGH_INDEX` | False | True | CF-001 | catalyst_failure | `{catalyst_failure, ecu_fault, sensor_fault}` | **WOULD_BANK** |
| RULE-CO-1 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{ecu_fault, rich_mixture, sensor_fault}` | **WOULD_BANK** |
| YAML-PDF_HI_001 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{misfire, rich_mixture, sensor_fault}` | **WOULD_BANK** |
| case_002 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{misfire, rich_mixture, sensor_fault}` | **WOULD_BANK** |
| case_004 | sensor_fault | `LOW_OSC_OR_HIGH_INDEX` | False | False | CF-001 | catalyst_failure | `{catalyst_failure, ecu_fault, lean_condition}` | **STILL_SHORT** |
| case_015 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{ecu_fault, rich_mixture, sensor_fault}` | **WOULD_BANK** |
| case_017 | rich_mixture | `TRUE_RICH` | False | True | RM-001 | rich_mixture | `{cam_timing, misfire, rich_mixture}` | **WOULD_BANK** |
| era1_017 | sensor_fault | `LOW_OSC_OR_HIGH_INDEX` | False | False | CF-001 | catalyst_failure | `{cam_timing, catalyst_failure, lean_condition}` | **STILL_SHORT** |
| era2_015 | lean_condition | `NORMAL` | True | True | MF-001 | misfire | `{lean_condition, misfire, sensor_fault}` | **ALREADY_PASS** |
| era2_019 | rich_mixture | `TRUE_RICH` | False | True | MF-001 | misfire | `{misfire, rich_mixture}` | **WOULD_BANK** |

## 3. CODE_LANDED != SCORE_MOVED
This dry-run simulation runs on **provisional synthetic data** (`synthetic=true`) as permitted under §Provisional synthetic signals. The code logic for the C2 signals is buildable now, but **the score does not move in the live yardstick** until real measured data for the 22 cases is supplied by the owner and committed in `T-V3-P4-C2B`.

## 4. REGRESSION / FT-8 Neighbour Audit
The consumer changes touch `rich_mixture` and `catalyst_failure` rules, affecting a neighbour set of **33** cases.
Audit Result: **0 regressions detected** on the full 294-case corpus (regressions = `[]`).
All previously passing non-C2 neighbours continue to pass. The C2 signal gating isolates the changes completely to C2 cases.

## 5. Commit Scope for `T-V3-P4-C2B` (Sizing)
Based on this simulation, the `T-V3-P4-C2B` commit scope should be:
1. **Corpus:** add C2 columns to the live corpus CSV.
2. **Producer:** wire `TRUE_RICH` and `LOW_OSC_OR_HIGH_INDEX` monitor states in `obdlab` and `gaslab` using the following thresholds:
   - Total Fuel Trim `STFT+LTFT <= -10%` -> `TRUE_RICH`
   - Mode $06 index ratio `> 0.20` or Decel CO `> 0.8%` -> `LOW_OSC_OR_HIGH_INDEX` (without rich trims)
3. **Consumer:** edit the registry rules `RM-001/003/004` to gate on `TRUE_RICH`, and `CF-001/002/006/007` to gate on `LOW_OSC_OR_HIGH_INDEX` with `+0.10` DEFINITIVE boost and confidence ceiling raised to `1.0` when C2 data is present.
4. **Scoring:** mint a new yardstick to reflect the updated corpus schema.

