"""SensorSignalTranslator — OBDLab pipeline orchestrator per §2.1.

Wires together the full §3–§12 processing chain:
  [1] PIDIngestionValidator     (§3)  → sanitized PIDs
  [2] State bucketing            (§8.2) → rpm_state_bucket (before semantic check — F-O7 fix)
  [3] SemanticConsistencyChecker (§4)  → thermal gate override
  [4] VEEngine.compute_ve        (§10) → ve_pct, maf_status, map_status, ve_validity
  [5] O2Normalizer.normalize     (§11) → normalized_obd_lambda, o2_mode, o2_failure_mode
  [6] TrimVectorAggregator       (§12) → total_trim_correction_delta
  [7] AnalyticsPreconditions     (§9)  → trim_analytics_gate
  ASSEMBLE OBDLivePayload        (§5)  → all analytics fields surfaced

Thermal gate at step [3] short-circuits steps [4]–[6] (analytics frozen)
but step [7] still runs to populate the trim_analytics_gate.
"""

import logging
from pathlib import Path
from typing import Any

from obdlab.core.analytics_preconditions import AnalyticsPreconditions
from obdlab.core.exceptions import PIDValidationError
from obdlab.core.maf_linearity import calculate_sensor_error_delta, calculate_w_theo
from obdlab.core.o2_normalizer import O2Normalizer
from obdlab.core.pid_ingestion_validator import PIDIngestionValidator
from obdlab.core.semantic_consistency_checker import SemanticConsistencyChecker
from obdlab.core.state_bucketing import compute_bucket
from obdlab.core.trim_vector_aggregator import TrimVectorAggregator
from obdlab.core.ve_engine import VEEngine
from obdlab.schemas.dna_view import AirMeteringStrategy, O2SensorType, ObdLabDnaView
from obdlab.schemas.payload import OBDLivePayload
from obdlab.schemas.vocabulary import (
    NodeMAFStatus,
    NodeMAPStatus,
    O2FailureMode,
    RpmStateBucket,
    VEValidity,
)

logger = logging.getLogger(__name__)

# Path to physical_sensor_bounds.json (same dir as obd_translation_rules.yaml)
_BOUNDS_PATH = (
    Path(__file__).resolve().parent.parent
    / "config" / "physical_sensor_bounds.json"
)


class LinearityAccumulator:
    """Accumulates stabilized and stress idle bands for two-point MAF/MAP linearity checks."""

    def __init__(self) -> None:
        self.stabilized_idle: tuple[float, float] | None = None
        self.stress_idle: tuple[float, float] | None = None


