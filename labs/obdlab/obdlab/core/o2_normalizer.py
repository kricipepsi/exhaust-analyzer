"""O2 sensor normalisation layer per OBDLab_KG_Wiki.md §11.

Routes on dna_view.upstream_o2_type:
  NARROWBAND_0_TO_1V  → 3-zone voltage-to-lambda (§11.1)
  WIDEBAND_LINEAR     → direct pass-through (§11.2)
  WIDEBAND_NB_SIM     → 3-zone voltage-to-lambda, WB-sim mode (§11.3)

Produces a single normalized_obd_lambda in 0.7–1.3.
Source: OBDLab_KG_Wiki.md §11, §6.3.
"""

import logging
from typing import Any

from obdlab.core.analytics_preconditions import (
    ECT_WARM_THRESHOLD,
    WOT_THROTTLE_THRESHOLD,
)
from obdlab.core.exceptions import PIDValidationError
from obdlab.schemas.dna_view import O2SensorType, ObdLabDnaView
from obdlab.schemas.vocabulary import (
    FuelSystemStatus,
    O2FailureMode,
    O2NormalizationMode,
)

logger = logging.getLogger(__name__)

# wiki: §11.1 — narrowband 3-zone voltage → lambda mapping
_ZONE_LEAN_BOUNDARY   = 0.40   # wiki: §11.1 — upper bound of LEAN_STATE (V)
_ZONE_STOICH_BOUNDARY = 0.50   # wiki: §11.1 — upper bound of STOICHIOMETRIC_CENTER (V)
_ZONE_MIN_VOLTAGE     = 0.10   # wiki: §11.1 — minimum valid narrowband voltage
_ZONE_MAX_VOLTAGE     = 0.90   # wiki: §11.1 — maximum valid narrowband voltage

# wiki: §11.1 — narrowband zone output lambdas
_LAMBDA_LEAN   = 1.05  # wiki: §11.1 — 0.10–0.40 V
_LAMBDA_STOICH = 1.00  # wiki: §11.1 — 0.41–0.50 V
_LAMBDA_RICH   = 0.95  # wiki: §11.1 — 0.51–0.90 V

# wiki: §5 — OBDLivePayload.normalized_obd_lambda field range
_LAMBDA_MIN = 0.7   # wiki: §5
_LAMBDA_MAX = 1.3   # wiki: §5


# wiki: o2-logic/03 §BIASED_OFFSET — stoichiometry midpoint
_LAMBDA_STOICH_TARGET = 1.0  # wiki: o2-logic/03 §BIASED_OFFSET

# wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08 — wideband offset limit
_WIDEBAND_OFFSET_THRESHOLD = 0.05  # wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08


