"""Detect the ECU-hardware digital-lie signature.

Source: COMLab wiki 02_lab_input_contract.md §2a
``CONCEPT_OBD_CONSUMER_BANDS`` and §2 trim authority bands.
"""

from dataclasses import dataclass

__all__ = ["ECUHardwareChecker", "ECUHardwareVerdict"]


_ECU_HW_TEMP_FLOOR_C = -40.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_ECU_HW_TPS_RAIL_PCT = 100.0  # wiki: 02_lab_input_contract.md §2a CONCEPT_OBD_CONSUMER_BANDS
_ECU_HW_RAILED_TRIM_PCT = 25.0  # wiki: 02_lab_input_contract.md §2 line 70; §2a
_ECU_HW_BANK_SYMMETRY_PCT = 5.0  # wiki: 02_lab_input_contract.md §2 authority bands; §2a
_ECU_HW_CONFIDENCE = 0.80  # wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER
_NO_EVIDENCE_CONFIDENCE = 0.0  # wiki: 08_scoring_to_fusion_rework.md §CONCEPT_EVIDENCE_INPUTS


@dataclass(frozen=True)
class ECUHardwareVerdict:
    """Result of checking the coherent multi-sensor ECU hardware lie."""

    is_ecu_hardware_fault: bool
    confidence: float


class ECUHardwareChecker:
    """Classify the COMLab-local ECU hardware-lie evidence tuple."""

    def check(
        self,
        intake_air_temp_c: float | None,
        coolant_temp_c: float | None,
        throttle_pos_pct: float | None,
        total_trim_correction_delta: float | None,
        per_bank_trim_delta: float | None,
    ) -> ECUHardwareVerdict:
        """Return ECU-fault evidence only when every required rail agrees.

        ``per_bank_trim_delta=None`` is accepted as symmetric because single-bank
        engines cannot emit a bank delta. All other absent inputs are inert.
        """
        required_inputs = (
            intake_air_temp_c,
            coolant_temp_c,
            throttle_pos_pct,
            total_trim_correction_delta,
        )
        if any(value is None for value in required_inputs):
            return ECUHardwareVerdict(False, _NO_EVIDENCE_CONFIDENCE)

        assert intake_air_temp_c is not None
        assert coolant_temp_c is not None
        assert throttle_pos_pct is not None
        assert total_trim_correction_delta is not None

        # WHY: requiring every rail simultaneously prevents one bad sensor from
        # being misclassified as a coherent ECU-hardware digital lie.
        bank_symmetric = (
            per_bank_trim_delta is None
            or abs(per_bank_trim_delta) <= _ECU_HW_BANK_SYMMETRY_PCT
        )
        is_fault = (
            intake_air_temp_c <= _ECU_HW_TEMP_FLOOR_C
            and coolant_temp_c <= _ECU_HW_TEMP_FLOOR_C
            and throttle_pos_pct >= _ECU_HW_TPS_RAIL_PCT
            and abs(total_trim_correction_delta) >= _ECU_HW_RAILED_TRIM_PCT
            and bank_symmetric
        )
        confidence = (
            _ECU_HW_CONFIDENCE if is_fault else _NO_EVIDENCE_CONFIDENCE
        )
        return ECUHardwareVerdict(is_fault, confidence)
