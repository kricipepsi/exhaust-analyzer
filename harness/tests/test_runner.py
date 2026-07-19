"""Tests for harness.runner — generic suite runner and parity gate."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import FieldRange, ModuleDescriptor
from harness.runner import run_suite

try:
    from harness.descriptor import build_gaslab_descriptor
    _HAS_GASLAB = True
except ImportError:
    _HAS_GASLAB = False
    build_gaslab_descriptor = None  # type: ignore[assignment]


# --- Generic runner tests (no gaslab needed) ---


def _make_stub_descriptor():
    """A minimal ModuleDescriptor for testing the runner loop."""
    return ModuleDescriptor(
        name="stub",
        fields=[FieldRange("x", "float", 0, 10)],
        boxes={},
        build_args=lambda row: (float(row["x"]),),
        entry_point=lambda x: type("Result", (), {"value": int(x * 2)})(),
        extract_expected=lambda row: {
            "result": int(row.get("expected_result", "") or "0"),
            "error": row.get("expected_error", ""),
        },
        diff=lambda actual, expected: (
            [] if actual.value == expected["result"]
            else [f"expected={expected['result']}, actual={actual.value}"]
        ),
    )


def test_runner_all_pass(tmp_path):
    desc = _make_stub_descriptor()
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "case_id,description,x,expected_result,gt_method,gt_source,notes\n"
        "S-001,double 2,2,4,spec,stub,\n"
        "S-002,double 5,5,10,spec,stub,\n",
        encoding="utf-8",
    )
    passes, failures, states, results = run_suite(desc, csv_path)
    assert passes == 2
    assert failures == 0
    assert len(results) == 2
    assert all(r["verdict"] == "PASS" for r in results)


def test_runner_mismatch_detected(tmp_path):
    desc = _make_stub_descriptor()
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "case_id,description,x,expected_result,gt_method,gt_source,notes\n"
        "S-001,double 2,2,99,spec,stub,\n",
        encoding="utf-8",
    )
    passes, failures, states, results = run_suite(desc, csv_path)
    assert passes == 0
    assert failures == 1
    assert results[0]["verdict"] == "FAIL"


def test_runner_valueerror_expected(tmp_path):
    """A row whose build_args raises ValueError matches expected_error=ValueError."""
    def _raise(_row):
        raise ValueError("out of range")

    desc = ModuleDescriptor(
        name="stub",
        fields=[],
        boxes={},
        build_args=_raise,
        entry_point=lambda: None,
        extract_expected=lambda row: {"error": row.get("expected_error", "")},
        diff=lambda a, e: [],
    )
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "case_id,description,expected_error,gt_method,gt_source,notes\n"
        "S-001,invalid,ValueError,spec,stub,\n",
        encoding="utf-8",
    )
    passes, failures, states, results = run_suite(desc, csv_path)
    assert passes == 1
    assert failures == 0


def test_runner_valueerror_unexpected(tmp_path):
    """ValueError when expected_error is blank -> FAIL."""
    def _raise(_row):
        raise ValueError("out of range")

    desc = ModuleDescriptor(
        name="stub",
        fields=[],
        boxes={},
        build_args=_raise,
        entry_point=lambda: None,
        extract_expected=lambda row: {"error": ""},
        diff=lambda a, e: [],
    )
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "case_id,description,expected_error,gt_method,gt_source,notes\n"
        "S-001,invalid,,spec,stub,\n",
        encoding="utf-8",
    )
    passes, failures, states, results = run_suite(desc, csv_path)
    assert passes == 0
    assert failures == 1


def test_runner_expected_error_not_raised(tmp_path):
    """Expected an error but build_args succeeded -> FAIL."""
    desc = _make_stub_descriptor()
    csv_path = tmp_path / "test.csv"
    csv_path.write_text(
        "case_id,description,x,expected_result,expected_error,gt_method,gt_source,notes\n"
        "S-001,should error,2,,ValueError,spec,stub,\n",
        encoding="utf-8",
    )
    passes, failures, states, results = run_suite(desc, csv_path)
    assert passes == 0
    assert failures == 1


# --- Parity gate (requires gaslab) ---


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_parity_replays_existing_csv():
    """Parity gate: driving the existing GASLab CSV through the descriptor + runner
    reproduces the current runner's verdicts with 0 mismatches."""
    if build_gaslab_descriptor is None:
        pytest.skip("gaslab not importable")
    desc = build_gaslab_descriptor()

    csv_path = Path(__file__).resolve().parent.parent.parent / "gaslab_suite_with_dna.csv"
    if not csv_path.is_file():
        pytest.skip(f"CSV not found: {csv_path}")

    passes, failures, actual_states, results = run_suite(desc, csv_path)
    total = passes + failures

    assert failures == 0, (
        f"Parity gate FAILED: {failures}/{total} mismatches.\n"
        + "\n".join(
            f"  {r['case_id']}: {r['detail']}"
            for r in results if r["verdict"] == "FAIL"
        )
    )
    assert passes == total, f"Expected {total} PASS, got {passes}"
