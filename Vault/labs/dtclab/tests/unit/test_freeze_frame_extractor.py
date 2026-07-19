"""Unit tests for freeze_frame_extractor — FreezeFrameRecord + derived flags.

Covers: valid 12-PID fixture, each derived flag on boundary values,
missing mandatory PID error, extended PIDs optional, codes_cleared
propagation, string→enum coercion for fuel_system_status.
"""

from __future__ import annotations

import pytest

from pydantic import ValidationError

from dtclab.core.freeze_frame_extractor import (
    FreezeFrameIncompleteError,
    extract_freeze_frame,
)
from dtclab.schemas.freeze_frame import FreezeFrameRecord
from dtclab.schemas.vocabulary import FuelSystemStatus


# ------------------------------------------------------------------
# Shared fixture — a fully populated 12-PID dict (warm, CL, normal driving)
# ------------------------------------------------------------------


def _valid_raw(**overrides):
    """Return a valid 12-mandatory-PID raw dict, with optional overrides."""
    data = {
        "calculated_load_pct": 35.0,
        "engine_rpm": 1200,
        "coolant_temp_c": 88.0,
        "short_term_ft1": 1.5,
        "long_term_ft1": -2.0,
        "manifold_pressure_kpa": 42.0,
        "vehicle_speed_kmh": 60,
        "ignition_advance_deg": 8.0,
        "intake_air_temp_c": 32.0,
        "maf_gps": 4.8,
        "throttle_pos_pct": 22.0,
        "fuel_system_status": FuelSystemStatus.CL,
    }
    data.update(overrides)
    return data


# ======================================================================
# Valid fixture — happy path
# ======================================================================


class TestValidFixture:
    def test_all_12_pids_parse_cleanly(self):
        ff = extract_freeze_frame(_valid_raw())
        assert ff.calculated_load_pct == 35.0
        assert ff.engine_rpm == 1200
        assert ff.coolant_temp_c == 88.0
        assert ff.short_term_ft1 == 1.5
        assert ff.long_term_ft1 == -2.0
        assert ff.manifold_pressure_kpa == 42.0
        assert ff.vehicle_speed_kmh == 60
        assert ff.ignition_advance_deg == 8.0
        assert ff.intake_air_temp_c == 32.0
        assert ff.maf_gps == 4.8
        assert ff.throttle_pos_pct == 22.0
        assert ff.fuel_system_status == FuelSystemStatus.CL

    def test_warm_closed_loop_no_flags(self):
        """Normal warm driving should set zero derived flags."""
        ff = extract_freeze_frame(_valid_raw())
        assert ff.ff_open_loop_at_fault is False
        assert ff.ff_load_high_at_low_rpm is False
        assert ff.ff_ect_warmup is False
        assert ff.ff_iat_ect_biased is False
        assert ff.ff_timing_retard_severe is False
        assert ff.ff_codes_cleared_invalidated is False
        assert ff.ff_fuel_spark_cut_at_crank is False


# ======================================================================
# ff_open_loop_at_fault
# ======================================================================


class TestFlagOpenLoop:
    def test_ol_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(fuel_system_status=FuelSystemStatus.OL)
        )
        assert ff.ff_open_loop_at_fault is True

    def test_ol_fault_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(fuel_system_status=FuelSystemStatus.OL_FAULT)
        )
        assert ff.ff_open_loop_at_fault is True

    def test_ol_drive_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(fuel_system_status=FuelSystemStatus.OL_DRIVE)
        )
        assert ff.ff_open_loop_at_fault is True

    def test_cl_does_not_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(fuel_system_status=FuelSystemStatus.CL)
        )
        assert ff.ff_open_loop_at_fault is False


# ======================================================================
# ff_load_high_at_low_rpm
# ======================================================================


