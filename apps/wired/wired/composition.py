"""Composition seam for wiring current 4DLab labs into COMLab.

This module is the only legal point that imports multiple labs together. It runs
lab public entry points, maps their typed outputs into COMLab's local mirror
schemas, and returns the verdict from ``LabPipelineAggregator.process()``.
"""

from __future__ import annotations

import math
import uuid
from typing import Any

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import (
    DTCLabPayload as COMDTCLabPayload,
)
from comlab.schemas.ingestion import (
    FreezeFramePIDs,
    OrchestratorInboundRequest,
    SessionMetadata,
)
from comlab.schemas.ingestion import (
    GasLabPayload as COMGasLabPayload,
)
from comlab.schemas.ingestion import (
    OBDLiveDataPayload as COMOBDLiveDataPayload,
)
from comlab.schemas.response import OrchestratorFinalUIOutput
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    DownstreamTrimRole,
    EngineStateBucket,
    O2FailureMode,
    SampleValidity,
    TrimAnalyticsGate,
    VEValidity,
    VinConfidence,
)
from dnalab import build_vehicle_dna
from dtclab import DataFusionSanitizer
from dtclab.schemas.dna_view import (
    AirMeteringStrategy as DtcAirMeteringStrategy,
)
from dtclab.schemas.dna_view import (
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
)
from dtclab.schemas.dna_view import (
    VinConfidence as DtcVinConfidence,
)
from gaslab import GasLabContext, GasReading, process
from gaslab.contracts import EngineStateBucket as GASEngineStateBucket
from gaslab.dna_view import GasLabDnaView
from obdlab import SensorSignalTranslator
from obdlab.schemas.dna_view import (
    AirMeteringStrategy as OBDAirMeteringStrategy,
)
from obdlab.schemas.dna_view import (
    InductionType as OBDInductionType,
)
from obdlab.schemas.dna_view import (
    O2SensorType,
    ObdLabDnaView,
)
from obdlab.schemas.dna_view import (
    VinConfidence as OBDVinConfidence,
)
from symptomlab import SymptomValidationError
from symptomlab import resolve as resolve_symptom
from vinlab import VINDecodeError
from vinlab import decode as decode_vin

from wired.tracing import span

_FALLBACK_VIN = "UNKNOWNVIN0000000"

# Required-input key sets. wired only checks that each key is present; the labs own the meaning.
_TRIAGE_KEYS = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")
# dnalab/assembly.py build_vehicle_dna `required` — pinned by tests/test_t_aud_1a_inputs.py
_GAS_LOW_IDLE_KEYS = ("hc", "co", "co2", "o2", "nox")  # the GasReading fields read in _run_gaslab
_OBD_REQUIRED_KEYS = ("shrtft1", "longft1", "engine_rpm", "coolant_temp_c")
# obdlab trim_vector_aggregator (STFT/LTFT B1) + OBDLivePayload (RPM, ECT); the O2 key is per sensor type
_OBD_BANK2_KEYS = ("shrtft2", "longft2")  # obdlab trim_vector_aggregator bank-2 null contract
_FREEZE_FRAME_KEYS = (
    "calculated_load_pct",  # wiki: DTC_VOCABULARY.md §12.1
    "engine_rpm",  # wiki: DTC_VOCABULARY.md §12.1
    "coolant_temp_c",  # wiki: DTC_VOCABULARY.md §12.1
    "short_term_ft1",  # wiki: DTC_VOCABULARY.md §12.1
    "long_term_ft1",  # wiki: DTC_VOCABULARY.md §12.1
    "manifold_pressure_kpa",  # wiki: DTC_VOCABULARY.md §12.1
    "vehicle_speed_kmh",  # wiki: DTC_VOCABULARY.md §12.1
    "ignition_advance_deg",  # wiki: DTC_VOCABULARY.md §12.1
    "intake_air_temp_c",  # wiki: DTC_VOCABULARY.md §12.1
    "maf_gps",  # wiki: DTC_VOCABULARY.md §12.1
    "throttle_pos_pct",  # wiki: DTC_VOCABULARY.md §12.1
    "fuel_system_status",  # wiki: DTC_VOCABULARY.md §12.1
)  # = dtclab freeze_frame_extractor._MANDATORY_PIDS — pinned by tests/test_t_aud_1a_inputs.py
# T-AUD-4s (F-C4-8): the raw OBD channels COMLab reads straight from the input, never through
# OBDLab. Each range equals the UI form's (apps/ui/ui_payload.py constants; mode06_min_margin_pct
# is app.py's literal) — pinned by apps/ui/tests/test_t_aud_4s_raw_obd_ranges.py.
_OBD_RAW_RANGES: dict[str, tuple[float, float, type]] = {
    "mode06_catalyst_margin_pct": (-1000.0, 100.0, float),
    "catalyst_index_ratio": (0.0, 2.0, float),
    "stft_idle_pct": (-127.0, 127.0, float),
    "ltft_idle_pct": (-127.0, 127.0, float),
    "stft_2500_pct": (-127.0, 127.0, float),
    "ltft_2500_pct": (-127.0, 127.0, float),
    "mode06_o2_response_margin_pct": (0.0, 100.0, float),
    "maf_actual_calc_delta_pct_idle": (-100.0, 100.0, float),
    "maf_actual_calc_delta_pct_2500": (-100.0, 100.0, float),
    "maf_gps_idle": (0.0, 500.0, float),
    "maf_gps_2500": (0.0, 500.0, float),
    "calc_airflow_gps_idle": (0.0, 500.0, float),
    "calc_airflow_gps_2500": (0.0, 500.0, float),
    "koeo_map_baro_delta_kpa": (0.0, 50.0, float),
    "module_voltage_loaded_v": (0.0, 18.0, float),
    "dlc_signal_ground_drop_v": (0.0, 5.0, float),
    "stft_load_pct": (-127.0, 127.0, float),
    "ltft_load_pct": (-127.0, 127.0, float),
    "calc_load_wot_pct": (0.0, 100.0, float),
    "fuel_rail_pressure_load_kpa": (0.0, 250000.0, float),
    "wideband_lambda_wot": (0.0, 3.0, float),
    "co2_idle_pct": (0.0, 22.0, float),
    "tailpipe_o2_elevation_pct": (0.0, 22.0, float),
    "downstream_o2_v": (0.0, 1.5, float),
    "propane_trim_shift_pct": (-100.0, 100.0, float),
    "stored_dtc_count": (0, 100, int),
    "pending_dtc_count": (0, 100, int),
    "permanent_dtc_count": (0, 100, int),
    "mode06_min_margin_pct": (-100.0, 100.0, float),
    "warmup_cycles_since_clear": (0, 255, int),
    "miles_since_clear": (0, 65535, int),
}
_NON_STARTER = "will_not_start"  # the triage engine_state comlab symptom_router suppresses GASLab on


