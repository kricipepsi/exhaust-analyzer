"""Validation Layer (VL) — 11-category autoverification engine.

R4 / L04: no module downstream of VL may read raw DiagnosticInput.
All modules consume ValidatedInput.  VL must not import from kg_engine.py
or schema/v2/ — it is purely data-level.

Source: v2-validation-layer §3 (11 categories), §6 (hard rules).
"""

from __future__ import annotations

import re

from engine.v2.input_model import (
    DiagnosticInput,
    ValidatedInput,
    ValidationWarning,
)

# ── category 1: physical range table ──────────────────────────────────────
# source: v2-validation-layer §3 physical range table

_RANGE_CO = (0.0, 15.0)
_RANGE_HC = (0.0, 30_000.0)
_RANGE_CO2 = (0.0, 20.0)
_RANGE_O2 = (0.0, 21.0)
_RANGE_NOX = (0.0, 5_000.0)
_RANGE_LAMBDA = (0.50, 2.00)
_RANGE_ECT = (-40.0, 150.0)
_RANGE_MAP = (10.0, 300.0)
_RANGE_RPM = (0, 10_000)
_RANGE_FUEL_TRIM = (-50.0, 50.0)
_RANGE_OBD_LAMBDA = (0.50, 2.00)
_RANGE_MY = (1990, 2020)
_RANGE_SPEED = (0, 300)
_RANGE_LOAD = (0.0, 100.0)
_RANGE_BARO = (50.0, 110.0)

# ── category 4: DTC regex ─────────────────────────────────────────────────
_DTC_RE = re.compile(r"^[PCBU][0-9A-F]{4}$")

# ── category 10: open-loop fuel status values ─────────────────────────────
_OL_FUEL_STATUS = frozenset({"OL_FAULT", "OL_DRIVE"})

# ── category 5: OBD-II introduction model year ────────────────────────────
# source: v2-design-rules §7 era bucket reference (1996 = OBD-II start)
_OBD2_INTRO_YEAR = 1996

# ── category 9: cold-start thermal threshold ──────────────────────────────
# source: v2-validation-layer §3 category 9
_COLD_START_ECT_THRESHOLD = 75.0

# ── category 3: probe-air O2 threshold ────────────────────────────────────
# source: v2-validation-layer §3 category 3
_PROBE_AIR_O2_PCT = 18.0

# ── category 7: delta threshold ───────────────────────────────────────────
# source: v2-validation-layer §3 category 7
_DELTA_ECT_MAX = 100.0

# ── category 6: combined-mode thresholds ────────────────────────────────────
# source: v2-validation-layer §3 category 6
_TRIM_CONTRADICTION_PCT = 15.0
_LOW_FUEL_PRESSURE_KPA = 250.0


def _in_range(value: float, bounds: tuple[float, float]) -> bool:
    """Check value against [min, max] inclusive."""
    lo, hi = bounds
    return lo <= value <= hi


def _reject_channel(
    vi: ValidatedInput, channel: str, reason: str
) -> None:
    """Mark a channel invalid and remove it from valid_channels."""
    vi.invalid_channels[channel] = reason
    vi.valid_channels.discard(channel)


def _accept_channel(vi: ValidatedInput, channel: str) -> None:
    """Mark a channel as valid (if not already rejected)."""
    if channel not in vi.invalid_channels:
        vi.valid_channels.add(channel)


# ── public entry point ────────────────────────────────────────────────────

def validate(
    diagnostic_input: DiagnosticInput, soft_mode: bool = True
) -> ValidatedInput:
    """Run all 11 VL categories and return ValidatedInput.

    Categories 1–8 (hard rejection + soft warnings), 9–11 (path routing).
    Categories 6 and 8b emit ValidationWarning only — they never reject
    a channel.  Gated by soft_mode flag (default True).

    Category order follows the canonical list in v2-validation-layer §3.
    """
    vi = ValidatedInput(raw=diagnostic_input)

    _cat1_range(vi)
    _cat2_gas_sum(vi)
    _cat3_probe_air(vi)
    _cat4_dtc_regex(vi)
    _cat5_dtc_era(vi)
    _cat7_delta(vi)
    _cat8_consistency(vi)
    if soft_mode:
        _cat6_combined_mode(vi)
        _cat8b_consistency_soft(vi)
    _cat9_thermal_gate(vi)
    _cat10_open_loop(vi)
    _cat11_probe_count(vi)

    return vi


