# T-VINA-10 progress note: era from model year when the euro norm is unknown

Task file: `labs/vinlab/tasks/T-VINA-10_era_from_year_when_euro_unknown(4).md` (plan: REQUIRED). This session is the
plan stop. No repo file is edited. The only write is this note. No hand-back finding: no `.blocker.json`.

## Readiness

- (a) Starting state matches the task. `git branch --show-current` = `fix/T-VINA-10`; `git log --oneline -1` =
  `0d299ee spec(T-VINA-10): era from model year when the euro norm is unknown`; `git rev-parse HEAD^` = `2ff9211…`.
  **Base = `0d299ee`** (the spec commit, child of `2ff9211`; step 5 logs `2ff9211..HEAD`). `git status --porcelain`
  printed nothing. Preconditions printed `0`, `checked`, and no `MISSING` or `EXISTS` line. P1, P2, P3 and P4 reproduce
  on the base:
  - `rehearse.py`: `{'decoded': 1131, 'no_applied_row': 563, 'row_euro_null': 541, 'euro_unknown_no_year': 438,
    'euro_known': 27}`; `horizon changes {('HORIZON_LEGACY', 'HORIZON_ADAPTIVE'): 416} total 416`; by year 2001 89,
    2002 59, 2003 43, 2004 49, 2005 50, 2006 26, 2007 20, 2008 25, 2009 20, 2010 35; `stress rpm changes
    {(3000, 3500): 416}`.
  - `rehearse.py --corpus` (68 s): `{'decodable': 306, 'runs_changed': 303, 'crash': 3}`; fields
    `.user_input_echo_audit.submitted_at` 303, `.execution_meta.resolved_horizon` 1,
    `.execution_meta.processing_confidence_rating` 1; no `verdict_differs` key, so 0 verdicts. The 303 is timestamp
    noise: the script's filter has no `submitted_at`. The real change is 1 run, as P3 says.
  - vinlab `297 passed, 8 skipped`; dnalab `27 passed`; wired `41 passed`; ui `30 passed`; `-k f1_`: `2 failed, 49
    deselected` (`test_f1_horizon_follows_year_when_euro_unknown`, `test_f1_year_fallback_has_no_production_caller`).
- (b) Test fails for the intended reason. Both `f1_` probes are red on the base for the finding: the first lists
  euro-unknown VINs whose horizon is not `_year_to_horizon(model_year)` (`JF1KD5LL01B005778`, `JHMAP11305S202318`, …);
  the second prints `documented fallback is never called`. The new tests do not exist yet (plan stage). Their predicted
  red run is under "Plan → Tests".
- (c) Independent decisive value. With my own euro-known code (not `rehearse.py`) over the 1,131 real VINs:
  euro known 27, unknown 1,104 (no year 438, 1990-2000 250, 2001-2010 416). All 416 are `HORIZON_LEGACY`/3000 today.
  Derived from the rules alone: a 2001-2010 year gives `ADAPTIVE` (`horizon.py:33-37`), and with no euro rule the
  ADAPTIVE fallback is 3500 (`stress_rpm.py:47-51`, LLD § 9). So 416 decodes go LEGACY → ADAPTIVE and 3000 → 3500,
  which equals P2. 0 euro-unknown VINs are `HIGH` today, so R4 changes no real VIN's confidence (P1).
- (d) No contradiction or missing decision prevents implementation. One gap is recorded below (assumption 2: the f9
  vocabulary probe). It is not a stop.
- (e) Teach-back: the decoder treats the euro as known only when the applied in-window `vref.db` row states a
  recognised `euro_norm`; otherwise it flags `euro_unknown`, takes the era from the model year (wiki §10.8) and lets the
  stress RPM use its horizon fallback. The decisive check is both `f1_` probes passing and `rehearse.py` on the build
  printing `horizon changes {} total 0`, with only the three named 2001-2002 snapshots changing.

## Assumptions worked past

1. **"Applied row" is `db_dict` after the window check.** `decode_vin_payload` sets `db_row = None` when the year is
   outside `[my_start, my_end]` (`decoder.py:589-594`), and `_apply_vref_techmask` returns `db_dict = {}` then. So
   "euro known" is `(db_dict.get("euro_norm") or "").strip().lower() in _EURO_MAP`, the same key `_normalise_euro`
   uses. No year means the row is kept, as today.
