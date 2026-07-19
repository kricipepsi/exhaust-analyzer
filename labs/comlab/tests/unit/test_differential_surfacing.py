"""T-V3-3 differential sibling surfacing regression tests."""

from __future__ import annotations

from typing import Any, cast

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter, RegistryRow
from tests.unit.test_fault_atlas_router import _make_request, _sanitized


def _router(registry_path: Any, *, use_v2_registry: bool) -> FaultAtlasRouter:
    """Build a router for differential sibling output assertions."""
    return FaultAtlasRouter(
        str(registry_path),
        FaultAtlasKG(),
        PowerLossAnalytics(),
        use_v2_registry=use_v2_registry,
    )


def _registry_row(fault_id: str, fault_name: str) -> RegistryRow:
    """Build a minimal v1 registry row for merge-only sibling tests."""
    return RegistryRow(
        fault_id=fault_id,
        fault_name=fault_name,
        target_horizons=["HORIZON_MODERN"],
        preconditions={},
        cross_domain_matrix=cast(
            Any,
            {
                "gas_lab_state": "NORMAL_OPERATION",
                "obd_live_pids": {},
                "dtc_lab_status": {
                    "active_mil": False,
                    "p_code_match": [],
                    "fallback_strategy": "PROCEED_ON_MATCH_OR_EMPTY",
                },
            },
        ),
        confidence_scoring=cast(
            Any,
            {"base_weight": 0.5, "bonus_on_dtc_match": 0.0},
        ),
    )


def test_merge_siblings_populates_fault_family(registry_path: Any) -> None:
    """Runtime and editor-curated siblings carry KG-resolved fault families."""
    router = _router(registry_path, use_v2_registry=False)
    runtime = [(_registry_row("ERR-CF-001", "catalyst_efficiency_below_threshold"), 0.9)]

    result = router._merge_differential_siblings(runtime, ["ERR-MF-001"])

    assert result[0].fault_id == "ERR-CF-001"
    assert result[0].fault_family == "catalyst_failure"
    assert result[0].source == "runtime"
    assert result[1].fault_id == "ERR-MF-001"
    assert result[1].fault_family == "misfire"
    assert result[1].source == "editor_curated"


def test_v2_route_surfaces_ranked_differential_with_family(registry_path: Any) -> None:
    """The REG-v2 output path emits runtime siblings with fault_family populated."""
    router = _router(registry_path, use_v2_registry=True)
    request = _make_request(
        chemical_state="LEAN_MIXTURE",
        gas_o2=5.0,
        lambda_chem=1.12,
        confirmed_dtcs=["P0171"],
        active_mil=True,
        short_term_ft1=18.0,
        long_term_ft1=12.0,
        obd_shrtft1=18.0,
        obd_longft1=12.0,
    )

    output = router.route(_sanitized(request))
    siblings = output.diagnostic_verdict.differential_siblings

    assert siblings
    assert all(sibling.source == "runtime" for sibling in siblings)
    assert all(sibling.fault_family for sibling in siblings)
    assert output.diagnostic_verdict.fault_code not in {
        sibling.fault_id for sibling in siblings
    }
