"""DTCLab-owned DNA view schema — typed replacement for the loose dict form.

Every class and enum value is sourced verbatim from DTC_VOCABULARY.md §14.
This is a DTCLab-owned mirror of the COMLab/DNALab projection — no cross-lab
imports.  The typed `dna_view: DtcLabDnaView | None` replaces the prior
loose `vin_dna: dict | None` per NewArchProposal_ImplementationPlan.md §4.
"""

from enum import StrEnum

from pydantic import BaseModel


# =============================================================================
# Mirror enums — DTC_VOCABULARY.md §14.1
# =============================================================================


class EuroEmissionCategory(StrEnum):
    """Euro emissions standard tier for the identified vehicle.

    Source: DTC_VOCABULARY.md §14.1.
    """

    EURO_1 = "EURO_1"  # wiki: §14.1
    EURO_2 = "EURO_2"  # wiki: §14.1
    EURO_3 = "EURO_3"  # wiki: §14.1
    EURO_4 = "EURO_4"  # wiki: §14.1
    EURO_5 = "EURO_5"  # wiki: §14.1
    EURO_6 = "EURO_6"  # wiki: §14.1
    EURO_7 = "EURO_7"  # wiki: §14.1
    UNKNOWN = "UNKNOWN"  # wiki: §14.1


class AirMeteringStrategy(StrEnum):
    """Primary air-metering strategy of the identified vehicle.

    Source: DTC_VOCABULARY.md §14.1.
    """

    MAF = "MAF"  # wiki: §14.1 — mass air flow
    MAP_SPEED_DENSITY = "MAP_SPEED_DENSITY"  # wiki: §14.1 — speed-density
    HYBRID = "HYBRID"  # wiki: §14.1 — MAF + MAP blended


class ResolvedHorizon(StrEnum):
    """Vehicle technology horizon resolved from VIN decoding.

    Source: DTC_VOCABULARY.md §14.1.
    """

    HORIZON_LEGACY = "HORIZON_LEGACY"  # wiki: §14.1 — Euro 1–2
    HORIZON_CLASSIC = "HORIZON_CLASSIC"  # wiki: §14.1 — Euro 3–4
    HORIZON_MODERN = "HORIZON_MODERN"  # wiki: §14.1 — Euro 5+


class VinConfidence(StrEnum):
    """Confidence tier of the VIN-to-DNA resolution.

    Source: DTC_VOCABULARY.md §14.1.
    """

    HIGH = "HIGH"  # wiki: §14.1 — all fields resolved from VIN
    PARTIAL = "PARTIAL"  # wiki: §14.1 — some fields defaulted
    NONE = "NONE"  # wiki: §14.1 — no VIN available; pure DTC-pattern routing


# =============================================================================
# Pydantic models — DTC_VOCABULARY.md §14
# =============================================================================


class DtcEmissionsView(BaseModel):
    """Emissions-equipment flags that gate DNA-screened routing tags.

    Source: DTC_VOCABULARY.md §14.
    """


    has_catalyst: bool  # wiki: §14 — gates CATALYST_HISTORY
    egr_equipped: bool  # wiki: §14 — gates EGR_HISTORY


class DtcLabDnaView(BaseModel):
    """Slim VehicleDNA projection consumed by DTCLab.

    Source: DTC_VOCABULARY.md §14.
    Produced by COMLab.project(..., target='dtc').
    """

    make: str
    model: str
    model_year: int
    euro_emission_category: EuroEmissionCategory
    air_metering_strategy: AirMeteringStrategy
    resolved_horizon: ResolvedHorizon
    emissions: DtcEmissionsView
    confidence: VinConfidence
