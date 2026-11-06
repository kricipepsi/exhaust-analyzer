# REVIEW T-COMA-1 — ACCEPT, score 98 (Windows Cowork, 2026-11-06 09:55 CET)

Branch `fix/T-COMA-1`: spec `8092b4c`, approval `e0d09ab` + `cba05c1`, build `208eca3`, revision 02 spec `d6bdda5`,
tests `2ba854b`. F-C1-7 (HIGH) fixed: a `will_not_start` session is decided by the `non_starter` family only.

## Facts re-derived by Cowork (before the RESULT)
- Verification steps 1-6 on `208eca3`: new file `14 passed`; comlab `531 passed, 4 skipped, 2 errors`; registry
  `5 failed, 502 passed, 4 deselected` (the known `test_build_corpus.py` set); wired `79 passed`; ui `38 passed`;
  15/15 probes `NS-NO-RULE` no_rule 0.0; corpus diff exactly REAL-002, REAL-003, case_006, case_007, case_040, and
  the whole dump equals Cowork's rehearsal (`True`), so the 309 running cases are unchanged on all six fields; the
  audit probe C1 `will_not_start_does_not_score` `1 passed`; ruff clean; isolation lines identical to the base.
- Mutants on the build: M2 (router `no_rule` off) `12 failed, 2 passed`; M1 (gate off) after revision 02
  `13 failed, 1 passed`. Both equal P5.
- Revision 02 (`2ba854b`): only the test file; wired `79 passed`.
- Diff read hunk by hunk: R1-R5, R7 and K4 implemented as ruled; the C2 restructure (enrichment locals per branch)
  keeps the no-fault and winner outputs (registry 502 and comlab 531 unchanged). K3's full shim output equals R2.

## Second review
- Plan: codex, PROCEED WITH CORRECTIONS (6 findings: 1, 2 upheld, 4 in part → K1-K3; 3, 5, 6 not upheld).
  `C:/4DApp/recheck/codex/T-COMA-1_plan_review.md`, filed as `authoring/evidence/T-COMA-1/plan_review/`.
- Code: codex, APPROVE (`C:/4DApp/recheck/codex/T-COMA-1_review.md`), no blocker; two test concerns, both re-derived
  and upheld (Cowork's own rehearsed asserts were weak) → revision 02 (R9).

## Score
100 − 2 (the build ran `ruff --fix` on the given test file without a stop; a correct call, recorded as A6, but the
fix was to Cowork's file) = 98. The revision is Cowork's spec defect and costs the implementer nothing.
Time: plan 6 + build 7 + revision 1 = 14 min (estimate 40-70).

## Successors
- T-COMA-2: gas readings optional for a non-starter (the T-AUD-4e residual). Cut from `fix/T-COMA-1`.
- T-COMA-3: GASLab marks cranking samples INVALID (NS-001..003 unreachable); NS-004's DTC list (P0335); REAL-002's label.
- Recorded risk, not a row: a dict-shaped `routing_directive` would turn the gate off (no producer builds one).
