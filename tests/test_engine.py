"""Test suite for the petrol diagnostic engine."""

import pytest
import json
from pathlib import Path

from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.matrix import match_case
from core.validator import validate_gas_data, check_probe_placement
from core.reporter import generate_report

from .calibration_data import GOLD_STANDARD, FAIL_STANDARD

# Load knowledge base for matrix tests
_KB_PATH = Path(__file__).parent.parent / "data" / "master_knowledge_base.json"


def _load_knowledge_base():
    with open(_KB_PATH, 'r') as f:
        return json.load(f)


def test_bretschneider_gold():
    """All gold standard cases should yield lambda within 0.02 of expected."""
    for case in GOLD_STANDARD:
        result = calculate_lambda(case['co'], case['co2'], case['hc'], case['o2'])
        calculated_lambda = result['lambda']
        expected = case['lambda']
        assert abs(calculated_lambda - expected) < 0.02, \
            f"Lambda mismatch in {case['case_id']}: got {calculated_lambda}, expected {expected}"


def test_bretschneider_fail_cases():
    """Fail cases should yield lambda outside stoichiometric range (mostly)."""
    for case in FAIL_STANDARD:
        result = calculate_lambda(case['co'], case['co2'], case['hc'], case['o2'])
        calculated_lambda = result['lambda']
        expected = case['lambda']
        # Allow wider tolerance for extreme cases
        assert abs(calculated_lambda - expected) < 0.05, \
            f"Lambda mismatch in {case['case_id']}: got {calculated_lambda}, expected {expected}"


def test_catalyst_efficiency_optimal():
    """Clean gases should result in >90% efficiency and 'Optimal' status."""
    gas = {'co2': 15.0, 'co': 0.1, 'o2': 0.2}
    eff, status = catalyst_efficiency(gas)
    assert eff > 90, f"Expected >90%, got {eff}%"
    assert status == "Optimal", f"Expected 'Optimal', got '{status}'"


def test_catalyst_efficiency_failed():
    """High CO and O2 should result in <80% efficiency and 'Failed' status."""
    gas = {'co2': 10.0, 'co': 1.0, 'o2': 1.0}
    eff, status = catalyst_efficiency(gas)
    assert eff < 80, f"Expected <80%, got {eff}%"
    assert status == "Failed", f"Expected 'Failed', got '{status}'"


def test_catalyst_efficiency_aged():
    """Medium efficiency should yield 'Aged/Marginal'."""
    gas = {'co2': 13.0, 'co': 0.5, 'o2': 0.4}
    eff, status = catalyst_efficiency(gas)
    assert 80 < eff <= 95, f"Expected 81-95%, got {eff}%"
    assert status == "Aged/Marginal", f"Expected 'Aged/Marginal', got '{status}'"


def test_validator_accepts_gold_ranges():
    """Gold standard gas values should pass validation."""
    for case in GOLD_STANDARD:
        gas = {
            'co': case['co'],
            'co2': case['co2'],
            'hc': case['hc'],
            'o2': case['o2'],
            'lambda': case['lambda']
        }
        valid, msg = validate_gas_data(gas)
        assert valid, f"Gold case {case['case_id']} failed validation: {msg}"


def test_validator_rejects_out_of_range():
    """Out-of-range values should be rejected."""
    gas = {'co': 15.0, 'co2': 15.0, 'hc': 100, 'o2': 1.0}  # CO way too high
    valid, msg = validate_gas_data(gas)
    assert not valid, "Should reject CO=15"


def test_probe_placement_warning():
    """Low CO+CO2 should trigger warning."""
    result = check_probe_placement(co=0.1, co2=5.0, threshold=12.0)
    assert result is not None
    assert 'warning' in result
    assert result['total'] == 5.1


def test_probe_placement_ok():
    """Adequate CO+CO2 should return None."""
    result = check_probe_placement(co=0.5, co2=12.0, threshold=12.0)
    assert result is None


def test_matrix_matches_vacuum_leak():
    """Should match Vacuum Leak case: high lambda at idle, low O2."""
    kb = _load_knowledge_base()
    low_idle = {
        'lambda': 1.15,
        'co': 0.10,
        'co2': 11.5,
        'hc': 450,
        'o2': 3.5
    }
    case = match_case(low_idle, 1.16, 1.15, kb)
    assert case['case_id'] == 'P_001', f"Expected P_001, got {case['case_id']}"


def test_matrix_matches_healthy_engine():
    """Should match Healthy Engine case."""
    kb = _load_knowledge_base()
    low_idle = {
        'lambda': 1.00,
        'co': 0.10,
        'co2': 15.1,
        'hc': 20,
        'o2': 0.15
    }
    case = match_case(low_idle, 1.00, 1.00, kb)
    assert case['case_id'] == 'P_100', f"Expected P_100, got {case['case_id']}"


def test_matrix_fallback_on_no_match():
    """Should return fallback case when no pattern matches."""
    kb = _load_knowledge_base()
    low_idle = {
        'lambda': 1.50,  # extreme condition not in matrix
        'co': 1.0,
        'co2': 10.0,
        'hc': 1000,
        'o2': 5.0
    }
    case = match_case(low_idle, 1.50, 1.50, kb)
    assert case['case_id'] == 'FALLBACK_001'


def test_reporter_penalties_applied():
    """Report should apply lambda delta and catalyst penalties."""
    kb = _load_knowledge_base()
    low_idle = {'lambda': 1.0}
    matched_case = {
        'case_id': 'P_100',
        'name': 'Healthy Engine',
        'verdict': 'OK',
        'action': 'None',
        'health_score': 100
    }

    # Lambda delta > 0.05 AND catalyst < 80
    report = generate_report(
        low_idle=low_idle,
        measured_lambda=1.10,
        calculated_lambda=1.00,  # delta = 0.10
        cat_eff=70,
        cat_status="Failed",
        matched_case=matched_case,
        knowledge_base=kb
    )

    # Base health 100 - 10 (lambda penalty) - 15 (catalyst penalty) = 75
    assert report['overall_health'] == 75
    assert report['cat_efficiency'] == 70
    assert report['lambda_delta'] == 0.1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
