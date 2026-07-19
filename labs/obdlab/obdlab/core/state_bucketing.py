"""Engine state bucketing per OBDLab_KG_Wiki.md §8.2.

Loads obd_translation_rules.yaml once at module import and evaluates
rules against sanitized PIDs + DNA view to determine RpmStateBucket.
"""

import logging
from pathlib import Path
from typing import Any

import yaml

from obdlab.schemas.dna_view import ObdLabDnaView
from obdlab.schemas.vocabulary import RpmStateBucket

logger = logging.getLogger(__name__)

_RULES_PATH = (
    Path(__file__).resolve().parent.parent
    / "config" / "obd_translation_rules.yaml"
)

_RULES = None
_BUCKETING = None


def _load_rules() -> None:
    global _RULES, _BUCKETING
    if _RULES is None:
        with open(_RULES_PATH, encoding="utf-8") as fh:
            _RULES = yaml.safe_load(fh)
        _BUCKETING = _RULES["state_bucketing_rules"]


def compute_bucket(
    sanitized_pids: dict[str, Any],
    dna_view: ObdLabDnaView | None = None,
) -> RpmStateBucket:
    """Determine engine state bucket from sanitized PIDs and optional DNA view.


    Priority-ordered evaluation per §8.2:
      1. COLD_OPEN_LOOP_INVALID — ECT < 75 °C (priority 1)
      2. STABILIZED_IDLE — RPM 650–900, load < 30%
      3. REGULATORY_HIGH_IDLE — RPM 2200–2800, load 15–40%  (§8.1)
      4. STRESS_IDLE — RPM ≈ stress_idle_rpm_target ±10%, load 10–60%
      Default: STABILIZED_IDLE (fallback when no rule matches)

    Args:
        sanitized_pids: dict with engine_rpm, coolant_temp_c,
            calculated_engine_load_pct.
        dna_view: typed DNA view (provides stress_idle_rpm_target).

    Returns:
        RpmStateBucket matching the first satisfied rule.
    """
    _load_rules()
    # Priority rules are evaluated first (sort by priority desc, then order)
    priority_rules = [r for r in _BUCKETING if "priority" in r]  # type: ignore
    other_rules = [r for r in _BUCKETING if "priority" not in r]  # type: ignore


    # Priority rules first (sorted by priority ascending — lower = higher priority)
    for rule in sorted(priority_rules, key=lambda r: r["priority"]):
        if _rule_matches(rule, sanitized_pids, dna_view):
            return RpmStateBucket(rule["bucket_id"])

    # Other rules in document order
    for rule in other_rules:
        if _rule_matches(rule, sanitized_pids, dna_view):
            return RpmStateBucket(rule["bucket_id"])

    # Fallback — wiki: §8
    logger.info(
        "bucket_fallback: no rule matched rpm=%s load=%s",
        sanitized_pids.get("engine_rpm"),
        sanitized_pids.get("calculated_engine_load_pct"),
    )
    return RpmStateBucket.STABILIZED_IDLE


def _rule_matches(
    rule: dict[str, Any],
    pids: dict[str, Any],
    dna_view: ObdLabDnaView | None,
) -> bool:
    """Check whether all conditions in a bucketing rule match."""
    for cond in rule["conditions"]:
        if not _condition_matches(cond, pids, dna_view):
            return False
    return True


def _condition_matches(
    cond: dict[str, Any],
    pids: dict[str, Any],
    dna_view: ObdLabDnaView | None,
) -> bool:
    """Evaluate a single condition against pids + dna_view."""
    node: str = cond["node"]
    operator: str = cond["operator"]
    raw_value = cond["value"]

    # Resolve the value — may be a literal or a DNA-view field reference
    if isinstance(raw_value, str) and raw_value in (
        "stress_idle_rpm_target",
    ):
        if dna_view is None:
            return False
        value = getattr(dna_view, raw_value, None)
        if value is None:
            return False
    else:
        value = raw_value

    actual = pids.get(node)
    if actual is None and node != "coolant_temp_c":
        return False

    if operator == "LESS_THAN":
        return actual is not None and actual < value

    if operator == "BETWEEN":
        lo, hi = value
        return actual is not None and lo <= actual <= hi

    if operator == "APPROXIMATELY":
        tolerance_pct = cond.get("tolerance_pct", 10)
        margin = value * (tolerance_pct / 100.0)
        return actual is not None and (value - margin) <= actual <= (value + margin)

    logger.warning("unknown_bucketing_operator: %s", operator)
    return False
