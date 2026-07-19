# T-V3-P4-C2A — progress note

**Task:** C2 (rich_mixture vs catalyst_failure) signal pack dry-run simulation.
**Date:** 2026-07-05 · **Coder:** Antigravity · **Mode:** STRICT (dual-gate)

## What shipped (all new, under `v3/` only)
- `v3/c2_signal_sim.py` — command-line simulator tool supporting `--self-check`, `--c2-data <path>`, and `--write <path>` output.
- `v3/reports/V3_C2_SIGNAL_DRYRUN_2026-07-05.json` — machine-readable simulation output for the 22 cases.
- `v3/reports/V3_C2_SIGNAL_DRYRUN_2026-07-05.md` — human-readable Markdown report documenting the C2 dryrun findings.

## Findings surfaced
- **Yield breakdown:** of the 22 C2 cases:
  - **15 WOULD_BANK:** `CASE-015`, `CASE-029`, `CASE-040`, `CSV-121`, `CSV-122`, `EXT-232`, `EXT-233`, `PDF-HI-001`, `PDF-HI-006`, `RULE-CO-1`, `YAML-PDF_HI_001`, `case_002`, `case_015`, `case_017`, `era2_019`. These cases flip from baseline FAIL to simulated PASS.
  - **4 ALREADY_PASS:** `CASE-023`, `EXP-N017`, `EXT-217`, `era2_015`. These cases were already passing and continue to pass.
  - **3 STILL_SHORT:** `CSV-100` (lean condition case, c2_state = `NORMAL`, stays FAIL as it needs Cluster 5 signals), `case_004` (sensor fault case, c2_state = `LOW_OSC_OR_HIGH_INDEX` confounded, stays FAIL), and `era1_017` (sensor fault case, c2_state = `LOW_OSC_OR_HIGH_INDEX` confounded, stays FAIL).
  - **0 ABSTAIN_NO_DATA:** All 22 cases are successfully simulated.
- **Yield summary:** the correct fault family in top-3 rises from **197/294 (67.01%)** in the baseline to **212/294 (72.11%)** under the simulated C2 signal pack. Coverage remains at **72.79% (214/294)**, and Top-3 on covered reaches **99.07%** (exceeding the 95% target).
- **FT-8 neighbour audit:** touched `rich_mixture` and `catalyst_failure` competition groups affect 33 neighbour cases. The audit shows **0 regressions** on the full 294-case corpus.

---

## VERIFICATION GATE — T-V3-P4-C2A
1. Compile : PASS  (`py_compile v3/c2_signal_sim.py`)
2. Lint    : PASS  (`ruff check v3/c2_signal_sim.py` → OK)
3. Types   : PASS  (`pyright v3/c2_signal_sim.py` → 0 errors, 0 warnings)
4. Tests   : PASS  (Self-check mode `python v3/c2_signal_sim.py --self-check` verifies that zero-overlay reproduces baseline results for all 294 cases with 0 drift.)
5. Contract: PASS  (Reports match five reveal-contract headings; C2 cases details are correctly mapped and split; yield is correctly attributed; FT-8 neighbour audit confirms 0 regressions.)
6. Orphan  : N-A   (Simulates in-memory; adds no live field or code that can orphan.)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C2A
Scope         : PASS  (only adds the simulation script, JSON results, and Markdown report under `v3/`; no live engine/registry edits.)
Composition   : PASS  (in-memory monkeypatch of `shim._score_rule` preserves the codebase architecture; no authorized imports from registry/composition violated.)
Consumers     : PASS  (sizes commit `T-V3-P4-C2B`; output formats conform to requirements.)
Literals      : PASS  (C2 producer state names, rule list, and thresholds cited exactly to spec.)
Docstrings    : PASS  (all modules, classes, and helper functions documented.)
Craft (WARN)  : Depth — exact scoring simulation captures raw score and handles ceiling removal correctly. Deletion — no debug or print residue left behind. Seam — clean monkeypatch interface for overlay evaluation.
Result: CLEAN

## Guardrails honoured
No live corpus column · no live registry/rule edit · no live re-score · no yardstick mint · no synthesized values in live corpus · MARGIN unchanged (0.02) · `run_suite.py` untouched · `Vault/` untouched · no `graphify` · no secrets · `git status` shows changes only under `v3/` (except `.gitignore` untracked files).
