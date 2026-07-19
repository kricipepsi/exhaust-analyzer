"""Generative boundary tests for GASLab."""

from __future__ import annotations

import pytest
from harness.generators.boundary import BoundaryGenerator
from tests.fixtures.descriptor import build_gaslab_descriptor


@pytest.mark.slow
def test_boundary_gaslab_run() -> None:
    """Generate boundary cases from the GASLab descriptor and run them."""
    desc = build_gaslab_descriptor()
    gen = BoundaryGenerator(desc)
    report = gen.run()

    # 34 boxes x 5 dims x 6 positions = 1020 cases
    assert len(report.cases) == 1020, f"Expected 1020 cases, got {len(report.cases)}"
    assert len(report.verdicts) == 1020

    # Verify every case produced a verdict (no crashes)
    for v in report.verdicts:
        assert v["actual"], f"{v['case_id']}: empty actual — entry_point likely crashed"
