"""Unit tests for digital_parser.py (M1) — DTC, OBD PID, freeze frame parsing.

Covers: DTC exact/family/prefix mapping, OBD trim/O2/bank-symmetry symptoms,
fuel-status gate (L18), freeze-frame symptom derivation, cold-engine flag,
breathing efficiency, deduplication, and golden-output integration tests
derived from corpus cases.
"""

from __future__ import annotations

import pytest

from engine.v2.digital_parser import (
    _compute_breathing_efficiency,
    _compute_open_loop_suppression,
    _extract_baro,
    _extract_ect,
    _extract_fuel_status,
    _extract_map,
    _map_dtc,
    _parse_dtcs,
    _parse_freeze_frame,
    _parse_o2_symptoms,
    _parse_obd_pids,
    _parse_trim_symptoms,
    parse_digital,
)
from engine.v2.dna_core import DNAOutput
from engine.v2.input_model import (
    DiagnosticInput,
    FreezeFrameRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)

# ── helpers ─────────────────────────────────────────────────────────────────

def _ctx(my: int = 2012) -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN", model="Golf", engine_code="EA111_1.2_TSI",
        displacement_cc=1197, my=my,
    )


def _dna_output() -> DNAOutput:
    return DNAOutput(
        engine_state="warm_closed_loop",
        era_bucket="ERA_CAN",
        tech_mask={"has_vvt": True, "has_gdi": True, "has_turbo": True,
                    "is_v_engine": False, "has_egr": False, "has_secondary_air": False},
        o2_type="wideband",
        target_rpm_u2=2500,
        target_lambda_v112=1.000,
        vref_missing=False,
        confidence_ceiling=0.95,
    )


def _validated(
    dtcs: list[str] | None = None,
    obd: OBDRecord | None = None,
    ff: FreezeFrameRecord | None = None,
    displacement_cc: int = 1595,
    my: int = 2005,
) -> ValidatedInput:
    return ValidatedInput(
        raw=DiagnosticInput(
            vehicle_context=VehicleContext(
                brand="VW", model="Golf", engine_code="EA113_1.6",
                displacement_cc=displacement_cc, my=my,
            ),
            dtcs=dtcs or [],
            analyser_type="5-gas",
            obd=obd,
            freeze_frame=ff,
        ),
        valid_channels={"obd", "dtcs", "freeze_frame"},
    )


# ═══════════════════════════════════════════════════════════════════════════════
# DTC mapping
# ═══════════════════════════════════════════════════════════════════════════════

class TestDtcExactMatch:
    def test_p0171_exact(self) -> None:
        assert _map_dtc("P0171") == "SYM_DTC_P0171"

    def test_p0172_exact(self) -> None:
        assert _map_dtc("P0172") == "SYM_DTC_P0172"

    def test_p0401_exact(self) -> None:
        assert _map_dtc("P0401") == "SYM_DTC_EGR"

    def test_p0101_exact(self) -> None:
        assert _map_dtc("P0101") == "SYM_DTC_INDUCTION"

    def test_p0053_exact(self) -> None:
        assert _map_dtc("P0053") == "SYM_DTC_HO2S_HEATER"

    def test_case_insensitive_via_parse_dtcs(self) -> None:
        """_map_dtc expects uppercase; normalization happens in _parse_dtcs."""
        assert _parse_dtcs(["p0171"]) == ["SYM_DTC_P0171"]


