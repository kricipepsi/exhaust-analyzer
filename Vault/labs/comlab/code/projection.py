"""Pure dict-to-Pydantic projection functions per LLD §5.2.

No I/O, no cross-lab imports.  The input is a plain dict (the JSON payload
from DNALab), not a typed object, to avoid importing the DNALab Pydantic model.
"""

from __future__ import annotations

from typing import Any, Literal, cast

from comlab.schemas.lab_dna_views import (
    DtcLabDnaView,
    GasLabDnaView,
    ObdLabDnaView,
    ProjectedViews,
)
from comlab.schemas.vocabulary import EuroEmissionCategory, Horizon, VinConfidence

VehicleDnaJson = dict[str, Any]


def _horizon_from_euro(euro: EuroEmissionCategory | str | None) -> Horizon:
    """Derive resolved_horizon from euro_emission_category.

    Mapping per COMLab_Horizon_Eras.md:
      EURO_1, EURO_2 → HORIZON_LEGACY    (pre-1997 to ~2001)
      EURO_3, EURO_4 → HORIZON_ADAPTIVE  (~2001–2011)
      EURO_5, EURO_6, EURO_7 → HORIZON_MODERN (~2011–present, future)

    Used as a fallback when resolved_horizon is absent from older payloads.
    """
    # lld: §5.2 — horizon fallback per wiki: COMLab_Horizon_Eras.md
    legacy = {EuroEmissionCategory.EURO_1, EuroEmissionCategory.EURO_2}
    adaptive = {EuroEmissionCategory.EURO_3, EuroEmissionCategory.EURO_4}
    if euro in legacy:
        return Horizon.LEGACY  # wiki: COMLab_Horizon_Eras.md §HORIZON_LEGACY
    if euro in adaptive:
        return Horizon.ADAPTIVE  # wiki: COMLab_Horizon_Eras.md §HORIZON_ADAPTIVE
    return Horizon.MODERN  # wiki: COMLab_Horizon_Eras.md §HORIZON_MODERN


def project(
    vehicle_dna_json: VehicleDnaJson,
    *,
    target: Literal["gas", "obd", "dtc"],
) -> GasLabDnaView | ObdLabDnaView | DtcLabDnaView:
    """Project a full VehicleDNA JSON dict into the requested LabDnaView.  # lld: §5.2

    Precondition: vehicle_dna_json conforms to the VehicleDNA schema (§3.2).
    Postcondition: returned model is frozen; mutation raises.
    Raises: pydantic.ValidationError if a required field is missing.
    """
    vin = vehicle_dna_json["vin_dna"]  # lld: §5.2 — top-level key

    resolved_horizon = vin.get("resolved_horizon")
    if resolved_horizon is None:
        resolved_horizon = _horizon_from_euro(vin.get("euro_emission_category"))
        # lld: §5.2 — fallback for older payloads missing resolved_horizon
    # Normalise string to Horizon value if needed
    if isinstance(resolved_horizon, str):
        resolved_horizon = Horizon(resolved_horizon)

    raw_confidence = vin.get("confidence")
    if isinstance(raw_confidence, str):
        confidence = VinConfidence(raw_confidence)
    else:
        confidence = raw_confidence

    if target == "gas":
        return GasLabDnaView(
            engine_displacement_liters=vin.get("engine_displacement_liters"),
            cylinder_count=vin.get("cylinder_count"),
            number_of_banks=vin.get("number_of_banks"),
            euro_emission_category=vin.get("euro_emission_category"),
            fuel_delivery_type=vin.get("fuel_delivery_type"),
            induction_type=vin.get("induction_type"),
            upstream_o2_type=vin.get("upstream_o2_type"),
            has_catalyst=vin.get("has_catalyst"),
            egr_equipped=vin.get("egr_equipped"),
            target_lambda_v112=vin.get("target_lambda_v112"),
            # consumer: GasLabDnaView.target_lambda_v112 — DEP-4 / proposal vehicle-dna-projection-paths
            co_low_idle=vin.get("co_low_idle"),
            # consumer: GasLabDnaView.co_low_idle — DEP-4 / proposal vehicle-dna-projection-paths
            co_high_idle=vin.get("co_high_idle"),
            # consumer: GasLabDnaView.co_high_idle — DEP-4 / proposal vehicle-dna-projection-paths
            confidence=confidence,
            resolved_horizon=resolved_horizon,
        )
    if target == "obd":
        return ObdLabDnaView(
            engine_displacement_liters=vin.get("engine_displacement_liters"),
            cylinder_count=vin.get("cylinder_count"),
            rated_rpm=vin.get("rated_rpm"),
            stress_idle_rpm_target=vin.get("stress_idle_rpm_target"),
            air_metering_strategy=vin.get("air_metering_strategy"),
            upstream_o2_type=vin.get("upstream_o2_type"),
            induction_type=vin.get("induction_type"),
            egr_equipped=vin.get("egr_equipped"),
            resolved_horizon=resolved_horizon,
            confidence=confidence,
        )
    # target == "dtc"
    return DtcLabDnaView(
        make=vin.get("make"),
        model_year=vin.get("model_year"),
        euro_emission_category=vin.get("euro_emission_category"),
        air_metering_strategy=vin.get("air_metering_strategy"),
        resolved_horizon=resolved_horizon,

        has_catalyst=vin.get("has_catalyst"),
        egr_equipped=vin.get("egr_equipped"),
        confidence=confidence,
    )


def project_all(vehicle_dna_json: VehicleDnaJson) -> ProjectedViews:
    """Project once into all three views.  # lld: §5.2

    Returned tuple-shaped model is what fault_atlas_router holds for
    the lifetime of one session.
    """
    return ProjectedViews(
        gas=cast(GasLabDnaView, project(vehicle_dna_json, target="gas")),
        obd=cast(ObdLabDnaView, project(vehicle_dna_json, target="obd")),
        dtc=cast(DtcLabDnaView, project(vehicle_dna_json, target="dtc")),
    )
