"""Script 1: Horizon Context Injector — the context gate.

Runs first on every diagnostic session. Reads pre-computed vehicle metadata
from VehicleDNA (resolved by DNALab), maps the architecture horizon, and emits
a sensitivity threshold mask that downstream labs use to tune their pass/fail
bounds.

COMLab does NOT parse the VIN or compute the horizon — both are pre-supplied
by DNALab per NewArchPlan §2.

Source: COMLab_LLD.md §6.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from comlab.schemas.ingestion import VehicleDNA
from comlab.schemas.vocabulary import EuroEmissionCategory, Horizon

__all__ = ["HorizonContext", "HorizonContextInjector"]


@dataclass(frozen=True)
class HorizonContext:
    """Final output of Stage A horizon resolution.

    Source: lld: §6.1.
    """

    resolved_horizon: Horizon  # lld: §6.1
    cylinder_count: int  # lld: §6.1
    number_of_banks: int  # lld: §6.1
    threshold_mask: dict[str, Any]  # lld: §6.1 — from eras_sensitivity_masks.yaml


class HorizonContextInjector:
    """Reads VehicleDNA, returns HorizonContext.

    Does NOT parse the VIN. Does NOT compute the horizon. Both are
    pre-supplied by DNALab. The injector's job collapsed to:
      1. read vehicle_dna.vin_dna.resolved_horizon (or derive from
         euro_emission_category if a v1.0 DNALab payload omits it)
      2. read vehicle_dna.vin_dna.cylinder_count and number_of_banks
      3. load the era-sensitivity threshold mask from yaml

    Source: lld: §6.1.
    """

    def __init__(self, masks_yaml_path: str | Path) -> None:
        """Load eras_sensitivity_masks.yaml once. Cached for process lifetime.

        Source: lld: §6.1.
        """
        self._masks_yaml_path = Path(masks_yaml_path)
        self._masks: dict[str, Any] | None = None
        self._default_mask: dict[str, Any] = {}  # T-FX-PURGE-1: cached default

    def _load_masks(self) -> dict[str, Any]:
        if self._masks is None:
            with self._masks_yaml_path.open("r", encoding="utf-8") as fh:
                self._masks = yaml.safe_load(fh)
        assert self._masks is not None  # guaranteed after load
        return self._masks

    def from_vehicle_dna(self, vehicle_dna: VehicleDNA) -> HorizonContext:
        """The only public method. Pure function over a parsed DNA.

        Source: lld: §6.1.
        """
        vin_dna = vehicle_dna.vin_dna

        resolved_horizon = vin_dna.resolved_horizon
        cylinder_count = vin_dna.cylinder_count
        number_of_banks = vin_dna.number_of_banks

        masks = self._load_masks()
        # WHY: MODERN (MY≥2010) uses default lab settings; no era-specific
        # thresholds are applied, matching the undecodable-VIN empty-mask path.
        # T-FX-PURGE-1.
        if resolved_horizon == Horizon.MODERN:
            threshold_mask = self._default_mask
        else:
            horizon_key = resolved_horizon.value  # lld: §6.1
            threshold_mask = masks.get("horizons", {}).get(horizon_key, {})

        return HorizonContext(
            resolved_horizon=resolved_horizon,
            cylinder_count=cylinder_count,
            number_of_banks=number_of_banks,
            threshold_mask=threshold_mask,
        )

    @staticmethod
    def _horizon_from_euro(category: EuroEmissionCategory) -> Horizon:
        """Derive horizon from euro_emission_category when DNALab ships a
        payload without resolved_horizon (v1.0 back-compat).

        Mapping per SEMANTIC_CONTRACT §6.4:
          EURO_1, EURO_2  → HORIZON_LEGACY    (wiki: OBD_VOCABULARY §7)
          EURO_3, EURO_4  → HORIZON_ADAPTIVE  (wiki: OBD_VOCABULARY §7)
          EURO_5, EURO_6, EURO_7 → HORIZON_MODERN  (wiki: OBD_VOCABULARY §7)

        Source: lld: §6.1.
        """
        if category in (EuroEmissionCategory.EURO_1, EuroEmissionCategory.EURO_2):
            return Horizon.LEGACY
        if category in (EuroEmissionCategory.EURO_3, EuroEmissionCategory.EURO_4):
            return Horizon.ADAPTIVE
        return Horizon.MODERN
