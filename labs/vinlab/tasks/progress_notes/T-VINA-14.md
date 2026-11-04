# T-VINA-14 progress note: decoder BOXER banks and stated induction; merge coalesces collisions

Task file: `labs/vinlab/tasks/T-VINA-14_decoder_banks_induction_remerge(4).md` (plan: REQUIRED). This session is the
plan stop. No repo file is edited. The only write is this note. No hand-back finding: no `.blocker.json`.

## Readiness

- (a) Starting state matches the task. `git branch --show-current` = `fix/T-VINA-14`; `git log --oneline -3` =
  `67bfd8c spec(T-VINA-14): …`, `b444481 ledger(T-VINA-13c): …`, `1695e3a review(T-VINA-13b): ACCEPT 92`. The spec
  commit is a child of `b444481`. **Base = `67bfd8c`** (spec commit; Verification step 5 logs `b444481..HEAD`).
  `git status --porcelain` printed nothing. Preconditions printed `checked`, no `MISSING`, no `EXISTS`. `reach.py` on the
  base prints P1 exactly: `vref outcome: {'no_engine_code': 16, 'not_in_vref': 550, 'out_of_window': 59,
  'row_applied': 506}`, euro `EURO_1` 1107, O₂ NARROWBAND 702 / WIDEBAND_AFR 429.
- (b) Test fails for the intended reason: plan stage, the tests do not exist yet. Predicted red set at step 2 (below,
  "Tests"): 4 decoder tests red on the value (banks 1 not 2; induction TURBOCHARGED not NATURALLY_ASPIRATED; AZQ
  displacement 0.0 not 1.198 because the shipped db has no AZQ row), 4 merge tests red on the skip reason
  (`map_banks`, `cylinder_heuristic`, `collision` ×2). The PIN tests are green before and after.
- (c) Independent decisive value: I re-derived the decode diff with my own in-memory patch (window-aware, see
  "Measurements" M2), not Cowork's `decoder_rehearse.py`. It gives the same VIN set as P2 + P4, and 7 real VINs with an
  R5-field change versus the base (list below). I attributed Cowork's 40 rehearsal codes to their 13b skip reasons
  with the current tool (M3): collision 33 + cylinder_heuristic 5 + map_banks 2 = 40, which reconciles P3
  (collision 44 → 9, cylinder_heuristic 39 → 34, map_banks 2 → 0, no_my_start 35 → 37: 2 coalesced codes lack
  `my_start`; 44 − 9 − 2 = 33).
- (d) No contradiction or missing decision prevents implementation. The open choices are listed under "Choices".
- (e) Teach-back: the decoder gives two banks to a vref row on a map BOXER engine and stops the cylinder heuristic
  replacing a TecDoc-stated induction; the merge tool mirrors that (G1 without BOXER, G2 without (ii), coalesced
  collisions) and inserts 40 codes into the shipped `vref.db`. The decisive check is `reach.py` after the merge
  printing `row_applied` 568 / `not_in_vref` 479 / `out_of_window` 68 / `no_engine_code` 16, with every real-VIN change
  in banks, induction, euro, O₂ and air metering attributed to a TecDoc field or the map BOXER.

## Assumptions worked past

1. **Stated induction means the applied row.** R2 says "when the vref row states a non-blank `induction_type`". I read
   the row the decoder applies (`db_dict`, after the F-C6-4 window check), so an out-of-window row counts as no row.
   Cowork's `decoder_rehearse.py` sets `stated` from `lookup_engine_ref` before the window check. On the 1,131 real
   VINs both readings give the same changed set (M2 matches P2 and P4), so the difference is not observable there.
2. **The real AZQ test asserts the row is applied.** On the shipped db before the merge, `TMBCY46Y733811341` already
   decodes NATURALLY_ASPIRATED and MAF_ONLY (no AZQ row, heuristic unresolved at 0.0 L). A test of only those two values
   passes before the code exists. I add `engine_displacement_liters == 1.198` (TecDoc 1198 cc) so it is red until
   step 5, and the induction/air asserts make it red under the R2 mutant after the merge.
