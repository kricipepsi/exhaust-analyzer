"""Tests for VEEngine — 3-branch polymorphic routing per OBDLab_KG_Wiki.md §10."""

import math

import pytest

from obdlab.core.ve_engine import (
    K_OFFSET,
    MM_AIR,
    R_GAS,
    VEEngine,
)
from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)
from obdlab.schemas.vocabulary import (
    NodeMAFStatus,
    NodeMAPStatus,
    RpmStateBucket,
    VEValidity,
)


def _expected_ve(maf, map_kpa, rpm, displacement, iat_c):
    """Compute expected VE using the same formula as _calc_ve_standard."""
    iat_k = iat_c + K_OFFSET
    numerator = maf * R_GAS * iat_k
    denominator = map_kpa * (rpm / 60.0) * (displacement / 2.0) * MM_AIR
    return (numerator / denominator) * 100.0


# ------------------------------------------------------------------
# Shared fixtures
# ------------------------------------------------------------------

def _dna_view(strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK):
    return ObdLabDnaView(
        engine_displacement_liters=2.0,
        rated_rpm=6500,
        stress_idle_rpm_target=4000,
        air_metering_strategy=strategy,
        upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
        induction_type=InductionType.NATURALLY_ASPIRATED,
        confidence=VinConfidence.HIGH,
    )



def _dual_pids(maf=2.5, map_kpa=30, rpm=800, iat=25, **kwargs):
    return {
        "mass_airflow_gps": maf,
        "manifold_vacuum_kpa": map_kpa,
        "engine_rpm": rpm,
        "intake_air_temp_c": iat,
        "rpm_state_bucket": RpmStateBucket.STABILIZED_IDLE.value,
        "total_trim_correction_delta": 5.0,
        "induction_type": InductionType.NATURALLY_ASPIRATED.value,
        **kwargs,
    }


@pytest.fixture
def engine():
    return VEEngine()


# ==================================================================
# Parametrized 3-branch routing test
# ==================================================================

def test_dual_branch_typical(engine):
    """DUAL_MAF_MAP_CROSSCHECK — typical warm idle VE ~50-75% for 2.0L NA."""
    pids = _dual_pids(maf=3.0, map_kpa=30, rpm=800, iat=25)
    expected = _expected_ve(3.0, 30, 800, 2.0, 25)
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, _dna_view(),
    )
    assert math.isclose(ve, expected, rel_tol=1e-6)
    assert maf_status == NodeMAFStatus.REAL_SENSOR_FEED
    assert map_status == NodeMAPStatus.REAL_SENSOR_FEED
    assert validity == VEValidity.VALID
    assert 40 < ve < 85  # realistic idle VE range


def test_map_only_branch_typical(engine):
    """MAP_ONLY_SPEED_DENSITY — emulate MAF, bucket=STRESS_IDLE."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
    pids = {"manifold_vacuum_kpa": 55, "engine_rpm": 4000, "intake_air_temp_c": 35}
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STRESS_IDLE, dna,
    )
    assert maf_status == NodeMAFStatus.VIRTUAL_EMULATION
    assert map_status == NodeMAPStatus.REAL_SENSOR_FEED
    assert ve is not None
    assert 50 < ve < 95  # reasonable VE at stress idle
    assert validity == VEValidity.UNKNOWN


def test_maf_only_branch_typical(engine):
    """MAF_ONLY — back-calc MAP, bucket=REGULATORY_HIGH_IDLE."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAF_ONLY)
    pids = {"mass_airflow_gps": 8.0, "engine_rpm": 2500, "intake_air_temp_c": 30}
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.REGULATORY_HIGH_IDLE, dna,
    )
    assert maf_status == NodeMAFStatus.REAL_SENSOR_FEED
    assert map_status == NodeMAPStatus.BACK_CALCULATED
    assert ve is not None
    assert 50 < ve < 95
    assert validity == VEValidity.UNKNOWN


# ==================================================================
# DUAL branch — boundary cases
# ==================================================================

def test_dual_high_rpm(engine):
    """DUAL at STRESS_IDLE ~4000 RPM."""
    pids = _dual_pids(maf=20.0, map_kpa=55, rpm=4000, iat=35,
                       rpm_state_bucket=RpmStateBucket.STRESS_IDLE.value)
    expected = _expected_ve(20.0, 55, 4000, 2.0, 35)
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STRESS_IDLE, _dna_view(),
    )
    assert math.isclose(ve, expected, rel_tol=1e-6)


