"""T-AUD-4l — COMLab accepts the binding inbound contract: vehicle_dna at the top level (F-D2-2)."""

from __future__ import annotations

import copy
import uuid
from typing import Any

import pytest
from pydantic import ValidationError

from comlab.schemas.ingestion import OrchestratorInboundRequest

SID = str(uuid.UUID("12345678-1234-4123-8123-123456789abc"))
VIN_DNA: dict[str, Any] = {
    "vin": "WVWZZZ1JZXW000001", "make": "VW", "model": "Golf", "model_year": 1999,
    "engine_displacement_liters": 1.6, "cylinder_count": 4, "number_of_banks": 1,
    "induction_type": "NATURALLY_ASPIRATED", "fuel_delivery_type": "PORT_INJECTION",
    "air_metering_architecture": {"has_maf_sensor": True, "has_map_sensor": False,
                                  "primary_load_calculation": "MAF_ONLY"},
    "air_metering_strategy": "MAF_ONLY",
    "emissions": {"upstream_o2_type": "NARROWBAND", "downstream_o2_present": True, "egr_equipped": True},
    "euro_emission_category": "EURO_3", "stress_idle_rpm_target": 3000,
    "confidence": "HIGH", "resolved_horizon": "HORIZON_ADAPTIVE",
}
GAS: dict[str, Any] = {"chemical_state": "NORMAL", "sample_validity": "VALID"}


def _vehicle_dna(**over: Any) -> dict[str, Any]:
    vd = {"session_id": SID, "timestamp": "2026-10-17T10:00:00Z", "schema_version": "1.0",
          "vin_dna": copy.deepcopy(VIN_DNA)}
    vd.update(over)
    return vd


def _gas() -> Any:
    from comlab.schemas.ingestion import GasLabPayload  # the minimal valid fragment comes from the model's own fields
    return GasLabPayload.model_construct(**GAS)


def test_vehicle_dna_shape_derives_metadata() -> None:
    req = OrchestratorInboundRequest.model_validate({"vehicle_dna": _vehicle_dna(), "gas_lab_output": _gas()})
    m = req.metadata
    assert (str(m.session_id), m.vin_dna_string, m.resolved_horizon, m.cylinder_count) == (
        SID, "WVWZZZ1JZXW000001", "HORIZON_ADAPTIVE", 4)
    assert str(m.air_metering_strategy.value) == "MAF_ONLY"
    assert str(m.vin_confidence.value) == "HIGH" and m.schema_version == "1.0"
    assert req.vehicle_dna is not None and req.vehicle_dna.vin_dna.vin == m.vin_dna_string


def test_both_shapes_are_refused() -> None:
    meta = {"session_id": SID, "vin_dna_string": "WVWZZZ1JZXW000001", "resolved_horizon": "HORIZON_ADAPTIVE",
            "cylinder_count": 4}
    with pytest.raises(ValidationError, match="not both"):
        OrchestratorInboundRequest.model_validate(
            {"vehicle_dna": _vehicle_dna(), "metadata": meta, "gas_lab_output": _gas()})


def test_symptom_and_catalyst_come_from_vehicle_dna() -> None:
    vd = _vehicle_dna(symptom_dna={"tier_1_primary_symptom": "x"})
    vd["vin_dna"]["emissions"]["has_catalyst"] = False
    req = OrchestratorInboundRequest.model_validate({"vehicle_dna": vd, "gas_lab_output": _gas()})
    assert req.symptom_dna == {"tier_1_primary_symptom": "x"}
    assert req.has_catalyst is False


def test_top_level_values_win() -> None:
    vd = _vehicle_dna(symptom_dna={"tier_1_primary_symptom": "x"})
    req = OrchestratorInboundRequest.model_validate(
        {"vehicle_dna": vd, "gas_lab_output": _gas(), "symptom_dna": {"tier_1_primary_symptom": "y"},
         "has_catalyst": False})
    assert req.symptom_dna == {"tier_1_primary_symptom": "y"}
    assert req.has_catalyst is False
