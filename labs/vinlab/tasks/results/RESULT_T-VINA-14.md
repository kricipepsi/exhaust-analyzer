# Result

## Status
completed

Branch and log:
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-14
$ git -C C:/4DApp/repo log --oneline b444481..HEAD
22a926a test(T-VINA-14): G1 and G2 run on the coalesced row; blank induction takes the hint
16b2e9e spec(T-VINA-14): correction 02 files-to-touch and precondition for the existing test file
15fb9fd spec(T-VINA-14): review correction 02 (three isolating tests, test files only)
50266c2 fix(T-VINA-14): decoder keeps map BOXER banks and stated induction; merge coalesces collisions (+40 rows)
3effcae spec(T-VINA-14): second plan review evidence
0e8654c spec(T-VINA-14): plan correction 01 (approved with C1-C2)
67bfd8c spec(T-VINA-14): decoder BOXER banks and stated induction; merge coalesces collisions
```
The implementer commits are `50266c2` (build) and `22a926a` (revision 02, test files only). The five `spec`
commits are Cowork's. Nothing pushed.

## Summary
- **R1:** `_apply_vref_techmask` gives a vref row 2 banks when `is_v_engine` is set or the map configuration starts
  `BOXER`.
- **R2:** `_cylinder_fallback` (keyword-only `induction_stated`, read from the applied `db_dict`) no longer replaces a
  TecDoc-stated induction.
- **R3:** The merge tool coalesces blank-against-value and 1 cc collisions (`_coalesce`), G1 drops its BOXER clause,
  and G2 drops test (ii). The tool ran once on the shipped `vref.db`: 40 rows inserted, `engine_ref` 1,234 → 1,274,
  and the 1,234 existing rows are unchanged. A second run inserts 0 rows and leaves the file unchanged.
- **R4:** the new decoder file holds 9 test items, and the merge file grows 20 → 27 tests. All 12 mutants (9 planned,
  3 from review correction 02) are killed.
- **Reach:** `row_applied` went 506 → 568. 7 real VINs change in banks, induction, euro, O₂ or air metering, each
  attributed below.

## Files changed
- `labs/vinlab/vinlab/decoder.py` (R1 banks, R2 `induction_stated` parameter and its call)
- `labs/vinlab/tools/merge_tecdoc_extract.py` (`_one_cc_spread`, `_coalesce`, G1, G2, `_skip_reason`, `_new_row`,
  `select_rows`, docstrings; `NATURALLY_ASPIRATED` removed; two decoder line cites moved)
- `labs/vinlab/vinlab/data/vref.db` (+40 rows)
- `labs/vinlab/tests/unit/test_vref_banks_induction.py` (NEW, 9 items: 7 in `50266c2`, + the parametrised
  `test_blank_induction_takes_the_hint` in `22a926a`)
- `labs/vinlab/tests/unit/test_vref_tecdoc_merge.py` (2 tests rewritten, 5 new in `50266c2`; + 2 in `22a926a`)
- `labs/vinlab/tasks/progress_notes/T-VINA-14.md`, this RESULT (untracked)
- Runtime only: `C:/4DApp/recheck/T-VINA-14/pt/*`, `C:/4DApp/recheck/T-VINA-14/mut/*` (mutant copies, `base_vref.db`)

The 40 new codes are `169A4000 18K4F 18K4K 1KR 1UZ-FE 4A 6FY ADY APQ AZQ B12S1 B38A15A B48A20A BBM BDY BKY BMD BME BZG
CDZ D16A8 EJ18 F18A3 FB20 FE G4FG HFX KDX KDY KFV KFW KFX PT204 RFJ RFK RFN RFU RFW RGX VK45DE`. By their 13b skip
reason: collision 33, cylinder_heuristic 5 (`AZQ BBM BMD BME BZG`), map_banks 2 (`EJ18 FB20`).

## Commands executed
See the progress note (`## Build`, `## VERIFICATION GATE`). In short:
1. The red run of the two files: `8 failed, 24 passed`.
2. The edits, the inner loop (`py_compile`, `ruff`, `ruff --select S`, `pyright`) and the merge run:
   `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py`.
3. Verification steps 1-4 and the commit.
4. The 9 mutants, then the R5 diff, then Verification step 5, import sanity and `isolation.py`.

## Validation evidence
- **Step 1:** `297 passed, 8 skipped` (revision 02; `293 passed, 8 skipped` at `50266c2`).
- **Step 2:** `36 passed` (revision 02; `32 passed` at `50266c2`).
- **Step 3** (at `50266c2`; no non-test file changed since): dnalab `27 passed`, wired `41 passed`, ui `30 passed`.
- **Step 4** (at `50266c2`; no non-test file changed since): `reach.py` before: `vref outcome: {'no_engine_code': 16, 'not_in_vref': 550, 'out_of_window': 59,
  'row_applied': 506}`. After: `vref outcome: {'no_engine_code': 16, 'not_in_vref': 479, 'out_of_window': 68,
  'row_applied': 568}`.
- **Step 5:** `inserted 0 rows; engine_ref now 1274 rows; schema rebuilt: no`, then no `vref.db` status line, then
  `All checks passed!`, then the log above. Porcelain shows only the note and this RESULT. Rerun after `22a926a`
  with the same output.
- **Deliverable merge run (first run):** skipped in_vref 1186, collision 9 (`1E 2GRFE A112A2000 A20NHT B6 FA20 JB K10B
  LFW`), status 0, no_my_start 37, span_gap 0, map_banks 0, cylinder_heuristic 34; `inserted 40 rows; engine_ref now
  1274 rows; schema rebuilt: no`.
- **Previous decisive failure absent:** the 8 red tests pass now. The 4 Subaru BOXER VINs of P2 now decode 2 banks.
- **Mutants:** 12 of 12 KILLED: 9 in `## Build`, 3 in `## Revision 02` (G1 and G2 on `group[0]`;
  `induction_stated` as `is not None`). Each of the 3 passes all the other tests of the two files.

### R5: every real VIN whose banks, induction, euro, O₂ or air metering changes
Measured: base decoder `b444481` on the base db, against `50266c2` on the merged db, over all 1,131 decoded real VINs.
Field changes: banks 4, induction 2, air 2, euro 1, O₂ 0. Also displacement 62, cylinders 3 and stress rpm 1, which
are not R5 fields.

| VIN | make, MY | code (map key, majority share) | change | cause |
|---|---|---|---|---|
| JF1GG9LK43G020691 | Subaru 2003 | EJ20 (BOXER_4; GG9LK 0.889) | banks 1 → 2 | map BOXER (R1) |
| JF1BH9LJB2G051603 | Subaru 2002 | EJ25 (BOXER_4; BH9LJ 0.960) | banks 1 → 2 | map BOXER (R1) |
| JF1BP9LKB4G011913 | Subaru 2004 | EJ25 (BOXER_4; BP9LK 0.982) | banks 1 → 2 | map BOXER (R1) |
| JF1BP9LKB5G025995 | Subaru 2005 | EJ25 (BOXER_4; BP9LK 0.982) | banks 1 → 2 | map BOXER (R1) |
| VF33BRFJC84042182 | Peugeot 2008 | RFJ (I4; 3BRFJ 1.000) | euro EURO_1 → EURO_4 (stress 3000 → 3500) | TecDoc `euro_norm` euro4 (PEUGEOT row; CITROEN blank; coalesced) |
| VF3221RA212038997 | Peugeot 2001 | RGX (I4; **`PEUGEOT,221RA` 0.400**) | induction NA → TURBOCHARGED; air MAF_ONLY → HYBRID_MAF_MAP | TecDoc `induction_type` TURBOCHARGED (RGX, XU10J2TE; `valvetrain_type` blank vs SOHC, coalesced) |
| VF7U6UA0012529661 | CITROEN 2001 | RGX (I4; **`CITROEN,U6UA0` 0.833**) | same | same |

No change is unattributed. The two AZQ VINs (`TMBCY46Y733811341`, `TMBDY16Y033784910`) keep NATURALLY_ASPIRATED and
MAF_ONLY against the base. Their displacement goes 0.0 → 1.198 and their cylinder count 0 → 3. Without R2 they would
turn TURBOCHARGED and HYBRID_MAF_MAP (P4; mutant R2 shows it).

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1 `297 passed, 8 skipped`; step 2 `36 passed`; 12/12 mutants killed by their named tests |
| 2 | MET | step 3 `27 / 41 / 30 passed` = P6. No value changes; the plan named none (no fixture touched) |
| 3 | MET | step 4 prints P3's outcome line; R5 table above, all 7 changes attributed |
| 4 | MET | `All checks passed!`; second merge `inserted 0 rows`, no `vref.db` status line; `50266c2` and `22a926a` on `fix/T-VINA-14` after the spec commits; porcelain = note + RESULT |

## Decisions the task did not specify
1. "Stated induction" is read from the row the decoder applies, after the window check (plan assumption 1). Cowork
   accepted this in correction 01.
2. The AZQ real-VIN test also asserts displacement 1.198, so it is red until the merge (assumption 2).
3. The R5 base db copy is at `C:/4DApp/recheck/T-VINA-14/mut/base_vref.db` (assumption 3).
4. `select_rows` raises `RuntimeError` on the unreachable case "no coalesced row, no skip reason", in place of an
   `assert` (ruff S101 in production code).
5. Two decoder line cites in the tool's comments were updated to the shifted lines (`:479-482`, `:465`).
6. The test module docstring of `test_vref_tecdoc_merge.py` now names T-VINA-14.

## Pre-existing changes preserved
At the start, porcelain was empty, then showed only this note. No other file was touched. The C:/4DApp master worktree
(`LOOP_STATE.md`, launcher) was not touched.

## Rollback
`git -C C:/4DApp/repo revert 22a926a 50266c2` on `fix/T-VINA-14` (or drop the commits before push). This restores `vref.db`
to 1,234 rows, because the db is in the commit.

## Remaining risks or uncertainties
- The RGX change comes from weak map keys (`PEUGEOT,221RA` 0.400; `CITROEN,U6UA0` 0.833). If the map picks the wrong
  engine for those VDS keys, the TURBOCHARGED and HYBRID decode is wrong too. This belongs to T-VINA-11 (map key).
- Coalescing takes the other brand's value where an AMBIGUOUS brand row left a field blank (for example, RGX PEUGEOT
  is AMBIGUOUS with a blank `valvetrain_type`). The inserted value may be one of that brand's disagreeing candidates.
- The downstream VIN scan covered only literal VINs. The suites still pass with the P6 counts.
- The repo-wide gates (comlab, dtclab, gaslab, obdlab, symptomlab) are NOT RUN (report-only; Cowork runs them).
- Context use is `ABSENT` in `## Time`: this session has no measurement for it.