def test_dual_low_rpm_idle(engine):
    """DUAL at STABILIZED_IDLE ~650 RPM (low end of idle band)."""
    pids = _dual_pids(maf=2.0, map_kpa=28, rpm=650, iat=25)
    expected = _expected_ve(2.0, 28, 650, 2.0, 25)
    ve, _, _, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, _dna_view(),
    )
    assert math.isclose(ve, expected, rel_tol=1e-6)
    assert validity == VEValidity.VALID


def test_dual_cold_iat(engine):
    """DUAL with cold intake air (-10°C)."""
    pids = _dual_pids(maf=3.5, map_kpa=32, rpm=900, iat=-10)
    expected = _expected_ve(3.5, 32, 900, 2.0, -10)
    ve, _, _, _ = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, _dna_view(),
    )
    assert math.isclose(ve, expected, rel_tol=1e-6)


def test_dual_hot_iat(engine):
    """DUAL with hot intake air (60°C)."""
    pids = _dual_pids(maf=2.2, map_kpa=28, rpm=800, iat=60)
    expected = _expected_ve(2.2, 28, 800, 2.0, 60)
    ve, _, _, _ = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, _dna_view(),
    )
    assert math.isclose(ve, expected, rel_tol=1e-6)


def test_dual_small_displacement(engine):
    """DUAL with 1.0L displacement."""
    dna = _dna_view()
    dna.engine_displacement_liters = 1.0
    pids = _dual_pids(maf=1.5, map_kpa=30, rpm=800, iat=25)
    expected = _expected_ve(1.5, 30, 800, 1.0, 25)
    ve, _, _, _ = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert math.isclose(ve, expected, rel_tol=1e-6)


# ==================================================================
# MAP_ONLY — boundary cases
# ==================================================================

def test_map_only_low_rpm(engine):
    """MAP_ONLY at low RPM ~1000."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
    pids = {"manifold_vacuum_kpa": 30, "engine_rpm": 1000, "intake_air_temp_c": 25}
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, dna,
    )
    assert maf_status == NodeMAFStatus.VIRTUAL_EMULATION
    assert map_status == NodeMAPStatus.REAL_SENSOR_FEED
    assert ve is not None
    assert validity == VEValidity.UNKNOWN


def test_map_only_missing_map(engine):
    """MAP_ONLY with MAP missing → UNKNOWN."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
    pids = {"engine_rpm": 2000, "intake_air_temp_c": 25}
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, dna,
    )
    assert ve is None
    assert validity == VEValidity.UNKNOWN


# ==================================================================
# MAF_ONLY — boundary cases
# ==================================================================

def test_maf_only_missing_maf(engine):
    """MAF_ONLY with MAF missing → UNKNOWN."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAF_ONLY)
    pids = {"engine_rpm": 2000, "intake_air_temp_c": 25}
    ve, maf_status, map_status, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, dna,
    )
    assert ve is None
    assert validity == VEValidity.UNKNOWN


def test_maf_only_zero_rpm(engine):
    """MAF_ONLY with RPM=0 → UNKNOWN."""
    dna = _dna_view(strategy=AirMeteringStrategy.MAF_ONLY)
    pids = {"mass_airflow_gps": 5.0, "engine_rpm": 0, "intake_air_temp_c": 25}
    ve, _, _, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, dna,
    )
    assert ve is None
    assert validity == VEValidity.UNKNOWN


# ==================================================================
# UNKNOWN / insufficient-inputs cases
# ==================================================================

def test_dual_missing_map_returns_unknown(engine):
    """DUAL branch missing MAP → UNKNOWN."""
    dna = _dna_view()
    pids = {"mass_airflow_gps": 5.0, "engine_rpm": 800, "intake_air_temp_c": 25}
    ve, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert ve is None
    assert validity == VEValidity.UNKNOWN


def test_dual_missing_displacement_returns_unknown(engine):
    """DUAL with DNA missing displacement → UNKNOWN."""
    dna = _dna_view()
    dna.engine_displacement_liters = None
    pids = _dual_pids()
    ve, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert ve is None
    assert validity == VEValidity.UNKNOWN


def test_no_dna_defaults_to_dual_unknown(engine):
    """No DNA view → defaults to DUAL with no displacement → UNKNOWN."""
    pids = _dual_pids(maf=3.0, map_kpa=30, rpm=800, iat=25)
    ve, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, None)
    assert ve is None
    assert validity == VEValidity.UNKNOWN


# ==================================================================
# VE-fault trigger: FAULT_VE_IDLE_COLLAPSE (§6.4)
# ==================================================================

def test_ve_idle_collapse_positive(engine):
    """VE < 50, STABILIZED_IDLE, MAP > 45 → FAULT_VE_IDLE_COLLAPSE."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0  # large disp → low VE for given MAF
    # With 3.0L, MAF=2.0, MAP=48 (just above threshold), RPM=800
    pids = _dual_pids(maf=2.0, map_kpa=48, rpm=800, iat=25)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert validity == VEValidity.FAULT_VE_IDLE_COLLAPSE


