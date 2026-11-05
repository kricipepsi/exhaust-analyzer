TASK REVIEW — T-AUD-4h_user_dtcs_and_ff_trim_gate(3) — 2026-11-05 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 98) — second review (second_review.py) APPROVE, no findings

Branch fix/T-AUD-4h on fix/T-AUD-4g (b4c6495): spec dd24964, fix 5c29e87. Implementer headless (sonnet medium).

MECHANICAL GATE
  ✓ deliverables exist           `_with_user_dtcs` (copy, explicit active_dtcs wins, all modes deduplicated, consumer
                                 comment) called by diagnose; FF guard `_ff_cold` at 70.0 (named constant citing
                                 ECT_WARM_THRESHOLD §9); NEW test_t_aud_4h_active_dtcs.py (3); NEW
                                 test_freeze_frame_trims_follow_ff_coolant (4 cases); note; RESULT
  ✓ changed files in scope       the 4 Files-to-touch paths; porcelain: note and RESULT only
  ✓ tests                        reviewer re-run: shim `44 passed`; registry `5 failed, 502 passed, 4 deselected` (only
                                 the known test_build_corpus.py, F-P2-1); wired 49; comlab 526/4/2 (R0-2); obdlab 391/2;
                                 ui 30; dtclab 590, gaslab 208/2/4, symptomlab 72, vinlab 376/8, dnalab 27; ruff clean
  ✓ mutants (reviewer run)       FF `<` → `<=`: 1 failed (70.0); route skipped: 1 failed; explicit-wins removed: 1 failed
  ✓ effect visible               on the new code `ff` and `UI=1 dtc` rehearsals are no-ops and the UI-shaped gates equal
                                 the corpus gates (289 VALID, 3 O2_FAULT_ACTIVE, 1 CKP_CMP_FAULT_ACTIVE); pre-change:
                                 UI shape 4 gate changes, FF gate 1 verdict change (era2_012 SF-008 → SF-001)

SECOND REVIEW (`C:/4DApp/recheck/codex/T-AUD-4h_review.md`)
  No findings; it cites R1-R5, the diff and the embedded re-run.

CONCERNS
  - `_ff_cold` adds a try/except for a non-numeric ECT that the spec did not ask for (harmless; DTCLab validates the
    field as a float). −1.
  - The commit has no Co-Authored-By trailer (bash_guard; known). −0.
  - A corpus row (case_011, a 'GARBAGE' DTC) raises DTCFormatError at base and after: by design of the case. −0.
  - The corpus hand-feeds obd.active_dtcs, so the route is measurable on the UI shape only (`UI=1`). −1.
