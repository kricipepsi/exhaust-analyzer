# P6 Calibration Log — T-P6-2

**Date:** 2026-05-10
**Pre-calibration dual-run:** 393 schema_gap, 7 threshold_tweak, 0 expected_drift, 0 blocker
**Post-calibration dual-run:** 0 schema_gap, 334 threshold_tweak, 54 expected_drift, 12 blocker
**Layer-2 family accuracy:** 4.8% (19/400)

## Changes Made

### 1. Dual-run classification fixes (`tools/dual_run_v1_v2.py`)

- **Added `_resolve_v1_fault()`**: Resolves V1 fault IDs through `label_aliases.yaml` before comparison, so renamed/restructured V1 nodes are correctly classified.
- **Added `label_aliases.yaml` to `_load_v2_fault_ids()`**: Alias targets (non-null) are included in the valid V2 fault ID set. The valid set grew from ~116 to 205 IDs.
- **Fixed `_classify()`**: Excludes `invalid_input` from schema_gap check (state value, not fault ID); resolves V1 fault through aliases before all comparisons.

### 2. Missing alias additions (`schema/v2/label_aliases.yaml`)

11 new entries added (144 → 155 total):

| V1 ID | V2 Target | Reason |
|---|---|---|
| `pcv_fault` | `PCV_System_Fault` | V1 family → V2 specific fault |
| `no_fault` | null | L19: insufficient_evidence instead |
| `invalid_input` | null | VL handles validation |
| `ignition_fault` | `Ignition_Timing_Fault` | V1 family → V2 fault |
| `cam_timing` | `Cam_Timing_Retard_Late` | V1 family → V2 fault |
| `ns_lean_no_start` | `Non_Starter_Fault` | V1 sub-type → V2 family |
| `ns_flooded` | `Non_Starter_Fault` | V1 sub-type → V2 family |
| `ns_no_fuel` | `Non_Starter_Fault` | V1 sub-type → V2 family |
| `ns_mechanical_partial` | `Non_Starter_Fault` | V1 sub-type → V2 family |
| `fuel_delivery_low` | `Fuel_Delivery_Low` | V1 snake_case → V2 |
| `cam_timing_retard_late` | `Cam_Timing_Retard_Late` | V1 snake_case → V2 |

### 3. Corpus replay alias resolution (`dev/run_corpus.py`)

Added `_load_alias_map()` to resolve `expected_top_fault` and `expected_top_fault_family` through aliases before accuracy comparison. Family accuracy improved from 0% to 4.8%.

## Remaining Issues

### 12 Blockers — V2 returns insufficient_evidence where V1 named fault

All 12 cases share the same pattern: V2 state=`insufficient_evidence`, V1 state=`named_fault`, expected fault matches V1 family. V2 is being appropriately cautious (L16 confidence ceiling working correctly), but the underlying evidence vector is too weak.

| Case IDs | Expected Family | Pattern |
|---|---|---|
| CSV-095, YAML-CSV95 | Exhaust_Air_Leak | V2=Fuel_Delivery_Low/insufficient_evidence |
| REAL-004, CSV-113, CSV-114 | EGR_Stuck_Open | V2=Fuel_Delivery_Low/insufficient_evidence |
| EGR-001, EGR-004, EGR-007, EGR-011, EGR-017 | EGR_Stuck_Open | V2=Fuel_Delivery_Low/insufficient_evidence |
| MECH-002 | Head_Gasket_Failure | V2=Fuel_Delivery_Low/insufficient_evidence |
| PDF-4G-03 | Rich_Mixture | V2=Leaking_Injector/insufficient_evidence |

**Root cause:** EGR/Exhaust leak symptoms (`SYM_STUCK_EGR_OPEN_PATTERN`, `SYM_EXHAUST_LEAK_GHOST`) have edge weights to their target faults but these weights don't overcome Fuel_Delivery_Low's broad evidence base when L16 confidence ceiling is applied.

### 334 Threshold Tweaks — V1 vs V2 disagree on specific fault

The dominant failure mode: V2 overwhelmingly returns `Fuel_Delivery_Low` (~62% of cases) and `Catalyst_Failure` (~15%). This is a structural scoring imbalance, not a calibration issue.

**Diagnosis:** `Fuel_Delivery_Low` receives positive edges from 7 symptoms (total combined CF ≈ 0.95 when all active), making it the default high-scorer whenever lean-related symptoms fire. This drowns out more specific faults.

**Required structural fixes (P3/P4):**
- M2 `gas_lab.py`: `SYM_LATE_TIMING_PATTERN` detection needs threshold calibration for Cam_Timing cases
- M4 `kg_engine.py`: Edge weight balance — `Fuel_Delivery_Low` needs stronger inhibitory edges or more specific discriminators
- M3 `arbitrator.py`: Flood control (R8) should limit Fuel_Delivery_Low's score when > 3 sibling symptoms fire

### Layer-2 Accuracy: 4.8% family (target: ≥ 60%)

Gap of 55.2 pp. The structural issues above explain the gap. This cannot be closed through calibration alone.

## Recommended Follow-ups

See `V2_PROGRESS.md` "Unplanned follow-ups — T-P6-2" for the canonical task list. Summary:

1. **T-P6-2b — gas_lab.py**: Tighten symptom thresholds feeding Fuel_Delivery_Low's 7 incoming edges. SYM_LAMBDA_HIGH (λ > 1.03) and SYM_IDLE_STOICH_LOAD_LEAN fire on almost every lean-ish case, producing a near-ceiling CF combination. Add discriminator_gate requiring co-occurrence.

2. **T-P6-2c — kg_engine.py**: Add inhibitory edges from fuel-contradictory symptoms (SYM_DUAL_IMPROVING, SYM_STUCK_EGR_OPEN_PATTERN) → Fuel_Delivery_Low. Today only SYM_DTC_INDUCTION (−0.17) inhibits it.

3. **T-P6-2d — gas_lab.py**: Implement SYM_LATE_TIMING_PATTERN detection. Pattern: HC > 250 ppm + CO2 < 13.5% + O2 < 2.0% + no DTC_P0300. This symptom has a 0.50 edge to Cam_Timing_Retard_Late but is never emitted.

4. **T-P6-2e — kg_engine.py**: Audit whether EGR_Stuck_Open / Exhaust_Air_Leak_Pre_Cat / Head_Gasket_Failure symptom patterns are actually emitted by M2 for the 12 blocker cases. Likely root cause is gas_lab.py thresholds, not edge weights.

## Calibration Assessment

T-P6-2 reached the calibration-only ceiling. Schema_gap eliminated (393 → 0) through alias resolution and classification fixes. Layer-2 family accuracy at 4.8% is the **pre-structural-fix floor** — not a calibration failure, but the baseline from which P3/P4 structural work must lift the engine. The 4.8% → 75% gap is the delta the unplanned follow-ups above are designed to close.
