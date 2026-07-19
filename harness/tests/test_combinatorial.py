"""Tests for harness.generators.combinatorial — pairwise (t-wise) corner generator."""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor
from harness.generators.boundary import GAS_DIMS
from harness.generators.combinatorial import (
    CombinatorialCase,
    CombinatorialGenerator,
    CombinatorialReport,
    write_combinatorial_report,
)

try:
    from harness.descriptor import build_gaslab_descriptor

    _HAS_GASLAB = True
except ImportError:
    _HAS_GASLAB = False
    build_gaslab_descriptor = None  # type: ignore[assignment]

import pytest


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
# Structural tests — pairwise counts
# ---------------------------------------------------------------------------


def test_pairwise_count_per_box():
    """N boxes x C(5,2)=10 dim-pairs x 4 corners = 40N generated cases."""
    desc = _make_stub_descriptor()
    gen = CombinatorialGenerator(desc)
    cases = gen.generate()

    # 1 box x 10 pairs x 4 corners = 40
    assert len(cases) == 40, f"Expected 40 cases, got {len(cases)}"

    for case in cases:
        assert case.box_signature == "TEST_BOX"
        d1, d2 = case.dim_pair
        assert d1 in GAS_DIMS and d2 in GAS_DIMS
        assert d1 != d2
        assert len(case.point) == 5  # all 5 gas dims present
        for d in GAS_DIMS:
            assert d in case.point
        assert case.corner in {("mn", "mn"), ("mn", "mx"), ("mx", "mn"), ("mx", "mx")}
        assert case.geometric_oracle in ("inside", "outside")
        assert case.source == "stub $1"

    # Exactly the 10 unordered dim-pairs, each with 4 corners.
    from collections import Counter

    pair_counts = Counter(case.dim_pair for case in cases)
    expected_pairs = set(combinations(GAS_DIMS, 2))
    assert set(pair_counts) == expected_pairs
    for pair in expected_pairs:
        assert pair_counts[pair] == 4, f"{pair}: expected 4 corners, got {pair_counts[pair]}"


def test_pairwise_count_scales_with_boxes():
    """Generator scales linearly: 2 boxes -> 80 cases."""
    box_a = FaultBox("A", {d: (0, 10) for d in GAS_DIMS}, "src")
    box_b = FaultBox("B", {d: (5, 15) for d in GAS_DIMS}, "src")
    desc = ModuleDescriptor(
        name="multi",
        fields=[FieldRange(d, "float", 0, 100) for d in GAS_DIMS],
        boxes={"A": box_a, "B": box_b},
        build_args=lambda row: (row,),
        entry_point=lambda row: None,
        extract_expected=lambda row: {},
        diff=lambda a, e: [],
    )
    gen = CombinatorialGenerator(desc)
    cases = gen.generate()
    assert len(cases) == 80
    assert {c.box_signature for c in cases} == {"A", "B"}


# ---------------------------------------------------------------------------
# Corner coverage correctness
# ---------------------------------------------------------------------------


def test_pairwise_corners_cover_all_combos():
    """For one dim-pair, the 4 points are exactly {min,max}x{min,max}; others at centroid."""
    desc = _make_stub_descriptor()
    box = desc.boxes["TEST_BOX"]
    gen = CombinatorialGenerator(desc)
    cases = gen.generate()

    # Focus on the (gas_hc, gas_co) pair.
    pair = ("gas_hc", "gas_co")
    pair_cases = [c for c in cases if c.dim_pair == pair]
    assert len(pair_cases) == 4

    hc_lo, hc_hi = box.dimensions["gas_hc"]
    co_lo, co_hi = box.dimensions["gas_co"]

    observed = {(c.point["gas_hc"], c.point["gas_co"]) for c in pair_cases}
    expected = {
        (hc_lo, co_lo),
        (hc_lo, co_hi),
        (hc_hi, co_lo),
        (hc_hi, co_hi),
    }
    assert observed == expected

    # Non-paired dims sit at centroid for every case in this pair.
    for d in ("gas_co2", "gas_o2", "gas_nox"):
        d_lo, d_hi = box.dimensions[d]
        centroid = (d_lo + d_hi) / 2.0
        for c in pair_cases:
            assert c.point[d] == centroid, f"{c.case_id}: {d} not at centroid {centroid}"


def test_combinatorial_geometric_oracle_inside():
    """All pairwise corners of a well-formed box are geometrically inside."""
    desc = _make_stub_descriptor()
    gen = CombinatorialGenerator(desc)
    cases = gen.generate()
    for c in cases:
        assert c.geometric_oracle == "inside", (
            f"{c.case_id}: expected inside (box corner), got {c.geometric_oracle}"
        )


def test_corner_outside_when_other_dim_collapsed():
    """If a non-paired dimension's centroid is itself outside, the oracle reports outside.

    Construct a box whose gas_co2 interval is degenerate so the centroid is the
    only inside value; then verify the oracle still keys on ALL dims. Here we use
    a box where a paired corner lands outside another dim — impossible for a valid
    box, so instead we assert the oracle is a pure all-dims AND by checking a
    point we know is outside via a hand-built case is not produced (all generated
    points are inside). This guards against an oracle that ignores non-paired dims.
    """
    desc = _make_stub_descriptor()
    gen = CombinatorialGenerator(desc)
    box = desc.boxes["TEST_BOX"]

    # Directly exercise the oracle helper on a crafted outside point.
    outside_point = {d: (box.dimensions[d][0] + box.dimensions[d][1]) / 2.0 for d in GAS_DIMS}
    outside_point["gas_nox"] = box.dimensions["gas_nox"][1] + 50  # push one dim out
    assert gen._oracle(box, outside_point) == "outside"

    inside_point = {d: (box.dimensions[d][0] + box.dimensions[d][1]) / 2.0 for d in GAS_DIMS}
    assert gen._oracle(box, inside_point) == "inside"


