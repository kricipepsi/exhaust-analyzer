"""Box-overlap and coverage-gap analyzer for the generative test harness.

Lab-agnostic: imports no lab runtime code. Operates on a ModuleDescriptor.
Computes pairwise box overlaps and Monte Carlo coverage-gap estimates in
N-D gas feature space, then emits a .md report. Pure static geometry —
the classifier is not invoked.

Targets the discrimination ceiling: overlapping boxes are structurally
ambiguous on gas chemistry alone; coverage gaps are regions where no
fault box claims the reading.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harness.descriptor import ModuleDescriptor
from harness.generators.boundary import GAS_DIMS

# Measurement envelope per-dimension (global plausible range for gas values).
# Sourced from GAS_VOCABULARY §2.
_ENVELOPE: dict[str, tuple[float, float]] = {
    "gas_hc": (0.0, 20000.0),
    "gas_co": (0.0, 15.0),
    "gas_co2": (0.0, 22.0),
    "gas_o2": (0.0, 22.0),
    "gas_nox": (0.0, 5000.0),
}

_MONTE_CARLO_N = 50_000
_SEED = 42


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class OverlapResult:
    """One unordered box pair's overlap status."""

    sig_a: str
    sig_b: str
    overlaps: bool
    identical_gas_signature: bool
    intersection_bounds: dict[str, tuple[float, float]] | None
    note: str


@dataclass
class CoverageGapEstimate:
    """Monte Carlo coverage-gap estimate."""

    total_samples: int
    no_box_count: int
    single_box_count: int
    multi_box_count: int
    no_box_pct: float
    single_box_pct: float
    multi_box_pct: float
    per_box_hit_counts: dict[str, int]


@dataclass
class OverlapReport:
    """Full overlap + coverage-gap analysis result."""

    module_name: str
    box_count: int
    dims: list[str]
    overlap_pairs: list[OverlapResult]
    coverage: CoverageGapEstimate
    total_pairs: int
    overlapping_count: int
    identical_count: int


# ---------------------------------------------------------------------------
# Overlap detection
# ---------------------------------------------------------------------------


