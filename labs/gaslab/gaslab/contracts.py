"""GASLab contracts — enums, input dataclass, and output Pydantic model.

Every enum, constant, and field constraint in this module derives from
``GAS_VOCABULARY.md``. Numeric thresholds cite ``GAS_VOCABULARY §10``;
enum values cite their defining vocabulary section.

Petrol-only, 5-gas only, warm-engine-only. No cross-lab imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chemical constants — GAS_VOCABULARY §6
# ---------------------------------------------------------------------------

Hcv: float = 1.85  # vocab: GAS_VOCABULARY §6 — hydrogen-to-carbon atomic ratio for pump petrol
AFR_STOICH: float = 14.71  # vocab: GAS_VOCABULARY §6 — stoichiometric petrol AFR (kg air / kg fuel)
HC_FACTOR: float = 0.0025  # vocab: GAS_VOCABULARY §6 — ppm HC → effective vol% in carbon-balance denominator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class ChemicalSignature(StrEnum):
    """The 34-value canonical fault label emitted by GASLab.

    Mirror of ``OBD_VOCABULARY.md §17``, declared locally so GASLab has no
    cross-lab Python imports.  Source: ``GAS_VOCABULARY §3``.
    """

    NORMAL_OPERATION = "NORMAL_OPERATION"
    RICH_MIXTURE = "RICH_MIXTURE"
    LEAN_MIXTURE = "LEAN_MIXTURE"
    IGNITION_MISFIRE = "IGNITION_MISFIRE"
    LEAN_MISFIRE = "LEAN_MISFIRE"
    RICH_MISFIRE = "RICH_MISFIRE"
    EXHAUST_AIR_LEAK = "EXHAUST_AIR_LEAK"
    HIGH_COMBUSTION_TEMP = "HIGH_COMBUSTION_TEMP"
    CATALYST_NOT_LIGHTING_OFF = "CATALYST_NOT_LIGHTING_OFF"
    CATALYST_OVERWHELMED = "CATALYST_OVERWHELMED"
    SAMPLE_INVALID = "SAMPLE_INVALID"
    TIMING_OVER_ADVANCED = "TIMING_OVER_ADVANCED"
    TIMING_RETARDED = "TIMING_RETARDED"
    O2_SENSOR_BIASED_LOW = "O2_SENSOR_BIASED_LOW"
    O2_SENSOR_BIASED_HIGH = "O2_SENSOR_BIASED_HIGH"
    WORN_ENGINE = "WORN_ENGINE"
    FLAT_CAMSHAFT = "FLAT_CAMSHAFT"
    GDI_INTAKE_VALVE_CARBON = "GDI_INTAKE_VALVE_CARBON"
    VACUUM_REGULATOR_DIAPHRAGM_RUPTURE = "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE"
    GDI_HPFP_INTERNAL_SEAL_LEAK = "GDI_HPFP_INTERNAL_SEAL_LEAK"
    WORN_VALVE_SEALS = "WORN_VALVE_SEALS"
    WORN_PISTON_RINGS = "WORN_PISTON_RINGS"
    POA_SIGNATURE = "POA_SIGNATURE"
    CAM_TIMING_RETARDED_MAP = "CAM_TIMING_RETARDED_MAP"  # vocab: GAS_VOCABULARY §3
    CAM_TIMING_RETARDED_MAF = "CAM_TIMING_RETARDED_MAF"  # vocab: GAS_VOCABULARY §3
    CAM_TIMING_ADVANCED = "CAM_TIMING_ADVANCED"  # vocab: GAS_VOCABULARY §3
    EGR_STUCK_CLOSED = "EGR_STUCK_CLOSED"
    EGR_STUCK_OPEN = "EGR_STUCK_OPEN"
    VVT_FAILURE = "VVT_FAILURE"
    EVAP_CANISTER_SATURATED = "EVAP_CANISTER_SATURATED"
    EGR_DILUTION_MISFIRE = "EGR_DILUTION_MISFIRE"  # vocab: GAS_VOCABULARY §3
    INCOMPLETE_OXIDATION = "INCOMPLETE_OXIDATION"  # vocab: GAS_VOCABULARY §3
    INCOMPLETE_COMBUSTION = "INCOMPLETE_COMBUSTION"  # vocab: GAS_VOCABULARY §3
    COOLANT_LEAK_INTERNAL = "COOLANT_LEAK_INTERNAL"  # vocab: GAS_VOCABULARY §3


class LambdaBand(StrEnum):
    """Discretised lambda regions.  Source: ``GAS_VOCABULARY §4``."""

    HEAVILY_RICH = "HEAVILY_RICH"  # λ < 0.92
    BORDERLINE_RICH = "BORDERLINE_RICH"  # 0.92 ≤ λ < 0.97
    STOICHIOMETRIC = "STOICHIOMETRIC"  # 0.97 ≤ λ < 1.03
    CATALYST_LIGHT_OFF = "CATALYST_LIGHT_OFF"  # 0.98 ≤ λ < 1.02 (sub-band)
    CATALYST_PEAK_EFFICIENCY = "CATALYST_PEAK_EFFICIENCY"  # 0.995 ≤ λ < 1.005 (sub-band)
    BORDERLINE_LEAN = "BORDERLINE_LEAN"  # 1.03 ≤ λ < 1.07
    HEAVILY_LEAN = "HEAVILY_LEAN"  # λ ≥ 1.07


class SampleValidity(StrEnum):
    """Triangle-gate verdict.  Source: ``GAS_VOCABULARY §5``."""

    VALID = "VALID"  # CO+CO2+O2 in [14, 16]
    BORDERLINE = "BORDERLINE"  # in [14, 15] or [15.5, 16]
    INVALID = "INVALID"  # < 14 or > 18 — halts evaluation
    EXTERNAL_O2_SUSPECT = "EXTERNAL_O2_SUSPECT"  # in (16, 18] — warn but continue


class EngineStateBucket(StrEnum):
    """RPM-bucket label consumed by GASLab.  Source: ``GAS_VOCABULARY §7``."""

    STABILIZED_IDLE = "STABILIZED_IDLE"
    REGULATORY_HIGH_IDLE = "REGULATORY_HIGH_IDLE"
    STRESS_IDLE = "STRESS_IDLE"
    COLD_OPEN_LOOP_INVALID = "COLD_OPEN_LOOP_INVALID"


class GasBehavior(StrEnum):
    """Directional pattern language for rule bodies.  Source: ``GAS_VOCABULARY §8``."""

    POSITIVE_SPIKE = "POSITIVE_SPIKE"
    POSITIVE_SHIFT = "POSITIVE_SHIFT"
    NORMAL = "NORMAL"
    SUPPRESSED = "SUPPRESSED"
    INVERSE_CORRELATION = "INVERSE_CORRELATION"
    COLLISION = "COLLISION"


class CatalystStatus(StrEnum):
    """Inferred catalyst health.  Internal-only in v1.  Source: ``GAS_VOCABULARY §9``."""

    LIT_AND_WORKING = "LIT_AND_WORKING"
    NOT_LIT = "NOT_LIT"
    OVERWHELMED = "OVERWHELMED"
    NOT_EVALUABLE = "NOT_EVALUABLE"


# ---------------------------------------------------------------------------
# Input dataclass
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GasReading:
    """Five raw analyser inputs.  All fields required — no 4-gas fallback.

    Source: ``GAS_VOCABULARY §2.1``.
    """

    hc: int  # ppm  (gas_hc)     vocab: GAS_VOCABULARY §2
    co: float  # vol % (gas_co)   vocab: GAS_VOCABULARY §2
    co2: float  # vol % (gas_co2) vocab: GAS_VOCABULARY §2
    o2: float  # vol % (gas_o2)   vocab: GAS_VOCABULARY §2
    nox: int  # ppm  (gas_nox)    vocab: GAS_VOCABULARY §2

    def __post_init__(self) -> None:
        """Reject readings outside analyser measurement envelope.

        Source: ``GAS_VOCABULARY §2`` range column.
        """
        if not (0 <= self.hc <= 20_000):  # vocab: GAS_VOCABULARY §2
            raise ValueError(f"gas_hc out of range: {self.hc}")
        if not (0.0 <= self.co <= 15.0):  # vocab: GAS_VOCABULARY §2
            raise ValueError(f"gas_co out of range: {self.co}")
        if not (0.0 <= self.co2 <= 22.0):  # vocab: GAS_VOCABULARY §2
            raise ValueError(f"gas_co2 out of range: {self.co2}")
        if not (0.0 <= self.o2 <= 22.0):  # vocab: GAS_VOCABULARY §2
            raise ValueError(f"gas_o2 out of range: {self.o2}")
        if not (0 <= self.nox <= 5_000):  # vocab: GAS_VOCABULARY §2
            raise ValueError(f"gas_nox out of range: {self.nox}")


# ---------------------------------------------------------------------------
# Output Pydantic model
# ---------------------------------------------------------------------------


class GasLabPayload(BaseModel):
    """Output fragment GASLab hands to COMLab.  Source: ``GAS_VOCABULARY §12.1``.

    Range bounds match the analyser measurement envelope from
    ``GAS_VOCABULARY §2``.  The Pydantic validator at COMLab will reject
    payloads outside these bounds — GASLab must never emit one.
    """

    chemical_state: ChemicalSignature
    gas_co: float = Field(..., ge=0.0, le=15.0)  # vocab: GAS_VOCABULARY §2
    gas_hc: int = Field(..., ge=0, le=20_000)  # vocab: GAS_VOCABULARY §2
    gas_co2: float = Field(..., ge=0.0, le=22.0)  # vocab: GAS_VOCABULARY §2
    gas_o2: float = Field(..., ge=0.0, le=22.0)  # vocab: GAS_VOCABULARY §2
    gas_nox: int = Field(..., ge=0, le=5_000)  # vocab: GAS_VOCABULARY §2
    lambda_chem: float = Field(..., ge=0.5, le=2.5)  # vocab: GAS_VOCABULARY §6
    sample_validity: SampleValidity
    lambda_measured: float | None = Field(
        default=None, ge=0.5, le=2.0
    )  # vocab: GAS_VOCABULARY §2/§6 — optional directly-measured analyser λ;
       # consumer: COMLab perception-contradiction detector (T-FX-7 no-OBD path)
    high_idle_hc: int | None = Field(
        default=None, ge=0, le=20_000
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_co: float | None = Field(
        default=None, ge=0.0, le=15.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_co2: float | None = Field(
        default=None, ge=0.0, le=22.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_o2: float | None = Field(
        default=None, ge=0.0, le=22.0
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_nox: int | None = Field(
        default=None, ge=0, le=5_000
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
    high_idle_lambda: float | None = Field(
        default=None, ge=0.5, le=2.5
    )  # OilburnCases.md §PCV/turbo; consumer: R3b PID resolver
