# T-OBDV2-FIX-7 — Code-hygiene bundle

## Plan
We will apply a bundle of low-priority code hygiene refactors:
1. **P-2 (restore exception chaining)**: Update `core/pid_ingestion_validator.py` to capture Value/Type errors `as exc` and raise `PIDValidationError(...) from exc` at the four integer/float conversion check sites (lines 83, 90, 131, 139).
2. **P-3 (single-source duplicated thresholds)**: Make `ECT_WARM_THRESHOLD = 70` and `WOT_THROTTLE_THRESHOLD = 90` public constants in `core/analytics_preconditions.py`, and remove their duplicate definitions from `core/o2_normalizer.py` by importing them from `analytics_preconditions.py`.
3. **P-4 (drop the dead total_trim param)**: Remove the unused `total_trim` parameter from `O2Normalizer.normalize` signature and docstring.
4. **P-5 (defer import-time YAML I/O)**: Defer loading of `obd_translation_rules.yaml` in `core/state_bucketing.py` by wrapping the load logic in `_load_rules()` and calling it on-demand from `compute_bucket()`.
5. **ARCH-3 (fix doc-vs-code drift)**: Align the `FAULT_VE_SENSOR_SKEW` docstring comment in `schemas/vocabulary.py` to match the correct 90% threshold defined in the code and the wiki.

## VERIFICATION GATE
- [x] `ruff check obdlab/ && pyright obdlab/` clean
- [x] `pytest -x -q` green (384 passed, 6 skipped)
- [x] Grep/Select-String confirms `ECT_WARM_THRESHOLD =` and `WOT_THROTTLE_THRESHOLD =` defined exactly once in `core/analytics_preconditions.py`.
- [x] Grep/Select-String confirms `total_trim` is completely gone from `o2_normalizer.py`.

## CODE REVIEW
- [x] Exception chaining properly set up in `pid_ingestion_validator.py` using `from exc`.
- [x] Duplicated thresholds hoisted and single-sourced.
- [x] Dead `total_trim` parameter removed.
- [x] Import-time file I/O eliminated in `state_bucketing.py`.
- [x] Vocabulary docstring updated to reflect 90% threshold for VE sensor skew.