def diagnose(
    raw_inputs: dict[str, Any],
    *,
    enable_fatal_gates: bool = False,
) -> OrchestratorFinalUIOutput:
    """Run DNALab, GASLab, optional OBDLab/DTCLab, then COMLab aggregation.

    Expected ``raw_inputs`` keys are ``vin``, ``triage``, ``gas``, optional
    ``obd``, optional ``dtc``, and optional technician ``overrides``. The return
    value is the public COMLab ``OrchestratorFinalUIOutput``. Fatal gates stay
    default-off and are forwarded only when explicitly requested.
    """
    with span("wired.diagnose"):
        return _diagnose(raw_inputs, enable_fatal_gates=enable_fatal_gates)


def _diagnose(
    raw_inputs: dict[str, Any],
    *,
    enable_fatal_gates: bool,
) -> OrchestratorFinalUIOutput:
    """Run the wired composition pipeline under the public diagnose span."""
    vin = str(raw_inputs.get("vin", ""))
    triage = _as_dict(raw_inputs.get("triage"))
    gas_inputs = _as_dict(raw_inputs.get("gas"))
    obd_inputs = raw_inputs.get("obd")
    dtc_inputs = raw_inputs.get("dtc")

    symptom_dna: dict[str, Any] = {}
    try:
        if _missing(triage, _TRIAGE_KEYS):
            # Absent or incomplete triage is the absent-symptom case: decode the VIN, no symptom.
            vin_dna = _as_dict(decode_vin(vin).to_json_payload())
        else:
            with span("lab.dnalab.build"):
                vehicle_dna = build_vehicle_dna(vin, triage)
            dna_payload = vehicle_dna.to_json_payload()
            vin_dna = _as_dict(dna_payload["vin_dna"])
            symptom_dna = _as_dict(dna_payload.get("symptom_dna"))
    except VINDecodeError:
        vin_dna = _build_fallback_vin_dna(vin)
        symptom_dna = _symptom_without_vin(triage)

    if "resolved_horizon" not in vin_dna:
        vin_dna["resolved_horizon"] = _derive_horizon(
            str(vin_dna.get("euro_emission_category", "EURO_6"))
        )

    # The technician's overrides win over the VIN decode, so they go in before any lab reads vin_dna.
    emissions = vin_dna["emissions"] = _as_dict(vin_dna.get("emissions"))
    overrides = _as_dict(raw_inputs.get("overrides"))
    if overrides.get("upstream_o2_type"):
        emissions["upstream_o2_type"] = overrides["upstream_o2_type"]
        # consumer: GASLab DNA view upstream_o2_type (_build_gas_dna_view), OBDLab O2SensorType
        # (_build_obd_dna_view) and the required O2 reading key (_obd_required_keys)
    if overrides.get("de_cat"):
        emissions["has_catalyst"] = False
        # consumer: GASLab DNA view has_catalyst (_build_gas_dna_view) and the request's has_catalyst
        # (power_loss_analytics catalyst index gate + perception_contradiction de-cat check)

    csv_symptom = triage.get("csv_primary_symptom")
    if csv_symptom:
        symptom_dna["_csv_primary_symptom"] = csv_symptom

    metadata = _build_metadata(vin_dna)
    incomplete = _incomplete_input(triage, gas_inputs, obd_inputs, dtc_inputs, vin_dna)
    if incomplete is not None:
        error_code, message = incomplete
        return LabPipelineAggregator(enable_fatal_gates=enable_fatal_gates).abort_incomplete(
            metadata, error_code, message
        )
    out_of_range = _out_of_range_input(obd_inputs)
    if out_of_range is not None:
        error_code, message = out_of_range
        return LabPipelineAggregator(enable_fatal_gates=enable_fatal_gates).abort_incomplete(
            metadata, error_code, message
        )
    gas_output = None if _gasless_non_starter(triage, gas_inputs) else _run_gaslab(gas_inputs, vin_dna)
    obd_output = (
        _run_obdlab(_with_user_dtcs(_as_dict(obd_inputs), dtc_inputs), vin_dna)
        if obd_inputs is not None
        else None
    )
    dtc_output = _run_dtclab(_as_dict(dtc_inputs), vin_dna) if dtc_inputs is not None else None

    request = OrchestratorInboundRequest(
        metadata=metadata,
        gas_lab_output=gas_output,
        obd_live_data=obd_output,
        dtc_lab_output=dtc_output,
        symptom_dna=symptom_dna,
        downstream_trim_role=DownstreamTrimRole(emissions.get("downstream_trim_role", "NONE")),
        # consumer: perception_contradiction O2-health verdict qualification (T-FX-9)
        has_catalyst=bool(emissions.get("has_catalyst", True)),
        # consumer: power_loss_analytics catalyst index gate + perception_contradiction de-cat check
    )
    with span("comlab.process"):
        return LabPipelineAggregator(enable_fatal_gates=enable_fatal_gates).process(request)


