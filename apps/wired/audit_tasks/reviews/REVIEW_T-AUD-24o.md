# REVIEW T-AUD-24o — no-start rpm and cold ECT gates (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 98.** Code row (rule data and test pins). Hydrogen lane (medium), 3.6 min (lane `.exit`
13:18:28-13:22:05 CET). The second review came from a second model, `second_review.py` (ds-flash): APPROVE, 2 Low
(`C:/4DApp/recheck/codex/T-AUD-24o_review.md`).

## Facts (Cowork re-ran, branch `fix/T-AUD-24o`, after promote)
- Commits after `fix/T-AUD-24p`: `2e91f16` spec, `09d6345` lane work, `3ca7190` merge. Name-status: M the two rule
  files and two test files, A note and RESULT. No D, no R. The code edits equal `recheck/T-AUD-24o/rehearsal.diff`.
- comlab 614 passed; registry 510 passed, 5 skipped; apps/wired 1 failed (T-COMA-10), 237 passed; step 4
  `24o OK [('lt', 400), ('gt', 400), ('lt', 10.0)]`; the v7 corpus output is byte-identical to
  `recheck/T-AUD-24k/promoted.json`. `git status --porcelain` empty.

## Findings
- **L1, L2 (second review, Low):** the unit tests pin the new values on NS-001, NS-003, NS-005 and MW-005 but not
  NS-002/NS-004 rpm, and they check presence, not absence. Both were covered at review time: step 4 collects every
  NS rpm gate into one set, so any 600 left behind would print `24o FAIL`. The permanent tests stay presence checks,
  which is a nit. Upheld as a nit, no correction. Score −2.