def test_ve_idle_collapse_negative_map_below_threshold(engine):
    """MAP <= 45 kPa — collapse trigger does NOT fire even with low VE."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=2.0, map_kpa=44, rpm=800, iat=25)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert validity != VEValidity.FAULT_VE_IDLE_COLLAPSE


def test_ve_idle_collapse_negative_wrong_bucket(engine):
    """Low VE at STRESS_IDLE — collapse trigger does NOT fire."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=2.0, map_kpa=48, rpm=4000, iat=25,
                       rpm_state_bucket=RpmStateBucket.STRESS_IDLE.value)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STRESS_IDLE, dna)
    assert validity != VEValidity.FAULT_VE_IDLE_COLLAPSE


# ==================================================================
# VE-fault trigger: FAULT_MAF_CONTAMINATION (§6.4)
# ==================================================================

def test_maf_contamination_positive(engine):
    """VE < 65, STRESS_IDLE, TFT > 15 → FAULT_MAF_CONTAMINATION."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=5.0, map_kpa=55, rpm=4000, iat=35,
                       rpm_state_bucket=RpmStateBucket.STRESS_IDLE.value,
                       total_trim_correction_delta=20.0)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STRESS_IDLE, dna)
    assert validity == VEValidity.FAULT_MAF_CONTAMINATION


def test_maf_contamination_negative_tft_below_threshold(engine):
    """TFT <= 15 — contamination trigger does NOT fire."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=5.0, map_kpa=55, rpm=4000, iat=35,
                       rpm_state_bucket=RpmStateBucket.STRESS_IDLE.value,
                       total_trim_correction_delta=14.0)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STRESS_IDLE, dna)
    assert validity != VEValidity.FAULT_MAF_CONTAMINATION


