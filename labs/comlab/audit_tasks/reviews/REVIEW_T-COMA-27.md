# REVIEW T-COMA-27 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-27` on `fix/T-COMA-26` `d8495f9`: spec `780e1a7`; build `7fd2cce` (10 REG-V2 rules, one
new test, four registry pins). Changed lines identical to `C:/4DApp/recheck/T-COMA-27/rehearsal.patch`. Porcelain: the
note and the RESULT only. Cowork re-ran comlab `563 passed`, wired `186`, ui `75`, registry `508 passed, 5 skipped`,
reweight + new test `23 passed`, probe `unrouted chemical states: 2` (`3 failed, 10 passed, 3 deselected`, R3),
corpus `changed 0 of 314` (family accuracy 216 of 314, equal), ruff clean.

## Hand-back finding
- SOFT (implementer): `rehearse.py` refuses any untracked file, but the header puts the note on disk before the first
  edit. The implementer parked the note in the runtime dir, ran the script and restored it. **Upheld as a spec
  defect** (Cowork's): a rehearsal script must ignore the task's own note and RESULT paths.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-COMA-27_review.md`).
- M1 (rehearsal output not in the gate): **not upheld.** The note's `Assumptions worked past` records
  `applied 10 files`, exit 0; the prompt embedded only the gate block.
- M2 (branch and final porcelain not shown): **not upheld.** Cowork's own run: branch `fix/T-COMA-27`,
  `d8495f9..HEAD` = `7fd2cce`, `780e1a7`; porcelain = note + RESULT.
- L1 (the `UNIT-COMA27-` skip is a prefix, not exact IDs), L3 (docstring wider than the ten states), L4 (base weight
  and GATING tier not pinned by the test): **upheld**, folded into T-COMA-28, which edits the same tests.
- L2 (the sinks can still reach 1.0 with more evidence): **upheld as the recorded residual**; T-COMA-28 gates LC-002
  and MF-005 on their chemistry.
- L5 (no corpus case shows RM-005 winning): **not a defect.** The four EVAP cases keep RM-001, in the same family.

## Score
97: the spec defect above (Cowork's) and three upheld Low test gaps.
