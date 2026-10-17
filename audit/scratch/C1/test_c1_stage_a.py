"""C1 probes: Stage A degradation / suppression / era handling / payload gaps."""
from __future__ import annotations

import logging

import pytest

from c1_builders import aggregator, request, run

logging.disable(logging.CRITICAL)

RUNNING = {"environmental_conditions": {"engine_state": "running", "occurs_during": "always"}}


# --- F9: degradation_mode never reflects OBD absence / suppression / single point ----

def test_cranking_obd_suppressed_is_gas_dominant():
    """wiki 07 §RULE_LAB_SUPPRESSION: 'OBD suppression sets degradation_mode = GAS_DOMINANT'."""
    out = run(request(chem="RICH_MIXTURE", symptom={
        "environmental_conditions": {"engine_state": "cranking", "occurs_during": "always"}}))
    m = out.execution_meta
    print("suppress_obd:", m.lab_routing_directive.suppress_obd_live_pids, "mode:", m.degradation_mode)
    assert m.lab_routing_directive.suppress_obd_live_pids is True
    assert m.degradation_mode == "GAS_DOMINANT"


def test_legacy_without_obd_is_gas_dominant():
    """BDD 'A legacy car without a scanner degrades to gas-dominant'."""
    out = run(request(chem="RICH_MIXTURE", horizon="HORIZON_LEGACY", include_obd=False))
    print("mode:", out.execution_meta.degradation_mode)
    assert out.execution_meta.degradation_mode == "GAS_DOMINANT"


def test_no_second_frame_is_single_point():
    """BDD 'Without a second frame the path is single-point'."""
    out = run(request(chem="RICH_MIXTURE"))
    print("second_operating_point: None  mode:", out.execution_meta.degradation_mode)
    assert out.execution_meta.degradation_mode == "SINGLE_POINT"


# --- F11: invalid gas sample still yields a chemistry-based fault on the default path --

def test_invalid_sample_does_not_produce_fault_verdict_by_default():
    """ADR-0007: 'chemistry trust depends on a clean sample, so GASLab's validity gate must
    pass first (Stage A ERR-ABORT-001)'. Production calls process() with fatal gates off."""
    out = run(request(chem="RICH_MIXTURE", gas_kw={"sample_validity": "INVALID"}))
    v = out.diagnostic_verdict
    print("INVALID ->", v.fault_code, v.fault_family, v.is_fault_detected,
          out.execution_meta.degradation_mode)
    assert out.execution_meta.degradation_mode == "FATAL_INCOMPLETE" or not v.is_fault_detected


# --- F12: EXTERNAL_O2_SUSPECT ('warn but continue') aborts -------------------------

def test_external_o2_suspect_continues_with_fatal_gates_on():
    out = run(request(chem="RICH_MIXTURE", gas_kw={"sample_validity": "EXTERNAL_O2_SUSPECT"}),
              enable_fatal_gates=True)
    print("EXTERNAL_O2_SUSPECT ->", out.diagnostic_verdict.fault_code,
          out.execution_meta.degradation_mode)
    # vocabulary.py SampleValidity.EXTERNAL_O2_SUSPECT: "warn but continue"
    assert out.execution_meta.degradation_mode != "FATAL_INCOMPLETE"


# --- F13: suppressed GASLab data still drives the verdict ------------------------------

def test_will_not_start_does_not_score_suppressed_gas():
    """wiki 07: 'Suppression skips that lab's fatal gates and excludes its data from the matrix'."""
    out = run(request(chem="RICH_MIXTURE", symptom={
        "environmental_conditions": {"engine_state": "will_not_start", "occurs_during": "always"}}))
    v = out.diagnostic_verdict
    print("suppress_gaslab:", out.execution_meta.lab_routing_directive.suppress_gaslab,
          "verdict:", v.fault_code, v.fault_family, v.confidence_score)
    assert out.execution_meta.lab_routing_directive.suppress_gaslab is True
    assert v.fault_family != "rich_mixture"


# --- F10: unknown horizon string silently becomes MODERN -----------------------------

@pytest.mark.parametrize("bad", ["", "HORIZON_FOO", "horizon_legacy"])
def test_unknown_horizon_is_rejected_or_flagged(bad):
    try:
        req = request(chem="RICH_MIXTURE", horizon=bad)
    except Exception as exc:  # schema rejection would satisfy the claim
        pytest.skip(f"schema rejected {bad!r}: {type(exc).__name__}")
    out = run(req)
    print(repr(bad), "->", out.execution_meta.resolved_horizon,
          out.execution_meta.processing_confidence_rating)
    # Scope 1990-2010 (ADR-0004); an unresolvable era must not be reported as a resolved MODERN
    # era with HIGH_ASSURANCE.
    assert out.execution_meta.resolved_horizon != "HORIZON_MODERN"


# --- F14: v1 (SINGLE_POINT fallback) path crashes when DTCLab output is absent ---------

def test_v1_path_accepts_missing_dtc_lab_output():
    """OrchestratorInboundRequest.dtc_lab_output is Optional (default None)."""
    agg = aggregator(use_v2_registry=False)
    out = agg.process(request(chem="RICH_MIXTURE", include_dtc=False))
    print("v1 no-DTC ->", out.diagnostic_verdict.fault_code)


# --- F-dead-fuses: Phase-5 evidence gates unreachable from production ---------------

def test_open_loop_trim_evidence_is_capped_on_production_path():
    """ADR-0010: 'open-loop trim evidence is capped (_OPEN_LOOP_TRIM_CONFIDENCE_CAP = 0.60)';
    BDD 'Trim evidence is suppressed outside closed loop': OL_FAULT -> 'trim-based findings
    are suppressed'. Gas chemistry is stoichiometric (NORMAL_OPERATION, ADR-0007 truth); the
    only lean evidence is +20 % LTFT / +10 % STFT reported while the loop is open on O2 fault."""
    from c1_builders import ff
    out = {}
    for fs in ("CL", "OL_FAULT"):
        out[fs] = run(request(
            chem="NORMAL_OPERATION",
            obd_kw=dict(total_trim_correction_delta=30.0, shrtft1=10.0, longft1=20.0,
                        fuel_system_status=fs),
            dtc_kw=dict(freeze=ff(fuel_system_status=fs, short_term_ft1=10.0,
                                  long_term_ft1=20.0, manifold_pressure_kpa=45.0))))
        v = out[fs].diagnostic_verdict
        print(fs, "->", v.fault_code, v.fault_family, round(v.confidence_score, 3))
    v = out["OL_FAULT"].diagnostic_verdict
    assert v.fault_family not in ("lean_condition", "rich_mixture") or v.confidence_score <= 0.60