class TestFlagLoadHighLowRpm:
    def test_triggers_above_70_pct_at_low_rpm(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=80.0, engine_rpm=800)
        )
        assert ff.ff_load_high_at_low_rpm is True

    def test_boundary_70_pct_does_not_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=70.0, engine_rpm=800)
        )
        assert ff.ff_load_high_at_low_rpm is False

    def test_boundary_71_pct_does_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=71.0, engine_rpm=800)
        )
        assert ff.ff_load_high_at_low_rpm is True

    def test_rpm_1500_does_not_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=80.0, engine_rpm=1500)
        )
        assert ff.ff_load_high_at_low_rpm is False

    def test_rpm_1499_does_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=80.0, engine_rpm=1499)
        )
        assert ff.ff_load_high_at_low_rpm is True

    def test_high_rpm_no_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=85.0, engine_rpm=2500)
        )
        assert ff.ff_load_high_at_low_rpm is False

    def test_low_load_no_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(calculated_load_pct=25.0, engine_rpm=800)
        )
        assert ff.ff_load_high_at_low_rpm is False


# ======================================================================
# ff_ect_warmup
# ======================================================================


class TestFlagECTWarmup:
    def test_below_60_triggers(self):
        ff = extract_freeze_frame(_valid_raw(coolant_temp_c=50.0))
        assert ff.ff_ect_warmup is True

    def test_at_60_does_not_trigger(self):
        ff = extract_freeze_frame(_valid_raw(coolant_temp_c=60.0))
        assert ff.ff_ect_warmup is False

    def test_above_60_does_not_trigger(self):
        ff = extract_freeze_frame(_valid_raw(coolant_temp_c=88.0))
        assert ff.ff_ect_warmup is False

    def test_negative_cold_soak_triggers(self):
        ff = extract_freeze_frame(_valid_raw(coolant_temp_c=-15.0))
        assert ff.ff_ect_warmup is True


# ======================================================================
# ff_iat_ect_biased
# ======================================================================


class TestFlagIATEctBiased:
    def test_triggers_delta_above_30_at_rpm_0(self):
        ff = extract_freeze_frame(
            _valid_raw(intake_air_temp_c=85.0, coolant_temp_c=50.0, engine_rpm=0)
        )
        assert ff.ff_iat_ect_biased is True

    def test_delta_30_boundary_does_not_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(intake_air_temp_c=80.0, coolant_temp_c=50.0, engine_rpm=0)
        )
        assert ff.ff_iat_ect_biased is False

    def test_delta_31_does_trigger(self):
        ff = extract_freeze_frame(
            _valid_raw(intake_air_temp_c=81.0, coolant_temp_c=50.0, engine_rpm=0)
        )
        assert ff.ff_iat_ect_biased is True

    def test_ect_higher_than_iat_delta_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(intake_air_temp_c=10.0, coolant_temp_c=45.0, engine_rpm=0)
        )
        assert ff.ff_iat_ect_biased is True

    def test_rpm_not_zero_suppresses(self):
        ff = extract_freeze_frame(
            _valid_raw(intake_air_temp_c=85.0, coolant_temp_c=50.0, engine_rpm=1)
        )
        assert ff.ff_iat_ect_biased is False


# ======================================================================
# ff_timing_retard_severe
# ======================================================================


class TestFlagTimingRetard:
    def test_below_neg10_triggers(self):
        ff = extract_freeze_frame(_valid_raw(ignition_advance_deg=-12.0))
        assert ff.ff_timing_retard_severe is True

    def test_at_neg10_does_not_trigger(self):
        ff = extract_freeze_frame(_valid_raw(ignition_advance_deg=-10.0))
        assert ff.ff_timing_retard_severe is False

    def test_at_neg11_does_trigger(self):
        ff = extract_freeze_frame(_valid_raw(ignition_advance_deg=-11.0))
        assert ff.ff_timing_retard_severe is True

    def test_normal_advance_no_trigger(self):
        ff = extract_freeze_frame(_valid_raw(ignition_advance_deg=12.0))
        assert ff.ff_timing_retard_severe is False

    def test_zero_advance_no_trigger(self):
        ff = extract_freeze_frame(_valid_raw(ignition_advance_deg=0.0))
        assert ff.ff_timing_retard_severe is False


