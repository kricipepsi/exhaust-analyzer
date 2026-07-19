"""OrchestratorFinalUIOutput — the single JSON contract for outbound data.

This is the boundary between ComLab and the UI (mobile app, web app, or
downstream service). One scannable, sanitized payload per diagnostic session.

Source: OrchestratorLabBP.md lines 1213-1253; COMLab_LLD.md §3.3.

Status: v0.1 skeleton + T-P1-1 KG-projection extensions
(``DifferentialSiblingOut``, ``FaultEnrichment``, ``LabRoutingDirectiveOut``;
``DiagnosticVerdict`` and ``ExecutionMeta`` extended).
"""

from __future__ import annotations

from typing import Literal, Optional
from pydantic import BaseModel, Field, UUID4

from comlab.schemas.ingestion import UserInputEchoAudit
from comlab.schemas.vocabulary import (
    FaultEnrichmentSeverity,
    LabRoutingDirectiveReason,
)


HorizonLit = Literal["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"]
DegradationLit = Literal["FULL_FUSION", "GAS_DOMINANT", "SINGLE_POINT", "FATAL_INCOMPLETE"]  # lld: §3.3 DegradationLit; SINGLE_POINT added by T-COMV2-DELTA-1 (wiki: delta-relations/01)
ConfidenceLit = Literal["HIGH_ASSURANCE", "DEGRADED_ASSURANCE", "LOW_CERTAINTY"]
VinConfidenceLit = Literal["HIGH", "PARTIAL", "NONE"]  # lld: §3.3 VinConfidenceLit
SeverityLit = Literal[
    "CRITICAL_IMMEDIATE_STOP",
    "WARNING_DEGRADED_PERFORMANCE",
    "OPTIMAL_HEALTH",
]
FaultFamilyLit = Literal[  # lld: §3.3 FaultFamilyLit
    "lean_condition",
    "rich_mixture",
    "misfire",
    "sensor_fault",
    "ecu_fault",
    "catalyst_failure",
    "exhaust_leak",
    "ignition_fault",
    "mechanical_wear",  # lld: §3.1 — T-P6-2c KG family
    "cam_timing",  # lld: §3.1 — T-P6-2c KG family
    "non_starter",  # lld: §3.1 — T-P6-2d KG family
    "no_fault",
    "invalid_input",  # lld: §3.3 — T-P6-5b-2 REG-V2 family
    "vacuum_leak",  # lld: §3.3 — T-P6-5b-2 REG-V2 family
    "overheating",  # lld: §3.3 — T-P6-5b-2 REG-V2 family
    "charging_system",  # lld: §3.3 — T-P6-5b-2 REG-V2 family
]


class LabRoutingDirectiveOut(BaseModel):
    """Surfaced in ``execution_meta`` per LLD §3.3 Q6 ruling.

    Consumer: PRD §5.6 grey-out panel.
    """

    suppress_gaslab: bool  # lld: §3.3 LabRoutingDirectiveOut
    suppress_obd_live_pids: bool  # lld: §3.3 LabRoutingDirectiveOut
    suppress_mode06_ui: bool  # lld: §3.3 LabRoutingDirectiveOut
    cold_start_mode: bool  # lld: §3.3 LabRoutingDirectiveOut
    reasons: list[LabRoutingDirectiveReason] = Field(default_factory=list)  # lld: §3.3 LabRoutingDirectiveOut.reasons


class ExecutionMeta(BaseModel):
    """Execution metadata surfaced beside the verdict.

    Consumer: UI header/status panel; source: LLD §3.3 execution envelope.
    """
    resolved_horizon: HorizonLit
    degradation_mode: DegradationLit
    processing_confidence_rating: ConfidenceLit
    vin_confidence: VinConfidenceLit  # lld: §3.3 ExecutionMeta.vin_confidence
    lab_routing_directive: LabRoutingDirectiveOut  # lld: §3.3 ExecutionMeta.lab_routing_directive — Q6


