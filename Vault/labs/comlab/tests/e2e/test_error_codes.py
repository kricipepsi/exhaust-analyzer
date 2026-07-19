"""Error-code contract coverage — one parametrized case per §10 code.

Walks every error code in ``COMLab_LLD.md §10`` and asserts that the
corresponding code path raises when given a triggering input.

Where the error-code path is not yet implemented (fallback tree stubbed),
the test documents current behaviour and the gap is tracked as a T-P5-1b
follow-up in COMLAB_PROGRESS.md.

Source: COMLab_LLD.md §9.6, §10.
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError

from comlab.core.lab_pipeline_aggregator import AggregatorAbort, LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest, VinDNA
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EuroEmissionCategory,
    FuelDeliveryType,
    Horizon,
    InductionType,
    PrimaryLoadCalculation,
    UpstreamO2Type,
    VinConfidence,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _session_id() -> str:
    return str(uuid4())


def _minimal_valid_payload() -> dict:
    """Return a dict that passes ``OrchestratorInboundRequest`` validation."""
    sid = _session_id()
    return {
        "metadata": {
            "session_id": sid,
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
        },
        "gas_lab_output": {
            "chemical_state": "NORMAL_OPERATION",
            "gas_co": 0.5,
            "gas_hc": 50,
            "gas_co2": 14.0,
            "gas_o2": 1.0,
            "gas_nox": 200,
            "lambda_chem": 1.0,
            "sample_validity": "VALID",
        },
        "obd_live_data": {
            "engine_warmed": True,
            "total_trim_correction_delta": -5.0,
            "ve_pct": 75.0,
            "ve_validity": "VALID",
            "rpm_state_bucket": "STABILIZED_IDLE",
            "trim_analytics_gate": "VALID",
            "o2_failure_mode": "STUCK_LEAN",
            "maf_status": "REAL_SENSOR_FEED",
            "map_status": "REAL_SENSOR_FEED",
        },
        "dtc_lab_output": {
            "active_mil": False,
            "mil_flashing": False,
            "confirmed_dtcs": [],
            "pending_dtcs": [],
            "permanent_dtcs": [],
            "routing_tags": [],
            "mode_06_monitors": {},
            "historical_fault_context": "UNKNOWN",
            "freeze_frame": {
                "fuel_system_status": "CL",
                "engine_rpm": 750,
                "vehicle_speed_kmh": 0,
                "coolant_temp_c": 90.0,
                "intake_air_temp_c": 25.0,
                "throttle_pos_pct": 5.0,
                "calculated_load_pct": 20.0,
                "maf_gps": 3.5,
                "manifold_pressure_kpa": 30.0,
                "short_term_ft1": -3.0,
                "long_term_ft1": -5.0,
                "ignition_advance_deg": 10.0,
                "o2_voltage_b1s1": 0.45,
            },
        },
        "symptom_dna": {},
    }


# ===================================================================
# ERR-CONTRACT-001 — DTC regex / range / missing
# ===================================================================
class TestErrContract001:
    """Pydantic gate rejects payloads failing DTC_REGEX (LLD §10)."""

    def test_invalid_dtc_string_rejected(self) -> None:
        """ERR-CONTRACT-001: confirmed_dtcs entry not matching DTC_REGEX."""
        payload = _minimal_valid_payload()
        payload["dtc_lab_output"]["confirmed_dtcs"] = ["BAD_CODE"]

        agg = LabPipelineAggregator()
        with pytest.raises(ValidationError) as exc_info:
            agg.validate_payload(payload)

        errors = str(exc_info.value)
        assert "ERR-CONTRACT-001" in errors

    def test_invalid_pending_dtc_rejected(self) -> None:
        """ERR-CONTRACT-001: pending_dtcs entry not matching DTC_REGEX."""
        payload = _minimal_valid_payload()
        payload["dtc_lab_output"]["pending_dtcs"] = ["X9999"]

        agg = LabPipelineAggregator()
        with pytest.raises(ValidationError) as exc_info:
            agg.validate_payload(payload)

        assert "ERR-CONTRACT-001" in str(exc_info.value)

    def test_invalid_permanent_dtc_rejected(self) -> None:
        """ERR-CONTRACT-001: permanent_dtcs entry not matching DTC_REGEX."""
        payload = _minimal_valid_payload()
        payload["dtc_lab_output"]["permanent_dtcs"] = ["P0xxx"]

        agg = LabPipelineAggregator()
        with pytest.raises(ValidationError) as exc_info:
            agg.validate_payload(payload)

        assert "ERR-CONTRACT-001" in str(exc_info.value)

    def test_valid_dtc_accepted(self) -> None:
        """ERR-CONTRACT-001: valid DTC should not raise."""
        payload = _minimal_valid_payload()
        payload["dtc_lab_output"]["confirmed_dtcs"] = ["P0172", "P0300"]

        agg = LabPipelineAggregator()
        result = agg.validate_payload(payload)
        assert result is not None

    def test_hex_tail_dtc_accepted(self) -> None:
        """ERR-CONTRACT-001: hex-tail DTC (P044A) must pass (regression: decimal-only regex false-rejected hex DTCs)."""
        payload = _minimal_valid_payload()
        payload["dtc_lab_output"]["confirmed_dtcs"] = ["P044A"]

        agg = LabPipelineAggregator()
        result = agg.validate_payload(payload)
        assert result is not None


# ===================================================================
# ERR-CONTRACT-002 — cross-field consistency
# ===================================================================
class TestErrContract002:
    """Air-metering consistency gate (LLD §10).

    The ``_air_metering_consistency`` model_validator on VinDNA rejects
    mismatched air_metering_strategy ↔ AirMeteringArchitecture booleans.
    """

    @staticmethod
    def _valid_vin_dna_dict() -> dict:
        """Return a minimal valid VinDNA dict for consistency tests."""
        return {
            "vin": "1FA6P8CF0HXXXXXXX",
            "make": "Ford",
            "model": "Mustang",
            "model_year": 2020,
            "engine_displacement_liters": 5.0,
            "cylinder_count": 8,
            "number_of_banks": 2,
            "induction_type": InductionType.NATURALLY_ASPIRATED,
            "fuel_delivery_type": FuelDeliveryType.PORT_INJECTION,
            "air_metering_architecture": {
                "has_maf_sensor": True,
                "has_map_sensor": True,
                "primary_load_calculation": PrimaryLoadCalculation.HYBRID_MAF_MAP,
            },
            "air_metering_strategy": AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
            "emissions": {
                "upstream_o2_type": UpstreamO2Type.WIDEBAND_AFR,
                "downstream_o2_present": True,
                "egr_equipped": True,
                "has_catalyst": True,
            },
            "euro_emission_category": EuroEmissionCategory.EURO_6,
            "stress_idle_rpm_target": 3500,
            "confidence": VinConfidence.HIGH,
            "resolved_horizon": Horizon.MODERN,
        }

    def test_maf_only_missing_maf_sensor_raises(self) -> None:
        """ERR-CONTRACT-002: MAF_ONLY strategy with has_maf_sensor=False."""
        data = self._valid_vin_dna_dict()
        data["air_metering_strategy"] = AirMeteringStrategy.MAF_ONLY
        data["air_metering_architecture"]["has_maf_sensor"] = False
        data["air_metering_architecture"]["has_map_sensor"] = True
        data["air_metering_architecture"]["primary_load_calculation"] = (
            PrimaryLoadCalculation.MAF_ONLY
        )

        with pytest.raises(ValidationError) as exc_info:
            VinDNA.model_validate(data)

        assert "ERR-CONTRACT-002" in str(exc_info.value)

    def test_map_only_missing_map_sensor_raises(self) -> None:
        """ERR-CONTRACT-002: MAP_ONLY_SPEED_DENSITY with has_map_sensor=False."""
        data = self._valid_vin_dna_dict()
        data["air_metering_strategy"] = AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY
        data["air_metering_architecture"]["has_maf_sensor"] = True
        data["air_metering_architecture"]["has_map_sensor"] = False
        data["air_metering_architecture"]["primary_load_calculation"] = (
            PrimaryLoadCalculation.MAP_ONLY
        )

        with pytest.raises(ValidationError) as exc_info:
            VinDNA.model_validate(data)

        assert "ERR-CONTRACT-002" in str(exc_info.value)

    def test_dual_crosscheck_missing_maf_raises(self) -> None:
        """ERR-CONTRACT-002: DUAL_MAF_MAP_CROSSCHECK with has_maf_sensor=False."""
        data = self._valid_vin_dna_dict()
        data["air_metering_architecture"]["has_maf_sensor"] = False

        with pytest.raises(ValidationError) as exc_info:
            VinDNA.model_validate(data)

        assert "ERR-CONTRACT-002" in str(exc_info.value)

    def test_consistent_config_accepted(self) -> None:
        """ERR-CONTRACT-002: valid VinDNA with consistent config accepted."""
        data = self._valid_vin_dna_dict()
        result = VinDNA.model_validate(data)
        assert result.air_metering_strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK


# ===================================================================
# ERR-ABORT-001 — sample_validity != VALID
# ===================================================================
class TestErrAbort001:
    """Sample validity fatal gate (LLD §10).

    ``run_fatal_gates_and_routing`` raises ``AggregatorAbort(ERR-ABORT-001)``
    when ``sample_validity`` is not VALID or BORDERLINE and GASLab is not
    suppressed.
    """

    def test_sample_invalid_aborts(self) -> None:
        """ERR-ABORT-001: sample_validity=INVALID raises AggregatorAbort."""
        payload = _minimal_valid_payload()
        payload["gas_lab_output"]["sample_validity"] = "INVALID"
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        with pytest.raises(AggregatorAbort) as exc_info:
            agg.run_fatal_gates_and_routing(request)

        assert exc_info.value.error_code == "ERR-ABORT-001"

    def test_sample_borderline_accepted(self) -> None:
        """ERR-ABORT-001: sample_validity=BORDERLINE does not abort."""
        payload = _minimal_valid_payload()
        payload["gas_lab_output"]["sample_validity"] = "BORDERLINE"
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        directive = agg.run_fatal_gates_and_routing(request)
        assert directive is not None


# ===================================================================
# ERR-ABORT-002 — engine_warmed != True
# ===================================================================
class TestErrAbort002:
    """Engine-warmed fatal gate (LLD §10).

    ``run_fatal_gates_and_routing`` raises ``AggregatorAbort(ERR-ABORT-002)``
    when ``engine_warmed`` is False and OBD live PIDs are not suppressed.
    """

    def test_engine_not_warmed_aborts(self) -> None:
        """ERR-ABORT-002: engine_warmed=False raises AggregatorAbort."""
        payload = _minimal_valid_payload()
        payload["obd_live_data"]["engine_warmed"] = False
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        with pytest.raises(AggregatorAbort) as exc_info:
            agg.run_fatal_gates_and_routing(request)

        assert exc_info.value.error_code == "ERR-ABORT-002"


# ===================================================================
# ERR-ABORT-004 — confidence == NONE
# ===================================================================
class TestErrAbort004:
    """VinConfidence fatal gate (LLD §10).

    ``run_fatal_gates_and_routing`` raises ``AggregatorAbort(ERR-ABORT-004)``
    when ``SessionMetadata.vin_confidence`` is ``NONE``.
    """

    def test_vin_confidence_none_aborts(self) -> None:
        """ERR-ABORT-004: vin_confidence=NONE raises AggregatorAbort."""
        payload = _minimal_valid_payload()
        payload["metadata"]["vin_confidence"] = "NONE"
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        with pytest.raises(AggregatorAbort) as exc_info:
            agg.run_fatal_gates_and_routing(request)

        assert exc_info.value.error_code == "ERR-ABORT-004"


# ===================================================================
# ERR-ABORT-005 — schema_version < MIN_SUPPORTED
# ===================================================================
class TestErrAbort005:
    """Schema-version gate (LLD §10).

    ``check_schema_version`` raises ``AggregatorAbort(ERR-ABORT-005)`` when
    ``SessionMetadata.schema_version`` is below ``MIN_SUPPORTED_SCHEMA_VERSION``.
    """

    def test_old_schema_version_aborts(self) -> None:
        """ERR-ABORT-005: schema_version < MIN_SUPPORTED raises AggregatorAbort."""
        payload = _minimal_valid_payload()
        payload["metadata"]["schema_version"] = "0.9"
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        with pytest.raises(AggregatorAbort) as exc_info:
            agg.check_schema_version(request.metadata.schema_version)

        assert exc_info.value.error_code == "ERR-ABORT-005"

    def test_current_schema_version_accepted(self) -> None:
        """ERR-ABORT-005: schema_version >= MIN_SUPPORTED does not abort."""
        payload = _minimal_valid_payload()
        payload["metadata"]["schema_version"] = "1.0"
        request = OrchestratorInboundRequest.model_validate(payload)

        agg = LabPipelineAggregator()
        agg.check_schema_version(request.metadata.schema_version)  # does not raise


# ===================================================================
# ERR-VIN-400 — VIN format invalid
# ===================================================================
class TestErrVin400:
    """VIN format validation (LLD §10).

    SessionMetadata.vin_dna_string requires 17-char uppercase alphanumeric.
    """

    def test_vin_too_short_rejected(self) -> None:
        """ERR-VIN-400: vin_dna_string shorter than 17 chars."""
        payload = _minimal_valid_payload()
        payload["metadata"]["vin_dna_string"] = "SHORT"

        agg = LabPipelineAggregator()
        with pytest.raises(ValidationError):
            agg.validate_payload(payload)

    def test_vin_too_long_rejected(self) -> None:
        """ERR-VIN-400: vin_dna_string longer than 17 chars."""
        payload = _minimal_valid_payload()
        payload["metadata"]["vin_dna_string"] = "WBA3A5C5XDF1234567"  # 18 chars

        agg = LabPipelineAggregator()
        with pytest.raises(ValidationError):
            agg.validate_payload(payload)

    def test_valid_vin_accepted(self) -> None:
        """ERR-VIN-400: valid 17-char VIN should not raise."""
        payload = _minimal_valid_payload()
        payload["metadata"]["vin_dna_string"] = "WBA3A5C5XDF123456"

        agg = LabPipelineAggregator()
        result = agg.validate_payload(payload)
        assert result is not None
