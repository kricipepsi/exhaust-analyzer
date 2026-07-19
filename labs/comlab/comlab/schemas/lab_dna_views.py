"""Lab DNA projection views — frozen Pydantic models per LLD §5.1.

Each view is a read-only subset of VehicleDNA fields relevant to one
upstream lab.  All models are frozen=True per HLD §6.3 — mutation raises
pydantic.ValidationError.

Consumer: ``comlab.projection.project()`` / ``project_all()`` → held by
``fault_atlas_router`` for the lifetime of one session.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict

from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EuroEmissionCategory,
    FuelDeliveryType,
    Horizon,
    InductionType,
    UpstreamO2Type,
    VinConfidence,
)


class GasLabDnaView(BaseModel):
    """Fields consumed by the Gas Lab per data_flow_report.md §1.  # lld: §5.1"""

    model_config = ConfigDict(frozen=True)  # lld: §5.1

    engine_displacement_liters: float  # lld: §5.1
    cylinder_count: int  # lld: §5.1
    number_of_banks: int  # lld: §5.1
    euro_emission_category: EuroEmissionCategory  # lld: §5.1
    fuel_delivery_type: FuelDeliveryType  # lld: §5.1
    induction_type: InductionType  # lld: §5.1
    upstream_o2_type: UpstreamO2Type  # lld: §5.1
    has_catalyst: bool  # lld: §5.1
    egr_equipped: bool  # lld: §5.1
    target_lambda_v112: Optional[float] = None  # lld: §5.1
    co_low_idle: Optional[float] = None  # lld: §5.1
    co_high_idle: Optional[float] = None  # lld: §5.1
    confidence: VinConfidence  # lld: §5.1
    resolved_horizon: Horizon  # lld: §5.1


class ObdLabDnaView(BaseModel):
    """Fields consumed by the OBD Live Lab per data_flow_report.md §2.  # lld: §5.1"""

    model_config = ConfigDict(frozen=True)  # lld: §5.1

    engine_displacement_liters: Optional[float]  # lld: §5.1
    cylinder_count: Optional[int]  # lld: §5.1
    rated_rpm: Optional[int]  # lld: §5.1
    stress_idle_rpm_target: Optional[int]  # lld: §5.1
    air_metering_strategy: AirMeteringStrategy  # lld: §5.1
    upstream_o2_type: UpstreamO2Type  # lld: §5.1
    induction_type: InductionType  # lld: §5.1
    egr_equipped: bool  # lld: §5.1
    resolved_horizon: Horizon  # lld: §5.1
    confidence: VinConfidence  # lld: §5.1


class DtcLabDnaView(BaseModel):
    """Fields consumed by the DTC Lab per data_flow_report.md §3.  # lld: §5.1"""

    model_config = ConfigDict(frozen=True)  # lld: §5.1

    make: str  # lld: §5.1
    model_year: int  # lld: §5.1
    euro_emission_category: EuroEmissionCategory  # lld: §5.1
    air_metering_strategy: AirMeteringStrategy  # lld: §5.1
    resolved_horizon: Horizon  # lld: §5.1

    has_catalyst: bool  # lld: §5.1
    egr_equipped: bool  # lld: §5.1
    confidence: VinConfidence  # lld: §5.1


class ProjectedViews(BaseModel):
    """All three lab DNA views in one frozen container.  # lld: §5.2"""

    model_config = ConfigDict(frozen=True)  # lld: §5.2
    gas: GasLabDnaView  # lld: §5.2
    obd: ObdLabDnaView  # lld: §5.2
    dtc: DtcLabDnaView  # lld: §5.2
