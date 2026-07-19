# T-V3-3B — progress note (emit verdict abstain)

**Task:** `T-V3-3B_emit_abstain.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Code:** `labs/comlab/comlab/schemas/response.py`, `labs/comlab/comlab/core/fault_atlas_router.py`, `apps/wired/fl_tasks/score_v3_yardstick.py`
**Tests:** `labs/comlab/tests/unit/test_abstain_emit.py`

## Plan

Emit the verdict-level abstain decision to decline low-confidence answers based on the calibrated floor (0.80) and margin (0.05) thresholds:
1. Add optional Pydantic fields `abstained` and `abstain_reason` to `DiagnosticVerdict` in response schema.
2. Define `ABSTAIN_FLOOR` and `ABSTAIN_MARGIN` constants in `FaultAtlasRouter` citing `V3_TOPK_CEILING` §6.
3. Compute and assign `abstained`/`abstain_reason` on the v1 default path if a fault is detected (floor < 0.80, margin <= 0.05).
4. Compute and assign `abstained`/`abstain_reason` on the REG-v2 path using the final scored rules (after priors, discriminators, and delta engine) if a fault is detected.
5. Rebind `score_v3_yardstick.py` read-site to read `verdict.abstained` instead of result-level `abstained` (preserving the `run_suite.py` hash lock).
6. Create comprehensive tests to verify abstain behavior on floor, margin, high-margin, and healthy cases on both paths.

## Disclosure

`/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score --write-results apps/wired/v7/runs/POST_T_V3_3B/results.json` produced:

- `top3_family`: **176/294 = 59.86%** (unchanged, as expected).
- `coverage`: **0.10** (`30/294` non-abstained).
- `top3_on_covered`: **24/30 = 80.00%** (up from 59.86%).
- `total_abstained`: **264** (all margin-triggered; floor is 0 because all fault-detected confidence scores are >= 0.80).
- `single_verdict family+state`: **18/294 = 6.12%**.

### Reconciliation
- Previously-passing single-verdict baseline (before abstain): **133**.
- Covered (non-abstained) passing single-verdict baseline: **18**.
- Abstained previously-passing cases (abstained ∩ previously-passing): **115**.
- Reconciliation: `18 + 115 == 133` (perfect match).

### Abstained Cases Right/Wrong Split
- **Abstained Wrong (149):** The engine would have gotten these wrong; abstaining is a correct silence:
  `CASE-009, CASE-013, CASE-014, CASE-015, CASE-020, CASE-022, CASE-023, CASE-029, CASE-032, CASE-035, CASE-039, CASE-040, CASE-045, CASE-048, CSV-001, CSV-005, CSV-025, CSV-041, CSV-045, CSV-095, CSV-100, CSV-113, CSV-114, CSV-117, CSV-118, CSV-119, CSV-120, CSV-121, CSV-122, CSV-123, CSV-124, CSV-125, CSV-126, CSV-127, CSV-128, CSV-129, CSV-130, ECU-001, ECU-003, ECU-009, EXP-N002, EXP-N004, EXP-N005, EXP-N007, EXP-N010, EXP-N011, EXP-N014, EXP-N015, EXP-N017, EXP-N018, EXP-N019, EXP-N021, EXP-N023, EXP-N025, EXP-N026, EXP-N027, EXP-N029, EXP-N030, EXT-207, EXT-208, EXT-211, EXT-212, EXT-213, EXT-216, EXT-217, EXT-219, EXT-221, EXT-222, EXT-223, EXT-224, EXT-229, EXT-230, EXT-231, EXT-232, EXT-233, EXT-238, EXT-239, MECH-001, MECH-002, MECH-005, MECH-006, PDF-4G-01, PDF-4G-02, PDF-4G-04, PDF-HI-001, PDF-HI-005, PDF-HI-007, PDF-HI-010, REAL-001, REAL-002, REAL-003, REAL-004, RULE-CO-1, TC-021, TC-046, TC-048, YAML-CSV1, YAML-CSV25, YAML-CSV41, YAML-CSV45, YAML-CSV5, YAML-CSV95, YAML-PDF_4G_01, YAML-PDF_4G_05, YAML-PDF_HI_001, YAML-PDF_HI_005, YAML-PDF_HI_006, YAML-RULE_NOx_1, YAML-TC1, YAML-TC46, YAML-TC47, case_001, case_002, case_003, case_004, case_006, case_007, case_008, case_013, case_014, case_015, case_016, case_017, case_028, case_040, case_044, case_046, era1_001, era1_002, era1_006, era1_011, era1_015, era1_016, era1_017, era1_019, era2_005, era2_006, era2_008, era2_012, era2_015, era2_016, era2_019, era3_005, era3_007, era3_008, era3_009, era3_014, era3_015, era3_019`

- **Abstained Right (115):** The engine would have gotten these right; abstaining hides a win:
  `CASE-010, CASE-011, CASE-012, CASE-016, CASE-017, CASE-019, CASE-021, CASE-024, CASE-026, CASE-027, CASE-028, CASE-030, CASE-031, CASE-033, CASE-036, CASE-037, CASE-038, CSV-016, CSV-018, CSV-022, CSV-052, CSV-066, CSV-068, CSV-101, CSV-102, CSV-103, CSV-104, CSV-105, CSV-106, CSV-107, CSV-108, CSV-109, CSV-110, CSV-111, CSV-112, CSV-115, CSV-116, ECU-007, ECU-008, EXP-N001, EXP-N003, EXP-N006, EXP-N008, EXP-N009, EXP-N012, EXP-N013, EXP-N016, EXP-N028, EXT-201, EXT-202, EXT-204, EXT-205, EXT-214, EXT-215, EXT-218, EXT-225, EXT-226, EXT-227, EXT-228, EXT-234, EXT-235, EXT-236, EXT-237, EXT-240, MECH-003, MECH-004, PDF-4G-03, PDF-HI-002, PDF-HI-008, REAL-005, TC-011, YAML-CSV18, YAML-CSV22, YAML-CSV52, YAML-CSV66, YAML-CSV68, YAML-PDF_4G_02, YAML-PDF_4G_03, YAML-PDF_4G_04, YAML-PDF_HI_002, YAML-TC12, YAML-TC36, YAML-TC37, case_005, case_010, case_018, case_019, case_022, case_023, case_034, era1_003, era1_004, era1_005, era1_007, era1_008, era1_012, era1_013, era1_018, era1_020, era2_001, era2_002, era2_003, era2_004, era2_009, era2_010, era2_013, era2_014, era2_017, era2_020, era3_001, era3_006, era3_011, era3_013, era3_016, era3_018`

## VERIFICATION GATE

```
VERIFICATION GATE — T-V3-3B
1. Compile : PASS  (labs/comlab/comlab/schemas/response.py, labs/comlab/comlab/core/fault_atlas_router.py, apps/wired/fl_tasks/score_v3_yardstick.py, labs/comlab/tests/unit/test_abstain_emit.py)
2. Lint    : PASS  (ruff -> OK)
3. Types   : PASS  (pyright -> 0 errors)
4. Tests   : PASS  (pytest -x -q labs/comlab -k abstain_emit -> 8 passed)
5. Contract: PASS  (verdict-level abstain; run_suite.py untouched, Hash lock ok; top3_family 176/294; coverage 0.10, top3_on_covered 80.00%, total_abstained 264; single_verdict 18/294)
6. Orphan  : PASS  (abstain fields are read by score_v3_yardstick.py and mapped in OrchestratorFinalUIOutput)
Result: CLEAN
```

## CODE REVIEW

```
CODE REVIEW — T-V3-3B
Scope         : PASS  (changed only response schema, fault-atlas router, score_v3_yardstick.py read-site, and added abstain unit tests)
Composition   : PASS  (COMLab-only; no lab edits, no 2nd-lab imports, no deferred fusion path)
Consumers     : PASS  (abstain fields are consumed by score_v3_yardstick.py)
Literals      : PASS  (ABSTAIN_FLOOR=0.80 and ABSTAIN_MARGIN=0.05 cited to V3_TOPK_CEILING §6)
Docstrings    : PASS  (test cases and new fields documented)
Craft (WARN)  : depth: abstention logic remains inside FaultAtlasRouter; deletion: all code and constants are exercised; seam: run_suite.py remains untouched and hash-locked, scoreboard read-site rebound; interface: tests assert public route() output
Result: CLEAN
```
