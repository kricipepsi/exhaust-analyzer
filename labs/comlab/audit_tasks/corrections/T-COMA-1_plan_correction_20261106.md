# T-COMA-1 — plan correction 01 (Windows Cowork, 2026-11-06)

Plan: `repo/labs/comlab/audit_tasks/progress_notes/T-COMA-1.md` § `## Plan`. Verdict: **APPROVED with corrections
K1-K4**, written into `repo/labs/comlab/audit_tasks/T-COMA-1_non_starter_family_gate(4).md` (§ Routing, R8). The task
file is the spec; this file is the approval record. No hand-back.

## Accepted from the plan
The approach, the signatures, the boundary cases, C1-C4 and C6-C8, A1-A3, the mutant order (commit first, restore
each mutant with `git restore`, `git diff --quiet` before Verification).

## Re-derived by Cowork
- Readiness (c): NS-004 0.75 + prior 0.10 = 0.85 ≥ floor 0.80 matches Cowork's `corpus_fix.json` (case_006 NS-004
  0.85, not abstained). The three mutant counts equal Cowork's rehearsal (P5).
- `py_compile` writes `__pycache__/*.pyc` even with `PYTHONDONTWRITEBYTECODE=1` (a copy of `app.py` under
  `recheck/scratch/` gained `x.cpython-314.pyc`).
- `audit/tools/isolation.py` on the base: `violations: 4` (test_abstain_margin_002.py:20; test_tunable_reweight.py:23,
  24, 25).

## Rulings on the plan's open points and the second review (`C:/4DApp/recheck/codex/T-COMA-1_plan_review.md`)
- **C5 (UI info line): changed → K4 (Cowork).** "No single confident verdict — top candidates:" over a verdict with no
  candidate is false.
- **1 py_compile writes outside the allow-list (BLOCKER): upheld → K1.**
- **2 isolation count can hide a swap (CONCERN): upheld → K2.**
- **3 Verification not reviewable (CONCERN): not upheld.** The prompt omitted the task's `### Verification ###`; step 3
  compares all six recorded fields of every corpus case, so the 309 running cases are checked whole.
- **4 R2's full output unchecked (CONCERN): upheld in part → K3** (a recorded output, no test change).
- **5 R4 has no behavioural test (CONCERN): not upheld.** A UI test scaffold for a four-line branch; Cowork reads the
  diff and K4's literal at review. Lost: an AppTest of the three captions.
- **6 "cranking" label (NIT): not upheld.** The plan's boundary list already keys the gate on the directive.
