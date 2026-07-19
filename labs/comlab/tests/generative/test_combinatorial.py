"""Bounded categorical combinatorial coverage for COMLab (T-COMTST-3)."""

from __future__ import annotations

from itertools import product
from typing import Any

from pydantic import ValidationError

from comlab.schemas.ingestion import OrchestratorInboundRequest
from comlab.schemas.response import OrchestratorFinalUIOutput
from tests.fixtures.descriptor import build_comlab_descriptor

_DESCRIPTOR = build_comlab_descriptor()
_AXIS_LIMIT = 4  # wiki: 12_corpus_eval_discipline.md §CONCEPT_CEILING — bounded non-accuracy coverage

_DEGRADATION_SCENARIOS: dict[str, dict[str, str]] = {
    "FULL_FUSION": {
        "gas_scenario": "warm_idle_baseline",
        "obd_scenario": "warm_idle_baseline",
        "dtc_scenario": "no_codes",
        "symptom_scenario": "neutral",
    },
    "GAS_DOMINANT": {
        "gas_scenario": "no_obd_legacy",
        "obd_scenario": "none",
        "dtc_scenario": "no_codes",
        "symptom_scenario": "will_not_start",
    },
    "SINGLE_POINT": {
        "gas_scenario": "healthy_baseline",
        "obd_scenario": "warm_idle_baseline",
        "dtc_scenario": "no_codes",
        "symptom_scenario": "neutral",
    },
    "FATAL_INCOMPLETE": {
        "gas_scenario": "sample_invalid",
        "obd_scenario": "warm_idle_baseline",
        "dtc_scenario": "no_codes",
        "symptom_scenario": "running",
    },
}


def _axis_values(name: str) -> list[str]:
    """Read one categorical axis from the COMLab descriptor."""
    field = _DESCRIPTOR.get_field(name)
    assert field is not None, f"descriptor field missing: {name}"
    assert field.enum_values, f"descriptor field is not categorical: {name}"
    return field.enum_values


def _representative(values: list[str], limit: int = _AXIS_LIMIT) -> list[str]:
    """Select stable, evenly spaced representatives from a categorical axis."""
    if len(values) <= limit:
        return values
    indexes = {(index * (len(values) - 1)) // (limit - 1) for index in range(limit)}
    return [values[index] for index in sorted(indexes)]


def _base_row(degradation: str) -> dict[str, str]:
    """Build descriptor input metadata for one degradation scenario."""
    return {
        "case_id": f"GEN-{degradation}",
        "family_hint": "characterization",
        "metadata_horizon": "HORIZON_MODERN",
        "metadata_vin": "1FA6P8CF0HXXXXXXX",
        "metadata_cylinders": "4",
        **_DEGRADATION_SCENARIOS[degradation],
    }


def _build_request(
    degradation: str,
    chemical_state: str,
    routing_tag: str,
    horizon: str,
) -> OrchestratorInboundRequest:
    """Assemble and validate one categorical product member."""
    request = _DESCRIPTOR.build_args(_base_row(degradation))[0]
    raw: dict[str, Any] = request.model_dump(mode="json")
    raw["metadata"]["resolved_horizon"] = horizon
    raw["gas_lab_output"]["chemical_state"] = chemical_state
    dtc_payload = raw["dtc_lab_output"]
    assert isinstance(dtc_payload, dict)
    dtc_payload["routing_tags"] = [routing_tag]
    return OrchestratorInboundRequest.model_validate(raw)


def test_combinatorial_comlab() -> None:
    """Every bounded categorical combination fails closed or returns valid output."""
    degradation_axis = _axis_values("degradation_mode")
    chemical_axis = _representative(_axis_values("gas_chemical_state"))
    routing_axis = _representative(_axis_values("dtc_routing_tag"))
    horizon_axis = _axis_values("metadata_horizon")
    cases = list(
        product(
            degradation_axis,
            chemical_axis,
            routing_axis,
            horizon_axis,
        )
    )

    valid_outputs = 0
    validation_failures = 0
    for degradation, chemical_state, routing_tag, horizon in cases:
        try:
            request = _build_request(
                degradation,
                chemical_state,
                routing_tag,
                horizon,
            )
        except ValidationError:
            validation_failures += 1
            continue

        result = _DESCRIPTOR.entry_point(request)
        assert isinstance(result, OrchestratorFinalUIOutput)
        valid_outputs += 1

    print(
        "\nCOMLab combinatorial coverage: "
        f"{len(cases)} cases "
        f"({valid_outputs} valid outputs, {validation_failures} validation failures); "
        f"axes=degradation:{len(degradation_axis)}, "
        f"chemical:{len(chemical_axis)}, routing:{len(routing_axis)}, "
        f"horizon:{len(horizon_axis)}"
    )
    assert cases
    assert valid_outputs + validation_failures == len(cases)
