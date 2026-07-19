"""Perception-contradiction detector — Lambda Truth vs Perception.

Pure function comparing OBDLab's ``normalized_obd_lambda`` (ECU perception)
against GASLab's ``lambda_chem`` (Brettschneider ground truth). When they
diverge beyond the era lambda tolerance while gas chemistry is near-normal,
surfaces an O2-sensor-bias finding.

Source: data_flow_report.md §4 OBDLab OUT, Sensor_Fault_Family.md §Lambda Truth filter,
COMLab_Lab_Input_Reference.md §Perception vs Truth axis.
"""

from __future__ import annotations

from dataclasses import dataclass

from comlab.schemas.vocabulary import ChemicalSignature, DownstreamTrimRole

__all__ = [
    "CompensatedRichResult",
    "PerceptionContradictionResult",
    "QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT",
    "QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM",
    "QUALIFIER_RAIL_OUT_OF_BAND",
    "detect",
    "detect_compensated_rich",
    "select_perception_lambda",
]


# Rich DTC pattern — P0172 (bank 1) and P0175 (bank 2) fuel system too rich
# wiki: DTC_VOCABULARY §8 — RICH_HISTORY routing tag
_RICH_DTC_CODES: frozenset[str] = frozenset({"P0172", "P0175"})

# Perception-contradiction qualifier constants — extensible tuple of caveats
# that qualify (but do not change) the bias_verdict. Downstream consumers
# check membership: ``QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers``.
# wiki: O2_MODEL_STRATEGY.md §4.3
QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM: str = "MASKED_BY_DOWNSTREAM_TRIM"
# wiki: O2_MODEL_STRATEGY.md §9.1 — de-cat + secondary trim is incoherent:
# the secondary loop depends on catalyst oxygen buffering which a de-cat
# vehicle cannot provide.
QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT: str = "DECAT_SECONDARY_TRIM_INCOHERENT"
# wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS;
# 13_proposals_register.md line 47 (EP-OBD-IN-04)
QUALIFIER_RAIL_OUT_OF_BAND: str = "RAIL_OUT_OF_BAND"

_VPWR_LOW_V: float = 12.0  # wiki: 02_lab_input_contract.md §2a — low rail boundary
_VPWR_HIGH_V: float = 15.0  # wiki: 02_lab_input_contract.md §2a — high rail boundary
_LAMBDA_DELTA_PRECISION_DIGITS: int = 6  # wiki: COMLab_Lab_Input_Reference.md §Perception vs Truth axis
_LAMBDA_TRUTH_FILTER_LOW: float = 0.90  # wiki: Sensor_Fault_Family.md §Lambda Truth filter
_LAMBDA_TRUTH_FILTER_HIGH: float = 1.10  # wiki: Sensor_Fault_Family.md §Lambda Truth filter
_COMPENSATED_RICH_STOICH_LOW: float = 0.95  # wiki: ERR-RM-003_Leaking_Fuel_Injector.md
_COMPENSATED_RICH_STOICH_HIGH: float = 1.05  # wiki: ERR-RM-003_Leaking_Fuel_Injector.md
_COMPENSATED_RICH_RAILED_TRIM_PCT: float = -15.0  # wiki: ERR-RM-003_Leaking_Fuel_Injector.md line 49
_COMPENSATED_RICH_BASE_CONFIDENCE: float = 0.75  # wiki: T-P6-6a — 3-gate baseline
_COMPENSATED_RICH_CONFIRMED_CONFIDENCE: float = 0.90  # wiki: T-P6-6a — perception axis confirms


@dataclass
class CompensatedRichResult:
    """Output of the compensated-rich detector.

    Identifies cases where near-stoich combustion chemistry co-exists with
    railed-negative fuel trim and a rich DTC — the ECU is masking a fuel leak
    by pulling trim to the rail.  GASLab alone would classify this as stoich
    or lean; the trim + DTC evidence contradicts that classification.

    Attributes:
        is_compensated_rich: ``True`` when all AND-gate conditions are met.
        confidence: 0.0–1.0 heuristic confidence in the finding.
    """

    is_compensated_rich: bool = False
    confidence: float = 0.0


