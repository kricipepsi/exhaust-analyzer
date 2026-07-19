"""Script 2: Lab Pipeline Aggregator — the data harvester + safety gate.

Sole ingestion point for ComLab. Validates the inbound JSON payload (the four
upstream labs' outputs + metadata) against the Pydantic ``OrchestratorInboundRequest``
schema, then runs the Fallback Error Execution Tree to either:

  - mark the session FATAL_INCOMPLETE (abort cleanly), or
  - mark the session GAS_DOMINANT (degrade gracefully — older car missing trims), or
  - mark the session FULL_FUSION (proceed with all sensors).

Output is a sanitized dict that Script 3 (fault_atlas_router) consumes.

Sub-components (per OrchestratorLabBP.md component tree, line 1396):
    - Pydantic_Ingestion_Gatekeeper     schema + DTC regex validation
    - Fallback_Error_Execution_Tree     missing-data classification
    - Graceful_Degradation_Handler      mode flag + permissive-vs-strict rigor
    - Lab_Data_Synchronizer             final merge into a single runtime payload

Status: v0.2 — Stage C KG enrichment wired (T-P4-2).
"""

from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from comlab.analytics.power_loss_analytics import PowerLossAnalytics
from comlab.core.fault_atlas_kg import FaultAtlasKG
from comlab.core.fault_atlas_router import FaultAtlasRouter
from comlab.core.horizon_context_injector import HorizonContextInjector
from comlab.core.perception_contradiction import (
    detect as detect_perception_contradiction,
    detect_compensated_rich,
    select_perception_lambda,
)
from comlab.core.symptom_router import route_symptom
from comlab.schemas.ingestion import (
    OrchestratorInboundRequest,
    UserInputEchoAudit,
)
from comlab.schemas.response import (
    ConfidenceLit,
    DegradationLit,
    DiagnosticVerdict,
    ExecutionMeta,
    FaultEnrichment,
    HorizonLit,
    LabRoutingDirectiveOut,
    OrchestratorFinalUIOutput,
    PerformanceAnalytics,
)
from comlab.schemas.vocabulary import (
    DegradationMode,
    Horizon,
    LabRoutingDirective,
    LabRoutingDirectiveReason,
    VinConfidence,
)

__all__ = ["AggregatorAbort", "LabPipelineAggregator"]

logger = logging.getLogger(__name__)

# lld: §6.4 — default config paths relative to this file
_PKG_ROOT = Path(__file__).parent.parent
_DEFAULT_KG_DIR = _PKG_ROOT / "config" / "kg"
_DEFAULT_MASKS_YAML = _PKG_ROOT / "config" / "eras_sensitivity_masks.yaml"
_DEFAULT_REGISTRY_PATH = _PKG_ROOT / "config" / "global_fault_registry.json"
_RICH_DTC_CODES: frozenset[str] = frozenset({"P0172", "P0175"})  # wiki: DTC_VOCABULARY §8
_FATAL_DISPLAY_HEADLINE_LIMIT = 140  # lld: §3.3 DiagnosticVerdict.display_headline
_FATAL_FAILURE_MODE_LIMIT = 280  # lld: §3.3 FaultEnrichment.mechanical_failure_mode
_OVERRIDE_PATH_CONFIDENCE_SCORE = 0.5  # lld: §6.3 — nominal; Stage B refines
_OVERRIDE_PATH_KINETIC_POWER_LOSS_PCT = 0.0  # lld: §6.4 — stubbed override path
_OVERRIDE_PATH_CATALYST_EFFICIENCY_PCT = 100.0  # lld: §6.4 — stubbed override path
_DEFAULT_LAMBDA_TOLERANCE = 0.05  # lld: §6.1 — mask fallback when lambda_tolerance absent
_ENGINE_WARMED_REMEDIATION_TEMP_C = 75  # wiki: 02_lab_input_contract.md §2 — warmed gate


