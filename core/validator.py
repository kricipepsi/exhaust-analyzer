"""Input validation and gatekeeper checks for exhaust gas data."""

import json
from pathlib import Path
from typing import Dict, Tuple, Optional

# Load master knowledge base
_KNOWLEDGE_BASE_PATH = Path(__file__).parent.parent / "data" / "expanded_knowledge_base.json"


def _load_validation_ranges() -> Dict:
    """Load validation gatekeeper ranges from expanded knowledge base."""
    try:
        with open(_KNOWLEDGE_BASE_PATH, 'r') as f:
            kb = json.load(f)
        return kb.get('validation_gatekeeper', {}).get('ranges', {})
    except Exception as e:
        # Fallback to permissive ranges if file not found
        return {
            "co": {"min": 0.0, "max": 10.0},
            "hc": {"min": 0, "max": 25000},
            "co2": {"min": 6.0, "max": 16.5},
            "o2": {"min": 0.0, "max": 20.0},
            "lambda": {"min": 0.6, "max": 1.5},
            "nox": {"min": 0, "max": 5000}
        }


def validate_gas_data(gas: dict) -> tuple[bool, str]:
    """Check gatekeeper ranges."""
    ranges = _load_validation_ranges()
    for param, config in ranges.items():
        if param in gas:
            value = gas[param]
            min_val = config.get('min', float('-inf'))
            max_val = config.get('max', float('inf'))
            error_msg = config.get('error', f'{param} out of range')
            if value < min_val or value > max_val:
                return False, f"{error_msg}: {param}={value} (valid range: {min_val}-{max_val})"
    return True, "All parameters within valid ranges"


def check_probe_placement(co: float, co2: float, threshold: float = 12.0) -> Optional[dict]:
    total = co + co2
    if total < threshold:
        return {
            "warning": "Probe placement issue",
            "message": f"Total CO+CO2 ({total:.2f}%) is below {threshold}% threshold. Check probe depth and exhaust integrity.",
            "co": co,
            "co2": co2,
            "total": total
        }
    return None
