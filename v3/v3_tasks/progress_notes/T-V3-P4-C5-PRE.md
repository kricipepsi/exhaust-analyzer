# T-V3-P4-C5-PRE — Progress Note

**Task:** C5 reveal-contract instance (read-only)  
**Date:** 2026-07-05  
**Status:** done

## Summary

Instanced the frozen reveal contract for **C5 — lean-condition root cause**.
Produced:

1. `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.md` — human-readable C5
   instance with all 5 reveal-contract sections.
2. `v3/reports/V3_C5_REVEAL_CONTRACT_2026-07-05.json` — machine-readable twin.
3. `v3/build_c5_contract.py` — deterministic extractor script (read-only).

Key findings:
- **10 cases** (5 DATA_GAP_ACQUISITION_GAP + 4 OUTRANKED_HARD + 1
  TUNABLE_HELD) — all SCORING_GATED, 0 BUILDABLE_NOW.
- Producer gates cited from `cluster5.md`: `VACUUM_LEAK_TRIM_PATTERN` via positive trims
  at idle that recover at 2500 RPM, `FUEL_DELIVERY_SHORTFALL` via WOT fuel rail pressure drop
  > 35 kPa and wide-range lambda > 1.05, `MAF_UNDERREAD` via WOT suppressed Calculated Engine
  Load < 80% with positive trims, and `SENSOR_HEALTH_UNPROVEN_ABSTAIN` for static-only or
  idle-only trim evidence.
- Grounding disclosed: fuel trim delta (ΔTFT) is empirical; Calculated Engine Load (80%)
  and fuel rail pressure drop (35 kPa) are manufacturer-typical / OEM-typical; WOT wide-range
  lambda (> 1.05) is standardized; static-only trims produce `SENSOR_HEALTH_UNPROVEN_ABSTAIN`.
- Consumers named: `lean_condition.json` LC-001/LC-002/LC-003, `vacuum_leak.json` VL-001/VL-002/VL-003,
  and `exhaust_leak.json` EL-001.
- **C6-MAF-collision disclosed:** Both C6 `SensorDynamicsState` and C5 `LeanRootCauseState`
  can emit a MAF-underread verdict from the same MAF columns, but attribute to different
  families (sensor_fault vs lean_condition). C6's sensor-attribution must require its Mode $06/dynamics
  evidence; C5's requires the trim+load pattern; neither fires on MAF delta alone. If both are present,
  C5 takes precedence. Lands in `integration_shim.py::_score_rule` after C3 and C6 branches.
- **C3 interaction surfaced:** live C3B `CONTROL_REFERENCE_FAULT` branch prunes
  SF-001/SF-002; C5B must preserve C3 prune precedence and static-only C5 evidence must abstain.
- **ALREADY-LIVE-COLUMN AUDIT:** Of the 11 required C5 columns, 6 already exist in the active
  schema (4 trims from C2B, 2 MAF from C6B). Genuinely new ask shrank to 5 columns
  (`stft_load_pct, ltft_load_pct, calc_load_wot_pct, fuel_rail_pressure_load_kpa, wideband_lambda_wot`).
  For C5 rows, the live columns exist in the schema but are currently empty.
- **FT-8 neighbour union = 68 cases** derived live from `lean_condition.json` (3 rules) +
  `vacuum_leak.json` (3 rules) + C3 lean-bias winners (`EXP-N002, EXP-N004, case_001`) currently
  winning under `LC-001/LC-002`. **2 dual target+neighbour** cases (`EXP-N011, case_003`).
- Confounders disclosed: EGR stuck open lookalikes (`CSV-113, CSV-114, REAL-004, era1_001`
  expecting `ERR-LC-005` but currently winning `misfire/MF-001`) must not be back-solved. PCV
  pressure sensor drift `era3_015` is TUNABLE_HELD. Exhaust leaks, misfires, speed-density,
  and C4 overlap are also confounders.
- Baseline pinned to `V3_YARDSTICK_2026-07-05-C6B` /
  `POST_T_V3_P4_C6B` (CSV hash `bf739368…`, oracle `3088a7c3…`).
- Score unchanged: `top3_family 241/294`, `Hash lock: ok`.

## VERIFICATION GATE — T-V3-P4-C5-PRE

1. Compile : PASS  (`py_compile v3/build_c5_contract.py`)
2. Lint    : PASS  (`ruff check v3/build_c5_contract.py` -> OK)
3. Types   : PASS  (`pyright v3/build_c5_contract.py` -> 0 errors)
4. Tests   : PASS  (report grep gate: 18 matches for `LC-00[123]|VACUUM_LEAK_TRIM_PATTERN|FUEL_DELIVERY_SHORTFALL|MAF_UNDERREAD|collision|already-live|35 kPa|80`; `score_v3_yardstick.py score` reports `top3_family 241/294`, `Hash lock: ok`)
5. Contract: PASS  (10/10 cases attributed; FT-8 union derived live [68]; every threshold grounding-tagged; C6-MAF collision + C3 interaction rule stated; baseline pin present; read-only — no corpus/engine/yardstick/scorer change)
6. Orphan  : N/A  (no producer/consumer wired — disclosure only; consumer rules named for C5-SYNTH/C5A/C5B inheritance)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C5-PRE

Scope         : PASS  (3 new files under `v3/` — contract md/json + extractor script; no file outside `v3/` touched except progress ledger/note bookkeeping)
Composition   : PASS  (no lab edits, no cross-lab imports, no deferred path, no engine/scorer/corpus/yardstick mutation)
Consumers     : PASS  (no field mapped — disclosure only; exact consumer rules named and evidence fields listed)
Literals      : PASS  (thresholds cite `cluster5.md` lines 127–129, 131–133, 135–137, 139–141, 155–159, 166 and acq-spec §C5 line 53; weak numeric grounding disclosed instead of laundered)
Docstrings    : PASS  (module docstring + public functions documented)
Craft (WARN)  : Depth — single-purpose read-only extractor; no diagnostic runtime logic. Deletion — no unused scaffolding; script is the regeneration source for both report twins. Seam — no mapping or scoring logic leaks into wired/runtime. Interface — verification exercises the extractor, report structural grep, JSON reconciliation, and public scoreboard.
Result: CLEAN

## Guardrails honoured

Read-only · no corpus column · no producer/consumer wiring · no rules/weights/shim edit · no synthetic values · no yardstick mint · score unchanged · `run_suite.py` untouched · `Vault/` untouched · no `graphify`/frozen-graph rebuild · no secrets.
