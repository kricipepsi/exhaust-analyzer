---
node_type: report
lab: apps/wired
module: v3/c3_signal_sim.py
implements: T-V3-P4-C3A
consumers: [owner acceptance read, next-decision C3B commit sizing]
tags: [v3, phase4, c3, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C3A_c3_signal_dryrun.md
---

# V3 C3 SIGNAL DRYRUN — ECU/control-system fault (read-only sim)

**Task:** [[T-V3-P4-C3A_c3_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)
**Baseline pin:** `POST_T_V3_P4_C2B` / `V3_YARDSTICK_2026-07-05` (csv `3df2e8cb…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**C3 Seed:** `v3/data/c3_synthetic_seed_2026-07-05.json` (`synthetic=true` provisional; Δλ is **empirical-anecdotal** — C3-PRE §7)
**Live engine status:** untouched (no corpus / rule / registry / yardstick edit)

## Headline
- **Baseline `top3_family`:** 212/294 → **Scenario 2: 228/294** (+16).
- **Scenario 1 (electrical-only, no Δλ):** 16 WOULD_BANK (4 covered / 12 still-abstained at MARGIN=0.02).
- **Scenario 2 (full contract, incl. Δλ):** 16 WOULD_BANK (4 covered / 12 still-abstained at MARGIN=0.02).
  - `WOULD_BANK` = correct family flips **into the top-3 window** (the pack's `top3_family` metric). A flipped case may still be **abstained** by the MARGIN=0.02 dial — disclosed, not hidden. C3B/abstain-cal decides whether to surface those.
- **Zero-overlay self-check:** drift = 0 across 294 vs `POST_T_V3_P4_C2B`.
- **Regressions (S2):** 0 (`(empty)`).
- **stay_abstained honoured:** 4 seed cases; banked = 0 (none — correct).

## 1. Producer simulation (`ControlPlausibilityState`)
Per contract §2 (grounding-tagged); any gate met → `CONTROL_REFERENCE_FAULT`, none → `ABSTAIN`:
- **lean-bias:** `dlc_signal_ground_drop_v > 0.2` AND `gas_obd_lambda_delta >= 0.05` — ground standardized, Δλ **empirical-anecdotal**.
- **rich-bias:** `koeo_map_baro_delta_kpa >= 5.0` AND `gas_obd_lambda_delta >= 0.05` — MAP/BARO manufacturer-typical, Δλ **empirical-anecdotal**.
- **processor (P0606):** `bidirectional_fuel_response_ok_bool == False` AND `module_voltage_loaded_v < 12.0` — manufacturer-typical, no Δλ (electrical-only).

## 2. Scenario ladder (acquisition-cost disclosure)
| Metric | Scenario 1 (electrical-only, no Δλ) | Scenario 2 (full, incl. Δλ) |
| --- | --- | --- |
| Top-3 family hits | 228/294 | 228/294 |
| WOULD_BANK (top-3 flip) | **16** | **16** |
| — of which covered | 4 | 4 |
| — of which still-abstained | 12 | 12 |
| Abstained count (all 294) | 84 | 84 |
| Coverage | 71.43% | 71.43% |
| Top-3 on covered | 80.00% | 80.00% |
| Regressions | 0 | 0 |

- Cases that bank **only with Δλ** (Scenario 2 but not Scenario 1): `(none)` — this is the price of action **A6 two-point 5-gas**.
- Cases that bank on **electrical alone** (Scenario 1): `['CSV-041', 'CSV-045', 'CSV-123', 'CSV-124', 'ECU-001', 'EXP-N002', 'EXP-N004', 'EXP-N019', 'EXT-221', 'TC-021', 'YAML-CSV41', 'YAML-CSV45', 'YAML-RULE_NOx_1', 'YAML-TC47', 'case_001', 'case_013']` — reachable with the cheaper **A5 electrical bench** (DMM ground drop + KOEO MAP/BARO + Vmod + bidirectional).
- **Δλ is NOT load-bearing for yield on this seed:** Scenario 1 banks the same set as Scenario 2. The expensive, weakest-grounded 5-gas divergence term can be dropped from the C3B column set.

## 3. Consumer simulation (EF/SF overlay)
On `CONTROL_REFERENCE_FAULT`: **EF-001, EF-002, EF-003** (ecu_fault) get a `+0.1` DEFINITIVE boost; **SF-001, SF-002** (sensor_fault) are **pruned** (contract §3 dispersion-as-sensor-bias mapping — a ground offset that *looks* like sensor bias must not out-rank ecu_fault). `ABSTAIN` leaves every rule at baseline. Boost mechanics mirror `v3/c2_signal_sim.py` / `v3/c4_signal_sim.py`.

## 4. Yield disclosure (22 C3 cases, Scenario 2)
| Outcome | Count | Case IDs |
| --- | --- | --- |
| **WOULD_BANK** | 16 | `CSV-041, CSV-045, CSV-123, CSV-124, ECU-001, EXP-N002, EXP-N004, EXP-N019, EXT-221, TC-021, YAML-CSV41, YAML-CSV45, YAML-RULE_NOx_1, YAML-TC47, case_001, case_013` |
| **ALREADY_PASS** | 0 | `(none)` |
| **STILL_SHORT** | 6 | `CASE-039, CSV-125, CSV-126, ECU-009, EXP-N005, EXP-N018` |
| **ABSTAIN_NO_DATA** | 0 | (none — synthetic seed covers all 22) |

### Per-case detail (Scenario 2: full contract)
| Case | Expected | Oracle fault | Band | seed stay_abstained | C3 state (S2) | sub-gate fired | Base hit | Base abst | Sim hit | Sim abst | Winner | Winner fam | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-039 | ecu_fault | ecu_fault_poa_context | C3-POA-CONFOUNDER | True | `ABSTAIN` | (none) | False | True | False | True | RM-001 | rich_mixture | **STILL_SHORT** |
| CSV-041 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| CSV-045 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | False | True | False | EF-003 | ecu_fault | **WOULD_BANK** |
| CSV-123 | ecu_fault | ecu_fault_rich_bias | C3-RICH-BIAS | False | `CONTROL_REFERENCE_FAULT` | rich-bias(map/baro+Δλ) | False | False | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| CSV-124 | ecu_fault | ecu_fault_rich_bias | C3-RICH-BIAS | False | `CONTROL_REFERENCE_FAULT` | rich-bias(map/baro+Δλ) | False | False | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| CSV-125 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | False | False | False | RM-001 | rich_mixture | **STILL_SHORT** |
| CSV-126 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | True | False | True | MF-001 | misfire | **STILL_SHORT** |
| ECU-001 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| ECU-009 | ecu_fault | ecu_fault_poa_context | C3-POA-CONFOUNDER | True | `ABSTAIN` | (none) | False | False | False | False | RM-001 | rich_mixture | **STILL_SHORT** |
| EXP-N002 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | False | True | True | LC-001 | lean_condition | **WOULD_BANK** |
| EXP-N004 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | False | True | True | LC-001 | lean_condition | **WOULD_BANK** |
| EXP-N005 | ecu_fault | ecu_fault_intermittent_normal_test | C3-INTERMITTENT | True | `ABSTAIN` | (none) | False | True | False | True | CF-001 | catalyst_failure | **STILL_SHORT** |
| EXP-N018 | ecu_fault | ecu_fault_poa_context | C3-POA-CONFOUNDER | True | `ABSTAIN` | (none) | False | False | False | False | SF-001 | sensor_fault | **STILL_SHORT** |
| EXP-N019 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | True | True | True | CF-001 | catalyst_failure | **WOULD_BANK** |
| EXT-221 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| TC-021 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| YAML-CSV41 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | RM-001 | rich_mixture | **WOULD_BANK** |
| YAML-CSV45 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | False | True | False | EF-003 | ecu_fault | **WOULD_BANK** |
| YAML-RULE_NOx_1 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | True | True | False | CF-001 | catalyst_failure | **WOULD_BANK** |
| YAML-TC47 | ecu_fault | ecu_internal_processor_fault | C3-PROCESSOR | False | `CONTROL_REFERENCE_FAULT` | processor(bidir=False+Vmod<12) | False | False | True | False | EF-003 | ecu_fault | **WOULD_BANK** |
| case_001 | ecu_fault | ecu_fault_lean_bias | C3-LEAN-BIAS | False | `CONTROL_REFERENCE_FAULT` | lean-bias(gnd+Δλ) | False | True | True | True | LC-001 | lean_condition | **WOULD_BANK** |
| case_013 | ecu_fault | ecu_fault_rich_bias | C3-RICH-BIAS | False | `CONTROL_REFERENCE_FAULT` | rich-bias(map/baro+Δλ) | False | False | True | True | RM-001 | rich_mixture | **WOULD_BANK** |

**stay_abstained honesty check:** the 4 seed-flagged cases (`CASE-039, ECU-009, EXP-N005, EXP-N018`) MUST land outside WOULD_BANK. Banked: `(none)` — honoured (correct: seeded below every gate).

### Why each STILL_SHORT case fell short
- `CASE-039` (C3-POA-CONFOUNDER): seed stay_abstained: seeded below every producer gate (state ABSTAIN); confounder — C3 signal cannot separate
- `CSV-125` (C3-PROCESSOR): producer fired (CONTROL_REFERENCE_FAULT) but ecu_fault still outside top-3 — the +0.1 boost did not out-rank competitors (top3=['catalyst_failure', 'misfire', 'rich_mixture']); needs a stronger consumer lift at C3B
- `CSV-126` (C3-PROCESSOR): producer fired (CONTROL_REFERENCE_FAULT) but ecu_fault still outside top-3 — the +0.1 boost did not out-rank competitors (top3=['catalyst_failure', 'misfire', 'rich_mixture']); needs a stronger consumer lift at C3B
- `ECU-009` (C3-POA-CONFOUNDER): seed stay_abstained: seeded below every producer gate (state ABSTAIN); confounder — C3 signal cannot separate
- `EXP-N005` (C3-INTERMITTENT): seed stay_abstained: seeded below every producer gate (state ABSTAIN); confounder — C3 signal cannot separate
- `EXP-N018` (C3-POA-CONFOUNDER): seed stay_abstained: seeded below every producer gate (state ABSTAIN); confounder — C3 signal cannot separate

> **Disclosure:** 2 case(s) the seed marks C3-separable (`CSV-125, CSV-126`) fire the producer state but ecu_fault still misses top-3. The paper-separable count (18) therefore exceeds the actual top-3 flips (16): the producer discriminates, but the fixed +0.10 consumer boost is not enough to out-rank the competing family for these rows. C3B must size a stronger lift (or accept them abstained).

## 5. FT-8 neighbour audit
Neighbour union re-derived **live** from `ecu_fault.json` (EF-*) + `sensor_fault.json` (SF-*) `passes_cases` (both competition groups): **48** cases.
- **Regressions (full 294, Scenario 2):** 0 — `(empty)` (target: empty).
- **Dual target+neighbour (18):** these are BOTH C3 targets AND regression-sensitive neighbours (the largest dual set of any pack). Their outcomes:
  - `CSV-041` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `CSV-045` → **WOULD_BANK** (winner EF-003/ecu_fault, C3 state `CONTROL_REFERENCE_FAULT`)
  - `CSV-123` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `CSV-124` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `CSV-125` → **STILL_SHORT** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `CSV-126` → **STILL_SHORT** (winner MF-001/misfire, C3 state `CONTROL_REFERENCE_FAULT`)
  - `ECU-001` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `ECU-009` → **STILL_SHORT** (winner RM-001/rich_mixture, C3 state `ABSTAIN`)
  - `EXP-N002` → **WOULD_BANK** (winner LC-001/lean_condition, C3 state `CONTROL_REFERENCE_FAULT`)
  - `EXP-N004` → **WOULD_BANK** (winner LC-001/lean_condition, C3 state `CONTROL_REFERENCE_FAULT`)
  - `EXP-N005` → **STILL_SHORT** (winner CF-001/catalyst_failure, C3 state `ABSTAIN`)
  - `EXT-221` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `TC-021` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `YAML-CSV41` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)
  - `YAML-CSV45` → **WOULD_BANK** (winner EF-003/ecu_fault, C3 state `CONTROL_REFERENCE_FAULT`)
  - `YAML-TC47` → **WOULD_BANK** (winner EF-003/ecu_fault, C3 state `CONTROL_REFERENCE_FAULT`)
  - `case_001` → **WOULD_BANK** (winner LC-001/lean_condition, C3 state `CONTROL_REFERENCE_FAULT`)
  - `case_013` → **WOULD_BANK** (winner RM-001/rich_mixture, C3 state `CONTROL_REFERENCE_FAULT`)

## 6. Commit scope for `T-V3-P4-C3B` (sized, not guessed)
- **Producer thresholds** (as simulated): lean-bias `gnd>0.20 ∧ Δλ≥0.05`, rich-bias `map_baro≥5 ∧ Δλ≥0.05`, processor `bidir=False ∧ Vmod<12.0`.
- **Consumer changes:** boost EF-001, EF-002, EF-003 on `CONTROL_REFERENCE_FAULT`; prune SF-001, SF-002 on the same state.
- **Column-set decision (Δλ load-bearing?):**
  - Scenario 1 == Scenario 2 on this seed → **Δλ (`gas_obd_lambda_delta`, `lambda_perception_delta`) is NOT load-bearing for yield.** C3B can commit the 4 electrical columns (`koeo_map_baro_delta_kpa`, `module_voltage_loaded_v`, `dlc_signal_ground_drop_v`, `bidirectional_fuel_response_ok_bool`) and defer the expensive, empirical-anecdotal Δλ ask.
- **stay_abstained (4):** stay abstained at MARGIN=0.02 (POA physical confounder + intermittent) — not committable by C3.

> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run runs on `synthetic=true` seed data. The producer/consumer LOGIC is buildable now; the live `top3_family` does **not** move until the owner supplies real column values and `T-V3-P4-C3B` commits them. Never read a synthetic bank as real accuracy.