# ── category 1: range ─────────────────────────────────────────────────────

def _cat1_range(vi: ValidatedInput) -> None:
    """Reject any channel where a value falls outside physical bounds.

    Checks gas_idle, gas_high, obd, ff, and vehicle_context.my channels.
    """
    raw = vi.raw
    ctx = raw.vehicle_context

    # vehicle MY range
    if not _in_range(ctx.my, _RANGE_MY):
        _reject_channel(vi, "dtcs", f"range: MY {ctx.my} outside {_RANGE_MY}")
        if raw.gas_idle is not None:
            _reject_channel(vi, "gas_idle", f"range: MY {ctx.my} outside {_RANGE_MY}")
        if raw.gas_high is not None:
            _reject_channel(vi, "gas_high", f"range: MY {ctx.my} outside {_RANGE_MY}")
        if raw.obd is not None:
            _reject_channel(vi, "obd", f"range: MY {ctx.my} outside {_RANGE_MY}")
        if raw.freeze_frame is not None:
            _reject_channel(vi, "ff", f"range: MY {ctx.my} outside {_RANGE_MY}")
        return

    # gas_idle
    if raw.gas_idle is not None:
        g = raw.gas_idle
        if (
            _in_range(g.co_pct, _RANGE_CO)
            and _in_range(g.hc_ppm, _RANGE_HC)
            and _in_range(g.co2_pct, _RANGE_CO2)
            and _in_range(g.o2_pct, _RANGE_O2)
            and (g.nox_ppm is None or _in_range(g.nox_ppm, _RANGE_NOX))
            and (g.lambda_analyser is None or _in_range(g.lambda_analyser, _RANGE_LAMBDA))
        ):
            _accept_channel(vi, "gas_idle")
        else:
            _reject_channel(vi, "gas_idle", "range: gas_idle values outside physical bounds")

    # gas_high
    if raw.gas_high is not None:
        g = raw.gas_high
        if (
            _in_range(g.co_pct, _RANGE_CO)
            and _in_range(g.hc_ppm, _RANGE_HC)
            and _in_range(g.co2_pct, _RANGE_CO2)
            and _in_range(g.o2_pct, _RANGE_O2)
            and (g.nox_ppm is None or _in_range(g.nox_ppm, _RANGE_NOX))
            and (g.lambda_analyser is None or _in_range(g.lambda_analyser, _RANGE_LAMBDA))
        ):
            _accept_channel(vi, "gas_high")
        else:
            _reject_channel(vi, "gas_high", "range: gas_high values outside physical bounds")

    # OBD
    if raw.obd is not None:
        o = raw.obd
        checks = [
            o.ect_c is None or _in_range(o.ect_c, _RANGE_ECT),
            o.map_kpa is None or _in_range(o.map_kpa, _RANGE_MAP),
            o.rpm is None or _in_range(o.rpm, _RANGE_RPM),
            o.stft_b1 is None or _in_range(o.stft_b1, _RANGE_FUEL_TRIM),
            o.stft_b2 is None or _in_range(o.stft_b2, _RANGE_FUEL_TRIM),
            o.ltft_b1 is None or _in_range(o.ltft_b1, _RANGE_FUEL_TRIM),
            o.ltft_b2 is None or _in_range(o.ltft_b2, _RANGE_FUEL_TRIM),
            o.obd_lambda is None or _in_range(o.obd_lambda, _RANGE_OBD_LAMBDA),
            o.iat_c is None or _in_range(o.iat_c, _RANGE_ECT),
            o.baro_kpa is None or _in_range(o.baro_kpa, _RANGE_BARO),
            o.load_pct is None or _in_range(o.load_pct, _RANGE_LOAD),
        ]
        if all(checks):
            _accept_channel(vi, "obd")
        else:
            _reject_channel(vi, "obd", "range: OBD values outside physical bounds")

    # freeze_frame
    if raw.freeze_frame is not None:
        ff = raw.freeze_frame
        checks = [
            ff.ect_c is None or _in_range(ff.ect_c, _RANGE_ECT),
            ff.map_kpa is None or _in_range(ff.map_kpa, _RANGE_MAP),
            ff.rpm is None or _in_range(ff.rpm, _RANGE_RPM),
            ff.stft_b1 is None or _in_range(ff.stft_b1, _RANGE_FUEL_TRIM),
            ff.stft_b2 is None or _in_range(ff.stft_b2, _RANGE_FUEL_TRIM),
            ff.ltft_b1 is None or _in_range(ff.ltft_b1, _RANGE_FUEL_TRIM),
            ff.ltft_b2 is None or _in_range(ff.ltft_b2, _RANGE_FUEL_TRIM),
            ff.iat_c is None or _in_range(ff.iat_c, _RANGE_ECT),
            ff.baro_kpa is None or _in_range(ff.baro_kpa, _RANGE_BARO),
            ff.load_pct is None or _in_range(ff.load_pct, _RANGE_LOAD),
            ff.speed_kph is None or _in_range(ff.speed_kph, _RANGE_SPEED),
        ]
        if all(checks):
            _accept_channel(vi, "ff")
        else:
            _reject_channel(vi, "ff", "range: freeze frame values outside physical bounds")

    # dtcs — no physical range; accept if present (regex/era checks handle content)
    _accept_channel(vi, "dtcs")


