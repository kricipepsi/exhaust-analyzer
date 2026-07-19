# Progress Note — T-V3-4B: Bounded rule-weight commit (reweight 8 TUNABLE)

Applied the bounded rule-weight lifts for the 8 REWEIGHTABLE TUNABLE cases. Verification via the scorecard shows `top3_family` successfully rose to **184/294** (+8 gain) and `newly_pass` contains exactly the 8 cases, with **no regressions** (`REGRESSIONS: (empty)`) and `Hash lock: ok` preserved.

## Honesty Caveat
The cluster discriminators that diagnostically separate these families are Phase-4 signals absent from the idle snapshot (e.g. two-point fuel-trim delta idle→2500 RPM, Mode $06, CO₂ dilution). Therefore, these weight lifts are prior nudges justified by the oracle ground truth + the cluster research (specifically Clusters 1, 2, 4, 6) — they do not represent real in-snapshot discrimination by the engine. The true diagnostic separation remains the task of the Phase-4 signal packs.

The 12 non-committed TUNABLE cases (1 signal-gated, 6 risky, 5 hard) remain open and route to their respective signal packs, rather than further reweighting.

## VERIFICATION GATE — T-V3-4B
1. Compile : PASS  (5 registry rules modified, labs/comlab/tests/unit/test_tunable_reweight.py created)
2. Lint    : PASS  (ruff check on touched files)
3. Types   : PASS  (pyright, 0 errors in touched files)
4. Tests   : PASS  (pytest labs/comlab -k tunable_reweight -> 2 passed; score_v3_yardstick.py -> top3 184/294)
5. Contract: PASS  (Weights updated, no regressions on overall or per-family verdicts, 8 recovered cases confirmed)
6. Orphan  : N-A  (No new fields mapped; registry weights are loaded dynamically by the existing engine)
Result: CLEAN

## CODE REVIEW — T-V3-4B
Scope         : PASS  (Only deliverables updated: 5 rule files, 1 test file, and results.json generated)
Composition   : PASS  (No engine/lab Python edits, no second-lab imports, no deferred path imports)
Consumers     : PASS  (Registry base_weight is consumed by FaultAtlasRouter)
Literals      : PASS  (Deltas follow T-V3-4A spec: EL-001=0.851, RM-001=0.90, LC-002=0.81, CF-002=0.701, MF-001=0.851, CF-001=0.851)
Docstrings    : PASS  (Test module and test functions documented)
Craft (WARN)  : Depth: Thin registry configuration edits. Deletion: No unused code/parameters added. Seam: Mapping firewall preserved; test calls diagnose() signature. Interface: Public diagnose() called directly by the test.
Result: CLEAN
