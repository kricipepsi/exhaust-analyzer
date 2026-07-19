"""Tests for AnalyticsPreconditions per OBDLab_KG_Wiki.md §9.

8 gates × (PASS + FAIL) = 16 tests + all-VALID integration check.
"""


from obdlab.core.analytics_preconditions import (
    CKP_CMP_FAULT_DTCS,
    O2_FAULT_DTCS,
    AnalyticsPreconditions,
)
from obdlab.schemas.vocabulary import TrimAnalyticsGate

# ==================================================================
# Helper — base healthy PID dict
# ==================================================================

def _healthy_pids(**overrides):
    """Return a PID dict where all 8 precondition gates should pass."""
    pids = {
        "coolant_temp_c": 90,
        "fuel_sys_status": "Closed_Loop",
        "active_dtcs": [],
        "drive_cycles_since_clear": 3,
        "throttle_pos": 15,
        "dfco_active": False,
    }
    pids.update(overrides)
    return pids


# ==================================================================
# Gate 1 — Engine warm: coolant_temp_c >= 70
# ==================================================================

def test_gate1_engine_warm_pass():
    """coolant_temp_c >= 70 → gate passes."""
    pids = _healthy_pids(coolant_temp_c=90)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate1_engine_cold_fails():
    """coolant_temp_c < 70 → ENGINE_COLD."""
    pids = _healthy_pids(coolant_temp_c=50)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.ENGINE_COLD


def test_gate1_engine_cold_at_boundary():
    """coolant_temp_c == 69 → ENGINE_COLD (threshold is >= 70)."""
    pids = _healthy_pids(coolant_temp_c=69)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.ENGINE_COLD


def test_gate1_engine_warm_at_boundary():
    """coolant_temp_c == 70 → gate passes."""
    pids = _healthy_pids(coolant_temp_c=70)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate1_ect_missing():
    """Missing coolant_temp_c → ENGINE_COLD."""
    pids = _healthy_pids()
    del pids["coolant_temp_c"]
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.ENGINE_COLD


# ==================================================================
# Gate 2 — Closed loop: fuel_sys_status == "Closed_Loop"
# ==================================================================

def test_gate2_closed_loop_pass():
    """fuel_sys_status == Closed_Loop → gate passes."""
    pids = _healthy_pids(fuel_sys_status="Closed_Loop")
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate2_open_loop_fails():
    """fuel_sys_status == Open_Loop_Cold → OPEN_LOOP."""
    pids = _healthy_pids(fuel_sys_status="Open_Loop_Cold")
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.OPEN_LOOP


def test_gate2_open_loop_drive_fails():
    """fuel_sys_status == Open_Loop_Drive → OPEN_LOOP."""
    pids = _healthy_pids(fuel_sys_status="Open_Loop_Drive")
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.OPEN_LOOP


# ==================================================================
# Gate 3 — No O₂ fault: no DTC in P0130–P0161
# ==================================================================