# ======================================================================
# ff_codes_cleared_invalidated
# ======================================================================


class TestFlagCodesCleared:
    def test_codes_cleared_true_sets_flag(self):
        ff = extract_freeze_frame(_valid_raw(), codes_cleared=True)
        assert ff.ff_codes_cleared_invalidated is True

    def test_codes_cleared_false_clears_flag(self):
        ff = extract_freeze_frame(_valid_raw(), codes_cleared=False)
        assert ff.ff_codes_cleared_invalidated is False

    def test_codes_cleared_default_is_false(self):
        ff = extract_freeze_frame(_valid_raw())
        assert ff.ff_codes_cleared_invalidated is False


# ======================================================================
# ff_fuel_spark_cut_at_crank
# ======================================================================


class TestFlagFuelSparkCutAtCrank:
    def test_declared_schema_field_round_trips(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.OL_FAULT,
                vehicle_speed_kmh=0,
                engine_rpm=0,
            )
        )
        assert "ff_fuel_spark_cut_at_crank" in FreezeFrameRecord.model_fields
        assert ff.ff_fuel_spark_cut_at_crank is True
        assert ff.model_dump()["ff_fuel_spark_cut_at_crank"] is True

    def test_ol_fault_stationary_rpm_180_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.OL_FAULT,
                vehicle_speed_kmh=0,
                engine_rpm=180,
            )
        )
        assert ff.ff_fuel_spark_cut_at_crank is True

    def test_ol_fault_stationary_rpm_zero_triggers(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.OL_FAULT,
                vehicle_speed_kmh=0,
                engine_rpm=0,
            )
        )
        assert ff.ff_fuel_spark_cut_at_crank is True

    def test_rpm_181_suppresses(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.OL_FAULT,
                vehicle_speed_kmh=0,
                engine_rpm=181,
            )
        )
        assert ff.ff_fuel_spark_cut_at_crank is False

    def test_closed_loop_suppresses(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.CL,
                vehicle_speed_kmh=0,
                engine_rpm=0,
            )
        )
        assert ff.ff_fuel_spark_cut_at_crank is False

    def test_vehicle_moving_suppresses(self):
        ff = extract_freeze_frame(
            _valid_raw(
                fuel_system_status=FuelSystemStatus.OL_FAULT,
                vehicle_speed_kmh=1,
                engine_rpm=0,
            )
        )
        assert ff.ff_fuel_spark_cut_at_crank is False


# ======================================================================
# All flags fire simultaneously
# ======================================================================


class TestAllFlags:
    def test_all_flags_simultaneous(self):
        """Cold start, open-loop fault, high-load low-rpm stall, IAT/ECT
        biased, severe timing retard, codes just cleared."""
        ff = extract_freeze_frame(
            _valid_raw(
                calculated_load_pct=85.0,
                engine_rpm=0,
                vehicle_speed_kmh=0,
                coolant_temp_c=20.0,
                intake_air_temp_c=55.0,
                ignition_advance_deg=-15.0,
                fuel_system_status=FuelSystemStatus.OL_FAULT,
            ),
            codes_cleared=True,
        )
        assert ff.ff_open_loop_at_fault is True
        assert ff.ff_load_high_at_low_rpm is True
        assert ff.ff_ect_warmup is True
        assert ff.ff_iat_ect_biased is True
        assert ff.ff_timing_retard_severe is True
        assert ff.ff_codes_cleared_invalidated is True
        assert ff.ff_fuel_spark_cut_at_crank is True


# ======================================================================
# Missing PID error
# ======================================================================


