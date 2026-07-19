"""Tests for harness.generators.overlap — box-overlap & coverage-gap analyzer."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import FaultBox, FieldRange, ModuleDescriptor
from harness.generators.boundary import GAS_DIMS
from harness.generators.overlap import (
    CoverageGapEstimate,
    OverlapAnalyzer,
    OverlapResult,
    OverlapReport,
    write_overlap_report,
)

try:
    from harness.descriptor import build_gaslab_descriptor

    _HAS_GASLAB = True
except ImportError:
    _HAS_GASLAB = False
    build_gaslab_descriptor = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _box(sig: str, dims: dict[str, tuple[float, float]], src: str = "test") -> FaultBox:
    return FaultBox(signature=sig, dimensions=dims, source=src)


def _make_descriptor(
    boxes: dict[str, FaultBox],
    name: str = "test",
) -> ModuleDescriptor:
    fields = [FieldRange(d, "float", 0, 100) for d in GAS_DIMS]
    return ModuleDescriptor(
        name=name,
        fields=fields,
        boxes=boxes,
        build_args=lambda row: (row,),
        entry_point=lambda row: None,
        extract_expected=lambda row: {},
        diff=lambda a, e: [],
    )


def _all_5_dims(lo_hc=0, hi_hc=100, lo_co=0.0, hi_co=1.0, lo_co2=0.0, hi_co2=20.0, lo_o2=0.0, hi_o2=20.0, lo_nox=0, hi_nox=100):
    return {
        "gas_hc": (float(lo_hc), float(hi_hc)),
        "gas_co": (lo_co, hi_co),
        "gas_co2": (lo_co2, hi_co2),
        "gas_o2": (lo_o2, hi_o2),
        "gas_nox": (float(lo_nox), float(hi_nox)),
    }


# ---------------------------------------------------------------------------
# Pairwise overlap detection
# ---------------------------------------------------------------------------


def test_pairwise_overlap_detects_intersection():
    """Two boxes that share region in all 5 dims are reported as overlapping."""
    box_a = _box("A", _all_5_dims(0, 100, 0.0, 1.0, 0.0, 20.0, 0.0, 20.0, 0, 100))
    box_b = _box("B", _all_5_dims(50, 150, 0.5, 1.5, 5.0, 20.0, 0.0, 20.0, 50, 150))
    desc = _make_descriptor({"A": box_a, "B": box_b})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert len(results) == 1  # one unordered pair
    r = results[0]
    assert r.sig_a == "A"
    assert r.sig_b == "B"
    assert r.overlaps is True
    assert r.identical_gas_signature is False
    inter = r.intersection_bounds
    assert inter is not None

    # Intersection bounds: max of mins, min of maxes
    assert inter["gas_hc"] == (50.0, 100.0)
    assert inter["gas_co"] == (0.5, 1.0)
    assert inter["gas_nox"] == (50.0, 100.0)


def test_pairwise_overlap_detects_disjoint():
    """Two boxes separated by a gap in one dimension are disjoint."""
    # Disjoint in gas_hc: A.hc=(0,100), B.hc=(200,300) — gap at 101-199
    box_a = _box("A", _all_5_dims(0, 100))
    box_b = _box("B", _all_5_dims(200, 300))
    desc = _make_descriptor({"A": box_a, "B": box_b})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert len(results) == 1
    r = results[0]
    assert r.overlaps is False
    assert r.intersection_bounds is None


def test_pairwise_overlap_touching_boundary_is_overlap():
    """Boxes that touch at a boundary (max of A == min of B) count as overlap."""
    box_a = _box("A", _all_5_dims(0, 100))
    box_b = _box("B", _all_5_dims(100, 200))
    desc = _make_descriptor({"A": box_a, "B": box_b})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert results[0].overlaps is True
    bounds = results[0].intersection_bounds
    assert bounds is not None
    assert bounds["gas_hc"] == (100.0, 100.0)


def test_pairwise_overlap_identical_gas_signature():
    """Two boxes with identical bounds in all 5 dims are flagged as identical."""
    dims = _all_5_dims(0, 100, 0.0, 0.5, 13.0, 16.0, 0.0, 0.5, 0, 100)
    box_a = _box("SIG_X", dims)
    box_b = _box("SIG_Y", dict(dims))  # same bounds, different dict
    desc = _make_descriptor({"SIG_X": box_a, "SIG_Y": box_b})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert results[0].overlaps is True
    assert results[0].identical_gas_signature is True
    assert "identical gas signature" in results[0].note


def test_pairwise_overlap_multiple_pairs():
    """With 3 boxes, all 3 unordered pairs are analyzed."""
    box_a = _box("A", _all_5_dims(0, 10))
    box_b = _box("B", _all_5_dims(5, 15))
    box_c = _box("C", _all_5_dims(100, 200))
    desc = _make_descriptor({"A": box_a, "B": box_b, "C": box_c})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert len(results) == 3  # AB, AC, BC
    sig_pairs = {(r.sig_a, r.sig_b) for r in results}
    assert sig_pairs == {("A", "B"), ("A", "C"), ("B", "C")}

    # A-B overlaps, A-C and B-C are disjoint
    overlaps = {("A", "B"): True, ("A", "C"): False, ("B", "C"): False}
    for r in results:
        assert r.overlaps == overlaps[(r.sig_a, r.sig_b)]


def test_pairwise_overlap_one_dim_gap_makes_disjoint():
    """A gap in any single dimension makes the pair disjoint regardless of
    overlap in all other dimensions."""
    # Identical in 4 dims, disjoint in gas_nox
    box_a = _box("A", {"gas_hc": (0, 100), "gas_co": (0, 1), "gas_co2": (0, 20), "gas_o2": (0, 20), "gas_nox": (0, 50)})
    box_b = _box("B", {"gas_hc": (0, 100), "gas_co": (0, 1), "gas_co2": (0, 20), "gas_o2": (0, 20), "gas_nox": (100, 200)})
    desc = _make_descriptor({"A": box_a, "B": box_b})
    analyzer = OverlapAnalyzer(desc)
    results = analyzer.analyze_overlaps()

    assert results[0].overlaps is False


# ---------------------------------------------------------------------------
# Coverage-gap estimation
# ---------------------------------------------------------------------------


def test_coverage_gap_sampling_sums_to_100():
    """Monte Carlo categories sum to 100%."""
    # Two small boxes in a large envelope → mostly no-box
    box_a = _box("A", _all_5_dims(0, 10, 0.0, 0.1, 0.0, 0.1, 0.0, 0.1, 0, 10))
    box_b = _box("B", _all_5_dims(50, 60, 0.5, 0.6, 10.0, 10.1, 5.0, 5.1, 50, 60))
    desc = _make_descriptor({"A": box_a, "B": box_b})
    analyzer = OverlapAnalyzer(desc)
    est = analyzer.estimate_coverage()

    assert est.total_samples == 50_000
    total_pct = est.no_box_pct + est.single_box_pct + est.multi_box_pct
    assert abs(total_pct - 100.0) < 0.1, f"sum={total_pct:.2f}%, expected ~100%"

    # With tiny boxes in a huge envelope, most samples hit nothing
    assert est.no_box_pct > 95.0, f"Expected >95% no-box, got {est.no_box_pct:.1f}%"
    assert est.multi_box_pct < 1.0


def test_coverage_gap_seeded_reproducible():
    """Same seed produces identical coverage estimates."""
    box = _box("X", _all_5_dims(0, 100))
    desc = _make_descriptor({"X": box})

    est1 = OverlapAnalyzer(desc, seed=42).estimate_coverage()
    est2 = OverlapAnalyzer(desc, seed=42).estimate_coverage()

    assert est1.no_box_count == est2.no_box_count
    assert est1.single_box_count == est2.single_box_count
    assert est1.multi_box_count == est2.multi_box_count


def test_coverage_gap_single_box_covers_all():
    """A single box covering the full envelope gets 100% single-box hits."""
    dims = _all_5_dims(0, 20000, 0.0, 15.0, 0.0, 22.0, 0.0, 22.0, 0, 5000)
    box = _box("FULL", dims)
    desc = _make_descriptor({"FULL": box})
    est = OverlapAnalyzer(desc).estimate_coverage()

    assert est.single_box_pct == 100.0
    assert est.no_box_pct == 0.0
    assert est.multi_box_pct == 0.0
    assert est.per_box_hit_counts["FULL"] == 50_000


def test_coverage_gap_identical_boxes_both_count():
    """Two identical full-envelope boxes → every point hits both = multi_box."""
    dims = _all_5_dims(0, 20000, 0.0, 15.0, 0.0, 22.0, 0.0, 22.0, 0, 5000)
    box_a = _box("A", dict(dims))
    box_b = _box("B", dict(dims))
    desc = _make_descriptor({"A": box_a, "B": box_b})
    est = OverlapAnalyzer(desc).estimate_coverage()

    assert est.single_box_pct == 0.0
    assert est.multi_box_pct == 100.0
    assert est.per_box_hit_counts["A"] == 50_000
    assert est.per_box_hit_counts["B"] == 50_000


# ---------------------------------------------------------------------------
# OverlapAnalyzer.run()
# ---------------------------------------------------------------------------


def test_run_produces_report_with_correct_counts():
    """run() produces an OverlapReport with correct summary stats."""
    box_a = _box("A", _all_5_dims(0, 100))
    box_b = _box("B", _all_5_dims(50, 150))
    box_c = _box("C", _all_5_dims(200, 300))
    desc = _make_descriptor({"A": box_a, "B": box_b, "C": box_c})
    report = OverlapAnalyzer(desc).run()

    assert report.module_name == "test"
    assert report.box_count == 3
    assert report.total_pairs == 3
    assert report.overlapping_count == 1  # A-B only
    assert report.identical_count == 0
    assert len(report.overlap_pairs) == 3
    assert report.coverage.total_samples == 50_000


# ---------------------------------------------------------------------------
# Report writing
# ---------------------------------------------------------------------------


def test_write_overlap_report_is_markdown(tmp_path):
    """write_overlap_report writes valid .md."""
    r = OverlapResult("A", "B", True, False, {"gas_hc": (0.0, 50.0)}, "")
    coverage = CoverageGapEstimate(
        total_samples=1000, no_box_count=500, single_box_count=300,
        multi_box_count=200, no_box_pct=50.0, single_box_pct=30.0,
        multi_box_pct=20.0, per_box_hit_counts={"A": 400, "B": 300},
    )
    report = OverlapReport(
        module_name="test", box_count=2, dims=["gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox"],
        overlap_pairs=[r], coverage=coverage, total_pairs=1,
        overlapping_count=1, identical_count=0,
    )
    output_path = tmp_path / "overlap_report.md"
    write_overlap_report(report, output_path)

    assert output_path.is_file()
    assert output_path.suffix == ".md"
    content = output_path.read_text(encoding="utf-8")
    assert content.startswith("# Box Overlap & Coverage-Gap Report")
    assert "**Module:** test" in content
    assert "No box (unclassifiable hole)" in content
    assert "50.0%" in content
    assert "A" in content and "B" in content


def test_write_overlap_report_with_identical(tmp_path):
    """Identical gas signatures get their own section."""
    r = OverlapResult("X", "Y", True, True, {"gas_hc": (0.0, 100.0)}, "identical gas signature")
    coverage = CoverageGapEstimate(1000, 0, 0, 1000, 0.0, 0.0, 100.0, {"X": 1000, "Y": 1000})
    report = OverlapReport(
        module_name="test", box_count=2, dims=list(GAS_DIMS),
        overlap_pairs=[r], coverage=coverage, total_pairs=1,
        overlapping_count=1, identical_count=1,
    )
    output_path = tmp_path / "overlap_report.md"
    write_overlap_report(report, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "## Identical Gas Signatures" in content
    assert "identical gas signature" in content


def test_write_overlap_report_with_disjoint(tmp_path):
    """Disjoint pairs are counted in summary."""
    r = OverlapResult("A", "B", False, False, None, "")
    coverage = CoverageGapEstimate(1000, 0, 1000, 0, 0.0, 100.0, 0.0, {"A": 500, "B": 500})
    report = OverlapReport(
        module_name="test", box_count=2, dims=list(GAS_DIMS),
        overlap_pairs=[r], coverage=coverage, total_pairs=1,
        overlapping_count=0, identical_count=0,
    )
    output_path = tmp_path / "overlap_report.md"
    write_overlap_report(report, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "**Disjoint pairs:** 1/1" in content


def test_write_overlap_report_zero_hit_boxes(tmp_path):
    """Boxes with zero Monte Carlo hits get a dedicated section."""
    coverage = CoverageGapEstimate(1000, 1000, 0, 0, 100.0, 0.0, 0.0, {"A": 0, "B": 0})
    report = OverlapReport(
        module_name="test", box_count=2, dims=list(GAS_DIMS),
        overlap_pairs=[], coverage=coverage, total_pairs=1,
        overlapping_count=0, identical_count=0,
    )
    output_path = tmp_path / "overlap_report.md"
    write_overlap_report(report, output_path)

    content = output_path.read_text(encoding="utf-8")
    assert "### Zero-coverage boxes" in content
    assert "- A" in content
    assert "- B" in content


# ---------------------------------------------------------------------------
# GASLab integration test
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_gaslab_overlap_run():
    """Run the overlap analyzer against the GASLab descriptor (34 boxes),
    identify overlapping pairs, estimate the coverage gap, and write the
    report to progress_notes."""
    if build_gaslab_descriptor is None:
        pytest.skip("gaslab not importable")

    desc = build_gaslab_descriptor()
    analyzer = OverlapAnalyzer(desc)
    report = analyzer.run()

    # 34 boxes → 34*33/2 = 561 unordered pairs
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

    # Write report to progress notes
    notes_dir = Path(__file__).resolve().parent.parent / "harness_tasks" / "progress_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    output_path = notes_dir / "T-TH-2_overlap_report.md"
    write_overlap_report(report, output_path)

    assert output_path.is_file()
    content = output_path.read_text(encoding="utf-8")
    # Sanity: the report mentions key findings
    assert "Box Overlap & Coverage-Gap Report" in content
    assert "SAMPLE_INVALID" in content or "discrimination" in content.lower()
