# T-V3-P4-C4A — progress note

**Task:** C4 (exhaust_leak vs true_lean vs biased_o2) signal pack dry-run simulation.
**Date:** 2026-07-05 · **Coder:** Antigravity · **Mode:** STRICT (dual-gate)

## What shipped (all new, under `v3/` only)
- `v3/c4_signal_sim.py` — command-line simulator tool supporting `--self-check`, `--c4-seed <path>`, and `--write <path>` output.
- `v3/reports/V3_C4_SIGNAL_DRYRUN_2026-07-05.json` — machine-readable simulation output for the 11 cases.
- `v3/reports/V3_C4_SIGNAL_DRYRUN_2026-07-05.md` — human-readable Markdown report documenting the C4 dryrun findings.

## Findings surfaced
- **Yield breakdown:** of the 11 C4 cases:
  - **10 WOULD_BANK:** `CASE-020, CSV-129, CSV-130, EXT-211, EXT-212, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95`. These cases flip from baseline FAIL (or abstained-FAIL) to simulated PASS.
  - **0 ALREADY_PASS:** None of the C4 target cases were passing and covered in the baseline.
  - **1 STILL_SHORT:** `CASE-022` (sensor fault case, c4_state = `PERSIST_BIAS`, expected family = `sensor_fault`). In the simulation, its expected family is in the top-3, but the case remains abstained because the confidence score of the winner (`LC-003` at 1.0) is much higher than the correct `sensor_fault` rules, so it stays short of being a covered pass.
  - **0 ABSTAIN_NO_DATA:** All 11 cases are successfully simulated.
- **Yield summary:** the correct fault family in top-3 rises from **197/294 (67.01%)** in the baseline to **207/294 (70.41%)** under the simulated C4 signal pack. Coverage is **74.15% (218/294)**, and Top-3 on covered reaches **77.06%** (up from **73.15%** in the baseline).
- **FT-8 neighbour audit:** touched `exhaust_leak`, `lean_condition`, and `sensor_fault` rules, affecting 35 neighbour cases. The audit shows **0 regressions** on the full 294-case corpus.

---

## VERIFICATION GATE — T-V3-P4-C4A
1. Compile : PASS  (`py_compile v3/c4_signal_sim.py` → OK)
2. Lint    : PASS  (`ruff check v3/c4_signal_sim.py` → OK)
3. Types   : PASS  (`pyright v3/c4_signal_sim.py` → 0 errors, 0 warnings)
4. Tests   : PASS  (Self-check mode `python v3/c4_signal_sim.py --self-check` verifies that zero-overlay reproduces baseline results for all 294 cases with 0 drift.)
5. Contract: PASS  (Reports match five reveal-contract headings; C4 cases details are correctly mapped and split; yield is correctly attributed; FT-8 neighbour audit confirms 0 regressions.)
6. Orphan  : N-A   (Simulates in-memory; adds no live field or code that can orphan.)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C4A
Scope         : PASS  (only adds the simulation script, JSON results, and Markdown report under `v3/`; no live engine/registry edits.)
Composition   : PASS  (in-memory monkeypatch of `shim._score_rule` preserves the codebase architecture; no unauthorized imports from registry/composition violated.)
Consumers     : PASS  (sizes commit `T-V3-P4-C4B` and provides clear recommendations on the column-add decision; output formats conform to requirements.)
Literals      : PASS  (C4 producer state names, rule list, and thresholds cited exactly to value4.1.md.)
Docstrings    : PASS  (all modules, classes, and helper functions documented.)
Craft (WARN)  : Depth — exact scoring simulation captures raw score and handles ceiling removal correctly. Deletion — no debug or print residue left behind. Seam — clean monkeypatch interface for overlay evaluation.
Result: CLEAN

## Guardrails honoured
No live corpus column · no live registry/rule edit · no live re-score · no yardstick mint · no synthesized values in live corpus · MARGIN unchanged (0.02) · `run_suite.py` untouched · `Vault/` untouched · no `graphify` · no secrets · `git status` shows changes only under `v3/` (except `.gitignore` untracked files).