class TestMissingPIDs:
    def test_empty_dict_raises(self):
        with pytest.raises(FreezeFrameIncompleteError) as exc:
            extract_freeze_frame({})
        assert len(exc.value.missing) == 12

    def test_single_missing_raises(self):
        raw = _valid_raw()
        del raw["engine_rpm"]
        with pytest.raises(FreezeFrameIncompleteError) as exc:
            extract_freeze_frame(raw)
        assert exc.value.missing == ["engine_rpm"]

    def test_error_message_lists_missing(self):
        with pytest.raises(FreezeFrameIncompleteError) as exc:
            extract_freeze_frame({"calculated_load_pct": 50.0})
        assert "freeze frame incomplete" in str(exc.value).lower()
        assert "engine_rpm" in exc.value.missing


# ======================================================================
# Extended PIDs passthrough
# ======================================================================


class TestExtendedPIDs:
    def test_extended_pids_present(self):
        ff = extract_freeze_frame(
            _valid_raw(
                short_term_ft2=3.0,
                long_term_ft2=-1.0,
                o2_voltage_b1s1=0.45,
                barometric_pressure_kpa=101.3,
                commanded_egr_pct=0.0,
                run_time_since_start_sec=340,
                fuel_level_pct=62.0,
            )
        )
        assert ff.short_term_ft2 == 3.0
        assert ff.long_term_ft2 == -1.0
        assert ff.o2_voltage_b1s1 == 0.45
        assert ff.barometric_pressure_kpa == 101.3
        assert ff.commanded_egr_pct == 0.0
        assert ff.run_time_since_start_sec == 340
        assert ff.fuel_level_pct == 62.0

    def test_extended_pids_default_none(self):
        ff = extract_freeze_frame(_valid_raw())
        assert ff.short_term_ft2 is None
        assert ff.long_term_ft2 is None
        assert ff.o2_voltage_b1s1 is None
        assert ff.barometric_pressure_kpa is None


# ======================================================================
# String → enum coercion
# ======================================================================


class TestStringCoercion:
    def test_string_fuel_status_accepted(self):
        ff = extract_freeze_frame(
            _valid_raw(fuel_system_status="OL_FAULT")
        )
        assert ff.fuel_system_status == FuelSystemStatus.OL_FAULT

    def test_all_string_variants(self):
        for status in ("CL", "OL", "OL_DRIVE", "OL_FAULT"):
            ff = extract_freeze_frame(
                _valid_raw(fuel_system_status=status)
            )
            assert ff.fuel_system_status == FuelSystemStatus(status)


# ======================================================================
# Pydantic field constraints
# ======================================================================


class TestFieldConstraints:
    def test_negative_load_pct_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(calculated_load_pct=-1.0))

    def test_load_pct_above_100_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(calculated_load_pct=101.0))

    def test_negative_rpm_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(engine_rpm=-1))

    def test_negative_manifold_pressure_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(manifold_pressure_kpa=-0.1))

    def test_negative_vehicle_speed_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(vehicle_speed_kmh=-1))

    def test_negative_maf_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(maf_gps=-0.1))

    def test_throttle_above_100_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(throttle_pos_pct=100.1))

    def test_negative_throttle_rejected(self):
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            extract_freeze_frame(_valid_raw(throttle_pos_pct=-0.1))

    def test_coolant_temp_negative_accepted(self):
        """§12.1 explicitly permits negative coolant_temp_c."""
        ff = extract_freeze_frame(_valid_raw(coolant_temp_c=-25.0))
        assert ff.coolant_temp_c == -25.0


# ======================================================================
# Smoke test — structural verification from task prompt
# ======================================================================


