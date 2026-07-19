"""Noise / fault-injection characterization for the generative test harness.

Lab-agnostic: imports no lab runtime code. Operates on a ModuleDescriptor.

Starting from each fault box's centroid (the most-definitely-inside point),
applies seeded random perturbation at increasing amplitude levels, runs each
perturbed point through descriptor.entry_point, and measures how the
classifier's label degrades as noise grows. Emits an .md degradation report.

This is a CHARACTERIZATION report, not a pass/fail gate (same posture as the
T-TH-2 overlap analyzer). It measures brittleness to real-world non-ideal
readings — analyzer jitter, sensor drift, sampling noise — which a clean
centroid run never exposes. It asserts no degradation threshold and must not be
wired into an inner-loop correctness gate.

"Retention" at an amplitude level = the fraction of perturbed points that still
classify as the BASELINE label (the label the unperturbed centroid produced for
that box). Retention is anchored to the observed centroid label, not the box
signature: T-TH-2 proved a centroid may already classify as a different
(overlapping) signature, so anchoring to the box signature would conflate the
overlap ceiling with noise brittleness. Anchoring to the observed baseline label
isolates the noise effect.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from harness.descriptor import ModuleDescriptor
from harness.generators.boundary import GAS_DIMS

# Amplitude sweep, expressed as a fraction of each dimension's box width.
# 0.0 is the unperturbed baseline (centroid) and is always included first.
DEFAULT_LEVELS: tuple[float, ...] = (0.0, 0.1, 0.25, 0.5, 1.0)

# Default number of perturbed draws per box per amplitude level.
DEFAULT_SAMPLES_PER_LEVEL = 100

# Default noise distribution. "uniform" draws in [-a*width, +a*width] (bounded,
# no long tail — a "within +/-X% of reading" jitter model). "gaussian" draws
# with sigma = a*width from the same seeded RNG.
DEFAULT_DISTRIBUTION = "uniform"


@dataclass
class NoiseCase:
    """One perturbed test point."""

    case_id: str
    box_signature: str
    amplitude: float  # fraction-of-width amplitude level this point was drawn at
    sample_index: int  # 0-based index within (box, amplitude)
    point: dict[str, float]  # gas dimension name -> perturbed, clamped value
    source: str  # box source citation


@dataclass
class NoiseReport:
    """Results of a noise characterization run."""

    cases: list[NoiseCase]
    baseline_labels: dict[str, str]  # box signature -> observed centroid label
    retention: dict[str, dict[float, float]]  # box -> {amplitude -> retained fraction}
    aggregate: dict[float, float]  # amplitude -> mean retention across boxes
    levels: tuple[float, ...]
    seed: int
    distribution: str
    samples_per_level: int
    summary: str


class NoiseCharacterizer:
    """Characterize classifier robustness to noise around each box centroid.

    For each box that defines all 5 gas dimensions, draws ``samples_per_level``
    perturbed points at each amplitude level, clamps them to the descriptor's
    field envelope, runs each through ``descriptor.entry_point``, and records
    the fraction that retain the box's observed baseline (centroid) label.
    """

    def __init__(
        self,
        descriptor: ModuleDescriptor,
        seed: int = 42,
        levels: tuple[float, ...] = DEFAULT_LEVELS,
        samples_per_level: int = DEFAULT_SAMPLES_PER_LEVEL,
        distribution: str = DEFAULT_DISTRIBUTION,
    ) -> None:
        if distribution not in ("uniform", "gaussian"):
            raise ValueError(f"Unknown distribution: {distribution!r}")
        self.descriptor = descriptor
        self.seed = seed
        self.levels = levels
        self.samples_per_level = samples_per_level
        self.distribution = distribution

    # -- geometry helpers ---------------------------------------------------

    def _boxes_with_all_dims(self) -> list[tuple[str, Any]]:
        """Boxes that define every gas dimension (the only ones perturbable)."""
        out: list[tuple[str, Any]] = []
        for sig, box in self.descriptor.boxes.items():
            if all(d in box.dimensions for d in GAS_DIMS):
                out.append((sig, box))
        return out

    @staticmethod
    def _centroid(box: Any) -> dict[str, float]:
        return {d: (box.dimensions[d][0] + box.dimensions[d][1]) / 2.0 for d in GAS_DIMS}

    def _clamp(self, dim: str, value: float) -> float:
        """Clamp to the descriptor's field envelope and round int dims."""
        fld = self.descriptor.get_field(dim)
        if fld is not None:
            if fld.min_ is not None and value < fld.min_:
                value = float(fld.min_)
            if fld.max_ is not None and value > fld.max_:
                value = float(fld.max_)
            if fld.type_ == "int":
                value = float(int(round(value)))
        return value

    def _perturb(
        self, rng: random.Random, centroid: dict[str, float], box: Any, amplitude: float
    ) -> dict[str, float]:
        """One perturbed, clamped point at the given amplitude."""
        point: dict[str, float] = {}
        for d in GAS_DIMS:
            lo, hi = box.dimensions[d]
            width = hi - lo
            if amplitude == 0.0 or width == 0:
                delta = 0.0
            elif self.distribution == "uniform":
                delta = rng.uniform(-amplitude * width, amplitude * width)
            else:  # gaussian
                delta = rng.gauss(0.0, amplitude * width)
            point[d] = self._clamp(d, centroid[d] + delta)
        return point

    # -- generation ---------------------------------------------------------

    def generate(self) -> list[NoiseCase]:
        """Generate all perturbed cases. Deterministic for a fixed seed.

        The RNG is advanced in a fixed order (box, level, sample, dimension) so
        the sequence of draws — and therefore every point — is reproducible.
        """
        rng = random.Random(self.seed)
        cases: list[NoiseCase] = []

        for sig, box in self._boxes_with_all_dims():
            centroid = self._centroid(box)
            for amplitude in self.levels:
                for s in range(self.samples_per_level):
                    point = self._perturb(rng, centroid, box, amplitude)
                    cases.append(
                        NoiseCase(
                            case_id=f"TH-NOI-{sig[:22]}-{amplitude}-{s}",
                            box_signature=sig,
                            amplitude=amplitude,
                            sample_index=s,
                            point=point,
                            source=box.source,
                        )
                    )
        return cases

    # -- row building (int vs float formatting, mirrors boundary.py) --------

    def _build_row(self, point: dict[str, float]) -> dict[str, str]:
        row: dict[str, str] = {}
        for dim, val in point.items():
            fld = self.descriptor.get_field(dim)
            if fld is not None and fld.type_ == "int":
                row[dim] = str(int(round(val)))
            else:
                row[dim] = str(val)
        return row

    def _classify(self, point: dict[str, float]) -> str:
        """Run a point through the live entry_point; "ERROR:<Type>" on raise."""
        row = self._build_row(point)
        try:
            args = self.descriptor.build_args(row)
            actual = self.descriptor.entry_point(*args)
            return actual.chemical_state.value
        except Exception as exc:  # noqa: BLE001 — surface as a non-retained label
            return f"ERROR:{type(exc).__name__}"

    # -- run ----------------------------------------------------------------

    def run(self) -> NoiseReport:
        """Generate, classify, and compute the retention curve."""
        cases = self.generate()

        # Baseline label per box = classification of its unperturbed centroid.
        baseline_labels: dict[str, str] = {}
        for sig, box in self._boxes_with_all_dims():
            baseline_labels[sig] = self._classify(self._centroid(box))

        # Tally retained samples per (box, amplitude).
        retained: dict[str, dict[float, int]] = {}
        total: dict[str, dict[float, int]] = {}
        for case in cases:
            sig = case.box_signature
            amp = case.amplitude
            retained.setdefault(sig, {}).setdefault(amp, 0)
            total.setdefault(sig, {}).setdefault(amp, 0)
            total[sig][amp] += 1
            if self._classify(case.point) == baseline_labels[sig]:
                retained[sig][amp] += 1

        retention: dict[str, dict[float, float]] = {}
        for sig in retained:
            retention[sig] = {
                amp: (retained[sig][amp] / total[sig][amp] if total[sig][amp] else 1.0)
                for amp in self.levels
            }

        # Aggregate = mean retention across boxes, per amplitude.
        aggregate: dict[float, float] = {}
        n_boxes = len(retention)
        for amp in self.levels:
            if n_boxes:
                aggregate[amp] = sum(retention[s][amp] for s in retention) / n_boxes
            else:
                aggregate[amp] = 1.0

        summary = self._summarize(retention, aggregate, baseline_labels)

        return NoiseReport(
            cases=cases,
            baseline_labels=baseline_labels,
            retention=retention,
            aggregate=aggregate,
            levels=self.levels,
            seed=self.seed,
            distribution=self.distribution,
            samples_per_level=self.samples_per_level,
            summary=summary,
        )

    def _summarize(
        self,
        retention: dict[str, dict[float, float]],
        aggregate: dict[float, float],
        baseline_labels: dict[str, str],
    ) -> str:
        n = len(retention)
        last = self.levels[-1]
        mean_last = aggregate.get(last, 1.0) * 100
        # Overlap artifacts: centroid whose observed label != its box signature.
        artifacts = [s for s, lbl in baseline_labels.items() if lbl != s]
        artifact_note = (
            f"  \n**{len(artifacts)} box(es)** classify their own centroid as a "
            f"different signature (overlap artifact — see "
            f"`T-TH-2_overlap_report.md`); retention is still measured against "
            f"the observed baseline label."
            if artifacts
            else ""
        )
        return (
            f"Characterization of **{n} box(es)** across amplitude levels "
            f"{list(self.levels)} ({self.distribution}, seed={self.seed}, "
            f"{self.samples_per_level} samples/level).  \n"
            f"Mean retention at amplitude {last}: **{mean_last:.1f}%**.{artifact_note}"
        )


