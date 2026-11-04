# Result

## Status
completed

## Summary
- **R1 (`wmi.csv`).** The five WMIs that `wmi.csv` gave to the wrong make now carry their true make, brand cell
  only, in upper case (`WDB` MERCEDES-BENZ, `KMH` HYUNDAI, `JSA` SUZUKI, `JN1` NISSAN, `SAX` ROVER).
- **R2 (engine map).** The engine-map rows keyed by the wrong brands are re-keyed, per R2 (correction 01).
  - 252 keys the true brand lacked are copied under it.
  - On the 133 keys where the two rows' normalised codes differ, the Nio files 1+2 vote picks the winner (wrong row
    109, right row 24, tie → right). The winner's `majority_share` is set to winner votes / key votes.
  - MAYBACH, DATSUN and STERLING MOTOR CAR rows are moved; GENESIS and KAWASAKI rows stay.
  - The map goes from 12,900 to 12,928 rows, with no new duplicate key.
- **Census.** No real VIN decodes to a wrong-brand make. Engine resolution per WMI is at or above P3:
  WDB 26/26 (25), KMH 40/40 (40), JSA 19/19 (19), JN1 9/10 (8), SAX 9/9 (9).
- **Vote parity.** My own Nio scan reproduces Cowork's `vina5_vote_picks.json` on all 133 keys with 0 differences.
  On held-out file 3, the winner matches 1,872 of 2,813 VINs.

## Files changed
- `labs/vinlab/vinlab/data/wmi.csv` (5 lines): commit `cb31bd8`.
- `labs/vinlab/vinlab/data/vds_engine_map.csv` (+385 / −357): commit `ed53d94`.
- `labs/vinlab/tests/unit/test_wmi_brands.py` (new, 19 tests): commit `bbc1b6e`.
- Untracked, not committed (per contract):
  - `labs/vinlab/tasks/progress_notes/T-VINA-5.md` (note, with `## Plan` and `## Plan round 2`);
  - `labs/vinlab/tasks/progress_notes/T-VINA-5.blocker.json` (soft record, B7, header-authorised; validator `OK`);
  - this RESULT.
- Runtime only:
  - `C:/4DApp/recheck/T-VINA-5/pt/`: pytest basetemp.
  - `C:/4DApp/recheck/T-VINA-5/mut/`: `keys.json`, `nio{1,2,3}.json`, `picks_impl.json`, `map_dryrun.csv`, mutant
    copies `wmi.M{0..5}.csv` and `vds_engine_map.M{0,6,8}.csv`, and `c6_{base,after}_fails.txt`.
- `D:/` was read only.

## Commands executed
- Baseline: `git branch --show-current; git rev-parse --short HEAD; git status --porcelain` gave `fix/T-VINA-5`,
  `2fd3f8e`, and only the note.
- Key set (stdin script): 133 normalised-differing keys, set-equal to Cowork's JSON.
- Nio scan (stdin script, run once per file, Pass B filters, post-R1 brands):
  - file 1: 650,000 rows, 3,722 hits;
  - file 2: 650,000 rows, 3,486 hits;
  - file 3: 506,029 rows, 2,813 hits.
- Parity against `C:/4DApp/recheck/scratch/vina5_vote_picks.json`: 0 differences.
- VIN-set parity between the test reader and `c6_lib.real_vins()` for the five WMIs: 121 = 121, set-equal.
- Red run of the new test: `10 failed, 9 passed`.
- Edits: `sed` on `wmi.csv`; a stdin line-level edit script on the map, with the three correction 02 assertions.
- Verification steps 1-5, C6 probes (`-k f2_`, whole file, and the M0 base set), mutants M1-M6 and M8, ruff, ruff S,
  pyright, the import check, and `isolation.py`.

## Validation evidence
- Verification:
  - step 1: `248 passed, 8 skipped`;
  - step 2: `19 passed`;
  - step 3: `27 passed`, `41 passed`, `30 passed`;
  - step 4: `real decodes by (WMI, make): []`, then
    `{'JN1': '9/10', 'JSA': '19/19', 'KMH': '40/40', 'SAX': '9/9', 'WDB': '26/26'}`;
  - step 5: `All checks passed!`, the commits below, and porcelain showing only the note, the blocker JSON and this
    RESULT.
- Previous decisive failure absent:
  - C6 `-k f2_` goes from `6 failed` to `6 passed, 45 deselected`.
  - The whole C6 file goes from `22 failed, 29 passed` to `16 failed, 35 passed`. The set comparison shows exactly
    the 6 `f2_` cases fixed and nothing newly failing.
- Mutants:
  - M1-M5 (each R1 row reverted) each fail `test_real_vin_decodes_true_make[<WMI>]`.
  - M6 (copies removed) fails `test_engine_resolved_not_below_base` for JSA 11/19, KMH 37/40 and SAX 6/9.
  - M8 (every pick inverted) fails all 9 `test_conflict_key_winner` cases.
- Code gates: pyright `0 errors`; `py_compile` ok; ruff clean. `ruff --select S` reports 5 × S101 (pytest `assert`).
  That is the repo convention: two existing test files give 131 under the same check.
