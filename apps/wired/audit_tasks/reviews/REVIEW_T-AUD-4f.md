TASK REVIEW — T-AUD-4f_frozen_lambda_none(3) — 2026-11-05 (Windows Cowork)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 95) — second review (second_review.py, DeepSeek) APPROVE WITH CORRECTIONS: 1 MEDIUM upheld as
a LOW concern (outside the write scope, folded into T-AUD-4g); 1 MEDIUM and 1 LOW not upheld; 1 INFO

Branch fix/T-AUD-4f on fix/T-AUD-4c (c49f9bf): spec 5f64322, fix 2f6a387. Implementer headless (sonnet medium).

MECHANICAL GATE
  ✓ deliverables exist           frozen branch emits None (comment cites §4.1); payload `float | None`, bounds kept;
                                 delta guard; 5 frozen pins updated; NEW test_frozen_payload_has_no_lambda; note; RESULT
  ✓ changed files in scope       the 7 Files-to-touch paths; porcelain: note and RESULT only
  ✓ tests                        reviewer re-run: obdlab `391 passed, 2 skipped`; wired 46, ui 30, dnalab 27, comlab
                                 526/4/2 (R0-2); ruff clean
  ✓ mutants (reviewer run)       sentinel back to 1.0: 6 failed (the 5 pins and the new test)
  ✓ effect visible               rehearsal on the new code: ECT-40 frozen 296, all None, 0 new exceptions; Cowork's
                                 pre-change run: 21 verdict changes (several NF-001 → a fault: the made-up stoich λ
                                 made cold engines look healthy)

SECOND REVIEW (`C:/4DApp/recheck/codex/T-AUD-4f_review.md`)
  F1 MED (the 21-change list is not from rehearse.out) — not upheld: Cowork's script prints only the first 12
    (`ch[:12]`); the implementer's full list matches P2's count. Cowork's artifact, not the build. −3 (spec cited it).
  F2 MED (`test_coverage_matrix_and_aggregate_rate` compares a set that now holds None; `lam > 1.01` would raise if
    None came first) — upheld as a LOW concern: stable under CPython hashing today, fragile. The file is outside the
    write scope → folded into T-AUD-4g (filter None before the comparisons). −2.
  F3 LOW (bounds not mutation-covered) — not upheld: bounds unchanged by this row.
  F4 INFO (perception_contradiction substitutes lambda_measured when the OBD λ is None) — intended; noted for 4g.

FOLLOW-UP: the F2 test fix rides with T-AUD-4g (ledger note).
