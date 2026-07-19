# Progress Note — T-V3-3D: Abstain margin calibration

Committed the owner-picked family-aware abstain margin operating point: `ABSTAIN_MARGIN` is now `0.02` in [[fault_atlas_router.py]] and the v3 scoreboard display constant matches it. No family-aware selection logic, floor logic, scorer hash-locked `run_suite.py`, corpus, oracle, or yardstick file changed.

## Disclosure

Current post-oracle/post-4B scorecard result (`apps/wired/v7/runs/POST_T_V3_3D/results.json`):

- `Hash lock: ok` against `V3_YARDSTICK_2026-07-01`.
- `top3_family`: **193/294 = 65.65%** — unchanged from the post `[[FL-V3-ORACLE-MW-MISFIRE]]` baseline because abstain changes coverage only.
- `coverage`: **0.73** (**216/294** non-abstained).
- `top3_on_covered`: **155/216 = 71.76%**.
- `total_abstained`: **78**.
- Abstained split: **38 hidden wins** (top-3-correct but abstained) and **40 correct silences** (top-3-wrong and abstained).

The 0.02 dial is net-honest by a narrow margin on the current engine: it silences slightly more wrong top-3 answers than right ones, but it still hides 38 wins and lets 61 top-3-wrong covered cases through. This does not solve the residual ambiguity; Phase-4 signal packs remain the path to 95%.

## VERIFICATION GATE — T-V3-3D
1. Compile : PASS  (`py_compile` on `labs/comlab/comlab/core/fault_atlas_router.py`, `apps/wired/fl_tasks/score_v3_yardstick.py`, `labs/comlab/tests/unit/test_abstain_margin_002.py`)
2. Lint    : PASS  (`ruff check` on touched Python files)
3. Types   : PASS  (`pyright comlab/` from `labs/comlab` -> 0 errors; `pyright .` from `apps/wired` -> 0 errors after the known root-level config miss)
4. Tests   : PASS  (`pytest -x -q labs/comlab -k abstain_margin_002` -> 3 passed, 1022 deselected; `score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_3D/results.json` -> Hash lock ok)
5. Contract: PASS  (`ABSTAIN_MARGIN` 0.05->0.02 only; `ABSTAIN_FLOOR` unchanged at 0.80; family-aware different-family margin logic unchanged; `run_suite.py` untouched; `top3_family` remained 193/294)
6. Orphan  : N-A  (No new field/signal emitted; existing `abstained` / `abstain_reason` consumers remain the UI verdict card and v3 scoreboard coverage metrics)
Result: CLEAN

## CODE REVIEW — T-V3-3D
Scope         : PASS  (Only the two constants, the specified boundary/invariance test, and the generated post-run results artifact changed)
Composition   : PASS  (No cross-lab imports added; no `run_suite.py`, oracle, CSV, yardstick, graph, or `Vault/` edits)
Consumers     : PASS  (Existing `abstained` / `abstain_reason` path consumed by scoreboard coverage and UI verdict-card contract; no new signal)
Literals      : PASS  (`0.02` is the owner-picked D6 sweep operating point from [[V3_ABSTAIN_CHECKPOINT_2026-07-01]])
Docstrings    : PASS  (New test module and test functions documented)
Craft (WARN)  : Depth: one constant calibration, no branching added. Deletion: no unused helper or shim. Seam: router owns emission, scoreboard owns display/measurement. Interface: tests exercise router `route()` and scoreboard `summarize()` rather than private threshold plumbing.
Result: CLEAN
