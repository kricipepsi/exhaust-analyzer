"""Ontology loader — reads ``gas_lab_ontology.yaml`` into a typed dict.

Pure function: one file read, no side effects.  Raises ``OntologyLoadError``
on parse or schema failure so callers never receive a broken ontology.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class OntologyLoadError(RuntimeError):
    """Raised when ``gas_lab_ontology.yaml`` cannot be parsed or is malformed."""

    def __init__(self, path: Path, detail: str = "") -> None:
        self.path = path
        msg = f"ontology unreadable: {path}"
        if detail:
            msg = f"{msg} — {detail}"
        super().__init__(msg)


def load_ontology(path: Path | None = None) -> dict[str, Any]:
    """Load and return the GASLab declarative ontology.

    Args:
        path: Path to ``gas_lab_ontology.yaml``.  Defaults to
            ``gaslab/data/gas_lab_ontology.yaml`` relative to this file.

    Returns:
        Parsed ontology dict with top-level keys ``version``, ``scope``,
        ``validity_gates``, ``reasoning_grammar``, ``faults``.

    Raises:
        OntologyLoadError: If the file is missing, unparseable, or missing
            required top-level keys.
    """
    if path is None:
        path = Path(__file__).resolve().parent / "data" / "gas_lab_ontology.yaml"

    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OntologyLoadError(path, f"cannot read file: {exc}") from exc

    try:
        ontology: dict[str, Any] = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise OntologyLoadError(path, f"YAML parse failed: {exc}") from exc

    if not isinstance(ontology, dict):
        raise OntologyLoadError(path, f"expected a mapping at top level, got {type(ontology).__name__}")

    for key in ("version", "scope", "validity_gates", "reasoning_grammar", "faults"):
        if key not in ontology:
            raise OntologyLoadError(path, f"missing required top-level key: {key!r}")

    return ontology
