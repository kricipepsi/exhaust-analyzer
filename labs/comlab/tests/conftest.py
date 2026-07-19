"""Shared pytest configuration + fixtures for ComLab tests.

Exposes the mock payload builders as pytest fixtures so tests can ask for
``gas_payload``, ``obd_payload``, ``dtc_payload`` etc. without importing the
fixtures module by hand.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from tests.fixtures import mock_gas_lab, mock_obd_lab, mock_dtc_lab


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def registry_path(repo_root: Path) -> Path:
    return repo_root / "comlab" / "config" / "global_fault_registry.json"


@pytest.fixture(scope="session")
def era_masks_path(repo_root: Path) -> Path:
    return repo_root / "comlab" / "config" / "eras_sensitivity_masks.yaml"


# ---------------------------------------------------------------------------
# Sample payloads
# ---------------------------------------------------------------------------


@pytest.fixture
def session_id():
    return str(uuid4())


@pytest.fixture
def modern_vin() -> str:
    """Example Euro 5/6 VIN used in the BP test harness."""
    return "1FA6P8CF0HXXXXXXX"


@pytest.fixture
def hpfp_leak_payload(session_id, modern_vin) -> dict:
    """Full ingestion payload for the GDI HPFP seal leak scenario.

    This is the canonical positive-test payload — Script 3 must resolve it to
    ``fault_name == "gdi_hpfp_internal_seal_leak"``.
    """
    return {
        "metadata": {
            "session_id": session_id,
            "vin_dna_string": modern_vin,
            "resolved_horizon": "HORIZON_MODERN",
            "cylinder_count": 4,
        },
        "gas_lab_output": mock_gas_lab.rich_unmetered_intrusion(),
        "obd_live_data": mock_obd_lab.hpfp_leak_signature(),
        "dtc_lab_output": mock_dtc_lab.fuel_system_rich("P0172"),
    }