class TestDtcFamilyMatch:
    def test_p0420_catalyst(self) -> None:
        assert _map_dtc("P0420") == "SYM_DTC_CATALYST"

    def test_p0430_catalyst(self) -> None:
        assert _map_dtc("P0430") == "SYM_DTC_CATALYST"

    def test_p0300_misfire(self) -> None:
        assert _map_dtc("P0300") == "SYM_DTC_MISFIRE"

    def test_p0305_misfire(self) -> None:
        assert _map_dtc("P0305") == "SYM_DTC_MISFIRE"

    def test_p0201_injector(self) -> None:
        assert _map_dtc("P0201") == "SYM_DTC_INJECTOR"

    def test_p0299_boost(self) -> None:
        assert _map_dtc("P0299") == "SYM_DTC_BOOST"

    def test_p0234_boost(self) -> None:
        assert _map_dtc("P0234") == "SYM_DTC_BOOST"

    def test_p0011_camshaft(self) -> None:
        assert _map_dtc("P0011") == "SYM_DTC_CAMSHAFT_TIMING"

    def test_p0324_knock(self) -> None:
        assert _map_dtc("P0324") == "SYM_DTC_KNOCK_SENSOR"


class TestDtcPrefixMatch:
    def test_p0606_ecu_internal(self) -> None:
        assert _map_dtc("P0606") == "SYM_DTC_ECU_INTERNAL"

    def test_p0610_ecu_internal(self) -> None:
        assert _map_dtc("P0610") == "SYM_DTC_ECU_INTERNAL"

    def test_p0100_sensor(self) -> None:
        assert _map_dtc("P0100") == "SYM_DTC_SENSOR"

    def test_p0102_sensor(self) -> None:
        assert _map_dtc("P0102") == "SYM_DTC_SENSOR"

    def test_p0101_not_sensor_prefix(self) -> None:
        """P0101 has an exact match so prefix P01 should NOT apply."""
        assert _map_dtc("P0101") == "SYM_DTC_INDUCTION"


class TestDtcUnknown:
    def test_unknown_returns_none(self) -> None:
        assert _map_dtc("P0999") is None

    def test_empty_string(self) -> None:
        assert _map_dtc("") is None


class TestParseDtcs:
    def test_multiple_dtcs(self) -> None:
        result = _parse_dtcs(["P0171", "P0420", "P0999", "P0302"])
        assert result == ["SYM_DTC_P0171", "SYM_DTC_CATALYST", "SYM_DTC_MISFIRE"]

    def test_empty_list(self) -> None:
        assert _parse_dtcs([]) == []

    def test_whitespace_stripped(self) -> None:
        assert _parse_dtcs([" P0171 "]) == ["SYM_DTC_P0171"]


# ═══════════════════════════════════════════════════════════════════════════════
# Fuel-status gate (L18)
# ═══════════════════════════════════════════════════════════════════════════════

class TestExtractFuelStatus:
    def test_from_obd(self) -> None:
        obd = OBDRecord(fuel_status="CL")
        assert _extract_fuel_status(obd, None) == "CL"

    def test_from_ff_fallback(self) -> None:
        ff = FreezeFrameRecord(fuel_status="OL_FAULT")
        assert _extract_fuel_status(None, ff) == "OL_FAULT"

    def test_obd_priority_over_ff(self) -> None:
        obd = OBDRecord(fuel_status="CL")
        ff = FreezeFrameRecord(fuel_status="OL_DRIVE")
        assert _extract_fuel_status(obd, ff) == "CL"

    def test_both_none(self) -> None:
        assert _extract_fuel_status(None, None) is None


class TestExtractEct:
    def test_from_obd(self) -> None:
        obd = OBDRecord(ect_c=90.0)
        assert _extract_ect(obd, None) == 90.0

    def test_from_ff_fallback(self) -> None:
        ff = FreezeFrameRecord(ect_c=65.0)
        assert _extract_ect(None, ff) == 65.0

    def test_both_none(self) -> None:
        assert _extract_ect(None, None) is None