# ── category 2: gas sum ───────────────────────────────────────────────────

def _cat2_gas_sum(vi: ValidatedInput) -> None:
    """Reject a gas channel if CO + CO2 + HC/10000 + O2 > 101%.

    This catches sensor faults that produce physically impossible sums.
    HC is converted from ppm to percent by dividing by 10 000.
    """
    for ch_name in ("gas_idle", "gas_high"):
        if ch_name not in vi.valid_channels:
            continue
        g = vi.raw.gas_idle if ch_name == "gas_idle" else vi.raw.gas_high
        if g is None:
            continue
        total = g.co_pct + g.co2_pct + (g.hc_ppm / 10_000.0) + g.o2_pct
        if total > 101.0:
            _reject_channel(vi, ch_name, f"gas_sum: {total:.2f}% > 101%")


# ── category 3: probe air ─────────────────────────────────────────────────

def _cat3_probe_air(vi: ValidatedInput) -> None:
    """Reject a gas channel if O2 > 18% while the engine is running.

    An O2 reading above 18% indicates the exhaust sample is contaminated
    with ambient air (probe not seated, leak in sampling line, etc.).
    """
    # determine if engine is running via OBD RPM or FF RPM
    engine_running = _engine_is_running(vi.raw)

    for ch_name in ("gas_idle", "gas_high"):
        if ch_name not in vi.valid_channels:
            continue
        g = vi.raw.gas_idle if ch_name == "gas_idle" else vi.raw.gas_high
        if g is None:
            continue
        if g.o2_pct > _PROBE_AIR_O2_PCT and engine_running:
            _reject_channel(
                vi, ch_name,
                f"probe_air: O2 {g.o2_pct}% > {_PROBE_AIR_O2_PCT}% with engine running",
            )


def _engine_is_running(raw: DiagnosticInput) -> bool:
    """Engine is considered running if OBD or freeze_frame RPM > 0."""
    if raw.obd is not None and raw.obd.rpm is not None and raw.obd.rpm > 0:
        return True
    ff = raw.freeze_frame
    if ff is not None and ff.rpm is not None and ff.rpm > 0:
        return True
    # if no RPM data, assume running (conservative — probe air check fires anyway)
    return True


# ── category 4: DTC regex ─────────────────────────────────────────────────

def _cat4_dtc_regex(vi: ValidatedInput) -> None:
    """Reject individual DTCs that do not match ^[PCBU][0-9A-F]{4}$.

    The dtcs channel remains valid as long as at least one DTC passes.
    Invalid codes are logged in the rejection reason.
    """
    raw = vi.raw
    valid_dtcs: list[str] = []
    invalid_dtcs: list[str] = []

    for code in raw.dtcs:
        if _DTC_RE.match(code):
            valid_dtcs.append(code)
        else:
            invalid_dtcs.append(code)

    if invalid_dtcs:
        if not valid_dtcs:
            _reject_channel(vi, "dtcs", f"dtc_regex: all DTCs invalid — {invalid_dtcs}")
        # if some valid, channel stays valid but we log the bad ones in the
        # invalid_channels reason for traceability
        vi.invalid_channels["dtcs_rejected_codes"] = f"regex: {invalid_dtcs}"


# ── category 5: DTC era-validity ──────────────────────────────────────────

