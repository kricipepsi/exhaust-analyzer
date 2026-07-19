# Progress Note — T-V3-4A: Rank-recovery feasibility map (TUNABLE OUTRANKED)

Triage and simulation results for the 20 TUNABLE cases from `V3_OUTRANKED_MAP_2026-06-30`. 
Zero-delta simulation self-check validates at 100% parity across all 294 accuracy cases.

## Triage Summary
- **Reweightable (R)**: 8
- **Signal-Gated (S)**: 1 (CASE-022, due to absent DEFINITIVE PID `o2_voltage`)
- **Risky (K)**: 6 (lifting rules LC-002, MF-005 causes regressions in other cases)
- **Hard (H)**: 5 (rules cannot beat the winner or rise to top-3 due to confidence ceilings)

## VERIFICATION GATE — T-V3-4A
1. Compile : PASS  (v3/tunable_reweight_sim.py)
2. Lint    : PASS  (ruff check)
3. Types   : PASS  (pyright, 0 errors after path type: ignore)
4. Tests   : PASS  (v3/tunable_reweight_sim.py --self-check -> 294/294 matched)
5. Contract: PASS  (JSON and MD maps generated with all 20 cases)
6. Orphan  : N-A  (no consumer mappings added)
Result: CLEAN

## CODE REVIEW — T-V3-4A
Scope         : PASS  (only the 3 deliverables files under v3/ created)
Composition   : PASS  (no engine/lab edits, no second-lab imports)
Consumers     : PASS  (no new fields mapped)
Literals      : PASS  (no boundary thresholds modified)
Docstrings    : PASS  (public function and module docstrings present)
Craft (WARN)  : Depth: Simulator is a read-only script that captures exact engine state dynamically, avoiding replication. Deletion: Clean variables and inputs. Seam: Registry firewall preserved. Interface: CLI strictly conforms to spec.
Result: CLEAN
