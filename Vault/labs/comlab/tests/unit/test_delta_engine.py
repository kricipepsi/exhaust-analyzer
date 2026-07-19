"""Unit tests for the cross-lab delta engine (T-COMV2-DELTA-1B + 1C).

Covers the two sub-task suites the engine must earn green before it is wired
into the router (T-COMV2-DELTA-1D):

  1B (gates / sentinel):
    - single-point sentinel (no second frame)
    - architecture gate (delta-relations/06): MAP-only NULLs ΔTrim, forced
      induction INVERTS it, both-unknown → permissive + confidence cap
    - validity gate (delta-relations/08): vsum out-of-band / dilution / rpm-unstable

  1C (per-signal profiles / abstain):
    - ΔTrim @ STRESS_IDLE (delta-relations/02-05): vacuum leak, fuel starvation,
      MAF under-report, exhaust backpressure
    - Δgas @ REGULATORY_HIGH_IDLE (delta-relations/07): worn rings, worn valve
      seals, flat cam, EGR stuck closed
    - abstain families: trim band-mismatch, starvation↔MAF ambiguous, gas
      no-signature
    - architecture interplay (delta-relations/06): speed-density nulls a real
      leak; forced induction inverts the sign (not misread as an NA leak)

Every fixture's numbers trace to a delta-relations chunk via a ``# wiki:`` cite;
"no chunk coverage → no fixture" (T-COMV2-DELTA-1C). The engine is pure math and
takes the request whole, so these build a minimal ``OrchestratorInboundRequest``
in the ``test_symptom_prior.py`` request-builder style and read the returned
:class:`DeltaSignature` directly — no router involved (wiring is 1D).
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.analytics.delta_engine import DeltaEngine, DeltaSignature
from comlab.schemas.ingestion import (
    GasLabPayload,
    OBDLiveDataPayload,
    OrchestratorInboundRequest,
    SecondOperatingPointFrame,
    SessionMetadata,
)
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EngineStateBucket,
    InductionType,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    SampleValidity,
    TrimAnalyticsGate,
    VEValidity,
    VinConfidence,
)

# Per-signal bands (locked decision — SWEEP_MANIFEST §7).
_TRIM_BAND = EngineStateBucket.STRESS_IDLE  # wiki: delta-relations/01
_GAS_BAND = EngineStateBucket.REGULATORY_HIGH_IDLE  # wiki: delta-relations/07


# ---------------------------------------------------------------------------
# Request builders (engine reads gas_lab_output, obd_live_data, second_operating_point)
# ---------------------------------------------------------------------------


def _metadata() -> SessionMetadata:
    return SessionMetadata(
        session_id=uuid4(),
        vin_dna_string="1FA6P8CF0HXXXXXXX",
        resolved_horizon="HORIZON_MODERN",
        cylinder_count=4,
        vin_confidence=VinConfidence.HIGH,
    )


def _low_gas(
    *,
    hc: int = 50,
    co: float = 0.1,
    co2: float = 14.5,
    o2: float = 0.3,
    nox: int = 10,
    lam: float = 1.0,
    validity: SampleValidity = SampleValidity.VALID,
) -> GasLabPayload:
    """Low-idle (primary) gas frame carried on the request.

    Defaults give a clean validity-passing sample: vsum ≈ 14.9 % (in [14, 18])
    and CO+CO₂ = 14.6 % > 6 %.  # wiki: delta-relations/08
    """
    return GasLabPayload(
        chemical_state="NORMAL_OPERATION",
        gas_co=co,
        gas_hc=hc,
        gas_co2=co2,
        gas_o2=o2,
        gas_nox=nox,
        lambda_chem=lam,
        sample_validity=validity,
    )


def _low_obd(total_trim: float = 0.0) -> OBDLiveDataPayload:
    """Low-idle OBD frame — the engine reads ``total_trim_correction_delta`` as
    the low-idle total trim (STFT/LTFT left None so the pre-aggregated total is
    used, per delta-relations/01)."""
    return OBDLiveDataPayload(
        engine_warmed=True,
        total_trim_correction_delta=total_trim,
        ve_pct=72.0,
        ve_validity=VEValidity.VALID,
        rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,
        trim_analytics_gate=TrimAnalyticsGate.VALID,
        o2_failure_mode=O2FailureMode.NO_FAULT,
        maf_status=NodeMAFStatus.REAL_SENSOR_FEED,
        map_status=NodeMAPStatus.REAL_SENSOR_FEED,
    )


def _request(
    *,
    gas: GasLabPayload | None = None,
    obd: OBDLiveDataPayload | None = None,
    frame: SecondOperatingPointFrame | None = None,
) -> OrchestratorInboundRequest:
    return OrchestratorInboundRequest(
        metadata=_metadata(),
        gas_lab_output=gas if gas is not None else _low_gas(),
        obd_live_data=obd if obd is not None else _low_obd(),
        second_operating_point=frame,
    )


def _na_arch() -> dict:
    """Naturally-aspirated MAF architecture → ΔTrim profiles apply directly,
    confidence is the primary 0.92 (delta-relations/06)."""
    return {
        "air_metering_strategy": AirMeteringStrategy.MAF_ONLY,
        "induction_type": InductionType.NATURALLY_ASPIRATED,
    }


# ===========================================================================
# 1B — single-point sentinel
# ===========================================================================


def test_sentinel_no_second_frame() -> None:
    """No second frame → present=False, SINGLE_POINT, confidence 0.0 (the static
    single-point signature is the fallback).  # wiki: delta-relations/01"""
    sig = DeltaEngine.compute_delta_signature(_request(frame=None))
    assert isinstance(sig, DeltaSignature)
    assert sig.present is False
    assert sig.degradation_mode == "SINGLE_POINT"
    assert sig.confidence == 0.0
    assert sig.validity.trusted is False
    assert sig.target_fault_family is None


