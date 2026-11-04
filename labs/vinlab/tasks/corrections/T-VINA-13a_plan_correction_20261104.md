# T-VINA-13a — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-13a.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C6**,
written into the task file `repo/labs/vinlab/tasks/T-VINA-13a_tecdoc_1q2019_extract(4).md` (§ Rulings that bind, R3-R5).
The task file is the spec; this file is the approval record.

## Re-derived by Cowork (snapshot `C:/4DApp/recheck/rea_1q2019/tecdoc_1q2019_engines.sqlite`)
- `C:/4DApp/recheck/scratch/vina13_alias.py`, the plan's tiers and alias table: T0 1,138 (petrol 1,119), T1 274
  (268), T0A 118 (116), rows **1,503**. All equal to the plan.
- `C:/4DApp/recheck/scratch/vina13_t1check.py`: T1 pairs by key kind: head + whole-X 152, head only 39, paren 76,
  whole-X only 7. Seven T1 codes are all digits: `ZASTAVA 100` → `100 GL. 0.64`, `SKODA 136` → `136 L`,
  `FIAT 6132` → `6132 AZ 2.000`, `PEUGEOT 106` → `106 (XN1)`, `PEUGEOT 118` → `118 (XL5)` (head or whole-X keys, model
  names), and `BMW 54121`, `BMW 56121` (paren keys, true type numbers).

## Second review (`C:/4DApp/recheck/codex/T-VINA-13a_plan_review.md`, ds-pro, embedded): APPROVE WITH CORRECTIONS
- **F1** (whole-X key is outside R3, MEDIUM): **not upheld as a plan defect.** My P3 measurement already used the
  whole-X key, and R3's wording omitted it: my defect. R3 now names it.
- **F2** (numeric head tokens, MEDIUM): **upheld** (Cowork found it too) → **C1**: a head-token or whole-X key that is
  all digits is not emitted. Paren keys stay. A length floor is rejected: PSA codes are 3 letters (`NFX`, `KFW`).
- **F3** (`GENESIS`→`HYUNDAI` is not a same-company alias, MEDIUM): **not upheld.** Genesis is a brand of Hyundai Motor
  Company, not a separate company like Kia. The map's GENESIS rows are WMIs `5NM`/`KMT`, which the vPIC last-make
  defect gave to Genesis (T-VINA-12). The alias stays.
- **F4** (family head-token pools are written `OK`, LOW): **upheld** → **C2**: `status` `FAMILY` when the kept ids
  carry more than one distinct normalised `Description` and every field agrees. `AMBIGUOUS` (a field disagrees) wins
  over `FAMILY`.
- **F5** (twincharger written `TURBOCHARGED`, LOW/MEDIUM): **upheld** → **C3**: `Turbocharger/Compressor` leaves
  `induction_type` blank and sets `has_turbo` `1`; the RESULT gives its count.
- **F6** (the determinism mutant survives, MEDIUM): **upheld** → **C4**: test 9 reverses the fixture map's rows and
  asserts the expected first and last output rows.
- **F7** (the open-end mutant may survive, MEDIUM): **upheld** → **C5**: test 7's fixture links one engine to one open
  and one closed car and asserts `my_end` blank.
- **Petrol order** (checked, not a defect): → **C6**: test 11 pins option (a). A diesel T0 hit plus a petrol T1 hit on
  one pair gives no row and counts as non-petrol.
- **F8** (alias counts contradict P4, HIGH): **not upheld.** P4 groups the misses by the full manufacturer set, so
  `VW` appears in several groups (`VW` 36, `SEAT`+`VW` 14, `AUDI`+`VW` 7, …). The plan's 118 is re-derived above.

## Next
Add `## Plan round 2` to the note: each change C1-C6, the new tier, status and no-row counts, the new real-VIN
prediction, and tests 1-11. Then build without a second stop. One return at most.
