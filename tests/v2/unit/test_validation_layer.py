"""Unit tests for validation.py -- VL categories 1–11, boundary cases, 100% coverage.

Covers v2-validation-layer §5 boundary catalogue.
"""

from __future__ import annotations

import pytest

from engine.v2.input_model import (
    DiagnosticInput,
    FreezeFrameRecord,
    GasRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)
from engine.v2.validation import (
    _cat2_gas_sum,
    _cat3_probe_air,
    _cat5_dtc_era,
    validate,
)

# ── fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def ctx_default() -> VehicleContext:
    return VehicleContext(
        brand="VW", model="Golf", engine_code="EA113_1.6", displacement_cc=1595, my=2005
    )


@pytest.fixture
def gas_clean() -> GasRecord:
    return GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0)


@pytest.fixture
def obd_default() -> OBDRecord:
    return OBDRecord(
        rpm=800, ect_c=85.0, map_kpa=35.0, stft_b1=2.0, ltft_b1=1.0,
        fuel_status="CL", obd_lambda=1.0, baro_kpa=101.0, iat_c=30.0, load_pct=25.0,
    )


@pytest.fixture
def input_minimal(ctx_default: VehicleContext) -> DiagnosticInput:
    return DiagnosticInput(
        vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Category 1 -- Range
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory1Range:
    """Physical bounds validation -- VL category 1."""

    def test_ect_150_pass(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=150.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_ect_151_reject(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=151.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_map_10_pass(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(map_kpa=10.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_map_9_reject(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(map_kpa=9.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_obd_ect_minus40_pass(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=-40.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_obd_ect_minus41_reject(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=-41.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_gas_idle_all_valid_accepted(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels

    def test_gas_idle_co_out_of_range_rejected(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=16.0, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
        )
        vi = validate(inp)
        assert "gas_idle" not in vi.valid_channels

    def test_gas_high_rejected_on_bad_nox(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_high=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0,
                               nox_ppm=6000.0),
        )
        vi = validate(inp)
        assert "gas_high" not in vi.valid_channels

    def test_gas_idle_nox_none_allowed(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0,
                               nox_ppm=None, lambda_analyser=None),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels

    def test_gas_high_lambda_out_of_range_rejected(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_high=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0,
                               lambda_analyser=2.5),
        )
        vi = validate(inp)
        assert "gas_high" not in vi.valid_channels

    def test_ff_out_of_range_rejected(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            freeze_frame=FreezeFrameRecord(ect_c=151.0),
        )
        vi = validate(inp)
        assert "ff" not in vi.valid_channels

    def test_ff_all_valid_accepted(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            freeze_frame=FreezeFrameRecord(
                ect_c=85.0, rpm=2500, map_kpa=60.0, stft_b1=-2.0, ltft_b1=3.0,
                load_pct=40.0, baro_kpa=100.0, iat_c=28.0, speed_kph=80,
            ),
        )
        vi = validate(inp)
        assert "ff" in vi.valid_channels

    def test_my_out_of_range_rejects_all_channels(self, ctx_default: VehicleContext) -> None:
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1985,
        )
        inp = DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
            gas_high=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
            obd=OBDRecord(ect_c=85.0), freeze_frame=FreezeFrameRecord(ect_c=85.0),
        )
        vi = validate(inp)
        assert "dtcs" in vi.invalid_channels
        assert "gas_idle" in vi.invalid_channels
        assert "gas_high" in vi.invalid_channels
        assert "obd" in vi.invalid_channels
        assert "ff" in vi.invalid_channels

    def test_my_out_of_range_skips_none_channels(self, ctx_default: VehicleContext) -> None:
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=2022,
        )
        inp = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
        vi = validate(inp)
        # no gas/obd/ff -> only dtcs rejected
        assert "dtcs" in vi.invalid_channels
        assert len(vi.valid_channels) == 0

    def test_obd_all_none_fields_accepted(self, ctx_default: VehicleContext) -> None:
        """OBD with all-None optional fields still passes range check."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_stft_out_of_range_rejects_obd(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=55.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_ltft_b2_out_of_range_rejects_obd(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ltft_b2=-55.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_dtcs_always_accepted_in_range(self, ctx_default: VehicleContext) -> None:
        """dtcs channel is accepted by cat1 range regardless of content."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301"], analyser_type="5-gas",
        )
        vi = validate(inp)
        assert "dtcs" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 2 -- Gas sum
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory2GasSum:
    """Physically impossible gas sum -- VL category 2."""

    def test_normal_gas_passes(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=200.0, co2_pct=14.0, o2_pct=1.0),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels

    def test_sum_exceeds_101_rejects(self, ctx_default: VehicleContext) -> None:
        """Direct internal call -- with current ranges max gas sum ~59%,
        so >101% is unreachable via public validate()."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=40.0, hc_ppm=10000.0, co2_pct=40.0, o2_pct=20.1),
        )
        vi = ValidatedInput(raw=inp)
        vi.valid_channels.add("gas_idle")
        _cat2_gas_sum(vi)
        assert "gas_idle" not in vi.valid_channels
        assert "gas_sum" in vi.invalid_channels["gas_idle"]

    def test_sum_at_boundary_101_passes(self, ctx_default: VehicleContext) -> None:
        """Sum = 101.0 not > 101, channel stays valid (direct call)."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=40.0, hc_ppm=0.0, co2_pct=40.0, o2_pct=21.0),
        )
        vi = ValidatedInput(raw=inp)
        vi.valid_channels.add("gas_idle")
        _cat2_gas_sum(vi)
        assert "gas_idle" in vi.valid_channels

    def test_channel_valid_but_gas_none_skipped(self, ctx_default: VehicleContext) -> None:
        """Line 231: channel in valid_channels but gas record is None."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = ValidatedInput(raw=inp)
        vi.valid_channels.add("gas_high")
        _cat2_gas_sum(vi)
        assert "gas_high" in vi.valid_channels

    def test_gas_high_also_checked(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_high=GasRecord(co_pct=12.0, hc_ppm=0.0, co2_pct=14.0, o2_pct=80.0),
        )
        vi = validate(inp)
        assert "gas_high" not in vi.valid_channels

    def test_hc_ppm_converted_for_sum(self, ctx_default: VehicleContext) -> None:
        """HC 2000 ppm = 0.2% -> CO 5 + CO2 14 + HC 0.2 + O2 0.5 = 19.7% -- fine."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=5.0, hc_ppm=2000.0, co2_pct=14.0, o2_pct=0.5),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 3 -- Probe air
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory3ProbeAir:
    """Probe air contamination check -- VL category 3."""

    def test_o2_18_1_with_engine_running_rejects(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=18.1),
            obd=OBDRecord(rpm=800),
        )
        vi = validate(inp)
        assert "gas_idle" not in vi.valid_channels
        assert "probe_air" in vi.invalid_channels["gas_idle"]

    def test_o2_18_0_passes(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=18.0),
            obd=OBDRecord(rpm=800),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels

    def test_high_o2_no_rpm_still_rejects(self, ctx_default: VehicleContext) -> None:
        """No RPM data -> engine assumed running -> probe air check fires."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=20.0),
        )
        vi = validate(inp)
        assert "gas_idle" not in vi.valid_channels

    def test_o2_high_ff_rpm_triggers_check(self, ctx_default: VehicleContext) -> None:
        """FF RPM > 0 -> engine running -> probe air check fires."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_high=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=19.0),
            freeze_frame=FreezeFrameRecord(rpm=1200),
        )
        vi = validate(inp)
        assert "gas_high" not in vi.valid_channels

    def test_obd_rpm_zero_ff_none_still_assumes_running(self, ctx_default: VehicleContext) -> None:
        """OBD rpm=0, no FF -> _engine_is_running falls to default True."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=20.0),
            obd=OBDRecord(rpm=0),
        )
        vi = validate(inp)
        assert "gas_idle" not in vi.valid_channels

    def test_no_rpm_data_engine_assumed_running(self, ctx_default: VehicleContext) -> None:
        """No OBD, no FF RPM data -> default to running -> check fires."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=19.0),
        )
        vi = validate(inp)
        assert "gas_idle" not in vi.valid_channels

    def test_skips_if_channel_already_rejected(self, ctx_default: VehicleContext) -> None:
        """If gas channel rejected by range, cat3 skips it."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=16.0, hc_ppm=0.0, co2_pct=0.0, o2_pct=20.0),
            obd=OBDRecord(rpm=800),
        )
        vi = validate(inp)
        # channel already rejected by cat1 (co=16%), cat3 does not re-process
        assert "gas_idle" not in vi.valid_channels

    def test_channel_valid_but_gas_none_skipped(self, ctx_default: VehicleContext) -> None:
        """Line 253: channel in valid_channels but gas record is None."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = ValidatedInput(raw=inp)
        vi.valid_channels.add("gas_high")
        _cat3_probe_air(vi)
        assert "gas_high" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 4 -- DTC regex
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory4DtcRegex:
    """DTC format validation -- VL category 4."""

    def test_p0301_valid(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels
        assert "dtcs_rejected_codes" not in vi.invalid_channels

    def test_p301_invalid_too_short(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels
        assert "P301" in str(vi.invalid_channels["dtcs"])

    def test_lowercase_rejected(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["p0301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels

    def test_x0301_invalid_prefix(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["X0301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels

    def test_mixed_valid_invalid_keeps_channel(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301", "BAD"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels
        assert "dtcs_rejected_codes" in vi.invalid_channels
        assert "BAD" in vi.invalid_channels["dtcs_rejected_codes"]

    def test_body_dtc_valid(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["B1200"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels

    def test_chassis_dtc_valid(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["C0035"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels

    def test_network_dtc_valid(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["U0100"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels

    def test_empty_dtcs_list_not_rejected_by_regex(self, ctx_default: VehicleContext) -> None:
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        ))
        # empty list means no invalid codes -> channel stays valid
        assert "dtcs" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 5 -- DTC era-validity
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory5DtcEra:
    """DTC era-validity -- VL category 5."""

    def test_p0420_my_1995_rejected(self) -> None:
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0420"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels
        assert "P0420" in vi.invalid_channels["dtcs"]

    def test_p0420_my_1997_valid(self) -> None:
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1997,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0420"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels

    def test_p0301_my_1995_with_valid_non_obd2(self) -> None:
        """Pre-1996: P/C/B/U DTCs rejected."""
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels

    def test_mixed_era_some_valid(self) -> None:
        """Pre-1996 with P0420 rejected but no valid left."""
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0420", "P0301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels

    def test_era_check_skips_if_dtcs_rejected(self, ctx_default: VehicleContext) -> None:
        """If dtcs channel already invalid, cat5 does nothing."""
        # MY out of range rejects dtcs in cat1 -> cat5 sees dtcs not in valid_channels
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1985,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
        ))
        assert "dtcs" not in vi.valid_channels

    def test_era_append_to_existing_invalid(self, ctx_default: VehicleContext) -> None:
        """When cat4 already logged invalid codes, cat5 appends."""
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0420", "BAD"], analyser_type="5-gas",
        ))
        # cat4 rejects BAD, logs to dtcs_rejected_codes
        # cat5 rejects P0420 on pre-1996, leaving no valid dtcs -> rejects channel
        assert "dtcs" not in vi.valid_channels

    def test_era_mixed_valid_partial_reject_direct(self) -> None:
        """Lines 324-325: some era-invalid but valid DTCs remain (direct call
        -- unreachable via public API because cat4 regex already enforces
        P/C/B/U prefix)."""
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        # XYZZY starts with X, not P/C/B/U -- would fail cat4 regex but cat5
        # treats non-PCBU codes on pre-1996 as era-valid
        inp = DiagnosticInput(
            vehicle_context=ctx, dtcs=["P0420", "XYZZY"], analyser_type="5-gas",
        )
        vi = ValidatedInput(raw=inp)
        vi.valid_channels.add("dtcs")
        _cat5_dtc_era(vi)
        assert "dtcs" in vi.valid_channels
        assert "dtcs_rejected_codes" in vi.invalid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 6 -- Combined-mode (soft warning)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory6CombinedMode:
    """Contradictory combined OBD signals -- VL category 6 (soft warning only)."""

    def test_neg_trim_low_fp_warns(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=-20.0, fuel_pressure_kpa=200.0),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 6 for w in vi.warnings)
        assert "obd" in vi.valid_channels  # never rejects

    def test_pos_trim_rich_o2_warns(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=20.0, o2_voltage_b1=0.9),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 6 for w in vi.warnings)
        assert "obd" in vi.valid_channels

    def test_ltft_neg_triggers_warn(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ltft_b1=-18.0, fuel_pressure_kpa=200.0),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 6 for w in vi.warnings)

    def test_ltft_pos_triggers_warn(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ltft_b1=18.0, o2_voltage_b1=0.9),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 6 for w in vi.warnings)

    def test_clean_data_no_warning(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=2.0, ltft_b1=1.0, fuel_pressure_kpa=350.0),
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 6 for w in vi.warnings)

    def test_no_obd_no_warning(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 6 for w in vi.warnings)

    def test_soft_mode_false_skips(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=-20.0, fuel_pressure_kpa=200.0),
        )
        vi = validate(inp, soft_mode=False)
        assert not any(w.category == 6 for w in vi.warnings)

    def test_neg_trim_at_boundary_no_warn(self, ctx_default: VehicleContext) -> None:
        """Exactly at -15.0% -> not < -15.0 -> no warning."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=-15.0, fuel_pressure_kpa=200.0),
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 6 for w in vi.warnings)

    def test_stft_none_ltft_valid(self, ctx_default: VehicleContext) -> None:
        """Only ltft set, stft=None -> still checks ltft."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=None, ltft_b1=-18.0, fuel_pressure_kpa=200.0),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 6 for w in vi.warnings)


# ═══════════════════════════════════════════════════════════════════════════════
# Category 7 -- Delta (ECT jump)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory7Delta:
    """ECT delta check -- VL category 7."""

    def test_ect_jump_25_to_999_rejects_obd(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=999.0),
            freeze_frame=FreezeFrameRecord(ect_c=25.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_ect_60_to_85_passes(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=85.0),
            freeze_frame=FreezeFrameRecord(ect_c=60.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_ect_above_150_sentinel_rejects(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=151.0),
        )
        vi = validate(inp)
        assert "obd" not in vi.valid_channels

    def test_ect_at_150_sentinel_ok(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=150.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels

    def test_no_obd_no_delta_check(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            freeze_frame=FreezeFrameRecord(ect_c=25.0),
        )
        vi = validate(inp)
        assert "ff" in vi.valid_channels  # FF unaffected

    def test_obd_ect_none_no_delta_ff_comparison(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=None, rpm=800),
            freeze_frame=FreezeFrameRecord(ect_c=25.0),
        )
        vi = validate(inp)
        # OBD ect is None, no comparison possible -> OBD stays valid
        assert "obd" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 8 -- Consistency (hard)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory8Consistency:
    """Consistency hard-rejection -- VL category 8 (pass-through in v2.0)."""

    def test_pass_through_does_not_reject(self, ctx_default: VehicleContext) -> None:
        """Cat8 is a no-op (deferred to M0/vref.db)."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(map_kpa=200.0),
        )
        vi = validate(inp)
        assert "obd" in vi.valid_channels


# ═══════════════════════════════════════════════════════════════════════════════
# Category 8b -- Consistency soft (warning)
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory8bConsistencySoft:
    """Soft consistency warnings -- VL category 8b."""

    def test_vvt_angle_present_warns(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(vvt_angle=25.0),
        )
        vi = validate(inp, soft_mode=True)
        assert any(w.category == 8 for w in vi.warnings)
        assert "obd" in vi.valid_channels  # never rejects

    def test_no_vvt_no_warning(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(),
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 8 for w in vi.warnings)

    def test_no_obd_no_warning(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 8 for w in vi.warnings)

    def test_soft_mode_false_skips_8b(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(vvt_angle=25.0),
        )
        vi = validate(inp, soft_mode=False)
        assert not any(w.category == 8 for w in vi.warnings)


# ═══════════════════════════════════════════════════════════════════════════════
# Category 9 -- Thermal gate
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory9ThermalGate:
    """Cold-start thermal gate -- VL category 9."""

    def test_ect_74_restricts_cold_start(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=74.0),
        )
        vi = validate(inp)
        assert vi.restricted_cold_start is True

    def test_ect_75_no_restriction(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=75.0),
        )
        vi = validate(inp)
        assert vi.restricted_cold_start is False

    def test_ect_from_ff(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            freeze_frame=FreezeFrameRecord(ect_c=60.0),
        )
        vi = validate(inp)
        assert vi.restricted_cold_start is True

    def test_ff_overrides_when_no_obd(self, ctx_default: VehicleContext) -> None:
        """_get_ect uses OBD first, FF fallback."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=None),
            freeze_frame=FreezeFrameRecord(ect_c=70.0),
        )
        vi = validate(inp)
        assert vi.restricted_cold_start is True

    def test_no_ect_no_flag(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = validate(inp)
        assert vi.restricted_cold_start is False


# ═══════════════════════════════════════════════════════════════════════════════
# Category 10 -- Open-loop gate
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory10OpenLoop:
    """Open-loop fuel status gate -- VL category 10."""

    def test_ol_fault_ect_80_suppresses(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=80.0, fuel_status="OL_FAULT"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is True

    def test_ol_drive_ect_80_suppresses(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=80.0, fuel_status="OL_DRIVE"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is True

    def test_ol_fault_ect_70_no_suppression(self, ctx_default: VehicleContext) -> None:
        """ECT < 75 -> engine not warm -> OL suppression does NOT fire."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=70.0, fuel_status="OL_FAULT"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is False

    def test_cl_fuel_status_no_suppression(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=80.0, fuel_status="CL"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is False

    def test_no_fuel_status_no_suppression(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=80.0),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is False

    def test_ff_fuel_status_used_when_obd_absent(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            freeze_frame=FreezeFrameRecord(ect_c=80.0, fuel_status="OL_FAULT"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is True

    def test_obd_fuel_status_takes_priority(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=80.0, fuel_status="CL"),
            freeze_frame=FreezeFrameRecord(ect_c=80.0, fuel_status="OL_FAULT"),
        )
        vi = validate(inp)
        # OBD fuel_status="CL" takes priority -> no suppression
        assert vi.open_loop_suppression is False

    def test_ol_fault_no_ect_available(self, ctx_default: VehicleContext) -> None:
        """fuel_status OL_FAULT but no ECT -> cannot verify warm -> no suppression."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(fuel_status="OL_FAULT"),
        )
        vi = validate(inp)
        assert vi.open_loop_suppression is False


# ═══════════════════════════════════════════════════════════════════════════════
# Category 11 -- Probe count gate
# ═══════════════════════════════════════════════════════════════════════════════


class TestCategory11ProbeCount:
    """4-gas vs 5-gas analyser gate -- VL category 11."""

    def test_4_gas_suppresses_nox(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="4-gas",
        )
        vi = validate(inp)
        assert vi.nox_suppressed is True

    def test_5_gas_does_not_suppress(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = validate(inp)
        assert vi.nox_suppressed is False


# ═══════════════════════════════════════════════════════════════════════════════
# Integration scenarios
# ═══════════════════════════════════════════════════════════════════════════════


class TestIntegrationScenarios:
    """Multi-category interactions and edge cases."""

    def test_all_channels_valid_full_input(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301", "P0420"], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
            gas_high=GasRecord(co_pct=0.3, hc_ppm=80.0, co2_pct=14.5, o2_pct=0.8),
            obd=OBDRecord(rpm=800, ect_c=85.0, map_kpa=35.0, fuel_status="CL"),
            freeze_frame=FreezeFrameRecord(ect_c=80.0, rpm=2500),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels
        assert "gas_high" in vi.valid_channels
        assert "dtcs" in vi.valid_channels
        assert "obd" in vi.valid_channels
        assert "ff" in vi.valid_channels
        assert vi.restricted_cold_start is False
        assert vi.open_loop_suppression is False
        assert vi.nox_suppressed is False

    def test_soft_mode_defaults_true(self, ctx_default: VehicleContext) -> None:
        """soft_mode defaults to True -- cat6/8b should run."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(vvt_angle=10.0),
        )
        vi = validate(inp)
        assert any(w.category == 8 for w in vi.warnings)

    def test_multiple_contradiction_warnings(self, ctx_default: VehicleContext) -> None:
        """Both cat6 contradiction patterns fire on the same OBD record."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(
                stft_b1=-20.0, fuel_pressure_kpa=200.0,
                ltft_b1=18.0, o2_voltage_b1=0.9,
            ),
        )
        vi = validate(inp, soft_mode=True)
        cat6_warnings = [w for w in vi.warnings if w.category == 6]
        assert len(cat6_warnings) == 2

    def test_rejected_gas_idle_skips_cat2_cat3(self, ctx_default: VehicleContext) -> None:
        """When cat1 rejects gas channel, cat2/cat3 skip it."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=16.0, hc_ppm=0.0, co2_pct=14.0, o2_pct=20.0),
            obd=OBDRecord(rpm=800),
        )
        vi = validate(inp)
        # Cat1 rejects (co=16%), cat2+cat3 see channel not in valid_channels -> skip
        assert "gas_idle" not in vi.valid_channels
        # The rejection reason should come from cat1 range
        assert "range" in vi.invalid_channels.get("gas_idle", "")

    def test_cat5_era_valid_with_no_obd2_dtc(self) -> None:
        """Pre-1996 vehicle with no P/C/B/U DTCs -- cat5 does nothing."""
        ctx = VehicleContext(
            brand="VW", model="Golf", engine_code="X", displacement_cc=1600, my=1995,
        )
        vi = validate(DiagnosticInput(
            vehicle_context=ctx, dtcs=[], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels

    def test_obd_none_and_ff_none_no_crash(self, ctx_default: VehicleContext) -> None:
        """Minimal input with just vehicle context -- no crash."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
        )
        vi = validate(inp)
        assert vi.valid_channels == {"dtcs"}
        assert vi.invalid_channels == {}
        assert vi.warnings == []
        assert vi.restricted_cold_start is False
        assert vi.open_loop_suppression is False

    def test_validated_input_has_raw_reference(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301"], analyser_type="5-gas",
        )
        vi = validate(inp)
        assert vi.raw is inp

    def test_invalid_channels_dict_has_reason_string(self, ctx_default: VehicleContext) -> None:
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=16.0, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.invalid_channels
        assert isinstance(vi.invalid_channels["gas_idle"], str)

    def test_dtcs_stays_valid_after_partial_rejections(self, ctx_default: VehicleContext) -> None:
        """Some DTCs rejected (cat4) but channel stays valid."""
        vi = validate(DiagnosticInput(
            vehicle_context=ctx_default, dtcs=["P0301", "BAD", "X9999"], analyser_type="5-gas",
        ))
        assert "dtcs" in vi.valid_channels
        assert "dtcs_rejected_codes" in vi.invalid_channels

    def test_gas_high_checked_independently(self, ctx_default: VehicleContext) -> None:
        """gas_idle passes range, gas_high fails -- independent checks."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
            gas_high=GasRecord(co_pct=20.0, hc_ppm=100.0, co2_pct=14.0, o2_pct=1.0),
        )
        vi = validate(inp)
        assert "gas_idle" in vi.valid_channels
        assert "gas_high" not in vi.valid_channels

    def test_ect_151_rejected_by_range_then_delta_skip(self, ctx_default: VehicleContext) -> None:
        """ECT=151 rejected by cat1 (range) before cat7 delta check."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(ect_c=151.0),
        )
        vi = validate(inp)
        # Cat1 rejects obd for ECT > 150
        assert "obd" not in vi.valid_channels

    def test_o2_voltage_b2_set_but_no_rich_check(self, ctx_default: VehicleContext) -> None:
        """Cat6 only checks o2_voltage_b1 -- b2 is ignored for rich check."""
        inp = DiagnosticInput(
            vehicle_context=ctx_default, dtcs=[], analyser_type="5-gas",
            obd=OBDRecord(stft_b1=20.0, o2_voltage_b1=None, o2_voltage_b2=0.9),
        )
        vi = validate(inp, soft_mode=True)
        assert not any(w.category == 6 for w in vi.warnings)
