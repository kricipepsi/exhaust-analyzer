"""VinDNA dataclass and enum vocabulary.

The VinDNA is the sole output of vinlab.decode(). Its schema is governed by
SEMANTIC_CONTRACT.md §4.1 — that contract wins over all other documents.

Enums are defined locally with exact contract §8 strings. Enum-typed fields
replaced bare str annotations per ADR 0004 (T-FX-5). The future cut-over to
comlab/schemas/vocabulary.py is a one-line import swap when Phase 0b ships.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum, StrEnum
from typing import Any

__all__ = [
    "AirMeteringArchitecture",
    "AirMeteringStrategy",
    "DownstreamTrimRole",
    "Emissions",
    "EuroEmissionCategory",
    "FuelDeliveryType",
    "Horizon",
    "InductionType",
    "PrimaryLoadCalculation",
    "UpstreamO2Type",
    "VinConfidence",
    "VinDNA",
]

# ===========================================================================
# Enums — contract §8 locked vocabulary
# (future: import from comlab.schemas.vocabulary when Phase 0b ships)
# ===========================================================================


class Horizon(StrEnum):
    """Architecture horizon derived from euro_emission_category per contract §6.4."""

    LEGACY = "HORIZON_LEGACY"
    ADAPTIVE = "HORIZON_ADAPTIVE"
    MODERN = "HORIZON_MODERN"


class EuroEmissionCategory(StrEnum):
    """Emission standard per contract §4.1."""

    EURO_1 = "EURO_1"
    EURO_2 = "EURO_2"
    EURO_3 = "EURO_3"
    EURO_4 = "EURO_4"
    EURO_5 = "EURO_5"
    EURO_6 = "EURO_6"
    EURO_7 = "EURO_7"


class InductionType(StrEnum):
    """Mechanical induction classifier per contract §6.1."""

    NATURALLY_ASPIRATED = "NATURALLY_ASPIRATED"
    TURBOCHARGED = "TURBOCHARGED"
    SUPERCHARGED = "SUPERCHARGED"


class AirMeteringStrategy(StrEnum):
    """OBDLab-canonical air metering strategy per contract §6.2."""

    DUAL_MAF_MAP_CROSSCHECK = "DUAL_MAF_MAP_CROSSCHECK"
    MAP_ONLY_SPEED_DENSITY = "MAP_ONLY_SPEED_DENSITY"
    MAF_ONLY = "MAF_ONLY"


class PrimaryLoadCalculation(StrEnum):
    """Developer-friendly load calculation label per contract §6.2."""

    HYBRID_MAF_MAP = "HYBRID_MAF_MAP"
    MAP_ONLY = "MAP_ONLY"
    MAF_ONLY = "MAF_ONLY"


class FuelDeliveryType(StrEnum):
    """Fuel delivery method per contract §8."""

    GDI = "GDI"
    PORT_INJECTION = "PORT_INJECTION"
    CARBURETOR = "CARBURETOR"


class UpstreamO2Type(StrEnum):
    """Pre-cat O2 sensor type per contract §6.3.

    WIDEBAND_NB_SIM: aftermarket WB controller in NB simulation mode.
    Sensor outputs 0–1 V simulated NB signal to ECU; physically a wideband
    sensor. ECU uses binary NB trim strategy. OBDLab reads
    pid_oxygen_sensor_volts.
    """

    NARROWBAND = "NARROWBAND"
    WIDEBAND_AFR = "WIDEBAND_AFR"
    WIDEBAND_LAMBDA = "WIDEBAND_LAMBDA"
    WIDEBAND_NB_SIM = "WIDEBAND_NB_SIM"
    NONE = "NONE"


class VinConfidence(StrEnum):
    """Decode confidence per contract §8."""

    HIGH = "HIGH"
    PARTIAL = "PARTIAL"
    NONE = "NONE"


class DownstreamTrimRole(StrEnum):
    """Role of the downstream O2 sensor in the ECU's closed-loop strategy.

    VINLab is the owning lab for this type; COMLab mirrors it via JSON-only
    boundary.  Source: O2_MODEL_STRATEGY.md §3; Osensorguide.md §2.
    """

    # wiki: O2_MODEL_STRATEGY.md §3
    NONE = "NONE"
    CATALYST_MONITOR_ONLY = "CATALYST_MONITOR_ONLY"
    SECONDARY_FUEL_TRIM = "SECONDARY_FUEL_TRIM"


def _derive_horizon_from_euro(euro: EuroEmissionCategory) -> Horizon:
    """Back-compat: derive Horizon from euro_emission_category per contract §6.4.

    Used only when deserializing a legacy payload that lacks resolved_horizon.
    """
    euro_str = euro.value if isinstance(euro, EuroEmissionCategory) else str(euro)
    if euro_str in ("EURO_1", "EURO_2"):
        return Horizon.LEGACY
    if euro_str in ("EURO_3", "EURO_4"):
        return Horizon.ADAPTIVE
    if euro_str in ("EURO_5", "EURO_6", "EURO_7"):
        return Horizon.MODERN
    return Horizon.MODERN


# ===========================================================================
# Nested dataclasses
# ===========================================================================


@dataclass(frozen=True)
class AirMeteringArchitecture:
    """Air metering sensor inventory and derived strategy.

    Contract §6.2: VinDNA ships both has_maf/has_map booleans AND
    primary_load_calculation. The top-level air_metering_strategy field
    mirrors this with OBDLab-canonical naming.
    """

    has_maf_sensor: bool = False
    has_map_sensor: bool = False
    primary_load_calculation: PrimaryLoadCalculation = PrimaryLoadCalculation.MAP_ONLY


@dataclass(frozen=True)
class Emissions:
    """Emissions control equipment inventory per contract §4.1."""

    upstream_o2_type: UpstreamO2Type = UpstreamO2Type.NARROWBAND
    downstream_o2_present: bool = False
    # wiki: O2_MODEL_STRATEGY.md §3
    downstream_trim_role: DownstreamTrimRole = DownstreamTrimRole.NONE
    # wiki: O2_MODEL_STRATEGY.md §9.1
    has_catalyst: bool = True
    egr_equipped: bool = False


# ===========================================================================
# VinDNA — the single public output dataclass
# ===========================================================================


@dataclass(frozen=True)
class VinDNA:
    """Decoded vehicle profile produced by vinlab.decode().

    Schema governed by SEMANTIC_CONTRACT.md §4.1. Includes contract-required
    fields plus CoC empirical targets sourced from petrol CSV medians.
    """

    # -- Required: caller-supplied -----------------------------------------
    vin: str = ""

    # -- Basic attributes (contract §4.1) ----------------------------------
    make: str = ""
    model_year: int | None = None
    engine_displacement_liters: float = 0.0
    cylinder_count: int = 0
    number_of_banks: int = 1

    # -- Aspiration + fuel (contract §4.1, §6.1) --------------------------
    induction_type: InductionType = InductionType.NATURALLY_ASPIRATED
    fuel_delivery_type: FuelDeliveryType = FuelDeliveryType.PORT_INJECTION

    # -- Air metering architecture (contract §4.1, §6.2) -------------------
    air_metering_architecture: AirMeteringArchitecture = field(
        default_factory=AirMeteringArchitecture
    )

    # -- Emissions equipment (contract §4.1) -------------------------------
    emissions: Emissions = field(default_factory=Emissions)

    # -- Era classification (contract §4.1, §6.4) -------------------------
    euro_emission_category: EuroEmissionCategory = EuroEmissionCategory.EURO_1
    resolved_horizon: Horizon = Horizon.MODERN  # lld: §6.4 — DNALab-computed

    # -- Clinical RPM target (contract §4.1, §6.5) -------------------------
    # source: OBD_VOCABULARY §3.2 — Euro 1 NA 1.0L baseline
    stress_idle_rpm_target: int = 3000
    # source: DBS/docs/vehicles_petrol_specimens.csv P14_rated_rpm
    rated_rpm: int | None = None

    # -- Decode confidence (contract §4.1) ---------------------------------
    confidence: VinConfidence = VinConfidence.NONE

    # -- Top-level air metering strategy (contract §6.2, Open Action #3) ---
    air_metering_strategy: AirMeteringStrategy = (
        AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY
    )

    # -- CoC empirical targets (from petrol CSV medians per engine_code) ---
    target_lambda_v112: float | None = None
    target_rpm_u2: int | None = None
    idle_rpm_low: int | None = None
    co_low_idle: float | None = None
    co_high_idle: float | None = None
    co_type_approval: float | None = None
    hc_type_approval: float | None = None
    nox_type_approval: float | None = None
    hc_nox_type_approval: float | None = None
    co2_type_approval: float | None = None
    noise_stationary_dba: float | None = None
    noise_rpm: int | None = None
    noise_driving_dba: float | None = None

    def to_json_payload(self) -> dict[str, Any]:
        """Serialize to a JSON-safe dict matching SEMANTIC_CONTRACT.md §4.1.

        Uses dataclasses.asdict() for structural walk; enum values are
        coerced to their .value form so T-FX-5 is a no-op here.
        """
        raw = asdict(self)
        return _coerce_enum_values(raw)

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_json_payload())

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> VinDNA:
        """Deserialize from the dict shape in SEMANTIC_CONTRACT.md §4.1.

        Required fields raise KeyError when missing; optional CoC fields
        preserve None defaults.
        """
        ama = payload["air_metering_architecture"]
        em = payload["emissions"]
        return cls(
            vin=payload["vin"],
            make=payload["make"],
            model_year=payload["model_year"],
            engine_displacement_liters=payload["engine_displacement_liters"],
            cylinder_count=payload["cylinder_count"],
            number_of_banks=payload["number_of_banks"],
            induction_type=InductionType(payload["induction_type"]),
            fuel_delivery_type=FuelDeliveryType(payload["fuel_delivery_type"]),
            air_metering_architecture=AirMeteringArchitecture(
                has_maf_sensor=ama.get("has_maf_sensor", False),
                has_map_sensor=ama.get("has_map_sensor", False),
                primary_load_calculation=PrimaryLoadCalculation(
                    ama.get("primary_load_calculation", "MAP_ONLY")
                ),
            ),
            emissions=Emissions(
                upstream_o2_type=UpstreamO2Type(
                    em.get("upstream_o2_type", "NARROWBAND")
                ),
                downstream_o2_present=em.get("downstream_o2_present", False),
                downstream_trim_role=DownstreamTrimRole(
                    em.get("downstream_trim_role", "NONE")
                ),
                has_catalyst=em.get("has_catalyst", True),
                egr_equipped=em.get("egr_equipped", False),
            ),
            euro_emission_category=EuroEmissionCategory(payload["euro_emission_category"]),
            resolved_horizon=(
                Horizon(payload["resolved_horizon"])
                if "resolved_horizon" in payload
                else _derive_horizon_from_euro(EuroEmissionCategory(payload["euro_emission_category"]))
            ),
            stress_idle_rpm_target=payload["stress_idle_rpm_target"],
            rated_rpm=payload.get("rated_rpm"),
            air_metering_strategy=AirMeteringStrategy(payload["air_metering_strategy"]),
            confidence=VinConfidence(payload["confidence"]),
            target_lambda_v112=payload.get("target_lambda_v112"),
            target_rpm_u2=payload.get("target_rpm_u2"),
            idle_rpm_low=payload.get("idle_rpm_low"),
            co_low_idle=payload.get("co_low_idle"),
            co_high_idle=payload.get("co_high_idle"),
            co_type_approval=payload.get("co_type_approval"),
            hc_type_approval=payload.get("hc_type_approval"),
            nox_type_approval=payload.get("nox_type_approval"),
            hc_nox_type_approval=payload.get("hc_nox_type_approval"),
            co2_type_approval=payload.get("co2_type_approval"),
            noise_stationary_dba=payload.get("noise_stationary_dba"),
            noise_rpm=payload.get("noise_rpm"),
            noise_driving_dba=payload.get("noise_driving_dba"),
        )


def _coerce_enum_values(obj: Any) -> Any:
    """Recursively convert Enum members to their .value form."""
    if isinstance(obj, dict):
        return {k: _coerce_enum_values(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_coerce_enum_values(v) for v in obj]
    if isinstance(obj, Enum):
        return obj.value
    return obj