@dataclass(frozen=True)
class PerceptionContradictionResult:
    """Output of the perception-contradiction detector.

    Attributes:
        lambda_perception_delta: Signed ``normalized_obd_lambda - lambda_chem``.
        bias_verdict: ``None``, ``O2_SENSOR_BIASED_LOW``, or ``O2_SENSOR_BIASED_HIGH``.
        guard_suppressed: ``True`` when the Lambda Truth filter suppressed a bias
            verdict because gas chemistry itself is deeply abnormal.
        qualifiers: Operational caveats that qualify but do not change
            ``bias_verdict``; consumers check tuple membership.
    """

    lambda_perception_delta: float
    bias_verdict: ChemicalSignature | None  # wiki: Sensor_Fault_Family.md §Lambda Truth filter
    guard_suppressed: bool
    qualifiers: tuple[str, ...] = ()
    # wiki: O2_MODEL_STRATEGY.md §4.3 — operational caveats that qualify but
    # do not change the bias_verdict. Downstream consumers check membership:
    # ``QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM in result.qualifiers``.
    # Tuple is extensible — future qualifiers (VOLTAGE_SAG_WARNING, etc.)
    # can be appended without breaking existing verdict checks.


def select_perception_lambda(
    normalized_obd_lambda: float | None,
    lambda_measured: float | None,
) -> float | None:
    """Choose the perception-source lambda for the contradiction detector.

    OBD lambda wins when the OBD channel is present (it is the live ECU
    perception signal). Falls back to the technician-entered gas-analyser λ
    only when the OBD channel is absent. Returns ``None`` when neither source
    is available (detector will be inert).

    Args:
        normalized_obd_lambda: ECU-perceived lambda from OBDLab, or ``None``
            if the OBD channel was not run.
        lambda_measured: Technician-entered directly-measured analyser λ from
            GASLab, or ``None`` if not supplied.

    Returns:
        The float to pass as ``normalized_obd_lambda`` to ``detect()``.

    Source: T-FX-7; data_flow_report.md §4 OBDLab OUT; UI/4DLab_UI_FieldMap.md §5/§14 #1.
    """
    # wiki: COMLab_Lab_Input_Reference.md §Perception vs Truth axis
    return normalized_obd_lambda if normalized_obd_lambda is not None else lambda_measured


