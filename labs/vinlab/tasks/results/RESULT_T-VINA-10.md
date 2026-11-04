# Result

T-VINA-10: era from model year when the euro norm is unknown (F-C6-1, F-D1-13). Plan approved with C1-C4
(`labs/vinlab/tasks/corrections/T-VINA-10_plan_correction_20261104.md`); review revision 02 (task file R7 "Ruled (02,
review …)", spec `54541fb`). Note: `labs/vinlab/tasks/progress_notes/T-VINA-10.md` (`## Revision 02`).

## Status
completed

## Summary
`decode_vin_payload` now treats the euro as known only when the applied (in-window) `vref.db` row states a `euro_norm`
that `_EURO_MAP` recognises after `strip()` and `lower()`. Otherwise it adds the confidence flag `euro_unknown`, takes
`resolved_horizon` from `_year_to_horizon(model_year)` (or `HORIZON_LEGACY` with no year), and passes `""` as the euro
to `stress_idle_rpm` so the horizon fallback applies. `euro_emission_category` still emits `EURO_1` when unknown. The
new wiki §10.8 states the bands and the 2001 and 2011 edges. It gives 98/69/EC and 715/2007 as the general EU
passenger-car deadlines, names their exceptions (above 2,500 kg; Art. 10(3) specific social needs to 2012), calls the
edges the decoder's heuristic, and states the 1-year fuzz and C3's MODERN sentence. `_year_to_horizon` cites it.
`VIN_VOCABULARY.md` § 4 documents the flag (C1). The `f1_` probe uses R1's "euro known" population. The three named
2001-2002 snapshots change `resolved_horizon` LEGACY → ADAPTIVE and `stress_idle_rpm_target` 3000 → 3500. On the 1,131
real VINs, 416 decodes change exactly as P2 says, and no confidence changes (no euro-unknown VIN was HIGH). Revision 02
added 4 tests (strip/lower and blank `euro_norm`; no-year euro5) and the wiki wording. `decoder.py` is unchanged since
`56caaa1`.

## Files changed
Commit `56caaa1` on `fix/T-VINA-10` (9 files, +240/-16):
- `labs/vinlab/vinlab/decoder.py`: R1-R4 (one block in `decode_vin_payload`; imports `Horizon`, `_year_to_horizon`)
- `labs/vinlab/vinlab/overlay/horizon.py`: `# wiki: …§10.8` on the two year-literal lines; docstring kept (one caller)
- `labs/vinlab/wiki/10_decode_scope_rules.md`: new `## 10.8 Era from model year when the euro norm is unknown`
- `labs/vinlab/docs/VIN_VOCABULARY.md`: one § 4 row, `euro_unknown` (C1)
- `audit/scratch/C6/test_c6_probes.py`: `test_f1_horizon_follows_year_when_euro_unknown` population only (R6)
- `labs/vinlab/tests/unit/test_euro_unknown_horizon.py`: NEW, 12 tests
- `labs/vinlab/tests/fixtures/vindna_pre_refactor/{VF1357K0F17697151,VF1BB0FCF23935016,VF1CB05CF25935016}.json`:
  `resolved_horizon`, `stress_idle_rpm_target`

Commit `3216544` on `fix/T-VINA-10` (revision 02, 2 files, +43/-6):
- `labs/vinlab/tests/unit/test_euro_unknown_horizon.py`: +`test_euro_norm_is_matched_after_strip_and_lower` (3 cases)
  and +`test_no_year_euro5_row_gives_modern`; 16 tests in total
- `labs/vinlab/wiki/10_decode_scope_rules.md`: §10.8 deadline wording (c)

Uncommitted, as step 5 expects: the progress note and this RESULT.

## Commands executed
- First action and Preconditions (round 1): `fix/T-VINA-10`, `0d299ee`, clean; `0`, `checked`. Revision 02:
  `EXISTS test`, `1`, `checked`, no `MISSING`.
- `rehearse.py` and `rehearse.py --corpus` on the base; `rehearse.py` on the build.
- Red run (round 2): `cd labs/vinlab && $PY -m pytest -q -p no:cacheprovider tests/unit/test_euro_unknown_horizon.py
  --basetemp=C:/4DApp/recheck/T-VINA-10/pt/t` → `7 failed, 5 passed`.
