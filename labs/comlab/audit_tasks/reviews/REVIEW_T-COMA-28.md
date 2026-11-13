# REVIEW T-COMA-28 — ACCEPT, score 96 (Windows Cowork, 2026-11-13)

Facts first: `fix/T-COMA-28` on `fix/T-COMA-27` `3cd8541`: spec `a80b5f2`; build `9a32ea6` (LC-002 and MF-005 chemistry
GATING with base +0.10; T-COMA-27 Lows; four re-stated pins; new test). Changed lines identical to
`C:/4DApp/recheck/T-COMA-28/rehearsal.patch`. Porcelain: the note, the RESULT and the header-authorised
`T-COMA-28.blocker.json`. Cowork re-ran comlab `569 passed`, wired `186`, ui `75`, registry `508 passed, 5 skipped`,
targeted `29 passed`, probe `LC-002 score: None MF-005 score: None` (`1 failed, 13 passed, 2 deselected`: the
every-state check), corpus `changed 32 of 314`, family accuracy `221 of 314 (before 216)`, `gained 9 lost 4`.

## Hand-back
- B10 (soft, STALE-ANCHOR): R4 said 8 cases; Cowork's staged test collects 6, and P2 agrees with 6. **Upheld as a spec
  defect** (Cowork's). `BLOCKER_LOG.md` B10; `blocker_corpus.jsonl`.

## Second review
APPROVE WITH CORRECTIONS (`C:/4DApp/recheck/codex/T-COMA-28_review.md`).
- M1 (porcelain lists `blocker.json`): **not upheld.** The header authorises that file; criterion 2's wording should
  have named it (Cowork's wording slip, scored below).
- M2 (score preservation not pinned: the firing tests assert only `is not None`): **upheld.** T-COMA-29 pins 0.96 and
  0.90.
- L1 (docstring does not list the ten states): **not upheld.** It identifies the set exactly; `ROUTED` lists it.
- L2 (no cross-chemistry case): **upheld.** T-COMA-29 adds LC-002 on IGNITION_MISFIRE and MF-005 on LEAN_MIXTURE.
- L3 (the probe's failure is unexplained): **not upheld.** Verification step 3 names it (the every-state check); the
  prompt did not embed that section.

## Score
96: two Cowork spec slips (the R4 count, the criterion 2 wording) and two upheld test gaps.