3. **R5 baseline files.** The R5 diff at the finish compares the base decoder (`git show b444481:…/decoder.py`, loaded
   in memory) on the base db against the new decoder on the merged db. The base db is written to
   `C:/4DApp/recheck/T-VINA-14/mut/base_vref.db` (a RUNTIME directory of this task) with
   `git show b444481:labs/vinlab/vinlab/data/vref.db`. The script runs from stdin (no script file); its text goes in
   this note. Reject this if Cowork wants another path.
4. **"Two values 1 cc apart"** is read as exactly two distinct non-blank `displacement_cc` values whose difference is 1.
5. **One mutant per rule**: R3 has three sub-rules; I name one mutant for G1 and one for the coalesce (G2 (ii) removal
   is killed by the same stated-NA test as R2's tool side). Listed below.

## Plan

### Approach

**R1 (decoder banks)**, `vinlab/decoder.py::_apply_vref_techmask`, the `banks = …` line (now `:364`):

```python
            # number of banks: is_v_engine, or a map BOXER configuration; the extract writes BOXER as
            # is_v_engine 0 (tools/extract_tecdoc_1q2019.py:64), so only the map states it (T-VINA-14 R1)
            csv_config = ((engine_row or {}).get("engine_configuration") or "").strip().upper()
            banks = 2 if db_dict.get("is_v_engine") or csv_config.startswith("BOXER") else 1
```

A map `V`/`W` with `is_v_engine 0` stays one bank (ruling; out of scope to fix the map).

**R2 (stated induction)**, `_cylinder_fallback` gains a keyword-only `induction_stated: bool`; the NA replacement
becomes `if not induction_stated and induction_type == InductionType.NATURALLY_ASPIRATED:`. The call in
`decode_vin_payload` (now `:641`) passes `induction_stated=bool((db_dict.get("induction_type") or "").strip())`, the same
predicate `_apply_vref_techmask:350-352` uses to apply the row's induction. `db_dict` is `{}` with no row or an
out-of-window row. Docstring gains one sentence. Signature after:
`_cylinder_fallback(self, cylinder_count: int, engine_row: dict[str, str] | None, displacement_liters: float, brand: str,
induction_type: InductionType, number_of_banks: int, *, induction_stated: bool) -> tuple[int, InductionType, int]`.
No exception added. The bank half of the fallback is unchanged (out of scope).

**R3 (tool)**, `tools/merge_tecdoc_extract.py`:
- New `_coalesce(group) -> dict[str, str] | None`: a copy of `group[0]` (alphabetically first brand, so brand and the
  13b brand rule hold) with each `COLLISION_FIELDS` field set to the first non-blank value in brand order, or `""`.
  It returns `None` when a field holds more than one distinct non-blank value, except `displacement_cc` with exactly two
  values 1 cc apart (then the first brand that states one wins, by brand order).
- `select_rows` computes `row = _coalesce(group)` once and passes it on. `_skip_reason(code, group, row, existing,
  map_rows)`: `collision` when `row is None`; `status`, `no_my_start`, `span_gap` stay on the group; G1 and G2 run on
  `row`. `_new_row(row, group)` reads the engine fields from `row` and the window from the group.
- G1 `_g1_map_banks`: drop the `BOXER` clause; keep `not row["is_v_engine"] and any(config[:1] in ("V", "W"))`
  (a V/W test, not `_two_bank`, so a blank `is_v_engine` on a map BOXER is not skipped: R1 gives it two banks).
- G2 `_g2_cylinder_heuristic`: delete test (ii) and the `stated_na` line; tests (i) and (iii) unchanged. The
  `NATURALLY_ASPIRATED` constant loses its only reader and is deleted (anti-orphan).
- Module docstring: names T-VINA-14, the coalesce rule, the narrowed G1 and G2. `_g1`/`_g2` docstrings updated.
- Then run `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py` once on the shipped db.

Rejected: passing `db_dict` into `_cylinder_fallback` (wider interface for one bit); returning a 22nd element from
`_apply_vref_techmask` (the tuple is already 21 wide); taking the min/max cc on a 1 cc spread (the ruling says first
brand that states one).

### Choices this task leaves open

| choice | taken | rejected | why |
|---|---|---|---|
| where "stated" is read | applied row `db_dict` (post-window) | raw lookup (rehearsal) | an out-of-window row's fields are not applied anywhere else (F-C6-4); same result on the real VINs |
| fallback interface | keyword-only bool | pass `db_dict` | minimal surface; caller already owns `db_dict` |
| coalesce placement | once in `select_rows`, passed to `_skip_reason` and `_new_row` | recompute inside each | one source of truth for the inserted values |
| decoder test VINs | real VINs on a `tmp_path` copy of the shipped db with fixture rows (below) | calling `_apply_vref_techmask` directly | the ruling says fixture rows on a temporary `vref.db` copy; full decode exercises the call site |
| AZQ real-VIN assert | add displacement 1.198 | induction + air only | otherwise green before the code (red gate) |

### Tests

`tests/unit/test_vref_banks_induction.py` (NEW, 7 tests). A `vref_copy` fixture copies `data_dir / "vref.db"` to
`tmp_path`, applies the test's fixture SQL before the first decode (the `_build_normalised_index` lru_cache is keyed on
the path; exact-code matches do not touch it), and returns a `RobustVINDecoder(data_dir)` with `db_path` set to it.

