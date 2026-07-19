# T-OBDV2-ARCH-2 — Proposal-or-prune the orphan vocab/schema members

## Plan
We will prune the orphan vocab and schema members per the owner/architect ruling:
1. **VERoutingMode**: Prune `VERoutingMode` from `schemas/vocabulary.py` and its reference in `AirMeteringStrategy`'s docstring in `schemas/dna_view.py`. Remove `VERoutingMode` and its case from `tests/unit/test_vocabulary.py`.
2. **cylinder_count**: Prune the `cylinder_count` field from the `ObdLabDnaView` model in `schemas/dna_view.py`. Clean up all references to `cylinder_count` from python test files:
   - `tests/unit/test_dna_view.py`
   - `tests/unit/test_ecu_perception_delta.py`
   - `tests/unit/test_maf_linearity.py`
   - `tests/unit/test_o2_normalizer.py`
   - `tests/unit/test_pid_ingestion_validator.py`
   - `tests/unit/test_semantic_consistency_checker.py`
   - `tests/unit/test_sensor_signal_translator.py`
   - `tests/unit/test_ve_engine.py`
   - `tests/integration/test_pipeline_smoke.py`
3. **Inactive O2FailureMode members**: Prune `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, and `HEATER_FAULT` from the `O2FailureMode` enum in `schemas/vocabulary.py` and from the expected values list in `tests/unit/test_vocabulary.py`.

## VERIFICATION GATE
- [x] `ruff check obdlab/ && pyright obdlab/` clean
- [x] `pytest -x -q` green (384 passed, 6 skipped)
- [x] Grep/Select-String confirms zero occurrences of `VERoutingMode`, `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, or `HEATER_FAULT` in the codebase's python files.
- [x] Grep/Select-String confirms zero occurrences of `cylinder_count` in the codebase's python files.

## CODE REVIEW
- [x] `VERoutingMode` removed entirely from `vocabulary.py` and test suites.
- [x] `cylinder_count` removed entirely from `dna_view.py` model and all test setups.
- [x] Unused `O2FailureMode` members (`SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`) removed from the enum and the vocabulary drift test.
