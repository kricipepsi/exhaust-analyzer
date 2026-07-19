"""Targeted tests for registry/rules/no_fault.json."""

import json
import pathlib
from typing import Any

from registry.integration_shim import RegistryV2Router
from registry.schema_v2 import EvidenceTier, RuleSet

RULES_DIR = pathlib.Path(__file__).resolve().parent.parent / "rules"
NO_FAULT_FILE = RULES_DIR / "no_fault.json"


def _load_ruleset() -> RuleSet:
    data = json.loads(NO_FAULT_FILE.read_text(encoding="utf-8"))
    return RuleSet.model_validate(data)


def _route(payload: dict[str, Any]) -> tuple[str, str]:
    output, diagnostics = RegistryV2Router().route_case_with_diagnostics(payload)
    family = output["diagnostic_verdict"]["fault_family"]
    return family, str(diagnostics["winner_rule_id"])


def _payload(
    *,
    chemical_state: str,
    hc: float,
    co: float,
    co2: float,
    o2: float,
    nox: float,
    dtcs: list[str] | None = None,
    tags: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "metadata": {"session_id": "00000000-0000-4000-8000-000000000000"},
        "horizon_ctx": "HORIZON_MODERN",
        "degradation_mode": "FULL_FUSION",
        "gas_lab_output": {
            "chemical_state": chemical_state,
            "sample_validity": "VALID",
            "gas_hc": hc,
            "gas_co": co,
            "gas_co2": co2,
            "gas_o2": o2,
            "gas_nox": nox,
        },
        "obd_live_data": {"normalized_obd_lambda": 1.0},
        "dtc_lab_output": {
            "confirmed_dtcs": dtcs or [],
            "routing_tags": tags or [],
            "freeze_frame": {},
        },
    }


def test_file_exists() -> None:
    assert NO_FAULT_FILE.is_file(), f"Missing {NO_FAULT_FILE}"


def test_ruleset_validates() -> None:
    rs = _load_ruleset()
    assert rs.version == "2.0"
    assert rs.fault_family.value == "no_fault"
    assert len(rs.rules) >= 2


def test_every_rule_is_gating_tight() -> None:
    rs = _load_ruleset()
    for rule in rs.rules:
        evidence = [
            *rule.chemistry_evidence,
            *rule.obd_evidence,
            *rule.dtc_evidence,
        ]
        assert evidence, f"{rule.rule_id}: expected evidence rows"
        assert all(ev.tier == EvidenceTier.GATING for ev in evidence), (
            f"{rule.rule_id}: no_fault acceptance rules must be GATING-tight"
        )


def test_clean_no_dtc_payload_routes_to_no_fault() -> None:
    family, winner = _route(
        _payload(
            chemical_state="TIMING_RETARDED",
            hc=12.0,
            co=0.1,
            co2=15.2,
            o2=0.3,
            nox=25.0,
        )
    )
    assert family == "no_fault"
    assert winner == "NF-001"


def test_clean_false_lean_dtc_payload_routes_to_no_fault() -> None:
    family, winner = _route(
        _payload(
            chemical_state="TIMING_RETARDED",
            hc=10.0,
            co=0.01,
            co2=14.8,
            o2=0.3,
            nox=0.0,
            dtcs=["P0171"],
            tags=["LEAN_HISTORY"],
        )
    )
    assert family == "no_fault"
    assert winner == "NF-002"


def test_no_fault_does_not_shadow_lean_condition() -> None:
    family, winner = _route(
        _payload(
            chemical_state="LEAN_MIXTURE",
            hc=45.0,
            co=0.02,
            co2=11.5,
            o2=4.5,
            nox=120.0,
            dtcs=["P0171"],
            tags=["LEAN_HISTORY"],
        )
    )
    assert family == "lean_condition"
    assert winner.startswith("LC-")


def test_no_fault_does_not_shadow_clean_gas_ecu_sensor_fault() -> None:
    family, winner = _route(
        _payload(
            chemical_state="TIMING_RETARDED",
            hc=10.0,
            co=0.1,
            co2=15.2,
            o2=0.2,
            nox=30.0,
            dtcs=["P0113"],
        )
    )
    assert family == "ecu_fault"
    assert winner.startswith("EF-")


def test_no_fault_does_not_shadow_silent_catalyst_decline() -> None:
    family, winner = _route(
        _payload(
            chemical_state="VVT_FAILURE",
            hc=25.0,
            co=0.2,
            co2=15.5,
            o2=0.1,
            nox=250.0,
        )
    )
    assert family == "catalyst_failure"
    assert winner.startswith("CF-")


def test_no_fault_does_not_shadow_rich_mixture() -> None:
    family, winner = _route(
        _payload(
            chemical_state="RICH_MIXTURE",
            hc=150.0,
            co=3.5,
            co2=13.0,
            o2=0.4,
            nox=0.0,
            dtcs=["P0172"],
            tags=["RICH_HISTORY"],
        )
    )
    assert family == "rich_mixture"
    assert winner.startswith("RM-")
