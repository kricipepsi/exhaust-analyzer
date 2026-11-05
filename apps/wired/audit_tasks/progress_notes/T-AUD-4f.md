# T-AUD-4f progress note

## Readiness
(a) Starting state matches: branch fix/T-AUD-4f, HEAD 5f64322 (spec commit, descendant of c49f9bf; base = 5f64322), `git status --porcelain` empty, all 9 preconditions present.
(b) Intended failure: the frozen branch sets `normalized_lambda = 1.0` (translator line 150), so a None expectation fails on the value, not on setup. Confirmed by running the new test red before the code edit.
(c) Decisive value derived from the code, not the test: frozen branch -> `normalized_lambda` becomes None -> payload `normalized_obd_lambda` None and `lambda_perception_delta` None (delta guarded). Step 4 expects base frozen lambdas all None, verdict changes 0.
(d) No contradiction found so far. One watch item: `tests/pid_logset/test_pid_logset_wiring_gate.py` is not in Files to touch; its coverage test does `lam > 1.01` over the logset lambdas, which raises on None once cases 23/24 become null. Checked after the edits (see Assumptions).
(e) Teach-back: frozen OBDLab runs emit `normalized_obd_lambda = None` (payload type `float | None`, delta guarded) instead of 1.0, and the 5 P3 tests plus a new test pin that. Decisive check: obdlab `391 passed, 2 skipped`, and step 4 shows 0 verdict changes with all base frozen lambdas None.

## Assumptions worked past
1. `tests/pid_logset/test_pid_logset_wiring_gate.py` is not in Files to touch. Its `test_coverage_matrix_and_aggregate_rate` runs `lam > 1.01` and `abs(lam - 1.0)` over the logset lambdas, which now include None (cases 23, 24). It passes today only because `any()` short-circuits before it reaches None (set order `[0.95, 1.0, 1.15, 1.05, 0.85, 0.7, 1.3, None]`, None last). SOFT: I left the file alone; the reviewer can correct it without data loss. A follow-up row should filter None there.
2. `normalized_obd_lambda` stays required (no default): `float | None = Field(ge=0.7, le=1.3)`. R2 changes only the type.
3. The commit trailer was refused by bash_guard, so the commit uses the AGENTS.md form without it.
4. R4: `rehearse.out` lists 12 of the 21 changes (the script caps the list at 12). I ran a copy under `recheck/T-AUD-4f/mut/` with the cap removed and the patch inverted (base = λ 1.0 when frozen, head = None). Output: `mut/base_vs_head.out`.

## Time
phase | start | end | minutes | context at end
all | 2026-11-05T13:19:26Z | 2026-11-05T13:25:40Z | 6 | ABSENT

## VERIFICATION GATE
CLEAN: steps 1-5 pass as specified (outputs in the RESULT). pyright: NOT RUN (not in the task's Verification).

## CODE REVIEW
Scope: only Files-to-touch paths changed. Contracts: no new field; `normalized_obd_lambda` is still read by `composition._run_obdlab` and COMLab. Provenance: the new None cites wiki §4.1. Finding: assumption 1.
