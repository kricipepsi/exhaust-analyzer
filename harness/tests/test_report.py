"""Tests for harness.report — .md report emitter."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from harness.report import write_report


def test_report_is_markdown(tmp_path):
    """The emitter writes a valid .md file with a header row count matching cases run."""
    results = [
        {"case_id": "GAS-001", "verdict": "PASS", "detail": "NORMAL_OPERATION", "duration_ms": 1.5},
        {"case_id": "GAS-002", "verdict": "PASS", "detail": "RICH_MIXTURE", "duration_ms": 2.0},
        {"case_id": "GAS-003", "verdict": "FAIL", "detail": "chemical_state: expected=X, actual=Y", "duration_ms": 3.0},
    ]
    output_path = tmp_path / "report.md"
    write_report(results, output_path, title="Test Report", source_csv="test.csv")

    assert output_path.is_file()
    content = output_path.read_text(encoding="utf-8")

    # Must not write .docx or .pdf
    assert not output_path.suffix == ".docx"
    assert not output_path.suffix == ".pdf"

    # Must be valid markdown with a title
    assert content.startswith("# Test Report")

    # Header row count must match cases run (3 data rows + 1 header)
    table_rows = [line for line in content.splitlines() if line.startswith("|")]
    # header separator row doesn't start with "| " + case_id pattern
    data_rows = [line for line in table_rows if "| GAS-" in line]
    assert len(data_rows) == 3, f"Expected 3 data rows in report table, got {len(data_rows)}"

    # Summary line
    assert "**Total:** 3" in content
    assert "**PASS:** 2" in content
    assert "**FAIL:** 1" in content


def test_report_all_pass(tmp_path):
    results = [
        {"case_id": "T-001", "verdict": "PASS", "detail": "ok", "duration_ms": 1.0},
    ]
    output_path = tmp_path / "report.md"
    write_report(results, output_path)
    content = output_path.read_text(encoding="utf-8")
    assert "**All cases passed.**" in content


def test_report_empty(tmp_path):
    results: list = []
    output_path = tmp_path / "report.md"
    write_report(results, output_path)
    content = output_path.read_text(encoding="utf-8")
    assert "**Total:** 0" in content
    assert "**All cases passed.**" in content