2. **`euro_unknown` is not added to `VIN_VOCABULARY.md` §4.** `audit/scratch/C6/test_f9_flags_documented` requires
   every `conf_flags.append("…")` literal to appear there. `labs/vinlab/docs/VIN_VOCABULARY.md` is not in
   `### Files to touch ###`. The probe is already red on the base (missing `vds_engine_ambiguous`,
   `wmi_brand_missing`; command: `cd audit/scratch/C6 && $PY -m pytest -q -s -p no:cacheprovider test_c6_probes.py -k
   f9_flags`), so it stays red with a third missing flag. No colour changes. If Cowork wants the row, the correction can
   authorise one line: `` | `euro_unknown` | no applied `vref.db` row states a recognised `euro_norm`; era from the
   model year (wiki §10.8) | PARTIAL | ``. I did not write the flag through a constant to hide it from the probe.
3. **The `horizon.py` docstring stays.** The plan adds one caller (`decoder.py`, euro unknown only). That makes "Used
   only when euro_emission_category is unknown" true, so R5's condition for dropping it ("a second caller") is not met.
4. **The rehearsal's corpus noise is not mine to fix.** `rehearse.py` is Cowork's file. I report its 303
   `submitted_at` diffs as noise, with the 1 real change.

## Plan

### Approach

One block in `decode_vin_payload` changes: the `# --- stress RPM ---` block at `decoder.py:663-670`. The techmask
tuple and `_normalise_euro` stay as they are; the raw value is read from `db_dict`, which the method already holds.

```python
        # --- horizon and stress RPM ------------------------------------------
        # T-VINA-10 R1: the euro is known only when the applied (in-window) vref.db row states a recognised euro_norm
        euro_known = (db_dict.get("euro_norm") or "").strip().lower() in _EURO_MAP
        if euro_known:
            horizon = euro_to_horizon(_euro_emission_category)
        else:
            conf_flags.append("euro_unknown")
            # wiki: labs/vinlab/wiki/10_decode_scope_rules.md §10.8 — era from the model year; no year stays LEGACY
            horizon = _year_to_horizon(model_year) if model_year is not None else Horizon.LEGACY
        _stress_idle_rpm_target = stress_idle_rpm(
            euro=_euro_emission_category if euro_known else "",  # "" takes the horizon fallback (LLD § 9)
            ...unchanged...
        )
```

Imports: `_year_to_horizon` from `vinlab.overlay.horizon`; `Horizon` added to the existing `vinlab.models` import (it is not
imported today). `euro_emission_category` keeps `EURO_1` when unknown (R1).

Choices this task leaves open:
- Where to read the raw euro. Taken: `db_dict` in `decode_vin_payload`. Rejected: a 22nd element in the
  `_apply_vref_techmask` return tuple, or a sentinel from `_normalise_euro`. Both widen the diff and touch callers.
- No year, euro unknown. Taken: explicit `Horizon.LEGACY`. Rejected: `euro_to_horizon(EURO_1)`. Same value, but the
  explicit form states the rule.
- The euro argument when unknown. Taken: `""` (what `rehearse.py` passes; the signature is `euro: str`). Rejected:
  `None` (not in the signature).
- Wiki: only the new section `## 10.8 Era from model year when the euro norm is unknown {#RULE_ERA_FROM_YEAR}`, after
  §10.7, in the page's form (prose, a code block of the bands, a `# source:` line). Rejected: front-matter, graph and
  entity lines (not asked for). Content: the three bands; Euro 3 compulsory for every new petrol car registered from
  2001-01-01 (Directive 98/69/EC) so 2001 is ADAPTIVE; Euro 5 from 2011-01-01 (Regulation (EC) No 715/2007) so 2011
  is MODERN; this settles the overlapping edges of `labs/comlab/wiki/04_horizon_eras.md:50-51` ("pre-1997 → ~2001",
  "~2001–2011"); a model year is not a registration date, so each edge has a 1-year fuzz; H2 caps decoded years at
  2010, so MODERN is never reached by a decoded VIN; no year → LEGACY; the flag `euro_unknown`.
- `horizon.py`: `# wiki: labs/vinlab/wiki/10_decode_scope_rules.md §10.8` on each of the two `if` lines that hold the
  year literals (1990, 2000; 2001, 2010). No code change. Docstring stays (assumption 3).

### One line per rule: edit, test, mutant