class OverlapAnalyzer:
    """Static-geometry analysis of a ModuleDescriptor's box table.

    Computes pairwise box overlaps and Monte Carlo coverage-gap estimates.
    No entry_point calls — pure geometry on the box definitions.
    """

    def __init__(
        self,
        descriptor: ModuleDescriptor,
        dims: tuple[str, ...] | None = None,
        seed: int = _SEED,
    ) -> None:
        self.descriptor = descriptor
        self.dims = tuple(dims) if dims is not None else GAS_DIMS
        self._rng = random.Random(seed)

    # --- Overlap detection ---

    def analyze_overlaps(self) -> list[OverlapResult]:
        """Compute pairwise overlap for every unordered pair of boxes.

        Two boxes overlap iff their intervals intersect in ALL dimensions
        simultaneously.  Boxes missing any dimension are skipped with a note.
        """
        sigs = sorted(self.descriptor.boxes.keys())
        results: list[OverlapResult] = []

        for i in range(len(sigs)):
            for j in range(i + 1, len(sigs)):
                sig_a, sig_b = sigs[i], sigs[j]
                box_a = self.descriptor.boxes[sig_a]
                box_b = self.descriptor.boxes[sig_b]

                # Both boxes must define all target dims
                missing = [d for d in self.dims if d not in box_a.dimensions or d not in box_b.dimensions]
                if missing:
                    results.append(
                        OverlapResult(
                            sig_a=sig_a,
                            sig_b=sig_b,
                            overlaps=False,
                            identical_gas_signature=False,
                            intersection_bounds=None,
                            note=f"skipped: missing dims {missing}",
                        )
                    )
                    continue

                # Check per-dimension interval overlap
                intersection: dict[str, tuple[float, float]] = {}
                overlaps = True
                for d in self.dims:
                    a_lo, a_hi = box_a.dimensions[d]
                    b_lo, b_hi = box_b.dimensions[d]
                    inter_lo = max(a_lo, b_lo)
                    inter_hi = min(a_hi, b_hi)
                    if inter_lo > inter_hi:
                        overlaps = False
                        break
                    intersection[d] = (inter_lo, inter_hi)

                # Identical gas signature: all per-dim bounds match exactly
                identical = overlaps and all(
                    box_a.dimensions[d] == box_b.dimensions[d]
                    for d in self.dims
                )

                note = ""
                if identical:
                    note = "identical gas signature — only non-gas evidence (DNA/engine state) can disambiguate"

                results.append(
                    OverlapResult(
                        sig_a=sig_a,
                        sig_b=sig_b,
                        overlaps=overlaps,
                        identical_gas_signature=identical,
                        intersection_bounds=intersection if overlaps else None,
                        note=note,
                    )
                )

        return results

    # --- Coverage-gap estimation ---

    def estimate_coverage(self) -> CoverageGapEstimate:
        """Monte Carlo sample the measurement envelope.

        Draws N random uniform points in the global plausible range and
        counts how many fall into 0, 1, or 2+ boxes.
        """
        # Build per-dim envelope from the boxes that actually define bounds.
        # Fall back to _ENVELOPE for dims not present in any box.
        dim_ranges: dict[str, tuple[float, float]] = {}
        for d in self.dims:
            lo = _ENVELOPE.get(d, (0.0, 1.0))[0]
            hi = _ENVELOPE.get(d, (0.0, 1.0))[1]
            dim_ranges[d] = (lo, hi)

        no_box = 0
        single_box = 0
        multi_box = 0
        per_box_hits: dict[str, int] = {sig: 0 for sig in self.descriptor.boxes}

        boxes_list = list(self.descriptor.boxes.items())

        for _ in range(_MONTE_CARLO_N):
            point: dict[str, float] = {}
            for d in self.dims:
                lo, hi = dim_ranges[d]
                point[d] = self._rng.uniform(lo, hi)

            containing = self._containing_boxes(point, boxes_list)

            if not containing:
                no_box += 1
            elif len(containing) == 1:
                single_box += 1
                per_box_hits[containing[0]] += 1
            else:
                multi_box += 1
                for sig in containing:
                    per_box_hits[sig] += 1

        total = _MONTE_CARLO_N
        return CoverageGapEstimate(
            total_samples=total,
            no_box_count=no_box,
            single_box_count=single_box,
            multi_box_count=multi_box,
            no_box_pct=no_box / total * 100.0,
            single_box_pct=single_box / total * 100.0,
            multi_box_pct=multi_box / total * 100.0,
            per_box_hit_counts=per_box_hits,
        )

    def _containing_boxes(
        self, point: dict[str, float], boxes: list[tuple[str, Any]]
    ) -> list[str]:
        """Return the list of box signatures that contain the point."""
        containing: list[str] = []
        for sig, box in boxes:
            inside = True
            for d in self.dims:
                if d not in box.dimensions:
                    inside = False
                    break
                lo, hi = box.dimensions[d]
                if not (lo <= point[d] <= hi):
                    inside = False
                    break
            if inside:
                containing.append(sig)
        return containing

    # --- Full analysis ---

    def run(self) -> OverlapReport:
        """Run full overlap + coverage-gap analysis."""
        sigs = sorted(self.descriptor.boxes.keys())
        pairs = self.analyze_overlaps()
        coverage = self.estimate_coverage()

        overlapping = [p for p in pairs if p.overlaps]
        identical = [p for p in overlapping if p.identical_gas_signature]

        return OverlapReport(
            module_name=self.descriptor.name,
            box_count=len(sigs),
            dims=list(self.dims),
            overlap_pairs=pairs,
            coverage=coverage,
            total_pairs=len(pairs),
            overlapping_count=len(overlapping),
            identical_count=len(identical),
        )


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------