class SensorSignalTranslator:
    """OBDLab pipeline orchestrator — wires §3–§12 into one OBDLivePayload.

    Public entry point: translate().
    Exposed as the OBDLab public surface via obdlab/__init__.py.
    """

    def __init__(self) -> None:
        self._validator = PIDIngestionValidator(_BOUNDS_PATH)
        self._semantic = SemanticConsistencyChecker()
        self._ve_engine = VEEngine()
        self._o2_normalizer = O2Normalizer()
        self._analytics = AnalyticsPreconditions()

    def translate(
        self,
        raw_user_inputs: dict[str, Any],
        dna_view: ObdLabDnaView | None = None,
        accumulator: LinearityAccumulator | None = None,
    ) -> OBDLivePayload:
        """Run the full OBDLab pipeline and return an OBDLivePayload.

        Pipeline order per §2.1:
          1. PIDIngestionValidator — bounds check + unit normalisation (§3)
          2. State bucketing (§8.2) — computed before semantic check so
             Physics Gate 3 can read rpm_state_bucket (F-O7 fix).
          3. SemanticConsistencyChecker — Physics Gates + thermal gate (§4)
          4. VEEngine.compute_ve (§10) — frozen if thermal gate triggered
          5. O2Normalizer.normalize (§11) — frozen if thermal gate triggered
          6. TrimVectorAggregator (§12) — frozen if thermal gate triggered
          7. AnalyticsPreconditions (§9) — always runs

        Args:
            raw_user_inputs: dict of manually-entered PID values (may include
                alternate-unit fields like coolant_temp_f, manifold_vacuum_psi).
            dna_view: typed DNA view or None (defaults to DUAL_MAF_MAP CROSSCHECK
                VE routing + NARROWBAND O2 + confidence NONE equivalent).

        Returns:
            OBDLivePayload with all 31 canonical fields populated.

        Raises:
            PIDValidationError: bounds violation, DNA-RPM exceedance, or
                bank-2 null contract breach.
            SemanticConsistencyError: Physics Gate violation.
        """
        # [1] PID validation + unit normalisation (§3)
        sanitized = self._validator.validate_and_convert(
            raw_user_inputs, dna_view=dna_view,
        )

        # [2] State bucketing (§8.2) — compute early so Physics Gate 3
        # can read rpm_state_bucket (F-O7 fix). Thermal gate may override below.
        rpm_bucket = compute_bucket(sanitized, dna_view)
        sanitized["rpm_state_bucket"] = rpm_bucket.value

        # Store induction_type for VE fault classifier
        if dna_view is not None:
            sanitized["induction_type"] = dna_view.induction_type.value

        # [3] Semantic consistency — Physics Gates + thermal gate (§4)
        # Physics Gate 3 reads rpm_state_bucket from sanitized (now present).
        # Thermal gate may override the bucket (cold engine → COLD_OPEN_LOOP_INVALID).
        semantic_result = self._semantic.evaluate(sanitized, dna_view)
        thermal_override: RpmStateBucket | None = semantic_result[
            "rpm_state_bucket_override"
        ]
        engine_warmed: bool = semantic_result["engine_warmed"]
        gates_passed: list[str] = semantic_result["gates_passed"]

        # Apply thermal override to bucket if set
        if thermal_override is not None:
            rpm_bucket = thermal_override
            sanitized["rpm_state_bucket"] = rpm_bucket.value

        sanitized["engine_warmed"] = engine_warmed

        analytics_frozen = rpm_bucket == RpmStateBucket.COLD_OPEN_LOOP_INVALID

        # [4] VE computation (§10) — frozen if thermal gate triggered
        if analytics_frozen:
            ve_pct_val: float = 0.0  # wiki: §10 — 0.0 sentinel when analytics frozen; ve_validity==UNKNOWN suppresses router use
            maf_status = NodeMAFStatus.REAL_SENSOR_FEED
            map_status = NodeMAPStatus.REAL_SENSOR_FEED
            ve_validity = VEValidity.UNKNOWN
        else:
            ve_pct_raw, maf_status, map_status, ve_validity = (
                self._ve_engine.compute_ve(sanitized, rpm_bucket, dna_view)
            )
            ve_pct_val = ve_pct_raw or 0.0  # wiki: §10 — None guard; 0.0 sentinel when None

        # [5] O2 normalisation (§11) — frozen if thermal gate triggered
        if analytics_frozen:
            normalized_lambda = 1.0  # wiki: stoich default when frozen
            o2_failure_mode_result: O2FailureMode = O2FailureMode.NO_FAULT
        else:
            normalized_lambda, _o2_mode, o2_failure_mode_result = self._o2_normalizer.normalize(
                sanitized, dna_view,
            )

        # [6] Trim vector aggregation (§12) — frozen if thermal gate triggered
        if analytics_frozen:
            total_trim = 0.0
            total_trim_b2 = None  # wiki: §12.1 — frozen, no bank-2 computation
            per_bank_trim_delta = None
        else:
            total_trim, total_trim_b2, per_bank_trim_delta = TrimVectorAggregator.aggregate(sanitized)

        # [7] Analytics preconditions (§9) — always runs
        trim_gate = self._analytics.evaluate(
            sanitized,
            semantic_gates_passed=(len(gates_passed) == 3),
        )

        # Compute lambda_perception_delta under the Q4 guard
        lambda_perception_delta = None
        if dna_view is not None and dna_view.upstream_o2_type == O2SensorType.WIDEBAND_LINEAR:
            cmd_lambda = sanitized.get("commanded_equivalence_ratio")
            if cmd_lambda is not None:
                if not isinstance(cmd_lambda, (int, float)):
                    raise PIDValidationError(
                        f"commanded_equivalence_ratio must be numeric, got {type(cmd_lambda).__name__}"
                    )
                lambda_perception_delta = normalized_lambda - cmd_lambda

        # Compute w_theo and sensor_error_delta under the two-point guard
        w_theo = None
        sensor_error_delta = None

        strategy = (
            dna_view.air_metering_strategy if dna_view is not None
            else AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
        )
        displacement = dna_view.engine_displacement_liters if dna_view is not None else None

        if (
            not analytics_frozen
            and strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
            and displacement is not None
        ):
            maf_val = sanitized.get("mass_airflow_gps")
            map_val = sanitized.get("manifold_vacuum_kpa")
            rpm_val = sanitized.get("engine_rpm")
            iat_val = sanitized.get("intake_air_temp_c")

            if (
                maf_val is not None
                and map_val is not None
                and rpm_val is not None
                and rpm_val > 0
                and iat_val is not None
            ):
                eta_v = VEEngine._expected_ve(rpm_bucket, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
                if eta_v is not None:
                    curr_w_theo = calculate_w_theo(eta_v, displacement, map_val, rpm_val, iat_val)
                    if accumulator is not None:
                        if rpm_bucket == RpmStateBucket.STABILIZED_IDLE:
                            accumulator.stabilized_idle = (maf_val, curr_w_theo)
                        elif rpm_bucket == RpmStateBucket.STRESS_IDLE:
                            accumulator.stress_idle = (maf_val, curr_w_theo)

                        # Only emit if both bands have been captured
                        if accumulator.stabilized_idle is not None and accumulator.stress_idle is not None:
                            w_theo = curr_w_theo
                            maf_idle, w_theo_idle = accumulator.stabilized_idle
                            maf_stress, w_theo_stress = accumulator.stress_idle
                            sensor_error_delta = calculate_sensor_error_delta(
                                maf_stress, w_theo_stress, maf_idle, w_theo_idle
                            )

        # Assemble OBDLivePayload (§5)
        number_of_banks = sanitized.get("number_of_banks", 1)

        return OBDLivePayload(
            engine_warmed=engine_warmed,
            rpm_state_bucket=rpm_bucket,
            engine_rpm=sanitized["engine_rpm"],
            coolant_temp_c=sanitized["coolant_temp_c"],
            calculated_engine_load_pct=sanitized.get("calculated_engine_load_pct", 0.0),
            mass_airflow_gps=sanitized.get("mass_airflow_gps"),
            manifold_vacuum_kpa=sanitized.get("manifold_vacuum_kpa"),
            shrtft1=sanitized.get("shrtft1", 0.0),
            longft1=sanitized.get("longft1", 0.0),
            shrtft2=sanitized.get("shrtft2") if number_of_banks == 2 else None,
            longft2=sanitized.get("longft2") if number_of_banks == 2 else None,
            total_trim_correction_delta=total_trim,
            total_trim_correction_delta_b2=total_trim_b2,
            per_bank_trim_delta=per_bank_trim_delta,
            normalized_obd_lambda=normalized_lambda,
            lambda_perception_delta=lambda_perception_delta,
            ve_pct=ve_pct_val,
            ve_validity=ve_validity,
            trim_analytics_gate=trim_gate,
            maf_status=maf_status,
            map_status=map_status,
            o2_failure_mode=o2_failure_mode_result,
            fuel_system_status=sanitized["fuel_system_status"],
            freeze_frame_pids=sanitized.get("freeze_frame_pids", {}),
            intake_air_temp_c=sanitized.get("intake_air_temp_c", 25.0),
            throttle_pos_pct=sanitized.get("throttle_pos_pct", 0.0),
            control_module_voltage_v=sanitized.get("control_module_voltage_v", 14.0),
            per_cylinder_misfire_counts=sanitized.get("per_cylinder_misfire_counts"),
            ltft_cell_vector=sanitized.get("ltft_cell_vector"),
            w_theo=w_theo,
            sensor_error_delta=sensor_error_delta,
        )
