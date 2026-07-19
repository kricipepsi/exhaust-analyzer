"""registry — v2 rule-data workstream (self-contained)

This package imports only its own modules + stdlib + Pydantic v2.
No imports from any lab (gaslab, obdlab, dtclab, dnalab),
from comlab, or from 4DLabWired.

COMLab reads registry artefacts at integration time (REG-V2-INTEGRATE);
the registry never reads COMLab.

wiki: labs/comlab/registry/docs/REGISTRY_START_HERE.md
"""

from registry.integration_shim import (
    RegistryV2Router,
    render_ranked_rule,
    route_case,
    route_case_with_diagnostics,
)
from registry.schema_v2 import (
    ChemistryState,
    DTCRoutingTag,
    EvidenceTier,
    FaultFamily,
    Rule,
    RuleSet,
)

__all__ = [
    "RegistryV2Router",
    "render_ranked_rule",
    "route_case",
    "route_case_with_diagnostics",
    "ChemistryState",
    "DTCRoutingTag",
    "EvidenceTier",
    "FaultFamily",
    "Rule",
    "RuleSet",
]

