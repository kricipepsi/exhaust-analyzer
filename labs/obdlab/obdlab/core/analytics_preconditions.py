"""Analytics precondition gate per OBDLab_KG_Wiki.md §9.

Evaluates the 8 precondition gates and returns the first failing
TrimAnalyticsGate enum value, or VALID if all pass.

DTC codes are checked as opaque token membership — no regex parsing.
Source: OBDLab_KG_Wiki.md §9.
"""

import logging
from typing import Any

from obdlab.schemas.vocabulary import FuelSystemStatus, TrimAnalyticsGate

logger = logging.getLogger(__name__)

# wiki: §9 — DTC ranges for O2 sensor faults (P0130–P0161)
O2_FAULT_DTCS: frozenset[str] = frozenset([
    "P0130", "P0131", "P0132", "P0133", "P0134",
    "P0135", "P0136", "P0137", "P0138", "P0139",
    "P0140", "P0141", "P0142", "P0143", "P0144",
    "P0145", "P0146", "P0147", "P0148", "P0149",
    "P0150", "P0151", "P0152", "P0153", "P0154",
    "P0155", "P0156", "P0157", "P0158", "P0159",
    "P0160", "P0161",
])

# wiki: §9 — DTC ranges for CKP/CMP sensor faults
CKP_CMP_FAULT_DTCS: frozenset[str] = frozenset([
    "P0335",  # wiki: §9 — Crankshaft Position Sensor circuit
    "P0340",  # wiki: §9 — Camshaft Position Sensor circuit
])

# wiki: §9 — coolant temp threshold for engine-warm gate (°C)
ECT_WARM_THRESHOLD = 70  # wiki: §9

# wiki: §9 — throttle position threshold for WOT gate (%)
WOT_THROTTLE_THRESHOLD = 90  # wiki: §9


class AnalyticsPreconditions:
    """Evaluate the 8 analytics-precondition gates per §9.

    Returns the first gate that fails in priority order, or VALID.
    All DTC membership checks use opaque token set intersection — no regex.
    """

    @staticmethod
    def evaluate(
        sanitized_pids: dict[str, Any],
        semantic_gates_passed: bool = True,
    ) -> TrimAnalyticsGate:
        """Evaluate preconditions and return TrimAnalyticsGate.

        Args:
            sanitized_pids: PID dict with coolant_temp_c, fuel_sys_status,
                active_dtcs (list[str] or None), drive_cycles_since_clear,
                throttle_pos, dfco_active.
            semantic_gates_passed: True if Physics Gates 1–4 all pass (§4).

        Returns:
            TrimAnalyticsGate.VALID if all preconditions pass, otherwise
            the first failing gate in priority order.
        """
        # Gate 1 — wiki: §9 — Engine warm (coolant_temp_c >= 70)
        ect = sanitized_pids.get("coolant_temp_c")
        if ect is None or ect < ECT_WARM_THRESHOLD:
            return TrimAnalyticsGate.ENGINE_COLD

        # Gate 2 — wiki: §9 — Closed loop
        fuel_status = sanitized_pids.get("fuel_system_status")
        if fuel_status is None:
            fuel_status = sanitized_pids.get("fuel_sys_status")
        fuel_status = FuelSystemStatus.from_wire(fuel_status)
        if fuel_status != FuelSystemStatus.CL:
            return TrimAnalyticsGate.OPEN_LOOP

        # Gate 3 — wiki: §9 — No O₂ fault (opaque DTC membership check)
        active_dtcs: list[str] = sanitized_pids.get("active_dtcs") or []
        if O2_FAULT_DTCS.intersection(active_dtcs):
            return TrimAnalyticsGate.O2_FAULT_ACTIVE

        # Gate 4 — wiki: §9 — No CKP/CMP fault
        if CKP_CMP_FAULT_DTCS.intersection(active_dtcs):
            return TrimAnalyticsGate.CKP_CMP_FAULT_ACTIVE

        # Gate 5 — wiki: §9 — Codes not recently cleared
        drive_cycles = sanitized_pids.get("drive_cycles_since_clear", 0)
        if drive_cycles is None or drive_cycles < 1:
            return TrimAnalyticsGate.CODES_RECENTLY_CLEARED

        # Gate 6 — wiki: §9 — Not WOT
        throttle = sanitized_pids.get("throttle_pos")
        if throttle is not None and throttle >= WOT_THROTTLE_THRESHOLD:
            return TrimAnalyticsGate.WOT_ACTIVE

        # Gate 7 — wiki: §9 — Not DFCO
        if sanitized_pids.get("dfco_active") is True:
            return TrimAnalyticsGate.DFCO_ACTIVE

        # Gate 8 — wiki: §9 — Semantic gates pass
        if not semantic_gates_passed:
            return TrimAnalyticsGate.SEMANTIC_ERROR

        return TrimAnalyticsGate.VALID