class DifferentialSiblingOut(BaseModel):
    """Up to 5 total per ``diagnostic_verdict``, per LLD §3.3 Q1.

    Consumer: PRD §5.3 runner-up panel.
    """

    fault_id: str  # lld: §3.3 DifferentialSiblingOut.fault_id
    fault_name: str  # lld: §3.3 DifferentialSiblingOut.fault_name
    fault_family: FaultFamilyLit  # lld: §3.3 DifferentialSiblingOut.fault_family — top-3 scorer/UI consumer
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)  # lld: §3.3 DifferentialSiblingOut.confidence_score
    source: Literal["runtime", "editor_curated"]  # lld: §3.3 DifferentialSiblingOut.source — UI badge


class DiagnosticVerdict(BaseModel):
    """Primary diagnostic verdict emitted to the UI.

    Consumer: PRD §5.2 verdict card and fault-atlas routing trace.
    """
    is_fault_detected: bool
    fault_code: str  # fault_id
    fault_name: str
    fault_family: FaultFamilyLit  # lld: §3.3 DiagnosticVerdict.fault_family
    display_headline: str = Field(max_length=140)  # lld: §3.3 DiagnosticVerdict.display_headline
    confidence_score: float = Field(ge=0.0, le=1.0)  # lld: §3.3 DiagnosticVerdict.confidence_score
    actionable_remediation: str
    differential_siblings: list[DifferentialSiblingOut] = Field(default_factory=list, max_length=5)  # lld: §3.3 Q1 ruling
    abstained: bool = False
    abstain_reason: Optional[Literal["floor", "margin"]] = None


class FaultEnrichment(BaseModel):
    """KG node values projected into the response payload.

    Consumer: PRD §5.2; populated by Stage C enrichment from
    ``FaultAtlasKG.resolve()`` (T-P3-1).
    """

    component_group: str  # lld: §3.3 FaultEnrichment.component_group
    impacted_subsystems: list[str]  # lld: §3.3 FaultEnrichment.impacted_subsystems
    mechanical_failure_mode: str = Field(max_length=280)  # lld: §3.3 FaultEnrichment.mechanical_failure_mode
    ui_remediation_steps: list[str] = Field(min_length=1, max_length=8)  # lld: §3.3 FaultEnrichment.ui_remediation_steps
    editor_severity_hint: Optional[FaultEnrichmentSeverity] = None  # lld: §3.3 FaultEnrichment.editor_severity_hint


class PerformanceAnalytics(BaseModel):
    """Power and perception analytics emitted with the verdict.

    Consumer: PRD §5.4 analytics panel; source: LLD §3.3 response schema.
    """
    kinetic_power_loss_pct: float = Field(..., ge=0.0, le=100.0)
    catalyst_efficiency_index_pct: Optional[float] = Field(default=None, ge=0.0, le=100.0)  # lld: §7 — None when downstream_o2_present == False
    lambda_perception_delta: float  # lld: §3.3 — signed: OBD lambda - GASLab lambda; consumer: UI Lambda Δ metric + sensor-bias classifier
    o2_sensor_bias_verdict: Optional[str] = None  # lld: §3.3 — O2_SENSOR_BIASED_LOW / O2_SENSOR_BIASED_HIGH / None; consumer: fault-atlas router Stage B + UI perception panel
    severity_level: SeverityLit


class OrchestratorFinalUIOutput(BaseModel):
    """The single JSON payload delivered to the front-end UI."""

    session_id: UUID4
    execution_meta: ExecutionMeta
    diagnostic_verdict: DiagnosticVerdict
    performance_analytics: PerformanceAnalytics
    fault_enrichment: FaultEnrichment  # lld: §3.3 — Stage C KG enrichment
    user_input_echo_audit: UserInputEchoAudit  # lld: §3.3 — pass-through from assembler