| rule | edit | test that pins it | mutant (step 9) and the test that kills it |
|---|---|---|---|
| R1 | `euro_known` from `db_dict` + `_EURO_MAP` | `test_null_euro_row_takes_year`, `test_unrecognised_euro_string_is_unknown` | M1 `euro_known = bool(db_dict)` (any applied row is known): both tests fail (LEGACY ≠ ADAPTIVE) |
| R2 | `_year_to_horizon(model_year)` when unknown with a year | `test_no_row_2005_takes_adaptive_from_year` | M2 unknown branch `horizon = Horizon.LEGACY`: fails (LEGACY ≠ ADAPTIVE) |
| R3 | `euro=""` when unknown | `test_no_row_2005_takes_adaptive_from_year` (stress 3500) | M3 `euro=_euro_emission_category` always: NA EURO_1 gives 3000 ≠ 3500 |
| R4 | `conf_flags.append("euro_unknown")` | `test_no_year_no_row_stays_legacy_with_flag`, `test_flag_alone_demotes_high_to_partial` | M4 delete the append: flag absent; HIGH ≠ PARTIAL |
| R5 | citations; wiki §10.8 | `test_year_bands_follow_wiki_10_8` (PIN) | M5 `1990 <= year <= 2001` in `_year_to_horizon`: 2001 gives LEGACY ≠ ADAPTIVE (the 3 roundtrip snapshots also fail) |
| R6 | probe population = R1's rule | `test_f1_horizon_follows_year_when_euro_unknown` | M1 on the decoder: the revised probe fails (it lists NULL-row 2001-2010 VINs). The old "any vref row" population skips those VINs and would pass M1 |

### Tests: `labs/vinlab/tests/unit/test_euro_unknown_horizon.py` (NEW, 9 tests)

A `vref_copy` fixture as in `test_vref_banks_induction.py`: `shutil.copyfile` of `vref.db` to `tmp_path`, optional
SQL, a `RobustVINDecoder(data_dir)` with `db_path` set to the copy. Every test decodes on a copy. A `flags` helper
wraps the instance's `_compute_confidence` with `monkeypatch` to record the flag list (the flags are not serialised;
`VIN_VOCABULARY.md` §4).

| # | test | VIN (base facts) | copy SQL | asserts | red before code |
|---|---|---|---|---|---|
| 1 | `test_no_row_2005_takes_adaptive_from_year` | `JHMAP11305S202318` (2005, F20C2 not in vref, NA 2.0 L) | none | ADAPTIVE, stress 3500, EURO_1, flag | yes |
| 2 | `test_no_row_1995_stays_legacy` (PIN) | `KLATF19T1SB604957` (1995, G15SF not in vref) | none | LEGACY, stress 3000 | no |
| 3 | `test_no_year_no_row_stays_legacy_with_flag` | `JMZBA145201537959` (no year, Z5 not in vref) | none | year None, LEGACY, stress 3000, flag | yes (flag) |
| 4 | `test_euro4_row_gives_adaptive_without_flag` (PIN) | `JF1GG9LK43G020691` (2003, EJ20 1998-2010 euro4) | none | ADAPTIVE, EURO_4, HIGH, no flag | no |
| 5 | `test_null_euro_row_takes_year` | `KL1NF356J8K002340` (2008, F16D3 2003-2020) | `SET euro_norm = NULL` on F16D3 | ADAPTIVE, stress 3500, EURO_1, flag | yes |
| 6 | `test_out_of_window_row_year_decides` | `SARRFMNHMAD141869` (2010, 14K4F 1991-2006) | `SET euro_norm = 'euro5'` on 14K4F | ADAPTIVE (not the row's MODERN), flag | yes |
| 7 | `test_unrecognised_euro_string_is_unknown` | `VF33BRFKC83559254` (2008, RFK 2003-2020) | `SET euro_norm = 'Euro IV'` on RFK | ADAPTIVE, EURO_1, stress 3500, flag | yes |
| 8 | `test_flag_alone_demotes_high_to_partial` | `JF1GG9LK43G020691` (HIGH today, no flags) | `SET euro_norm = NULL` on EJ20 | PARTIAL, ADAPTIVE from 2003 | yes |
| 9 | `test_year_bands_follow_wiki_10_8` (PIN) | none | none | `_year_to_horizon`: 1990, 2000 LEGACY; 2001, 2010 ADAPTIVE; 2011 MODERN | no |

Tests 1-7 are R7's seven cases. Tests 8 and 9 are added: 8 is the only externally visible effect of R4 (the flag
alone moves HIGH to PARTIAL); 9 gives R5's edges a test that a threshold mutant fails. Predicted red run (step 2,
before the decoder edit): `6 failed, 3 passed` (2, 4, 9 pass).