def validate_triage(triage: dict[str, Any]) -> str | None:
    """Return why a complete triage selection is invalid, or ``None`` when it is valid.

    The check is SymptomLab's own (``symptomlab.resolve``); the UI calls this before a run
    so an invalid selection becomes a field warning. An absent or incomplete triage is valid:
    ``diagnose`` treats it as the absent-symptom case.
    """
    if _missing(triage, _TRIAGE_KEYS):
        return None
    try:
        resolve_symptom(
            tier_1=triage["tier_1"],
            tier_2=triage["tier_2"],
            occurs_during=triage["occurs_during"],
            engine_state=triage["engine_state"],
            load_state=triage["load_state"],
        )
    except SymptomValidationError as exc:
        return str(exc)
    return None


def _symptom_without_vin(triage: dict[str, Any]) -> dict[str, Any]:
    """Resolve the triage alone when the VIN does not decode; {} when it is incomplete or invalid."""
    # consumer: comlab symptom_router (lld §6.2) via request.symptom_dna — engine_state / occurs_during routing
    if _missing(triage, _TRIAGE_KEYS):
        return {}
    try:
        symptom = resolve_symptom(**{key: triage[key] for key in _TRIAGE_KEYS})
    except SymptomValidationError:
        return {}  # _incomplete_input reports the invalid triage
    return _as_dict(symptom.to_json_payload())


def _missing(inputs: dict[str, Any], keys: tuple[str, ...]) -> list[str]:
    """Return the keys of *keys* that are absent, ``None`` or blank in *inputs*."""
    return [key for key in keys if inputs.get(key) is None or str(inputs[key]).strip() == ""]


def _raw_obd_value(obd_inputs: dict[str, Any], key: str) -> float | int | None:
    """Return the raw OBD channel *key* parsed and range-checked, or ``None`` when absent or blank.

    Raises ``ValueError`` for a value that is not a finite number, not a whole number for an
    integer channel, or outside ``_OBD_RAW_RANGES[key]`` (T-AUD-4s, F-C4-8).
    """
    value = obd_inputs.get(key)
    if value is None or str(value).strip() == "":
        return None
    low, high, kind = _OBD_RAW_RANGES[key]
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{key}={value!r} is not a number") from None
    if not math.isfinite(number):
        raise ValueError(f"{key}={value!r} is not a finite number")
    if kind is int and not number.is_integer():
        raise ValueError(f"{key}={value!r} is not a whole number")
    if not low <= number <= high:
        raise ValueError(f"{key}={value!r} is outside {low}–{high}")
    return int(number) if kind is int else number


def _out_of_range_input(obd_inputs: Any) -> tuple[str, str] | None:
    """Return ``("OBD_INPUT_OUT_OF_RANGE", message)`` naming every bad raw OBD channel, or ``None``."""
    if obd_inputs is None:
        return None
    obd = _as_dict(obd_inputs)
    problems = []
    for key in _OBD_RAW_RANGES:
        try:
            _raw_obd_value(obd, key)
        except ValueError as exc:
            problems.append(str(exc))
    if not problems:
        return None
    return (
        "OBD_INPUT_OUT_OF_RANGE",
        f"OBD readings out of range: {'; '.join(problems)}. Correct them or leave them blank.",
    )


def _obd_required_keys(obd_inputs: dict[str, Any], vin_dna: dict[str, Any]) -> tuple[str, ...]:
    """Return the OBD keys OBDLab needs: the upstream O2 key for the sensor type, trims, RPM, ECT."""
    if _build_obd_dna_view(vin_dna).upstream_o2_type == O2SensorType.WIDEBAND_LINEAR:
        o2_key = "pid_wideband_equivalence_ratio"  # obdlab o2_normalizer wideband branch
    else:
        o2_key = "pid_oxygen_sensor_volts"  # obdlab o2_normalizer narrowband / NB-sim branches
    keys = (o2_key, *_OBD_REQUIRED_KEYS)
    if obd_inputs.get("number_of_banks") == 2:
        keys = (*keys, *_OBD_BANK2_KEYS)
    return keys


