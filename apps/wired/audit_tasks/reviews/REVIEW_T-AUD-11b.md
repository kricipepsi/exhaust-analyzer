# REVIEW T-AUD-11b — ACCEPT, score 82 (Windows Cowork, 2026-11-05 21:38 CET)

Facts first: commit `bba7274` on `fix/T-AUD-11b` (after spec `61b1a50`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_dnalab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 11,
refs ok 21/21`, `REPORT OK` (exit 0). `git diff --name-only HEAD~1 HEAD`: the report only. Docs row: no second-model review.

## The missing note and RESULT (written here by Cowork)
The operator stopped the implementer at usage 95 % (20:58 CET) with `close --no-accept`, after the report commit and
before the note and the RESULT. No `progress_notes/T-AUD-11b.md`, no `RESULT_T-AUD-11b.md`, no `.blocker.json` exist.
Facts that replace them: branch `fix/T-AUD-11b`; `git log --oneline 3dfc3ea..fix/T-AUD-11b` = `61b1a50`, `bba7274`;
time from the spec commit (20:55:38) to the report commit (20:58:16) is 2 min 38 s (the run started at launch, so the
real wall-clock is longer; no `## Time` record exists: ABSENT).

## Findings re-derived (11)
- UPHELD (10):
  - README:8 "no cross-lab Python imports" vs `assembly.py:7,9` (imports symptomlab and vinlab).
  - PRD:86 (KR2) and PRD:127-128 (P0 pre-validation), DLD:107 (required-key check): four keys; `assembly.py:32` requires
    five, with `load_state` (T-DNA-7 made it required: HLD:157).
  - DLD:109 Part B passes four arguments; `assembly.py:42-46` passes five.
  - PRD:126 and HLD:52 `symptomlab.resolve(**triage)`; `assembly.py:41-47` passes five named keys, so any other key
    (`free_text_notes`) is dropped. HLD:83 and HLD:158 already say so: a doc-vs-doc conflict too.
  - HLD:106, LLD:74, DLD:70: `to_json_payload()` delegates to each model's `to_json()`; `models.py:74-75` calls
    `to_json_payload()`. Confirmed: `vinlab/models.py:251` and `symptomlab/models.py:74` `to_json()` return `str`, so the
    documented delegation would nest JSON strings.
- REJECTED (1, concern): README:3 "VIN decode" vs no decoder in `dnalab`. The README's title is "DNALab / VINLab v2"; its
  role line covers both labs, and the decode is delegated to `vinlab.decode` by design (HLD:51). Not drift.

## Population gap (Cowork's, not the implementer's)
P1 omitted `labs/dnalab/docs/ADR_DNALab.md` (it exists; `ls labs/dnalab/docs/`). No document in the report covers it.
The fix row checks it.

## Score
100 − 6 (one false finding) − 8 (no note, RESULT, readiness lines or `## Time`; operator stop, so not the full 15)
− 4 (three findings quote a line that names the topic, not the drifting value: PRD:128, DLD:107, assembly.py:32
"required = (") = 82.

## Follow-up
T-AUD-13 (DNALab docs drift fixes): the 10 upheld findings; one fix covers the four-key lists (PRD, DLD), one the
`**triage` wording (PRD, HLD), one the `to_json` delegation (HLD, LLD, DLD), one the README boundary line (name the
composition imports as the lab's purpose); and a drift check of `docs/ADR_DNALab.md`.

## Calibration for T-AUD-11c+
P1 comes from `ls <lab>/docs/` whole, not from a name pattern. A quote must hold the drifting value itself.
Measured: one lab (DNALab) → 11 findings, 10 upheld.
