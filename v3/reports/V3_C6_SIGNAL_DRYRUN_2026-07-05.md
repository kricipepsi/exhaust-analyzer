---
node_type: report
lab: apps/wired
module: v3/c6_signal_sim.py
implements: T-V3-P4-C6A
consumers: [owner acceptance read, next-decision C6B commit sizing]
tags: [v3, phase4, c6, signal, dryrun, synthetic]
source: v3/v3_tasks/T-V3-P4-C6A_c6_signal_dryrun.md
---

# V3 C6 SIGNAL DRYRUN — Sensor fault under-detection (read-only sim)

**Task:** [[T-V3-P4-C6A_c6_signal_dryrun]] · **Date:** 2026-07-05 · **Mode:** STRICT (read-only sim)
**Baseline pin:** `POST_T_V3_P4_C3B` / `V3_YARDSTICK_2026-07-05-C3B` (csv `9f530695…`, oracle `3088a7c3…`, `run_suite.py` untouched)
**C6 Seed:** `v3/data/c6_synthetic_seed_2026-07-05.json` (`synthetic=true`; 13 separable + `PDF-4G-05` stay-abstained)
**Live engine status:** untouched (no corpus / rule / registry / yardstick edit)

## Headline
- **Baseline `top3_family`:** 228/294 → **Scenario 3: 241/294** (+13).
- **Yield split (Scenario 3, 14 C6 cases):** 13 WOULD_BANK / 0 ALREADY_PASS / 1 STILL_SHORT / 0 ABSTAIN_NO_DATA.
- **Covered-vs-masked at MARGIN=0.02:** 8 covered / 5 still-abstained among WOULD_BANK.
- **Scenario ladder WOULD_BANK:** S1 Mode$06=12; S2 +O2 timing=12; S3 +MAF=13.
- **Zero-overlay self-check:** drift = 0 across 294 vs `POST_T_V3_P4_C3B`.
- **FT-8 regressions:** 0 full-corpus regressions; 0 no_fault-neighbour regressions.
- **`PDF-4G-05` back-solve alarm:** banked = `(none)` — honoured.
- **C3 precedence assertion:** dual C3+C6 decisive state cases = `(none)`.

`WOULD_BANK` means the expected family flips into the 3-distinct-family top-3 window. A flipped case may still be hidden by the abstain dial; that split is disclosed above.