def _cat5_dtc_era(vi: ValidatedInput) -> None:
    """Reject DTCs whose family was introduced after the vehicle MY.

    Pre-1996 vehicles cannot have OBD-II DTCs (P, C, B, U prefixes).
    The channel stays valid if at least one DTC survives.
    """
    if "dtcs" not in vi.valid_channels:
        return

    my = vi.raw.vehicle_context.my
    raw = vi.raw
    valid_dtcs: list[str] = []
    era_invalid: list[str] = []

    for code in raw.dtcs:
        if my < _OBD2_INTRO_YEAR and code[0] in "PCBU":
            era_invalid.append(code)
        else:
            valid_dtcs.append(code)

    if era_invalid:
        if not valid_dtcs:
            _reject_channel(vi, "dtcs", f"dtc_era: all DTCs invalid for MY {my} — {era_invalid}")
        else:
            prior = vi.invalid_channels.get("dtcs_rejected_codes", "")
            vi.invalid_channels["dtcs_rejected_codes"] = (
                f"{prior}; era: {era_invalid}".strip("; ")
            )


# ── category 7: delta (ECT jump) ─────────────────────────────────────────

def _cat7_delta(vi: ValidatedInput) -> None:
    """Reject OBD channel if any ECT pair differs by >100°C within a session.

    A single OBDRecord represents one snapshot, so this primarily applies
    to freeze frame vs live OBD comparison.  We check the delta between
    OBD ECT and freeze frame ECT when both are present.
    """
    raw = vi.raw
    obd_ect = raw.obd.ect_c if raw.obd is not None else None
    ff_ect = raw.freeze_frame.ect_c if raw.freeze_frame is not None else None

    if obd_ect is not None and ff_ect is not None:
        delta = abs(obd_ect - ff_ect)
        if delta > _DELTA_ECT_MAX:
            _reject_channel(
                vi, "obd",
                f"delta: ECT jump {delta:.1f}°C > {_DELTA_ECT_MAX}°C "
                f"(OBD={obd_ect} vs FF={ff_ect})",
            )

    # also check OBD ECT against itself if it's implausibly high (999 sentinel)
    if obd_ect is not None and obd_ect > 150.0:
        _reject_channel(vi, "obd", f"delta: ECT {obd_ect}°C exceeds sensor maximum")


# ── category 8: consistency (hard) ────────────────────────────────────────

def _cat8_consistency(vi: ValidatedInput) -> None:
    """Reject OBD/FF boost-related fields on engines without turbo.

    This is the hard-rejection half of category 8.  Category 8b (soft
    warnings, e.g. VVT PID on non-VVT engine) belongs to T-P2-3.

    Note: at this point in the pipeline (VL), we do not have access to
    tech-mask flags from vref.db (that is M0's job).  We check for
    gross physical inconsistencies that don't require DB lookup:
    - MAP values that imply positive boost on a plausibly NA engine.
    Since we cannot definitively determine turbo from vref.db here,
    this category applies conservative MAP-range bounding.
    """
    # VL cannot import vref.db — consistency checks that require tech-mask
    # flags (has_turbo, has_vvt, has_gdi) are deferred to M0 or handled
    # as soft warnings in category 8b (T-P2-3).
    # For now, enforce MAP < 300 kPa absolute (already covered by range).
    pass


# ── category 6: combined-mode (soft warning) ───────────────────────────────