def test_shared_rank_policy_promotes_only_matching_trusted_family() -> None:
    signature = DeltaSignature(
        present=True,
        degradation_mode="FULL_FUSION",
        primary_profile="WORN_PISTON_RINGS",
        target_fault_family="mechanical_wear",
        confidence=0.92,
    )

    promoted, applied = DeltaEngine.apply_rank_score(
        0.75, "mechanical_wear", signature
    )
    unchanged, other_applied = DeltaEngine.apply_rank_score(
        0.85, "catalyst_failure", signature
    )

    assert promoted == pytest.approx(0.92)
    assert applied is True
    assert unchanged == pytest.approx(0.85)
    assert other_applied is False


@pytest.mark.parametrize(
    "signature",
    [
        None,
        DeltaSignature(),
        DeltaSignature(
            present=True,
            degradation_mode="FULL_FUSION",
            target_fault_family="mechanical_wear",
            confidence=0.0,
        ),
    ],
)
def test_shared_rank_policy_keeps_sentinel_and_abstain_inert(
    signature: DeltaSignature | None,
) -> None:
    score, applied = DeltaEngine.apply_rank_score(
        0.75, "mechanical_wear", signature
    )

    assert score == pytest.approx(0.75)
    assert applied is False


# ===========================================================================
# 1B — architecture gate (delta-relations/06)
# ===========================================================================


def test_architecture_gate_map_only_nulls_trim() -> None:
    """Speed-density (MAP-only) → trim_nulled, trim_inverted False.  # wiki: delta-relations/06"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        air_metering_strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY,
    )
    verdict = DeltaEngine._architecture_gate(frame)
    assert verdict.trim_nulled is True
    assert verdict.trim_inverted is False


@pytest.mark.parametrize(
    "induction",
    [InductionType.TURBOCHARGED, InductionType.SUPERCHARGED],
)
def test_architecture_gate_forced_induction_inverts(induction: InductionType) -> None:
    """Forced induction (turbo / supercharger) → trim_inverted set.  # wiki: delta-relations/06"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        induction_type=induction,
    )
    verdict = DeltaEngine._architecture_gate(frame)
    assert verdict.trim_inverted is True
    assert verdict.trim_nulled is False


def test_architecture_gate_unknown_is_permissive() -> None:
    """Both architecture inputs absent → permissive (no null, no invert); the
    confidence cap is applied downstream in _assemble.  # wiki: delta-relations/06"""
    frame = SecondOperatingPointFrame(rpm_state_bucket=_TRIM_BAND, engine_rpm=4000)
    verdict = DeltaEngine._architecture_gate(frame)
    assert verdict.trim_nulled is False
    assert verdict.trim_inverted is False
    assert verdict.air_metering_strategy is None
    assert verdict.induction_type is None


def test_unknown_architecture_caps_confidence() -> None:
    """A resolved trim profile with unknown architecture is capped at 0.70 so an
    un-gated profile cannot win outright.  # wiki: delta-relations/06 (risk)"""
    # Vacuum-leak ΔTrim numbers (low +20 / elev +2) but NO architecture fields.
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        total_trim_correction_delta=2.0,  # wiki: delta-relations/02 — stress ≈ 0..+5
    )
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=20.0), frame=frame)  # wiki: delta-relations/02 — low +15..+25
    )
    assert sig.trim.profile == "VACUUM_LEAK"
    assert sig.target_fault_family == "vacuum_leak"
    assert sig.confidence == pytest.approx(0.70)


