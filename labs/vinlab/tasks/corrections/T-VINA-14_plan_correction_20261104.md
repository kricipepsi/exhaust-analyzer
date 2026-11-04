# T-VINA-14 — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-14.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C2**,
written into `repo/labs/vinlab/tasks/T-VINA-14_decoder_banks_induction_remerge(4).md` (§ Routing, R4). The task file is
the spec; this file is the approval record. No hand-back.

## Accepted from the plan
R1 as written (`csv_config.startswith("BOXER")` in the row branch); R2 with a keyword-only `induction_stated` read
from the applied `db_dict` (assumption 1: the window check runs first); `_coalesce` computed once in `select_rows`;
G1 narrowed to a blank `is_v_engine` with a V/W map; G2 (ii) and the `NATURALLY_ASPIRATED` constant deleted; the 7
decoder tests and the merge test changes; assumptions 2-5; the R5 list of 7 VINs; the predicted step 4 and step 5
lines.

## Re-derived by Cowork
- Test 2's fixture is real: shipped `XFX` has `is_v_engine 1` (CITROEN, 2000-2020), so setting it to `0` gives a
  base value of 1 bank. `B5254S` and `EJ25` have `is_v_engine 0`; the shipped db has no `AZQ`, `RGX` or `RFJ` row.
- All 17 map rows whose `engine_configuration` starts `BOXER` are SUBARU.
- The only readers of the tool's `NATURALLY_ASPIRATED` constant are in G2 (ii) (`merge_tecdoc_extract.py:201,211`).
- Counts: 35 coalesced − 2 newly `no_my_start` = 33, + G2 5 + G1 2 = 40; 1,186 + 9 + 37 + 34 + 40 = 1,306.

## Second review (`C:/4DApp/recheck/codex/T-VINA-14_plan_review.md`, codex after the DeepSeek route exited 1, embedded): APPROVE WITH CORRECTIONS
- **F1** (no mutant row for restoring G2 (ii) in the tool, MEDIUM): **upheld.** The decoder tests the table names
  cannot see a tool-only mutation. → **C1**: add the mutant "restore `stated_na` and the G2 (ii) clause in the tool",
  killed by `test_stated_na_heuristic_code_is_inserted`.
- **F2** (coalesce rejections tested only on a two-value displacement, MEDIUM): **upheld.** The plan's rule already
  rejects both cases; the gap is the tests. → **C2**: two `PIN` tests in `test_vref_tecdoc_merge.py`:
  `test_three_cc_values_stay_collision` (1597/1598/1599 under three brands) and
  `test_non_displacement_conflict_stays_collision` (one brand `NATURALLY_ASPIRATED`, the other `TURBOCHARGED`,
  everything else equal). Mutants: "accept adjacent 1 cc steps" (killed by the first) and "coalesce any field by
  first brand" (killed by the second). The plan's suggestion to parametrise over every field is not required.

## Counts after C1-C2
Merge file 23 → **25** tests; step 2 **32 passed**; step 1 **293 passed, 8 skipped**; the red run **8 failed, 24 passed**
(both new tests are green on the base: each group is a `collision` there).

## Concern carried to the RESULT (no change to the build)
The two RGX VINs (`VF3221RA212038997`, `VF7U6UA0012529661`) turn TURBOCHARGED from TecDoc's RGX row, but their map
keys pick RGX with a weak majority (`PEUGEOT,221RA` 0.400; `CITROEN,U6UA0` 0.833). The RESULT names that share beside
the change. The map key is T-VINA-11's.
