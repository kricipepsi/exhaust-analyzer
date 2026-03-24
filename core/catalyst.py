"""Catalyst efficiency calculation module."""

from typing import Dict, Optional, Tuple


def catalyst_efficiency(gas: Dict[str, float], config: Optional[Dict] = None) -> Tuple[int, str]:
    """
    Calculate catalyst oxidation efficiency.

    Args:
        gas: dict with keys 'co2', 'co', 'o2' (all volume %)
        config: optional catalyst_config dict from KB with co_o2_penalty and status_thresholds

    Returns:
        (efficiency_percent, status_string)

    Formula:
        efficiency = (co2 / (co2 + co + o2)) * 100

    Note: Efficiency is clamped to 0-100 range.
    """
    co2 = gas.get('co2', 0.0)
    co = gas.get('co', 0.0)
    o2 = gas.get('o2', 0.0)

    total = co2 + co + o2

    if total == 0:
        efficiency = 0
    else:
        efficiency = (co2 / total) * 100.0

    # Read penalty config or use defaults
    if config and 'co_o2_penalty' in config:
        p = config['co_o2_penalty']
        co_thresh = p.get('co_threshold', 0.5)
        o2_thresh = p.get('o2_threshold', 0.5)
        penalty = p.get('penalty', 15)
    else:
        co_thresh = 0.5
        o2_thresh = 0.5
        penalty = 15

    if co > co_thresh and o2 > o2_thresh:
        efficiency -= penalty

    # Clamp to 0-100
    efficiency = max(0.0, min(100.0, efficiency))

    eff_int = round(efficiency)

    # Read status thresholds or use defaults
    if config and 'status_thresholds' in config:
        t = config['status_thresholds']
        optimal_thresh = t.get('optimal', 95)
        marginal_thresh = t.get('marginal', 85)
    else:
        optimal_thresh = 95
        marginal_thresh = 85

    if eff_int > optimal_thresh:
        status = "Optimal"
    elif eff_int > marginal_thresh:
        status = "Aged/Marginal"
    else:
        status = "Failed"

    return eff_int, status
