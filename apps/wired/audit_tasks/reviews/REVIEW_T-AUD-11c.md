# REVIEW T-AUD-11c — ACCEPT, score 94 (Windows Cowork, 2026-11-05 21:47 CET)

Facts first: commit `6f0ffc9` on `fix/T-AUD-11c` (after spec `3e20cf3` and index `fcc2516`) changes only
`audit/drift/2026-11-05_DRIFT_REPORT_vinlab.md`. Cowork re-run of `check_report.py`: `sections 8/8, findings 20,
refs ok 38/38`, `REPORT OK` (exit 0). Porcelain: note and RESULT only. Headless run 20:41:20-20:46:16 UTC, exit 0;
note `## Time` 4 min. Docs row: no second-model review.

## Findings re-derived (20)
- UPHELD (19):
  - PRD:108 (KR6 citation rule) and LLD:146 (`# source: OBD-II mandate`) vs `decoder.py:388` `model_year >= 1996`, no comment.
  - HLD:135 "positions 12–13" vs `decoder.py:850` `vin[11:14]` (positions 12-14; the HLD's own next line and the
    `decoder.py:845` docstring repeat the error).
  - HLD:99 "engine None → NONE" vs `decoder.py:614`: with `wmi_brand_missing` the flag `engine_not_in_csv` is skipped,
    and `_compute_confidence` (`decoder.py:536-539`) grades NONE only on `engine_not_in_csv`, so the grade is PARTIAL.
  - HLD:50 "COMLab projector" as a caller: no `.py` under `labs/comlab` imports `vinlab` (`grep -rn --include=*.py -E
    "^\s*(import vinlab|from vinlab)" labs/comlab` prints nothing).
  - UNDOCUMENTED, each line confirmed: type-code WMI year return (`decoder.py:878`; HLD:140, LLD:120); VDS ambiguity
    below 0.70 (`:816`; HLD:151, VOCAB:126); year-window discard (`:610`; HLD:98); `euro_unknown` (`:690`; HLD:104);
    O2 year default 2000 (`:384`; LLD:196); four VDS indexes (`:222`; DLD:188); missing flags (DLD:271); `vref_db1.db`
    (DLD:65); normalised engine-code retry (`tecdoc_query.py:75`; DLD:258).
  - LLD:145 banks vs `decoder.py:374` BOXER; DLD:208 `has_maf` vs the 0/0 rule at `decoder.py:506-510`; DLD:130
    `from_json()` as the inverse of `to_json()` (a `str`) vs `models.py:256` taking a dict.
- REJECTED (1, concern): README:8 `mysql_data/` "copied verbatim". `.gitignore:41` ignores `**/mysql_data/`, so
  `git ls-files` = 0 proves nothing, and the folder's absence is a fact of this host, not drift between the docs and
  the code.

## Other observations
- The note records that `bash_guard` refused a commit whose message held the attribution line, so `6f0ffc9` has no
  trailer. Not reproduced: Cowork's commits with the trailer pass (`972f3eb`, `3e20cf3`). Watch on the next row; no row
  yet (hypothesis).
- The note's `Assumptions worked past` holds 7 well-argued exclusions (R4), including `open_vref_readonly` with no caller.

## Score
100 − 6 (one false finding, with an ABSENT command that cannot show its claim) = 94.

## Follow-up
T-AUD-14 (VINLab docs drift fixes): the 19 upheld findings, grouped as: citation comments (PRD, LLD), the 12-14 wording
(HLD, docstring), the PARTIAL grade with `wmi_brand_missing` (HLD; or a code ruling), caller list (HLD), the confidence
flag lists (DLD, VOCAB), the pipeline steps the HLD/LLD/DLD omit, `from_json` wording (DLD).

Measured: VINLab (78 KB docs, 1,918 code lines) → 20 findings in 4 min on Sonnet medium.
