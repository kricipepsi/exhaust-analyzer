# REVIEW T-AUD-11a — ACCEPT, score 88 (Windows Cowork, 2026-11-05)

Facts first: commit `ccf472d` on `fix/T-AUD-11a` changes only `audit/drift/2026-11-05_DRIFT_REPORT_symptomlab.md`;
Cowork re-run of `check_report.py`: `sections 8/8, findings 13, refs ok 24/24`, `REPORT OK`. Porcelain: note and RESULT only.
Docs row: no second-model review.

## Findings re-derived (13)
- UPHELD (11): PRD:30 signature lacks `free_text_notes`/`allowed_path` (`__init__.py:25-26`); PRD:98 and ADR-0002:15 "open
  vocabulary" vs `validator.py:36` hard cap `!= 21` (the HLD:190 text itself calls 21 an invariant: a doc-vs-doc conflict
  too); PRD:203 and HLD:190 "oil_consumption not in schema" vs the YAML's 7th tier_1 (HLD:113 already lists it);
  HLD:50 sole caller vs `composition.py:73,209,227`; LLD:104 and DLD:78 `to_json()` dict vs `models.py:44` `-> str`;
  DLD:92 / DLD:124 undocumented structural checks (`models.py:93`, `validator.py:67`).
- UPHELD with wrong wording (2, concern): DLD:174 and BDD:32 name `tests/test_models.py`, which does not exist (true);
  but "the tests live under tests/unit/" is false: `tests/unit/` holds only `test_drift_guard.py`. The named test files
  exist nowhere.
- REJECTED (1, blocker-class for that finding): PRD:149 "Python 3.14" vs `pyproject.toml:8` `>=3.11` is not drift: 3.14
  satisfies `>=3.11` (Render pins 3.14.3). Its code quote `"requires-python"` also omits the value.

## Score
100 − 6 (one false finding) − 4 (wrong wording ×2) − 2 (weak quote) = 88.

## Follow-up
The 11 upheld findings + the missing-tests fact become one row, T-AUD-12 (SymptomLab docs drift fixes). The 21-pair cap
needs a ruling (keep the cap and correct the ADR/PRD wording, or derive it from the YAML); T-AUD-12 decides it.

## Calibration for T-AUD-11b+
Add to R1: "a version range the documented value satisfies is not drift"; "an ABSENT claim states only what the command
shows". Measured: one lab of 45.7 KB → 13 findings in one run.