| # | test | VIN (map row) | fixture | expect | base result |
|---|---|---|---|---|---|
| 1 | `test_vref_zero_with_map_boxer_gives_two_banks` | `JF1BH9LJB2G051603` (EJ25, BOXER_4) | `UPDATE engine_ref SET is_v_engine=0 WHERE engine_code='EJ25'` | banks 2 | 1: red |
| 2 | `test_vref_zero_with_map_v6_gives_one_bank` PIN | `VF38CXFXA81270589` (XFX, V6, 2008) | `is_v_engine=0` on XFX | banks 1 | 1: green |
| 3 | `test_vref_one_gives_two_banks` PIN | `YV1LW5502V2373912` (B5254S, I5) | `is_v_engine=1` on B5254S | banks 2 | 2: green |
| 4 | `test_stated_na_is_not_replaced_by_turbo_hint` | `TMBCY46Y733811341` (AZQ, map blank) | `INSERT OR REPLACE` AZQ, 1198 cc, 2001-2009, induction NATURALLY_ASPIRATED | NA, cylinders 3 | TURBOCHARGED: red |
| 5 | `test_null_induction_takes_the_hint` PIN | same | same row, induction NULL | TURBOCHARGED, cylinders 3 | green |
| 6 | `test_real_boxer_vin_has_two_banks` | `JF1BH9LJB2G051603` on the shipped db | none | banks 2 | 1: red |
| 7 | `test_real_azq_vin_after_merge_is_na_and_maf_only` | `TMBCY46Y733811341` on the shipped db | none | displacement 1.198, NA, MAF_ONLY | 0.0: red until step 5 |

Note on test 2: the base already gives one bank there (`banks = 2 if is_v_engine else 1`), so it is a true PIN (green
before and after); it kills the mutant that copies the decoder's no-row V/W rule into the row branch.

`tests/unit/test_vref_tecdoc_merge.py` (MODIFY, 20 → 23 tests):
- `test_map_boxer_code_is_skipped` → `test_map_boxer_code_is_inserted`: inserted `("ZZ9NEW",)`, `map_banks` empty,
  row `is_v_engine` 0. Base: skipped `map_banks` (red).
- `test_cylinder_heuristic_hazard_is_skipped` → `test_stated_na_heuristic_code_is_inserted`: same SKODA ZZ5SKQ fixture;
  inserted, `cylinder_heuristic` empty, row induction NATURALLY_ASPIRATED. Base: skipped (red).
- NEW `test_blank_against_value_collision_is_coalesced`: BRANDA (`euro_norm` "", `valvetrain_type` "") and BRANDB
  (`euro4`, `SOHC`, `induction_type` "") with BRANDA `induction_type` NATURALLY_ASPIRATED: inserted; row euro4, SOHC,
  NATURALLY_ASPIRATED, brand BRANDA. Base: `collision` (red).
- NEW `test_one_cc_collision_takes_first_stating_brand_cc`: BRANDA cc "", BRANDB 1598, BRANDC 1597: inserted; cc 1598
  (not the min), brand BRANDA. Base: `collision` (red).
- NEW `test_two_cc_spread_stays_collision` PIN: 1597 vs 1599: `collision`. Green before and after.
- `test_blank_is_v_engine_with_v_map_is_skipped` unchanged, stays green; `test_skips_collision_code` (1598 vs 1796)
  stays green.

