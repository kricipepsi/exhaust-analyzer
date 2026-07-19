# T-V3-P4-C3-PRE — Progress Note

**Task:** C3 reveal-contract instance (read-only)
**Date:** 2026-07-05
**Status:** done

## Summary

Instanced the frozen reveal contract for **C3 — ECU/control-system fault**.
Produced:

1. `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.md` — human-readable C3
   instance with all 5 reveal-contract sections.
2. `v3/reports/V3_C3_REVEAL_CONTRACT_2026-07-05.json` — machine-readable twin.
3. `v3/build_c3_contract.py` — deterministic extractor script (read-only).

Key findings:
- **22 cases** (18 OUTRANKED_HARD + 3 PRODUCER_GAP_SIGNAL_REQUIRED + 1
  CLASSIFIER_FIXABLE_REROUTED [CASE-039]) — all SCORING_GATED, 0 BUILDABLE_NOW.
- **6 producer thresholds** cited from `cluster3_prepped.md` §Quantitative
  Diagnostic Signature Mapping lines 183–188; grounding-tagged (1 empirical-
  anecdotal [Δλ ≥ 0.05], 3 manufacturer-typical, 2 standardized).
- **EF-001/EF-002/EF-003 + SF-001/SF-002** consumer mapping named.
- **FT-8 neighbour union = 48 cases** derived live from `ecu_fault.json` (5
  rules) + `sensor_fault.json` (8 rules). **18 dual target+neighbour** cases.
- **2 confounders** (upstream exhaust leaks, severe misfires) disclosed as
  mimic risk per `cluster3_prepped.md` §Conditions Under Which Signatures May
  Fail.
- Baseline pinned to `V3_YARDSTICK_2026-07-05` / `POST_T_V3_P4_C2B`.
- Score unchanged: `top3_family 212/294`, `Hash lock: ok`.

## VERIFICATION GATE — T-V3-P4-C3-PRE

1. Compile : PASS  (v3/build_c3_contract.py)
2. Lint    : PASS  (ruff, 0 issues)
3. Types   : PASS  (pyright, 0 errors)
4. Tests   : PASS  (grep gate: 17 matches for EF-00[123]|SF-00[12]|0.05|5 kPa|0.20 V|0.10 V|anecdotal|CASE-039; score_v3_yardstick: top3_family 212/294, Hash lock: ok)
5. Contract: PASS  (22/22 cases attributed; FT-8 union derived live [48]; every threshold grounding-tagged; baseline pin present; read-only — no corpus/engine/yardstick/scorer change)
6. Orphan  : N/A  (no producer/consumer wired — disclosure only)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C3-PRE

Scope         : PASS  (3 new files under v3/ — contract md/json + extractor script; no file outside v3/ touched)
Composition   : PASS  (no lab edits, no cross-lab imports, no deferred path)
Consumers     : PASS  (no field mapped — disclosure only; consumer rules named but not edited)
Literals      : PASS  (all thresholds cited to cluster3_prepped.md lines 183–188)
Docstrings    : PASS  (module docstring + all public functions documented)
Craft (WARN)  : Extractor mirrors C2's `build_reveal_contract.py` structure instead of extending it — acceptable because the task spec says "CREATE `v3/build_c3_contract.py` — do not fork shared logic silently" and the C2 script is C2-specific (its constants, case-split, FT-8 all hardcode C2 families). Shared logic is the reveal-contract template sections (identical between both scripts). No depth/deletion/seam concern — single-purpose read-only script.
Result: CLEAN