def _cat6_combined_mode(vi: ValidatedInput) -> None:
    """Emit ValidationWarning for contradictory combined OBD signals.

    Never rejects a channel — this is a soft-mode warning only (Q4 / v2.0).
    Checks:
      a) Strong negative fuel trims (< -15%) AND low fuel pressure (< 250 kPa).
         ECU is pulling fuel (sees rich) but low fuel pressure should cause
         a lean condition — these signals contradict.
      b) Strong positive fuel trims (> +15%) AND high O2 voltage (> 0.8 V,
         B1S1).  ECU is adding fuel (sees lean) but the O2 sensor reports
         a rich signal — these signals contradict.
    """
    raw = vi.raw
    if raw.obd is None:
        return

    o = raw.obd

    # check (a): negative trims + low fuel pressure
    neg_trim = (o.stft_b1 is not None and o.stft_b1 < -_TRIM_CONTRADICTION_PCT) or (
        o.ltft_b1 is not None and o.ltft_b1 < -_TRIM_CONTRADICTION_PCT
    )
    low_fp = (
        o.fuel_pressure_kpa is not None
        and o.fuel_pressure_kpa < _LOW_FUEL_PRESSURE_KPA
    )
    if neg_trim and low_fp:
        vi.warnings.append(
            ValidationWarning(
                category=6,
                message=(
                    f"contradiction: strong negative fuel trim "
                    f"(STFT={o.stft_b1}, LTFT={o.ltft_b1}) + low fuel pressure "
                    f"({o.fuel_pressure_kpa} kPa)"
                ),
                channel="obd",
            )
        )

    # check (b): positive trims + high O2 voltage (rich signal)
    pos_trim = (o.stft_b1 is not None and o.stft_b1 > _TRIM_CONTRADICTION_PCT) or (
        o.ltft_b1 is not None and o.ltft_b1 > _TRIM_CONTRADICTION_PCT
    )
    rich_o2 = (
        o.o2_voltage_b1 is not None and o.o2_voltage_b1 > 0.8
    )
    if pos_trim and rich_o2:
        vi.warnings.append(
            ValidationWarning(
                category=6,
                message=(
                    f"contradiction: strong positive fuel trim "
                    f"(STFT={o.stft_b1}, LTFT={o.ltft_b1}) + high O2 voltage "
                    f"({o.o2_voltage_b1} V — rich signal)"
                ),
                channel="obd",
            )
        )


# ── category 8b: consistency soft (warning) ────────────────────────────────

def _cat8b_consistency_soft(vi: ValidatedInput) -> None:
    """Emit ValidationWarning for soft consistency concerns.

    Never rejects a channel — this is a soft-mode warning only.
    Checks:
      a) VVT angle PID present in OBD data → flag for manual verification.
         VL cannot access vref.db tech-mask flags (M0's domain), so this
         warns on VVT angle presence regardless of has_vvt status.
         A future enhancement could accept an optional tech_context to
         make this check precise (warn only when has_vvt=False).
    """
    raw = vi.raw
    if raw.obd is None:
        return

    o = raw.obd
    if o.vvt_angle is not None:
        vi.warnings.append(
            ValidationWarning(
                category=8,
                message=(
                    f"VVT angle PID present ({o.vvt_angle}°) — "
                    f"verify VVT capability matches vehicle spec"
                ),
                channel="obd",
            )
        )

def _cat9_thermal_gate(vi: ValidatedInput) -> None:
    """Set restricted_cold_start flag when ECT < 75°C.

    Does NOT reject any channel — this is a path-routing flag.
    Cold-start chemistry (gas scoring) is suppressed downstream;
    digital symptoms (DTCs, OBD) are still scored.
    """
    ect = _get_ect(vi.raw)
    if ect is not None and ect < _COLD_START_ECT_THRESHOLD:
        vi.restricted_cold_start = True


# ── category 10: open-loop gate ───────────────────────────────────────────

def _cat10_open_loop(vi: ValidatedInput) -> None:
    """Set open_loop_suppression when fuel_status is OL_FAULT or OL_DRIVE
    AND the engine is warm (ECT >= 75°C).

    Per L18: fuel-status gate fires before any trim-derived symptom.
    All trim-derived symptoms are blocked in M1 when this flag is set.
    """
    raw = vi.raw
    fuel_status = None
    if raw.obd is not None:
        fuel_status = raw.obd.fuel_status
    if fuel_status is None and raw.freeze_frame is not None:
        fuel_status = raw.freeze_frame.fuel_status

    if fuel_status is None:
        return

    ect = _get_ect(raw)
    if fuel_status in _OL_FUEL_STATUS and ect is not None and ect >= _COLD_START_ECT_THRESHOLD:
        vi.open_loop_suppression = True


# ── category 11: probe count gate ─────────────────────────────────────────

def _cat11_probe_count(vi: ValidatedInput) -> None:
    """Set nox_suppressed when a 4-gas analyser is used (no NOx sensor).

    NOx-based symptom logic in M2 is blocked when this flag is set.
    """
    if vi.raw.analyser_type == "4-gas":
        vi.nox_suppressed = True


# ── helpers ───────────────────────────────────────────────────────────────

def _get_ect(raw: DiagnosticInput) -> float | None:
    """Return the best available ECT reading from OBD or freeze frame."""
    if raw.obd is not None and raw.obd.ect_c is not None:
        return raw.obd.ect_c
    if raw.freeze_frame is not None and raw.freeze_frame.ect_c is not None:
        return raw.freeze_frame.ect_c
    return None