### Changed test values (R8)

Measured with an in-memory patch of `RobustVINDecoder.decode_vin_payload` to R1-R4, running each suite in-process
(no file written). vinlab: `3 failed, 294 passed, 8 skipped`; dnalab `27 passed`; wired `41 passed`; ui `30 passed`.
The three failures are `test_vindna_roundtrip.py::test_vindna_roundtrip_byte_identical`, and the field diff against
each snapshot is exactly:
- `tests/fixtures/vindna_pre_refactor/VF1357K0F17697151.json` (2001): `resolved_horizon` `HORIZON_LEGACY` →
  `HORIZON_ADAPTIVE`; `stress_idle_rpm_target` 3000 → 3500.
- `tests/fixtures/vindna_pre_refactor/VF1BB0FCF23935016.json` (2002): the same two fields, the same values.
- `tests/fixtures/vindna_pre_refactor/VF1CB05CF25935016.json` (2002): the same two fields, the same values.
- `WBA4W9C5ZLYYYYYYY.json` (1990): no change. `confidence` stays `PARTIAL` in all four.

No other test, fixture or downstream value changes. The edit is two values per file, in place (the files are LF;
`git ls-files --eol` shows `i/lf w/lf`).

### Predicted verification output

1. vinlab `306 passed, 8 skipped` (297 + 9).
2. `9 passed`.
3. dnalab `27 passed`, wired `41 passed`, ui `30 passed` (P4, unchanged).
4. `2 passed, 49 deselected`; `rehearse.py | sed -n 3p` → `horizon changes {} total 0`. `rehearse.py` on the build:
   the same `euro_known 27` / `row_euro_null 541` / `no_applied_row 563` line as the base.
5. `All checks passed!`; `git log --oneline 2ff9211..HEAD` = my commit(s) over `0d299ee`; `git status --porcelain` =
   `?? labs/vinlab/tasks/progress_notes/T-VINA-10.md`, `?? labs/vinlab/tasks/results/RESULT_T-VINA-10.md`.

Other probes: the full C6 file is `16 failed, 35 passed` on the base; I expect `14 failed, 37 passed` (only the two
`f1_` probes change colour; f9 stays red, assumption 2).

### Gates the plan adds

- **R6 probe population.** Checked on: the 1,131 real VINs (`L.real_vins()`), with my own R1 code: 1,104 euro unknown,
  27 known. Runs over: the same population, via step 4 (`pytest test_c6_probes.py -k f1_`). False pass: a decoder that
  derives the era from the year for every VIN (euro known too) passes this probe, because it checks only euro-unknown
  VINs; test 4 (euro4 → ADAPTIVE with EURO_4, HIGH) and the 27 known VINs in `rehearse.py` cover that side. False
  fail: none found; a VIN whose `_resolve_engine` result differs from the decode's (ambiguity flags are discarded in
  the probe) would mis-classify, but the probe calls the same resolver with the same inputs.
- **Test 8 (flag → PARTIAL).** Checked on: EJ20 with a NULL euro on a copy. False pass: none, since the base value is
  HIGH. False fail: if the shipped EJ20 row later gains a NULL CoC field, the base would already be PARTIAL; test 4
  pins HIGH, so that drift shows as a test 4 failure first.
- **Order.** Step 6 (fixtures) changes what step 7 runs against. Steps 2-5 do not touch the snapshots, so the
  roundtrip test is red between steps 3 and 6 for the three named files only.

### Commands and the paths they write

- Steps 2, 7: the `### Verification ###` pytest lines; `--basetemp` under `C:/4DApp/recheck/T-VINA-10/pt/`.
- Step 3-6 edits: `labs/vinlab/vinlab/decoder.py`, `labs/vinlab/vinlab/overlay/horizon.py`,
  `labs/vinlab/wiki/10_decode_scope_rules.md`, `audit/scratch/C6/test_c6_probes.py` (lines 39-63 only),
  `labs/vinlab/tests/unit/test_euro_unknown_horizon.py`, the three snapshot JSON files above.
