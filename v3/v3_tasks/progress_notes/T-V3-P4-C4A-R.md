# Progress note — T-V3-P4-C4A-R

**Task:** [[T-V3-P4-C4A-R_c4_rebaseline_dryrun]]  
**Date:** 2026-07-06  
**Mode:** STRICT C4 signal-pack re-baseline dry-run (read-only simulator)

## Scope confirmation

Performed the C4 signal-pack re-baseline dry-run by simulating the proposed C4 producer states and consumer rule overlays read-only in memory against the current `POST_T_V3_P4_C5B` baseline and `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`). Created the simulator script `v3/c4_signal_sim_rebase.py`, ran the zero-overlay self-check (drift=0), ran the scenario simulations, derived the FT-8 neighbour union dynamically, and wrote reports at `v3/reports/V3_C4_SIGNAL_DRYRUN_REBASE_2026-07-06.{json,md}`. No files in the live codebase outside of the `v3/` directory were modified.

## Implementation notes

- **Fidelity fix in `my_score_rule`:** To resolve mismatches during the self-check, we refactored the monkeypatch in `v3/c4_signal_sim_rebase.py`. The original simulator temporarily cleared `rule.confidence_ceiling` for all rules across the entire corpus. In the presence of active C3, C5, and C6 overrides in the live shim, this inverted the order of clamping and boosting (clamping the boosted score vs boosting the clamped score), resulting in 20 mismatches. The new implementation immediately passes through non-C4 rules and non-C4 cases to the live `shim._score_rule`, preserving 100% of the live engine's override logic, and only applies the confidence ceiling bypass/boost for C4 cases and C4-affected rules.
- **Dynamic FT-8 derivation:** The neighbour set is re-derived live by reading the `passes_cases` arrays from `exhaust_leak.json`, `lean_condition.json`, and `sensor_fault.json` and excluding the 11 C4 target cases. The union consists of exactly 35 cases.
- **Zero-overlay self-check:** Verified at `OK (all 294 cases matched, drift = 0)` against `apps/wired/v7/runs/POST_T_V3_P4_C5B/results.json`.

## Pre-flight / Simulation result

Command:
```bash
/agent_workspace/.venv-wired/bin/python v3/c4_signal_sim_rebase.py --write v3/reports/V3_C4_SIGNAL_DRYRUN_REBASE_2026-07-06.json
```

Observed:
- **Scenario 1 (ΔSTFT-only, 8pt):** Banks **4** of the 7 leaks. `top3_family` moves 250 → 253/294.
- **Scenario 2 (ΔSTFT-only, 5pt):** Banks **7** of the 7 leaks. `top3_family` moves 250 → 256/294.
- **Scenario 3 (Full-signal):** Banks **10** cases (7 leaks + 3 leans). `top3_family` moves 250 → 260/294.
- **Regressions:** 0 regressions detected on neighbours or the wider corpus.
- **Biased O2 case (`CASE-022`):** Correctly separated but remains `STILL_SHORT` of top-3 (staying abstained at `MARGIN=0.02` due to baseline scores).

## Score result

Against the active `V3_YARDSTICK_2026-07-06-C5B` (csv `c49c17af…`):
- **Baseline top3:** 250/294 (85.03%)
- **Simulated top3:** 260/294 (88.44%)
- **Newly passing (yield):** 10 (`CASE-020, CSV-129, CSV-130, EXT-211, EXT-212, EXT-238, EXT-239, PDF-HI-007, TC-048, YAML-CSV95`)
- **Regressions:** 0
- **Coverage:** 71.43% (210/294 covered, 84 abstained)
- **Top-3 on covered:** 90.00%
- **abstained count:** 84 (all margin-triggered)
- **Hash lock:** `ok`

## VERIFICATION GATE — T-V3-P4-C4A-R

1. **Compile:** PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/c4_signal_sim_rebase.py` -> OK)
2. **Lint:** PASS (`/agent_workspace/.venv-wired/bin/ruff check v3/c4_signal_sim_rebase.py` -> OK)
3. **Types:** PASS (`/agent_workspace/.venv-wired/bin/pyright v3/c4_signal_sim_rebase.py` -> OK)
4. **Tests:** PASS (`/agent_workspace/.venv-wired/bin/python v3/c4_signal_sim_rebase.py --self-check` -> 0 drift; `/agent_workspace/.venv-wired/bin/pytest -q apps/wired/v7/tests/` -> 38 passed)
5. **Contract:** PASS (reports generated at `v3/reports/V3_C4_SIGNAL_DRYRUN_REBASE_2026-07-06.{md,json}`)
6. **Orphan:** PASS (read-only task; no live code changes made)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C4A-R

Scope: PASS (all changes trace to T-V3-P4-C4A-R deliverables: simulator script, MD/JSON reports, progress notes, ledger update)
Composition: PASS (no changes to live codebase or `Vault/`; `v3/` only)
Consumers: PASS (no live changes; consumer sizing recommended for C4B)
Literals: PASS (the thresholds used are the ones pinned in the seed and `value4.1.md`)
Docstrings: PASS (added docstrings to new functions in `c4_signal_sim_rebase.py`)
Craft (WARN): Depth: read-only simulator script. Deletion test: N/A. Seam discipline: monkeypatch restored in finally block. Interface=test surface: self-check ensures no drift.
Result: CLEAN

## Delta-vs-C4A & Follow-on (Sizing for C4B)

- **What changed since C4A:**
  - The baseline is two generations newer (`POST_T_V3_P4_C5B` vs `POST_T_V3_3D`), starting at 250/294 accuracy instead of 197/294.
  - The covered pool was reduced by C5B (from 211 to 208 cases), so baseline coverage is 71.43% instead of 73.47%.
  - Under Scenario 3, `top3_family` rises to **260/294** (+10 yield).
  - The FT-8 neighbour set remains 35 cases, and 0 regressions are detected.
  - **Live-interaction audit:** Evaluated `c3_state`, `c5_state`, and `c6_state` for all 11 C4 cases under both baseline and simulated conditions. They all returned `None`. This confirms that C4 cases do not trigger any decisive overrides in the live shim, meaning C4 proposed overrides will not conflict or fight with existing overrides on these cases.
- **C4B Sizing Recommendation:**
  - Recommends adding `co2_idle_pct`, `tailpipe_o2_elevation_pct`, `downstream_o2_v`, and `propane_trim_shift_pct` to the corpus CSV to reclaim the 3 lean cases and target a yield of 10 cases, otherwise they must stay abstained.