# ===========================================================================
# 1B — validity gate (delta-relations/08)
# ===========================================================================


def test_validity_reject_elevated_dilution() -> None:
    """Elevated frame CO+CO₂ ≤ 6 % (near-ambient) → untrusted, confidence 0.0.

    vsum stays in band (14.5 %) so this isolates the dilution rule, not the vsum
    band.  # wiki: delta-relations/08"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_GAS_BAND,
        engine_rpm=2500,
        gas_hc=10,
        gas_co=0.5,
        gas_co2=4.0,  # CO+CO₂ = 4.5 ≤ 6 → dilution fail
        gas_o2=10.0,  # lifts vsum to 14.5 so the band check passes first
        gas_nox=0,
    )
    sig = DeltaEngine.compute_delta_signature(_request(frame=frame))
    assert sig.present is True
    assert sig.validity.trusted is False
    assert sig.confidence == 0.0
    assert "CO+CO2" in sig.validity.reason


def test_validity_reject_elevated_vsum_below_band() -> None:
    """Elevated frame vsum < 14 % (severe dilution) → untrusted, confidence 0.0.  # wiki: delta-relations/08"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_GAS_BAND,
        engine_rpm=2500,
        gas_hc=50,
        gas_co=0.3,
        gas_co2=8.0,
        gas_o2=2.0,  # vsum ≈ 10.3 < 14
        gas_nox=0,
    )
    sig = DeltaEngine.compute_delta_signature(_request(frame=frame))
    assert sig.validity.trusted is False
    assert sig.confidence == 0.0
    assert "vsum" in sig.validity.reason


def test_validity_reject_rpm_unstable() -> None:
    """Elevated frame RPM not settled → untrusted even with valid gas.  # wiki: delta-relations/08"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_GAS_BAND,
        engine_rpm=2500,
        gas_hc=50,
        gas_co=0.3,
        gas_co2=14.5,
        gas_o2=0.3,
        gas_nox=10,
        rpm_stable=False,
    )
    sig = DeltaEngine.compute_delta_signature(_request(frame=frame))
    assert sig.validity.trusted is False
    assert sig.confidence == 0.0
    assert "RPM" in sig.validity.reason


def test_validity_reject_low_frame_invalid() -> None:
    """Low frame's own GASLab triangle-gate INVALID verdict is authoritative.  # wiki: delta-relations/08"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_GAS_BAND,
        engine_rpm=2500,
        gas_hc=50,
        gas_co=0.3,
        gas_co2=14.5,
        gas_o2=0.3,
        gas_nox=10,
    )
    sig = DeltaEngine.compute_delta_signature(
        _request(gas=_low_gas(validity=SampleValidity.INVALID), frame=frame)
    )
    assert sig.validity.trusted is False
    assert sig.validity.low_frame_valid is False
    assert sig.confidence == 0.0


# ===========================================================================
# 1C — ΔTrim profiles @ STRESS_IDLE (delta-relations/02-05)
# ===========================================================================


def _trim_frame(elev_total: float) -> SecondOperatingPointFrame:
    return SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        total_trim_correction_delta=elev_total,
        **_na_arch(),
    )


def test_trim_vacuum_leak() -> None:
    """low +20 / elev +2 → ΔTrim −18 ≤ −10, low-idle ≥ +15 → VACUUM_LEAK → vacuum_leak.

    # wiki: delta-relations/02 (low +15..+25, stress ≈0..+5, ΔTrim ≤ −10)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=20.0), frame=_trim_frame(2.0))
    )
    assert sig.trim.profile == "VACUUM_LEAK"
    assert sig.trim.sign == "NEGATIVE"
    assert sig.trim.delta_total_trim == pytest.approx(-18.0)
    assert sig.target_fault_family == "vacuum_leak"
    assert sig.confidence == pytest.approx(0.92)


def test_trim_fuel_starvation() -> None:
    """low +3 / elev +20 → ΔTrim +17 ≥ +10, low-idle ≤ +5 → FUEL_STARVATION → lean_condition.

    # wiki: delta-relations/03 (low 0..+5, stress +15..+25, ΔTrim ≥ +10)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=3.0), frame=_trim_frame(20.0))
    )
    assert sig.trim.profile == "FUEL_STARVATION"
    assert sig.trim.sign == "POSITIVE"
    assert sig.target_fault_family == "lean_condition"
    assert sig.confidence == pytest.approx(0.92)


