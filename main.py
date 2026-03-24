#!/usr/bin/env python3
"""
Petrol Diagnostic Engine - Main Entry Point
4D System using Bretschneider's Formula
"""

from core.validator import validate_gas_data, check_probe_placement
from core.bretschneider import calculate_lambda
from core.catalyst import catalyst_efficiency
from core.matrix import match_case
from core.reporter import generate_report
import json

def main():
    # Load knowledge base
    with open('data/master_knowledge_base.json', 'r') as f:
        kb = json.load(f)

    # Example data (will be replaced by UI/API input)
    low_idle = {
        'co': 0.12,
        'co2': 14.8,
        'hc': 25,
        'o2': 0.25,
        'lambda': 1.01,
        'nox': 50
    }
    measured_lambda = 1.01
    fuel_type = 'e10'

    # 1. Validate
    valid, msg = validate_gas_data(low_idle)
    if not valid:
        print(f"Validation Error: {msg}")
        return

    # 2. Check probe placement
    probe_check = check_probe_placement(low_idle['co'], low_idle['co2'])
    if probe_check:
        print(f"Probe Warning: {probe_check['message']}")
        # Continue or return based on severity

    # 3. Calculate Bretschneider (Theoretical Lambda)
    calc_result = calculate_lambda(
        low_idle['co'], low_idle['co2'], low_idle['hc'], low_idle['o2'], fuel_type
    )
    calculated_lambda = calc_result['lambda']

    # 4. Catalyst Efficiency
    cat_eff, cat_status = catalyst_efficiency(low_idle, config=kb.get('catalyst_config'))

    # 5. Match case from static knowledge graph
    high_idle = None  # Set to a dict of gas readings at ~2500 RPM for differential diagnosis
    matched_case = match_case(low_idle, calculated_lambda, measured_lambda, kb, high_idle=high_idle)

    # 6. Generate final report
    report = generate_report(
        low_idle=low_idle,
        measured_lambda=measured_lambda,
        calculated_lambda=calculated_lambda,
        cat_eff=cat_eff,
        cat_status=cat_status,
        matched_case=matched_case,
        knowledge_base=kb
    )

    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
