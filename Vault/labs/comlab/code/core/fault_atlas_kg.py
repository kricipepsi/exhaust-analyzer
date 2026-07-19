"""Fault-Atlas Knowledge Graph loader.

Loads all 6 ``comlab/config/kg/*.json`` files once at process start,
validates them against the Pydantic schema, and exposes an O(1) ``resolve()``
lookup by ``fault_id``.

Source: COMLab_LLD.md §6.5.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from comlab.schemas.kg import KGFile, KGNode

logger = logging.getLogger(__name__)

KG_DIRNAME: str = "kg"  # lld: §6.5 — config subdirectory name

__all__ = ["FaultAtlasKG"]


class FaultAtlasKG:
    """Boot-time KG loader. Loads all family files once, validates, indexes by ID.

    No lazy loading, no file I/O in ``resolve()``, no hardware precondition
    filtering (that is Stage B's responsibility).
    """

    _ALIAS_MAP: dict[str, str] = {
        "ERR-E1-M032": "ERR-LC-005",  # lld: §6.5 — legacy registry alias → canonical KG ID
        "ERR-E2-I104": "ERR-MF-001",  # lld: §6.5
        "ERR-E3-F501": "ERR-RM-005",  # lld: §6.5
    }

    def __init__(self, kg_dir: str | Path | None = None) -> None:
        """Load every ``kg/*.json`` file, validate, and index by ``fault_id``.

        Args:
            kg_dir: Override path to the ``kg/`` directory.  When ``None``
                (default), resolves to ``<package_root>/config/kg/`` relative
                to this file.
        """
        if kg_dir is None:
            kg_dir = Path(__file__).parent.parent / "config" / KG_DIRNAME
        self._kg_dir = Path(kg_dir)
        self._nodes: dict[str, KGNode] = {}
        self._file_count: int = 0  # lld: §6.5 — loaded file counter

        self._load_all()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def resolve(self, fault_id: str) -> KGNode:
        """Return the ``KGNode`` for *fault_id*.

        Performs a two-step lookup: first consults ``_ALIAS_MAP`` to resolve
        legacy registry IDs (ERR-E1-M032, etc.) to their canonical KG IDs,
        then does a direct dict lookup.

        Args:
            fault_id: e.g. ``"ERR-RM-001"`` or ``"OPTIMAL_HEALTH"``.

        Returns:
            The matching ``KGNode``.

        Raises:
            KeyError: If *fault_id* (and any alias target) is not in the
                loaded index.
        """
        resolved_id = self._ALIAS_MAP.get(fault_id, fault_id)
        try:
            return self._nodes[resolved_id]
        except KeyError:
            raise KeyError(
                f"Unknown fault_id {fault_id!r} — "
                f"not found in any of the {self._file_count} loaded KG files"
            ) from None

    @property
    def node_count(self) -> int:
        """Total number of indexed nodes (should be 30 for the full dataset)."""
        return len(self._nodes)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _load_all(self) -> None:
        """Iterate ``*.json`` files in *kg_dir*, load and index each."""
        json_files = sorted(
            p for p in self._kg_dir.glob("*.json")
            if not p.name.startswith("_")  # lld: §6.5 — skip _kg_schema.json and friends
        )
        if not json_files:
            raise FileNotFoundError(
                f"No .json files found in KG directory: {self._kg_dir}"
            )

        for path in json_files:
            self._load_one(path)

        logger.info(
            "FaultAtlasKG loaded %d nodes from %d file(s) in %s",
            len(self._nodes),
            self._file_count,
            self._kg_dir,
        )

    def _load_one(self, path: Path) -> None:
        """Load and validate a single family JSON file, merging its nodes."""
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Invalid JSON in KG file {path}: {exc}"
            ) from exc

        try:
            kg_file = KGFile.model_validate(raw)
        except Exception as exc:
            raise ValueError(
                f"Schema validation failed for KG file {path}: {exc}"
            ) from exc

        family = kg_file.fault_family
        for node_id, node in kg_file.nodes.items():
            if node_id in self._nodes:
                raise ValueError(
                    f"Duplicate fault_id {node_id!r} in {path} "
                    f"(already loaded from another KG file)"
                )
            # lld: §6.5 — every node's fault_family must match its file's family
            if node.fault_family != family:
                raise ValueError(
                    f"fault_id {node_id!r} in {path} has fault_family "
                    f"{node.fault_family!r} but the file declares family "
                    f"{family!r}"
                )
            self._nodes[node_id] = node

        self._file_count += 1