- Inner loop: `$PY -m py_compile`, `py -m ruff check`, `py -m ruff check --select S`, `py -m pyright --pythonpath
  C:/4DApp/.venv/Scripts/python.exe` on each edited `.py` file.
- Step 8: `git add <those 8 paths>`, then one commit `fix(T-VINA-10): …` on `fix/T-VINA-10`.
- Step 9: copies under `C:/4DApp/recheck/T-VINA-10/mut/`, `cp` over, the named test, `git restore <path>`.
- R6 edit (probe, lines 51-53): the "euro known" skip becomes the R1 rule: look up the row, drop it outside its window,
  skip the VIN only when `(row or {}).get("euro_norm")` stripped and lowered is in `vinlab.decoder._EURO_MAP`. The
  print label "no vref.db row (euro unknown)" becomes "euro unknown (applied row has no recognised euro_norm)".

## Plan round 2

Approval: `labs/vinlab/tasks/corrections/T-VINA-10_plan_correction_20261104.md` (APPROVED with C1-C4), spec commit
`49005b7`. Redispatch start 2026-11-04T17:52:45Z. `git status --porcelain` = only this note; HEAD `49005b7` on
`fix/T-VINA-10`. The correction has no `### Plan-time digest ###` table (`grep -c` = 0), so there is nothing to recompute.

- **C1:** `labs/vinlab/docs/VIN_VOCABULARY.md` § 4 gains the drafted `euro_unknown` row (PARTIAL), after
  `vref_year_out_of_window`. f9 stays red on its two older missing flags.
- **C2:** two PIN tests. `test_euro5_row_stays_modern`: `VF7SA5FR8AW511081` (base: 2010, EURO_5, MODERN, 4000, HIGH)
  stays MODERN with no flag; it fails the "year for every VIN" mutant (gives ADAPTIVE). `test_euro4_row_keeps_euro_stress_rule`:
  EJ20 on a copy with `displacement_cc = 2000`, `JF1GG9LK43G020691` (base on the copy: 2.0 L, EURO_4, NA, 4000) gives
  4000; it fails the `euro=""`-for-every-VIN mutant (fallback 3500).
- **C3:** §10.8 states that the unknown-euro year fallback cannot give MODERN inside the supported years (H2 caps them
  at 2010), and that a recognised euro5 or later on the applied row still gives MODERN.
- **C4:** `test_decoder_calls_the_cited_year_helper` monkeypatches `vinlab.decoder._year_to_horizon` to return
  `Horizon.MODERN` and asserts `JHMAP11305S202318` decodes MODERN. The decoder imports the name into its module and
  calls it by that name. Mutant M6: a hard-coded `Horizon.ADAPTIVE if model_year >= 2001 else Horizon.LEGACY` fails it.
- **New counts:** the new file holds 12 tests; red run `7 failed, 5 passed` (the 5 green: tests 2, 4, 9 and the two C2
  PINs); step 2 `12 passed`; step 1 `309 passed, 8 skipped`. Other suites unchanged (dnalab 27, wired 41, ui 30).
- **Mutants (step 9):** M1-M5 as in round 1, plus M7 "year for every VIN" (killed by `test_euro5_row_stays_modern`),
  M8 `euro=""` for every VIN (killed by `test_euro4_row_keeps_euro_stress_rule`) and M6 above.
- Step 8 commit adds `VIN_VOCABULARY.md` (9 paths).

## Build (redispatch)

- Step 2, red run of the new file before the decoder edit: `7 failed, 5 passed`. The 7 failures, each for the intended
  reason: 5 on `LEGACY == ADAPTIVE`, one `'euro_unknown' in ['engine_not_in_vref']`, one `HIGH == PARTIAL`, and C4 on
  `vinlab.decoder has no attribute '_year_to_horizon'`. Passing: tests 2, 4, 9 and the two C2 PINs.
- Step 3, `decoder.py` (+12/-4) and `horizon.py` (two `# wiki:` comments): `12 passed`, ruff clean.
- Steps 4-5: wiki §10.8 (+37, with C3), `VIN_VOCABULARY.md` § 4 row (C1), probe lines 41-58 (R6). `-k f1_`:
  `2 passed`; the probe prints `euro unknown (applied row has no recognised euro_norm)=1104; horizon != documented year
  fallback: 0`. The second probe now finds `decoder.py:34` and `decoder.py:672`.