- `### Verification ###` steps 1-5, verbatim, on `56caaa1`. Steps 1, 2 and 5 again on `3216544`.
- `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe` and `py -m ruff check --select S` on the touched
  `.py` files; the full C6 probe file; `audit/tools/isolation.py`; the deployed-layout `from wired import diagnose`.
- Mutants M1-M11 (copies in `C:/4DApp/recheck/T-VINA-10/mut/`, `cp` over, named test, `git restore`).

## Validation evidence
| step | expected | got |
|---|---|---|
| 1 | `313 passed, 8 skipped` (revision 02: 309 + 4) | `313 passed, 8 skipped in 9.08s` (on `3216544`; `309 passed, 8 skipped` on `56caaa1`) |
| 2 | `16 passed` (revision 02: 12 + 4) | `16 passed in 3.30s` (on `3216544`; `12 passed` on `56caaa1`) |
| 3 | dnalab 27, wired 41, ui 30 | `27 passed`, `41 passed`, `30 passed` (on `56caaa1`; revision 02 changes no code) |
| 4 | `2 passed`; `horizon changes {} total 0` | `2 passed, 49 deselected`; `horizon changes {} total 0` (on `56caaa1`) |
| 5 | `All checks passed!`; commits; note + RESULT | `All checks passed!`; log below; status below (on `3216544`) |

`rehearse.py` on the base:
```
{'decoded': 1131, 'no_applied_row': 563, 'row_euro_null': 541, 'euro_unknown_no_year': 438, 'euro_known': 27}
horizon changes {('HORIZON_LEGACY', 'HORIZON_ADAPTIVE'): 416} total 416
by year [(2001, 89), (2002, 59), (2003, 43), (2004, 49), (2005, 50), (2006, 26), (2007, 20), (2008, 25), (2009, 20), (2010, 35)]
stress rpm changes {(3000, 3500): 416} total 416
```
`rehearse.py` on the build (`56caaa1`):
```
{'decoded': 1131, 'no_applied_row': 563, 'row_euro_null': 541, 'euro_unknown_no_year': 438, 'euro_known': 27}
horizon changes {} total 0
by year []
stress rpm changes {} total 0
```
`rehearse.py --corpus` on the base: `{'decodable': 306, 'runs_changed': 303, 'crash': 3}`. 303 is `submitted_at`
timestamp noise that the script does not filter. The real change is 1 run (`resolved_horizon`,
`processing_confidence_rating`) and 0 verdicts. `rehearse.py --corpus` on the build: NOT RUN by me (Cowork ran it).

Previous decisive failure absent: on the base, `-k f1_` was `2 failed` (`assert not ['JF1KD5LL01B005778', …]`;
`documented fallback is never called`). On the build, both pass. The probe prints `euro unknown …=1104; horizon !=
documented year fallback: 0`, and the second probe finds `decoder.py:34` and `decoder.py:672`.

Other gates (on `56caaa1`): the full C6 file is `14 failed, 37 passed` (base `16 failed, 35 passed`; only the `f1_`
pair changed colour). pyright `0 errors` on the 3 touched `.py` files. Import `ok`. Isolation `violations: 4`.
Revision 02: ruff on the test file `All checks passed!`.

Mutants, 11 in total, each failing its named test:
- **M1** `euro_known = bool(db_dict)` → `test_null_euro_row_takes_year`, `test_unrecognised_euro_string_is_unknown`
  (2 failed), and the R6 probe (1 failed, 1 passed).
- **M2** → `test_no_row_2005_takes_adaptive_from_year`.
- **M3** → the same test (stress 3000).
- **M4** → `test_no_year_no_row_stays_legacy_with_flag`, `test_flag_alone_demotes_high_to_partial`.
- **M5** (`<= 2001`) → `test_year_bands_follow_wiki_10_8`.
- **M6** hard-coded `>= 2001` → `test_decoder_calls_the_cited_year_helper`.
- **M7** year for every VIN → `test_euro5_row_stays_modern`.
- **M8** `euro=""` always → `test_euro4_row_keeps_euro_stress_rule`.
- **M9** drop `.strip()` → `test_euro_norm_is_matched_after_strip_and_lower[mixed_case_spaces]` (1 failed, 2 passed).
- **M10** drop `.lower()` → the same case (1 failed, 2 passed).
- **M11** no year always LEGACY → `test_no_year_euro5_row_gives_modern`.