def _gasless_non_starter(triage: dict[str, Any], gas_inputs: dict[str, Any]) -> bool:
    """True for a will_not_start session with no gas reading at all (T-COMA-2: GASLab is not run)."""
    return triage.get("engine_state") == _NON_STARTER and len(
        _missing(gas_inputs, _GAS_LOW_IDLE_KEYS)
    ) == len(_GAS_LOW_IDLE_KEYS)


def _incomplete_input(
    triage: dict[str, Any],
    gas_inputs: dict[str, Any],
    obd_inputs: Any,
    dtc_inputs: Any,
    vin_dna: dict[str, Any],
) -> tuple[str, str] | None:
    """Return ``(error_code, message)`` for the first incomplete required input, or ``None``.

    A presence check only, run before any lab: low-idle gas, then OBD live data (when sent),
    then the freeze frame (when a DTC dict is sent). The verdict comes from
    ``LabPipelineAggregator.abort_incomplete``.
    """
    missing = _missing(gas_inputs, _GAS_LOW_IDLE_KEYS)
    if missing and not _gasless_non_starter(triage, gas_inputs):
        fields = ", ".join(missing)
        return "GAS_INPUT_INCOMPLETE", f"Low-idle gas readings are incomplete. Tick GASLab and enter: {fields}."
    if obd_inputs is not None:
        obd = _as_dict(obd_inputs)
        missing = _missing(obd, _obd_required_keys(obd, vin_dna))
        if missing:
            return (
                "OBD_INPUT_INCOMPLETE",
                f"OBD live data is incomplete. Enter: {', '.join(missing)}, or untick OBDLab.",
            )
    if dtc_inputs is not None:
        freeze_frame = _as_dict(_as_dict(dtc_inputs).get("raw_freeze_frame"))
        missing = _missing(freeze_frame, _FREEZE_FRAME_KEYS)
        if missing:
            return (
                "FREEZE_FRAME_INCOMPLETE",
                f"Freeze frame is incomplete. Enter: {', '.join(missing)}.",
            )
    return None


def _build_metadata(vin_dna: dict[str, Any]) -> SessionMetadata:
    """Build COMLab session metadata from VIN/DNA output."""
    strategy_value = vin_dna.get("air_metering_strategy")
    strategy = AirMeteringStrategy(strategy_value) if strategy_value else None
    vin_for_metadata = str(vin_dna.get("vin") or _FALLBACK_VIN)
    if len(vin_for_metadata) != 17:
        vin_for_metadata = _FALLBACK_VIN

    return SessionMetadata(
        session_id=uuid.uuid4(),
        vin_dna_string=vin_for_metadata,
        resolved_horizon=str(vin_dna["resolved_horizon"]),
        cylinder_count=int(vin_dna.get("cylinder_count") or 4),
        schema_version="1.0",
        vin_confidence=VinConfidence(str(vin_dna.get("confidence", "NONE"))),
        air_metering_strategy=strategy,
        # consumer: fault_atlas_router.execute_triage_loop VE circularity gate
    )


