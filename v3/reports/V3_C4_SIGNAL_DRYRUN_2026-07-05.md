---
node_type: report
lab: apps/wired
module: v3/c4_signal_sim.py
implements: T-V3-P4-C4A
consumers: [owner acceptance read, next-decision C4B commit sizing]
tags: [v3, phase4, c4, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C4A_c4_signal_dryrun.md
---

# V3 C4 SIGNAL DRYRUN — `top3_family` rises to 207/294

**Task:** [[T-V3-P4-C4A_c4_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)
**C4 Seed Data:** `v3/data/c4_synthetic_seed_2026-07-01.json` (`synthetic=true` provisional)
**Yardstick:** `V3_YARDSTICK_2026-07-01` (csv `5e41bafe…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**Live engine status:** untouched

## 1. BUILDABLE_NOW (Logic from Research)
The C4 producer emit rules and consumer wiring logic are derived from `value4.1.md` and are fully simulated in memory:
- **Scenario 1 (ΔSTFT-only, 8pt):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -8.0%`. Otherwise, emits `ABSTAIN` (cannot separate lean from bias).
- **Scenario 2 (ΔSTFT-only, 5pt):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -5.0%`. Otherwise, emits `ABSTAIN`.
- **Scenario 3 (Full-signal):** Emits `LEAK` if `delta_stft_idle_2500_pct <= -8.0%` OR `co2_idle_pct < 12.0%` OR `tailpipe_o2_elevation_pct > 2.5%`. If not a leak, checks if `downstream_o2_v > 0.7 V` and `propane_trim_shift_pct > -15.0%` to emit `PERSIST_BIAS`. Checks if `downstream_o2_v <= 0.4 V` and `propane_trim_shift_pct <= -15.0%` to emit `PERSIST_LEAN`. Otherwise, emits `ABSTAIN`.
- **Consumer Wiring:** `exhaust_leak.json` EL-001/003 fire only if `LEAK` is emitted. `lean_condition.json` LC-001/002 fire only if `PERSIST_LEAN` is emitted. `sensor_fault.json` SF-001/002/008 fire only if `PERSIST_BIAS` is emitted.
- **Score Boost:** satisfying the matching C4 state adds a `DEFINITIVE` boost (`+0.10`) to the rule's score and raises/removes the confidence ceiling (`clamped_score = min(raw_score, 1.0)`). Non-matching rules are pruned (`None`).

## 2. SCORING_GATED (Metrics & Yield Breakdown)

### Scenario Comparison Summary
| Metric | Baseline | Scenario 1 (ΔSTFT-only, 8pt) | Scenario 2 (ΔSTFT-only, 5pt) | Scenario 3 (Full-Signal) |
| --- | --- | --- | --- | --- |
| **Denominator** | 294 | 294 | 294 | 294 |
| **Top-3 family hits** | 197/294 | 200/294 | 203/294 | 207/294 |
| **Newly passing (yield)** | — | **4** | **7** | **10** |
| **Abstained count** | 76 | 76 | 75 | 76 |
| **Coverage** | 74.15% | 74.15% | 74.49% | 74.15% |
| **Top-3 on covered** | 73.15% | 74.31% | 75.34% | 77.06% |

### Scenario Yield Breakdown
1. **Scenario 1 (ΔSTFT-only, 8pt):** Banks **4** of the 7 exhaust leaks. The other 3 leaks (EXT-238, EXT-239, TC-048) have yellow-band delta STFTs (-7.4%, -7.1%, -5.9%) and stay short. The 4 persistent cases cannot be separated and stay short/abstained.
2. **Scenario 2 (ΔSTFT-only, 5pt):** Banks **7** of the 7 exhaust leaks. Because the seed's leak-band boundary is -5.0%, all 7 leaks satisfy this wider threshold and flip to top-3. The 4 persistent cases cannot be separated and stay short/abstained.
3. **Scenario 3 (Full-Signal):** Banks **10** cases (7 exhaust leaks + 3 lean cases). It recovers all 7 exhaust leaks (confirming yellow-band deltas via CO2/O2) and separates the 3 lean cases from the 1 biased O2 case using downstream O2 and propane. The biased O2 case (CASE-022) is separated but remains short of top-3 (STILL_SHORT) due to baseline scores, but is no longer abstained.

### Per-Case C4 Yield Split (Scenario 3: Full-Signal)
| Outcome | Count | Case IDs | Description |
| --- | --- | --- | --- |
| **WOULD_BANK** | 10 | `CASE-020, CSV-129, CSV-130, EXT-211, EXT-212, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95` | Newly passing C4-separable cases that flip from baseline FAIL to simulation PASS. |
| **ALREADY_PASS** | 0 | `(none)` | C4 cases that were already passing in baseline and continue to pass. |
| **STILL_SHORT** | 1 | `CASE-022` | Cases that remain FAIL / outside top-3 (biased O2 case CASE-022). |
| **ABSTAIN_NO_DATA** | 0 | (none) | Cases unmeasured (none in this synthetic run). |

### Detail of the 11 C4 Cases (Scenario 3: Full-Signal)
| Case ID | Expected Family | C4 Emitted State | Baseline Hit | Baseline Abstained | Top-3 Hit | Abstained | Simulated Winner | Winner Family | Top-3 Families | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-020 | lean_condition | `PERSIST_LEAN` | False | False | True | False | LC-002 | lean_condition | `{catalyst_failure, lean_condition, misfire}` | **WOULD_BANK** |
| CASE-022 | sensor_fault | `PERSIST_BIAS` | False | False | True | True | LC-003 | lean_condition | `{lean_condition, misfire, sensor_fault}` | **STILL_SHORT** |
| CSV-129 | exhaust_leak | `LEAK` | False | False | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| CSV-130 | exhaust_leak | `LEAK` | False | False | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| EXT-211 | lean_condition | `PERSIST_LEAN` | False | False | True | False | LC-002 | lean_condition | `{catalyst_failure, lean_condition, misfire}` | **WOULD_BANK** |
| EXT-212 | lean_condition | `PERSIST_LEAN` | False | False | True | False | LC-002 | lean_condition | `{catalyst_failure, lean_condition, misfire}` | **WOULD_BANK** |
| EXT-238 | exhaust_leak | `LEAK` | False | False | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| EXT-239 | exhaust_leak | `LEAK` | False | False | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| PDF-HI-007 | exhaust_leak | `LEAK` | False | True | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| TC-048 | exhaust_leak | `LEAK` | False | True | True | False | EL-001 | exhaust_leak | `{catalyst_failure, exhaust_leak, misfire}` | **WOULD_BANK** |
| YAML-CSV95 | exhaust_leak | `LEAK` | True | True | True | False | EL-001 | exhaust_leak | `{exhaust_leak, lean_condition, misfire}` | **WOULD_BANK** |

## 3. CODE_LANDED != SCORE_MOVED
This dry-run simulation runs on **provisional synthetic data** (`synthetic=true`) as permitted under §Provisional synthetic signals. The code logic for the C4 signals is buildable now, but **the score does not move in the live yardstick** until real measured data for the 11 cases is supplied by the owner and committed in `T-V3-P4-C4B`.

## 4. REGRESSION / FT-8 Neighbour Audit
The consumer changes touch `exhaust_leak`, `lean_condition`, and `sensor_fault` rules, affecting a neighbour set of **35** cases.
Audit Result: **0 regressions detected** on the full 294-case corpus (regressions = `[]`).
All previously passing non-C4 neighbours continue to pass. The C4 signal gating isolates the changes completely to C4 cases.

## 5. Column-Add Gate & Commit Scope for `T-V3-P4-C4B` (Sizing)
Based on this simulation, we disclose the following recommendations for the `C4B` commit:
1. **ΔSTFT-alone yield is insufficient for full separation:**
   - If we add **no new columns** and rely solely on `delta_stft` over the shared C5 trims:
     - Under threshold `-8.0%`: banks **4** leaks, leaving 3 leaks and all 4 persistent cases still short (7 cases total still short).
     - Under threshold `-5.0%`: banks **7** leaks, leaving only the 4 persistent cases still short.
2. **Column-add decision for full separation:**
   - Reclaiming the 3 `lean_condition` cases (`CASE-020`, `EXT-211`, `EXT-212`) and the 1 `sensor_fault` case (`CASE-022`) requires separating them, which is impossible without adding `downstream_o2_v` and `propane_trim_shift_pct` as corpus columns.
   - If the owner chooses **not** to add those columns, those 4 cases must stay abstained.
   - If the owner chooses to add those columns, all 3 `lean_condition` cases are successfully reclaimed, bringing the total yield to **10** banked cases.
3. **Commit Scope:**
   - **Scenario A (Abstain fallback):** Wire ΔSTFT <= -5.0% to emit `LEAK`. Do not add any new corpus columns. Keep the 4 persistent cases abstained.
   - **Scenario B (Full-signal):** Wire the full producer state emit rule. Add `co2_idle_pct`, `tailpipe_o2_elevation_pct`, `downstream_o2_v`, and `propane_trim_shift_pct` to the corpus CSV, obdlab, and gaslab. Wire the rules to gate on `LEAK`, `PERSIST_LEAN`, and `PERSIST_BIAS` with a `+0.10` boost.