def test_gate3_no_o2_fault_pass():
    """No O2 DTCs in active_dtcs → gate passes."""
    pids = _healthy_pids(active_dtcs=["P0420"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate3_o2_fault_fails():
    """P0135 in active_dtcs → O2_FAULT_ACTIVE."""
    pids = _healthy_pids(active_dtcs=["P0135"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.O2_FAULT_ACTIVE


def test_gate3_o2_fault_boundary_low():
    """P0130 (first O2 DTC) → O2_FAULT_ACTIVE."""
    pids = _healthy_pids(active_dtcs=["P0130"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.O2_FAULT_ACTIVE


def test_gate3_o2_fault_boundary_high():
    """P0161 (last O2 DTC) → O2_FAULT_ACTIVE."""
    pids = _healthy_pids(active_dtcs=["P0161"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.O2_FAULT_ACTIVE


# ==================================================================
# Gate 4 — No CKP/CMP fault: no P0335 / P0340
# ==================================================================

def test_gate4_no_ckp_cmp_fault_pass():
    """No crank/cam DTCs in active_dtcs → gate passes."""
    pids = _healthy_pids(active_dtcs=["P0420"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate4_ckp_fault_fails():
    """P0335 in active_dtcs → CKP_CMP_FAULT_ACTIVE."""
    pids = _healthy_pids(active_dtcs=["P0335"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.CKP_CMP_FAULT_ACTIVE


def test_gate4_cmp_fault_fails():
    """P0340 in active_dtcs → CKP_CMP_FAULT_ACTIVE."""
    pids = _healthy_pids(active_dtcs=["P0340"])
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.CKP_CMP_FAULT_ACTIVE


# ==================================================================
# Gate 5 — Codes not recently cleared: drive_cycles_since_clear >= 1
# ==================================================================

def test_gate5_codes_not_cleared_pass():
    """drive_cycles_since_clear >= 1 → gate passes."""
    pids = _healthy_pids(drive_cycles_since_clear=5)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate5_codes_cleared_fails():
    """drive_cycles_since_clear == 0 → CODES_RECENTLY_CLEARED."""
    pids = _healthy_pids(drive_cycles_since_clear=0)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.CODES_RECENTLY_CLEARED


def test_gate5_drive_cycles_none_fails():
    """drive_cycles_since_clear is None → CODES_RECENTLY_CLEARED."""
    pids = _healthy_pids(drive_cycles_since_clear=None)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.CODES_RECENTLY_CLEARED


# ==================================================================
# Gate 6 — Not WOT: throttle_pos < 90
# ==================================================================

def test_gate6_not_wot_pass():
    """throttle_pos < 90 → gate passes."""
    pids = _healthy_pids(throttle_pos=25)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate6_wot_fails():
    """throttle_pos >= 90 → WOT_ACTIVE."""
    pids = _healthy_pids(throttle_pos=95)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.WOT_ACTIVE


def test_gate6_wot_boundary():
    """throttle_pos == 90 → WOT_ACTIVE."""
    pids = _healthy_pids(throttle_pos=90)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.WOT_ACTIVE


def test_gate6_throttle_missing_pass():
    """Missing throttle_pos → gate passes (treat as not-WOT)."""
    pids = _healthy_pids()
    del pids["throttle_pos"]
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


# ==================================================================
# Gate 7 — Not DFCO: dfco_active is not True
# ==================================================================

def test_gate7_not_dfco_pass():
    """dfco_active is False → gate passes."""
    pids = _healthy_pids(dfco_active=False)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.VALID


def test_gate7_dfco_fails():
    """dfco_active is True → DFCO_ACTIVE."""
    pids = _healthy_pids(dfco_active=True)
    result = AnalyticsPreconditions.evaluate(pids)
    assert result == TrimAnalyticsGate.DFCO_ACTIVE


# ==================================================================
# Gate 8 — Semantic gates pass
# ==================================================================

def test_gate8_semantic_pass():
    """semantic_gates_passed == True → gate passes."""
    pids = _healthy_pids()
    result = AnalyticsPreconditions.evaluate(pids, semantic_gates_passed=True)
    assert result == TrimAnalyticsGate.VALID


def test_gate8_semantic_fails():
    """semantic_gates_passed == False → SEMANTIC_ERROR."""
    pids = _healthy_pids()
    result = AnalyticsPreconditions.evaluate(pids, semantic_gates_passed=False)
    assert result == TrimAnalyticsGate.SEMANTIC_ERROR


# ==================================================================
# All-VALID integration
# ==================================================================

def test_all_gates_pass_returns_valid():
    """Healthy PID dict with semantic_gates_passed=True → VALID."""
    pids = _healthy_pids()
    result = AnalyticsPreconditions.evaluate(pids, semantic_gates_passed=True)
    assert result == TrimAnalyticsGate.VALID


# ==================================================================
# Priority order check — first failing gate wins
# ==================================================================

def test_first_failing_gate_wins():
    """When multiple gates fail, only the first in priority order is returned."""
    # ECT cold fails gate 1, but everything else would also fail
    pids = _healthy_pids(
        coolant_temp_c=30,
        fuel_sys_status="Open_Loop_Cold",
        active_dtcs=["P0135"],
        drive_cycles_since_clear=0,
        throttle_pos=95,
        dfco_active=True,
    )
    result = AnalyticsPreconditions.evaluate(pids, semantic_gates_passed=False)
    # Gate 1 (ENGINE_COLD) has highest priority
    assert result == TrimAnalyticsGate.ENGINE_COLD


# ==================================================================
# Frozen-set DTC membership — verify ranges are complete
# ==================================================================

def test_o2_fault_dtcs_bounds():
    """Verify P0130 and P0161 are in O2_FAULT_DTCS (range endpoints)."""
    assert "P0130" in O2_FAULT_DTCS
    assert "P0161" in O2_FAULT_DTCS
    assert len(O2_FAULT_DTCS) == 32  # P0130–P0161 inclusive


def test_ckp_cmp_fault_dtcs_bounds():
    """Verify P0335 and P0340 are in CKP_CMP_FAULT_DTCS."""
    assert "P0335" in CKP_CMP_FAULT_DTCS
    assert "P0340" in CKP_CMP_FAULT_DTCS
    assert len(CKP_CMP_FAULT_DTCS) == 2
