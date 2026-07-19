"""Air metering classification — single deep module replacing two parallel switches.

source: SEMANTIC_CONTRACT.md §8 PrimaryLoadCalculation + AirMeteringStrategy enums
source: architecture_fixes/T-FX-2 (audit candidate #3 — two views of one fact)
"""

from __future__ import annotations

from dataclasses import dataclass

from vinlab.models import AirMeteringStrategy, PrimaryLoadCalculation

__all__ = ["AirMeteringClassification", "classify_air_metering"]


@dataclass(frozen=True)
class AirMeteringClassification:
    """One classification for the (has_maf, has_map) fact.

    Contract §8:
      primary_load_calculation — developer-facing label for VinDNA.air_metering_architecture
      strategy_label          — OBDLab-canonical label for VinDNA.air_metering_strategy
    """

    primary_load_calculation: PrimaryLoadCalculation
    strategy_label: AirMeteringStrategy


def classify_air_metering(has_maf: bool, has_map: bool) -> AirMeteringClassification:
    """Return both air-metering labels from a single classification of (has_maf, has_map).

    Mapping (contract §8):
        both sensors  → HYBRID_MAF_MAP        / DUAL_MAF_MAP_CROSSCHECK
        MAF only      → MAF_ONLY              / MAF_ONLY
        MAP only      → MAP_ONLY              / MAP_ONLY_SPEED_DENSITY
        neither       → MAP_ONLY              / MAP_ONLY_SPEED_DENSITY
    """
    if has_maf and has_map:
        return AirMeteringClassification(
            primary_load_calculation=PrimaryLoadCalculation.HYBRID_MAF_MAP,
            strategy_label=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
        )
    if has_maf:
        return AirMeteringClassification(
            primary_load_calculation=PrimaryLoadCalculation.MAF_ONLY,
            strategy_label=AirMeteringStrategy.MAF_ONLY,
        )
    return AirMeteringClassification(
        primary_load_calculation=PrimaryLoadCalculation.MAP_ONLY,
        strategy_label=AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY,
    )
