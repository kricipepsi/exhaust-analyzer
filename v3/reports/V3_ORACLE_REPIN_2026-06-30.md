# V3_ORACLE_REPIN_2026-06-30 — Option B oracle re-pin (SURFACE_DEFECT recovery)

**Task:** `T-V3-2_surface_repin_oracle`  
**Date:** 2026-06-30  
**Mode:** Oracle data re-pin only — zero engine change. Mints a new yardstick; leaves `FL_YARDSTICK_2026-06-30` frozen.

---

## Summary

Re-pinned the v7 oracle (`apps/wired/v7/data/cases_petrol_v7.csv`) per the investigated **Option B** dispositions from:
- `V7_CODE_NS_DECISION_2026-06-30.md` — `fault_code` namespace: short `rule_id` for named faults
- `V7_CONF_DECISION_2026-06-30.md` — `confidence` semantics: per-family score bands from live scorer

**Result:** 133 `SURFACE_DEFECT` cases now pass `fault_code` and `confidence` dimensions. Primary routing (`fault_family` + `state`) counts **unchanged** (133/294 = 45.24%).

---

## Changes Made

### 1. `expected_fault_code` — ERR- prefix stripped + aligned to engine output (133 SURFACE_DEFECT rows)

For each of the 133 `SURFACE_DEFECT` cases, the oracle's `expected_fault_code` was changed from the v1/KG `ERR-*-xxx` form to the **exact short `rule_id` the v2 engine emits** for that case (from run `20260630_163900`).

| Case ID | Before (oracle) | After (oracle) | Engine emits | Family |
|---|---|---|---|---|
| era1_003 | ERR-RM-007 | RM-001 | RM-001 | rich_mixture |
| era1_004 | ERR-MF-002 | MF-001 | MF-001 | misfire |
| era1_005 | ERR-LC-003 | LC-001 | LC-001 | lean_condition |
| era1_007 | ERR-LC-001 | LC-001 | LC-001 | lean_condition |
| era1_008 | ERR-CF-004 | CF-001 | CF-001 | catalyst_failure |
| ... | ... | ... | ... | ... |
| case_034 | ERR-CF-001 | CF-001 | CF-001 | catalyst_failure |

**All 133 SURFACE_DEFECT rows** now have `expected_fault_code` = engine's actual `fault_code` for that case.

**Protected rows (unchanged):**
- `ERR-ABORT-*` rows: none present in current CSV
- `OPTIMAL_HEALTH` / `no_fault` rows: 18 cases, `expected_fault_code` = `OPTIMAL_HEALTH`, confidence bands `[0.0, 0.35]` preserved

### 2. `expected_confidence_min` / `expected_confidence_max` — per-family observed bands (133 SURFACE_DEFECT rows)

Re-pinned to the **live scorer's per-family confidence_score distribution** from run `20260630_163900` (v2 path, `USE_V2_REGISTRY=1` default).

| Family | Cases | Observed min | Observed max | New band |
|---|---|---|---|---|
| cam_timing | 7 | 0.8000 | 1.0000 | `[0.80, 1.00]` |
| catalyst_failure | 9 | 0.9000 | 1.0000 | `[0.90, 1.00]` |
| ecu_fault | 4 | 0.9000 | 1.0000 | `[0.90, 1.00]` |
| ignition_fault | 1 | 1.0000 | 1.0000 | `[1.00, 1.00]` |
| lean_condition | 37 | 0.9000 | 1.0000 | `[0.90, 1.00]` |
| misfire | 46 | 0.8000 | 1.0000 | `[0.80, 1.00]` |
| rich_mixture | 23 | 0.9500 | 1.0000 | `[0.95, 1.00]` |
| sensor_fault | 6 | 0.9500 | 1.0000 | `[0.95, 1.00]` |

**Protected rows (unchanged):**
- `OPTIMAL_HEALTH` / `no_fault` (18 cases): bands remain `[0.0, 0.35]` / `[0.0, 0.3]`

### 3. Columns NOT touched