def write_noise_report(report: NoiseReport, output_path: Path) -> None:
    """Write a .md noise characterization report.

    Project rule: reports are always .md — never .docx, .pdf, or other formats.
    """
    BRITTLE_AMP = 0.25
    BRITTLE_THRESHOLD = 0.5

    lines: list[str] = []
    lines.append("# Noise Characterization Report")
    lines.append("")
    lines.append(f"**Date:** {_today()}  ")
    lines.append(f"**Seed:** {report.seed}  ")
    lines.append(f"**Distribution:** {report.distribution}  ")
    lines.append(f"**Amplitude levels (fraction of box width):** {list(report.levels)}  ")
    lines.append(f"**Samples per level:** {report.samples_per_level}  ")
    lines.append(f"**Boxes characterized:** {len(report.retention)}  ")
    lines.append("")
    lines.append(
        "> **Characterization, not a gate.** This report measures how far a "
        "reading can drift from a box centroid before the classifier changes "
        "its label. No degradation threshold is asserted. Retention is measured "
        "against each box's *observed centroid label* (not its signature) so the "
        "overlap ceiling (T-TH-2) is not conflated with noise brittleness."
    )
    lines.append("")
    lines.append(report.summary)
    lines.append("")

    # --- Aggregate degradation curve ---
    lines.append("## Aggregate degradation curve")
    lines.append("")
    lines.append("| Amplitude | Mean retention % | Boxes fully retained | Boxes fully collapsed |")
    lines.append("|---|---|---|---|")
    for amp in report.levels:
        fully_retained = sum(1 for s in report.retention if report.retention[s][amp] >= 0.999)
        fully_collapsed = sum(1 for s in report.retention if report.retention[s][amp] <= 0.001)
        lines.append(
            f"| {amp} | {report.aggregate[amp] * 100:.1f} | "
            f"{fully_retained} | {fully_collapsed} |"
        )
    lines.append("")

    # --- Per-box retention table ---
    lines.append("## Per-box retention")
    lines.append("")
    header = "| Box | Baseline label | " + " | ".join(f"a={a}" for a in report.levels) + " | brittle? |"
    sep = "|---|---|" + "---|" * len(report.levels) + "---|"
    lines.append(header)
    lines.append(sep)
    for sig in sorted(report.retention):
        curve = report.retention[sig]
        base = report.baseline_labels.get(sig, "")
        base_cell = base if base == sig else f"{base} ⚠"
        brittle = curve.get(BRITTLE_AMP, 1.0) < BRITTLE_THRESHOLD
        cells = " | ".join(f"{curve[a] * 100:.0f}%" for a in report.levels)
        lines.append(f"| {sig} | {base_cell} | {cells} | {'yes' if brittle else ''} |")
    lines.append("")

    # --- Brittle-box callout ---
    brittle_boxes = [
        sig
        for sig in report.retention
        if report.retention[sig].get(BRITTLE_AMP, 1.0) < BRITTLE_THRESHOLD
    ]
    brittle_boxes.sort(key=lambda s: report.retention[s].get(BRITTLE_AMP, 1.0))
    if brittle_boxes:
        lines.append(
            f"## Brittle boxes (retention < {int(BRITTLE_THRESHOLD * 100)}% at "
            f"amplitude {BRITTLE_AMP})"
        )
        lines.append("")
        lines.append(
            "These signatures lose their baseline label fastest under noise — "
            "the least field margin. Source citations let the architect target "
            "wiki/box refinement."
        )
        lines.append("")
        for sig in brittle_boxes:
            ret = report.retention[sig].get(BRITTLE_AMP, 1.0) * 100
            # source pulled from the cases (all share the box source)
            src = next((c.source for c in report.cases if c.box_signature == sig), "")
            lines.append(f"- **{sig}** — {ret:.0f}% retained at a={BRITTLE_AMP}  \n  _{src}_")
        lines.append("")

    # --- Overlap caveat ---
    artifacts = [s for s, lbl in report.baseline_labels.items() if lbl != s]
    if artifacts:
        lines.append("## Overlap caveat")
        lines.append("")
        lines.append(
            "The following boxes classify their own centroid as a *different* "
            "signature. This is an overlap artifact (see "
            "`T-TH-2_overlap_report.md`), not a noise finding. Retention for "
            "these boxes is measured against the observed baseline label, marked "
            "⚠ in the per-box table:"
        )
        lines.append("")
        for sig in sorted(artifacts):
            lines.append(f"- **{sig}** → centroid classifies as `{report.baseline_labels[sig]}`")
        lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _today() -> str:
    from datetime import date

    return date.today().isoformat()
