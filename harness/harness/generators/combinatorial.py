"""Pairwise (t-wise) combinatorial corner generator for the generative test harness.

Lab-agnostic: imports no lab runtime code. Operates on a ModuleDescriptor.
For each fault box, takes every unordered pair of the box's gas dimensions and
places that pair at their four ``{min, max}`` corners while holding the other
dimensions at the box centroid. Each point carries a geometric box-membership
oracle. Then runs each point through descriptor.entry_point and checks agreement.

Catches multi-dimension interaction bugs that the per-axis boundary sweep
(T-TH-1) structurally cannot: a defect that only fires when two thresholds are
crossed together is invisible to a one-dimension-at-a-time sweep.

Pairwise (t=2) coverage is the standard t-wise reduction — C(5,2)=10 dim-pairs x
2^2=4 corners = 40 points per box, a bounded count that still exercises every
2-dimension corner interaction. Full-grid (2^5) and higher t are out of scope.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

from harness.descriptor import FaultBox, ModuleDescriptor
from harness.generators.boundary import GAS_DIMS

# Corner labels: "mn" = min bound, "mx" = max bound.
_CORNER_LABELS = ("mn", "mx")


@dataclass
class CombinatorialCase:
    """One pairwise corner test point."""

    case_id: str
    box_signature: str
    dim_pair: tuple[str, str]
    corner: tuple[str, str]  # (label_d1, label_d2), each "mn" | "mx"
    point: dict[str, float]  # gas dimension name -> value
    geometric_oracle: str  # "inside" | "outside"
    source: str  # box source citation


@dataclass
class CombinatorialReport:
    """Results of a combinatorial generator run."""

    cases: list[CombinatorialCase]
    verdicts: list[dict[str, Any]]
    passes: int
    failures: int
    summary: str


class CombinatorialGenerator:
    """Generate pairwise (t=2) corner test points for each fault box.

    For each box and each unordered pair of its gas dimensions, generates the
    4 ``{min,max} x {min,max}`` corners with the other dimensions held at the
    box centroid. ``t`` is fixed at 2 for this task; the parameter exists so a
    later task can raise it, but ``t != 2`` is rejected here as out of scope.
    """

    def __init__(self, descriptor: ModuleDescriptor, t: int = 2) -> None:
        if t != 2:
            raise ValueError(f"only pairwise (t=2) is supported; got t={t}")
        self.descriptor = descriptor
        self.t = t

    def _oracle(self, box: FaultBox, point: dict[str, float]) -> str:
        """Geometric box-membership: inside iff point lies within ALL box dims."""
        for d, (lo, hi) in box.dimensions.items():
            if d not in point:
                return "outside"
            if not (lo <= point[d] <= hi):
                return "outside"
        return "inside"

    def generate(self) -> list[CombinatorialCase]:
        """Generate all pairwise corner cases from the descriptor's box table."""
        cases: list[CombinatorialCase] = []

        for sig, box in self.descriptor.boxes.items():
            box_dims = [d for d in GAS_DIMS if d in box.dimensions]
            if len(box_dims) < 2:
                continue

            # Centroid for each gas dim (mean of min, max).
            centroid: dict[str, float] = {}
            for d in box_dims:
                lo, hi = box.dimensions[d]
                centroid[d] = (lo + hi) / 2.0

            for d1, d2 in combinations(box_dims, 2):
                d1_lo, d1_hi = box.dimensions[d1]
                d2_lo, d2_hi = box.dimensions[d2]
                bounds = {
                    "mn": {d1: d1_lo, d2: d2_lo},
                    "mx": {d1: d1_hi, d2: d2_hi},
                }

                for c1 in _CORNER_LABELS:
                    for c2 in _CORNER_LABELS:
                        point = dict(centroid)
                        point[d1] = bounds[c1][d1]
                        point[d2] = bounds[c2][d2]

                        oracle = self._oracle(box, point)

                        sig_short = sig[:18]
                        case_id = f"TH-CMB-{sig_short}-{d1}-{d2}-{c1}{c2}"

                        cases.append(
                            CombinatorialCase(
                                case_id=case_id,
                                box_signature=sig,
                                dim_pair=(d1, d2),
                                corner=(c1, c2),
                                point=point,
                                geometric_oracle=oracle,
                                source=box.source,
                            )
                        )

        return cases

    def _build_row(self, point: dict[str, float]) -> dict[str, str]:
        """Convert a gas point to a row dict for descriptor.build_args.

        Uses FieldRange type info to format ints without a decimal point,
        floats as-is — same convention as the boundary generator.
        """
        row: dict[str, str] = {}
        for dim, val in point.items():
            fld = self.descriptor.get_field(dim)
            if fld is not None and fld.type_ == "int":
                row[dim] = str(int(round(val)))
            else:
                row[dim] = str(val)
        return row

    def run(self) -> CombinatorialReport:
        """Generate cases, run each through entry_point, check the oracle."""
        cases = self.generate()
        verdicts: list[dict[str, Any]] = []
        passes = 0
        failures = 0

        for case in cases:
            row = self._build_row(case.point)

            try:
                args = self.descriptor.build_args(row)
                actual = self.descriptor.entry_point(*args)
                actual_state = actual.chemical_state.value
            except Exception as exc:
                actual_state = f"ERROR:{type(exc).__name__}"

            predicted_inside = actual_state == case.box_signature
            oracle_inside = case.geometric_oracle == "inside"
            match = predicted_inside == oracle_inside

            if match:
                passes += 1
            else:
                failures += 1

            verdicts.append(
                {
                    "case_id": case.case_id,
                    "box": case.box_signature,
                    "dim_pair": f"({case.dim_pair[0]}, {case.dim_pair[1]})",
                    "corner": f"({case.corner[0]}, {case.corner[1]})",
                    "oracle": case.geometric_oracle,
                    "actual": actual_state,
                    "match": match,
                }
            )

        total = passes + failures
        pct = (passes / total * 100) if total > 0 else 100.0

        overlap_note = (
            "\n\n**Overlap caveat:** mismatches may be caused by overlapping "
            "fault boxes (analyzed in T-TH-2). A FAIL with oracle=inside means "
            "the classifier returned a different signature for a corner "
            "geometrically inside this box — which may be correct if the corner "
            "also falls inside another box."
            if failures > 0
            else ""
        )

        summary = (
            f"**{passes}/{total}** pairwise corners match geometric oracle "
            f"({pct:.1f}%).  \n"
            f"**{failures} mismatch(es)**.{overlap_note}"
        )

        return CombinatorialReport(
            cases=cases,
            verdicts=verdicts,
            passes=passes,
            failures=failures,
            summary=summary,
        )