class O2Normalizer:
    """Normalize O2 sensor input to a unified lambda scalar per §11.

    Public entry point: normalize().
    """

    def normalize(
        self,
        pids: dict[str, Any],
        dna_view: ObdLabDnaView | None = None,
    ) -> tuple[float, O2NormalizationMode, O2FailureMode]:
        """Route to the matching O2 normalisation branch and return (lambda, mode, failure).

        Args:
            pids: sanitized PID dict.
            dna_view: typed DNA view or None (defaults to NARROWBAND_0_TO_1V).

        Returns:
            (normalized_obd_lambda, O2NormalizationMode, O2FailureMode).
            O2FailureMode.NO_FAULT for healthy readings; STUCK_LEAN/STUCK_RICH
            when O2_CHANNEL_FAULT is set with a corresponding clamped lambda.

        Raises:
            PIDValidationError: input voltage/ratio out of range or missing field.
        """
        sensor_type = (
            dna_view.upstream_o2_type if dna_view
            else O2SensorType.NARROWBAND_0_TO_1V
        )

        if dna_view is None:
            logger.info(
                "o2_normalize_defaulting: reason=dna_view_absent "
                "fallback=%s",
                O2SensorType.NARROWBAND_0_TO_1V.value,
            )

        if sensor_type == O2SensorType.NARROWBAND_0_TO_1V:
            return self._narrowband_to_lambda(pids)

        if sensor_type == O2SensorType.WIDEBAND_LINEAR:
            return self._wideband_passthrough(pids)

        if sensor_type == O2SensorType.WIDEBAND_NB_SIM:
            return self._wideband_nb_sim_to_lambda(pids)

        raise PIDValidationError(
            f"Unknown upstream_o2_type: {sensor_type}"
        )

    # ------------------------------------------------------------------
    # Narrowband — voltage → lambda §11.1
    # ------------------------------------------------------------------

    def _narrowband_to_lambda(self, pids: dict[str, Any]) -> tuple[float, O2NormalizationMode, O2FailureMode]:
        """3-zone narrowband voltage → lambda mapping per §11.1.

        Reads pid_oxygen_sensor_volts from pids.
        """
        volts = pids.get("pid_oxygen_sensor_volts")
        if volts is None:
            raise PIDValidationError(
                "pid_oxygen_sensor_volts missing for NARROWBAND_0_TO_1V branch"
            )

        if not isinstance(volts, (int, float)):
            raise PIDValidationError(
                f"pid_oxygen_sensor_volts must be numeric, got {type(volts).__name__}"
            )

        if volts < _ZONE_MIN_VOLTAGE:
            logger.info(
                "o2_channel_fault: sensor=narrowband volts=%s action=clamp_to_lean",
                volts,
            )
            # wiki: §6.7 — below min voltage → STUCK_LEAN
            return (_LAMBDA_LEAN, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.STUCK_LEAN)
        if volts > _ZONE_MAX_VOLTAGE:
            logger.info(
                "o2_channel_fault: sensor=narrowband volts=%s action=clamp_to_rich",
                volts,
            )
            # wiki: §6.7 — above max voltage → STUCK_RICH
            return (_LAMBDA_RICH, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.STUCK_RICH)

        # wiki: §11.1 — 5-zone mapping collapsed to 3 lambda outputs
        if volts <= _ZONE_LEAN_BOUNDARY:          # 0.10–0.40 V
            return (_LAMBDA_LEAN, O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)
        if volts <= _ZONE_STOICH_BOUNDARY:        # 0.41–0.50 V
            return (_LAMBDA_STOICH, O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)
        # volts > 0.50, ≤ 0.90  (enforced by range check above)
        return (_LAMBDA_RICH, O2NormalizationMode.NARROWBAND_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)

    # ------------------------------------------------------------------
    # Wideband — direct pass-through §11.2
    # ------------------------------------------------------------------

    def _wideband_passthrough(self, pids: dict[str, Any]) -> tuple[float, O2NormalizationMode, O2FailureMode]:
        """Direct wideband pass-through per §11.2.

        Reads pid_wideband_equivalence_ratio from pids.
        """
        ratio = pids.get("pid_wideband_equivalence_ratio")
        if ratio is None:
            raise PIDValidationError(
                "pid_wideband_equivalence_ratio missing for WIDEBAND_LINEAR branch"
            )

        if not isinstance(ratio, (int, float)):
            raise PIDValidationError(
                f"pid_wideband_equivalence_ratio must be numeric, got {type(ratio).__name__}"
            )

        if ratio < _LAMBDA_MIN:
            logger.info(
                "o2_channel_fault: sensor=wideband ratio=%s action=clamp_to_min",
                ratio,
            )
            return (_LAMBDA_MIN, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.NO_FAULT)
        if ratio > _LAMBDA_MAX:
            logger.info(
                "o2_channel_fault: sensor=wideband ratio=%s action=clamp_to_max",
                ratio,
            )
            return (_LAMBDA_MAX, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.NO_FAULT)

        # check persistent offset conditions
        ect = pids.get("coolant_temp_c")
        fuel_status = pids.get("fuel_sys_status")
        throttle = pids.get("throttle_pos")
        dfco = pids.get("dfco_active")

        is_warm = ect is not None and ect >= ECT_WARM_THRESHOLD
        is_closed_loop = FuelSystemStatus.from_wire(fuel_status) == FuelSystemStatus.CL
        is_wot = throttle is not None and throttle >= WOT_THROTTLE_THRESHOLD
        is_dfco = dfco is True

        if is_warm and is_closed_loop and not is_wot and not is_dfco:
            if abs(ratio - _LAMBDA_STOICH_TARGET) > _WIDEBAND_OFFSET_THRESHOLD:
                return (float(ratio), O2NormalizationMode.WIDEBAND_PASSTHROUGH, O2FailureMode.WIDEBAND_OFFSET_CANDIDATE)

        return (float(ratio), O2NormalizationMode.WIDEBAND_PASSTHROUGH, O2FailureMode.NO_FAULT)

    # ------------------------------------------------------------------
    # Wideband-in-NB-simulation — voltage → lambda §11.3
    # ------------------------------------------------------------------

    def _wideband_nb_sim_to_lambda(self, pids: dict[str, Any]) -> tuple[float, O2NormalizationMode, O2FailureMode]:
        """3-zone voltage → lambda mapping for WB sensor in NB simulation mode §11.3.

        Physically a wideband sensor; ECU sees 0–1 V simulated NB signal.
        PID and voltage range identical to narrowband branch (§11.1).
        Mode differs: WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA — tells COMLab
        TrimAnalyticsGate to apply WB-sim trim weight coefficient.

        Reads pid_oxygen_sensor_volts from pids.
        """
        volts = pids.get("pid_oxygen_sensor_volts")
        if volts is None:
            raise PIDValidationError(
                "pid_oxygen_sensor_volts missing for WIDEBAND_NB_SIM branch"
            )

        if not isinstance(volts, (int, float)):
            raise PIDValidationError(
                f"pid_oxygen_sensor_volts must be numeric, got {type(volts).__name__}"
            )

        if volts < _ZONE_MIN_VOLTAGE:
            logger.info(
                "o2_channel_fault: sensor=wb_nb_sim volts=%s action=clamp_to_lean",
                volts,
            )
            # wiki: §6.7 — below min voltage → STUCK_LEAN
            return (_LAMBDA_LEAN, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.STUCK_LEAN)
        if volts > _ZONE_MAX_VOLTAGE:
            logger.info(
                "o2_channel_fault: sensor=wb_nb_sim volts=%s action=clamp_to_rich",
                volts,
            )
            # wiki: §6.7 — above max voltage → STUCK_RICH
            return (_LAMBDA_RICH, O2NormalizationMode.O2_CHANNEL_FAULT, O2FailureMode.STUCK_RICH)

        # Same 3-zone voltage mapping as §11.1 — mode distinguishes WB-sim context
        if volts <= _ZONE_LEAN_BOUNDARY:
            return (_LAMBDA_LEAN, O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)
        if volts <= _ZONE_STOICH_BOUNDARY:
            return (_LAMBDA_STOICH, O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)
        return (_LAMBDA_RICH, O2NormalizationMode.WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA, O2FailureMode.NO_FAULT)