def detect(
    lambda_chem: float,
    normalized_obd_lambda: float | None,
    era_lambda_tolerance: float,
    downstream_trim_role: DownstreamTrimRole = DownstreamTrimRole.NONE,
    has_catalyst: bool = True,
    *,
    control_module_voltage_v: float | None = None,
    enable_vpwr_gate: bool = False,
) -> PerceptionContradictionResult:
    """Compare ECU-perceived lambda against Brettschneider ground truth.

    Args:
        lambda_chem: Brettschneider lambda from GASLab (ground truth).
        normalized_obd_lambda: ECU-perceived lambda from OBDLab, or ``None``
            if the OBD channel is absent.
        era_lambda_tolerance: Active era's ``lambda_tolerance`` from
            ``eras_sensitivity_masks.yaml`` (e.g. MODERN=0.02, ADAPTIVE=0.05,
            LEGACY=0.10).
        downstream_trim_role: Role of the downstream O2 sensor in the ECU's
            closed-loop strategy. When ``SECONDARY_FUEL_TRIM``, an in-tolerance
            perception/truth agreement is qualified as weak evidence (the
            downstream loop may be masking upstream O2 drift). Default ``NONE``
            preserves existing behaviour.
        has_catalyst: Whether the vehicle has a catalytic converter. When
            ``False`` (de-cat) AND ``downstream_trim_role == SECONDARY_FUEL_TRIM``,
            the configuration is flagged as incoherent — the secondary loop
            depends on catalyst oxygen buffering.  # wiki: O2_MODEL_STRATEGY.md §9.1
        control_module_voltage_v: OBD control-module supply voltage, or ``None``
            when the OBD channel or PID is unavailable.
        enable_vpwr_gate: Whether to suppress sensor-bias routing when the
            control-module rail is outside the COMLab-local healthy band.

    Returns:
        ``PerceptionContradictionResult`` with the signed delta, bias verdict,
        guard-suppressed flag, and qualifiers.
    """
    # WHY: configuration caveats are reported even when the OBD lambda
    # channel is absent; de-cat + secondary trim is physically incoherent.
    # wiki: O2_MODEL_STRATEGY.md §9.1
    config_qualifiers: list[str] = []
    if not has_catalyst and downstream_trim_role == DownstreamTrimRole.SECONDARY_FUEL_TRIM:
        config_qualifiers.append(QUALIFIER_DECAT_SECONDARY_TRIM_INCOHERENT)

    # -- OBD channel absent → detector inert (data_flow_report.md §4 OBDLab OUT) --
    if normalized_obd_lambda is None:
        return PerceptionContradictionResult(
            lambda_perception_delta=0.0,
            bias_verdict=None,
            guard_suppressed=False,
            qualifiers=tuple(config_qualifiers),
        )

    delta = round(normalized_obd_lambda - lambda_chem, _LAMBDA_DELTA_PRECISION_DIGITS)

    # WHY: deeply abnormal gas chemistry invalidates the sensor-bias comparison;
    # route the chemistry fault family instead of fabricating an O2 bias verdict.
    # wiki: Sensor_Fault_Family.md §Lambda Truth filter
    # wiki: ERR-SF-002_O2_Sensor_Fixed_Voltage.md §Diagnostic Fingerprint
    if lambda_chem < _LAMBDA_TRUTH_FILTER_LOW or lambda_chem > _LAMBDA_TRUTH_FILTER_HIGH:
        return PerceptionContradictionResult(
            lambda_perception_delta=delta,
            bias_verdict=None,
            guard_suppressed=True,
            qualifiers=tuple(config_qualifiers),
        )

    # WHY: an out-of-band module rail can mimic sensor bias, so the default-off
    # VPWR gate qualifies the result without making a chemical/routing claim.
    # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
    # wiki: 13_proposals_register.md line 47 — EP-OBD-IN-04
    if (
        enable_vpwr_gate
        and control_module_voltage_v is not None
        and (
            control_module_voltage_v < _VPWR_LOW_V
            or control_module_voltage_v > _VPWR_HIGH_V
        )
    ):
        config_qualifiers.append(QUALIFIER_RAIL_OUT_OF_BAND)
        return PerceptionContradictionResult(
            lambda_perception_delta=delta,
            bias_verdict=None,
            guard_suppressed=False,
            qualifiers=tuple(config_qualifiers),
        )

    # -- Divergence check against era tolerance --
    # wiki: COMLab_Lab_Input_Reference.md §Perception vs Truth axis (0.05-0.08 band)
    # lld: eras_sensitivity_masks.yaml lambda_tolerance per horizon
    if delta > era_lambda_tolerance:
        # OBD lambda leaner than truth -> sensor reads artificially lean/high lambda
        return PerceptionContradictionResult(
            lambda_perception_delta=delta,
            bias_verdict=ChemicalSignature.O2_SENSOR_BIASED_HIGH,
            guard_suppressed=False,
            qualifiers=tuple(config_qualifiers),
        )

    if -delta > era_lambda_tolerance:
        # OBD lambda richer than truth -> sensor reads artificially rich/low lambda
        return PerceptionContradictionResult(
            lambda_perception_delta=delta,
            bias_verdict=ChemicalSignature.O2_SENSOR_BIASED_LOW,
            guard_suppressed=False,
            qualifiers=tuple(config_qualifiers),
        )

    # -- Within tolerance -> no bias --
    # WHY: secondary-fuel-trim ECUs can mask upstream O2 drift by actively
    # biasing fuel, so in-tolerance agreement is only weak healthy-sensor evidence.
    # wiki: O2_MODEL_STRATEGY.md §4.3
    if downstream_trim_role == DownstreamTrimRole.SECONDARY_FUEL_TRIM:
        config_qualifiers.append(QUALIFIER_MASKED_BY_DOWNSTREAM_TRIM)
    return PerceptionContradictionResult(
        lambda_perception_delta=delta,
        bias_verdict=None,
        guard_suppressed=False,
        qualifiers=tuple(config_qualifiers),
    )


