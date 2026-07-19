from __future__ import annotations

import io
from contextlib import redirect_stdout

from wired import diagnose
from wired.composition import _build_fallback_vin_dna, _run_gaslab
from wired.run_case import load_case, main

ROUTED_CASES = (
    ("MW-002", "MW-002"),
    ("MW-009", "MW-009"),
)

KNOWN_BLOCKED_CASES = (
    ("MW-001", "CF-001"),
    ("MW-008", "SF-001"),
)


def test_run_case_cli_prints_fault_code() -> None:
    """The public CLI entry point runs one fixture and prints verdict fields."""
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(["--case", "MW-002"])

    output = stdout.getvalue()
    assert exit_code == 0
    assert "fault_code=MW-002" in output
    assert "confidence=" in output


def test_oil_cases_route_to_expected_faults() -> None:
    """Routed oil fixtures reach their live mechanical-wear verdicts."""
    for case_id, expected_fault_code in ROUTED_CASES:
        result = diagnose(load_case(case_id))

        assert result.diagnostic_verdict.fault_code == expected_fault_code


def test_known_blocked_oil_cases_document_current_non_route() -> None:
    """Rings and PCV assert the T-PREP-WIRE-1 documented non-routes."""
    for case_id, expected_non_route in KNOWN_BLOCKED_CASES:
        result = diagnose(load_case(case_id))

        assert result.diagnostic_verdict.fault_code == expected_non_route


def test_pcv_captures_gaslab_chemical_state() -> None:
    """PCV follows the ruling's non-POA known-blocked branch in the live tree."""
    raw_inputs = load_case("MW-008")
    gas_output = _run_gaslab(raw_inputs["gas"], _build_fallback_vin_dna(raw_inputs["vin"]))

    assert gas_output.chemical_state == "INCOMPLETE_OXIDATION"
    assert diagnose(raw_inputs).diagnostic_verdict.fault_code == "SF-001"