class TestOpenLoopSuppression:
    def test_ol_fault_warm_suppressed(self) -> None:
        assert _compute_open_loop_suppression("OL_FAULT", 90.0) is True

    def test_ol_drive_warm_suppressed(self) -> None:
        assert _compute_open_loop_suppression("OL_DRIVE", 85.0) is True

    def test_ol_warm_suppressed(self) -> None:
        assert _compute_open_loop_suppression("OL", 80.0) is True

    def test_open_loop_cold_not_suppressed(self) -> None:
        assert _compute_open_loop_suppression("OL_FAULT", 30.0) is False

    def test_closed_loop_not_suppressed(self) -> None:
        assert _compute_open_loop_suppression("CL", 90.0) is False

    def test_no_fuel_status_not_suppressed(self) -> None:
        assert _compute_open_loop_suppression(None, 90.0) is False

    def test_no_ect_not_suppressed(self) -> None:
        assert _compute_open_loop_suppression("OL_FAULT", None) is False

    def test_case_insensitive(self) -> None:
        assert _compute_open_loop_suppression("ol_fault", 90.0) is True


# ═══════════════════════════════════════════════════════════════════════════════
# OBD trim symptoms
# ═══════════════════════════════════════════════════════════════════════════════

class TestTrimSymptoms:
    def test_stft_positive_high(self) -> None:
        obd = OBDRecord(stft_b1=18.0, ltft_b1=5.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_POSITIVE_HIGH" in result

    def test_stft_negative_high(self) -> None:
        obd = OBDRecord(stft_b1=-18.0, ltft_b1=-5.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_NEGATIVE_HIGH" in result

    def test_ltft_positive_high(self) -> None:
        obd = OBDRecord(stft_b1=5.0, ltft_b1=18.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_POSITIVE_HIGH" in result

    def test_ltft_negative_high(self) -> None:
        obd = OBDRecord(stft_b1=-5.0, ltft_b1=-18.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_NEGATIVE_HIGH" in result

    def test_trim_sum_positive_high(self) -> None:
        obd = OBDRecord(stft_b1=8.0, ltft_b1=8.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_SUM_POSITIVE_HIGH" in result

    def test_trim_sum_negative_high(self) -> None:
        obd = OBDRecord(stft_b1=-8.0, ltft_b1=-8.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_SUM_NEGATIVE_HIGH" in result

    def test_normal_trims_no_symptoms(self) -> None:
        obd = OBDRecord(stft_b1=2.0, ltft_b1=1.0)
        result = _parse_trim_symptoms(obd)
        assert result == []

    def test_stft_b2_positive_high(self) -> None:
        obd = OBDRecord(stft_b1=2.0, stft_b2=18.0)
        result = _parse_trim_symptoms(obd)
        assert "SYM_TRIM_POSITIVE_HIGH" in result

    def test_all_none_trims(self) -> None:
        obd = OBDRecord()
        result = _parse_trim_symptoms(obd)
        assert result == []

    def test_does_not_duplicate_same_symptom(self) -> None:
        """Both STFT and LTFT high positive should emit one symptom."""
        obd = OBDRecord(stft_b1=18.0, ltft_b1=18.0)
        result = _parse_trim_symptoms(obd)
        assert result.count("SYM_TRIM_POSITIVE_HIGH") == 1


# ═══════════════════════════════════════════════════════════════════════════════
# O2 sensor symptoms
# ═══════════════════════════════════════════════════════════════════════════════

class TestO2Symptoms:
    def test_upstream_lazy(self) -> None:
        obd = OBDRecord(o2_voltage_b1=0.5)
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_UPSTREAM_LAZY" in result

    def test_upstream_not_lazy_high(self) -> None:
        obd = OBDRecord(o2_voltage_b1=0.8)
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_UPSTREAM_LAZY" not in result

    def test_upstream_not_lazy_low(self) -> None:
        obd = OBDRecord(o2_voltage_b1=0.2)
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_UPSTREAM_LAZY" not in result

    def test_upstream_b1_none(self) -> None:
        obd = OBDRecord()
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_UPSTREAM_LAZY" not in result

    def test_downstream_active_with_catalyst_dtc(self) -> None:
        obd = OBDRecord(o2_voltage_b2=0.5)
        result = _parse_o2_symptoms(obd, ["P0420"])
        assert "SYM_O2_DOWNSTREAM_ACTIVE" in result

    def test_downstream_steady_without_catalyst_dtc(self) -> None:
        obd = OBDRecord(o2_voltage_b2=0.5)
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_DOWNSTREAM_STEADY" in result

    def test_downstream_steady_high_voltage(self) -> None:
        obd = OBDRecord(o2_voltage_b2=0.75)
        result = _parse_o2_symptoms(obd, [])
        assert "SYM_O2_DOWNSTREAM_STEADY" in result

    def test_downstream_b2_none(self) -> None:
        obd = OBDRecord(o2_voltage_b1=0.5)
        result = _parse_o2_symptoms(obd, ["P0420"])
        assert "SYM_O2_DOWNSTREAM_ACTIVE" not in result
        assert "SYM_O2_DOWNSTREAM_STEADY" not in result


# ═══════════════════════════════════════════════════════════════════════════════
# Bank symmetry
# ═══════════════════════════════════════════════════════════════════════════════

class TestBankSymmetry:
    def test_global_both_banks_positive(self) -> None:
        obd = OBDRecord(stft_b1=8.0, ltft_b1=8.0, stft_b2=7.0, ltft_b2=7.0)
        result = _parse_obd_pids(obd, False, [])
        assert "SYM_TRIM_GLOBAL_BOTH_BANKS" in result

    def test_global_both_banks_negative(self) -> None:
        obd = OBDRecord(stft_b1=-8.0, ltft_b1=-8.0, stft_b2=-7.0, ltft_b2=-7.0)
        result = _parse_obd_pids(obd, False, [])
        assert "SYM_TRIM_GLOBAL_BOTH_BANKS" in result

    def test_local_one_bank(self) -> None:
        obd = OBDRecord(stft_b1=0.0, ltft_b1=0.0, stft_b2=8.0, ltft_b2=8.0)
        result = _parse_obd_pids(obd, False, [])
        assert "SYM_TRIM_LOCAL_ONE_BANK" in result

    def test_bank2_lean(self) -> None:
        obd = OBDRecord(stft_b1=0.0, ltft_b1=0.0, stft_b2=8.0, ltft_b2=8.0)
        result = _parse_obd_pids(obd, False, [])
        assert "SYM_BANK2_LEAN" in result

    def test_bank2_rich(self) -> None:
        obd = OBDRecord(stft_b1=0.0, ltft_b1=0.0, stft_b2=-8.0, ltft_b2=-8.0)
        result = _parse_obd_pids(obd, False, [])
        assert "SYM_BANK2_RICH" in result

    def test_insufficient_data_returns_empty(self) -> None:
        obd = OBDRecord(stft_b1=5.0)  # only one bank, missing others
        result = _parse_obd_pids(obd, False, [])
        syms = [s for s in result if s.startswith("SYM_TRIM_") and "BANK" in s]
        assert syms == []


# ═══════════════════════════════════════════════════════════════════════════════
# OBD open-loop suppression (L18)
# ═══════════════════════════════════════════════════════════════════════════════

class TestObdOpenLoopSuppression:
    def test_trim_symptoms_suppressed_in_open_loop(self) -> None:
        obd = OBDRecord(stft_b1=18.0, ltft_b1=18.0, stft_b2=8.0, ltft_b2=8.0,
                        o2_voltage_b1=0.5)
        result = _parse_obd_pids(obd, True, [])
        assert "SYM_TRIM_POSITIVE_HIGH" not in result
        assert "SYM_TRIM_SUM_POSITIVE_HIGH" not in result
        assert "SYM_TRIM_GLOBAL_BOTH_BANKS" not in result
        assert "SYM_TRIM_LOCAL_ONE_BANK" not in result

    def test_o2_symptoms_still_fire_in_open_loop(self) -> None:
        obd = OBDRecord(o2_voltage_b1=0.5)
        result = _parse_obd_pids(obd, True, [])
        assert "SYM_O2_UPSTREAM_LAZY" in result


# ═══════════════════════════════════════════════════════════════════════════════
# Freeze frame symptoms
# ═══════════════════════════════════════════════════════════════════════════════

class TestFreezeFrameSymptoms:
    def test_open_loop_at_fault(self) -> None:
        ff = FreezeFrameRecord(fuel_status="OL_FAULT")
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_OPEN_LOOP_AT_FAULT" in result

    def test_high_load_at_low_rpm(self) -> None:
        ff = FreezeFrameRecord(load_pct=85.0, rpm=1200)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_LOAD_HIGH_AT_LOW_RPM" in result

    def test_load_not_high_enough(self) -> None:
        ff = FreezeFrameRecord(load_pct=60.0, rpm=1200)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_LOAD_HIGH_AT_LOW_RPM" not in result

    def test_rpm_not_low_enough(self) -> None:
        ff = FreezeFrameRecord(load_pct=85.0, rpm=1600)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_LOAD_HIGH_AT_LOW_RPM" not in result

    def test_ect_warmup(self) -> None:
        ff = FreezeFrameRecord(ect_c=50.0)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_ECT_WARMUP" in result

    def test_ect_above_warmup(self) -> None:
        ff = FreezeFrameRecord(ect_c=85.0)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_ECT_WARMUP" not in result

    def test_iat_ect_biased_at_zero_rpm(self) -> None:
        ff = FreezeFrameRecord(iat_c=80.0, ect_c=40.0, rpm=0)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_IAT_ECT_BIASED" in result

    def test_iat_ect_not_biased_when_running(self) -> None:
        ff = FreezeFrameRecord(iat_c=80.0, ect_c=40.0, rpm=800)
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_IAT_ECT_BIASED" not in result

    def test_empty_ff(self) -> None:
        ff = FreezeFrameRecord()
        result = _parse_freeze_frame(ff)
        assert result == []

    def test_case_insensitive_fuel_status(self) -> None:
        ff = FreezeFrameRecord(fuel_status="ol_drive")
        result = _parse_freeze_frame(ff)
        assert "SYM_FF_OPEN_LOOP_AT_FAULT" in result


# ═══════════════════════════════════════════════════════════════════════════════
# Breathing efficiency
# ═══════════════════════════════════════════════════════════════════════════════

class TestBreathingEfficiency:
    def test_normal_efficiency(self) -> None:
        obd = OBDRecord(map_kpa=50.0, baro_kpa=100.0)
        result = _compute_breathing_efficiency(obd, None, 2000)
        assert result == pytest.approx(0.5)

    def test_boosted(self) -> None:
        obd = OBDRecord(map_kpa=150.0, baro_kpa=100.0)
        result = _compute_breathing_efficiency(obd, None, 2000)
        assert result == pytest.approx(1.5)

    def test_missing_map_returns_none(self) -> None:
        obd = OBDRecord(baro_kpa=100.0)
        result = _compute_breathing_efficiency(obd, None, 2000)
        assert result is None

    def test_missing_baro_returns_none(self) -> None:
        obd = OBDRecord(map_kpa=50.0)
        result = _compute_breathing_efficiency(obd, None, 2000)
        assert result is None

    def test_baro_zero_returns_none(self) -> None:
        obd = OBDRecord(map_kpa=50.0, baro_kpa=0.0)
        result = _compute_breathing_efficiency(obd, None, 2000)
        assert result is None

    def test_ff_fallback(self) -> None:
        ff = FreezeFrameRecord(map_kpa=50.0, baro_kpa=100.0)
        result = _compute_breathing_efficiency(None, ff, 2000)
        assert result == pytest.approx(0.5)


class TestExtractMap:
    def test_from_obd(self) -> None:
        assert _extract_map(OBDRecord(map_kpa=50.0), None) == 50.0

    def test_from_ff(self) -> None:
        assert _extract_map(None, FreezeFrameRecord(map_kpa=60.0)) == 60.0

    def test_both_none(self) -> None:
        assert _extract_map(None, None) is None


class TestExtractBaro:
    def test_from_obd(self) -> None:
        assert _extract_baro(OBDRecord(baro_kpa=101.0), None) == 101.0

    def test_from_ff(self) -> None:
        assert _extract_baro(None, FreezeFrameRecord(baro_kpa=99.0)) == 99.0

    def test_both_none(self) -> None:
        assert _extract_baro(None, None) is None


# ═══════════════════════════════════════════════════════════════════════════════
# Integration — parse_digital golden-output tests
# ═══════════════════════════════════════════════════════════════════════════════

class TestParseDigitalIntegration:
    def test_cold_engine_flag(self) -> None:
        """ECT below 75°C should set cold_engine=True and emit CTX symptom."""
        vi = _validated(obd=OBDRecord(ect_c=30.0, rpm=800))
        result = parse_digital(vi, _dna_output())
        assert result.cold_engine is True
        assert "SYM_CTX_COLD_ENGINE" in result.symptoms

    def test_warm_engine_no_cold_flag(self) -> None:
        vi = _validated(obd=OBDRecord(ect_c=90.0, rpm=800))
        result = parse_digital(vi, _dna_output())
        assert result.cold_engine is False
        assert "SYM_CTX_COLD_ENGINE" not in result.symptoms

    def test_open_loop_warm_trims_suppressed(self) -> None:
        """L18: warm engine + open loop = trim suppression."""
        vi = _validated(
            dtcs=["P0171"],
            obd=OBDRecord(
                fuel_status="OL_FAULT", ect_c=90.0,
                stft_b1=18.0, ltft_b1=18.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert result.open_loop_suppression is True
        assert "SYM_TRIM_POSITIVE_HIGH" not in result.symptoms
        assert "SYM_DTC_P0171" in result.symptoms

    def test_closed_loop_trims_active(self) -> None:
        vi = _validated(
            obd=OBDRecord(
                fuel_status="CL", ect_c=90.0,
                stft_b1=18.0, ltft_b1=5.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert result.open_loop_suppression is False
        assert "SYM_TRIM_POSITIVE_HIGH" in result.symptoms

    def test_deduplication(self) -> None:
        """Duplicate symptoms from different paths should be collapsed."""
        vi = _validated(
            dtcs=["P0171"],
            obd=OBDRecord(ect_c=30.0, rpm=800),
        )
        # If somehow P0171 appeared twice, dedup ensures one
        result = parse_digital(vi, _dna_output())
        assert result.symptoms.count("SYM_DTC_P0171") == 1
        assert result.symptoms.count("SYM_CTX_COLD_ENGINE") == 1

    def test_no_inputs_empty_output(self) -> None:
        vi = _validated()
        result = parse_digital(vi, _dna_output())
        assert result.symptoms == []
        assert result.open_loop_suppression is False
        assert result.cold_engine is False

    def test_corpus_csv041_physical_rich_ecu_sees_lean(self) -> None:
        """CSV-041: Physical rich; ECU sees lean — P0171, perception gap.
        STFT +25%, LTFT +15% = strong positive trim, both banks."""
        vi = _validated(
            dtcs=["P0171"],
            obd=OBDRecord(
                stft_b1=25.0, ltft_b1=15.0, stft_b2=20.0, ltft_b2=10.0,
                o2_voltage_b1=0.1, o2_voltage_b2=0.5,  # B1 low (rich), B2 mid
                fuel_status="CL", ect_c=90.0, rpm=2500,
                map_kpa=45.0, baro_kpa=100.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_DTC_P0171" in result.symptoms
        assert "SYM_TRIM_POSITIVE_HIGH" in result.symptoms
        assert result.open_loop_suppression is False

    def test_corpus_csv022_misfire_p0302(self) -> None:
        """CSV-022: HC>>1000 + O2 = misfire with P0302 DTC."""
        vi = _validated(
            dtcs=["P0302"],
            obd=OBDRecord(
                fuel_status="CL", ect_c=90.0, rpm=800,
                stft_b1=10.0, ltft_b1=5.0,
                map_kpa=35.0, baro_kpa=100.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_DTC_MISFIRE" in result.symptoms

    def test_corpus_csv025_oscillating_trims(self) -> None:
        """CSV-025: Oscillating trims; gas clean — Lazy O2 sensor aging.
        STFT +10%, LTFT -10% with O2 voltage mid-range (lazy).
        Trim sum = 0 — within ±10% band, so no trim-sum symptom fires."""
        vi = _validated(
            obd=OBDRecord(
                stft_b1=10.0, ltft_b1=-10.0,
                o2_voltage_b1=0.5, o2_voltage_b2=0.5,
                fuel_status="CL", ect_c=90.0, rpm=800,
                map_kpa=35.0, baro_kpa=100.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_O2_UPSTREAM_LAZY" in result.symptoms
        assert "SYM_TRIM_SUM_NEGATIVE_HIGH" not in result.symptoms

    def test_corpus_csv018_rich_co_ecu_correcting(self) -> None:
        """CSV-018: Rich CO; ECU correcting negatively — P0172.
        STFT -15%, LTFT -10%: STFT not < -15 (exclusive threshold),
        but trim sum -25 < -10 fires SYM_TRIM_SUM_NEGATIVE_HIGH."""
        vi = _validated(
            dtcs=["P0172"],
            obd=OBDRecord(
                stft_b1=-15.0, ltft_b1=-10.0,
                fuel_status="CL", ect_c=90.0, rpm=800,
                map_kpa=35.0, baro_kpa=100.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_DTC_P0172" in result.symptoms
        assert "SYM_TRIM_SUM_NEGATIVE_HIGH" in result.symptoms

    def test_multiple_dtc_families(self) -> None:
        """DTCs from different families should all map."""
        vi = _validated(
            dtcs=["P0420", "P0301", "P0299", "P0203"],
            obd=OBDRecord(fuel_status="CL", ect_c=90.0),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_DTC_CATALYST" in result.symptoms
        assert "SYM_DTC_MISFIRE" in result.symptoms
        assert "SYM_DTC_BOOST" in result.symptoms
        assert "SYM_DTC_INJECTOR" in result.symptoms

    def test_breathing_efficiency_in_output(self) -> None:
        vi = _validated(
            obd=OBDRecord(map_kpa=60.0, baro_kpa=100.0, fuel_status="CL", ect_c=90.0),
        )
        result = parse_digital(vi, _dna_output())
        assert result.breathing_cluster_efficiency == pytest.approx(0.6)

    def test_codes_cleared_default_false(self) -> None:
        vi = _validated()
        result = parse_digital(vi, _dna_output())
        assert result.codes_cleared is False

    def test_ff_open_loop_with_dtcs(self) -> None:
        """Freeze frame showing open loop at fault + DTCs."""
        vi = _validated(
            dtcs=["P0420"],
            ff=FreezeFrameRecord(fuel_status="OL_FAULT", ect_c=90.0, load_pct=85.0, rpm=1200),
        )
        result = parse_digital(vi, _dna_output())
        assert "SYM_DTC_CATALYST" in result.symptoms
        assert "SYM_FF_OPEN_LOOP_AT_FAULT" in result.symptoms
        assert "SYM_FF_LOAD_HIGH_AT_LOW_RPM" in result.symptoms

    def test_cold_open_loop_no_trim_suppression(self) -> None:
        """Cold engine + open loop: trim suppression should be False
        (ECT below 75°C threshold)."""
        vi = _validated(
            obd=OBDRecord(
                fuel_status="OL_DRIVE", ect_c=40.0,
                stft_b1=18.0, ltft_b1=18.0,
            ),
        )
        result = parse_digital(vi, _dna_output())
        assert result.open_loop_suppression is False
        assert result.cold_engine is True
        assert "SYM_CTX_COLD_ENGINE" in result.symptoms
