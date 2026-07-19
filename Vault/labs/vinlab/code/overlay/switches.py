"""Derived field computation for upstream O2 sensor type."""

from __future__ import annotations

from vinlab.models import UpstreamO2Type

__all__ = ["derive_upstream_o2_type"]

# source: OBD_VOCABULARY.md §4.3 upstream O2 sensor type


def derive_upstream_o2_type(year: int, fuel_delivery: str, o2_type_hint: str) -> UpstreamO2Type:
    """Return the upstream O2 sensor type per contract §8 UpstreamO2Type enum.

    Args:
        year: Resolved model year.
        fuel_delivery: FuelDeliveryType value (GDI / PORT_INJECTION / CARBURETOR).
        o2_type_hint: Raw o2_type from vref.db engine_ref (NB / WB / None).

    Returns one of: NARROWBAND | WIDEBAND_AFR | WIDEBAND_LAMBDA | NONE
    """
    if o2_type_hint == "WB":
        return UpstreamO2Type.WIDEBAND_AFR
    if o2_type_hint == "NB":
        # wiki: SEMANTIC_CONTRACT.md §6.3 — explicit vref.db hint wins over year-rule
        return UpstreamO2Type.NARROWBAND
    if year >= 2001 and fuel_delivery in {"GDI", "PORT_INJECTION"}:
        # source: OBD_VOCABULARY.md §4.3 — wideband became standard ~2001 for fuel-injected petrol
        return UpstreamO2Type.WIDEBAND_AFR
    if fuel_delivery == "CARBURETOR":
        return UpstreamO2Type.NARROWBAND
    return UpstreamO2Type.NARROWBAND