### Mutants (step 8; copy to `C:/4DApp/recheck/T-VINA-14/mut/`, edit the copy, copy over, run the named test, `git restore`)

| rule | mutant | killed by |
|---|---|---|
| R1 | `banks = 2 if db_dict.get("is_v_engine") else 1` (BOXER clause removed) | banks #1 and #6 |
| R1 PIN | `… or csv_config[:1] in ("V", "W") or csv_config.startswith("BOXER")` | banks #2 |
| R2 | `if induction_type == InductionType.NATURALLY_ASPIRATED:` (stated flag ignored) | banks #4 (and #7 after the merge) |
| R2 PIN | `if induction_type == InductionType.NATURALLY_ASPIRATED and False:` (never replace) | banks #5 |
| R3 G1 | restore `if any(c.startswith("BOXER") for c in configs): return True` | merge `test_map_boxer_code_is_inserted` |
| R3 coalesce | 1 cc check `== 1` → `<= 2` | merge `test_two_cc_spread_stays_collision` |

### Predicted outputs (steps 1-5)

1. vinlab: `291 passed, 8 skipped` (281 + 7 + 3).
2. the two files: `30 passed` (23 + 7).
3. dnalab `27 passed`, wired `41 passed`, ui `30 passed`: unchanged (P6). The 11 VIN literals in those suites decode
   identically under the new rules and the rehearsal db (M4). No fixture change; no dnalab/wired/ui file is touched.
4. `vref outcome: {'no_engine_code': 16, 'not_in_vref': 479, 'out_of_window': 68, 'row_applied': 568}` (P3).
5. The step-5 merge run (the first run is the step-5 deliverable run, this is the second):
   `inserted 0 rows; engine_ref now 1274 rows; schema rebuilt: no`; no `vref.db` status line; `All checks passed!`;
   `git log` shows `67bfd8c` plus my commits; porcelain shows only the note and the RESULT.
   The deliverable run (step 5 of R6) prints: skipped in_vref 1186, collision 9 (`1E 2GRFE A112A2000 A20NHT B6 FA20 JB
   K10B LFW`), status 0, no_my_start 37, span_gap 0, map_banks 0, cylinder_heuristic 34; `inserted 40 rows; engine_ref
   now 1274 rows; schema rebuilt: no`.

### R5: predicted decode changes on the 1,131 real VINs (base `b444481` vs R1-R3 on the rehearsal db, M2)

Field changes: banks 4, induction 2, air 2, euro 1, O₂ 0; also displacement 62, cylinders 3, stress rpm 1.

| VIN | make, MY | code (map) | change | cause |
|---|---|---|---|---|
| JF1GG9LK43G020691 | Subaru 2003 | EJ20 (BOXER_4) | banks 1 → 2 | map BOXER (R1) |
| JF1BH9LJB2G051603 | Subaru 2002 | EJ25 (BOXER_4) | banks 1 → 2 | map BOXER (R1) |
| JF1BP9LKB4G011913 | Subaru 2004 | EJ25 (BOXER_4) | banks 1 → 2 | map BOXER (R1) |
| JF1BP9LKB5G025995 | Subaru 2005 | EJ25 (BOXER_4) | banks 1 → 2 | map BOXER (R1) |
| VF33BRFJC84042182 | Peugeot 2008 | RFJ (I4) | euro EURO_1 → EURO_4 (stress 3000 → 3500) | TecDoc `euro_norm` euro4 (PEUGEOT row; CITROEN blank, coalesced) |
| VF3221RA212038997 | Peugeot 2001 | RGX (I4) | induction NA → TURBOCHARGED; air MAF_ONLY → HYBRID_MAF_MAP | TecDoc `induction_type` TURBOCHARGED (XU10J2TE; valvetrain blank vs SOHC, coalesced) |
| VF7U6UA0012529661 | CITROEN 2001 | RGX (I4) | same | same |

