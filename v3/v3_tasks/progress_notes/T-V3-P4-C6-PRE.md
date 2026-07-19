# T-V3-P4-C6-PRE — Progress Note

**Task:** C6 reveal-contract instance (read-only)  
**Date:** 2026-07-05  
**Status:** done

## Summary

Instanced the frozen reveal contract for **C6 — sensor fault under-detection**.
Produced:

1. `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md` — human-readable C6
   instance with all 5 reveal-contract sections.
2. `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json` — machine-readable twin.
3. `v3/build_c6_contract.py` — deterministic extractor script (read-only).

Key findings:
- **14 cases** (3 DATA_GAP_ACQUISITION_GAP + 6 OUTRANKED_HARD + 5
  TUNABLE_HELD) — all SCORING_GATED, 0 BUILDABLE_NOW.
- Producer gates cited from `cluster6.md`: `O2_LAZY_OR_BIASED` via Mode $06
  margin or active rich↔lean/lean↔rich response timing, `MAF_UNDERREAD` via
  sustained 10–15% actual-vs-calculated shortfall at idle and 2500 rpm, and
  `SENSOR_HEALTH_UNPROVEN_ABSTAIN` for static-only O2/MAF evidence.
- Grounding disclosed: Mode $06 is standardized transport with vehicle-specific
  numeric limits; active O2 timing is manufacturer-typical; MAF 10–15% is
  empirical-inferred; static-only evidence abstains.
- Consumers named: `sensor_fault.json` SF-005/SF-008/SF-001/SF-002 and
  `no_fault.json` NF-001/NF-002.
- **C3 interaction surfaced:** live C3B `CONTROL_REFERENCE_FAULT` branch prunes
  SF-001/SF-002; C6B must preserve C3 prune precedence unless decisive dynamic
  C6 sensor evidence exists. Static-only C6 evidence must abstain, not undo C3.
- **FT-8 neighbour union = 33 cases** derived live from `sensor_fault.json` (8
  rules) + `no_fault.json` (2 rules). **9 dual target+neighbour** cases.
- Confounders disclosed: upstream exhaust leak/intake disconnection,
  MAF-architecture mismatch, wideband-vs-switching O2 limits, and C4 overlap.
  `PDF-4G-05` is called out as an oracle-misfire/current-sensor lookalike that
  must not be back-solved into a sensor pass.
- Baseline pinned to `V3_YARDSTICK_2026-07-05-C3B` /
  `POST_T_V3_P4_C3B` (CSV hash `9f530695…`, oracle `3088a7c3…`).
- Score unchanged: `top3_family 228/294`, `Hash lock: ok`.

## VERIFICATION GATE — T-V3-P4-C6-PRE

1. Compile : PASS  (`py_compile v3/build_c6_contract.py`)
2. Lint    : PASS  (`ruff check v3/build_c6_contract.py` -> OK)
3. Types   : PASS  (`pyright v3/build_c6_contract.py` -> 0 errors)
4. Tests   : PASS  (report grep gate: 49 matches for `SF-00[1258]|NF-00[12]|MAF_UNDERREAD|O2_LAZY|CONTROL_REFERENCE_FAULT|interaction|abstain`; `score_v3_yardstick.py score` reports `top3_family 228/294`, `Hash lock: ok`)
5. Contract: PASS  (14/14 cases attributed; FT-8 union derived live [33]; every threshold grounding-tagged; C3 interaction rule stated; baseline pin present; read-only — no corpus/engine/yardstick/scorer change)
6. Orphan  : N/A  (no producer/consumer wired — disclosure only; consumer rules named for C6-SYNTH/C6A/C6B inheritance)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C6-PRE

Scope         : PASS  (3 new files under `v3/` — contract md/json + extractor script; no file outside `v3/` touched except progress ledger/note bookkeeping)
Composition   : PASS  (no lab edits, no cross-lab imports, no deferred path, no engine/scorer/corpus/yardstick mutation)
Consumers     : PASS  (no field mapped — disclosure only; exact consumer rules named and evidence fields listed)
Literals      : PASS  (thresholds cite `cluster6.md` lines 114–118, 147–161, 171–174 and acq-spec §C6 line 93; weak numeric grounding disclosed instead of laundered)
Docstrings    : PASS  (module docstring + public functions documented)
Craft (WARN)  : Depth — single-purpose read-only extractor; no diagnostic runtime logic. Deletion — no unused scaffolding; script is the regeneration source for both report twins. Seam — no mapping or scoring logic leaks into wired/runtime. Interface — verification exercises the extractor, report structural grep, JSON reconciliation, and public scoreboard.
Result: CLEAN

## Guardrails honoured

Read-only · no corpus column · no producer/consumer wiring · no rules/weights/shim edit · no synthetic values · no yardstick mint · score unchanged · `run_suite.py` untouched · `Vault/` untouched · no `graphify`/frozen-graph rebuild · no secrets.