- Step 6: the three snapshots, `resolved_horizon` and `stress_idle_rpm_target` only (`git diff`: 6 lines).
- Step 8: `56caaa1 fix(T-VINA-10): …` on `fix/T-VINA-10`, 9 paths by name. The first commit attempt was chained after
  `cd … &&` and `bash_guard` refused it; I re-ran it as a single `git -C` command.
- Step 9, mutants (copies in `C:/4DApp/recheck/T-VINA-10/mut/`, `git restore` after each; tree clean afterwards and
  the file `12 passed`):

| mutant | edit | named test | result |
|---|---|---|---|
| M1 (R1) | `euro_known = bool(db_dict)` | `test_null_euro_row_takes_year`, `test_unrecognised_euro_string_is_unknown` | 2 failed |
| M1 → R6 | same decoder, probe `-k f1_` | `test_f1_horizon_follows_year_when_euro_unknown` | 1 failed, 1 passed |
| M2 (R2) | unknown branch `horizon = Horizon.LEGACY` | `test_no_row_2005_takes_adaptive_from_year` | 1 failed |
| M3 (R3) | `euro=_euro_emission_category` always | `test_no_row_2005_takes_adaptive_from_year` | 1 failed |
| M4 (R4) | append removed | `test_no_year_no_row_stays_legacy_with_flag`, `test_flag_alone_demotes_high_to_partial` | 2 failed |
| M5 (R5) | `1990 <= year <= 2001` | `test_year_bands_follow_wiki_10_8` | 1 failed |
| M6 (C4) | hard-coded `model_year >= 2001` | `test_decoder_calls_the_cited_year_helper` | 1 failed |
| M7 (C2) | known euro uses the year whenever a year exists | `test_euro5_row_stays_modern` | 1 failed |
| M8 (C2) | `euro=""` always | `test_euro4_row_keeps_euro_stress_rule` | 1 failed |

## VERIFICATION GATE

Run from `C:/4DApp/repo` in Git Bash on `56caaa1`, exactly as `### Verification ###`:

| step | expected (plan round 2) | got |
|---|---|---|
| 1 vinlab | `309 passed, 8 skipped` | `309 passed, 8 skipped in 7.29s` |
| 2 new file | `12 passed` | `12 passed in 2.67s` |
| 3 dnalab / wired / ui | `27` / `41` / `30 passed` | `27 passed` / `41 passed` / `30 passed` |
| 4 probes | `2 passed`; `horizon changes {} total 0` | `2 passed, 49 deselected`; `horizon changes {} total 0` |
| 5 | `All checks passed!`; commits; note + RESULT | `All checks passed!`; `56caaa1`, `49005b7`, `0d299ee`; status in RESULT |

Absence of the previous decisive failure: the base's `f1_` failures (`assert not ['JF1KD5LL01B005778', …]` and
`documented fallback is never called`) are gone, and `rehearse.py` on the build prints `stress rpm changes {} total 0`
and the same `euro_known 27`, `row_euro_null 541`, `no_applied_row 563`, `euro_unknown_no_year 438` as the base.
Also run: the full C6 file `14 failed, 37 passed` (base `16 failed, 35 passed`; only the two `f1_` probes changed
colour; f9 now lists `euro_unknown` as documented and stays red on `vds_engine_ambiguous`, `wmi_brand_missing`).
pyright on the three `.py` files: `0 errors, 0 warnings, 0 informations`. Deployed-layout import: `import ok`.
`audit/tools/isolation.py`: `violations: 4`. Not run: `audit/tools/baseline.sh` and the repo-wide report-only gates
(comlab, dtclab, gaslab, obdlab, symptomlab), which Cowork runs at review.

