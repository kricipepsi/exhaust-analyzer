"""T-AUD-4p (F-C4-5): no COMLab mirror field ships without a reader.

high_idle_co2/o2/nox and maf_status/map_status had no reader on any path; they are no
longer mirrored. The ten v1-only OBD fields stay, labelled v1-only.
"""

from __future__ import annotations

from pathlib import Path

from comlab.schemas.ingestion import GasLabPayload, OBDLiveDataPayload

from wired import composition

DROPPED_GAS = ("high_idle_co2", "high_idle_o2", "high_idle_nox")
DROPPED_OBD = ("maf_status", "map_status")
V1_ONLY = (
    "total_trim_correction_delta_b2",
    "per_cylinder_misfire_counts",
    "ltft_cell_vector",
    "w_theo",
    "sensor_error_delta",
    "manifold_vacuum_kpa",
    "ve_pct",
    "ve_validity",
    "fuel_system_status",
    "o2_failure_mode",
)


def test_gas_mirror_drops_unread_high_idle_fields() -> None:
    assert not set(DROPPED_GAS) & set(GasLabPayload.model_fields)
    # the read high-idle fields stay (registry shim _PID_DISPATCH -> MW-008/009)
    assert {"high_idle_hc", "high_idle_co", "high_idle_lambda"} <= set(GasLabPayload.model_fields)


def test_obd_mirror_drops_unread_provenance_fields() -> None:
    assert not set(DROPPED_OBD) & set(OBDLiveDataPayload.model_fields)


def test_v1_only_fields_stay_and_docstring_says_so() -> None:
    assert set(V1_ONLY) <= set(OBDLiveDataPayload.model_fields)
    doc = OBDLiveDataPayload.__doc__ or ""
    assert "Every field has a named consumer" not in doc
    assert "v1 loop only" in doc
    for name in V1_ONLY:
        assert name in doc, name


def test_composition_claims_no_dropped_field() -> None:
    src = Path(composition.__file__).read_text(encoding="utf-8")
    for name in DROPPED_GAS + DROPPED_OBD:
        assert f"{name}=" not in src, name
    assert "MW-008/MW-009 high-idle CO2" not in src
