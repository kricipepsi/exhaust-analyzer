"""engine class -> stress_idle_rpm_target mapping.

Per OBD_VOCABULARY.md §3.2: the clinically useful high-RPM measurement point
is VIN-dependent. This module derives the per-vehicle target from emission
category, induction type, fuel delivery, displacement, and horizon.
"""

from __future__ import annotations

from vinlab.models import Horizon

__all__ = ["stress_idle_rpm"]

# source: OBD_VOCABULARY.md §3.2 stress_idle_rpm_target table
# source: PATH_FORWARD.md Risk 2 update — peak-stress idle RPM correction
# source: task T-VL-4 build scripts — Euro-era fallback tiers


def stress_idle_rpm(
    euro: str,
    induction: str,
    fuel_delivery: str,
    displacement: float,
    horizon: Horizon,
) -> int:
    """Return the stress-idle RPM target for a given vehicle profile.

    Args:
        euro: EuroEmissionCategory value (EURO_1 .. EURO_7).
        induction: InductionType value.
        fuel_delivery: FuelDeliveryType value.
        displacement: Engine displacement in litres.
        horizon: Resolved Horizon for fallback when euro is unknown.
    """
    # Match table from T-VL-4 build rules + OBD_VOCABULARY.md §3.2
    if euro == "EURO_1" and induction == "NATURALLY_ASPIRATED":
        return 3000  # source: Euro 1 NA baseline — legacy headroom
    if euro in ("EURO_2", "EURO_3") and induction == "NATURALLY_ASPIRATED" and displacement < 2.0:
        return 3500  # source: Euro 2-3 NA small-displacement
    if euro in ("EURO_3", "EURO_4") and induction == "NATURALLY_ASPIRATED" and displacement >= 2.0:
        return 4000  # source: Euro 3-4 NA large-displacement
    if euro in ("EURO_4", "EURO_5") and induction == "TURBOCHARGED":
        return 4000  # source: Euro 4-5 turbo — boost ramps engage
    if euro in ("EURO_5", "EURO_6") and fuel_delivery == "GDI":
        return 4500  # source: Euro 5-6 GDI — HPFP fully loaded

    # Fallback by horizon when euro is absent or unrecognised
    if horizon == Horizon.LEGACY:
        return 3000
    if horizon == Horizon.ADAPTIVE:
        return 3500
    # MODERN or unknown
    return 4000
