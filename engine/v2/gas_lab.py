"""M2 — Gas lab: Brettschneider lambda, per-state symptom detection, dual-state delta.

R4 / L04: consumes ValidatedInput, never raw DiagnosticInput.
R10 / L08: every threshold cites source_guide provenance.
L05: analyser_lambda is raw_score for downstream gates.

Source: v2-gas-chemistry §1–§6.
Brettschneider formula: V1 verified implementation (core/bretschneider.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.v2.dna_core import DNAOutput
from engine.v2.input_model import GasRecord, ValidatedInput

# ── Brettschneider fuel constants ─────────────────────────────────────────────
# source: v2-gas-chemistry §1 — petrol H:C and O:C ratios
_HCV: float = 1.7261
_OCV: float = 0.0175

# source: Bridge Analyzers Brettschneider reference — water-gas shift constant
_K1: float = 3.5

# ── Lambda thresholds ────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2 per-state symptom detection (re-thresholded)
# source: timing_compression_forensic_2026-05-03.md — corrected from V1 values
# source: docs/master_guides/gases/master_gas_guide.md §3.1
_LAMBDA_RICH: float = 0.97
_LAMBDA_LEAN: float = 1.03

# ── HC thresholds ────────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2
# source: docs/master_guides/gases/master_gas_guide.md §6
_HC_MISFIRE_PPM_MPFI: float = 600.0
# source: docs/master_guides/gases/master_gas_guide.md §6.2 — GDI footnote
_HC_MISFIRE_PPM_GDI: float = 900.0

# ── CO thresholds ────────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2
# source: docs/master_guides/gases/master_gas_guide.md §4
_CO_HIGH_PCT: float = 3.0

# ── CO2 thresholds ───────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2
# source: docs/master_guides/gases/master_gas_guide.md §3
_CO2_LOW_PCT: float = 12.5

# ── O2 thresholds ────────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2
# source: docs/master_guides/gases/master_gas_guide.md §5
_O2_ELEVATED_PCT: float = 2.0

# ── NOx thresholds ───────────────────────────────────────────────────────────
# source: v2-gas-chemistry §2
# source: docs/master_guides/gases/master_gas_guide.md §7
_NOX_HIGH_PPM: float = 1500.0

# ── Baseline deviation ───────────────────────────────────────────────────────
# source: v2-gas-chemistry §2 — |analyser_lambda_high − target_lambda| > 0.02
# source: docs/master_guides/gases/master_gas_guide.md §3.1
_BASELINE_DEVIATION_THRESHOLD: float = 0.02

# ── Dual-state delta thresholds ──────────────────────────────────────────────
# source: v2-gas-chemistry §3 dual-state delta tags
_DELTA_CO2_IMPROVING: float = 2.0    # CO2_high − CO2_idle ≥ +2 pp
_DELTA_O2_IMPROVING: float = -0.5    # O2_high − O2_idle ≤ −0.5 pp
_DELTA_CO2_STABLE: float = 1.0       # |CO2 change| < 1 pp
_DELTA_CO2_DECLINING: float = -1.0   # CO2_high − CO2_idle ≤ −1 pp
_DELTA_O2_DECLINING: float = 1.0     # O2_high − O2_idle ≥ +1 pp


# ── Output dataclass ──────────────────────────────────────────────────────────


@dataclass(slots=True)
class GasLabOutput:
    """M2 output — gas analysis results consumed by M3 (arbitrator).

    R9: symptom IDs match schema/v2/symptoms.yaml emitted_by M2.
    L05: analyser_lambda is raw_score for downstream gate thresholds.
    """
    symptoms_idle: list[str] = field(default_factory=list)
    symptoms_high: list[str] = field(default_factory=list)
    dual_state_tag: str | None = None
    analyser_lambda_idle: float | None = None
    analyser_lambda_high: float | None = None
    baseline_deviation_high: float | None = None


# ── Public entry point ────────────────────────────────────────────────────────


def analyse_gas(
    validated_input: ValidatedInput,
    dna_output: DNAOutput,
) -> GasLabOutput:
    """Run M2 gas analysis on idle and high-idle exhaust samples.

    Args:
        validated_input: Post-VL input (R4/L04 — never raw DiagnosticInput).
        dna_output: M0 vehicle DNA profile (target_lambda_v112, target_rpm_u2).

    Returns:
        GasLabOutput with per-state symptom lists, dual-state delta tag,
        computed Brettschneider lambdas, and baseline deviation.
    """
    raw = validated_input.raw
    gas_idle = raw.gas_idle
    gas_high = raw.gas_high
    nox_suppressed = validated_input.nox_suppressed
    has_gdi = dna_output.tech_mask.get("has_gdi", False)

    symptoms_idle: list[str] = []
    symptoms_high: list[str] = []
    analyser_lambda_idle: float | None = None
    analyser_lambda_high: float | None = None

    # ── idle analysis ────────────────────────────────────────────────────
    if gas_idle is not None:
        analyser_lambda_idle = _brettschneider(gas_idle)
        symptoms_idle = _detect_gas_symptoms(
            gas_idle, analyser_lambda_idle, nox_suppressed, has_gdi=has_gdi,
        )

    # ── high-idle analysis ───────────────────────────────────────────────
    if gas_high is not None:
        analyser_lambda_high = _brettschneider(gas_high)
        symptoms_high = _detect_gas_symptoms(
            gas_high, analyser_lambda_high, nox_suppressed, has_gdi=has_gdi,
        )

    # ── dual-state delta ─────────────────────────────────────────────────
    dual_state_tag = _compute_dual_state_delta(gas_idle, gas_high)

    # ── baseline deviation ───────────────────────────────────────────────
    # source: v2-gas-chemistry §2 — |analyser_lambda_high − target_lambda| > 0.02
    baseline_deviation_high: float | None = None
    if analyser_lambda_high is not None:
        baseline_deviation_high = abs(analyser_lambda_high - dna_output.target_lambda_v112)
        if baseline_deviation_high > _BASELINE_DEVIATION_THRESHOLD:
            symptoms_high.append("SYM_BASELINE_DEVIATION")

    return GasLabOutput(
        symptoms_idle=symptoms_idle,
        symptoms_high=symptoms_high,
        dual_state_tag=dual_state_tag,
        analyser_lambda_idle=analyser_lambda_idle,
        analyser_lambda_high=analyser_lambda_high,
        baseline_deviation_high=baseline_deviation_high,
    )


# ── Brettschneider lambda ────────────────────────────────────────────────────


def _brettschneider(gas: GasRecord) -> float:
    """Compute Brettschneider lambda from exhaust gas concentrations.

    V1 verified formula from core/bretschneider.py.  All inputs in analyser
    units (%, ppm).  HC is converted to vol% internally.

    Pin test: HC=80ppm, CO=0.18%, CO2=14.6%, O2=1.8%
              → λ ≈ 1.080 (±0.002) with Hcv=1.7261, Ocv=0.0175.

    Args:
        gas: GasRecord with co_pct, hc_ppm, co2_pct, o2_pct.

    Returns:
        Computed lambda value (dimensionless, ~0.85–1.20 for petrol engines).
    """
    # source: core/bretschneider.py — V1 verified implementation
    hc_pct = gas.hc_ppm / 10000.0

    co2 = gas.co2_pct
    co = gas.co_pct
    o2 = gas.o2_pct

    if co2 == 0.0:
        co2 = 0.001

    water_gas_factor = (_HCV / 4.0) * (_K1 / (_K1 + (co / co2))) - (_OCV / 2.0)

    numerator = co2 + (co / 2.0) + o2 + (water_gas_factor * (co2 + co))
    denominator = (1.0 + (_HCV / 4.0) - (_OCV / 2.0)) * (co2 + co + hc_pct)

    return numerator / denominator if denominator != 0.0 else 0.0


# ── Per-state symptom detection ──────────────────────────────────────────────


def _detect_gas_symptoms(
    gas: GasRecord,
    lamb: float,
    nox_suppressed: bool,
    has_gdi: bool = False,
) -> list[str]:
    """Detect gas symptoms from a single exhaust sample.

    source: v2-gas-chemistry §2 per-state symptom detection table.
    source: master_gas_guide.md §6.2 — GDI HC threshold = 900 ppm.

    Args:
        gas: Gas record for a single RPM state (idle or high-idle).
        lamb: Computed Brettschneider lambda for this sample.
        nox_suppressed: True on 4-gas analysers — skips NOx checks.
        has_gdi: True for GDI engines — raises HC misfire threshold to 900 ppm.

    Returns:
        List of matching symptom IDs from schema/v2/symptoms.yaml (emitted_by: M2).
    """
    symptoms: list[str] = []

    # Lambda — source: v2-gas-chemistry §2, master_gas_guide.md §3.1
    if lamb < _LAMBDA_RICH:
        symptoms.append("SYM_LAMBDA_LOW")
    elif lamb > _LAMBDA_LEAN:
        symptoms.append("SYM_LAMBDA_HIGH")
    else:
        symptoms.append("SYM_LAMBDA_NORMAL")

    # HC — source: v2-gas-chemistry §2, master_gas_guide.md §6
    # source: master_gas_guide.md §6.2 — GDI threshold 900 ppm (wall-wetting)
    _hc_threshold = _HC_MISFIRE_PPM_GDI if has_gdi else _HC_MISFIRE_PPM_MPFI
    if gas.hc_ppm > _hc_threshold:
        symptoms.append("SYM_HC_HIGH")
    else:
        symptoms.append("SYM_HC_LOW")

    # CO — source: v2-gas-chemistry §2, master_gas_guide.md §4
    if gas.co_pct > _CO_HIGH_PCT:
        symptoms.append("SYM_CO_HIGH")

    # CO2 — source: v2-gas-chemistry §2, master_gas_guide.md §3
    if gas.co2_pct < _CO2_LOW_PCT:
        symptoms.append("SYM_CO2_LOW")
    else:
        symptoms.append("SYM_CO2_GOOD")

    # O2 — source: v2-gas-chemistry §2, master_gas_guide.md §5
    if gas.o2_pct > _O2_ELEVATED_PCT:
        symptoms.append("SYM_O2_HIGH")

    # NOx — source: v2-gas-chemistry §2, master_gas_guide.md §7
    if not nox_suppressed and gas.nox_ppm is not None and gas.nox_ppm > _NOX_HIGH_PPM:
        symptoms.append("SYM_NOX_HIGH")

    return symptoms


# ── Dual-state delta ─────────────────────────────────────────────────────────


def _compute_dual_state_delta(
    gas_idle: GasRecord | None,
    gas_high: GasRecord | None,
) -> str | None:
    """Compute dual-state delta tag comparing idle → high-idle gas changes.

    source: v2-gas-chemistry §3 dual-state delta tags.

    Args:
        gas_idle: Idle gas sample (L1).
        gas_high: High-idle gas sample (L2).

    Returns:
        One of SYM_DUAL_IMPROVING, SYM_DUAL_STABLE, SYM_DUAL_DECLINING,
        or None if either state sample is missing.
    """
    if gas_idle is None or gas_high is None:
        return None

    co2_delta = gas_high.co2_pct - gas_idle.co2_pct
    o2_delta = gas_high.o2_pct - gas_idle.o2_pct

    # improving — source: v2-gas-chemistry §3
    if co2_delta >= _DELTA_CO2_IMPROVING and o2_delta <= _DELTA_O2_IMPROVING:
        return "SYM_DUAL_IMPROVING"

    # stable — source: v2-gas-chemistry §3
    if abs(co2_delta) < _DELTA_CO2_STABLE:
        return "SYM_DUAL_STABLE"

    # declining — source: v2-gas-chemistry §3
    if co2_delta <= _DELTA_CO2_DECLINING or o2_delta >= _DELTA_O2_DECLINING:
        return "SYM_DUAL_DECLINING"

    return None