def test_maf_contamination_negative_wrong_bucket(engine):
    """VE < 65 at STABILIZED_IDLE — contamination trigger does NOT fire."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=2.0, map_kpa=48, rpm=800, iat=25,
                       total_trim_correction_delta=20.0)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    # Should fire collapse, not contamination
    assert validity != VEValidity.FAULT_MAF_CONTAMINATION


def test_maf_contamination_regulatory_high_idle(engine):
    """FAULT_MAF_CONTAMINATION also triggers at REGULATORY_HIGH_IDLE."""
    dna = _dna_view()
    dna.engine_displacement_liters = 3.0
    pids = _dual_pids(maf=5.0, map_kpa=50, rpm=2500, iat=30,
                       rpm_state_bucket=RpmStateBucket.REGULATORY_HIGH_IDLE.value,
                       total_trim_correction_delta=18.0)
    _, _, _, validity = engine.compute_ve(
        pids, RpmStateBucket.REGULATORY_HIGH_IDLE, dna,
    )
    assert validity == VEValidity.FAULT_MAF_CONTAMINATION


# ==================================================================
# VE-fault trigger: FAULT_VE_SENSOR_SKEW (§6.4)
# ==================================================================

def test_ve_sensor_skew_positive(engine):
    """VE > 90, STABILIZED_IDLE, NA induction → FAULT_VE_SENSOR_SKEW."""
    dna = _dna_view()
    dna.engine_displacement_liters = 1.0  # small disp → high VE for given MAF
    # With 1.0L, MAF=2.0, MAP=18, RPM=800
    pids = _dual_pids(maf=2.0, map_kpa=18, rpm=800, iat=25)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert validity == VEValidity.FAULT_VE_SENSOR_SKEW


def test_ve_sensor_skew_negative_turbo(engine):
    """VE > 90 but turbocharged → skew trigger does NOT fire."""
    dna = _dna_view()
    dna.engine_displacement_liters = 1.0
    dna.induction_type = InductionType.TURBOCHARGED
    pids = _dual_pids(maf=2.0, map_kpa=18, rpm=800, iat=25,
                       induction_type=InductionType.TURBOCHARGED.value)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert validity != VEValidity.FAULT_VE_SENSOR_SKEW


def test_ve_sensor_skew_negative_wrong_bucket(engine):
    """VE > 90 at STRESS_IDLE — skew trigger does NOT fire."""
    dna = _dna_view()
    dna.engine_displacement_liters = 1.0
    pids = _dual_pids(maf=2.0, map_kpa=18, rpm=4000, iat=25,
                       rpm_state_bucket=RpmStateBucket.STRESS_IDLE.value)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STRESS_IDLE, dna)
    assert validity != VEValidity.FAULT_VE_SENSOR_SKEW


# ==================================================================
# _classify_validity edge cases
# ==================================================================

def test_validity_valid_when_no_faults_triggered(engine):
    """Normal operating point returns VALID."""
    pids = _dual_pids(maf=3.0, map_kpa=30, rpm=800, iat=25)
    _, _, _, validity = engine.compute_ve(
        pids, RpmStateBucket.STABILIZED_IDLE, _dna_view(),
    )
    assert validity == VEValidity.VALID


def test_validity_unknown_ve_none(engine):
    """When ve is None (missing input), validity is UNKNOWN."""
    dna = _dna_view()
    dna.engine_displacement_liters = None
    pids = _dual_pids(maf=3.0, map_kpa=30, rpm=800, iat=25)
    _, _, _, validity = engine.compute_ve(pids, RpmStateBucket.STABILIZED_IDLE, dna)
    assert validity == VEValidity.UNKNOWN


# ==================================================================
# _expected_ve lookup
# ==================================================================

def test_expected_ve_known_entries():
    """All 6 known (bucket, strategy) pairs return a float."""
    from obdlab.core.ve_engine import _EXPECTED_VE
    assert _EXPECTED_VE[(RpmStateBucket.STABILIZED_IDLE.value, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value)] == 0.65
    assert _EXPECTED_VE[(RpmStateBucket.STABILIZED_IDLE.value, AirMeteringStrategy.MAF_ONLY.value)] == 0.70
    assert _EXPECTED_VE[(RpmStateBucket.STRESS_IDLE.value, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value)] == 0.80
    assert _EXPECTED_VE[(RpmStateBucket.STRESS_IDLE.value, AirMeteringStrategy.MAF_ONLY.value)] == 0.82


def test_expected_ve_missing_entry_returns_none(engine):
    """Lookup for a key not in _EXPECTED_VE returns None."""
    result = engine._expected_ve(RpmStateBucket.COLD_OPEN_LOOP_INVALID, AirMeteringStrategy.MAF_ONLY)
    assert result is None


# ==================================================================
# Exhaustive switch — all 3 branches return correct status enums
# ==================================================================

def test_all_three_branches_implemented(engine):
    """Each AirMeteringStrategy routes to correct MAF/MAP status pair."""
    dna_dual = _dna_view(strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK)
    dna_map = _dna_view(strategy=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
    dna_maf = _dna_view(strategy=AirMeteringStrategy.MAF_ONLY)

    _, maf_s, map_s, _ = engine.compute_ve(
        _dual_pids(), RpmStateBucket.STABILIZED_IDLE, dna_dual,
    )
    assert maf_s == NodeMAFStatus.REAL_SENSOR_FEED
    assert map_s == NodeMAPStatus.REAL_SENSOR_FEED

    _, maf_s, map_s, _ = engine.compute_ve(
        {"manifold_vacuum_kpa": 30, "engine_rpm": 2000, "intake_air_temp_c": 25},
        RpmStateBucket.STABILIZED_IDLE, dna_map,
    )
    assert maf_s == NodeMAFStatus.VIRTUAL_EMULATION
    assert map_s == NodeMAPStatus.REAL_SENSOR_FEED

    _, maf_s, map_s, _ = engine.compute_ve(
        {"mass_airflow_gps": 5.0, "engine_rpm": 2000, "intake_air_temp_c": 25},
        RpmStateBucket.STABILIZED_IDLE, dna_maf,
    )
    assert maf_s == NodeMAFStatus.REAL_SENSOR_FEED
    assert map_s == NodeMAPStatus.BACK_CALCULATED


# ==================================================================
# Module-level constants
# ==================================================================

def test_module_constants():
    """MM_AIR, R_GAS, K_OFFSET are present and correctly typed."""
    assert isinstance(MM_AIR, float)
    assert isinstance(R_GAS, float)
    assert isinstance(K_OFFSET, float)
    assert MM_AIR == 28.97
    assert R_GAS == 8.314
    assert K_OFFSET == 273.15