def _run_gaslab(gas_inputs: dict[str, Any], vin_dna: dict[str, Any]) -> COMGasLabPayload:
    """Run GASLab and map its output into COMLab's ``GasLabPayload`` mirror."""
    reading = GasReading(
        hc=int(gas_inputs["hc"]),
        co=float(gas_inputs["co"]),
        co2=float(gas_inputs["co2"]),
        o2=float(gas_inputs["o2"]),
        nox=int(gas_inputs["nox"]),
    )

    high_reading = None
    high_keys = ("hc_high", "co_high", "co2_high", "o2_high", "nox_high")
    if all(gas_inputs.get(key) is not None for key in high_keys):
        high_reading = GasReading(
            hc=int(gas_inputs["hc_high"]),
            co=float(gas_inputs["co_high"]),
            co2=float(gas_inputs["co2_high"]),
            o2=float(gas_inputs["o2_high"]),
            nox=int(gas_inputs["nox_high"]),
        )

    context = GasLabContext(
        dna=_build_gas_dna_view(
            vin_dna,
            coc_target_lambda_v112=gas_inputs.get("coc_target_lambda_v112"),
            coc_target_lambda_low=gas_inputs.get("coc_target_lambda_low"),
            coc_target_lambda_high=gas_inputs.get("coc_target_lambda_high"),
            coc_co_low_idle=gas_inputs.get("coc_co_low_idle"),
            coc_co_high_idle=gas_inputs.get("coc_co_high_idle"),
        ),
        engine_state=GASEngineStateBucket(gas_inputs.get("engine_state", "STABILIZED_IDLE")),
        lambda_measured=gas_inputs.get("lambda_measured"),
        block_test_passed=bool(gas_inputs.get("block_test_passed", False)),
        reading_high=high_reading,
        fuel_trim=gas_inputs.get("fuel_trim"),
    )
    with span("lab.gaslab.process"):
        gas_payload = process(reading, context)

    return COMGasLabPayload(
        chemical_state=_enum_value(gas_payload.chemical_state),
        # consumer: perception_contradiction + Stage-D power_loss_analytics chemistry branch
        gas_co=gas_payload.gas_co,
        # consumer: fault_atlas_router combustion evidence
        gas_hc=gas_payload.gas_hc,
        # consumer: fault_atlas_router combustion evidence
        gas_co2=gas_payload.gas_co2,
        # consumer: fault_atlas_router combustion evidence
        gas_o2=gas_payload.gas_o2,
        # consumer: fault_atlas_router combustion evidence
        gas_nox=gas_payload.gas_nox,
        # consumer: fault_atlas_router combustion evidence
        lambda_chem=gas_payload.lambda_chem,
        # consumer: perception_contradiction.select_perception_lambda
        sample_validity=SampleValidity(_enum_value(gas_payload.sample_validity)),
        # consumer: lab_pipeline_aggregator Stage A fatal gate ERR-ABORT-001
        lambda_measured=gas_payload.lambda_measured,
        # consumer: perception_contradiction.select_perception_lambda (T-FX-7 no-OBD path)
        high_idle_hc=gas_payload.high_idle_hc,
        # consumer: registry REG-V2 shim PID resolver -> MW-008/MW-009 high-idle HC
        high_idle_co=gas_payload.high_idle_co,
        # consumer: registry REG-V2 shim PID resolver -> MW-008/MW-009 high-idle CO
        # high_idle_co2/o2/nox: not mirrored, no reader (F-C4-5, T-AUD-4p)
        high_idle_lambda=gas_payload.high_idle_lambda,
        # consumer: registry REG-V2 shim PID resolver -> MW-008/MW-009 high-idle lambda
        decel_co_pct=float(gas_inputs["decel_co_pct"]) if gas_inputs.get("decel_co_pct") is not None and str(gas_inputs["decel_co_pct"]).strip() != "" else None,
        pre_post_cat_hc_delta_ppm=float(gas_inputs["pre_post_cat_hc_delta_ppm"]) if gas_inputs.get("pre_post_cat_hc_delta_ppm") is not None and str(gas_inputs["pre_post_cat_hc_delta_ppm"]).strip() != "" else None,
        pre_post_cat_co_delta_pct=float(gas_inputs["pre_post_cat_co_delta_pct"]) if gas_inputs.get("pre_post_cat_co_delta_pct") is not None and str(gas_inputs["pre_post_cat_co_delta_pct"]).strip() != "" else None,
    )


def _build_gas_dna_view(
    vin_dna: dict[str, Any],
    *,
    coc_target_lambda_v112: float | None = None,
    coc_target_lambda_low: float | None = None,
    coc_target_lambda_high: float | None = None,
    coc_co_low_idle: float | None = None,
    coc_co_high_idle: float | None = None,
) -> GasLabDnaView:
    """Project VIN/DNA output into GASLab's local DNA view."""
    emissions = _as_dict(vin_dna.get("emissions"))
    target_lambda = coc_target_lambda_v112
    if target_lambda is None:
        if coc_target_lambda_low is not None and coc_target_lambda_high is not None:
            target_lambda = (coc_target_lambda_low + coc_target_lambda_high) / 2.0
            # wiki: GAS_VOCABULARY §3 — CoC lambda target midpoint fallback
        else:
            target_lambda = vin_dna.get("target_lambda_v112")

    induction = str(vin_dna.get("induction_type", "NATURALLY_ASPIRATED"))
    if induction in {"TURBOCHARGED", "SUPERCHARGED"}:
        induction = "forced"

    return GasLabDnaView(
        engine_displacement_liters=float(vin_dna.get("engine_displacement_liters") or 2.0),
        cylinder_count=int(vin_dna.get("cylinder_count") or 4),
        number_of_banks=int(vin_dna.get("number_of_banks") or 1),
        euro_emission_category=str(vin_dna.get("euro_emission_category", "EURO_6")),
        fuel_delivery_type=str(vin_dna.get("fuel_delivery_type", "PORT_INJECTION")),
        induction_type=induction,
        upstream_o2_type=str(emissions.get("upstream_o2_type", "NARROWBAND_0_TO_1V")),
        has_catalyst=bool(emissions.get("has_catalyst", True)),
        egr_equipped=bool(emissions.get("egr_equipped", False)),
        target_lambda_v112=target_lambda,
        # consumer: GASLab rule_engine._coc_adjust_normal_bounds lambda target window
        co_low_idle=coc_co_low_idle if coc_co_low_idle is not None else vin_dna.get("co_low_idle"),
        # consumer: GASLab rule_engine._coc_adjust_normal_bounds low-idle CO max
        co_high_idle=coc_co_high_idle
        if coc_co_high_idle is not None
        else vin_dna.get("co_high_idle"),
        # consumer: GASLab rule_engine._coc_adjust_normal_bounds high-idle CO max
        confidence=str(vin_dna.get("confidence", "NONE")),
    )