def detect_compensated_rich(
    lambda_chem: float,
    total_trim_correction_delta: float,
    obd_lambda: float | None,
    era_lambda_tolerance: float,
    rich_dtc_present: bool,
) -> CompensatedRichResult:
    """Detect compensated-rich: ECU masks a fuel leak by pulling trim to the rail.

    GASLab sees near-stoich chemistry (the leak is being compensated), but the
    ECU's railed-negative fuel trim + rich DTC tell a different story.  This
    detector is the bridge — it does NOT mutate ``chemical_state``; instead it
    returns a finding that the fault-atlas router uses as a bypass gate in Phase 2
    chemistry pruning.

    AND-gate (all must be true):
    1. ``lambda_chem`` ∈ [0.95, 1.05] — true stoich window
       wiki: ERR-RM-003_Leaking_Fuel_Injector.md §Diagnostic Fingerprint
    2. ``total_trim_correction_delta`` < −15 % — railed negative
       wiki: ERR-RM-003_Leaking_Fuel_Injector.md line 49
    3. ``rich_dtc_present`` — P0172 or P0175 confirms ECU perception of rich
       wiki: DTC_VOCABULARY §8 — RICH_HISTORY

    Confidence is boosted when the OBD lambda also reads richer than chemistry
    (perception-contradiction axis confirms the direction), but a small OBD
    delta does NOT suppress the finding — the trim + DTC evidence already
    carries the signal.

    Returns:
        ``CompensatedRichResult`` with ``is_compensated_rich`` and a 0.0–1.0
        confidence score.
    """
    # Gate 1 — stoich window (suppresses genuinely lean chemistry like case_013 λ=1.08)
    # wiki: ERR-RM-003_Leaking_Fuel_Injector.md §Diagnostic Fingerprint
    if not (_COMPENSATED_RICH_STOICH_LOW <= lambda_chem <= _COMPENSATED_RICH_STOICH_HIGH):
        return CompensatedRichResult(is_compensated_rich=False, confidence=0.0)

    # Gate 2 — railed-negative trim
    # wiki: ERR-RM-003_Leaking_Fuel_Injector.md line 49 (threshold −15 %)
    if total_trim_correction_delta >= _COMPENSATED_RICH_RAILED_TRIM_PCT:
        return CompensatedRichResult(is_compensated_rich=False, confidence=0.0)

    # Gate 3 — rich DTC confirms ECU perception
    # wiki: DTC_VOCABULARY §8 — RICH_HISTORY
    if not rich_dtc_present:
        return CompensatedRichResult(is_compensated_rich=False, confidence=0.0)

    # All gates passed — base confidence.
    confidence: float = _COMPENSATED_RICH_BASE_CONFIDENCE

    # Confidence modifier: OBD lambda delta confirms direction
    # When OBD reads richer than chemistry beyond era tolerance,
    # the perception-contradiction axis agrees → boost confidence.
    # When the delta is small or absent, the finding still stands
    # (CASE-025: Δ=−0.03, within LEGACY tolerance, still a real compensated-rich).
    if obd_lambda is not None:
        delta = round(obd_lambda - lambda_chem, _LAMBDA_DELTA_PRECISION_DIGITS)
        if -delta > era_lambda_tolerance:
            confidence = _COMPENSATED_RICH_CONFIRMED_CONFIDENCE

    return CompensatedRichResult(is_compensated_rich=True, confidence=confidence)
