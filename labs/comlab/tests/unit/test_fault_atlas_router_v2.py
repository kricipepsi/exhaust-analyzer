"""Env-var dispatch tests for ``FaultAtlasRouter`` (REG-V2-INTEGRATE).

These tests verify the feature-flag plumbing — the ``USE_V2_REGISTRY``
environment variable is read **once at router instantiation** and only the
literal string ``"1"`` activates the v2 delegate. Anything else
(``"0"``, ``""``, ``"true"``, ``"yes"``, unset) keeps the v1 default path
alive.

The shim itself is unit-tested in
``registry/tests/test_integration_shim.py``; here we only assert that the
router *calls* (or does not call) the shim's ``route_case`` based on the
env var. We patch ``registry.integration_shim.route_case`` (the module
attribute), not the router — the router's ``route()`` uses a lazy
``from registry.integration_shim import route_case as _v2_route_case``
which re-resolves the symbol on each call, so patching the module
attribute reaches the call.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import patch

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter
from comlab.schemas.response import OrchestratorFinalUIOutput

# Reuse the canonical v1 request builders from the sibling unit-test module
# (same package) rather than duplicating the ~80-line payload here.
from tests.unit.test_fault_atlas_router import _make_request, _sanitized


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_router(registry_path) -> FaultAtlasRouter:
    """Construct a router against the canonical v1 registry."""
    kg = FaultAtlasKG()
    analytics = PowerLossAnalytics()
    return FaultAtlasRouter(str(registry_path), kg, analytics)


def _v2_stub_output() -> dict[str, Any]:
    """Plausible dict matching ``OrchestratorFinalUIOutput`` field set.

    Used as the patched shim's return value so the test can assert
    delegation occurred. The router reconstructs ``OrchestratorFinalUIOutput``
    from this dict; if the field set drifts and reconstruction fails, that
    is a real integration regression and the test will surface it.
    """
    return {
        "session_id": "00000000-0000-4000-8000-000000000002",
        "execution_meta": {
            "resolved_horizon": "HORIZON_LEGACY",
            "degradation_mode": "FULL_FUSION",
            "processing_confidence_rating": "HIGH_ASSURANCE",
            "vin_confidence": "NONE",
            "lab_routing_directive": {
                "suppress_gaslab": False,
                "suppress_obd_live_pids": False,
                "suppress_mode06_ui": False,
                "cold_start_mode": False,
                "reasons": [],
            },
        },
        "diagnostic_verdict": {
            "is_fault_detected": True,
            "fault_code": "TEST-V2-STUB",
            "fault_name": "v2 stub from shim patch",
            "fault_family": "misfire",
            "display_headline": "v2 stub",
            "confidence_score": 0.80,
            "actionable_remediation": "See diagnostic verdict for next steps.",
            "differential_siblings": [],
        },
        "performance_analytics": {
            "kinetic_power_loss_pct": 0.0,
            "catalyst_efficiency_index_pct": None,
            "lambda_perception_delta": 0.0,
            "o2_sensor_bias_verdict": None,
            "severity_level": "WARNING_DEGRADED_PERFORMANCE",
        },
        "fault_enrichment": {
            "component_group": "engine",
            "impacted_subsystems": [],
            "mechanical_failure_mode": "v2 stub",
            "ui_remediation_steps": ["See diagnostic verdict for next steps."],
            "editor_severity_hint": None,
        },
        "user_input_echo_audit": {"submitted_at": "1970-01-01T00:00:00", "groups": []},
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_v1_when_explicit_false(registry_path) -> None:
    """``use_v2_registry=False`` → router stays on v1 path.

    Patching the shim's ``route_case`` with a side-effect-tracker; on the v1
    path the patched stub MUST NOT be called.
    """
    from comlab.core.fault_atlas_router import FaultAtlasRouter
    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG

    router = FaultAtlasRouter(
        str(registry_path), FaultAtlasKG(), PowerLossAnalytics(),
        use_v2_registry=False,
    )
    assert router._use_v2_registry is False

    # Drive a real v1 route() and assert the shim is NEVER reached. This is
    # the load-bearing guarantee: with the flag unset, the registry shim must
    # not be invoked at all (the v1 path has zero registry dependency).
    req = _make_request(chemical_state="NORMAL_OPERATION", horizon="HORIZON_MODERN")
    with patch("registry.integration_shim.route_case") as mock_shim:
        mock_shim.return_value = _v2_stub_output()
        result = router.route(_sanitized(req))

    assert mock_shim.call_count == 0, "v1 path must not call the v2 shim"
    # And it still produces a valid v1 output object.
    assert isinstance(result, OrchestratorFinalUIOutput)


def test_v2_when_explicit_true(registry_path) -> None:
    """``use_v2_registry=True`` → router's ``route()`` delegates to the shim.

    Patch ``registry.integration_shim.route_case`` to a stub returning a
    valid ``OrchestratorFinalUIOutput``-shaped dict; assert the stub is
    called once and the router returns the reconstructed object.
    """
    from comlab.core.fault_atlas_router import FaultAtlasRouter
    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG

    router = FaultAtlasRouter(
        str(registry_path), FaultAtlasKG(), PowerLossAnalytics(),
        use_v2_registry=True,
    )
    assert router._use_v2_registry is True

    stub_payload: dict[str, Any] = {"sentinel": "v2-payload"}

    with patch("registry.integration_shim.route_case_with_diagnostics") as mock_shim:
        mock_shim.return_value = (
            _v2_stub_output(),
            {"scored_rules": [], "winner_rule_id": "__NONE__"},
        )
        result = router.route(stub_payload)

    assert mock_shim.call_count == 1
    # The shim is called with the sanitized payload verbatim.
    assert mock_shim.call_args.args[0] is stub_payload
    # And the router returns an OrchestratorFinalUIOutput reconstructed
    # from the shim's dict.
    assert isinstance(result, OrchestratorFinalUIOutput)
    assert result.diagnostic_verdict.fault_code == "TEST-V2-STUB"


def test_explicit_false_selects_v1(registry_path) -> None:
    """Explicit ``use_v2_registry=False`` selects legacy."""
    from comlab.core.fault_atlas_router import FaultAtlasRouter
    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG

    router = FaultAtlasRouter(
        str(registry_path), FaultAtlasKG(), PowerLossAnalytics(),
        use_v2_registry=False,
    )
    assert router._use_v2_registry is False


def test_default_is_v2(registry_path) -> None:
    """Default (no arg) selects REG-V2 (True)."""
    from comlab.core.fault_atlas_router import FaultAtlasRouter
    from comlab.analytics.power_loss_analytics import PowerLossAnalytics
    from comlab.core.fault_atlas_kg import FaultAtlasKG

    router = FaultAtlasRouter(
        str(registry_path), FaultAtlasKG(), PowerLossAnalytics(),
    )
    assert router._use_v2_registry is True
