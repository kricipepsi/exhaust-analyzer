"""Pipeline orchestrator — wires VL → M0 → M1/M2 → M3 → M4 → M5.

R1: pipeline order is fixed and non-negotiable.
R4: VL runs before any module receives data.
R7: resolve_conflicts() called only in M5 (ranker.py).
"""

from __future__ import annotations

import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml

from engine.v2.arbitrator import arbitrate
from engine.v2.digital_parser import parse_digital
from engine.v2.dna_core import load_dna
from engine.v2.gas_lab import analyse_gas
from engine.v2.input_model import DiagnosticInput, ValidatedInput
from engine.v2.kg_engine import score_faults, score_root_causes
from engine.v2.ranker import ResolutionContext, resolve_conflicts
from engine.v2.validation import validate

logger = logging.getLogger(__name__)

# ── schema loading ──────────────────────────────────────────────────────────

_SCHEMA_ROOT = Path(__file__).resolve().parent.parent.parent / "schema" / "v2"
_schema_cache: dict[str, dict | list] | None = None


def _load_schemas() -> dict[str, dict | list]:
    """Load faults, edges, and root_causes from schema YAML files.

    Cached at module level — files are read once per process lifetime.
    """
    global _schema_cache
    if _schema_cache is not None:
        return _schema_cache

    with (_SCHEMA_ROOT / "faults.yaml").open(encoding="utf-8") as f:
        faults: dict = yaml.safe_load(f)
    with (_SCHEMA_ROOT / "edges.yaml").open(encoding="utf-8") as f:
        edges_raw: dict = yaml.safe_load(f)
    with (_SCHEMA_ROOT / "root_causes.yaml").open(encoding="utf-8") as f:
        root_causes: dict = yaml.safe_load(f)

    _schema_cache = {
        "faults": faults,
        "edges": edges_raw.get("edges", []),
        "root_causes": root_causes,
    }
    return _schema_cache


# ── public API ──────────────────────────────────────────────────────────────


def diagnose(
    diagnostic_input: DiagnosticInput,
    *,
    db_path: Path | str | None = None,
    backward_chaining: bool = False,
) -> dict[str, Any]:
    """Run the full V2 diagnostic pipeline on a single case.

    Pipeline order (R1): VL → M0 → M1/M2 → M3 → M4 → M5.
    VL is mandatory and runs first (R4).

    Args:
        diagnostic_input: Raw diagnostic data.
        db_path: Path to vref.db; auto-resolved from repo layout if None.
        backward_chaining: If True, populate next_steps[] when state is
            insufficient_evidence.

    Returns:
        R9-shaped dict with state, primary, alternatives, and metadata.
    """
    validated = validate(diagnostic_input)

    if not validated.valid_channels:
        return _invalid_input_result(validated)

    dna = load_dna(validated, db_path)
    digital = parse_digital(validated, dna)
    gas = analyse_gas(validated, dna)
    evidence = arbitrate(validated, dna, digital, gas)

    schemas = _load_schemas()
    raw_probs = score_faults(
        evidence, dna, schemas["faults"], schemas["edges"]  # type: ignore[arg-type]
    )

    qualified_root_causes = score_root_causes(
        raw_probs, schemas["root_causes"]  # type: ignore[arg-type]
    )

    ctx = ResolutionContext(
        dtcs=list(diagnostic_input.dtcs),
        symptoms=list(evidence.active_symptoms),
        engine_state=dna.engine_state,
        evidence_layers_used=_derive_evidence_layers(diagnostic_input, validated),
        known_issues=list(dna.known_issues),
        backward_chaining=backward_chaining,
        perception_gap=evidence.perception_gap,
        validation_warnings=list(validated.warnings),
        cascading_consequences=list(evidence.cascading_consequences),
    )

    result = resolve_conflicts(
        raw_probs, ctx, schemas["faults"], qualified_root_causes  # type: ignore[arg-type]
    )
    return _result_to_dict(result)


# ── helpers ─────────────────────────────────────────────────────────────────


def _derive_evidence_layers(
    raw: DiagnosticInput, validated: ValidatedInput,
) -> list[str]:
    """Determine which evidence layers contributed usable data channels."""
    layers: list[str] = []
    if "gas_idle" in validated.valid_channels:
        layers.append("L1")
    if "gas_high" in validated.valid_channels:
        layers.append("L2")
    if validated.raw.obd is not None and "obd" in validated.valid_channels:
        layers.append("L3")
    if (
        validated.raw.freeze_frame is not None
        and "freeze_frame" in validated.valid_channels
    ):
        layers.append("L4")
    return layers


def _invalid_input_result(validated: ValidatedInput) -> dict[str, Any]:
    """Return the R9 invalid_input shape when VL rejects all channels."""
    return {
        "state": "invalid_input",
        "primary": None,
        "alternatives": [],
        "perception_gap": None,
        "validation_warnings": [asdict(w) for w in validated.warnings],
        "cascading_consequences": [],
        "confidence_ceiling": 0.0,
        "next_steps": [],
    }


def _result_to_dict(result: Any) -> dict[str, Any]:
    """Convert a RankedResult to a plain dict matching the R9 JSON shape."""
    return {
        "state": result.state,
        "primary": asdict(result.primary) if result.primary else None,
        "alternatives": [asdict(a) for a in result.alternatives],
        "perception_gap": asdict(result.perception_gap)
        if result.perception_gap
        else None,
        "validation_warnings": [asdict(w) for w in result.validation_warnings],
        "cascading_consequences": list(result.cascading_consequences),
        "confidence_ceiling": result.confidence_ceiling,
        "next_steps": list(result.next_steps),
    }
