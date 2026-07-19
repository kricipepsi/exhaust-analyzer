# T-OBDV2-FIX-4 — Align the `number_of_banks` default across the pipeline

## Plan
We will align the default value of the `number_of_banks` field to `1` across all components of the OBDLab pipeline. This changes the fallback value from `2` to `1` at the two validation sites in `obdlab.core.pid_ingestion_validator` (namely `_validate_bounds` and `_enforce_bank2_contract`). This aligns them with `TrimVectorAggregator` and `SensorSignalTranslator` which already default to `1`.

We will also:
1. Add unit tests to `tests/unit/test_pid_ingestion_validator.py` verifying that when `number_of_banks` is omitted, it defaults to 1, passing when bank 2 fields are null and raising a contract violation when bank 2 fields are non-null.
2. Add a new regression fixture `tests/regression/fixtures/case_07_omitted_bank_default.json` omitting `number_of_banks` to verify the end-to-end integration pipeline handles omitted-bank inputs properly as a 1-bank engine.

## VERIFICATION GATE
- [x] `ruff check obdlab/ && npx pyright obdlab/` clean
- [x] `pytest -x -q` green
- [x] Default `2` removed from `number_of_banks` in `pid_ingestion_validator.py` (verified via `grep`)
- [x] Verification suite passes and all 385 tests run clean

## CODE REVIEW
- [x] Verified that omitting `number_of_banks` defaults to a single-bank engine, producing `shrtft2` and `longft2` as `None` (no bank-2 validation applied, no bank-2 contract raise).
- [x] Confirmed the aggregator and assembly already default to 1 bank, ensuring end-to-end pipeline consistency.