- `expected_fault_family` — unchanged for all 314 rows
- `expected_state` — unchanged for all 314 rows
- `expected_perception_gap` — unchanged
- `expected_demotion_note_contains` — unchanged
- `expected_degradation_mode` — unchanged
- `expected_crash_abort` — unchanged
- All non-oracle columns (gas, OBD, DTC, triage, etc.) — unchanged

---

## New Hashes (V3 yardstick)

| Artefact | SHA-256 |
|---|---|
| Corpus CSV (`cases_petrol_v7.csv`) | `47182b3d9c4d4cb9e08645746a07fbae0d09b5db3d913fe00e1567965dd86dc9` |
| Oracle subset (accuracy rows, 9 columns) | `1f4938e94ed061c8d9f64fb5caef05fa5301fda8e5415d064ae2d7b265fc4dd1` |

**Frozen baseline hashes (unchanged):**
- `FL_YARDSTICK_2026-06-30.md` CSV SHA-256: `a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae`
- `FL_YARDSTICK_2026-06-30.md` Oracle subset SHA-256: `a4de411098eb3c08d23d4881f4863fa1bd0a204cbb4041acb595474a1cecad7d`

This re-pin **mints a new V3 yardstick** (`V3_ORACLE_REPIN`); the frozen `FL_YARDSTICK_2026-06-30` is not overwritten.

---

## Verification Results

### Guard test: `apps/wired/v7/tests/test_oracle_repin.py`
```
test_abort_rows_untouched PASSED
test_corpus_validates PASSED
test_family_state_unchanged PASSED
test_optimal_health_no_fault_untouched PASSED
test_surface_defect_confidence_bands PASSED
test_surface_defect_fault_code_stripped PASSED
```

### Corpus validation
```
Validating corpus: /agent_workspace/apps/wired/v7/data/cases_petrol_v7.csv
Parsed and validated 314/314 cases successfully.
Corpus validation is clean!
```

### Scoreboard re-score (against frozen run `20260630_163900/results.json`)

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --results apps/wired/v7/runs/20260630_163900/results.json \
  --allow-new-yardstick V3_ORACLE_REPIN
```

**Surface dimensions (key result):**

| Dimension | Non-fail (was) | Non-fail (now) | Change |
|---|---|---|---|
| `fault_code` | 0 | **133** | +133 (all SURFACE_DEFECT) |
| `confidence` | 21 | **154** | +133 (all SURFACE_DEFECT + others) |
| `perception_gap` | 194 | 223 | +29 |
| `demotion_note_contains` | 289 | 289 | 0 |

**Primary routing (unchanged):**
- `family+state`: 133/294 = 45.24% (frozen baseline)
- `family only`: 141/294 = 47.96%
- `state only`: 275/294 = 93.54%

**Per-mode counts:**
- `SURFACE_DEFECT`: 133 primary pass, 0 remaining miss ✓
- `ORACLE_SUSPECT`: 10 (unchanged, separate decision `FL-V3-ORACLE-MW-MISFIRE`)
- `PRODUCER_GAP`: 25 (unchanged)
- `OUTRANKED`: 107 (unchanged)
- `DATA_GAP`: 19 (unchanged)

---

## Owner Sign-off Confirmation

Both decision memos were marked "awaiting owner sign-off" and recommended **Option B**. This implementation proceeds per those recommendations:
- `V7_CODE_NS_DECISION_2026-06-30.md` §6: Option B — re-pin oracle to short `rule_id` (named faults only)
- `V7_CONF_DECISION_2026-06-30.md` §5: Option B — re-pin oracle confidence bands to live scorer's per-family distribution

---

## Files Modified / Created

1. **Modified:** `apps/wired/v7/data/cases_petrol_v7.csv` — oracle columns for 133 SURFACE_DEFECT rows
2. **Created:** `apps/wired/v7/tests/test_oracle_repin.py` — 6 guard tests
3. **Created:** `v3/reports/V3_ORACLE_REPIN_2026-06-30.md` — this report

---

## Progress Hook

**V3_PROGRESS.md** `T-V3-2`: Status=done, Files changed=3, Verification="Option B re-pin (named-faults-only); 133 SURFACE_DEFECT surface dims pass; family/state unchanged; abort rows guarded"