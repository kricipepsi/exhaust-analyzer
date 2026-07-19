# T-V3-3C — progress note (family-aware abstain margin)

**Task:** `T-V3-3C_family_aware_abstain_margin.md` · **Status:** done · **Author:** Antigravity · **Date:** 2026-07-01
**Code:** `labs/comlab/comlab/core/fault_atlas_router.py`
**Tests:** `labs/comlab/tests/unit/test_abstain_family_margin.py`

## Plan

Fix the abstain margin definition so the honesty dial compares the winner to the first sibling of a different family, instead of comparing to the very next sibling (which might be of the same family, sharing the exact score or a tie). This prevents silencing cases where the engine already agrees on the fault family.
1. On the **REG-v2** path: change the `top2_score` selection loop to skip rules whose family matches the winner's family.
2. On the **v1 default** path: change the selection of runner-up score to be the score of the first runner-up whose family differs from the winner's family.
3. Keep thresholds (`FLOOR=0.80` / `MARGIN=0.05`) unchanged.
4. Verify using unit tests and the scoreboard yardstick.

## Disclosure

`/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_3C/results.json` produced:

- `top3_family`: **176/294 = 59.86%** (invariant kept).
- `coverage`: **0.37** (`109/294` non-abstained, up from `0.10` / `30/294` in T-V3-3B).
- `top3_on_covered`: **88/109 = 80.73%** (vs `80.00%` in T-V3-3B).
- `total_abstained`: **185** (down from `264` in T-V3-3B).
- `single_verdict family+state`: **81/294 = 27.55%** (up from `18/294` in T-V3-3B).

### Reconciliation & Recovered Wins
- Previously-passing single-verdict baseline (before abstain): **133**
- Unmasked passing single-verdict baseline in T-V3-3B: **18**
- Unmasked passing single-verdict baseline in T-V3-3C: **81**
- Hidden wins in T-V3-3B: **115** (`133 - 18`)
- Hidden wins in T-V3-3C: **52** (`133 - 81`)
- **Recovered Wins:** **63** wins recovered from unnecessary margin-abstentions!
- **Residual same-family abstentions:** **47** cases. In these cases, even though the margin is measured against a different-family sibling, a different-family sibling exists within 0.05, so the dial still abstains (correctly).

### Abstained Cases Right/Wrong Split
- **Abstained Wrong (97):** The engine would have gotten these wrong (correct family not in top-3); abstaining is a correct silence:
  `CASE-014, CASE-015, CASE-020, CASE-022, CASE-029, CASE-039, CASE-040, CSV-025, CSV-041, CSV-045, CSV-095, CSV-113, CSV-117, CSV-118, CSV-119, CSV-121, CSV-122, CSV-123, CSV-124, CSV-125, CSV-127, CSV-128, CSV-129, CSV-130, ECU-001, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N010, EXP-N011, EXP-N014, EXP-N018, EXP-N019, EXP-N023, EXP-N027, EXP-N029, EXP-N030, EXT-211, EXT-212, EXT-221, EXT-222, EXT-223, EXT-229, EXT-230, EXT-232, EXT-233, EXT-238, EXT-239, MECH-001, PDF-4G-04, PDF-HI-001, PDF-HI-005, PDF-HI-007, PDF-HI-010, REAL-001, REAL-002, REAL-003, REAL-004, RULE-CO-1, TC-021, TC-046, TC-048` and others.

- **Abstained Right (88):** The engine would have gotten these right (correct family in top-3); abstaining hides a win:
  `CASE-009, CASE-010, CASE-011, CASE-012, CASE-013, CASE-017, CASE-019, CASE-023, CASE-030, CASE-032, CASE-035, CASE-036, CASE-037, CASE-038, CSV-001, CSV-005, CSV-016, CSV-104, CSV-109, CSV-110, CSV-111, CSV-112, CSV-115, CSV-116, CSV-120, ECU-003, EXP-N006, EXP-N007, EXP-N008, EXP-N009, EXP-N015, EXP-N017, EXP-N021, EXP-N025, EXP-N026, EXP-N028, EXT-201, EXT-202, EXT-204, EXT-205, EXT-207, EXT-208, EXT-213, EXT-214, EXT-215, EXT-217, EXT-218, EXT-231, EXT-236, EXT-240, MECH-003, MECH-004, MECH-005, PDF-4G-01, PDF-4G-02, PDF-4G-03` and others.

## VERIFICATION GATE

```
VERIFICATION GATE — T-V3-3C
1. Compile : PASS  (labs/comlab/comlab/core/fault_atlas_router.py)
2. Lint    : PASS  (ruff check -> OK)
3. Types   : PASS  (pyright -> 0 errors)
4. Tests   : PASS  (pytest -x -q labs/comlab -k abstain_family_margin -> 2 passed)
5. Contract: PASS  (family-aware abstain margin on both paths; top3_family unchanged 176/294; Hash lock ok; coverage 0.10->0.37, total_abstained 264->185, hidden-wins recovered=63; residual same-family abstain=47)
6. Orphan  : PASS  (no new fields or contracts; all logic resides inside fault_atlas_router.py)
Result: CLEAN
```

## CODE REVIEW

```
CODE REVIEW — T-V3-3C
Scope         : PASS  (only changed margin top2/runner-up selection in fault_atlas_router.py and added unit tests)
Composition   : PASS  (COMLab-only; no cross-lab imports, no legacy code referenced)
Consumers     : PASS  (consumed by scoreboard and UI verdict)
Literals      : PASS  (no new thresholds introduced; existing ones cited)
Docstrings    : PASS  (added test docstrings)
Craft (WARN)  : depth: logic is completely in FaultAtlasRouter; deletion: no unused variables or code; seam: unchanged public interfaces and hash locks; interface: unit tests utilize router.route() and mock KG nodes
Result: CLEAN
```
