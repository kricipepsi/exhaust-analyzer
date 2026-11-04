# T-VINA-5 — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-5.md` § `## Plan`. Verdict: **APPROVED with corrections R2-R5**,
and the registry measurement below, written into the task file `repo/labs/vinlab/tasks/T-VINA-5_wmi_brand_table(4).md` (§ Rulings that bind). The task
file is the spec; this file is the approval record.

## Re-derived by Cowork (`C:/4DApp/recheck/scratch/vina5_rederive.py`, run from `audit/scratch/C6`)
- Map 12,900 rows. Per pair `rows / pos8 / collide / same / differ / copy`: MAYBACH 131/0/103/23/80/28, GENESIS
  130/0/66/30/36/64, KAWASAKI 152/0/25/18/7/127, DATSUN 39/0/18/7/11/21, STERLING MOTOR CAR 28/0/16/9/7/12. All equal
  to the plan's table. `real_vins()` = 1,364.
- The four counterexample keys and the real VINs that reach them (any Mercedes or Nissan WMI):
  `12602` → `WDB1260201A209445` (observed `MB617912`) and `WDB12602212002803` (observed `110987`): the two real VINs
  disagree, so no single row serves both. `14005`, `20102`, `BAAN1` → the one counterexample VIN each.
- `14005`, `20102`: the map holds three rows each. `MERCEDES-BENZ` (`119980`, `102985`, exact, wins), `MERCEDES BENZ`
  (`M119,119.970`, `M102102962`, blank share, the observed string verbatim) and `MAYBACH` (`119970`, `102962`, Nio
  vote). So these two are an existing conflict between two Mercedes spellings. They are not a wrong-brand defect.
  `BAAN1` and `12602` are a WMI population split (JN1 against other Nissan WMIs; two WDB VINs).
- This confirms the plan's bias note. Some blank-share right-brand rows copy `cylinder_count_resolved.md` verbatim, so
  "89 against 63" is agreement with the reference, not validation.

## Second review (`C:/4DApp/recheck/codex/T-VINA-5_plan_review.md`, Codex, embedded prompt): RETHINK, 7 findings
- **F1** (right wins picks wrong engines for 4 real VINs): **upheld.** At first I ruled "right wins" with 4 known false
  fails. The operator then pointed to the registry (`D:/4DLab/4DLabV2/DBS/`, the Nio CSVs this host was said to lack).
  Measured (`C:/4DApp/recheck/scratch/vina5_nio3.py`, `vina5_nio12.py`), file 3 is held out of the map build
  (`build_vds_map.py`: "never file 3"). On it, the 133 differing keys go to the wrong-brand row 82, to the right-brand
  row 22, ties 18, no evidence 11. VINs: 1,754 against 459. So "right wins" was wrong, and the plan's 89 against 63 was
  circular. **Ruling:** R2 is now the Pass B vote on files 1+2 over the merged post-R1 population (wrong 109,
  right 24). It matches 1,872 held-out VINs and agrees with file 3 on 84 of the 104 keys that file 3 decides. 14005
  and 20102 recover. 12602 stays a WMI population split (neither code matches file 3's 8 VINs) → T-VINA-11.
  *Tradeoff that lost:* "right wins" (no right-brand row edited; 459 held-out VINs) and per-key overrides.
- **R1 cross-check from the same file:** the registry brand (`D1-Znamka`) for WDB is `MERCEDES BENZ`/`MERCEDES-BENZ`
  (6,643), KMH `HYUNDAI` 4,550, JSA `SUZUKI` 1,918, JN1 `NISSAN` 670, SAX `ROVER` 29. JSK is `KAWASAKI` (10). File 3
  has no 5NM, KMT or JSL VIN.
- **F2** (the evidence is not independent; 27 VINs not classified): **upheld, CONCERN** → R2: the full outcome table,
  split by the winning row's `majority_share` (blank or numeric), worded as agreement.
- **F3** (tests guard coverage, not precedence): **upheld** → R4: `test_conflict_key_winner` and mutant M8.
- **F4** (the corpus guard does not prove P3's population): **upheld, CONCERN** → R4: set parity with `real_vins()`
  before the first edit, and exact denominators in the test.
- **F5** (R3 ledger note against "never edit the ledger"): **upheld, my defect.** R3 named the ledger and the header
  forbids the implementer to edit it. The plan's choice (the text in the RESULT) is right → R3 amended.
- **F6** (5NM unsupported): **upheld** → R1: 5NM stays `Genesis`. The open-case tests are dropped (no M7).
- **F7** (mutant and commit order inconsistent): **upheld** → R5 gives one order.

## Next
Add `## Plan round 2` to the note: each change from R2-R5, the parity result, the named conflict cases and the new
test and map-row counts. Then build without a second stop. One return at most. The Nio CSVs are
read-only input (operator, 2026-11-04).