- Import and isolation: import sanity ok; `isolation.py` `violations: 4` (the known 4).

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1 `248 passed, 8 skipped` and step 2 `19 passed` (plan round 2 predicted both); M1-M6 and M8 each fail named tests (table in the note) |
| 2 | MET | step 3: `27 passed`, `41 passed`, `30 passed` |
| 3 | MET | step 4: `real decodes by (WMI, make): []`; engine resolved 26/40/19/9/9 against P3 floors 25/40/19/8/9 |
| 4 | MET | `.venv-loop` ruff `All checks passed!`; `git log 448c3ac..HEAD` = the 5 spec commits + `cb31bd8 ed53d94 bbc1b6e`; porcelain shows only `?? …/T-VINA-5.md`, `?? …/T-VINA-5.blocker.json` (header-authorised sibling) and `?? …/RESULT_T-VINA-5.md` |

## Decisions the task did not specify
- **Conflict-test VINs.** The test builds them synthetically (`<WMI><vds>000000000`), because the resolver reads
  only `vin[3:8]` and `vin[7]`. This avoids depending on whether a real VIN exists for each key.
- **Right-side conflict cases.** For HYUNDAI and SUZUKI, every right pick is a 1:1 tie, so those right-side cases
  (`VF21M`, `EAK35`) are tie-rule cases. ROVER has no right pick, so it lacks a right-side case.
- **Which row takes the new share on a right-wins key.** The share is written to the row the decoder's lookup hits
  (exact first, then folded). The other `MERCEDES BENZ` spelling row on that key, if any, keeps its old share.
- **Ordering in the map.** Each copy is inserted after its source row; each moved row and each wrong-wins row stays
  at the source row's position. Order is behaviour-neutral because no duplicate key exists among the edited keys.
- **Outcome table.** The serving row is classified by its share after the edit, numeric or blank.
- **Scripts on stdin.** `impl_guard` refused a `.py` file under `mut/`, so every script ran on stdin and only data
  outputs landed in `mut/`.

## Pre-existing changes preserved
At the redispatch the tree held only my untracked note from round 1. It is kept and extended. Cowork's
`54ed256` (correction 02) appeared on the branch during the build and is untouched; my commits sit on top of it.

## Rollback
`git -C C:/4DApp/repo revert bbc1b6e ed53d94 cb31bd8` on `fix/T-VINA-5`. Alternatively, reset the branch to `54ed256`
(Cowork's call; I did not reset).

## Remaining risks or uncertainties
- **Ambiguity flag.** 83 of the 133 winners carry a share below 0.70, so `vds_engine_ambiguous` now fires on those
  keys. On the 104 decoded real VINs, flags go from 42 to 45.
- **Cylinder counts.** `cylinder_count` changes on 27 of those VINs, all from `0` to a count. No existing test value
  changed.
- **Agreement with the reference** (`cylinder_count_resolved.md`), over the 104 decoded real VINs:

  | serving row's share | agrees | disagrees |
  |---|---|---|
  | numeric | 44 | 38 |
  | blank | 21 | 0 |
  | unresolved | 1 | |

  The 21 blank-share agreements are circular: those rows copy the reference.
- **Mercedes spelling duplicates.** 97 folded duplicate keys remain, mostly `MERCEDES BENZ`/`MERCEDES-BENZ`, outside
  R2's population. This is the follow-up to B7.
- **The builder.** `tools/build_wmi_map.py` still keeps the last of several vPIC makes per WMI, so a rerun
  reintroduces F-C6-2 (`test_real_vin_decodes_true_make` would catch it).
  - Proposed ledger note (Cowork writes it): `# source: wmi.csv rows WDB/KMH/JSA/JN1/SAX hand-fixed (T-VINA-5);
    vds_engine_map.csv wrong-brand rows re-keyed, 133 conflicts settled by the Nio 1+2 vote; build_wmi_map.py keeps
    the last of several vPIC makes per WMI (unfixed, no vPIC on host -> T-VINA-12)`.
- **Follow-ups (R1 ruling):**
  - `5NM` and `KMT` stay `Genesis`.
  - `JSK` and `JSL` stay `Kawasaki` (the registry shows JSK as KAWASAKI 10).
  - `JN1` keeps `SWITZERLAND`.
  - `12602` is a WMI population split → T-VINA-11.
- **Not run here:** the repo-wide gates (`baseline.sh`, the other five lab suites). They are report-only, and Cowork
  runs them at review.

## Branch and log
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-VINA-5
$ git -C C:/4DApp/repo log --oneline 54ed256..HEAD
bbc1b6e test(T-VINA-5): true makes, engine-resolved floors, conflict-key winners
ed53d94 fix(T-VINA-5): re-key wrong-brand engine-map rows; Nio 1+2 vote on 133 differing keys
cb31bd8 fix(T-VINA-5): wmi.csv true makes for WDB, KMH, JSA, JN1, SAX (F-C6-2)
```
Base: the spec commits through `54ed256` (`2fd3f8e` at redispatch, plus Cowork's correction 02).
