"""DNA-gated routing-tag engine.

map() — pure DTC-to-tag function. No external inputs beyond dna_view.
POA_HISTORY is no longer emitted here — COMLab fault_atlas_router injects
it directly when GASLab chemical_state == POA_SIGNATURE (T-FX-3).

Source: DTC_VOCABULARY.md §4 (17 tags + DNA gates), §15 (mapping table);
        dtclab-python §6.7 (DNA gate pattern).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

import yaml

from dtclab.schemas.dna_view import DtcLabDnaView, VinConfidence
from dtclab.schemas.vocabulary import DTCRoutingTag

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class _RoutingRule:
    """Single DTC-pattern → tag mapping with optional DNA gate."""

    patterns: tuple[re.Pattern[str], ...]
    tag: DTCRoutingTag
    dna_gate: str | None  # wiki: DTC_VOCABULARY.md §4.1


class RoutingTagMapper:
    """Maps confirmed DTC codes to DTCRoutingTag values with DNA-gate filtering.

    Constructor accepts the typed ``dna_view: DtcLabDnaView | None`` per the
    DNA-first arch (NewArchProposal_ImplementationPlan.md §4 Step 4).
    """

    def __init__(
        self, map_path: Path, dna_view: DtcLabDnaView | None
    ) -> None:
        self._dna_view = dna_view
        self._rules: list[_RoutingRule] = self._load_map(map_path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def map(self, confirmed_dtcs: list[str]) -> list[DTCRoutingTag]:
        """Return the deduplicated routing tags for *confirmed_dtcs*.

        Args:
            confirmed_dtcs: Validated DTC strings (already through the
                ingestion gate).  Each must match ``DTC_REGEX``.

        Returns:
            Deduplicated list of routing tags in enum-definition order.
        """
        tags: set[DTCRoutingTag] = set()

        for dtc in confirmed_dtcs:
            for rule in self._rules:
                if _matches_any(dtc, rule.patterns):
                    if self._gate_allows(rule.tag, rule.dna_gate):
                        tags.add(rule.tag)

        # Return in enum-definition order for determinism.
        all_tags = list(DTCRoutingTag)
        return [t for t in all_tags if t in tags]

    # ------------------------------------------------------------------
    # YAML loader
    # ------------------------------------------------------------------

    def _load_map(self, map_path: Path) -> list[_RoutingRule]:
        with open(map_path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        rules: list[_RoutingRule] = []
        for entry in data["entries"]:
            patterns = tuple(re.compile(p) for p in entry["patterns"])
            tag = DTCRoutingTag(entry["tag"])
            gate = entry.get("dna_gate")
            rules.append(_RoutingRule(patterns, tag, gate))
        return rules

    # ------------------------------------------------------------------
    # DNA gate — three-branch confidence pattern (§6.7)
    # ------------------------------------------------------------------

    def _gate_allows(self, tag: DTCRoutingTag, gate_name: str | None) -> bool:
        """Return True if *tag* is allowed through its DNA gate.

        No gate → always True.
        DNA-gated tags follow the three-branch pattern:
          - HIGH       → strict hardware-presence check
          - PARTIAL    → emit with downgrade log
          - NONE/None  → emit unconditionally (pre-DNA fallback)
        """
        if gate_name is None:
            return True  # wiki: DTC_VOCABULARY.md §4.1 — no gate

        if self._dna_view is None:
            return True  # wiki: DTC_VOCABULARY.md §14.3 — None ≡ NONE

        confidence = self._dna_view.confidence

        if confidence == VinConfidence.NONE:
            return True  # wiki: DTC_VOCABULARY.md §14.2 — pure DTC-pattern routing

        if confidence == VinConfidence.PARTIAL:
            logger.info(
                "dna_gate_downgraded: tag=%s gate=%s", tag.value, gate_name
            )
            return True  # wiki: DTC_VOCABULARY.md §4.1, §14.2 — advisory-emit

        # HIGH confidence — strict gate
        return self._check_high_confidence_gate(gate_name)

    def _check_high_confidence_gate(self, gate_name: str) -> bool:
        """Evaluate the strict hardware-presence check for HIGH confidence."""
        assert self._dna_view is not None  # guaranteed by _gate_allows caller
        emissions = self._dna_view.emissions

        if gate_name == "has_catalyst":
            return emissions.has_catalyst  # wiki: DTC_VOCABULARY.md §4.1
        if gate_name == "egr_equipped":
            return emissions.egr_equipped  # wiki: DTC_VOCABULARY.md §4.1


        # Unknown gate — defensive: emit (fail open).
        logger.warning("unknown_dna_gate: gate=%s", gate_name)
        return True


# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------


def _matches_any(dtc: str, patterns: tuple[re.Pattern[str], ...]) -> bool:
    """True if *dtc* matches at least one compiled regex in *patterns*."""
    return any(p.match(dtc) for p in patterns)