# ---------------------------------------------------------------------------
# t parameter guard
# ---------------------------------------------------------------------------


def test_rejects_non_pairwise_t():
    """t != 2 is out of scope for this task and raises."""
    desc = _make_stub_descriptor()
    with pytest.raises(ValueError):
        CombinatorialGenerator(desc, t=3)


# ---------------------------------------------------------------------------
# Row building (int vs float formatting) — reuse boundary convention
# ---------------------------------------------------------------------------


def test_build_row_formats_int_dims():
    """Integer dimensions are formatted without decimal point."""
    desc = _make_stub_descriptor()
    gen = CombinatorialGenerator(desc)
    point = {"gas_hc": 50.0, "gas_co": 0.25, "gas_co2": 14.5, "gas_o2": 0.25, "gas_nox": 30.0}
    row = gen._build_row(point)
    assert row["gas_hc"] == "50"
    assert row["gas_nox"] == "30"
    assert row["gas_co"] == "0.25"


# ---------------------------------------------------------------------------
# run() — stub integration
# ---------------------------------------------------------------------------


def test_combinatorial_run_with_stub():
    """run() executes all cases through the descriptor and checks the oracle."""
    desc = _make_stub_descriptor()
    gen = CombinatorialGenerator(desc)
    report = gen.run()

    assert len(report.cases) == 40
    assert len(report.verdicts) == 40
    # Stub always returns "TEST_BOX"; all corners are inside, so all match.
    assert report.passes == 40
    assert report.failures == 0
    assert report.summary.startswith("**40/40**")


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def test_write_combinatorial_report_is_markdown(tmp_path):
    """write_combinatorial_report writes valid .md."""
    cases = [
        CombinatorialCase(
            "TH-CMB-X-gas_hc-gas_co-mnmn", "X", ("gas_hc", "gas_co"), ("mn", "mn"),
            {"gas_hc": 0, "gas_co": 0, "gas_co2": 0, "gas_o2": 0, "gas_nox": 0},
            "inside", "src",
        ),
    ]
    report = CombinatorialReport(
        cases=cases,
        verdicts=[{
            "case_id": "TH-CMB-X-gas_hc-gas_co-mnmn", "box": "X",
            "dim_pair": "(gas_hc, gas_co)", "corner": "(mn, mn)",
            "oracle": "inside", "actual": "X", "match": True,
        }],
        passes=1,
        failures=0,
        summary="**1/1** pairwise corners match.",
    )
    output_path = tmp_path / "combinatorial_report.md"
    write_combinatorial_report(report, output_path)

    assert output_path.is_file()
    assert output_path.suffix == ".md"
    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("# Combinatorial Generator Report")
    assert "**1/1**" in content
    assert "TH-CMB-X-gas_hc-gas_co-mnmn" in content


def test_write_combinatorial_report_with_failures(tmp_path):
    """Report includes a Failures section when mismatches exist."""
    cases = [
        CombinatorialCase(
            "TH-CMB-Y-gas_hc-gas_o2-mxmx", "Y", ("gas_hc", "gas_o2"), ("mx", "mx"),
            {"gas_hc": 100, "gas_co": 0, "gas_co2": 0, "gas_o2": 0.5, "gas_nox": 0},
            "inside", "src",
        ),
    ]
    report = CombinatorialReport(
        cases=cases,
        verdicts=[{
            "case_id": "TH-CMB-Y-gas_hc-gas_o2-mxmx", "box": "Y",
            "dim_pair": "(gas_hc, gas_o2)", "corner": "(mx, mx)",
            "oracle": "inside", "actual": "OTHER", "match": False,
        }],
        passes=0,
        failures=1,
        summary="**0/1** pairwise corners match.",
    )
    output_path = tmp_path / "combinatorial_report.md"
    write_combinatorial_report(report, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "## Failures" in content
    assert "TH-CMB-Y-gas_hc-gas_o2-mxmx" in content


# ---------------------------------------------------------------------------
# GASLab integration test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_combinatorial_gaslab_run():
    """Generate pairwise cases from the GASLab descriptor, run through the live
    entry_point, and write the report to progress_notes."""
    if build_gaslab_descriptor is None:
        pytest.skip("gaslab not importable")

    desc = build_gaslab_descriptor()
    gen = CombinatorialGenerator(desc)
    report = gen.run()

    # 34 boxes x C(5,2)=10 pairs x 4 corners = 1360 cases
    assert len(report.cases) == 1360, f"Expected 1360 cases, got {len(report.cases)}"
    assert len(report.verdicts) == 1360

    notes_dir = Path(__file__).resolve().parent.parent / "harness_tasks" / "progress_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    output_path = notes_dir / "T-TH-3_combinatorial_report.md"
    write_combinatorial_report(report, output_path)

    # Every case produced a verdict (no crashes).
    for v in report.verdicts:
        assert v["actual"], f"{v['case_id']}: empty actual — entry_point likely crashed"

    # At least some pairwise corners match the geometric oracle.
    assert report.passes > 0, "Zero pairwise corners matched — entry_point may be broken"
