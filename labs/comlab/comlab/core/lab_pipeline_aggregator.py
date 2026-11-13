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
    CompensatedRichResult,
    PerceptionContradictionResult,
    detect as detect_perception_contradiction,
    detect_compensated_rich,
    select_perception_lambda,
)
from comlab.core.symptom_router import route_symptom
from comlab.schemas.ingestion import (
    OrchestratorInboundRequest,
    SessionMetadata,
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
_TIER_HIGH_MIN = 0.80  # wiki: 09 §CONCEPT_CONF_TIER — HIGH_ASSURANCE posterior ≳ 0.80 (T-COMA-21)
_TIER_DEGRADED_MIN = 0.50  # wiki: 09 §CONCEPT_CONF_TIER — DEGRADED_ASSURANCE 0.50-0.80 (T-COMA-21)
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
    def _map_degradation(
        directive: LabRoutingDirective, request: OrchestratorInboundRequest
    ) -> DegradationLit:
        """GAS_DOMINANT when GASLab or OBD is suppressed or OBD live data is absent, else FULL_FUSION.

        wiki 07 CONCEPT_DEGRADATION_MODE. The test reads gas and OBD only; DTC output does not change the mode.

        T-COMA-21 (F-C1-11). SINGLE_POINT stays on the delta engine's own result (COMLab_BDD deviation table).
        """
        if directive.suppress_gaslab or directive.suppress_obd_live_pids or request.obd_live_data is None:
            return "GAS_DOMINANT"  # lld: §3.3 DegradationLit
        return "FULL_FUSION"  # lld: §3.3 DegradationLit

    # ------------------------------------------------------------------
    # Verdict score → Confidence tier (wiki 09 CONCEPT_CONF_TIER)
    # ------------------------------------------------------------------

    @staticmethod
    def _confidence_for(
        verdict: DiagnosticVerdict,
        reasons: list[LabRoutingDirectiveReason],
        degradation_mode: DegradationLit,
    ) -> ConfidenceLit:
        """The band of the verdict's own score, never the era (T-COMA-21, F-C1-12).

        LOW_CERTAINTY when the verdict abstained or the gas sample is INVALID (T-COMA-17); GAS_DOMINANT caps the
        tier at DEGRADED_ASSURANCE (wiki 07 "confidence ceiling applies").
        """
        if verdict.abstained or LabRoutingDirectiveReason.GAS_SAMPLE_INVALID in reasons:
            return "LOW_CERTAINTY"
        if verdict.confidence_score < _TIER_DEGRADED_MIN:
            return "LOW_CERTAINTY"
        if verdict.confidence_score < _TIER_HIGH_MIN or degradation_mode == "GAS_DOMINANT":
            return "DEGRADED_ASSURANCE"
        return "HIGH_ASSURANCE"

    @staticmethod
    def _gas_sample_reasons(
        request: OrchestratorInboundRequest, directive: LabRoutingDirective
    ) -> list[LabRoutingDirectiveReason]:
        """The gas-sample qualifier for an unsuppressed GASLab sample (T-COMA-17, ADR-0007 amendment).

        An INVALID sample stays scored (fatal gates off) but is flagged; EXTERNAL_O2_SUSPECT warns.
        """
        gas = request.gas_lab_output
        if directive.suppress_gaslab or gas is None:
            return []
        validity = gas.sample_validity
        if validity == "INVALID":
            return [LabRoutingDirectiveReason.GAS_SAMPLE_INVALID]
        if validity == "EXTERNAL_O2_SUSPECT":
            return [LabRoutingDirectiveReason.GAS_SAMPLE_O2_SUSPECT]
        return []

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
        return self.abort_incomplete(
            request.metadata,
            abort.error_code,
            abort.ui_remediation_message,
            horizon=horizon,
            echo=request.user_input_echo_audit,
        )

    def abort_incomplete(
        self,
        metadata: SessionMetadata,
        error_code: str,
        message: str,
        *,
        horizon: Horizon | None = None,
        echo: UserInputEchoAudit | None = None,
    ) -> OrchestratorFinalUIOutput:
        """Return a ``FATAL_INCOMPLETE`` output for a session whose input is incomplete.

        Needs only the session *metadata*, so a caller can abort before it can
        build an ``OrchestratorInboundRequest`` (for example when the gas
        readings that ``gas_lab_output`` requires are missing). The verdict is
        ``fault_family="invalid_input"`` with *error_code* as the fault code and
        *message* as the remediation. *horizon* defaults to
        ``metadata.resolved_horizon``, resolved as ``process()`` does. *echo*
        is carried verbatim; ``None`` gives the empty sentinel.
        # wiki: vocabulary.py:571, lld: §6.3
        """
        meta = metadata
        if horizon is None:
            try:
                horizon = Horizon(meta.resolved_horizon)
            except ValueError:
                horizon = Horizon.MODERN  # lld: §6.1 — safe default, as in process()
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
            fault_code=error_code,
            fault_name=f"Fatal Abort: {error_code}",
            fault_family="invalid_input",  # wiki: response.py:47 — session aborted on invalid/missing input
            display_headline=message[:_FATAL_DISPLAY_HEADLINE_LIMIT],
            confidence_score=0.0,
            actionable_remediation=message,
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
            mechanical_failure_mode=message[:_FATAL_FAILURE_MODE_LIMIT],
            ui_remediation_steps=[message],
        )

        if echo is None:
            echo = UserInputEchoAudit(
                submitted_at=datetime.now(timezone.utc),  # lld: §3.3 sentinel
                groups=[],  # lld: §3.3 sentinel
            )

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
            if validity not in ("VALID", "BORDERLINE", "EXTERNAL_O2_SUSPECT"):  # O2-suspect: warn but continue (F-C1-14)
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
        gas = request.gas_lab_output
        perception_lambda = select_perception_lambda(
            normalized_obd_lambda=obd_lambda_val,
            lambda_measured=gas.lambda_measured if gas is not None else None,
        )
        # T-COMA-2: a non-starter without gas has no chemistry truth, so both lambda detectors are inert.
        perception_result = PerceptionContradictionResult(
            lambda_perception_delta=0.0, bias_verdict=None, guard_suppressed=False, qualifiers=()
        ) if gas is None else detect_perception_contradiction(
            lambda_chem=gas.lambda_chem,
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
        compensated_rich_result = CompensatedRichResult(
            is_compensated_rich=False, confidence=0.0
        ) if gas is None else detect_compensated_rich(
            lambda_chem=gas.lambda_chem,
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
        degradation_mode: DegradationLit = self._map_degradation(directive, request)

        # -- Build shared Stage A outputs (used by both paths) --
        reasons_out: list[LabRoutingDirectiveReason] = list(directive.reasons)
        reasons_out += self._gas_sample_reasons(request, directive)
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
                processing_confidence_rating=self._confidence_for(
                    router_output.diagnostic_verdict, reasons_out, degradation_mode
                ),
                vin_confidence=request.metadata.vin_confidence.value,  # lld: §3.3; F-C1-9 (T-COMA-8): echoed
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
            processing_confidence_rating=self._confidence_for(verdict, reasons_out, degradation_mode),
            vin_confidence=request.metadata.vin_confidence.value,  # lld: §3.3; F-C1-9 (T-COMA-8): echoed
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
                "fuel_delivery_type": request.metadata.fuel_delivery_type,  # consumer: integration_shim._hardware_gate
            },
            "gas_lab_output": (
                request.gas_lab_output.model_dump() if request.gas_lab_output is not None else None
            ),
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

