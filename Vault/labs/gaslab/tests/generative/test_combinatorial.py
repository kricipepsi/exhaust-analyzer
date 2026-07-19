"""Generative combinatorial tests for GASLab."""

from __future__ import annotations

import pytest
from harness.generators.combinatorial import CombinatorialGenerator
from tests.fixtures.descriptor import build_gaslab_descriptor


@pytest.mark.slow
def test_combinatorial_gaslab_run() -> None:
    """Generate pairwise cases from the GASLab descriptor and run them."""
    desc = build_gaslab_descriptor()
    gen = CombinatorialGenerator(desc)
    report = gen.run()

    # 34 boxes x C(5,2)=10 pairs x 4 corners = 1360 cases
    assert len(report.cases) == 1360, f"Expected 1360 cases, got {len(report.cases)}"
    assert len(report.verdicts) == 1360

    # Verify every case produced a verdict (no crashes)
    for v in report.verdicts:
        assert v["actual"], f"{v['case_id']}: empty actual — entry_point likely crashed"
