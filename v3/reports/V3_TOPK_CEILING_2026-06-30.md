# V3_TOPK_CEILING -- correct-in-top-1 / top-2 / top-3 measured from frozen trace

**Task:** `T-V3-0`  **Date:** 2026-06-30  **Source:** `v3/measure_topk.py`
**Inputs:** trace spans (294 accuracy cases, 73 rules mapped, FL localization modes)
**Mode:** measurement-only -- zero engine/oracle/CSV edits.

---

## 1. Headline

| Metric | Accuracy (294) |
|---|---|
| top-1 (single verdict) | 141/294 (47.96%) |
| top-2 | 161/294 (54.76%) |
| top-3 | 175/294 (59.52%) |

top-1 = 141/294 (47.96%) reproduces frozen baseline (141/294 = 47.96%).

---

## 2. Per-family top-3

| Family | n | t1 | t2 | t3 |
|---|---:|---:|---:|---:|
| cam_timing | 11 | 7 | 9 | 9 |
| catalyst_failure | 23 | 9 | 12 | 15 |
| ecu_fault | 31 | 4 | 8 | 9 |
| exhaust_leak | 10 | 0 | 0 | 0 |
| ignition_fault | 4 | 1 | 3 | 3 |
| lean_condition | 62 | 37 | 41 | 43 |
| mechanical_wear | 14 | 0 | 1 | 1 |
| misfire | 54 | 46 | 47 | 51 |
| no_fault | 18 | 8 | 8 | 8 |
| non_starter | 5 | 0 | 0 | 0 |
| rich_mixture | 37 | 23 | 24 | 27 |
| sensor_fault | 25 | 6 | 8 | 9 |
**TOTAL** | **294** | **141** | **161** | **175** |

---

## 3. Per-mode (FL) breakdown

| Mode | n | t1 | t2 | t3 | t3% |
|---|---:|---:|---:|---:|---:|
| SURFACE_DEFECT | 133 | 133 | 133 | 133 | 133/133 (100.00%) |
| OUTRANKED | 107 | 8 | 26 | 38 | 38/107 (35.51%) |
| ORACLE_SUSPECT | 10 | 0 | 1 | 1 | 1/10 (10.00%) |
| PRODUCER_GAP | 25 | 0 | 1 | 3 | 3/25 (12.00%) |
| DATA_GAP | 19 | 0 | 0 | 0 | 0/19 (0.00%) |

---

## 4. OUTRANKED outside top-3 (n=69)

Case IDs: CASE-014, CASE-015, CASE-020, CASE-022, CSV-025, CSV-041, CSV-045, CSV-095, CSV-100, CSV-113, CSV-114, CSV-121, CSV-122, CSV-123, CSV-124, CSV-129, CSV-130, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N014, EXP-N017, EXP-N018, EXP-N019, EXP-N020, EXP-N027, EXT-207, EXT-211, EXT-212, EXT-221, EXT-229, EXT-230, EXT-232, EXT-233, EXT-238, EXT-239, PDF-4G-04, PDF-4G-05, PDF-HI-006, PDF-HI-007, REAL-004, TC-021, TC-046, TC-048, YAML-CSV25, YAML-CSV41, YAML-CSV45, YAML-CSV95, YAML-PDF_4G_01, YAML-TC47, case_001, case_004, case_006, case_013, case_044, case_046, era1_001, era1_006, era1_016, era1_017, era2_011, era2_012, era2_015, era2_016, era3_007, era3_015, era3_019

---

## 5. V3 arithmetic (measured)

**Measured from frozen trace (correct-in-top-3):**

| Bucket | Top-3 hits |
|---|---|
| SURFACE_DEFECT (#1, counted) | 133 |
| OUTRANKED (in top-3 vs outside) | 38 in-top-3, 69 outside-top-3 |
| ORACLE_SUSPECT (re-pin needed) | 10 |
| **Measurable achievable** | **181 / 294 = 61.56%** |
| PRODUCER_GAP (requires signal) | 25 |
| DATA_GAP (requires signal) | 19 |

Bottom line: 69/107 OUTRANKED cases need ranker tuning;
the remaining 38 recoverable by scorer reframing alone.

---

## 6. Abstain recommendation

Close-margin wrong top-1 cases (<0.03 gap): 64.
Recommend: abstain_floor at winner_score <0.80, abstain_margin <0.05.

---
*Generated: 20260630_202643*
