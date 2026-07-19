"""Fault-Atlas Knowledge Graph types.

Pydantic models that mirror the on-disk KG schema (one ``kg/<family>.json``
file per fault family). Consumer: ``comlab.core.fault_atlas_kg.FaultAtlasKG``
(T-P3-1) — every field below has a named consumer in the KG provenance map
(``_comlab_skills/comlab-kg-provenance/SKILL.md`` §1).

Source: COMLab_LLD.md §3.4.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from comlab.schemas.vocabulary import FaultEnrichmentSeverity


# Mirror of response.FaultFamilyLit — duplicated here to keep ``kg.py`` free
# of response-layer imports. The 6 values are locked in COMLab_LLD.md §3.1.
FaultFamilyLit = Literal[
    "lean_condition",
    "rich_mixture",
    "misfire",
    "sensor_fault",
    "ecu_fault",
    "catalyst_failure",
    "exhaust_leak",
    "ignition_fault",
    "mechanical_wear",
    "cam_timing",
    "non_starter",
    "no_fault",
    "invalid_input",
    "vacuum_leak",
    "overheating",
    "charging_system",
]


class KGNode(BaseModel):
    """One fault entry. Mirrors a single object in any ``kg/*.json`` file.

    Consumer: ``fault_atlas_kg.FaultAtlasKG.resolve()`` projects this into
    ``DiagnosticVerdict`` + ``FaultEnrichment`` for the UI payload.

    Source: COMLab_LLD.md §3.4 KGNode.
    """

    fault_name: str  # lld: §3.4 KGNode.fault_name
    fault_family: FaultFamilyLit  # lld: §3.4 KGNode.fault_family
    component_group: str  # lld: §3.4 KGNode.component_group
    impacted_subsystems: list[str] = Field(min_length=1, max_length=8)  # lld: §3.4 KGNode.impacted_subsystems
    mechanical_failure_mode: str = Field(max_length=280)  # lld: §3.4 KGNode.mechanical_failure_mode
    ui_remediation_steps: list[str] = Field(min_length=1, max_length=8)  # lld: §3.4 KGNode.ui_remediation_steps
    differential_siblings: list[str] = Field(default_factory=list, max_length=5)  # lld: §3.3 Q1 ruling
    editor_severity_hint: Optional[FaultEnrichmentSeverity] = None  # lld: §3.4 KGNode.editor_severity_hint


class KGFile(BaseModel):
    """The full shape of one ``kg/<family>.json`` file.

    Six instances exist on disk (one per fault family). Loaded by
    ``FaultAtlasKG`` at COMLab startup and validated against
    ``comlab/config/kg/_kg_schema.json``.

    Source: COMLab_LLD.md §3.4 KGFile.
    """

    schema_version: str = Field(pattern=r"^\d+\.\d+$")  # lld: §3.4 KGFile.schema_version
    fault_family: FaultFamilyLit  # lld: §3.4 KGFile.fault_family
    nodes: dict[str, KGNode]  # lld: §3.4 KGFile.nodes — key = fault_id e.g. "ERR-RM-001"