def write_overlap_report(report: OverlapReport, output_path: Path) -> None:
    """Write a .md overlap + coverage-gap report.

    Project rule: reports are always .md — never .docx, .pdf, or other formats.
    """
    lines: list[str] = []
    lines.append("# Box Overlap & Coverage-Gap Report")
    lines.append("")
    lines.append(f"**Module:** {report.module_name}  ")
    lines.append(f"**Date:** {_today()}  ")
    lines.append(f"**Boxes:** {report.box_count} | **Dimensions:** {', '.join(report.dims)}  ")
    n = report.total_pairs
    lines.append(
        f"**Pairs analyzed:** {n} | "
        f"**Overlapping:** {report.overlapping_count} | "
        f"**Identical gas signatures:** {report.identical_count}  "
    )
    lines.append("")

    # --- Coverage gap ---
    c = report.coverage
    lines.append("## Coverage Gap (Monte Carlo)")
    lines.append("")
    lines.append(f"**Samples:** {c.total_samples:,} (seeded, reproducible)  ")
    lines.append("")
    lines.append("| Category | Count | Pct |")
    lines.append("|---|---|---|")
    lines.append(f"| No box (unclassifiable hole) | {c.no_box_count:,} | {c.no_box_pct:.1f}% |")
    lines.append(f"| Exactly one box (unambiguous) | {c.single_box_count:,} | {c.single_box_pct:.1f}% |")
    lines.append(f"| Two or more boxes (ambiguous) | {c.multi_box_count:,} | {c.multi_box_pct:.1f}% |")
    lines.append("")

    disc_ceiling = 100.0 - c.single_box_pct
    lines.append(f"**Discrimination ceiling:** {disc_ceiling:.1f}% of the measurement envelope falls into 0 or 2+ boxes — structurally unresolvable on gas chemistry alone.")
    lines.append("")

    # --- Per-box hit counts (top/bottom 5) ---
    sorted_boxes = sorted(c.per_box_hit_counts.items(), key=lambda x: x[1], reverse=True)
    lines.append("### Per-box coverage (top 10)")
    lines.append("")
    lines.append("| Box | Monte Carlo hits |")
    lines.append("|---|---|")
    for sig, count in sorted_boxes[:10]:
        lines.append(f"| {sig} | {count:,} |")
    lines.append("")

    lines.append("### Per-box coverage (bottom 10)")
    lines.append("")
    lines.append("| Box | Monte Carlo hits |")
    lines.append("|---|---|")
    for sig, count in sorted_boxes[-10:]:
        lines.append(f"| {sig} | {count:,} |")
    lines.append("")

    # --- Zero-hit boxes ---
    zero_hits = [sig for sig, count in sorted_boxes if count == 0]
    if zero_hits:
        lines.append("### Zero-coverage boxes")
        lines.append("")
        lines.append("These boxes received **zero** Monte Carlo hits — their volume in "
                     "5-D gas space may be too small to sample at N=50,000:")
        lines.append("")
        for sig in zero_hits:
            lines.append(f"- {sig}")
        lines.append("")

    # --- Overlap pairs ---
    overlapping = [p for p in report.overlap_pairs if p.overlaps]
    identical = [p for p in overlapping if p.identical_gas_signature]
    non_identical = [p for p in overlapping if not p.identical_gas_signature]

    if identical:
        lines.append("## Identical Gas Signatures (cannot separate on gas alone)")
        lines.append("")
        for p in identical:
            lines.append(f"- **{p.sig_a} ↔ {p.sig_b}**")
            if p.note:
                lines.append(f"  — {p.note}")
        lines.append("")

    if non_identical:
        lines.append("## Overlapping Box Pairs (non-identical bounds)")
        lines.append("")
        lines.append("| # | Box A | Box B | Intersection region (per dim) |")
        lines.append("|---|---|---|---|")
        for idx, p in enumerate(non_identical, 1):
            inter_str = _format_intersection(p.intersection_bounds)
            lines.append(f"| {idx} | {p.sig_a} | {p.sig_b} | {inter_str} |")
        lines.append("")

    # --- Non-overlapping count ---
    disjoint = [p for p in report.overlap_pairs if not p.overlaps]
    if disjoint:
        lines.append(f"**Disjoint pairs:** {len(disjoint)}/{report.total_pairs} "
                     f"({len(disjoint) / max(report.total_pairs, 1) * 100:.0f}%)")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Report generated by T-TH-2 box-overlap & coverage-gap analyzer.*")
    lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _format_intersection(bounds: dict[str, tuple[float, float]] | None) -> str:
    if bounds is None:
        return "—"
    parts: list[str] = []
    for d, (lo, hi) in bounds.items():
        d_short = d.replace("gas_", "")
        parts.append(f"{d_short}: [{lo}, {hi}]")
    return "<br>".join(parts)


def _today() -> str:
    from datetime import date

    return date.today().isoformat()
