# REVIEW T-AUD-4o — ACCEPT, score 98 (Windows Cowork, 2026-11-06 10:28 CET)

Branch `fix/T-AUD-4o`: spec `54eace8`, build `3f7589e`. F-C5-9 fixed: a PARTIAL decode is basic mode (FieldMap §1.2),
and basic mode pins `overrides.upstream_o2_type` NARROWBAND, so the labs read the O2 type the form showed.

## Facts re-derived by Cowork (before the RESULT)
- The build's changed lines equal the rehearsal patch exactly; the test file is identical to the rehearsed one.
- Verification on `3f7589e`: new file `4 passed`; ui `49 passed`; wired `85 passed`; `f9_wideband.py` (corpus era2_015):
  "Upstream O₂ (V)" 0-1 and `EF-004 … mode=FULL_FUSION` with the box ticked and unticked (base: AFR field and
  `OBD_INPUT_INCOMPLETE` both ways); ruff clean.
- Cowork's rehearsal ran the new file in place on the base: `3 failed, 1 passed`, `test_partial_decode_is_basic_mode`
  failing on the gating (not a path error); M1 fails it, M2 fails the payload and run tests.

## Second review
Codex, APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-AUD-4o_review.md`). One CONCERN: the implementer's base run
of the AppTest failed on a path error, so its base count proves nothing for that test. Upheld as a record gap; settled
by Cowork's in-place base run above. No code correction.

## Score
100 − 2 (the base check of the AppTest ran from the wrong path; disclosed in the RESULT) = 98. Time: 1 min.

## Successors
T-AUD-4p, 4q, 4r and T-COMA-3 queued (handoff `handoffs/HANDOFF_20261106_1027.md`).
