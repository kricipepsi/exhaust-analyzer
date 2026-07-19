"""Tests for PIDIngestionValidator — boundary checks, unit conversions,
DNA-RPM three-branch confidence, and bank-2 null contract."""

from pathlib import Path

import pytest

from obdlab.core.exceptions import PIDValidationError
from obdlab.core.pid_ingestion_validator import PIDIngestionValidator
from obdlab.schemas.dna_view import (
    ObdLabDnaView,
    VinConfidence,
)

CONFIG_PATH = (
    Path(__file__).resolve().parents[2]
    / "obdlab" / "config" / "physical_sensor_bounds.json"
)


def _make_dna(
    confidence: VinConfidence = VinConfidence.HIGH,
    rated_rpm: int | None = 6500,
) -> ObdLabDnaView:
    return ObdLabDnaView.model_validate({
        "air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
        "upstream_o2_type": "WIDEBAND_LINEAR",
        "induction_type": "NATURALLY_ASPIRATED",
        "confidence": confidence.value,
        "rated_rpm": rated_rpm,
        "engine_displacement_liters": 2.0,
        "stress_idle_rpm_target": 4000,
    })



def _make_validator() -> PIDIngestionValidator:
    return PIDIngestionValidator(CONFIG_PATH)


# ======================================================================
# Boundary tests — each of 10 fields at min, max, below-min, above-max
# ======================================================================

BOUNDARY_CASES = [
    # (field, min_ok, max_ok, below_min, above_max)
    ("engine_rpm",                0,    8000,    -1,    8001),
    ("coolant_temp_c",           -40,   140,     -41,   141),
    ("calculated_engine_load_pct", 0,  100,     -0.1,  100.1),
    ("mass_airflow_gps",          0,    655.35,  -0.1,  655.36),
    ("manifold_vacuum_kpa",       0,    255,     -0.1,  255.1),
    ("shrtft1",                  -127,   127,   -127.1,  127.1),
    ("longft1",                  -127,   127,   -127.1,  127.1),
    ("shrtft2",                  -127,   127,   -127.1,  127.1),
    ("longft2",                  -127,   127,   -127.1,  127.1),
    ("intake_air_temp_c",        -40,   140,     -41,   141),
    ("throttle_pos_pct",           0,   100,    -0.1,   100.1),
]


@pytest.mark.parametrize("field, min_ok, max_ok, below_min, above_max", BOUNDARY_CASES)
def test_bound_at_min(field, min_ok, max_ok, below_min, above_max):
    validator = _make_validator()
    result = validator.validate_and_convert({field: min_ok, "number_of_banks": 2})
    assert result[field] == min_ok


@pytest.mark.parametrize("field, min_ok, max_ok, below_min, above_max", BOUNDARY_CASES)
def test_bound_at_max(field, min_ok, max_ok, below_min, above_max):
    validator = _make_validator()
    result = validator.validate_and_convert({field: max_ok, "number_of_banks": 2})
    assert result[field] == max_ok


@pytest.mark.parametrize("field, min_ok, max_ok, below_min, above_max", BOUNDARY_CASES)
def test_bound_below_min(field, min_ok, max_ok, below_min, above_max):
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match=field):
        validator.validate_and_convert({field: below_min, "number_of_banks": 2})


@pytest.mark.parametrize("field, min_ok, max_ok, below_min, above_max", BOUNDARY_CASES)
def test_bound_above_max(field, min_ok, max_ok, below_min, above_max):
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match=field):
        validator.validate_and_convert({field: above_max, "number_of_banks": 2})


# Bank-2 bound validation gated on number_of_banks
def test_bank2_validated_when_two_banks():
    validator = _make_validator()
    # Below min for shrtft2 should raise when banks == 2
    with pytest.raises(PIDValidationError, match="shrtft2"):
        validator.validate_and_convert({
            "shrtft2": -200.0,
            "number_of_banks": 2,
        })


def test_bank2_not_validated_when_one_bank():
    validator = _make_validator()
    # shrtft2 = null should pass silently when banks == 1
    result = validator.validate_and_convert({
        "number_of_banks": 1,
        "shrtft2": None,
        "longft2": None,
    })
    assert result["shrtft2"] is None
    assert result["longft2"] is None


# ======================================================================
# Unit-conversion tests — §3.2
# ======================================================================

def test_convert_fahrenheit_to_celsius():
    validator = _make_validator()
    result = validator.validate_and_convert({"coolant_temp_f": 212})  # 212°F = 100°C
    assert "coolant_temp_f" not in result
    assert result["coolant_temp_c"] == pytest.approx(100.0)


def test_convert_psi_to_kpa():
    validator = _make_validator()
    result = validator.validate_and_convert({"manifold_vacuum_psi": 10.0})
    assert "manifold_vacuum_psi" not in result
    assert result["manifold_vacuum_kpa"] == pytest.approx(68.95)