def test_trim_maf_underreport() -> None:
    """low +6 / elev +24 → ΔTrim +18 ≥ +10, low-idle in (+5, +8] → MAF_UNDERREPORT → lean_condition.

    # wiki: delta-relations/04 (low 0..+8, stress +15..+30, ΔTrim ≥ +10)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=6.0), frame=_trim_frame(24.0))
    )
    assert sig.trim.profile == "MAF_UNDERREPORT"
    assert sig.target_fault_family == "lean_condition"
    assert sig.confidence == pytest.approx(0.92)


def test_trim_exhaust_backpressure() -> None:
    """low 0 / elev −14 → ΔTrim −14 ≤ −10, low-idle ≈0 + elev ≤ −12 → EXHAUST_BACKPRESSURE → exhaust_leak.

    # wiki: delta-relations/05 (low ≈0, stress ≤ −12, ΔTrim ≤ −10)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=0.0), frame=_trim_frame(-14.0))
    )
    assert sig.trim.profile == "EXHAUST_BACKPRESSURE"
    assert sig.trim.sign == "NEGATIVE"
    assert sig.target_fault_family == "exhaust_leak"
    assert sig.confidence == pytest.approx(0.92)


# ===========================================================================
# 1C — Δgas profiles @ REGULATORY_HIGH_IDLE (delta-relations/07)
# ===========================================================================


def _gas_frame(
    *,
    hc: int,
    co: float,
    co2: float,
    o2: float,
    nox: int = 0,
    lam: float = 1.0,
) -> SecondOperatingPointFrame:
    return SecondOperatingPointFrame(
        rpm_state_bucket=_GAS_BAND,
        engine_rpm=2500,
        gas_hc=hc,
        gas_co=co,
        gas_co2=co2,
        gas_o2=o2,
        gas_nox=nox,
        lambda_chem=lam,
        **_na_arch(),
    )


def test_gas_worn_piston_rings() -> None:
    """GAS-WPR-001: HC 15→180 (ΔHC +165 ≥ +100), elev O₂ 0.5 < 2.0 → WORN_PISTON_RINGS → mechanical_wear.

    # wiki: delta-relations/07 (oil burn intensifies at 2500)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(
            gas=_low_gas(hc=15, co=0.10, co2=14.8, o2=0.30, nox=0, lam=1.014),
            frame=_gas_frame(hc=180, co=0.30, co2=14.1, o2=0.50, lam=1.005),
        )
    )
    assert sig.gas.gas_profile == "WORN_PISTON_RINGS"
    assert sig.gas.d_hc == 165
    assert sig.target_fault_family == "mechanical_wear"
    assert sig.confidence == pytest.approx(0.92)


def test_gas_worn_valve_seals() -> None:
    """GAS-WVS-001: HC 120→15 (ΔHC −105 ≤ −50) → WORN_VALVE_SEALS → mechanical_wear.

    # wiki: delta-relations/07 (oil induction clears at 2500)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(
            gas=_low_gas(hc=120, co=0.30, co2=14.2, o2=0.50, nox=0, lam=1.003),
            frame=_gas_frame(hc=15, co=0.08, co2=15.3, o2=0.20, lam=1.000),
        )
    )
    assert sig.gas.gas_profile == "WORN_VALVE_SEALS"
    assert sig.target_fault_family == "mechanical_wear"


def test_gas_flat_cam() -> None:
    """GAS-FC-001: HC 30→220 (ΔHC +190) AND elev O₂ 2.5 ≥ 2.0 → FLAT_CAM → cam_timing.

    The high elevated O₂ separates a breathing misfire from worn rings.
    # wiki: delta-relations/07"""
    sig = DeltaEngine.compute_delta_signature(
        _request(
            gas=_low_gas(hc=30, co=0.08, co2=14.0, o2=0.40, nox=0, lam=1.020),
            frame=_gas_frame(hc=220, co=0.25, co2=12.2, o2=2.50, lam=1.090),
        )
    )
    assert sig.gas.gas_profile == "FLAT_CAM"
    assert sig.target_fault_family == "cam_timing"


