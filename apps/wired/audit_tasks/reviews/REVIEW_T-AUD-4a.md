TASK REVIEW — T-AUD-4a_o2_downstream_pid(2) — 2026-11-05 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 96) — second review (second_review.py, DeepSeek; first attempt void: prompt had one invalid
UTF-8 byte from a `cut`, repaired) APPROVE WITH CORRECTIONS: 2 MEDIUM + 2 LOW, none upheld for this row

Branch fix/T-AUD-4a on fix/T-VINA-16 (49060ac): ledger 1afdecc, spec 12f853a, fix 1d8aa51. Implementer headless
(sonnet medium), session f1f52303. t = 2.5 min (session_times.py).

MECHANICAL GATE
  ✓ deliverables exist           `_PID_DISPATCH["o2_downstream"] = (("obd", "downstream_o2_v"),)` with its comment; three
                                 tests in registry/tests/test_integration_shim.py; note; RESULT
  ✓ changed files in scope       git diff 12f853a..HEAD: integration_shim.py, test_integration_shim.py; porcelain: note
                                 and RESULT only
  ✓ tests                        reviewer re-run: four registry files `87 passed`; comlab `526 passed, 4 skipped,
                                 2 errors` (R0-2); wired 41, ui 30, dtclab 590, obdlab 388/2, gaslab 208/2/4; ruff clean
  ✓ mutants (reviewer run)       base entry restored: `2 failed, 28 passed`
  ✓ effect visible               resolver: two-source payload 0.85 → 0.10, FF-only 0.85 → None, o2_voltage 0.85 kept.
                                 Corpus (Cowork's pre-change rehearse.out vs the post-change run): o2_downstream
                                 non-None 0 → 11, one score change (CASE-022: EL-002 0.8 now fires), 0 verdict changes

SECOND REVIEW (`C:/4DApp/recheck/codex/T-AUD-4a_review.md`)
  F1 MED (step 4 after the change is a self-comparison) — not upheld: the spec rules it so and names P4 (Cowork's
    pre-change run) as the before/after; the RESULT labels it that way, and the reviewer re-derived the after state.
  F2 MED (v1 router `o2_downstream` reads `freeze_frame_pids.o2_downstream`) — not upheld for this row: the v1 path does
    not run on the production default (F-C4-5); recorded here as a known second contract on the non-default path.
  F3 LOW (`if val:` truthiness mutant in the shared resolver survives) — not upheld: the resolver is unchanged by this
    row; too small for a row.
  F4 LOW (labels of the post-change run) — not upheld: same as F1.

CONCERNS: none new. FOLLOW-UP ROWS: none (v1 router contracts sit with F-C4-5 in T-AUD-4e).