AZQ (`TMBCY46Y733811341`, `TMBDY16Y033784910`): versus the base, induction stays NATURALLY_ASPIRATED and air stays
MAF_ONLY; displacement 0.0 → 1.198 and cylinders 0 → 3 (heuristic count at TecDoc's displacement). P4's
TURBOCHARGED → NATURALLY_ASPIRATED is the R2 effect against an R1+R3-only decoder, not against the base.

### Each rule: population checked, population run over, false pass, false fail

| rule | checked on | runs over (command) | false pass | false fail |
|---|---|---|---|---|
| R1 banks | 1,131 real VINs, base code patched in memory, shipped and rehearsal db (M2) | every decode with an applied row; step 4 `reach.py`, step 1 suite | a map BOXER on a non-boxer engine: the 17 BOXER map rows are all SUBARU (`awk` on `vds_engine_map.csv`), so none known | a true V engine with TecDoc `is_v_engine 0` keeps 1 bank (ruled: map wrong there, out of scope) |
| R2 stated induction | same (M2) | every decode whose map count is unknown and that has an applied row | TecDoc states NA for a turbo engine: the heuristic no longer overrides it (accepted: TecDoc outranks the heuristic) | a NULL/blank row induction still takes the hint (by rule) |
| coalesce | 1,306 normalised extract codes, 44 collisions → 35 coalesced, 9 kept (M3, P5) | the extract; step 5 deliverable run | an AMBIGUOUS brand row blanks a field its TecDoc candidates disagree on; coalescing takes the other brand's value, which may be one of those candidates (RGX PEUGEOT is AMBIGUOUS, blank `valvetrain_type`) | two brands that state the same engine with a 2+ cc spread stay `collision` (conservative) |
| G1 narrowed | same | same | none new: a map BOXER code inserted gets 2 banks from R1 | – |
| G2 (ii) removed | same: all 40 inserted rows state induction (M3 query), so no blank-induction row takes a hint | same | a blank-induction code whose new displacement turns the hint turbo would decode TURBOCHARGED without a TecDoc statement; none among the 40 | – |

Step-order effect: step 5 (the merge) changes what steps 1, 2 and 4 run against: test #7 and `reach.py` are only
green after it, and the merge tests use their own pre-13b fixture db, not the shipped one.

### Commands for the redispatch and the paths they write

- step 2 red: `(cd labs/vinlab && PYTHONDONTWRITEBYTECODE=1 timeout 120 $PY -m pytest -q -p no:cacheprovider
  tests/unit/test_vref_tecdoc_merge.py tests/unit/test_vref_banks_induction.py
  --basetemp=C:/4DApp/recheck/T-VINA-14/pt/red)`: writes `pt/red`. Expect 8 failed (4 + 4), 22 passed.
- steps 3-4: edits to `decoder.py`, `merge_tecdoc_extract.py`; inner loop `py -m ruff check`, `--select S`,
  `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe` on the 4 files; writes nothing.
- step 5: `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py`: writes `vinlab/data/vref.db`. Then a `sqlite3`
  one-liner lists the 40 new codes (compare with `git show b444481:…vref.db` deserialised in memory).
- step 6: Verification 1-4; writes `pt/v`, `pt/t`, `pt/dnalab`, `pt/wired`, `pt/ui`.
- step 7: `git add` the 5 paths, then the commit (own command).
- step 8: mutants, `mut/`; `git restore` each file after.
- R5 measure: stdin script; writes `mut/base_vref.db` (assumption 3).
- step 9: Verification 5; then the note, `## Time`, the RESULT.

### Remaining risks

- The downstream VIN scan (M4) covers literal 17-character VINs only; a VIN built at run time in a dnalab/wired/ui test
  is not covered. Step 3 measures it.
- The merged db bytes depend on SQLite page layout; only the counts and codes are compared, as the task states.

## Measurements (all read-only)

- M1 `reach.py` on the base: P1 exactly (above).
- M2 decode diff: stdin script from `audit/scratch/C6`; snapshot with the base decoder on the shipped db, then patch
  `_apply_vref_techmask` (banks = `is_v_engine` or map BOXER; record `stated` from the applied `db_row`) and
  `_cylinder_fallback` (keep the input induction when stated), point `DEC.db_path` at
  `C:/4DApp/recheck/T-VINA-14/vref_rehearsal.db` (1,274 rows), snapshot again. Output: `decoded 1131 1131`,
  `field changes {'banks': 4, 'disp': 62, 'cyl': 3, 'induction': 2, 'air': 2, 'euro': 1, 'stress': 1}`, the 7 VINs above.
- M3 13b reasons of the 40 rehearsal codes (current tool's `select_rows` on the shipped db): `13b-on-shipped inserted 0
  {'in_vref': 1186, 'collision': 44, 'status': 0, 'no_my_start': 35, 'span_gap': 0, 'map_banks': 2,
  'cylinder_heuristic': 39}`; collision 33 (`169A4000 18K4F 18K4K 1KR 1UZ-FE 4A 6FY ADY APQ B12S1 B38A15A B48A20A BDY BKY
  CDZ D16A8 F18A3 FE G4FG HFX KDX KDY KFV KFW KFX PT204 RFJ RFK RFN RFU RFW RGX VK45DE`), cylinder_heuristic 5 (`AZQ BBM
  BMD BME BZG`), map_banks 2 (`EJ18 FB20`). All 40 have non-blank `induction_type` and `displacement_cc`.
- M4 the 11 VIN literals in `labs/dnalab`, `apps/wired`, `apps/ui` (`grep -rhoE` 17-char): all `SAME` under the M2
  patch and the rehearsal db (3 raise in both: `1FA6P8CF0HXXXXXXX`, `TMAD251CAGJ331435`, `W0LGM6ET6E1072040`).

## Plan stop

Stopped before the first edit. Cowork reviews this plan in `labs/vinlab/tasks/corrections/`.


## Redispatch 01: readiness

- Clock at redispatch start: 2026-11-04T16:44:56Z.
- (a) `git branch --show-current` = `fix/T-VINA-14`; `git log --oneline -3` = `3effcae spec(T-VINA-14): second plan
  review evidence`, `0e8654c spec(T-VINA-14): plan correction 01 (approved with C1-C2)`, `67bfd8c …`. Porcelain: only
  this note (`?? labs/vinlab/tasks/progress_notes/T-VINA-14.md`). The header now reads `plan: APPROVED`; the approval
  record `labs/vinlab/tasks/corrections/T-VINA-14_plan_correction_20261104.md` has no `### Plan-time digest ###` table,
  so there is nothing to recompute. Base for the build = `3effcae`; Verification step 5 logs `b444481..HEAD`.
- (b)-(e) unchanged from the plan stop; red set grows by nothing (both C2 tests are PINs, green on the base).

## Plan round 2 (correction 01, C1-C2)

- **C1**: new mutant row. R3 G2 (ii): restore `stated_na = (row["induction_type"] or "NATURALLY_ASPIRATED") ==
  "NATURALLY_ASPIRATED"` and the clause `if stated_na and after.induction != "NATURALLY_ASPIRATED" and (before.count <= 0
  or before.induction != after.induction): return True` in `_g2_cylinder_heuristic`; killed by
  `test_stated_na_heuristic_code_is_inserted`.
- **C2**: two PIN merge tests.
  - `test_three_cc_values_stay_collision`: BRANDA 1597, BRANDB 1598, BRANDC 1599 → `collision`. Mutant "accept adjacent
    1 cc steps" (`max - min == len(values) - 1` with consecutive values) → killed.
  - `test_non_displacement_conflict_stays_collision`: BRANDA NATURALLY_ASPIRATED, BRANDB TURBOCHARGED, all else equal
    → `collision`. Mutant "coalesce any field by first brand" (non-displacement conflicts take the first value instead of
    returning `None`) → killed.
- Counts: merge file 23 → **25**; step 2 **32 passed**; step 1 **293 passed, 8 skipped**; red run **8 failed, 24
  passed**.
- The RESULT names the RGX map majority share beside the two RGX changes (`PEUGEOT,221RA` 0.400; `CITROEN,U6UA0`
  0.833).

## Build (redispatch 01)

- Step 2 red (`pt/red`): `8 failed, 24 passed`, as predicted. Failures: merge `test_map_boxer_code_is_inserted`,
  `test_stated_na_heuristic_code_is_inserted`, `test_blank_against_value_collision_is_coalesced`,
  `test_one_cc_collision_takes_first_stating_brand_cc` (each `assert () == ('<code>',)`: skipped); decoder
  `test_vref_zero_with_map_boxer_gives_two_banks` and `test_real_boxer_vin_has_two_banks` (`assert 1 == 2`),
  `test_stated_na_is_not_replaced_by_turbo_hint` (TURBOCHARGED), `test_real_azq_vin_after_merge_is_na_and_maf_only`
  (`assert 0.0 == 1.198`).
- Steps 3-4: decoder and tool edits as planned. Also moved two decoder line cites in the tool's `_two_bank` and
  `_map_cylinders_unknown` comments (`:474-477` → `:479-482`, `:461` → `:465`): the decoder edit shifted them. The loop
  in `select_rows` raises `RuntimeError` on the unreachable "no row, no reason" case rather than an `assert` (ruff S101).
  After the code, before the merge: `1 failed, 31 passed` (only the AZQ real-VIN test, as planned).
- Step 5, `cd labs/vinlab && $PY tools/merge_tecdoc_extract.py` on the shipped db: skipped in_vref 1186, collision 9
  (`1E 2GRFE A112A2000 A20NHT B6 FA20 JB K10B LFW`), status 0, no_my_start 37, span_gap 0, map_banks 0,
  cylinder_heuristic 34; `inserted 40 rows; engine_ref now 1274 rows; schema rebuilt: no`. Compared with
  `git show b444481:…/vref.db` deserialised in memory: 40 new codes, 0 removed, 0 existing rows changed; every row
  equals Cowork's `vref_rehearsal.db`.
- Step 7: commit `50266c2` on `fix/T-VINA-14` (5 explicit paths).
- Step 8 mutants (stdin script; copy in `C:/4DApp/recheck/T-VINA-14/mut/<name>_<file>`, copied over, named tests,
  `git restore`): all 9 KILLED; porcelain afterwards: only this note.

| mutant | named tests | result |
|---|---|---|
| R1 BOXER clause removed | banks #1, #6 | KILLED, 2 failed |
| R1 PIN map V/W in the row branch | banks #2 | KILLED, 1 failed |
| R2 stated flag ignored | banks #4, #7 | KILLED, 2 failed |
| R2 PIN never replace | banks #5 | KILLED, 1 failed |
| R3 G1 BOXER clause restored | `test_map_boxer_code_is_inserted` | KILLED, 1 failed |
| R3 coalesce `== 1` → `<= 2` | `test_two_cc_spread_stays_collision` | KILLED, 1 failed |
| C1 G2 (ii) restored | `test_stated_na_heuristic_code_is_inserted` | KILLED, 1 failed |
| C2 accept adjacent 1 cc steps | `test_three_cc_values_stay_collision` | KILLED, 1 failed |
| C2 coalesce any field by first brand | `test_non_displacement_conflict_stays_collision` | KILLED, 1 failed |

- R5 measured (stdin script from `audit/scratch/C6`: base decoder from `git show b444481:…/decoder.py` executed in
  memory on `mut/base_vref.db`, against the committed decoder on the committed db): `decoded both 1131`, field changes
  `{'banks': 4, 'disp': 62, 'cyl': 3, 'induction': 2, 'air': 2, 'euro': 1, 'stress': 1}`; the same 7 VINs as the plan
  prediction (RESULT lists them). 233 inputs of `c6_lib.real_vins()` raise in both decoders alike.

## VERIFICATION GATE

| # | check | command | result |
|---|---|---|---|
| 1 | vinlab suite | Verification step 1 | `293 passed, 8 skipped` (plan round 2: 293/8) |
| 2 | named files | step 2 | `32 passed` (plan: 32) |
| 3 | dnalab, wired, ui | step 3 | `27 passed`, `41 passed`, `30 passed` (P6, unchanged) |
| 4 | reach | step 4 | `vref outcome: {'no_engine_code': 16, 'not_in_vref': 479, 'out_of_window': 68, 'row_applied': 568}` (P3) |
| 5 | second merge, ruff, log, porcelain | step 5 | `inserted 0 rows; engine_ref now 1274 rows; schema rebuilt: no`; no vref.db status line; `All checks passed!`; log `50266c2 3effcae 0e8654c 67bfd8c`; porcelain only the note (RESULT added after) |
| 6 | compile, ruff, ruff S, pyright | `py_compile`; `py -m ruff check`; `--select S`; `py -m pyright --pythonpath …` on the 4 files | compiled; `All checks passed!`; S: 101 hits, all S101 in the two test files (production files: `All checks passed!`); pyright `0 errors, 0 warnings` |
| 7 | import sanity | `$PY -c "…from wired import diagnose"` | `import ok` |
| 8 | isolation | `$PY audit/tools/isolation.py` | `violations: 4` (known R0-2) |
| 9 | anti-orphan | `grep -rn "induction_stated\|_coalesce\|_one_cc_spread"` | each read outside its definition |
| 10 | previous decisive failure absent | step 2 red run vs step 2 | 8 red tests now green; P2 banks-1 Subaru decodes now 2 |

Repo-wide gates (comlab, dtclab, gaslab, obdlab, symptomlab): NOT RUN (report-only; Cowork runs them at review).
Verdict: **CLEAN** (in-scope gates).

## CODE REVIEW

- Scope: every changed line traces to R1-R4 or to a cite the edit moved; no dnalab/wired/ui file touched; the
  out-of-scope list holds (`_cylinder_fallback`'s bank half, G2 (i)/(iii), map rows, `lookup_engine_ref` untouched).
- Contracts: no new payload field; `_cylinder_fallback` has one caller, updated.
- Provenance: the R1 comment cites `tools/extract_tecdoc_1q2019.py:64` (`NOT_V_ENGINE` holds `BOXER`); no new numeric
  literal except the ruled 1 cc.
- Boundaries: no cross-lab import.
- Tests: no network; fixture tests write only under `--basetemp`.
- Craft: `_coalesce` is computed once per code; `_new_row` takes it explicitly. Residual: `_two_bank` is now read only by
  G2 (iii) (still a reader, not an orphan).

## Revision 02 (review correction 02, test files only)

- Start 2026-11-04T17:15:29Z. HEAD `16b2e9e` (spec commits `15fb9fd`, `16b2e9e` after `50266c2`); porcelain: the note
  and the RESULT only. Ruling: task file R4 "Ruled (02, review …)"; the decoder, the tool and `vref.db` do not change.
- Added (a) `test_g1_runs_on_the_coalesced_row` and (b) `test_g2_runs_on_the_coalesced_row` to
  `test_vref_tecdoc_merge.py`, and (c) `test_blank_induction_takes_the_hint[""]` / `["   "]` to
  `test_vref_banks_induction.py`, with the R4 (02) inputs. All three are green on `50266c2`: they isolate surviving
  mutants, they do not test new behaviour.
- ruff `All checks passed!`; pyright `0 errors, 0 warnings, 0 informations`; the two files `36 passed`.
- Mutants (same procedure as step 8: copy in `mut/R02*_<file>`, copied over, `git restore`). For each, the named test
  and, separately, the other tests of the two files under the same mutant:

| mutant | named test | result | the other tests under the mutant |
|---|---|---|---|
| (a) `_g1_map_banks(group[0], map_rows)` | `test_g1_runs_on_the_coalesced_row` | KILLED, 1 failed | `35 passed, 1 deselected` (survivor before 02, confirmed) |
| (b) `_g2_cylinder_heuristic(group[0], map_rows)` | `test_g2_runs_on_the_coalesced_row` | KILLED, 1 failed | `35 passed, 1 deselected` |
| (c) `induction_stated=db_dict.get("induction_type") is not None` | `test_blank_induction_takes_the_hint` | KILLED, 2 failed | `34 passed, 2 deselected` |

  Mutant total: 12 run, 12 killed. Porcelain after the restores: the two test files (then committed), the note, the
  RESULT.
- Commit `22a926a test(T-VINA-14): …` (2 explicit paths) on `fix/T-VINA-14`.
- Reruns: step 1 `297 passed, 8 skipped`; step 2 `36 passed`; step 5 `inserted 0 rows; engine_ref now 1274 rows;
  schema rebuilt: no`, no `vref.db` status line, `All checks passed!`, log `22a926a 16b2e9e 15fb9fd 50266c2 3effcae
  0e8654c 67bfd8c`, porcelain = note + RESULT. `git diff --stat 50266c2..HEAD -- labs/vinlab/vinlab labs/vinlab/tools`
  prints nothing. Steps 3-4 were not rerun: no non-test file changed since `50266c2`.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| plan (first action → plan stop) | 2026-11-04T16:17:05Z | 2026-11-04T16:23:04Z | 5 | ABSENT |
| redispatch 01 (readiness → finish line) | 2026-11-04T16:44:56Z | 2026-11-04T16:50:04Z | 5 | ABSENT |
| revision 02 | 2026-11-04T17:15:29Z | 2026-11-04T17:17:20Z | 1 | ABSENT |