After the mutants, the tree is clean and the file is `16 passed`.

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1 `313 passed, 8 skipped`; step 2 `16 passed` (revision 02 counts); M1-M11 each fail a named test |
| 2 | MET | step 3 `27`/`41`/`30 passed` (P4, as planned); changed values named in the plan (3 snapshots × 2 fields) |
| 3 | MET | step 4 `2 passed, 49 deselected`; `horizon changes {} total 0` |
| 4 | MET | ruff `All checks passed!`; `56caaa1` and `3216544` on `fix/T-VINA-10` after spec commits `0d299ee`, `49005b7`, `54541fb`; status = note + RESULT |

## Decisions the task did not specify
- The raw euro is read from `db_dict` in `decode_vin_payload` (the post-window row) and not from a widened techmask
  tuple. Approved in round 1.
- `""` is the unknown euro for `stress_idle_rpm`; `Horizon.LEGACY` is explicit with no year. Approved in round 1.
- The tests observe the internal flags through a `monkeypatch` spy on the instance's `_compute_confidence`, because the
  flags are not serialised.
- Test VINs are real VINs from the C6 set. Test rows are set on a `tmp_path` copy of `vref.db` (F16D3 NULL, 14K4F
  `euro5`, RFK `Euro IV`, EJ20 NULL or 2000 cc or a blank/mixed-case `euro_norm`, 1KR-FE `euro5`).
- Revision 02 (b) uses `JTDJG18C40N041061`: no model year, and the 1KR-FE row is applied (no year to compare).
- Revision 02 (c) names the later 98/69/EC date for cars above 2,500 kg without stating that date. The ruling names no
  date, and I did not verify one.
- §10.8 got the anchor `{#RULE_ERA_FROM_YEAR}` and a `# source:` line in the page's form. The front matter, graph and
  entity lists are untouched.

## Pre-existing changes preserved
The start state was clean apart from my own untracked note. `C:/4DApp` `LOOP_STATE.md` and its launcher are outside
the clone and untouched. Pre-existing probe-file lint is unchanged: F401 at line 319 (`test_f12`) and ruff S
`23 errors` before and after.

## Rollback
Both commits: `git -C C:/4DApp/repo revert 3216544 56caaa1` on `fix/T-VINA-10` (the spec commit `54541fb` between
them is Cowork's and stays). Revision 02 alone: `git -C C:/4DApp/repo revert 3216544`. Nothing is pushed.

## Remaining risks or uncertainties
- `_year_to_horizon` returns MODERN for a year below 1990. The H2 guard makes that unreachable today, and it is out of
  this row's scope.
- The `rehearse.py --corpus` diff filter counts `submitted_at`. That is Cowork's file, reported and not edited.
- `audit/tools/baseline.sh` and the repo-wide report-only suites: NOT RUN (Cowork runs them at review).
- Steps 3 and 4 were not rerun on `3216544`. Revision 02 changes only the test file and the wiki, and the ruling asks
  for steps 1, 2 and 5.

## Step 5 status
```
$ git status --porcelain
?? labs/vinlab/tasks/progress_notes/T-VINA-10.md
?? labs/vinlab/tasks/results/RESULT_T-VINA-10.md
```

## Branch and log
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-10
$ git -C C:/4DApp/repo log --oneline 2ff9211..HEAD
3216544 test(T-VINA-10): euro_norm strip/lower and no-year euro5 tests; wiki 10.8 deadline wording
54541fb spec(T-VINA-10): review correction 02 (tests and wiki wording); register R3 rows (T-VINA-17, 18, T-AUD-7b)
56caaa1 fix(T-VINA-10): era from model year when the euro norm is unknown
49005b7 spec(T-VINA-10): plan correction 01 (approved with C1-C4)
0d299ee spec(T-VINA-10): era from model year when the euro norm is unknown
```