def test_convert_inhg_to_kpa():
    validator = _make_validator()
    result = validator.validate_and_convert({"manifold_vacuum_inhg": 10.0})
    assert "manifold_vacuum_inhg" not in result
    assert result["manifold_vacuum_kpa"] == pytest.approx(33.86)


def test_convert_lbmin_to_gps():
    validator = _make_validator()
    result = validator.validate_and_convert({"mass_airflow_lbmin": 1.0})
    assert "mass_airflow_lbmin" not in result
    assert result["mass_airflow_gps"] == pytest.approx(7.559)


def test_canonical_takes_precedence_over_alternate():
    """When both canonical and alternate are present, keep canonical, drop alternate."""
    validator = _make_validator()
    result = validator.validate_and_convert({
        "coolant_temp_c": 50.0,
        "coolant_temp_f": 212,
    })
    assert result["coolant_temp_c"] == 50.0
    assert "coolant_temp_f" not in result


def test_unknown_fields_pass_through():
    validator = _make_validator()
    result = validator.validate_and_convert({
        "unknown_field": "some_value",
        "vss_kmh": 55,
    })
    assert result["unknown_field"] == "some_value"
    assert result["vss_kmh"] == 55


# ======================================================================
# DNA-RPM three-branch confidence tests
# ======================================================================

def test_dna_high_over_rated_raises():
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.HIGH, rated_rpm=6000)
    # engine_rpm=6500 > 6000 * 1.05 = 6300
    with pytest.raises(PIDValidationError, match="rated_rpm"):
        validator.validate_and_convert({"engine_rpm": 6500}, dna_view=dna)


def test_dna_high_under_rated_passes():
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.HIGH, rated_rpm=6000)
    result = validator.validate_and_convert({"engine_rpm": 6200}, dna_view=dna)
    assert result["engine_rpm"] == 6200


def test_dna_partial_over_rated_passes():
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.PARTIAL, rated_rpm=6000)
    # PARTIAL → log and fall through to static 0..8000
    result = validator.validate_and_convert({"engine_rpm": 6500}, dna_view=dna)
    assert result["engine_rpm"] == 6500


def test_dna_none_over_rated_passes():
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.NONE, rated_rpm=6000)
    result = validator.validate_and_convert({"engine_rpm": 6500}, dna_view=dna)
    assert result["engine_rpm"] == 6500


def test_dna_view_none_passes():
    validator = _make_validator()
    result = validator.validate_and_convert({"engine_rpm": 7999}, dna_view=None)
    assert result["engine_rpm"] == 7999


def test_dna_high_rated_rpm_none_passes():
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.HIGH, rated_rpm=None)
    result = validator.validate_and_convert({"engine_rpm": 7999}, dna_view=dna)
    assert result["engine_rpm"] == 7999


def test_dna_high_still_validates_static_bound():
    """DNA-HIGH with rated_rpm=None still gets static 0..8000 check."""
    validator = _make_validator()
    dna = _make_dna(confidence=VinConfidence.HIGH, rated_rpm=None)
    with pytest.raises(PIDValidationError, match="engine_rpm"):
        validator.validate_and_convert({"engine_rpm": 9000}, dna_view=dna)


# ======================================================================
# Bank-2 null contract tests
# ======================================================================

def test_bank2_contract_one_bank_shrtft2_non_null_raises():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="shrtft2"):
        validator.validate_and_convert({
            "number_of_banks": 1,
            "shrtft2": 0.0,
            "longft2": None,
        })


def test_bank2_contract_one_bank_longft2_non_null_raises():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="longft2"):
        validator.validate_and_convert({
            "number_of_banks": 1,
            "shrtft2": None,
            "longft2": 5.0,
        })


def test_bank2_contract_one_bank_both_null_passes():
    validator = _make_validator()
    result = validator.validate_and_convert({
        "number_of_banks": 1,
        "shrtft2": None,
        "longft2": None,
    })
    assert result["shrtft2"] is None
    assert result["longft2"] is None


def test_bank2_contract_two_banks_allows_values():
    validator = _make_validator()
    result = validator.validate_and_convert({
        "number_of_banks": 2,
        "shrtft2": -10.0,
        "longft2": 5.0,
    })
    assert result["shrtft2"] == -10.0
    assert result["longft2"] == 5.0


# ======================================================================
# Error message tests
# ======================================================================

def test_error_message_includes_field_and_bounds():
    validator = _make_validator()
    with pytest.raises(PIDValidationError) as exc_info:
        validator.validate_and_convert({"engine_rpm": 9000})
    msg = str(exc_info.value)
    assert "engine_rpm" in msg
    assert "8000" in msg


