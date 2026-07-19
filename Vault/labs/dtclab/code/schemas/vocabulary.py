"""DTCLab canonical vocabulary — StrEnums, DTC_REGEX, and confidence weights.

All values sourced verbatim from docs/wiki/DTC_VOCABULARY.md (split wiki contract
surface). The archived monolithic wiki at docs/_archive/ and the legacy BP at
bp/DTCLabBP.md are explicitly not sources of truth.
"""

from enum import StrEnum
from typing import Final, Mapping

# =============================================================================
# Enums
# =============================================================================


class DTCRoutingTag(StrEnum):
    """Fault-family routing hint derived from confirmed DTCs.

    Source: DTC_VOCABULARY.md §4 (17-value canonical form).
    """

    LEAN_HISTORY = "LEAN_HISTORY"  # wiki: §4 — P0171, P0174
    RICH_HISTORY = "RICH_HISTORY"  # wiki: §4 — P0172, P0175
    MISFIRE_HISTORY = "MISFIRE_HISTORY"  # wiki: §4 — P0300–P0312
    CATALYST_HISTORY = "CATALYST_HISTORY"  # wiki: §4 — P0420, P0430 (DNA-gated)
    EGR_HISTORY = "EGR_HISTORY"  # wiki: §4 — P0400–P0409 (DNA-gated)
    O2_HISTORY = "O2_HISTORY"  # wiki: §4 — P0130–P0161
    INJECTOR_HISTORY = "INJECTOR_HISTORY"  # wiki: §4 — P0200–P0212
    VVT_HISTORY = "VVT_HISTORY"  # wiki: §4 — P0010–P0023
    EVAP_HISTORY = "EVAP_HISTORY"  # wiki: §4 — P0440–P0459
    THERMAL_HISTORY = "THERMAL_HISTORY"  # wiki: §4 — P0116–P0128
    ECU_INTERNAL_HISTORY = "ECU_INTERNAL_HISTORY"  # wiki: §4 — P0600–P0699
    POA_HISTORY = "POA_HISTORY"  # wiki: §4 — gas-chem signature only; no direct DTC
    IDLE_CONTROL_HISTORY = "IDLE_CONTROL_HISTORY"  # wiki: §4 — P0505–P0511

    BOOST_HISTORY = "BOOST_HISTORY"  # wiki: §4 — P0234, P0299, P0235–P0245
    KNOCK_HISTORY = "KNOCK_HISTORY"  # wiki: §4 — P0325–P0334
    COOLANT_SYSTEM_MALFUNCTION = "COOLANT_SYSTEM_MALFUNCTION"  # wiki: §4 — P0128/P0117 in OL_FAULT
    CYLINDER_FLUID_MISFIRE = "CYLINDER_FLUID_MISFIRE"  # wiki: §4 — P030x in CL with coolant evidence


class DTCSeverityClass(StrEnum):
    """DTC severity tier per SAE J2012 §6.

    Source: DTC_VOCABULARY.md §5.
    """

    A = "A"  # wiki: §5 — catalyst-damaging; MIL flashes on first detection
    B = "B"  # wiki: §5 — emission-relevant; MIL solid after 2 drive cycles
    C = "C"  # wiki: §5 — driveability / non-emission
    D = "D"  # wiki: §5 — informational; no MIL


class DTCState(StrEnum):
    """OBD-II DTC confirmation state — reserved contract surface.

    Not consumed by production code; the wire payload uses the three
    DTC lists (confirmed_dtcs, pending_dtcs, permanent_dtcs).  The
    enum is kept for future typed-API consumers.

    Source: DTC_VOCABULARY.md §6.
    """

    PENDING = "PENDING"  # wiki: §6 — Mode $07; failed once, awaiting confirmation
    CONFIRMED = "CONFIRMED"  # wiki: §6 — Mode $03; confirmed across drive cycles
    PERMANENT = "PERMANENT"  # wiki: §6 — Mode $0A; survives scanner clears


class Mode06MonitorState(StrEnum):
    """Mode $06 on-board monitor test result tri-state.

    Source: DTC_VOCABULARY.md §7; wiki/10_nonstart_diagnostics.md §10.3.
    """

    PASSED = "PASSED"  # wiki: §7 — margin > 15%; confidence 0.0
    PENDING_FAIL_MARGINAL = "PENDING_FAIL_MARGINAL"  # wiki: §7 — margin 1–15%; confidence 0.4
    CRITICAL_FAIL = "CRITICAL_FAIL"  # wiki: §7 — margin ≤ 0%; confidence 0.7
    MONITOR_ABORTED = "MONITOR_ABORTED"  # wiki: §10.3 — Incomplete/all-zero monitor; test never ran


class FuelSystemStatus(StrEnum):
    """Fuel system loop status at freeze-frame capture.

    Source: DTC_VOCABULARY.md §8.
    """

    CL = "CL"  # wiki: §8 — closed loop; O₂ feedback active
    OL = "OL"  # wiki: §8 — open loop; base map (cold start)
    OL_DRIVE = "OL_DRIVE"  # wiki: §8 — open loop driving (WOT, decel)
    OL_FAULT = "OL_FAULT"  # wiki: §8 — open loop due to O₂ sensor fault


class HistoricalFaultContext(StrEnum):
    """Load / thermal context at the moment the DTC was stored.

    Source: DTC_VOCABULARY.md §9.
    """

    HISTORICAL_IDLE_FAULT = "HISTORICAL_IDLE_FAULT"  # wiki: §9 — RPM < 1000, load < 25%
    HISTORICAL_LOAD_FAULT = "HISTORICAL_LOAD_FAULT"  # wiki: §9 — RPM > 2000, load > 45%
    COLD_START_TRANSIT_FAULT = "COLD_START_TRANSIT_FAULT"  # wiki: §9 — ECT < 60°C (priority first)
    UNKNOWN = "UNKNOWN"  # wiki: §9 — none of the above


# =============================================================================
# Constants
# =============================================================================

DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"  # wiki: §2.3, §10

DTC_CONFIDENCE_WEIGHTS: Final[Mapping[str, float]] = {
    "confirmed": 1.0,  # wiki: §16 — Mode $03; two-drive-cycle confirmation
    "permanent": 1.0,  # wiki: §16 — Mode $0A; emissions-critical, monitor-confirmed
    "pending": 0.5,  # wiki: §16 — Mode $07; single failure
    "mode06_critical_fail": 0.7,  # wiki: §16 — test failed
    "mode06_marginal": 0.4,  # wiki: §16 — approaching limit
    "mode06_passed": 0.0,  # wiki: §16 — no contribution
}
