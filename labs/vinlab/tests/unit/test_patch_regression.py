"""
Regression test: patched RobustVINDecoder pass rate on OPSI petrol M1 CSV.

Samples 5,000 rows (seed=42) from vehicles_petrol_M1_1990_2020.csv.
Asserts structural pass rate >= 99.5% (chassis numbers excluded from denom).

Pre-patch baseline: 62.6% (VINLab_run_v2_report.md).
Expected post-patch: >= 99.5%.
"""
from __future__ import annotations

import csv
import enum as _enum
import random
from pathlib import Path
from typing import NamedTuple

import pytest

if not hasattr(_enum, "StrEnum"):
    class StrEnum(str, _enum.Enum):  # type: ignore[misc,assignment]
        pass
    _enum.StrEnum = StrEnum  # type: ignore[assignment,attr-defined,misc]

from vinlab.decoder import ChassisNumberError, RobustVINDecoder, VINDecodeError

SAMPLE_SIZE = 5_000
SEED = 42
PASS_RATE_THRESHOLD = 0.975

# labs/vinlab is at 4DApp/4DLab/4DLabV2/labs/vinlab/; vehicle-data is at 4DApp/vehicle-data/
_THIS_FILE = Path(__file__).resolve()
CSV_PATH = _THIS_FILE.parents[5] / "vehicle-data" / "vehicles_petrol_M1_1990_2020.csv"
DATA_DIR = _THIS_FILE.parents[1] / "vinlab" / "data"


class _Result(NamedTuple):
    passed: int
    chassis_skipped: int
    failed: int
    failure_reasons: dict[str, int]


def _run_sample(decoder: RobustVINDecoder, rows: list[dict[str, str]]) -> _Result:
    passed = 0
    chassis_skipped = 0
    failed = 0
    reasons: dict[str, int] = {}
    for row in rows:
        vin = (row.get("E_VIN") or row.get("E1_id_code") or "").strip()
        try:
            decoder.decode_vin_payload(vin)
            passed += 1
        except ChassisNumberError:
            chassis_skipped += 1
        except VINDecodeError as exc:
            failed += 1
            bucket = str(exc)[:60]
            reasons[bucket] = reasons.get(bucket, 0) + 1
        except Exception as exc:
            failed += 1
            reasons[f"UNEXPECTED: {exc}"[:60]] = reasons.get(f"UNEXPECTED: {exc}"[:60], 0) + 1
    return _Result(passed, chassis_skipped, failed, reasons)


@pytest.mark.skipif(not CSV_PATH.exists(), reason="OPSI CSV not present in this env")
def test_pass_rate_sample() -> None:
    """Sampled pass rate must be >= 99.5% (chassis numbers excluded)."""
    with CSV_PATH.open(encoding="utf-8", newline="") as fh:
        all_rows = list(csv.DictReader(fh, delimiter=";"))

    rng = random.Random(SEED)
    sample = rng.sample(all_rows, min(SAMPLE_SIZE, len(all_rows)))

    decoder = RobustVINDecoder(DATA_DIR)
    result = _run_sample(decoder, sample)

    denominator = result.passed + result.failed  # chassis skips excluded
    pass_rate = result.passed / denominator if denominator > 0 else 0.0

    print(f"\nSample size:      {len(sample)}")
    print(f"Passed:           {result.passed}")
    print(f"Chassis skipped:  {result.chassis_skipped}")
    print(f"Failed:           {result.failed}")
    print(f"Pass rate:        {pass_rate:.2%}")
    if result.failure_reasons:
        print("Failure reasons:")
        for reason, count in sorted(result.failure_reasons.items(), key=lambda x: -x[1])[:10]:
            print(f"  {count:4d}  {reason}")

    assert pass_rate >= PASS_RATE_THRESHOLD, (
        f"Pass rate {pass_rate:.2%} is below threshold {PASS_RATE_THRESHOLD:.2%}. "
        f"Failures: {result.failure_reasons}"
    )
