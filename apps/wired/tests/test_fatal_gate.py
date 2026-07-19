from __future__ import annotations

import io
from contextlib import redirect_stdout
from copy import deepcopy

from wired import diagnose
from wired.run_case import load_case, main

NORMAL_CASE_ID = "MW-002"
INVALID_CASE_ID = "INVALID_sample"
FATAL_DEGRADATION = "FATAL_INCOMPLETE"
INVALID_SAMPLE_ABORT = "ERR-ABORT-001"


def test_default_off_verdict_unchanged() -> None:
    """Fatal gates are default-off and preserve the existing verdict bytes."""
    raw_inputs = load_case(NORMAL_CASE_ID)

    default_verdict = diagnose(deepcopy(raw_inputs)).diagnostic_verdict.model_dump_json()
    explicit_off_verdict = diagnose(
        deepcopy(raw_inputs),
        enable_fatal_gates=False,
    ).diagnostic_verdict.model_dump_json()

    assert explicit_off_verdict == default_verdict


def test_invalid_reaches_fatal_incomplete() -> None:
    """Explicit fatal gates turn an invalid GAS sample into FATAL_INCOMPLETE."""
    result = diagnose(load_case(INVALID_CASE_ID), enable_fatal_gates=True)

    assert result.execution_meta.degradation_mode == FATAL_DEGRADATION
    assert result.diagnostic_verdict.fault_code == INVALID_SAMPLE_ABORT


def test_run_case_fatal_gate_flag_prints_flagged_result() -> None:
    """The public CLI flag forwards fatal-gate mode and prints the flagged outcome."""
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        exit_code = main(["--case", INVALID_CASE_ID, "--fatal-gates"])

    output = stdout.getvalue()
    assert exit_code == 0
    assert f"fault_code={INVALID_SAMPLE_ABORT}" in output
    assert f"degradation={FATAL_DEGRADATION}" in output
