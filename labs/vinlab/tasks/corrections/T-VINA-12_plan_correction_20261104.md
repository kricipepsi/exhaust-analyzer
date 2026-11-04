# T-VINA-12 — plan correction 01 (Windows Cowork, 2026-11-04)

Plan: `repo/labs/vinlab/tasks/progress_notes/T-VINA-12.md` § `## Plan`. Verdict: **APPROVED with corrections C1-C6**,
written into `repo/labs/vinlab/tasks/T-VINA-12_wmi_make_by_registry(4).md` (§ Routing, R2, R3, R4, R5). The task file
is the spec; this file is the approval record. No hand-back.

## Accepted from the plan
R1 as planned (10 brand cells, `LSJ,MG,CHINA,modern`). R2's rule (`plan/rekey.py`): K from files 1+2, copy, same, and
the files 1+2 vote with the existing row winning a tie; old-brand rows never edited. R3's design
(`_pick_vpic_make`, `_registry_majority`, the `--registry-csv` flag). R4's 8 new cases and mutants M1-M6. A1 and A3.

## Re-derived by Cowork
- `join_check.py` on `plan/data`: W `n 1667 eng 1126 match 1004 err 105`; C equal to the base line for line.
- New control set N (the other WMIs whose base brand is TOYOTA, KIA, JEEP, CHRYSLER, NISSAN, RENAULT or MG), base and
  plan: `n 50439 eng 44941 match 40056 err 3225`, equal line for line.

## Rulings on the plan's open points and the second review (`C:/4DApp/recheck/codex/T-VINA-12_plan_review.md`)
- **A2, the `1C4` loss (2 matches): accepted.** R2's totals bind, not a per-WMI floor. Lost: a per-WMI floor. The two
  VINs are Chrysler Voyagers under a WMI the registry gives to Jeep (share 0.833); the only files-1+2 recovery copies
  every old row and pollutes the new brands' keys.
- **Biased vote (HIGH): not upheld.** One row serves every VIN on a key, so the vote over all VINs that reach the key
  is the objective (T-VINA-5 R2). N confirms that it costs the new brands' own WMIs nothing.
- **Tie rule (MEDIUM): not upheld.** The existing row wins a tie, as in T-VINA-5. No evidence favours either side.
- **Stale share on the 59 copies (LOW): not upheld.** It changes only the `vds_engine_ambiguous` flag, never a match.
- **Encoding (LOW): upheld → C1.** The registry is cp1250. Under latin-1, `Š` reads as U+008A, so a `ŠKODA` majority
  can never fold to vPIC's `Skoda`.
- **Over-deletion via the folded key (MEDIUM, latent): upheld → C3.**
- **`build()` chain untested, empty makes (MEDIUM, LOW): upheld → C4.**
- **Six renames without a test (MEDIUM-LOW): upheld → C5.**
- **Path B (LOW-MEDIUM): upheld → C6.**
- **New, Cowork: control set N → C2.**

## Corrections
- **C1** `rekey.py` and `_registry_majority` read the registry as cp1250. The `_registry_majority` test has one row
  whose brand holds a cp1250 byte (`ŠKODA` written as cp1250 bytes) and expects `ŠKODA`.
- **C2** R2's floors gain N: `match` ≥ 40056 and `eng` ≥ 44941. `join_check.py` (Cowork, updated) prints `TOTAL N`.
- **C3** `rekey.py` asserts that each old-wins delete removes exactly one row (the deleted-row count equals the number of
  old-wins keys that had an existing row).
- **C4** A test calls `build(...)` with an in-memory vPIC file, a petrol CSV and `registry_make`, and asserts the brand
  in the written `wmi.csv`. `_pick_vpic_make([], ...)` returns `""`, with a test.
- **C5** One VIN per WMI for `5TD`, `ZAC`, `1C4`, `3C4`, `1C3`, `3N1`, `LSJ`, taken from registry files 1+2 (petrol),
  that decodes without an exception: `test_real_vin_decodes_true_make` asserts the P1 make (comment `# registry file
  N`). A WMI with no such VIN is listed in the note. Mutant M7: the `1C3` brand cell reverted → its case fails.
- **C6** One command on files 1+2 shows how many W VINs resolve through Path B (`pos_8_only`) on the base and on the
  plan data. Record both counts.