def write_combinatorial_report(report: CombinatorialReport, output_path: Path) -> None:
    """Write a .md combinatorial test report.

    Project rule: reports are always .md — never .docx, .pdf, or other formats.
    """
    lines: list[str] = []
    lines.append("# Combinatorial Generator Report")
    lines.append("")
    lines.append(f"**Date:** {_today()}  ")
    lines.append("**Coverage:** pairwise (t=2) corners — C(5,2) dim-pairs x 4 corners per box  ")
    lines.append(f"**Total cases:** {len(report.cases)}  ")
    lines.append(f"**PASS:** {report.passes} | **FAIL:** {report.failures}  ")
    lines.append("")
    lines.append(report.summary)
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| # | case_id | Box | Dim pair | Corner | Oracle | Actual | Match |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for i, v in enumerate(report.verdicts, 1):
        match_str = "PASS" if v["match"] else "FAIL"
        lines.append(
            f"| {i} | {v['case_id']} | {v['box']} | {v['dim_pair']} | "
            f"{v['corner']} | {v['oracle']} | {v['actual']} | {match_str} |"
        )

    lines.append("")

    failed = [v for v in report.verdicts if not v["match"]]
    if failed:
        lines.append("## Failures")
        lines.append("")
        for v in failed:
            lines.append(
                f"- **{v['case_id']}:** {v['dim_pair']} corner {v['corner']}, "
                f"oracle={v['oracle']}, actual={v['actual']}"
            )
        lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _today() -> str:
    from datetime import date

    return date.today().isoformat()
