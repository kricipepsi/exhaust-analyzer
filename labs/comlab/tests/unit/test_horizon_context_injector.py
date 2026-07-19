"""Unit tests for HorizonContextInjector — v1 rewritten interface.

Covers: from_vehicle_dna(), _horizon_from_euro(), mask loading,
HorizonContext frozen contract, and VIN-parsing removal.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from comlab.core.horizon_context_injector import (
    HorizonContext,
    HorizonContextInjector,
)
from comlab.schemas.vocabulary import EuroEmissionCategory, Horizon


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_vin_dna_stub(*, resolved_horizon=Horizon.MODERN, cylinder_count=4,
                        number_of_banks=1, euro_emission_category=EuroEmissionCategory.EURO_6):
    """Build a minimal VinDNA stub with only the fields the injector reads."""
    vin_dna = MagicMock()
    vin_dna.resolved_horizon = resolved_horizon
    vin_dna.cylinder_count = cylinder_count
    vin_dna.number_of_banks = number_of_banks
    vin_dna.euro_emission_category = euro_emission_category
    return vin_dna


def _make_vehicle_dna_stub(vin_dna=None):
    """Build a minimal VehicleDNA stub."""
    vehicle_dna = MagicMock()
    vehicle_dna.vin_dna = vin_dna or _make_vin_dna_stub()
    return vehicle_dna


_MASKS_YAML = """
version: "0.1.0"
horizons:
  HORIZON_LEGACY:
    routing_rigor: LOW_PERMISSIVE
  HORIZON_ADAPTIVE:
    routing_rigor: MEDIUM
  HORIZON_MODERN:
    routing_rigor: STRICT_HIGH