## 1. Producer simulation (`SensorDynamicsState`)
Per C6-PRE §2: decisive dynamic evidence emits `O2_LAZY_OR_BIASED` or `MAF_UNDERREAD`; static-only / healthy dynamics emit `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.
- `O2_LAZY_OR_BIASED`: Mode $06 margin ≤ 10% OR rich→lean / lean→rich response ≥ 600 ms.
- `MAF_UNDERREAD`: measured-vs-calculated MAF delta ≤ -15% at BOTH idle and 2500 rpm; `None` MAF columns make the MAF gate not applicable.
- `SENSOR_HEALTH_UNPROVEN_ABSTAIN`: neither dynamic O2 nor two-point MAF gate fires.

## 2. Column-subset scenario ladder
| Metric | S1 Mode$06 only | S2 + O2 timing | S3 full (+ MAF) |
| --- | ---: | ---: | ---: |
| Top-3 family hits | 240/294 | 240/294 | 241/294 |
| WOULD_BANK | **12** | **12** | **13** |
| Already pass | 0 | 0 | 0 |
| Still short | 2 | 2 | 1 |
| Covered WOULD_BANK | 7 | 7 | 8 |
| Still-abstained WOULD_BANK | 5 | 5 | 5 |
| Regressions | 0 | 0 | 0 |

- S2-only banks over S1: `(none)`.
- S3-only banks over S2: `['EXP-N020']`.
- Full S3 bank set: `['CASE-014', 'CASE-045', 'CASE-048', 'CSV-025', 'EXP-N020', 'EXT-229', 'EXT-230', 'TC-046', 'YAML-CSV25', 'YAML-TC46', 'case_046', 'era1_006', 'era2_012']`.

## 3. Consumer simulation with C3 precedence
On decisive C6 states (`O2_LAZY_OR_BIASED` / `MAF_UNDERREAD`), the overlay boosts SF-005, SF-008, SF-001, SF-002 by +0.1 and prunes NF-001, NF-002. On `SENSOR_HEALTH_UNPROVEN_ABSTAIN`, it applies no boost and no NF prune.

C3 precedence is asserted in-sim: live C3 control-reference state and decisive C6 dynamic state are disjoint today. If any future row carries both, C6B must implement the precedence inside `integration_shim.py::_score_rule`: C3 prune first; only decisive C6 dynamics may re-enable/boost SF-001/SF-002; static-only C6 must preserve the C3 prune.

## 4. Yield disclosure (14 C6 cases, Scenario 3)
| Outcome | Count | Case IDs |
| --- | ---: | --- |
| **WOULD_BANK** | 13 | `CASE-014, CASE-045, CASE-048, CSV-025, EXP-N020, EXT-229, EXT-230, TC-046, YAML-CSV25, YAML-TC46, case_046, era1_006, era2_012` |
| **ALREADY_PASS** | 0 | `(none)` |
| **STILL_SHORT** | 1 | `PDF-4G-05` |
| **ABSTAIN_NO_DATA** | 0 | `(none)` |

### Per-case detail (Scenario 3 full contract)
| Case | Expected | Oracle code | Band | Seed emit | S1 | S2 | S3 | Gate fired | Base hit | Base winner | Sim hit | Sim abst | Winner | Winner fam | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CASE-014 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | EL-001/exhaust_leak | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| CASE-045 | sensor_fault | ERR-SF-005 | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | MF-001/misfire | True | True | MF-001 | misfire | **WOULD_BANK** |
| CASE-048 | sensor_fault | ERR-SF-005 | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | MF-001/misfire | True | True | MF-001 | misfire | **WOULD_BANK** |
| CSV-025 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | RM-001/rich_mixture | True | True | SF-008 | sensor_fault | **WOULD_BANK** |
| EXP-N020 | sensor_fault | ERR-SF-004 | C6-MAF-UNDERREAD | MAF_UNDERREAD | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `MAF_UNDERREAD` | maf_delta_both<=-15% | False | RM-001/rich_mixture | True | False | RM-001 | rich_mixture | **WOULD_BANK** |
| EXT-229 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | EL-001/exhaust_leak | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| EXT-230 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | NF-001/no_fault | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| PDF-4G-05 | misfire | ERR-MF-005 | C6-HEALTHY-LOOKALIKE-MISFIRE | SENSOR_HEALTH_UNPROVEN_ABSTAIN | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | `SENSOR_HEALTH_UNPROVEN_ABSTAIN` | (none — abstain/healthy) | False | SF-002/sensor_fault | False | False | SF-002 | sensor_fault | **STILL_SHORT** |
| TC-046 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | RM-001/rich_mixture | True | True | SF-008 | sensor_fault | **WOULD_BANK** |
| YAML-CSV25 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | NF-001/no_fault | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| YAML-TC46 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | MF-005/misfire | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| case_046 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | NF-001/no_fault | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| era1_006 | sensor_fault | ERR-SF-001 | C6-O2-LAZY | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | NF-001/no_fault | True | False | SF-001 | sensor_fault | **WOULD_BANK** |
| era2_012 | sensor_fault | ERR-SF-005 | C6-O2-IMPLAUSIBLE-NORMAL-CHEM | O2_LAZY_OR_BIASED | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | `O2_LAZY_OR_BIASED` | mode06_margin<=10% ; rich_to_lean>=600ms ; lean_to_rich>=600ms | False | RM-001/rich_mixture | True | True | SF-008 | sensor_fault | **WOULD_BANK** |

### Why each STILL_SHORT case fell short
- `PDF-4G-05` (C6-HEALTHY-LOOKALIKE-MISFIRE): seed stay-abstained: healthy C6 dynamics; PDF-4G-05 banking would be a back-solve alarm

## 5. FT-8 neighbour audit
Neighbour union re-derived live from `sensor_fault.json` + `no_fault.json` `passes_cases`: **33** cases.
- Dual target+neighbour: **9** — `['CASE-014', 'CSV-025', 'EXP-N020', 'EXT-229', 'EXT-230', 'TC-046', 'YAML-CSV25', 'YAML-TC46', 'case_046']`.
- Full-corpus regressions (Scenario 3): **0** — `(empty)`.
- FT-8 neighbour regressions: `(empty)`.
- no_fault rule neighbours (13): `['CASE-009', 'CSV-001', 'CSV-005', 'EXT-220', 'EXT-231', 'PDF-HI-005', 'PDF-HI-010', 'YAML-CSV5', 'YAML-PDF_HI_005', 'YAML-TC1', 'case_012', 'case_028', 'case_049']`.
- no_fault neighbours currently passing at baseline: `['CASE-009', 'CSV-001', 'CSV-005', 'EXT-220', 'EXT-231', 'YAML-CSV5', 'case_028']`.
- no_fault-neighbour regressions: `(empty)`.
- Healthy no_fault cases regressed to a fault winner: `(empty)`.

Per-rule live `passes_cases` counts:

| Rule | Count |
| --- | ---: |
| NF-001 | 12 |
| NF-002 | 1 |
| SF-001 | 5 |
| SF-002 | 3 |
| SF-003 | 3 |
| SF-004 | 1 |
| SF-005 | 3 |
| SF-006 | 1 |
| SF-007 | 3 |
| SF-008 | 5 |

## 6. Commit scope for `T-V3-P4-C6B` (sized, not guessed)
- **Producer gates simulated:** Mode $06 margin ≤ 10%; O2 response ≥ 600 ms; two-point MAF delta ≤ -15% at both points.
- **Consumer deltas simulated:** boost SF-005, SF-008, SF-001, SF-002 by +0.1; prune NF-001, NF-002 only on decisive dynamic C6 evidence; abstain state is no-op.
- **Column-set pricing:**
  - Scenario 1 banked 12; Scenario 2 banked 12; Scenario 3 banked 13.
  - MAF columns are load-bearing for: `['EXP-N020']`.
  - If C6B wants the MAF-underread row, it needs the six MAF/airflow columns; otherwise Mode $06 + O2 timing carries the O2-lazy rows.
- **Precedence implementation point:** `integration_shim.py::_score_rule`, after the live C3 branch has computed/pruned and before any C6 SF/NF overlay returns a score.

> **CODE_LANDED ≠ SCORE_MOVED.** This dry-run uses `synthetic=true` data. Live `top3_family` stays 228/294 until C6B commits real/accepted columns and mints a new yardstick.