Verdict: **CLEAN-WITH-FINDINGS**. Every in-scope gate passed. The findings are pre-existing, in a file I touched:
`audit/scratch/C6/test_c6_probes.py` has ruff F401 at line 319 (`test_f12`, outside the `f1_` scope) and ruff S
`23 errors` (S101, plus S603/S607 on the second `f1_` probe's `subprocess` grep), the same as `git show HEAD~1:…`.

## CODE REVIEW

- Scope: every changed line traces to R1-R6, R8 or C1-C4. The probe edit is inside `test_f1_horizon_follows_year_…`.
  `switches.py`, the `>= 1996` literal, the COMLab wiki, `vref.db` and the contract enum are untouched.
- Contracts: no new payload field. `euro_emission_category` still emits `EURO_1` when unknown (R1).
- Provenance: each year literal in `_year_to_horizon` and the decoder fallback cite §10.8; §10.8 cites 98/69/EC and
  715/2007.
- Anti-orphan: the flag `euro_unknown` is read by `_compute_confidence` (any flag → PARTIAL), documented in
  `VIN_VOCABULARY.md` § 4, and asserted by 6 tests. `_year_to_horizon` now has its production caller.
- Boundaries: no cross-lab import. Tests use no network and decode against a `tmp_path` copy of `vref.db`.
- One process note: before the commit, to compare pyright against the base decoder, I ran `git stash push -- decoder.py`
  and `git stash pop`. The diff stat after the pop is identical (12+/4-). The base pyright line printed empty, so that
  comparison is NOT RUN. The current file has 0 errors.

## Revision 02

Ruling: task file R7 "Ruled (02, review …)", HEAD `54541fb` at start (2026-11-04T18:17:33Z). `decoder.py` is
unchanged since `56caaa1` (`git diff 56caaa1 HEAD --stat -- labs/vinlab/vinlab` is empty). Preconditions: `EXISTS
test`, `1`, `checked`, no `MISSING`, as revision 02 expects.

- (a) `test_euro_norm_is_matched_after_strip_and_lower`, 3 cases on EJ20 at `displacement_cc` 2000,
  `JF1GG9LK43G020691` (2003): `" EuRo 4 "` → EURO_4, ADAPTIVE, 4000, no flag; `""` and `"  "` → EURO_1, ADAPTIVE from
  the year, 3500 (fallback), flag.
- (b) `test_no_year_euro5_row_gives_modern`: `JTDJG18C40N041061` (no model year; 1KR-FE row 2005-2020 applied, euro4 on
  the shipped db) with `euro_norm = 'euro5'` on a copy → EURO_5, MODERN, no flag.
- (c) §10.8: both dates are the general EU deadlines for passenger cars; 98/69/EC gives passenger cars above 2,500 kg
  a later date; 715/2007 Art. 10(3) gives vehicles for specific social needs until 2012; 2001 and 2011 are the
  decoder's heuristic edges.
- The new tests pass on the committed decoder: they pin behaviour that `56caaa1` already has. Their proof is the
  mutants, run after the commit (copies in `C:/4DApp/recheck/T-VINA-10/mut/`, `git restore` after each):

| mutant | edit | named test | result |
|---|---|---|---|
| M9 | drop `.strip()` from `euro_known` | `test_euro_norm_is_matched_after_strip_and_lower` | `[mixed_case_spaces]` failed; 1 failed, 2 passed |
| M10 | drop `.lower()` from `euro_known` | the same | `[mixed_case_spaces]` failed; 1 failed, 2 passed |
| M11 | `if model_year is None: horizon = Horizon.LEGACY` before the stress call | `test_no_year_euro5_row_gives_modern` | 1 failed |

  Mutant total: 11 (M1-M8, M9-M11), plus the M1 → R6 probe run. Each fails its named test.
- Commit `3216544 test(T-VINA-10): …` (2 paths: the test file, the wiki).
- Rerun: step 1 `313 passed, 8 skipped` (309 + 4); step 2 `16 passed` (12 + 4); step 5 `All checks passed!`, log
  `3216544`, `54541fb`, `56caaa1`, `49005b7`, `0d299ee`, status = the note and the RESULT. After the mutants:
  `16 passed`, tree clean.
- The corpus line in the RESULT: the "no-op" inference is replaced by NOT RUN (Cowork ran the corpus rehearsal).

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| precheck and plan | 2026-11-04T17:25:14Z | 2026-11-04T17:33:33Z | 8 | ABSENT (no context meter in this session) |
| redispatch: plan round 2, build, verification, mutants, RESULT | 2026-11-04T17:52:45Z | 2026-11-04T17:58:39Z | 5 | ABSENT (no context meter in this session) |
| revision 02: tests, wiki, mutants, steps 1, 2, 5, note, RESULT | 2026-11-04T18:17:33Z | 2026-11-04T18:19:36Z | 2 | ABSENT (no context meter in this session) |

Total 15 minutes of session time, against an expected 40-60 and an 80-minute stop rule. The minutes come from
`date -u` and `$(( (end - start) / 60 ))`.
