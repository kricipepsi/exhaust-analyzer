"""COMLab categorical descriptor and assembled upstream-verdict fixtures."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, get_args
from uuid import uuid4

_HARNESS_ROOT = Path(__file__).resolve().parents[4] / "harness"
if str(_HARNESS_ROOT) not in sys.path:
    sys.path.insert(0, str(_HARNESS_ROOT))

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator  # noqa: E402
from comlab.schemas.ingestion import OrchestratorInboundRequest  # noqa: E402
from comlab.schemas.response import (  # noqa: E402
    ConfidenceLit,
    DegradationLit,
    FaultFamilyLit,
    HorizonLit,
    OrchestratorFinalUIOutput,
)
from comlab.schemas.vocabulary import (  # noqa: E402
    DTCRoutingTag,
    EngineStateBucket,
    HistoricalFaultContext,
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    SampleValidity,
    TrimAnalyticsGate,
    VEValidity,
)
from harness.descriptor import FieldRange, ModuleDescriptor  # noqa: E402
from tests.fixtures import mock_dtc_lab, mock_gas_lab, mock_obd_lab  # noqa: E402

_EXPECTED_COLS = (
    "expected_top_fault",
    "expected_fault_family",
    "expected_degradation_mode",
    "expected_confidence",
)

_GAS_SCENARIOS = {
    name: getattr(mock_gas_lab, name)
    for name in (
        "catalyst_overwhelmed",
        "exhaust_air_leak",
        "healthy_baseline",
        "ignition_misfire_heavy_hc",
        "incomplete_combustion",
        "no_obd_legacy",
        "rich_unmetered_intrusion",
        "sample_invalid",
        "warm_idle_baseline",
        "cam_timing_retarded_map",
    )
}
_OBD_SCENARIOS = {
    name: getattr(mock_obd_lab, name)
    for name in (
        "cold_engine",
        "coil_arc_under_load",
        "hpfp_leak_signature",
        "legacy_missing_trims",
        "no_obd_channel",
        "sensor_biased_high",
        "sensor_biased_low",
        "warm_idle_baseline",
    )
}
_DTC_SCENARIOS = {
    name: getattr(mock_dtc_lab, name)
    for name in (
        "full_confirmed",
        "malformed_dtc",
        "no_codes",
        "p0016_cam_timing_retard",
        "p0171_exhaust_leak_manifold",
        "p0172_rich_hpfp_leak",
        "p0300_mechanical_wear",
        "p0302_misfire_coil_arc",
        "p0351_ignition_coil_driver",
        "p0401_egr_stuck_open",
        "p0420_catalyst_below_threshold",
    )
}


def _dtc_payload(code: str, routing_tag: str) -> dict[str, Any]:
    payload = mock_dtc_lab.no_codes()
    payload["active_mil"] = True
    payload["confirmed_dtcs"] = [code]
    payload["routing_tags"] = [routing_tag]
    return payload


def _build_dtc_scenario(name: str) -> dict[str, Any] | None:
    if name == "none":
        return None
    if name == "p0131_o2_sensor":
        return _dtc_payload("P0131", "O2_HISTORY")
    if name == "p0335_nonstarter":
        return _dtc_payload("P0335", "MISFIRE_HISTORY")
    if name == "p0606_ecu_internal":
        return _dtc_payload("P0606", "ECU_INTERNAL_HISTORY")
    try:
        return _DTC_SCENARIOS[name]()
    except KeyError as exc:
        raise ValueError(f"unknown DTC scenario: {name!r}") from exc


def _build_args(row: dict[str, str]) -> tuple[OrchestratorInboundRequest]:
    """Assemble one validated COMLab request from a fixture row."""
    try:
        gas_payload = _GAS_SCENARIOS[row["gas_scenario"].strip()]()
        obd_name = row["obd_scenario"].strip()
        obd_payload = None if obd_name == "none" else _OBD_SCENARIOS[obd_name]()
    except KeyError as exc:
        raise ValueError(f"unknown upstream scenario: {exc.args[0]!r}") from exc

    symptom_scenario = row["symptom_scenario"].strip()
    symptom_dna = (
        {}
        if symptom_scenario == "neutral"
        else {"environmental_conditions": {"engine_state": symptom_scenario}}
    )

    request = OrchestratorInboundRequest.model_validate(
        {
            "metadata": {
                "session_id": str(uuid4()),
                "vin_dna_string": row["metadata_vin"].strip(),
                "resolved_horizon": row["metadata_horizon"].strip(),
                "cylinder_count": int(row["metadata_cylinders"]),
            },
            "gas_lab_output": gas_payload,
            "obd_live_data": obd_payload,
            "dtc_lab_output": _build_dtc_scenario(row["dtc_scenario"].strip()),
            "symptom_dna": symptom_dna,
        }
    )
    return (request,)


def _entry_point(request: OrchestratorInboundRequest) -> OrchestratorFinalUIOutput:
    """Run the production COMLab aggregation entry point."""
    return LabPipelineAggregator().process(request)


def _extract_expected(row: dict[str, str]) -> dict[str, Any]:
    """Return characterization placeholders; empty values are not asserted."""
    return {column: row.get(column, "") for column in _EXPECTED_COLS}


def _diff(actual: Any, expected: dict[str, Any]) -> list[str]:
    """Compare populated expectations while skipping characterization blanks."""
    if not isinstance(actual, OrchestratorFinalUIOutput):
        return [f"expected OrchestratorFinalUIOutput, got {type(actual).__name__}"]

    observed = {
        "expected_top_fault": actual.diagnostic_verdict.fault_code,
        "expected_fault_family": actual.diagnostic_verdict.fault_family,
        "expected_degradation_mode": actual.execution_meta.degradation_mode,
        "expected_confidence": actual.execution_meta.processing_confidence_rating,
    }
    return [
        f"{column} mismatch: {observed[column]} != {wanted}"
        for column, wanted in expected.items()
        if str(wanted).strip() and observed[column] != wanted
    ]


def build_comlab_descriptor() -> ModuleDescriptor:
    """Build COMLab's categorical harness descriptor.

    COMLab consumes upstream verdict states rather than raw continuous sensor
    geometry, so every field is enumerated and ``boxes`` is intentionally empty.
    """
    chemical_states = sorted(
        {
            str(builder()["chemical_state"])
            for builder in _GAS_SCENARIOS.values()
        }
    )
    fields = [
        FieldRange("metadata_horizon", "str", enum_values=list(get_args(HorizonLit))),
        FieldRange("gas_chemical_state", "str", enum_values=chemical_states),
        FieldRange(
            "gas_sample_validity",
            "str",
            enum_values=[member.value for member in SampleValidity],
        ),
        FieldRange(
            "obd_rpm_state_bucket",
            "str",
            enum_values=[member.value for member in EngineStateBucket],
        ),
        FieldRange(
            "obd_trim_analytics_gate",
            "str",
            enum_values=[member.value for member in TrimAnalyticsGate],
        ),
        FieldRange(
            "obd_o2_failure_mode",
            "str",
            enum_values=[member.value for member in O2FailureMode],
        ),
        FieldRange(
            "obd_ve_validity",
            "str",
            enum_values=[member.value for member in VEValidity],
        ),
        FieldRange(
            "obd_maf_status",
            "str",
            enum_values=[member.value for member in NodeMAFStatus],
        ),
        FieldRange(
            "obd_map_status",
            "str",
            enum_values=[member.value for member in NodeMAPStatus],
        ),
        FieldRange(
            "dtc_routing_tag",
            "str",
            enum_values=[member.value for member in DTCRoutingTag],
        ),
        FieldRange(
            "dtc_historical_context",
            "str",
            enum_values=[member.value for member in HistoricalFaultContext],
        ),
        FieldRange(
            "symptom_engine_state",
            "str",
            enum_values=["neutral", "running", "cranking", "will_not_start"],
        ),
        FieldRange(
            "degradation_mode",
            "str",
            enum_values=list(get_args(DegradationLit)),
        ),
        FieldRange(
            "fault_family",
            "str",
            enum_values=list(get_args(FaultFamilyLit)),
        ),
        FieldRange(
            "confidence",
            "str",
            enum_values=list(get_args(ConfidenceLit)),
        ),
    ]
    return ModuleDescriptor(
        name="COMLab",
        fields=fields,
        boxes={},
        build_args=_build_args,
        entry_point=_entry_point,
        extract_expected=_extract_expected,
        diff=_diff,
    )