class AggregatorAbort(RuntimeError):
    """Raised when the fallback tree determines the session cannot continue.

    Carries the ``error_code`` and ``ui_remediation_message`` so the UI can
    show the technician an actionable next step.
    """

    def __init__(self, error_code: str, ui_remediation_message: str) -> None:
        super().__init__(f"{error_code}: {ui_remediation_message}")
        self.error_code = error_code
        self.ui_remediation_message = ui_remediation_message


class LabPipelineAggregator:
    """Sub-Components: Pydantic_Ingestion_Gatekeeper + Lab_Data_Synchronizer + ...

    T-P4-2: Stage C KG enrichment wired into ``process()``.
    """

    def __init__(
        self,
        kg_dir: str | Path | None = None,
        masks_yaml_path: str | Path | None = None,
        registry_path: str | Path | None = None,
        use_v2_registry: bool | None = None,  # consumer: FaultAtlasRouter v1/v2 path gate
        enable_delta: bool = False,  # consumer: FaultAtlasRouter Phase 5 delta input
        enable_delta_v2: bool = False,  # consumer: v2 scored_rules re-rank
        enable_vpwr_gate: bool = False,  # consumer: perception-contradiction rail pre-check
        enable_fatal_gates: bool = False,  # consumer: Stage-A fatal gates (ERR-ABORT-00x → FATAL_INCOMPLETE)
    ) -> None:
        """Create aggregator with KG loader, horizon injector, and fault router.

        All paths default to ``comlab/config/`` subdirectories when None.

        *use_v2_registry* (None = resolve from ``USE_V2_REGISTRY`` env var,
        defaulting to True / REG-V2) is the single default-resolution point
        for the registry-selection env var (T-W-ARCH-6).
        """
        if use_v2_registry is None:
            use_v2_registry = os.environ.get("USE_V2_REGISTRY", "1") == "1"
        self._enable_vpwr_gate: bool = enable_vpwr_gate
        self._enable_fatal_gates: bool = enable_fatal_gates
        self._kg = FaultAtlasKG(kg_dir if kg_dir is not None else _DEFAULT_KG_DIR)
        self._injector = HorizonContextInjector(
            masks_yaml_path if masks_yaml_path is not None else _DEFAULT_MASKS_YAML
        )
        self._analytics = PowerLossAnalytics()
        self._router = FaultAtlasRouter(
            registry_path if registry_path is not None else _DEFAULT_REGISTRY_PATH,
            self._kg,
            self._analytics,
            use_v2_registry=use_v2_registry,
            enable_delta=enable_delta,
            enable_delta_v2=enable_delta_v2,
        )

    # ------------------------------------------------------------------
    # Stage C — KG enrichment  (lld: §6.3)
    # ------------------------------------------------------------------

    def _stage_c_enrich(self, fault_code: str) -> FaultEnrichment:
        """Resolve *fault_code* via ``FaultAtlasKG`` and project into
        ``FaultEnrichment``.

        Degraded mode: if *fault_code* is unknown, log the error and return a
        ``FaultEnrichment`` with empty strings and an error note.
        """
        try:
            node = self._kg.resolve(fault_code)
        except KeyError:
            logger.error(
                "Stage C: unknown fault_code %r — emitting degraded enrichment",
                fault_code,
            )
            return FaultEnrichment(
                component_group="",  # lld: §6.3 degraded
                impacted_subsystems=[],  # lld: §6.3 degraded
                mechanical_failure_mode="",  # lld: §6.3 degraded
                ui_remediation_steps=[
                    f"Unknown fault code: {fault_code}. Manual diagnosis required."
                ],  # lld: §6.3 degraded
                editor_severity_hint=None,
            )
        return FaultEnrichment(
            component_group=node.component_group,  # lld: §6.3
            impacted_subsystems=node.impacted_subsystems,  # lld: §6.3
            mechanical_failure_mode=node.mechanical_failure_mode,  # lld: §6.3
            ui_remediation_steps=node.ui_remediation_steps,  # lld: §6.3
            editor_severity_hint=node.editor_severity_hint,  # lld: §6.3
        )

    # ------------------------------------------------------------------
    # Echo pass-through  (lld: §3.3)
    # ------------------------------------------------------------------

    @staticmethod
    def _echo_pass_through(request: OrchestratorInboundRequest) -> UserInputEchoAudit:
        """Carry ``user_input_echo_audit`` through verbatim, or emit sentinel."""
        if request.user_input_echo_audit is not None:
            return request.user_input_echo_audit
        return UserInputEchoAudit(
            submitted_at=datetime.now(timezone.utc),  # lld: §3.3 sentinel
            groups=[],  # lld: §3.3 sentinel
        )

    # ------------------------------------------------------------------
    # Degradation mode mapping
    # ------------------------------------------------------------------

    @staticmethod
    def _map_degradation(directive: LabRoutingDirective) -> DegradationLit:
        """Map symptom-router directive flags to degradation mode literal."""
        if directive.suppress_gaslab:
            return "GAS_DOMINANT"  # lld: §3.3 DegradationLit
        return "FULL_FUSION"  # lld: §3.3 DegradationLit

    # ------------------------------------------------------------------
    # Horizon → Confidence heuristic
    # ------------------------------------------------------------------

    @staticmethod
    def _confidence_from_horizon(horizon: Horizon) -> ConfidenceLit:
        """Heuristic confidence from resolved horizon.  # lld: §6.3"""
        if horizon == Horizon.MODERN:
            return "HIGH_ASSURANCE"
        if horizon == Horizon.ADAPTIVE:
            return "DEGRADED_ASSURANCE"
        return "LOW_CERTAINTY"

    # ------------------------------------------------------------------
    # Era threshold helpers
    # ------------------------------------------------------------------

    def _lambda_tolerance_for_horizon(self, horizon: Horizon) -> float:
        """Read ``lambda_tolerance`` from the active era's sensitivity mask.

        Source: lld: §6.1 — eras_sensitivity_masks.yaml.
        """
        masks = self._injector._load_masks()  # noqa: SLF001 — owned component
        horizon_key = horizon.value
        gas_thresholds = (
            masks.get("horizons", {}).get(horizon_key, {}).get("gas_lab_thresholds", {})
        )
        return float(gas_thresholds.get("lambda_tolerance", _DEFAULT_LAMBDA_TOLERANCE))

    # ------------------------------------------------------------------
    # Stage A fatal gates  (lld: §6.3)
    # ------------------------------------------------------------------

    MIN_SUPPORTED_SCHEMA_VERSION: str = "1.0"  # lld: §6.3

    def check_schema_version(self, schema_version: str) -> None:
        """Raise ``AggregatorAbort(ERR-ABORT-005)`` when *schema_version*
        is below ``MIN_SUPPORTED_SCHEMA_VERSION``.  # lld: §10
        """
        def _parse(v: str) -> tuple[int, ...]:
            return tuple(int(x) for x in v.split("."))

        if _parse(schema_version) < _parse(self.MIN_SUPPORTED_SCHEMA_VERSION):
            raise AggregatorAbort(
                "ERR-ABORT-005",
                "Schema version is too old. "
                "Update the client to a version that supports schema v"
                f"{self.MIN_SUPPORTED_SCHEMA_VERSION} or later.",
            )

    # ------------------------------------------------------------------
    # Fatal-gate abort → FATAL_INCOMPLETE output builder
    # ------------------------------------------------------------------

    def _build_fatal_incomplete_output(
        self,
        request: OrchestratorInboundRequest,
        abort: AggregatorAbort,
        horizon: Horizon,
    ) -> OrchestratorFinalUIOutput:
        """Build a ``FATAL_INCOMPLETE`` output when a Stage-A fatal gate aborts the session.

        Constructs the minimal required ``OrchestratorFinalUIOutput`` fields
        without running Stage B–E.  # wiki: vocabulary.py:571, lld: §6.3
        """
        meta = request.metadata
        horizon_lit: HorizonLit = horizon.value  # type: ignore[assignment]

        exec_meta = ExecutionMeta(
            resolved_horizon=horizon_lit,
            degradation_mode="FATAL_INCOMPLETE",  # wiki: vocabulary.py:571
            processing_confidence_rating="LOW_CERTAINTY",  # aborted — no confidence
            vin_confidence=meta.vin_confidence.value,  # VinConfidence is StrEnum
            lab_routing_directive=LabRoutingDirectiveOut(
                suppress_gaslab=False,
                suppress_obd_live_pids=False,
                suppress_mode06_ui=False,
                cold_start_mode=False,
                reasons=[],
            ),
        )

        verdict = DiagnosticVerdict(
            is_fault_detected=False,
            fault_code=abort.error_code,
            fault_name=f"Fatal Abort: {abort.error_code}",
            fault_family="invalid_input",  # wiki: response.py:47 — session aborted on invalid/missing input
            display_headline=abort.ui_remediation_message[:_FATAL_DISPLAY_HEADLINE_LIMIT],
            confidence_score=0.0,
            actionable_remediation=abort.ui_remediation_message,
            differential_siblings=[],
        )

        perf = PerformanceAnalytics(
            kinetic_power_loss_pct=0.0,
            catalyst_efficiency_index_pct=None,
            lambda_perception_delta=0.0,
            o2_sensor_bias_verdict=None,
            severity_level="OPTIMAL_HEALTH",
        )

        enrichment = FaultEnrichment(
            component_group="n/a — session aborted",
            impacted_subsystems=[],
            mechanical_failure_mode=abort.ui_remediation_message[:_FATAL_FAILURE_MODE_LIMIT],
            ui_remediation_steps=[abort.ui_remediation_message],
        )

        echo = self._echo_pass_through(request)

        return OrchestratorFinalUIOutput(
            session_id=meta.session_id,
            execution_meta=exec_meta,
            diagnostic_verdict=verdict,
            performance_analytics=perf,
            fault_enrichment=enrichment,
            user_input_echo_audit=echo,
        )

    def run_fatal_gates_and_routing(
        self,
        request: OrchestratorInboundRequest,
    ) -> LabRoutingDirective:
        """Run Stage A fatal gates honouring suppression flags.

        Checks sample_validity (ERR-ABORT-001), engine_warmed (ERR-ABORT-002),
        vin_confidence (ERR-ABORT-004), and schema_version (ERR-ABORT-005).
        Returns the routing directive on success.  # lld: §6.3, §10
        """
        directive = route_symptom(request.symptom_dna)

        # ERR-ABORT-001: sample_validity != VALID (when GASLab not suppressed)
        if not directive.suppress_gaslab:
            validity = request.gas_lab_output.sample_validity
            if validity not in ("VALID", "BORDERLINE"):
                raise AggregatorAbort(
                    "ERR-ABORT-001",
                    "Gas sample is invalid. Check probe connections, "
                    "verify sample line integrity, and re-sample.",
                )

        # ERR-ABORT-002: engine not warmed (when OBD not suppressed)
        if not directive.suppress_obd_live_pids and request.obd_live_data is not None:
            if not request.obd_live_data.engine_warmed:
                raise AggregatorAbort(
                    "ERR-ABORT-002",
                    "Engine not at operating temperature "
                    f"(ECT < {_ENGINE_WARMED_REMEDIATION_TEMP_C} °C). "
                    "Warm engine to full operating temperature and re-test.",
                )

        # ERR-ABORT-004: VIN confidence == NONE
        if request.metadata.vin_confidence == VinConfidence.NONE:
            raise AggregatorAbort(
                "ERR-ABORT-004",
                "VIN could not be decoded. "
                "Enter vehicle details manually before proceeding.",
            )

        # ERR-ABORT-005: schema_version < MIN_SUPPORTED
        self.check_schema_version(request.metadata.schema_version)

        return directive

    # ------------------------------------------------------------------
    # Pipeline entry point
    # ------------------------------------------------------------------

    def process(
        self,
        request: OrchestratorInboundRequest,
        fault_code: str | None = None,
    ) -> OrchestratorFinalUIOutput:
        """Run the full pipeline on *request* and return the final UI payload.

        Stages: A (horizon context) → symptom routing → B (fault resolution)
        → C (KG enrichment) → differential siblings → D (power loss, stubbed).

        *fault_code* override is a test hook for when Stage B is not yet
        implemented.  In production it is resolved by ``FaultAtlasRouter``.
        """
        meta = request.metadata

        # -- Stage A: horizon context (pre-resolved by DNALab) --
        try:
            horizon = Horizon(meta.resolved_horizon)
        except ValueError:
            horizon = Horizon.MODERN  # lld: §6.1 — safe default
        horizon_lit: HorizonLit = horizon.value  # type: ignore[assignment]

        # -- Perception-contradiction detector (runs before Stage B) --
        # WHY: Stage B needs the sensor-bias evidence before router pruning;
        # OBD lambda is the ECU perception channel, with GAS λ only as no-OBD fallback.
        # wiki: Sensor_Fault_Family.md §Lambda Truth filter
        # lld: T-FX-6 — data_flow_report.md §4 OBDLab OUT
        # T-FX-7: OBD lambda wins when present; fall back to GASLab measured λ for no-OBD cars
        era_tolerance = self._lambda_tolerance_for_horizon(horizon)
        obd_lambda_val = (
            request.obd_live_data.normalized_obd_lambda
            if request.obd_live_data is not None
            else None
        )
        perception_lambda = select_perception_lambda(
            normalized_obd_lambda=obd_lambda_val,
            lambda_measured=request.gas_lab_output.lambda_measured,
        )
        perception_result = detect_perception_contradiction(
            lambda_chem=request.gas_lab_output.lambda_chem,
            normalized_obd_lambda=perception_lambda,
            era_lambda_tolerance=era_tolerance,
            downstream_trim_role=request.downstream_trim_role,
            has_catalyst=request.has_catalyst,
            control_module_voltage_v=(
                request.obd_live_data.control_module_voltage_v
                if request.obd_live_data is not None
                else None
            ),
            enable_vpwr_gate=self._enable_vpwr_gate,
        )

        # -- Compensated-rich detector (runs after perception contradiction) --
        # WHY: trim+DTC evidence can expose an ECU-masked fuel leak even when
        # gas chemistry remains near stoich.
        # wiki: T-P6-6a
        rich_dtc_present = bool(
            _RICH_DTC_CODES
            & set(
                request.dtc_lab_output.confirmed_dtcs
                if request.dtc_lab_output is not None
                else []
            )
        )
        obd_trim_delta = (
            request.obd_live_data.total_trim_correction_delta
            if request.obd_live_data is not None
            else 0.0
        )
        compensated_rich_result = detect_compensated_rich(
            lambda_chem=request.gas_lab_output.lambda_chem,
            total_trim_correction_delta=obd_trim_delta,
            obd_lambda=perception_lambda,
            era_lambda_tolerance=era_tolerance,
            rich_dtc_present=rich_dtc_present,
        )

        # -- Symptom routing (with optional Stage-A fatal gates) --
        # WHY: fatal gates are default-off so legacy flag-off verdicts stay byte-identical.
        if self._enable_fatal_gates:
            try:
                directive = self.run_fatal_gates_and_routing(request)
            except AggregatorAbort as abort:
                return self._build_fatal_incomplete_output(request, abort, horizon)
        else:
            directive = route_symptom(request.symptom_dna)
        degradation_mode: DegradationLit = self._map_degradation(directive)

        # -- Build shared Stage A outputs (used by both paths) --
        reasons_out: list[LabRoutingDirectiveReason] = list(directive.reasons)
        bias_verdict_value: str | None = (
            perception_result.bias_verdict.value
            if perception_result.bias_verdict is not None
            else None
        )

        # -- Stage B→E: normal path — delegate to FaultAtlasRouter (lld: §6.4) --
        if fault_code is None:
            sanitized = self._build_sanitized_payload(
                request, directive, horizon, degradation_mode
            )
            sanitized["compensated_rich_result"] = compensated_rich_result  # wiki: T-P6-6c
            sanitized["perception_result"] = perception_result  # wiki: T-P6-11 — sensor_fault routing
            sanitized["era_lambda_tolerance"] = era_tolerance
            # consumer: fault_atlas_router ECU fuse — T-COMV2-ECU-FUSE-1
            router_output = self._router.route(sanitized)

            # Enrich execution_meta with aggregator Stage A data —
            # the router produces a skeletal ExecutionMeta; replace with
            # the aggregator's fully-resolved version (lld: §6.3)
            exec_meta = ExecutionMeta(
                resolved_horizon=horizon_lit,
                degradation_mode=degradation_mode,
                processing_confidence_rating=self._confidence_from_horizon(horizon),
                vin_confidence="HIGH",  # lld: §3.3 — nominal; Literal "HIGH"
                lab_routing_directive=LabRoutingDirectiveOut(
                    suppress_gaslab=directive.suppress_gaslab,
                    suppress_obd_live_pids=directive.suppress_obd_live_pids,
                    suppress_mode06_ui=directive.suppress_mode06_ui,
                    cold_start_mode=directive.cold_start_mode,
                    reasons=reasons_out,
                ),
            )

            # Merge perception data into router's performance analytics —
            # the router owns kinetic/catalyst/severity; the aggregator
            # owns lambda perception delta + O2 bias verdict (Stage A)
            router_perf = router_output.performance_analytics
            perf = PerformanceAnalytics(
                kinetic_power_loss_pct=router_perf.kinetic_power_loss_pct,
                catalyst_efficiency_index_pct=router_perf.catalyst_efficiency_index_pct,
                lambda_perception_delta=perception_result.lambda_perception_delta,
                o2_sensor_bias_verdict=bias_verdict_value,
                severity_level=router_perf.severity_level,
            )

            echo = self._echo_pass_through(request)

            return OrchestratorFinalUIOutput(
                session_id=meta.session_id,
                execution_meta=exec_meta,
                diagnostic_verdict=router_output.diagnostic_verdict,
                performance_analytics=perf,
                fault_enrichment=router_output.fault_enrichment,
                user_input_echo_audit=echo,
            )

        # -- fault_code override path (test hook) --
        fc: str = fault_code  # type: ignore[assignment]

        # -- Stage C: KG enrichment --
        enrichment = self._stage_c_enrich(fc)

        # -- KG node for verdict + differential siblings --
        try:
            kg_node = self._kg.resolve(fc)
            siblings = self._router.build_differential_siblings(kg_node)
            verdict_fault_name = kg_node.fault_name
            verdict_fault_family = kg_node.fault_family
        except KeyError:
            siblings = []
            verdict_fault_name = fc
            verdict_fault_family = "no_fault"  # type: ignore[assignment]

        is_fault = fc != "OPTIMAL_HEALTH"
        verdict = DiagnosticVerdict(
            is_fault_detected=is_fault,
            fault_code=fc,
            fault_name=verdict_fault_name,
            fault_family=verdict_fault_family,  # type: ignore[arg-type]
            display_headline=verdict_fault_name if is_fault else "No fault detected",
            confidence_score=_OVERRIDE_PATH_CONFIDENCE_SCORE,
            actionable_remediation=(
                enrichment.ui_remediation_steps[0]
                if enrichment.ui_remediation_steps
                else ""
            ),
            differential_siblings=siblings,
        )

        # -- Execution meta --
        execution_meta = ExecutionMeta(
            resolved_horizon=horizon_lit,
            degradation_mode=degradation_mode,
            processing_confidence_rating=self._confidence_from_horizon(horizon),
            vin_confidence="HIGH",  # lld: §3.3 — nominal; Literal "HIGH"
            lab_routing_directive=LabRoutingDirectiveOut(
                suppress_gaslab=directive.suppress_gaslab,
                suppress_obd_live_pids=directive.suppress_obd_live_pids,
                suppress_mode06_ui=directive.suppress_mode06_ui,
                cold_start_mode=directive.cold_start_mode,
                reasons=reasons_out,
            ),
        )

        # -- Performance analytics (Stage D stubbed for override path) --
        perf = PerformanceAnalytics(
            kinetic_power_loss_pct=_OVERRIDE_PATH_KINETIC_POWER_LOSS_PCT,
            catalyst_efficiency_index_pct=_OVERRIDE_PATH_CATALYST_EFFICIENCY_PCT,
            lambda_perception_delta=perception_result.lambda_perception_delta,
            o2_sensor_bias_verdict=bias_verdict_value,
            severity_level=(  # type: ignore[arg-type]
                "CRITICAL_IMMEDIATE_STOP" if is_fault else "OPTIMAL_HEALTH"
            ),
        )

        # -- Echo pass-through --
        echo = self._echo_pass_through(request)

        return OrchestratorFinalUIOutput(
            session_id=meta.session_id,
            execution_meta=execution_meta,
            diagnostic_verdict=verdict,
            performance_analytics=perf,
            fault_enrichment=enrichment,
            user_input_echo_audit=echo,
        )

    # ------------------------------------------------------------------
    # Legacy / compatibility (keep existing signatures)
    # ------------------------------------------------------------------

    def _build_sanitized_payload(
        self,
        request: OrchestratorInboundRequest,
        directive: LabRoutingDirective,
        horizon: Horizon,
        degradation_mode: DegradationLit,
    ) -> dict[str, Any]:
        """Build the sanitized dict payload for the fault-atlas router.

        Includes the ``request`` object, horizon context, degradation mode,
        and routing directive so ``FaultAtlasRouter.route()`` has everything
        it needs for triage + assembly (lld: §6.4).
        """
        return {
            "request": request,
            "horizon_ctx": horizon.value,
            "degradation_mode": degradation_mode,
            "metadata": {
                "session_id": str(request.metadata.session_id),
                "resolved_horizon": request.metadata.resolved_horizon,
                "cylinder_count": request.metadata.cylinder_count,
                "degradation_mode": degradation_mode,
            },
            "gas_lab_output": request.gas_lab_output.model_dump(),
            "obd_live_data": request.obd_live_data.model_dump() if request.obd_live_data is not None else None,
            "dtc_lab_output": request.dtc_lab_output.model_dump() if request.dtc_lab_output is not None else None,
            "routing_directive": directive,
        }

    def validate_payload(self, raw_input: dict[str, Any]) -> dict[str, Any]:
        """Sub-Component: Pydantic_Ingestion_Gatekeeper.

        Parse + validate ``raw_input`` against ``OrchestratorInboundRequest``.
        Returns the validated payload as a plain dict (``model_dump()``).
        Raises ``pydantic.ValidationError`` on schema violation.
        """
        request = OrchestratorInboundRequest.model_validate(raw_input)
        return request.model_dump()

    def run_fallback_tree(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Sub-Components: Fallback_Error_Execution_Tree + Graceful_Degradation_Handler.

        Non-starter short-circuit: if symptom routing suppresses GASLab,
        absent GASLab data is expected — do not raise AggregatorAbort.
        Full fallback tree (BP lines 1086-1162) deferred to phase 3.
        """
        directive = route_symptom(payload.get("symptom_dna", {}))

        if directive.suppress_gaslab:
            payload["degradation_mode"] = DegradationMode.GAS_DOMINANT
            payload["routing_directive"] = directive
            return payload

        raise NotImplementedError(
            "run_fallback_tree: full fallback tree not yet implemented (phase 3). "
            "Non-starter path handled above."
        )

    def sanitize_and_aggregate(self, raw_input: dict[str, Any]) -> dict[str, Any]:
        """End-to-end Script 2 entrypoint.

        validate_payload -> run_fallback_tree -> return sanitized payload.
        """
        payload = self.validate_payload(raw_input)
        return self.run_fallback_tree(payload)
