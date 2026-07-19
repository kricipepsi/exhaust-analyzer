"""euro_emission_category -> Horizon enum mapping per SEMANTIC_CONTRACT §6.4."""

from __future__ import annotations

from vinlab.models import EuroEmissionCategory, Horizon

__all__ = ["euro_to_horizon"]


def euro_to_horizon(euro: str | EuroEmissionCategory) -> Horizon:
    """Map EuroEmissionCategory to architecture horizon per contract §6.4.

    EURO_1, EURO_2          -> HORIZON_LEGACY
    EURO_3, EURO_4          -> HORIZON_ADAPTIVE
    EURO_5, EURO_6, EURO_7  -> HORIZON_MODERN
    """
    if isinstance(euro, EuroEmissionCategory):
        euro = euro.value
    if euro in ("EURO_1", "EURO_2"):
        return Horizon.LEGACY
    if euro in ("EURO_3", "EURO_4"):
        return Horizon.ADAPTIVE
    if euro in ("EURO_5", "EURO_6", "EURO_7"):
        return Horizon.MODERN
    raise ValueError(f"Unknown euro_emission_category: {euro!r}")


def _year_to_horizon(year: int) -> Horizon:
    """Map a calendar year to its architecture horizon.

    Used only when euro_emission_category is unknown.
    """
    if 1990 <= year <= 2000:
        return Horizon.LEGACY
    if 2001 <= year <= 2010:
        return Horizon.ADAPTIVE
    return Horizon.MODERN
