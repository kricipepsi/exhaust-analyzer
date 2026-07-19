"""Validation audit helpers for GASLab.

Pure functions used by the T-P5-1 validation suite: collision audit
(unresolved overlapping fault pairs) and vocabulary-threshold parsing
(wiki-drift guard). Source: ``GasLabIteration §5``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


# ---------------------------------------------------------------------------
# Collision audit
# ---------------------------------------------------------------------------


def _signatures_overlap(sig_a: dict, sig_b: dict) -> bool:
    """Return True if two fault signatures overlap in all six dimensions."""
    for gas in ("hc", "co", "co2", "o2", "nox", "lambda"):
        a_min = sig_a[gas]["min"]
        a_max = sig_a[gas]["max"]
        b_min = sig_b[gas]["min"]
        b_max = sig_b[gas]["max"]
        if a_min > b_max or b_min > a_max:
            return False
    return True


def _is_catch_all(entry: dict) -> bool:
    """Return True if the fault entry carries ``signature_type: catch_all``."""
    return entry.get("signature_type") == "catch_all"


def _has_resolution(entry: dict) -> bool:
    """Return True if the fault entry carries a differentiator or DNA gate."""
    if entry.get("dna_gate"):
        return True
    diff_edges = entry.get("differentiator_edges")
    return bool(diff_edges)


def find_uncovered_overlaps(ontology: dict) -> list[tuple[str, str]]:
    """Return fault pairs whose signatures overlap with no resolution path.

    A pair is "uncovered" when their per-gas bounds overlap in all six
    dimensions AND neither entry has a ``differentiator_edges`` list nor a
    ``dna_gate`` field.  SAMPLE_INVALID is excluded from the comparison
    because its catch-all signature would flag every other fault as overlapping.

    Source: ``GasLabIteration §5`` collision audit.
    """
    faults: dict[str, dict[str, Any]] = ontology.get("faults", {})
    names = sorted(faults.keys())
    uncovered: list[tuple[str, str]] = []

    for i, name_a in enumerate(names):
        if name_a == "SAMPLE_INVALID":
            continue
        entry_a = faults[name_a]
        if _is_catch_all(entry_a):
            continue
        sig_a = entry_a.get("signature")
        if sig_a is None:
            continue
        res_a = _has_resolution(entry_a)

        for j in range(i + 1, len(names)):
            name_b = names[j]
            if name_b == "SAMPLE_INVALID":
                continue
            entry_b = faults[name_b]
            if _is_catch_all(entry_b):
                continue
            sig_b = entry_b.get("signature")
            if sig_b is None:
                continue
            res_b = _has_resolution(entry_b)

            if res_a or res_b:
                continue

            if _signatures_overlap(sig_a, sig_b):
                uncovered.append((name_a, name_b))

    return uncovered


# ---------------------------------------------------------------------------
# Wiki-drift guard
# ---------------------------------------------------------------------------

# Map GAS_VOCABULARY §10 subsection numbers to the short gas keys used in
# gas_lab_ontology.yaml and the rule engine.  Source: GAS_VOCABULARY §10.
_SECTION_TO_GAS: dict[str, str] = {
    "10.1": "hc",              # vocab: GAS_VOCABULARY §10.1
    "10.2": "co",              # vocab: GAS_VOCABULARY §10.2
    "10.3": "co2",             # vocab: GAS_VOCABULARY §10.3
    "10.4": "o2",              # vocab: GAS_VOCABULARY §10.4
    "10.5": "nox",             # vocab: GAS_VOCABULARY §10.5
    "10.6": "volumetric_sum",  # vocab: GAS_VOCABULARY §10.6
    "10.7": "lambda",          # vocab: GAS_VOCABULARY §10.7
}


def parse_vocabulary_thresholds(vocab_md: Path) -> dict[str, dict[str, dict[str, float]]]:
    """Parse per-gas threshold tables from ``GAS_VOCABULARY.md §10``.

    Returns a dict keyed by short gas name (``"hc"``, ``"co"``, …) whose
    values are tier-name → ``{min, max}`` mappings.  Only ``min`` and/or
    ``max`` are present when the tier defines that bound; open-ended tiers
    omit the missing key.

    The function extracts YAML blocks from the markdown fenced sections
    beneath each ``### 10.N`` heading.  If the markdown table format
    changes, this function raises ``ValueError`` — the wiki-drift test
    fails loudly, which is the intended behaviour.
    """
    text = vocab_md.read_text(encoding="utf-8")
    result: dict[str, dict[str, dict[str, float]]] = {}

    for section_num, gas_key in _SECTION_TO_GAS.items():
        pattern = re.compile(
            rf"###\s+{re.escape(section_num)}\s.*?\n\n```yaml\n(.*?)```",
            re.DOTALL,
        )
        match = pattern.search(text)
        if match is None:
            raise ValueError(
                f"Could not find §{section_num} YAML block in {vocab_md}. "
                f"Has the markdown table format changed?"
            )
        yaml_text = match.group(1)
        parsed: dict[str, dict[str, dict[str, float]]] = yaml.safe_load(yaml_text)
        result[gas_key] = parsed.get("thresholds", {})

    return result
