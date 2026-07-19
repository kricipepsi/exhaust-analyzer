"""Generative overlap tests for GASLab."""

from __future__ import annotations

import pytest
from harness.generators.overlap import OverlapAnalyzer
from tests.fixtures.descriptor import build_gaslab_descriptor


@pytest.mark.slow
def test_gaslab_overlap_run() -> None:
    """Run the overlap analyzer against the GASLab descriptor (34 boxes) and verify counts."""
    desc = build_gaslab_descriptor()
    analyzer = OverlapAnalyzer(desc)
    report = analyzer.run()

    # 34 boxes -> 34*33/2 = 561 unordered pairs
    assert report.box_count == 34, f"Expected 34 boxes, got {report.box_count}"
    assert report.total_pairs == 561, f"Expected 561 pairs, got {report.total_pairs}"
    assert report.overlapping_count >= 0
    assert report.overlapping_count <= report.total_pairs

    # Coverage should have all 3 categories summing to ~100%
    c = report.coverage
    assert c.total_samples == 50_000
    assert abs(c.no_box_pct + c.single_box_pct + c.multi_box_pct - 100.0) < 0.2

    # SAMPLE_INVALID is a recognized box in the descriptor
    assert "SAMPLE_INVALID" in desc.boxes
