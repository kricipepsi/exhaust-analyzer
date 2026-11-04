TASK REVIEW — T-VINA-14_decoder_banks_induction_remerge(4) — 2026-11-04 (Windows Cowork; plan correction 01, review correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 93) — second review (second_review.py: ds route exit 1 → codex) APPROVE WITH CORRECTIONS:
1 MEDIUM + 1 LOW test gap, both upheld and fixed in revision 02; no code or data defect found

Branch fix/T-VINA-14 on fix/T-VINA-13b (b444481): spec 67bfd8c, correction 01 0e8654c + evidence 3effcae, build
50266c2, correction 02 15fb9fd + 16b2e9e, tests 22a926a. Implementer impl-T-VINA-14 (opus high), PID 11172.
t = 11 min (plan 5, build 5, revision 1). Score: −5 revision round (three rules without an isolating test), −2 my
correction-02 commit before its authoring check (CREATE tag; fixed in 16b2e9e before the redispatch message).

MECHANICAL GATE
  ✓ deliverables exist           decoder (R1 banks, R2 induction_stated); tool (_coalesce, G1, G2); vref.db 1,234 →
                                 1,274; test_vref_banks_induction.py (9 items); merge tests 20 → 27; note with ## Plan,
                                 round 2, Revision 02; RESULT with reach before/after and the R5 table
  ✓ changed files in scope       git diff b444481..HEAD: the 5 Files-to-touch paths + spec commits; no dnalab/wired/ui
                                 file; porcelain: note and RESULT only
  ✓ commits on the task branch   50266c2, 22a926a: `git branch --contains` → fix/T-VINA-14 only
  ✓ tests                        reviewer re-run: vinlab `297 passed, 8 skipped`; two files `36 passed`; dnalab 27,
                                 wired 41, ui 30; comlab 526/4/2 (known, --continue-on-collection-errors), dtclab 590,
                                 gaslab 208/2/4, obdlab 388/2, symptomlab 72 (all = base); ruff clean
  ✓ red                          base decoder put back: 4 failed, 3 passed (decoder file); base tool put back: 4
                                 failed, 21 passed (merge file); PINs green both times
  ✓ mutants (reviewer run)       G1 on group[0]: 1 failed; G2 on group[0]: 1 failed; induction_stated "is not None":
                                 2 failed (all three survived at 50266c2: 32 passed each)
  ✓ effect visible               reach.py row_applied 506 → 568 (predicted 568), not_in_vref 550 → 479,
                                 out_of_window 59 → 68; euro EURO_4 15 → 16; HYBRID_MAF_MAP 32 → 34; second merge run
                                 on a copy inserts 0 rows and leaves the bytes equal

INDEPENDENT DATA CHECK (Cowork, against `git show b444481:…/vref.db` and Cowork's rehearsal db)
  1,234 base rows: 0 changed, 0 missing. 40 new rows, the same code set as `C:/4DApp/recheck/T-VINA-14/rehearse.py`
  built independently; all 1,274 rows equal the rehearsal db field by field (0 mismatches). 0 rows hold a blank-string
  induction_type.

SECOND REVIEW (codex, embedded 69 KB; out C:/4DApp/recheck/codex/T-VINA-14_review.md)
  F1 (MED) G1/G2 receiving the coalesced row was untested (group[0] mutants survive): UPHELD → revision 02
     `test_g1_runs_on_the_coalesced_row`, `test_g2_runs_on_the_coalesced_row`.
  F2 (LOW) a blank-string vref induction was untested ("is not None" mutant survives): UPHELD → revision 02
     `test_blank_induction_takes_the_hint` ["", "   "].
  No ruling mismatch; counts reconcile; RuntimeError branch unreachable.

DISCLOSED EFFECTS (accepted; R5 table in the RESULT)
  7 real VINs change an R5 field: 4 Subaru EJ20/EJ25 banks 1 → 2 (map BOXER); RFJ VF33BRFJC84042182 EURO_1 → EURO_4
  (TecDoc euro4, PEUGEOT row); RGX VF3221RA212038997, VF7U6UA0012529661 NA → TURBOCHARGED, MAF_ONLY → HYBRID (TecDoc
  RGX turbo). Also displacement 62, cylinders 3 (heuristic at TecDoc displacement), stress rpm 1. O₂ 0.

CONCERNS (not blocking; filed)
  - RGX map keys are weak (`PEUGEOT,221RA` 0.400; `CITROEN,U6UA0` 0.833): if the map picks the wrong engine there, the
    turbo decode is wrong → T-VINA-11 (ledger note added).
  - Coalescing fills an AMBIGUOUS brand's blank field from the other brand (RGX valvetrain): no decoder reader of
    valvetrain_type; noted.
  - The map's V/W configuration and cylinder count are wrong on inline engines (AEB, NG, 346KB, 326S4, 366S1) →
    T-VINA-16 (cylinder column) and T-VINA-11.
