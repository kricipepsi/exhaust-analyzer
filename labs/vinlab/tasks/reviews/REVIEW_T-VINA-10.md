TASK REVIEW — T-VINA-10_era_from_year_when_euro_unknown(4) — 2026-11-04 (Windows Cowork; plan correction 01, review correction 02)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 90) — second review (codex) APPROVE WITH CORRECTIONS: 3 MEDIUM upheld and fixed in revision
02 (two test gaps, one wiki overstatement inherited from my R5), 1 LOW settled by Cowork's own corpus run; no code defect

Branch fix/T-VINA-10 on fix/T-VINA-14 (2ff9211): spec 0d299ee, correction 01 49005b7, build 56caaa1, correction 02
54541fb (also registers the R3 rows), revision 3216544. Implementer impl-T-VINA-10 (opus high), PID 6324.
t = 15 min (plan 8, build 5, revision 2). Score: −5 revision round (three rules without an isolating test), −3 my R5
stated the EU dates as universal and the first plan review's date check did not catch the exceptions, −2 my mutant
script left decoder.py with CRLF endings (restored, no content change).

MECHANICAL GATE
  ✓ deliverables exist           decoder (euro_known, year horizon, "" stress euro, flag); horizon.py citations; wiki
                                 §10.8; VIN_VOCABULARY row; probe population; test file (16); 3 snapshot fixtures; note
                                 with ## Plan, round 2, Revision 02; RESULT
  ✓ changed files in scope       git diff 0d299ee..HEAD: the Files-to-touch paths + spec commits; fixtures = the 3 named
  ✓ commits on the task branch   56caaa1, 3216544 on fix/T-VINA-10
  ✓ tests                        reviewer re-run: vinlab `313 passed, 8 skipped`; new file `16 passed`; dnalab 27, wired
                                 41, ui 30; comlab 526/4/2 (known), dtclab 590, gaslab 208/2/4, obdlab 388/2,
                                 symptomlab 72 (all = base); ruff clean
  ✓ red                          base decoder put back: 7 failed, 5 passed (the 12 build-time tests)
  ✓ mutants (reviewer run)       year for every VIN 1 failed; euro "" always 1 failed; hard-coded >= 2001 1 failed; no
                                 .strip() 1 failed; no .lower() 1 failed; known euro without a year → LEGACY 1 failed
  ✓ effect visible               f1_ probes `2 passed` (were 2 failed); C6 file 16 → 14 failed; rehearse.py on the build
                                 0 changes on 1,131 real VINs; corpus on the build: only `submitted_at` timestamp noise

DISCLOSED EFFECTS (accepted)
  416 real VINs (model years 2001-2010, euro unknown) HORIZON_LEGACY → HORIZON_ADAPTIVE, stress 3000 → 3500; 1 corpus
  run changes horizon and confidence rating, 0 verdicts; 3 snapshot fixtures (2001-2002) change the same two fields.
  euro_emission_category stays EURO_1 when unknown (contract enum), with the internal flag euro_unknown.

SECOND REVIEW (codex, embedded 53 KB; out C:/4DApp/recheck/codex/T-VINA-10_review.md)
  F1 (MED) strip/lower untested: UPHELD → parametrised test (" EuRo 4 ", "", "  ").
  F2 (MED) yearless decode with a known euro untested: UPHELD → euro5 no-year test.
  F3 (MED) §10.8 states the EU dates as universal: UPHELD → general deadlines plus the >2,500 kg and Art. 10(3)
     exceptions; 2001/2011 named as heuristic edges.
  F4 (LOW) corpus not rerun on the build: settled by Cowork's run (no substantive change).

CONCERNS (not blocking)
  - 438 real VINs with neither a known euro nor a model year stay LEGACY (ruled; flagged euro_unknown).
  - The f9 vocabulary probe stays red for two older undocumented flags (vds_engine_ambiguous, wmi_brand_missing).
