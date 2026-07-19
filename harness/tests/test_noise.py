"""Tests for harness.generators.noise — noise / fault-injection characterization.

This is a CHARACTERIZATION report, not a pass/fail gate. These tests assert
generator shape, seeded determinism, envelope clamping, and report emission —
never a degradation threshold on the retention curve itself.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor
from harness.generators.boundary import GAS_DIMS
from harness.generators.noise import (
    DEFAULT_LEVELS,
    NoiseCase,
    NoiseCharacterizer,
    NoiseReport,
    write_noise_report,
)

try:
    from harness.descriptor import build_gaslab_descriptor

    _HAS_GASLAB = True
except ImportError:
    _HAS_GASLAB = False
    build_gaslab_descriptor = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Stub descriptor for unit tests (no gaslab import needed)
# ---------------------------------------------------------------------------


def _make_stub_descriptor() -> ModuleDescriptor:
    """A minimal descriptor with one known box.

    The stub entry_point returns a label that depends on gas_hc: it returns
    "TEST_BOX" while gas_hc stays within [0, 100] and "OTHER" once gas_hc
    leaves that band. This lets retention tests observe a label flip under
    noise without needing the live classifier.
    """
    box = FaultBox(
        signature="TEST_BOX",
        dimensions={
            "gas_hc": (0, 100),
            "gas_co": (0.0, 0.5),
            "gas_co2": (13.0, 16.0),
            "gas_o2": (0.0, 0.5),
            "gas_nox": (0, 100),
        },
        source="stub $1",
    )

    def _entry_point(row: dict) -> object:
        hc = float(row["gas_hc"])
        label = "TEST_BOX" if 0 <= hc <= 100 else "OTHER"
        return type(
            "Result",
            (),
            {"chemical_state": type("CS", (), {"value": label})()},
        )()

    return ModuleDescriptor(
        name="stub",
        fields=[
            FieldRange("gas_hc", "int", 0, 20000),
            FieldRange("gas_co", "float", 0.0, 15.0),
            FieldRange("gas_co2", "float", 0.0, 22.0),
            FieldRange("gas_o2", "float", 0.0, 22.0),
            FieldRange("gas_nox", "int", 0, 5000),
        ],
        boxes={"TEST_BOX": box},
        build_args=lambda row: (row,),
        entry_point=_entry_point,
        extract_expected=lambda row: {},
        diff=lambda actual, expected: [],
    )


# ---------------------------------------------------------------------------
# Structural test — case count
# ---------------------------------------------------------------------------


def test_noise_generates_expected_count():
    """N boxes x len(levels) x samples_per_level perturbed cases."""
    desc = _make_stub_descriptor()
    levels = (0.0, 0.1, 0.5)
    samples = 8
    char = NoiseCharacterizer(desc, levels=levels, samples_per_level=samples)
    cases = char.generate()

    # 1 box x 3 levels x 8 samples = 24
    assert len(cases) == 24, f"Expected 24 cases, got {len(cases)}"

    for case in cases:
        assert case.box_signature == "TEST_BOX"
        assert case.amplitude in levels
        assert len(case.point) == 5
        for d in GAS_DIMS:
            assert d in case.point
        assert case.source == "stub $1"

    # Each (level) gets exactly `samples` cases for the one box
    from collections import Counter

    level_counts = Counter(case.amplitude for case in cases)
    for lvl in levels:
        assert level_counts[lvl] == samples, (
            f"level {lvl}: expected {samples}, got {level_counts[lvl]}"
        )

    # At amplitude 0.0, every sample equals the centroid (no perturbation).
    centroid = {"gas_hc": 50.0, "gas_co": 0.25, "gas_co2": 14.5, "gas_o2": 0.25, "gas_nox": 50.0}
    zero_cases = [c for c in cases if c.amplitude == 0.0]
    for c in zero_cases:
        for d in GAS_DIMS:
            assert c.point[d] == pytest.approx(centroid[d]), (
                f"amplitude 0 should not perturb {d}: {c.point[d]} != {centroid[d]}"
            )


# ---------------------------------------------------------------------------
# Seeded determinism — the hard requirement
# ---------------------------------------------------------------------------


def test_noise_is_seeded_deterministic():
    """Same seed → identical points and retention; different seed → differs."""
    desc = _make_stub_descriptor()
    levels = (0.0, 0.25, 1.0)

    char_a = NoiseCharacterizer(desc, seed=42, levels=levels, samples_per_level=10)
    char_b = NoiseCharacterizer(desc, seed=42, levels=levels, samples_per_level=10)
    cases_a = char_a.generate()
    cases_b = char_b.generate()

    assert len(cases_a) == len(cases_b)
    for ca, cb in zip(cases_a, cases_b, strict=True):
        assert ca.point == cb.point, "same seed must yield identical points"

    # Retention curves identical under same seed
    report_a = char_a.run()
    report_b = char_b.run()
    assert report_a.retention == report_b.retention

    # Different seed → at least one perturbed point differs
    char_c = NoiseCharacterizer(desc, seed=999, levels=levels, samples_per_level=10)
    cases_c = char_c.generate()
    # Compare only perturbed (amplitude > 0) points; amplitude-0 points are
    # always the centroid regardless of seed.
    perturbed_a = [c.point for c in cases_a if c.amplitude > 0]
    perturbed_c = [c.point for c in cases_c if c.amplitude > 0]
    assert perturbed_a != perturbed_c, "different seed should change perturbations"


# ---------------------------------------------------------------------------
# Envelope clamping
# ---------------------------------------------------------------------------


def test_noise_amplitude_clamped_to_envelope():
    """Perturbed values stay within [field.min_, field.max_]; ints are integral."""
    desc = _make_stub_descriptor()
    # Large amplitude to force perturbation toward / past the envelope edges.
    char = NoiseCharacterizer(desc, seed=7, levels=(2.0,), samples_per_level=200)
    cases = char.generate()

    for case in cases:
        for d in GAS_DIMS:
            fld = desc.get_field(d)
            assert fld is not None
            assert fld.min_ is not None and fld.max_ is not None
            v = case.point[d]
            assert v >= fld.min_, f"{d}={v} below envelope min {fld.min_}"
            assert v <= fld.max_, f"{d}={v} above envelope max {fld.max_}"
        # int dims must be whole numbers
        assert float(case.point["gas_hc"]).is_integer()
        assert float(case.point["gas_nox"]).is_integer()


# ---------------------------------------------------------------------------
# Retention semantics (stub: label flips when gas_hc leaves [0,100])
# ---------------------------------------------------------------------------


def test_noise_retention_decreases_with_amplitude():
    """With the stub's hc-dependent label, retention at high amplitude is
    no greater than at zero amplitude (which is always 100%)."""
    desc = _make_stub_descriptor()
    char = NoiseCharacterizer(desc, seed=3, levels=(0.0, 1.0), samples_per_level=100)
    report = char.run()

    ret = report.retention["TEST_BOX"]
    assert ret[0.0] == pytest.approx(1.0), "zero-amplitude retention must be 100%"
    assert ret[1.0] <= ret[0.0], "retention should not increase with amplitude"


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def test_write_noise_report_is_markdown(tmp_path):
    """write_noise_report writes valid .md with the expected sections."""
    cases = [
        NoiseCase("TH-NOI-X-0.0-0", "X", 0.0, 0, {"gas_hc": 50.0}, "src"),
    ]
    report = NoiseReport(
        cases=cases,
        baseline_labels={"X": "X"},
        retention={"X": {0.0: 1.0, 0.5: 0.4}},
        aggregate={0.0: 1.0, 0.5: 0.4},
        levels=(0.0, 0.5),
        seed=42,
        distribution="uniform",
        samples_per_level=10,
        summary="**characterization** of 1 box.",
    )
    output_path = tmp_path / "noise_report.md"
    write_noise_report(report, output_path)

    assert output_path.is_file()
    assert output_path.suffix == ".md"
    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("# Noise Characterization Report")
    assert "Aggregate" in content
    assert "X" in content  # per-box table mentions the box
    assert "seed" in content.lower()


def test_default_levels_present():
    """DEFAULT_LEVELS is the documented amplitude sweep."""
    assert DEFAULT_LEVELS[0] == 0.0  # baseline included
    assert DEFAULT_LEVELS == (0.0, 0.1, 0.25, 0.5, 1.0)


# ---------------------------------------------------------------------------
# GASLab integration test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_noise_gaslab_run():
    """Run the characterizer against the GASLab descriptor, write the report."""
    if build_gaslab_descriptor is None:
        pytest.skip("gaslab not importable")

    desc = build_gaslab_descriptor()
    char = NoiseCharacterizer(desc, seed=42)
    report = char.run()

    # 34 boxes, all defining 5 gas dims → 34 retention curves
    assert len(report.retention) == 34, (
        f"Expected 34 box curves, got {len(report.retention)}"
    )
    # Every box has a retention value at every level
    for sig, curve in report.retention.items():
        for lvl in report.levels:
            assert lvl in curve, f"{sig} missing level {lvl}"
            assert 0.0 <= curve[lvl] <= 1.0

    # Aggregate has one value per level, zero-amplitude is full retention
    assert report.aggregate[0.0] == pytest.approx(1.0)

    notes_dir = Path(__file__).resolve().parent.parent / "harness_tasks" / "progress_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    output_path = notes_dir / "T-TH-4_noise_report.md"
    write_noise_report(report, output_path)
    assert output_path.is_file()
