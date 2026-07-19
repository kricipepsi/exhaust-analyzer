"""Fail-closed malformed and sentinel input fuzz for COMLab (T-COMTST-3)."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Callable

import pytest
from pydantic import ValidationError

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest
from tests.fixtures.descriptor import build_comlab_descriptor

_DESCRIPTOR = build_comlab_descriptor()


def _valid_raw_request() -> dict[str, Any]:
    """Return a fresh valid inbound payload for mutation."""
    row = {
        "case_id": "FUZZ-BASE",
        "family_hint": "characterization",
        "metadata_horizon": "HORIZON_MODERN",
        "metadata_vin": "1FA6P8CF0HXXXXXXX",
        "metadata_cylinders": "4",
        "gas_scenario": "warm_idle_baseline",
        "obd_scenario": "warm_idle_baseline",
        "dtc_scenario": "no_codes",
        "symptom_scenario": "neutral",
    }
    request = _DESCRIPTOR.build_args(row)[0]
    return request.model_dump(mode="json")


def _delete_metadata(raw: dict[str, Any]) -> None:
    del raw["metadata"]


def _delete_gas_key(raw: dict[str, Any]) -> None:
    del raw["gas_lab_output"]["gas_co2"]


def _empty_gas(raw: dict[str, Any]) -> None:
    raw["gas_lab_output"] = {}


def _empty_obd(raw: dict[str, Any]) -> None:
    raw["obd_live_data"] = {}


def _empty_dtc(raw: dict[str, Any]) -> None:
    raw["dtc_lab_output"] = {}


def _negative_sentinel(raw: dict[str, Any]) -> None:
    raw["gas_lab_output"]["gas_hc"] = -127  # wiki: 12_corpus_eval_discipline.md §CONCEPT_CEILING


def _high_sentinel(raw: dict[str, Any]) -> None:
    raw["gas_lab_output"]["gas_co"] = 999  # wiki: 12_corpus_eval_discipline.md §CONCEPT_CEILING


def _wrong_sample_enum(raw: dict[str, Any]) -> None:
    raw["gas_lab_output"]["sample_validity"] = "NOT_A_VALIDITY"


def _wrong_o2_enum(raw: dict[str, Any]) -> None:
    raw["obd_live_data"]["o2_failure_mode"] = "NOT_AN_O2_MODE"


def _wrong_routing_enum(raw: dict[str, Any]) -> None:
    raw["dtc_lab_output"]["routing_tags"] = ["NOT_A_ROUTING_TAG"]


def _bad_dtc_regex(raw: dict[str, Any]) -> None:
    raw["dtc_lab_output"]["confirmed_dtcs"] = ["P03ZZ"]


_FUZZ_CASES: list[tuple[str, Callable[[dict[str, Any]], None]]] = [
    ("missing_metadata", _delete_metadata),
    ("missing_gas_key", _delete_gas_key),
    ("empty_gas_block", _empty_gas),
    ("empty_obd_block", _empty_obd),
    ("empty_dtc_block", _empty_dtc),
    ("sentinel_minus_127", _negative_sentinel),
    ("sentinel_999", _high_sentinel),
    ("wrong_sample_enum", _wrong_sample_enum),
    ("wrong_o2_enum", _wrong_o2_enum),
    ("wrong_routing_enum", _wrong_routing_enum),
    ("bad_dtc_regex", _bad_dtc_regex),
]


@pytest.mark.parametrize(
    "label,mutate",
    _FUZZ_CASES,
    ids=[label for label, _ in _FUZZ_CASES],
)
def test_fuzz_comlab(
    label: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    """Each malformed payload is rejected or reaches the fatal terminal."""
    raw = deepcopy(_valid_raw_request())
    mutate(raw)

    try:
        request = OrchestratorInboundRequest.model_validate(raw)
    except ValidationError:
        return

    result = LabPipelineAggregator().process(request)
    assert result.execution_meta.degradation_mode == "FATAL_INCOMPLETE", (
        f"{label}: malformed input was accepted without fatal degradation"
    )