def _run_obdlab(obd_inputs: dict[str, Any], vin_dna: dict[str, Any]) -> COMOBDLiveDataPayload:
    """Run OBDLab and map its output into COMLab's ``OBDLiveDataPayload`` mirror."""
    with span("lab.obdlab.translate"):
        obd_payload = SensorSignalTranslator().translate(obd_inputs, _build_obd_dna_view(vin_dna))
    freeze_frame = None
    if obd_payload.freeze_frame_pids:
        freeze_frame = FreezeFramePIDs(**obd_payload.freeze_frame_pids)

    return COMOBDLiveDataPayload(
        engine_warmed=obd_payload.engine_warmed,
        # consumer: lab_pipeline_aggregator Stage A thermal gate
        total_trim_correction_delta=obd_payload.total_trim_correction_delta,
        # consumer: fault_atlas_router rich/lean differential diagnosis
        total_trim_correction_delta_b2=obd_payload.total_trim_correction_delta_b2,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        lambda_perception_delta=obd_payload.lambda_perception_delta,
        # consumer: fault_atlas_router ecu_fault fuse (T-COMV2-ECU-FUSE-1)
        per_bank_trim_delta=obd_payload.per_bank_trim_delta,
        # consumer: fault_atlas_router bank-asymmetry verdict (T-COMV2-BANK-FUSE-1)
        per_cylinder_misfire_counts=obd_payload.per_cylinder_misfire_counts,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        ltft_cell_vector=obd_payload.ltft_cell_vector,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        control_module_voltage_v=obd_payload.control_module_voltage_v,
        # consumer: perception_contradiction.detect VPWR gate (T-COMV2-VPWR-GATE-1)
        w_theo=obd_payload.w_theo,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        sensor_error_delta=obd_payload.sensor_error_delta,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        shrtft1=obd_payload.shrtft1,
        # consumer: fault_atlas_router SF-008 + EF-001/002/003 evidence
        longft1=obd_payload.longft1,
        # consumer: fault_atlas_router SF-008 + EF-001/002/003 evidence
        mass_airflow_gps=obd_payload.mass_airflow_gps,
        # consumer: fault_atlas_router SF-004 evidence
        manifold_vacuum_kpa=obd_payload.manifold_vacuum_kpa,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        coolant_temp_c=obd_payload.coolant_temp_c,
        # consumer: fault_atlas_router SF-006 evidence
        intake_air_temp_c=obd_payload.intake_air_temp_c,
        # consumer: ecu_hardware_checker.ECUHardwareChecker
        throttle_pos_pct=obd_payload.throttle_pos_pct,
        # consumer: ecu_hardware_checker.ECUHardwareChecker
        normalized_obd_lambda=obd_payload.normalized_obd_lambda,
        # consumer: perception_contradiction cross-check vs lambda_chem
        ve_pct=obd_payload.ve_pct,
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        ve_validity=VEValidity(_enum_value(obd_payload.ve_validity)),
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        rpm_state_bucket=EngineStateBucket(_enum_value(obd_payload.rpm_state_bucket)),
        # consumer: fault_atlas_router evidence weighting per operating regime
        trim_analytics_gate=TrimAnalyticsGate(_enum_value(obd_payload.trim_analytics_gate)),
        # consumer: registry/integration_shim._resolve_single_source drops live trims when blocked
        fuel_system_status=_enum_value(obd_payload.fuel_system_status),
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        o2_failure_mode=O2FailureMode(_enum_value(obd_payload.o2_failure_mode)),
        # consumer: v1 execute_triage_loop only (use_v2_registry=False); no reader on the default v2 path (F-C4-5)
        # maf_status/map_status: not mirrored, no reader (F-C4-5, T-AUD-4p)
        freeze_frame_pids=freeze_frame,
        # consumer: fault_atlas_router SF-001/002/003/006/007 O2-voltage evidence
        mode06_catalyst_margin_pct=_raw_obd_value(obd_inputs, "mode06_catalyst_margin_pct"),
        catalyst_index_ratio=_raw_obd_value(obd_inputs, "catalyst_index_ratio"),
        stft_idle_pct=_raw_obd_value(obd_inputs, "stft_idle_pct"),
        ltft_idle_pct=_raw_obd_value(obd_inputs, "ltft_idle_pct"),
        stft_2500_pct=_raw_obd_value(obd_inputs, "stft_2500_pct"),
        ltft_2500_pct=_raw_obd_value(obd_inputs, "ltft_2500_pct"),
        mode06_o2_response_margin_pct=_raw_obd_value(obd_inputs, "mode06_o2_response_margin_pct"),
        # consumer: registry integration_shim SensorDynamicsState O2_LAZY_OR_BIASED branch (T-V3-P4-C6B)
        maf_actual_calc_delta_pct_idle=_raw_obd_value(obd_inputs, "maf_actual_calc_delta_pct_idle"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        maf_actual_calc_delta_pct_2500=_raw_obd_value(obd_inputs, "maf_actual_calc_delta_pct_2500"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        maf_gps_idle=_raw_obd_value(obd_inputs, "maf_gps_idle"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        maf_gps_2500=_raw_obd_value(obd_inputs, "maf_gps_2500"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        calc_airflow_gps_idle=_raw_obd_value(obd_inputs, "calc_airflow_gps_idle"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        calc_airflow_gps_2500=_raw_obd_value(obd_inputs, "calc_airflow_gps_2500"),
        # consumer: registry integration_shim SensorDynamicsState MAF_UNDERREAD branch (T-V3-P4-C6B)
        koeo_map_baro_delta_kpa=_raw_obd_value(obd_inputs, "koeo_map_baro_delta_kpa"),
        # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch (T-V3-P4-C3B)
        module_voltage_loaded_v=_raw_obd_value(obd_inputs, "module_voltage_loaded_v"),
        # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch (T-V3-P4-C3B)
        dlc_signal_ground_drop_v=_raw_obd_value(obd_inputs, "dlc_signal_ground_drop_v"),
        # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch (T-V3-P4-C3B)
        bidirectional_fuel_response_ok_bool=obd_inputs.get("bidirectional_fuel_response_ok_bool"),
        # consumer: registry integration_shim CONTROL_REFERENCE_FAULT branch (T-V3-P4-C3B)
        stft_load_pct=_raw_obd_value(obd_inputs, "stft_load_pct"),
        # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
        ltft_load_pct=_raw_obd_value(obd_inputs, "ltft_load_pct"),
        # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
        calc_load_wot_pct=_raw_obd_value(obd_inputs, "calc_load_wot_pct"),
        # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
        fuel_rail_pressure_load_kpa=_raw_obd_value(obd_inputs, "fuel_rail_pressure_load_kpa"),
        # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
        wideband_lambda_wot=_raw_obd_value(obd_inputs, "wideband_lambda_wot"),
        # consumer: registry integration_shim LeanRootCauseState branch — T-V3-P4-C5B
        # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
        co2_idle_pct=_raw_obd_value(obd_inputs, "co2_idle_pct"),
        # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
        tailpipe_o2_elevation_pct=_raw_obd_value(obd_inputs, "tailpipe_o2_elevation_pct"),
        # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
        downstream_o2_v=_raw_obd_value(obd_inputs, "downstream_o2_v"),
        # consumer: registry integration_shim C4SignalState branch — T-V3-P4-C4B
        propane_trim_shift_pct=_raw_obd_value(obd_inputs, "propane_trim_shift_pct"),
        readiness_supported_complete_bool=obd_inputs.get("readiness_supported_complete_bool"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        stored_dtc_count=_raw_obd_value(obd_inputs, "stored_dtc_count"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        pending_dtc_count=_raw_obd_value(obd_inputs, "pending_dtc_count"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        permanent_dtc_count=_raw_obd_value(obd_inputs, "permanent_dtc_count"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        mode06_min_margin_pct=_raw_obd_value(obd_inputs, "mode06_min_margin_pct"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        warmup_cycles_since_clear=_raw_obd_value(obd_inputs, "warmup_cycles_since_clear"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
        miles_since_clear=_raw_obd_value(obd_inputs, "miles_since_clear"),
        # consumer: registry integration_shim HealthConfirmationState branch — T-V3-P4-C9B
    )


def _build_obd_dna_view(vin_dna: dict[str, Any]) -> ObdLabDnaView:
    """Project VIN/DNA output into OBDLab's local DNA view."""
    emissions = _as_dict(vin_dna.get("emissions"))
    induction = str(vin_dna.get("induction_type", "NATURALLY_ASPIRATED"))
    if induction == "SUPERCHARGED":
        # OBDLab's InductionType separates NA from forced induction only (its reader is the NA VE
        # ceiling, obdlab/core/ve_engine.py), so a supercharged engine projects as TURBOCHARGED.
        induction = "TURBOCHARGED"
    return ObdLabDnaView(
        engine_displacement_liters=float(vin_dna.get("engine_displacement_liters") or 0.0)
        or None,
        rated_rpm=vin_dna.get("rated_rpm"),
        stress_idle_rpm_target=vin_dna.get("stress_idle_rpm_target"),
        air_metering_strategy=OBDAirMeteringStrategy(
            vin_dna.get("air_metering_strategy", "MAP_ONLY_SPEED_DENSITY")
        ),
        upstream_o2_type=O2SensorType(
            _map_o2_sensor_type(str(emissions.get("upstream_o2_type", "NARROWBAND_0_TO_1V")))
        ),
        induction_type=OBDInductionType(induction),
        confidence=OBDVinConfidence(str(vin_dna.get("confidence", "NONE"))),
    )


_DTC_AIR_METERING = {
    "MAF_ONLY": "MAF",
    "MAP_ONLY_SPEED_DENSITY": "MAP_SPEED_DENSITY",
    "DUAL_MAF_MAP_CROSSCHECK": "HYBRID",
}  # DTC_VOCABULARY.md §14.1
_DTC_HORIZON = {
    "HORIZON_LEGACY": "HORIZON_LEGACY",
    "HORIZON_ADAPTIVE": "HORIZON_CLASSIC",
    "HORIZON_MODERN": "HORIZON_MODERN",
}  # DTC_VOCABULARY.md §14.1 (CLASSIC = Euro 3-4 = COMLab ADAPTIVE)
_DTC_EURO = {f"EURO_{n}" for n in range(1, 8)}


def _build_dtc_dna_view(vin_dna: dict[str, Any]) -> DtcLabDnaView | None:
    """Project VIN/DNA output into DTCLab's DNA view, or None when a required field is unknown."""
    emissions = _as_dict(vin_dna.get("emissions"))
    has_catalyst = emissions.get("has_catalyst")
    egr_equipped = emissions.get("egr_equipped")
    model_year = vin_dna.get("model_year")
    air = _DTC_AIR_METERING.get(str(vin_dna.get("air_metering_strategy")))
    horizon = _DTC_HORIZON.get(str(vin_dna.get("resolved_horizon")))
    confidence = str(vin_dna.get("confidence", "NONE"))
    if (
        not isinstance(has_catalyst, bool)
        or not isinstance(egr_equipped, bool)
        or model_year is None
        or air is None
        or horizon is None
        or confidence not in {"HIGH", "PARTIAL", "NONE"}
    ):
        return None  # DTC_VOCABULARY.md §14.3: None is treated as confidence NONE
    euro = str(vin_dna.get("euro_emission_category"))
    return DtcLabDnaView(
        make=str(vin_dna.get("make") or ""),
        model=str(vin_dna.get("model") or ""),
        model_year=int(model_year),
        euro_emission_category=EuroEmissionCategory(euro if euro in _DTC_EURO else "UNKNOWN"),
        air_metering_strategy=DtcAirMeteringStrategy(air),
        resolved_horizon=ResolvedHorizon(horizon),
        emissions=DtcEmissionsView(has_catalyst=has_catalyst, egr_equipped=egr_equipped),
        # consumer: dtclab routing_tag_mapper HIGH-confidence CATALYST_HISTORY / EGR_HISTORY gates
        confidence=DtcVinConfidence(confidence),
    )


def _run_dtclab(dtc_inputs: dict[str, Any], vin_dna: dict[str, Any]) -> COMDTCLabPayload:
    """Run DTCLab with its DNA view and map its JSON boundary output into COMLab's mirror type."""
    with span("lab.dtclab.sanitize"):
        dtc_payload = DataFusionSanitizer(dna_view=_build_dtc_dna_view(vin_dna)).sanitize(
            raw_dtcs=_as_dict(dtc_inputs.get("raw_dtcs")),
            raw_freeze_frame=_as_dict(dtc_inputs.get("raw_freeze_frame")),
            raw_mode06=_as_dict(dtc_inputs.get("raw_mode06")),
            codes_cleared=bool(dtc_inputs.get("codes_cleared", False)),
            active_mil=bool(dtc_inputs.get("active_mil", False)),
            mil_flashing=bool(dtc_inputs.get("mil_flashing", False)),
        )
    return COMDTCLabPayload(**dtc_payload.model_dump(mode="json"))


def _build_fallback_vin_dna(vin: str) -> dict[str, Any]:
    """Build the MODERN/NONE fallback DNA dict for undecodable or absent VIN input."""
    safe_vin = vin if len(vin) == 17 else _FALLBACK_VIN
    return {
        "vin": safe_vin,
        "make": "",
        "model_year": None,
        "resolved_horizon": "HORIZON_MODERN",
        "cylinder_count": 4,
        "number_of_banks": 1,
        "engine_displacement_liters": 2.0,
        "euro_emission_category": "EURO_6",
        "fuel_delivery_type": "PORT_INJECTION",
        "induction_type": "NATURALLY_ASPIRATED",
        "air_metering_strategy": "MAP_ONLY_SPEED_DENSITY",
        "emissions": {
            "upstream_o2_type": "NARROWBAND_0_TO_1V",
            "downstream_trim_role": "NONE",
            "egr_equipped": False,
            "has_catalyst": True,
        },
        "confidence": "NONE",
    }


def _derive_horizon(euro: str) -> str:
    """Map Euro-emission category to COMLab horizon as a fallback-only translation."""
    if euro in {"EURO_1", "EURO_2"}:
        return "HORIZON_LEGACY"
    if euro in {"EURO_3", "EURO_4"}:
        return "HORIZON_ADAPTIVE"
    return "HORIZON_MODERN"


def _map_o2_sensor_type(vocab_o2: str) -> str:
    """Translate VINLab O2 vocabulary into OBDLab's local O2 sensor enum."""
    if vocab_o2 in {"WIDEBAND_AFR", "WIDEBAND_LAMBDA"}:
        return "WIDEBAND_LINEAR"
    if vocab_o2 == "NARROWBAND":
        return "NARROWBAND_0_TO_1V"
    return vocab_o2


def _enum_value(value: Any) -> Any:
    """Return enum wire value without importing the source enum class."""
    return getattr(value, "value", value)


def _with_user_dtcs(obd_inputs: dict[str, Any], dtc_inputs: Any) -> dict[str, Any]:
    """Return a copy of ``obd_inputs`` with the user's DTC codes as ``active_dtcs``.

    A non-empty ``active_dtcs`` already in ``obd_inputs`` wins unchanged. With no
    DTC input or no codes the copy gains no key (T-AUD-4h, F-C3-3).
    """
    out = dict(obd_inputs)
    if out.get("active_dtcs") or dtc_inputs is None:
        return out
    codes: list[str] = []
    for mode_codes in _as_dict(_as_dict(dtc_inputs).get("raw_dtcs")).values():
        for code in mode_codes or []:
            if code not in codes:
                codes.append(code)
    if codes:
        # consumer: OBDLab AnalyticsPreconditions gates 3-4 (O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE)
        out["active_dtcs"] = codes
    return out


def _as_dict(value: Any) -> dict[str, Any]:
    """Return ``value`` as a mutable dict, using empty dict for ``None``."""
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"expected dict-like payload, got {type(value).__name__}")
    return dict(value)