def test_bank2_error_message_includes_contract_reference():
    validator = _make_validator()
    with pytest.raises(PIDValidationError) as exc_info:
        validator.validate_and_convert({
            "number_of_banks": 1,
            "shrtft2": 0.0,
            "longft2": None,
        })
    assert "SEMANTIC_CONTRACT" in str(exc_info.value)


def test_fuel_system_status_mapping():
    validator = _make_validator()
    from obdlab.schemas.vocabulary import FuelSystemStatus

    # Test mapping of valid strings and enum values
    cases = [
        ("Closed_Loop", FuelSystemStatus.CL),
        ("Open_Loop_Cold", FuelSystemStatus.OL),
        ("Open_Loop_Fault", FuelSystemStatus.OL_FAULT),
        ("Open_Loop_Driving", FuelSystemStatus.OL_DRIVE),
        ("CL", FuelSystemStatus.CL),
        ("OL", FuelSystemStatus.OL),
        ("OL_DRIVE", FuelSystemStatus.OL_DRIVE),
        ("OL_FAULT", FuelSystemStatus.OL_FAULT),
        (FuelSystemStatus.CL, FuelSystemStatus.CL),
    ]
    for raw_val, expected_enum in cases:
        # Test input via fuel_system_status
        res1 = validator.validate_and_convert({"fuel_system_status": raw_val})
        assert res1["fuel_system_status"] == expected_enum
        assert res1["fuel_sys_status"] == expected_enum

        # Test input via fuel_sys_status
        res2 = validator.validate_and_convert({"fuel_sys_status": raw_val})
        assert res2["fuel_system_status"] == expected_enum
        assert res2["fuel_sys_status"] == expected_enum

    # Test invalid values raise PIDValidationError
    with pytest.raises(PIDValidationError):
        validator.validate_and_convert({"fuel_system_status": "Invalid_Status"})


# ======================================================================
# per_cylinder_misfire_counts tests
# ======================================================================

def test_misfire_counts_default_none():
    validator = _make_validator()
    result = validator.validate_and_convert({})
    assert result["per_cylinder_misfire_counts"] is None


def test_misfire_counts_valid_dict():
    validator = _make_validator()
    raw = {"per_cylinder_misfire_counts": {1: 0, 2: 15, 3: 100, 4: 5}}  # wiki: research/chunks/fuel-trim/17
    result = validator.validate_and_convert(raw)
    assert result["per_cylinder_misfire_counts"] == {1: 0, 2: 15, 3: 100, 4: 5}  # wiki: research/chunks/fuel-trim/17


def test_misfire_counts_valid_string_conversion():
    validator = _make_validator()
    raw = {"per_cylinder_misfire_counts": {"1": "0", "2": "15"}}
    result = validator.validate_and_convert(raw)
    assert result["per_cylinder_misfire_counts"] == {1: 0, 2: 15}  # wiki: research/chunks/fuel-trim/17


def test_misfire_counts_invalid_type():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="expected dict"):
        validator.validate_and_convert({"per_cylinder_misfire_counts": "not-a-dict"})


def test_misfire_counts_invalid_cylinder_index():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="cylinder index must be >= 1"):
        validator.validate_and_convert({"per_cylinder_misfire_counts": {0: 10}})  # wiki: research/chunks/fuel-trim/17


def test_misfire_counts_invalid_misfire_value():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="must be non-negative"):
        validator.validate_and_convert({"per_cylinder_misfire_counts": {1: -1}})  # wiki: research/chunks/fuel-trim/17


def test_misfire_counts_non_numeric_keys():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="cylinder key must be integer"):
        validator.validate_and_convert({"per_cylinder_misfire_counts": {"abc": 10}})  # wiki: research/chunks/fuel-trim/17


def test_misfire_counts_non_numeric_values():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="misfire count for cylinder .* must be integer"):
        validator.validate_and_convert({"per_cylinder_misfire_counts": {1: "abc"}})  # wiki: research/chunks/fuel-trim/17


# ======================================================================
# number_of_banks default-to-1 alignment tests
# ======================================================================

def test_bank2_omitted_defaults_to_one_bank_success():
    validator = _make_validator()
    result = validator.validate_and_convert({
        "shrtft2": None,
        "longft2": None,
    })
    assert "shrtft2" not in result or result["shrtft2"] is None
    assert "longft2" not in result or result["longft2"] is None


def test_bank2_omitted_defaults_to_one_bank_raises_on_non_null_shrtft2():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="shrtft2 must be null when number_of_banks == 1"):
        validator.validate_and_convert({
            "shrtft2": 0.0,
            "longft2": None,
        })


def test_bank2_omitted_defaults_to_one_bank_raises_on_non_null_longft2():
    validator = _make_validator()
    with pytest.raises(PIDValidationError, match="longft2 must be null when number_of_banks == 1"):
        validator.validate_and_convert({
            "shrtft2": None,
            "longft2": 0.0,
        })


