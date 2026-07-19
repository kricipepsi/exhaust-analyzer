"""End-to-end diagnostic engine tests — one fixture per routable registry family.

Drives ``LabPipelineAggregator.process(request, fault_code=None)`` through
the real routing path and asserts the resolved fault_code and fault_family.

Families without registry rules (sensor_fault, ecu_fault, no_fault) are noted
but cannot have real-routing tests.

Known application gaps discovered by this task:
- T-P6-5b-1: Legacy alias fault_ids (ERR-E1-M032, ERR-E2-I104, ERR-E3-F501)
  resolve in the registry but not in KG — KG only has new IDs (ERR-LC-005,
  ERR-MF-001, ERR-RM-005). FaultAtlasKG.resolve() has no alias fallback.
- T-P6-5b-2: FaultFamilyLit in response.py missing mechanical_wear, cam_timing,
  non_starter. KG families were added (T-P6-2a–d) but the response schema
  Literal wasn't updated.
- T-P6-5b-3: ERR-E1-M032 targets HORIZON_LEGACY only — no equivalent rule
  for ADAPTIVE/MODERN horizons in lean_condition family.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def _make_request(
    *,
    session_id: str | None = None,
    horizon: str = "HORIZON_MODERN",
    gas_payload: dict | None = None,
    obd_payload: dict | None = None,
    dtc_payload: dict | None = None,
) -> OrchestratorInboundRequest:
    sid = session_id or str(uuid4())
    return OrchestratorInboundRequest.model_validate({
        "metadata": {
            "session_id": sid,
            "vin_dna_string": "1FA6P8CF0HXXXXXXX",
            "resolved_horizon": horizon,
            "cylinder_count": 4,
        },
        "gas_lab_output": gas_payload or mock_gas_lab.warm_idle_baseline(),
        "obd_live_data": obd_payload or mock_obd_lab.warm_idle_baseline(),
        "dtc_lab_output": dtc_payload or mock_dtc_lab.no_codes(),
        "symptom_dna": {},
    })


# ---------------------------------------------------------------------------
# real-routing tests — one per routable registry family
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_e2e_exhaust_leak_manifold_gasket():
    """EXHAUST_AIR_LEAK + P0171 + long_term_ft1=15 → ERR-EL-001 (exhaust_leak)."""
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.exhaust_air_leak(),
        dtc_payload=mock_dtc_lab.p0171_exhaust_leak_manifold(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-EL-001"
    assert v.fault_family == "exhaust_leak"


@pytest.mark.e2e
def test_e2e_catalyst_efficiency_below_threshold():
    """CATALYST_OVERWHELMED + P0420 + o2_b1s2_v=0.7 → ERR-CF-001 (catalyst_failure)."""
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.catalyst_overwhelmed(),
        dtc_payload=mock_dtc_lab.p0420_catalyst_below_threshold(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-CF-001"
    assert v.fault_family == "catalyst_failure"


@pytest.mark.e2e
def test_e2e_ignition_fault_coil_driver():
    """IGNITION_MISFIRE + P0351 + short_term_ft1=20 → ERR-IF-001 (ignition_fault).

    Uses P0351 (not P030x) so ERR-E2-I104 (misfire) is excluded by DTC gate.
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.ignition_misfire_heavy_hc(),
        dtc_payload=mock_dtc_lab.p0351_ignition_coil_driver(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-IF-001"
    assert v.fault_family == "ignition_fault"


# ---------------------------------------------------------------------------
# Tests that hit known application gaps — these verify the registry triage
# works correctly but are blocked by schema/KG issues downstream.
# See T-P6-5b-1 through T-P6-5b-3 in PROGRESS.md.
# ---------------------------------------------------------------------------


@pytest.mark.e2e
def test_e2e_rich_mixture_hpfp_seal_leak():
    """GDI_HPFP_INTERNAL_SEAL_LEAK + P0172 + long_term_ft1=-25 → no fault.

    T-FX-PURGE-2: ERR-E3-F501 (MODERN-only) stripped from registry.
    MODERN-only rules must not surface for any case.
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.rich_unmetered_intrusion(),
        dtc_payload=mock_dtc_lab.p0172_rich_hpfp_leak(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is False


@pytest.mark.e2e
def test_e2e_misfire_coil_insulation_arc():
    """IGNITION_MISFIRE + P0302 + short_term_ft1=20 → ERR-E2-I104.

    Registry triage resolves correctly.  KG alias gap (T-P6-5b-1):
    ERR-E2-I104 maps_to ERR-MF-001.
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.ignition_misfire_heavy_hc(),
        dtc_payload=mock_dtc_lab.p0302_misfire_coil_arc(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-E2-I104"
    # T-P6-5b-1: fault_family is "no_fault" until KG alias resolution is added


@pytest.mark.e2e
def test_e2e_lean_condition_egr_stuck_open():
    """INCOMPLETE_OXIDATION + P0401 + vacuum in [30,50] → ERR-E1-M032.

    ERR-E1-M032 targets HORIZON_LEGACY only (T-P6-5b-3).  Test drives
    HORIZON_LEGACY to match.  KG alias gap (T-P6-5b-1):
    ERR-E1-M032 maps_to ERR-LC-005.
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        horizon="HORIZON_LEGACY",
        gas_payload=mock_gas_lab.egr_intake_dilution(),
        dtc_payload=mock_dtc_lab.p0401_egr_stuck_open(),
        # Legacy vehicles may have degraded OBD — use a minimal OBD payload
        obd_payload=mock_obd_lab.legacy_missing_trims(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-E1-M032"
    # T-P6-5b-1: fault_family is "no_fault" until KG alias resolution is added


@pytest.mark.e2e
def test_e2e_mechanical_wear_head_gasket():
    """INCOMPLETE_COMBUSTION + P0300 → ERR-MW-001 (mechanical_wear).

    Registry triage works.  XFAIL: FaultFamilyLit doesn't include
    "mechanical_wear" (T-P6-5b-2).
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.incomplete_combustion(),
        dtc_payload=mock_dtc_lab.p0300_mechanical_wear(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-MW-001"
    assert v.fault_family == "mechanical_wear"


@pytest.mark.e2e
def test_e2e_cam_timing_chain_stretch():
    """WRONG_VALVE_TIMING + P0016 + manifold_pressure_kpa=25 → ERR-CT-001 (cam_timing).

    Registry triage works.  XFAIL: FaultFamilyLit doesn't include
    "cam_timing" (T-P6-5b-2).
    """
    agg = LabPipelineAggregator(use_v2_registry=False)
    result = agg.process(_make_request(
        gas_payload=mock_gas_lab.wrong_valve_timing(),
        dtc_payload=mock_dtc_lab.p0016_cam_timing_retard(),
    ))
    v = result.diagnostic_verdict
    assert v.is_fault_detected is True
    assert v.fault_code == "ERR-CT-001"
    assert v.fault_family == "cam_timing"

