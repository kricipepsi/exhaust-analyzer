"""Generative noise tests for GASLab."""

from __future__ import annotations

import pytest
from harness.generators.noise import NoiseCharacterizer
from tests.fixtures.descriptor import build_gaslab_descriptor


@pytest.mark.slow
def test_noise_gaslab_run() -> None:
    """Run the characterizer against the GASLab descriptor."""
    desc = build_gaslab_descriptor()
    char = NoiseCharacterizer(desc, seed=42)
    report = char.run()

    # 34 boxes, all defining 5 gas dims -> 34 retention curves
    assert len(report.retention) == 34, f"Expected 34 box curves, got {len(report.retention)}"

    # Every box has a retention value at every level
    for sig, curve in report.retention.items():
        for lvl in report.levels:
            assert lvl in curve, f"{sig} missing level {lvl}"
            assert 0.0 <= curve[lvl] <= 1.0

    # Aggregate has one value per level, zero-amplitude is full retention
    assert report.aggregate[0.0] == pytest.approx(1.0)