def test_gas_egr_stuck_closed() -> None:
    """GAS-ESC-001: NOx 1500→2800 (ΔNOx +1300 ≥ +800), no HC signature → EGR_STUCK_CLOSED → lean_condition.

    # wiki: delta-relations/07 (no dilution → NOx runaway)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(
            gas=_low_gas(hc=50, co=0.30, co2=15.0, o2=0.30, nox=1500, lam=1.006),
            frame=_gas_frame(hc=35, co=0.15, co2=15.2, o2=0.20, nox=2800, lam=1.002),
        )
    )
    assert sig.gas.gas_profile == "EGR_STUCK_CLOSED"
    assert sig.gas.d_nox == 1300
    assert sig.target_fault_family == "lean_condition"


# ===========================================================================
# 1C — abstain families
# ===========================================================================


def test_trim_abstains_on_band_mismatch() -> None:
    """ΔTrim is only defined at STRESS_IDLE; a frame at any other band ABSTAINS
    rather than differencing against a baseline at a different RPM.

    # wiki: SWEEP_MANIFEST §7 (per-signal bands — no silent mixing)"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=EngineStateBucket.STABILIZED_IDLE,  # neither band
        engine_rpm=750,
        total_trim_correction_delta=20.0,
        **_na_arch(),
    )
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=0.0), frame=frame)
    )
    assert sig.trim.profile == "ABSTAIN"
    assert sig.target_fault_family is None
    assert sig.confidence == 0.0


def test_trim_abstains_on_starvation_maf_ambiguous() -> None:
    """Positive ΔTrim with low-idle in the overlapping (+8, +15) band cannot
    separate fuel starvation from MAF under-report → ABSTAIN.

    low +10 / elev +25 → ΔTrim +15 ≥ +10, but low-idle +10 ∉ starve(≤+5)/MAF(≤+8).
    # wiki: delta-relations/03,04 (overlapping low-idle band is ambiguous)"""
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=10.0), frame=_trim_frame(25.0))
    )
    assert sig.trim.profile == "ABSTAIN"
    assert sig.target_fault_family is None
    assert sig.confidence == 0.0


def test_gas_no_signature_resolves_none() -> None:
    """A Δgas with no profile-crossing change resolves to NONE (not a false family).

    HC 50→55 (ΔHC +5 < +100), no NOx/λ shift → gas_profile NONE → confidence 0.0.
    # wiki: delta-relations/07"""
    sig = DeltaEngine.compute_delta_signature(
        _request(
            gas=_low_gas(hc=50, co=0.5, co2=14.5, o2=0.3, nox=10, lam=1.0),
            frame=_gas_frame(hc=55, co=0.5, co2=14.5, o2=0.3, nox=10, lam=1.0),
        )
    )
    assert sig.gas.gas_profile == "NONE"
    assert sig.target_fault_family is None
    assert sig.confidence == 0.0


# ===========================================================================
# 1C — architecture interplay (delta-relations/06)
# ===========================================================================


def test_speed_density_nulls_real_leak() -> None:
    """A real vacuum leak (low +20 / elev +2, ΔTrim −18) on a MAP-only engine is
    NULLED — sign NULL, no leak profile, confidence 0.0 (route to IAC/MAP-at-idle).

    # wiki: delta-relations/06 (speed-density paradox)"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        total_trim_correction_delta=2.0,
        air_metering_strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY,
        induction_type=InductionType.NATURALLY_ASPIRATED,
    )
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=20.0), frame=frame)
    )
    assert sig.architecture.trim_nulled is True
    assert sig.trim.sign == "NULL"
    assert sig.trim.profile == "NONE"
    assert sig.target_fault_family is None
    assert sig.confidence == 0.0


def test_forced_induction_inverts_sign_not_na_leak() -> None:
    """A post-turbo boost leak reads ≈ −20 % STFT at the elevated point; the
    architecture gate INVERTS the sign so it is NOT misread as an NA negative-ΔTrim
    leak (vacuum leak / exhaust backpressure).

    low 0 / elev −20 → raw ΔTrim −20, inverted → +20.
    # wiki: delta-relations/06 (turbo boost-leak sign inversion, ≈ −20 % STFT)"""
    frame = SecondOperatingPointFrame(
        rpm_state_bucket=_TRIM_BAND,
        engine_rpm=4000,
        total_trim_correction_delta=-20.0,
        air_metering_strategy=AirMeteringStrategy.MAF_ONLY,
        induction_type=InductionType.TURBOCHARGED,
    )
    sig = DeltaEngine.compute_delta_signature(
        _request(obd=_low_obd(total_trim=0.0), frame=frame)
    )
    assert sig.architecture.trim_inverted is True
    assert sig.trim.delta_total_trim == pytest.approx(20.0)  # sign flipped
    assert sig.trim.sign == "POSITIVE"
    assert sig.trim.profile not in ("VACUUM_LEAK", "EXHAUST_BACKPRESSURE")