class TestStructuralSmoke:
    def test_task_prompt_smoke(self):
        """Replicate the exact structural smoke test from the task file."""
        ff = extract_freeze_frame(
            {
                "calculated_load_pct": 80.0,
                "engine_rpm": 800,
                "coolant_temp_c": 50.0,
                "short_term_ft1": 5.0,
                "long_term_ft1": 3.0,
                "manifold_pressure_kpa": 35.0,
                "vehicle_speed_kmh": 0,
                "ignition_advance_deg": -12.0,
                "intake_air_temp_c": 85.0,
                "maf_gps": 2.1,
                "throttle_pos_pct": 15.0,
                "fuel_system_status": FuelSystemStatus.OL,
            },
            codes_cleared=False,
        )
        assert ff.ff_load_high_at_low_rpm is True  # 80 > 70, rpm 800 < 1500
        assert ff.ff_ect_warmup is True  # 50 < 60
        assert ff.ff_timing_retard_severe is True  # -12 < -10
        assert ff.ff_open_loop_at_fault is True  # OL


# ======================================================================
# Input robustness — M3 audit remediation
# ======================================================================


class TestInputRobustness:
    """T-FU-4: None-valued PIDs, non-numeric strings, coercible strings."""

    def test_none_valued_mandatory_pid_raises_incomplete(self):
        """A present-but-None mandatory PID is treated as missing."""
        raw = _valid_raw()
        raw["engine_rpm"] = None
        with pytest.raises(FreezeFrameIncompleteError) as exc:
            extract_freeze_frame(raw)
        assert "engine_rpm" in exc.value.missing

    def test_none_valued_pid_error_message(self):
        raw = _valid_raw()
        raw["coolant_temp_c"] = None
        with pytest.raises(FreezeFrameIncompleteError) as exc:
            extract_freeze_frame(raw)
        assert "freeze frame incomplete" in str(exc.value).lower()
        assert "coolant_temp_c" in exc.value.missing

    def test_non_numeric_string_pid_raises_validation_error(self):
        """A non-numeric PID string (e.g. 'abc') raises ValidationError."""
        raw = _valid_raw()
        raw["engine_rpm"] = "abc"
        with pytest.raises(ValidationError):
            extract_freeze_frame(raw)

    def test_non_numeric_string_load_pct_raises_validation_error(self):
        raw = _valid_raw()
        raw["calculated_load_pct"] = "not_a_number"
        with pytest.raises(ValidationError):
            extract_freeze_frame(raw)

    def test_coercible_numeric_strings_succeed(self):
        """Pydantic coerces '800' → 800 and flags derive correctly."""
        raw = _valid_raw()
        raw["engine_rpm"] = "800"
        raw["calculated_load_pct"] = "85.0"
        raw["vehicle_speed_kmh"] = "60"
        ff = extract_freeze_frame(raw)
        assert ff.engine_rpm == 800
        assert ff.calculated_load_pct == 85.0
        assert ff.vehicle_speed_kmh == 60

    def test_coercible_numeric_strings_derive_flags(self):
        """Derived flags must be correct when PIDs are supplied as strings."""
        raw = _valid_raw(
            calculated_load_pct="85.0",
            engine_rpm="800",
            ignition_advance_deg="-15.0",
            fuel_system_status="OL",
            coolant_temp_c="50.0",
        )
        ff = extract_freeze_frame(raw)
        assert ff.ff_load_high_at_low_rpm is True  # 85 > 70, 800 < 1500
        assert ff.ff_timing_retard_severe is True  # -15 < -10
        assert ff.ff_open_loop_at_fault is True  # OL
        assert ff.ff_ect_warmup is True  # 50 < 60

    def test_coercible_fuel_system_status_strings(self):
        """Pydantic coerces StrEnum from string via the record-first path."""
        for status_str in ("CL", "OL", "OL_DRIVE", "OL_FAULT"):
            raw = _valid_raw(fuel_system_status=status_str)
            ff = extract_freeze_frame(raw)
            assert ff.fuel_system_status == FuelSystemStatus(status_str)

    def test_none_in_extended_pid_is_passthrough(self):
        """None in extended PID is passthrough (not mandatory)."""
        raw = _valid_raw(fuel_level_pct=None)
        ff = extract_freeze_frame(raw)
        assert ff.fuel_level_pct is None