"""


@pytest.fixture
def masks_yaml_path():
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(_MASKS_YAML)
    yield f.name
    Path(f.name).unlink()


# ---------------------------------------------------------------------------
# _horizon_from_euro mapping
# ---------------------------------------------------------------------------

class TestHorizonFromEuro:
    def test_euro_1_maps_to_legacy(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_1) == Horizon.LEGACY

    def test_euro_2_maps_to_legacy(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_2) == Horizon.LEGACY

    def test_euro_3_maps_to_adaptive(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_3) == Horizon.ADAPTIVE

    def test_euro_4_maps_to_adaptive(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_4) == Horizon.ADAPTIVE

    def test_euro_5_maps_to_modern(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_5) == Horizon.MODERN

    def test_euro_6_maps_to_modern(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_6) == Horizon.MODERN

    def test_euro_7_maps_to_modern(self):
        assert HorizonContextInjector._horizon_from_euro(EuroEmissionCategory.EURO_7) == Horizon.MODERN


# ---------------------------------------------------------------------------
# from_vehicle_dna
# ---------------------------------------------------------------------------

class TestFromVehicleDNA:
    def test_reads_resolved_horizon_from_vin_dna(self, masks_yaml_path):
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(resolved_horizon=Horizon.ADAPTIVE)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.resolved_horizon == Horizon.ADAPTIVE

    def test_reads_cylinder_count(self, masks_yaml_path):
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(cylinder_count=8)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.cylinder_count == 8

    def test_reads_number_of_banks(self, masks_yaml_path):
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(number_of_banks=2)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.number_of_banks == 2

    def test_modern_returns_default_empty_mask(self, masks_yaml_path):
        """T-FX-PURGE-1: MODERN (MY≥2010) → default lab settings (empty mask)."""
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(resolved_horizon=Horizon.MODERN)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.threshold_mask == {}

    def test_legacy_still_loads_era_mask(self, masks_yaml_path):
        """T-FX-PURGE-1: in-scope parity — LEGACY unchanged."""
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(resolved_horizon=Horizon.LEGACY)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.threshold_mask["routing_rigor"] == "LOW_PERMISSIVE"

    def test_adaptive_still_loads_era_mask(self, masks_yaml_path):
        """T-FX-PURGE-1: in-scope parity — ADAPTIVE unchanged."""
        injector = HorizonContextInjector(masks_yaml_path)
        vin_dna = _make_vin_dna_stub(resolved_horizon=Horizon.ADAPTIVE)
        vehicle_dna = _make_vehicle_dna_stub(vin_dna=vin_dna)

        ctx = injector.from_vehicle_dna(vehicle_dna)

        assert ctx.threshold_mask["routing_rigor"] == "MEDIUM"

    def test_mask_is_cached(self, masks_yaml_path):
        injector = HorizonContextInjector(masks_yaml_path)
        vehicle_dna = _make_vehicle_dna_stub()

        ctx1 = injector.from_vehicle_dna(vehicle_dna)
        ctx2 = injector.from_vehicle_dna(vehicle_dna)

        assert ctx1.threshold_mask is ctx2.threshold_mask


# ---------------------------------------------------------------------------
# HorizonContext frozen
# ---------------------------------------------------------------------------

class TestHorizonContext:
    def test_frozen(self):
        ctx = HorizonContext(
            resolved_horizon=Horizon.MODERN,
            cylinder_count=6,
            number_of_banks=1,
            threshold_mask={"routing_rigor": "STRICT_HIGH"},
        )
        with pytest.raises(Exception):
            ctx.cylinder_count = 4  # type: ignore[misc]

    def test_fields(self):
        ctx = HorizonContext(
            resolved_horizon=Horizon.LEGACY,
            cylinder_count=4,
            number_of_banks=1,
            threshold_mask={},
        )
        assert ctx.resolved_horizon == Horizon.LEGACY
        assert ctx.cylinder_count == 4
        assert ctx.number_of_banks == 1
        assert ctx.threshold_mask == {}


# ---------------------------------------------------------------------------
# VIN parsing removed
# ---------------------------------------------------------------------------

class TestVinParsingRemoved:
    def test_parse_vin_dna_not_present(self):
        assert not hasattr(HorizonContextInjector, "parse_vin_dna")

    def test_resolve_horizon_vin_not_present(self):
        assert not hasattr(HorizonContextInjector, "resolve_horizon")

    def test_vin_regex_not_present(self):
        assert not hasattr(HorizonContextInjector, "_VIN_REGEX")

    def test_vin_metadata_not_importable(self):
        import comlab.core.horizon_context_injector as hci
        assert "VinMetadata" not in dir(hci)


# ---------------------------------------------------------------------------
# T-FX-PURGE-5 — live era config assertions
# ---------------------------------------------------------------------------

class TestModernEraConfigPURGE5:
    """T-FX-PURGE-5: era config guards — MODERN rule_pack absent,
    MODERN-only activate_nodes stripped, in-scope parity confirmed."""

    def test_modern_has_no_rule_pack_key(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        modern = config["horizons"]["HORIZON_MODERN"]
        assert "rule_pack" not in modern, (
            "MODERN rule_pack must be absent — re-adding it re-enables "
            "PURGE-2-deactivated MODERN-only scoring rules"
        )

    def test_modern_activate_nodes_excludes_stripped_nodes(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        modern_activate = config["horizons"]["HORIZON_MODERN"].get("activate_nodes", [])
        assert "gdi_hpfp_seal_integrity" not in modern_activate
        assert "ecu_perception_logic_inversion" not in modern_activate

    def test_modern_activate_nodes_is_catalyst_only(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        assert config["horizons"]["HORIZON_MODERN"]["activate_nodes"] == [
            "catalyst_oxygen_storage_capacity"
        ]

    def test_legacy_has_rule_pack(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        assert config["horizons"]["HORIZON_LEGACY"]["rule_pack"] == "era_1_mechanical_rules"

    def test_adaptive_has_rule_pack(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        assert config["horizons"]["HORIZON_ADAPTIVE"]["rule_pack"] == "era_2_electronic_overdrive_rules"

    def test_legacy_deactivates_gdi_hpfp_node(self, era_masks_path):
        import yaml
        with open(era_masks_path) as f:
            config = yaml.safe_load(f)
        assert "gdi_hpfp_seal_integrity" in config["horizons"]["HORIZON_LEGACY"]["deactivate_nodes"]
