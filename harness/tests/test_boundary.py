"""Tests for harness.generators.boundary — boundary / edge-point generator."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor
from harness.generators.boundary import (
    DEFAULT_EPS,
    GAS_DIMS,
    POSITIONS,
    BoundaryCase,
    BoundaryGenerator,
    BoundaryReport,
    write_boundary_report,
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
    """A minimal descriptor with one known box for testing generation logic."""
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

    # entry_point returns a dummy whose .chemical_state.value is always "TEST_BOX"
    def _entry_point(row: dict) -> object:
        return type(
            "Result",
            (),
            {"chemical_state": type("CS", (), {"value": "TEST_BOX"})()},
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
# Structural tests
# ---------------------------------------------------------------------------


def test_boundary_generates_six_per_dim_per_box():
    """N boxes x 5 gas dims x 6 positions = 30N generated cases."""
    desc = _make_stub_descriptor()
    gen = BoundaryGenerator(desc)
    cases = gen.generate()

    # 1 box x 5 dims x 6 positions = 30
    assert len(cases) == 30, f"Expected 30 cases, got {len(cases)}"

    # Every case has the expected shape
    for case in cases:
        assert case.box_signature == "TEST_BOX"
        assert case.dim_name in GAS_DIMS
        assert case.position in POSITIONS
        assert len(case.point) == 5  # all 5 gas dims set
        for d in GAS_DIMS:
            assert d in case.point
        assert case.geometric_oracle in ("inside", "outside")
        assert case.source == "stub $1"

    # Each dim gets exactly 6 positions
    from collections import Counter

    dim_counts = Counter(case.dim_name for case in cases)
    for dim in GAS_DIMS:
        assert dim_counts[dim] == 6, f"{dim}: expected 6, got {dim_counts[dim]}"

    # Each position appears exactly once per dim
    for dim in GAS_DIMS:
        dim_positions = [
            case.position for case in cases if case.dim_name == dim
        ]
        assert set(dim_positions) == set(POSITIONS), f"{dim}: missing positions"


def test_boundary_generates_multiple_boxes():
    """Generator scales linearly with box count."""
    box_a = FaultBox("A", {"gas_hc": (0, 10), "gas_co": (0, 1), "gas_co2": (0, 1), "gas_o2": (0, 1), "gas_nox": (0, 10)}, "src")
    box_b = FaultBox("B", {"gas_hc": (5, 15), "gas_co": (0, 1), "gas_co2": (0, 1), "gas_o2": (0, 1), "gas_nox": (0, 10)}, "src")

    desc = ModuleDescriptor(
        name="multi",
        fields=[FieldRange(d, "float", 0, 100) for d in GAS_DIMS],
        boxes={"A": box_a, "B": box_b},
        build_args=lambda row: (row,),
        entry_point=lambda row: None,
        extract_expected=lambda row: {},
        diff=lambda a, e: [],
    )
    gen = BoundaryGenerator(desc)
    cases = gen.generate()

    # 2 boxes x 5 dims x 6 positions = 60
    assert len(cases) == 60
    sigs = {case.box_signature for case in cases}
    assert sigs == {"A", "B"}


# ---------------------------------------------------------------------------
# Geometric oracle correctness
# ---------------------------------------------------------------------------


def test_boundary_geometric_oracle_correct():
    """For a known box, inside/outside labels match the geometry."""
    desc = _make_stub_descriptor()
    gen = BoundaryGenerator(desc)
    cases = gen.generate()

    # Pick a specific case: gas_hc at min-eps
    # Box gas_hc bounds: (0, 100), eps=1
    # min-eps = -1 → outside (hc < 0)
    min_eps_cases = [
        c for c in cases
        if c.dim_name == "gas_hc" and c.position == "min-eps"
    ]
    assert len(min_eps_cases) == 1
    assert min_eps_cases[0].geometric_oracle == "outside"
    assert min_eps_cases[0].point["gas_hc"] == 0 - DEFAULT_EPS["gas_hc"]

    # max+eps = 101 → outside (hc > 100)
    max_eps_cases = [
        c for c in cases
        if c.dim_name == "gas_hc" and c.position == "max+eps"
    ]
    assert len(max_eps_cases) == 1
    assert max_eps_cases[0].geometric_oracle == "outside"
    assert max_eps_cases[0].point["gas_hc"] == 100 + DEFAULT_EPS["gas_hc"]

    # min → inside (hc == 0, boundary)
    min_cases = [
        c for c in cases
        if c.dim_name == "gas_hc" and c.position == "min"
    ]
    assert len(min_cases) == 1
    assert min_cases[0].geometric_oracle == "inside"
    assert min_cases[0].point["gas_hc"] == 0.0

    # min+eps = 1 → inside (0 < 1 < 100)
    min_plus_cases = [
        c for c in cases
        if c.dim_name == "gas_hc" and c.position == "min+eps"
    ]
    assert len(min_plus_cases) == 1
    assert min_plus_cases[0].geometric_oracle == "inside"
    assert min_plus_cases[0].point["gas_hc"] == 0 + DEFAULT_EPS["gas_hc"]

    # Centroid is the base value for non-target dims
    # Box gas_hc=(0,100) → centroid=50. When testing gas_co boundary,
    # gas_hc should be at centroid 50.
    for case in cases:
        if case.dim_name != "gas_hc":
            assert case.point["gas_hc"] == 50.0, (
                f"{case.case_id}: expected gas_hc at centroid 50.0, "
                f"got {case.point['gas_hc']}"
            )


def test_boundary_oracle_outside_when_one_dim_outside():
    """A point is outside the box if even one dimension is outside bounds."""
    desc = _make_stub_descriptor()
    gen = BoundaryGenerator(desc)

    # Generate cases, find a min-eps case → should be "outside"
    cases = gen.generate()
    outside_cases = [c for c in cases if c.position in ("min-eps", "max+eps")]
    assert len(outside_cases) > 0
    for case in outside_cases:
        assert case.geometric_oracle == "outside", (
            f"{case.case_id}: expected outside, got {case.geometric_oracle}"
        )

    # min/max/min+eps/max-eps → should be "inside"
    inside_cases = [
        c for c in cases if c.position in ("min", "min+eps", "max-eps", "max")
    ]
    for case in inside_cases:
        assert case.geometric_oracle == "inside", (
            f"{case.case_id}: expected inside, got {case.geometric_oracle}"
        )


# ---------------------------------------------------------------------------
# Row building (int vs float formatting)
# ---------------------------------------------------------------------------


def test_build_row_formats_int_dims():
    """Integer dimensions are formatted without decimal point."""
    desc = _make_stub_descriptor()
    gen = BoundaryGenerator(desc)

    point = {"gas_hc": 50.0, "gas_co": 0.25, "gas_co2": 14.5, "gas_o2": 0.25, "gas_nox": 30.0}
    row = gen._build_row(point)

    assert row["gas_hc"] == "50"  # int, no ".0"
    assert row["gas_nox"] == "30"  # int
    assert row["gas_co"] == "0.25"  # float
    assert row["gas_co2"] == "14.5"  # float
    assert row["gas_o2"] == "0.25"  # float


# ---------------------------------------------------------------------------
# Epsilon configurability
# ---------------------------------------------------------------------------


def test_custom_epsilon():
    """Custom epsilon values are used when provided."""
    desc = _make_stub_descriptor()
    custom_eps = {"gas_hc": 5.0, "gas_co": 0.05}
    gen = BoundaryGenerator(desc, eps=custom_eps)

    cases = gen.generate()

    # gas_hc min-eps with custom eps=5 → 0 - 5 = -5
    hc_min_eps = [
        c for c in cases if c.dim_name == "gas_hc" and c.position == "min-eps"
    ]
    assert hc_min_eps[0].point["gas_hc"] == -5.0

    # gas_co min-eps with custom eps=0.05 → 0 - 0.05 = -0.05
    co_min_eps = [
        c for c in cases if c.dim_name == "gas_co" and c.position == "min-eps"
    ]
    assert co_min_eps[0].point["gas_co"] == pytest.approx(-0.05)

    # Unspecified dims fall back to DEFAULT_EPS
    nox_min_eps = [
        c for c in cases if c.dim_name == "gas_nox" and c.position == "min-eps"
    ]
    assert nox_min_eps[0].point["gas_nox"] == 0 - DEFAULT_EPS["gas_nox"]


# ---------------------------------------------------------------------------
# BoundaryGenerator.run() — stub integration
# ---------------------------------------------------------------------------


def test_boundary_run_with_stub():
    """run() executes all cases through the descriptor and checks oracle."""
    desc = _make_stub_descriptor()
    gen = BoundaryGenerator(desc)
    report = gen.run()

    assert len(report.cases) == 30
    assert len(report.verdicts) == 30
    # Stub entry_point always returns "TEST_BOX", so:
    # - inside points → match (predicted TEST_BOX, oracle=inside)
    # - outside points → mismatch (predicted TEST_BOX, oracle=outside)
    inside_count = sum(1 for c in report.cases if c.geometric_oracle == "inside")
    outside_count = sum(1 for c in report.cases if c.geometric_oracle == "outside")
    assert report.passes == inside_count
    assert report.failures == outside_count
    assert report.summary.startswith(f"**{inside_count}/{len(report.cases)}**")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def test_write_boundary_report_is_markdown(tmp_path):
    """write_boundary_report writes valid .md."""
    cases = [
        BoundaryCase("TH-BND-X-gas_hc-min", "X", "gas_hc", "min", {"gas_hc": 0}, "inside", "src"),
    ]
    report = BoundaryReport(
        cases=cases,
        verdicts=[{"case_id": "TH-BND-X-gas_hc-min", "box": "X", "dim": "gas_hc", "position": "min", "oracle": "inside", "actual": "X", "match": True}],
        passes=1,
        failures=0,
        summary="**1/1** boundary points match.",
    )
    output_path = tmp_path / "boundary_report.md"
    write_boundary_report(report, output_path)

    assert output_path.is_file()
    assert output_path.suffix == ".md"
    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("# Boundary Generator Report")
    assert "**1/1**" in content
    assert "**All cases passed.**" not in content  # summary is custom
    assert "TH-BND-X-gas_hc-min" in content


def test_write_boundary_report_with_failures(tmp_path):
    """Report includes a Failures section when mismatches exist."""
    cases = [
        BoundaryCase("TH-BND-Y-gas_hc-max+eps", "Y", "gas_hc", "max+eps", {"gas_hc": 101}, "outside", "src"),
    ]
    report = BoundaryReport(
        cases=cases,
        verdicts=[{"case_id": "TH-BND-Y-gas_hc-max+eps", "box": "Y", "dim": "gas_hc", "position": "max+eps", "oracle": "outside", "actual": "Y", "match": False}],
        passes=0,
        failures=1,
        summary="**0/1** boundary points match.",
    )
    output_path = tmp_path / "boundary_report.md"
    write_boundary_report(report, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "## Failures" in content
    assert "TH-BND-Y-gas_hc-max+eps" in content


# ---------------------------------------------------------------------------
# GASLab integration test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_boundary_gaslab_run():
    """Generate boundary cases from the GASLab descriptor, run through live
    entry_point, and write the report to progress_notes."""
    if build_gaslab_descriptor is None:
        pytest.skip("gaslab not importable")

    desc = build_gaslab_descriptor()
    gen = BoundaryGenerator(desc)
    report = gen.run()

    # 34 boxes x 5 dims x 6 positions = 1020 cases
    assert len(report.cases) == 1020, f"Expected 1020 cases, got {len(report.cases)}"
    assert len(report.verdicts) == 1020

    # Write report to progress notes
    notes_dir = Path(__file__).resolve().parent.parent / "harness_tasks" / "progress_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    output_path = notes_dir / "T-TH-1_boundary_report.md"
    write_boundary_report(report, output_path)

    # Every case produced a verdict (no crashes)
    for v in report.verdicts:
        assert v["actual"], f"{v['case_id']}: empty actual — entry_point likely crashed"

    # Sanity: at least some cases pass (classifier matches geometric oracle
    # for unambiguous points).  We don't assert a specific number because
    # overlap (T-TH-2) may explain some mismatches.
    assert report.passes > 0, "Zero boundary points matched — entry_point may be broken"
