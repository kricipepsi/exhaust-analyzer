"""Boundary / edge-point generator for the generative test harness.

Lab-agnostic: imports no lab runtime code. Operates on a ModuleDescriptor.
For each fault box and each gas dimension, generates six test points
(min-eps, min, min+eps, max-eps, max, max+eps) with a geometric
box-membership oracle, then runs each through descriptor.entry_point and
checks agreement.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harness.descriptor import ModuleDescriptor

# Per-dimension default epsilon values.
# gas_hc / gas_nox are int; smallest integer step = 1.
# gas_co / gas_co2 / gas_o2 are float; 0.01 vol% is the measurement resolution.
DEFAULT_EPS: dict[str, float] = {
    "gas_hc": 1.0,
    "gas_co": 0.01,
    "gas_co2": 0.01,
    "gas_o2": 0.01,
    "gas_nox": 1.0,
}

GAS_DIMS = ("gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox")
POSITIONS = ("min-eps", "min", "min+eps", "max-eps", "max", "max+eps")


@dataclass
class BoundaryCase:
    """One boundary test point."""

    case_id: str
    box_signature: str
    dim_name: str
    position: str  # min-eps | min | min+eps | max-eps | max | max+eps
    point: dict[str, float]  # gas dimension name → value
    geometric_oracle: str  # "inside" | "outside"
    source: str  # box source citation


@dataclass
class BoundaryReport:
    """Results of a boundary generator run."""

    cases: list[BoundaryCase]
    verdicts: list[dict[str, Any]]
    passes: int
    failures: int
    summary: str


class BoundaryGenerator:
    """Generate boundary/edge test points for each dimension of each fault box.

    For each box and each of the 5 gas dimensions, generates 6 points
    (min-eps, min, min+eps, max-eps, max, max+eps).  Non-target dimensions
    are held at the box centroid — the most-definitely-inside point — so
    boundary cases are as unambiguous as possible without overlap analysis.
    """

    def __init__(
        self,
        descriptor: ModuleDescriptor,
        eps: dict[str, float] | None = None,
    ) -> None:
        self.descriptor = descriptor
        self.eps = eps or dict(DEFAULT_EPS)

    def generate(self) -> list[BoundaryCase]:
        """Generate all boundary test cases from the descriptor's box table."""
        cases: list[BoundaryCase] = []

        for sig, box in self.descriptor.boxes.items():
            # Which gas dims does this box define?
            box_dims = [d for d in GAS_DIMS if d in box.dimensions]
            if not box_dims:
                continue

            # Centroid for each gas dim (mean of min, max)
            centroid: dict[str, float] = {}
            for d in box_dims:
                lo, hi = box.dimensions[d]
                centroid[d] = (lo + hi) / 2.0

            for dim in box_dims:
                lo, hi = box.dimensions[dim]
                eps = self.eps.get(dim, 1.0)

                positions: dict[str, float] = {
                    "min-eps": lo - eps,
                    "min": float(lo),
                    "min+eps": lo + eps,
                    "max-eps": hi - eps,
                    "max": float(hi),
                    "max+eps": hi + eps,
                }

                for pos_label, pos_val in positions.items():
                    # Build the gas point: target dim at boundary value,
                    # all other dims at centroid.
                    point = dict(centroid)
                    point[dim] = pos_val

                    # Geometric oracle: is this point inside all box dimensions?
                    inside = True
                    for d in box_dims:
                        blo, bhi = box.dimensions[d]
                        if not (blo <= point[d] <= bhi):
                            inside = False
                            break
                    oracle = "inside" if inside else "outside"

                    # Truncate signature for case_id length
                    sig_short = sig[:22]
                    case_id = f"TH-BND-{sig_short}-{dim}-{pos_label}"

                    cases.append(
                        BoundaryCase(
                            case_id=case_id,
                            box_signature=sig,
                            dim_name=dim,
                            position=pos_label,
                            point=point,
                            geometric_oracle=oracle,
                            source=box.source,
                        )
                    )

        return cases

    def _build_row(self, point: dict[str, float]) -> dict[str, str]:
        """Convert a gas point to a row dict for descriptor.build_args.

        Uses FieldRange type info from the descriptor to format values
        correctly (ints without decimal point, floats as-is).
        """
        row: dict[str, str] = {}
        for dim, val in point.items():
            fld = self.descriptor.get_field(dim)
            if fld is not None and fld.type_ == "int":
                row[dim] = str(int(round(val)))
            else:
                row[dim] = str(val)
        return row

    def run(self) -> BoundaryReport:
        """Generate boundary cases, run through descriptor.entry_point, check oracle.

        Returns a BoundaryReport with per-case verdicts.
        """
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
                    "dim": case.dim_name,
                    "position": case.position,
                    "oracle": case.geometric_oracle,
                    "actual": actual_state,
                    "match": match,
                }
            )

        total = passes + failures
        pct = (passes / total * 100) if total > 0 else 100.0

        overlap_note = (
            "\n\n**Overlap caveat:** mismatches may be caused by overlapping "
            "fault boxes (to be analyzed in T-TH-2). A FAIL with oracle=inside "
            "means the classifier returned a different signature for a point "
            "geometrically inside this box — which may be correct if the point "
            "also falls inside another box."
            if failures > 0
            else ""
        )

        summary = (
            f"**{passes}/{total}** boundary points match geometric oracle "
            f"({pct:.1f}%).  \n"
            f"**{failures} mismatch(es)**.{overlap_note}"
        )

        return BoundaryReport(
            cases=cases,
            verdicts=verdicts,
            passes=passes,
            failures=failures,
            summary=summary,
        )


def write_boundary_report(report: BoundaryReport, output_path: Path) -> None:
    """Write a .md boundary test report.

    Project rule: reports are always .md — never .docx, .pdf, or other formats.
    """
    lines: list[str] = []
    lines.append("# Boundary Generator Report")
    lines.append("")
    lines.append(f"**Date:** {_today()}  ")
    lines.append(f"**Total cases:** {len(report.cases)}  ")
    lines.append(f"**PASS:** {report.passes} | **FAIL:** {report.failures}  ")
    lines.append("")
    lines.append(report.summary)
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append(
        "| # | case_id | Box | Dim | Position | Oracle | Actual | Match |"
    )
    lines.append(
        "|---|---|---|---|---|---|---|---|"
    )

    for i, v in enumerate(report.verdicts, 1):
        match_str = "PASS" if v["match"] else "FAIL"
        lines.append(
            f"| {i} | {v['case_id']} | {v['box']} | {v['dim']} | "
            f"{v['position']} | {v['oracle']} | {v['actual']} | {match_str} |"
        )

    lines.append("")

    failed = [v for v in report.verdicts if not v["match"]]
    if failed:
        lines.append("## Failures")
        lines.append("")
        for v in failed:
            lines.append(
                f"- **{v['case_id']}:** oracle={v['oracle']}, "
                f"actual={v['actual']}"
            )
        lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _today() -> str:
    from datetime import date

    return date.today().isoformat()
