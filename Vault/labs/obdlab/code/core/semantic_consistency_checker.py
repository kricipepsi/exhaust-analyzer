"""Semantic consistency checker — 4 Physics Gates per OBDLab_KG_Wiki.md §4.

Applies after §3 PID validation and before §10-§12 computation.
Raises SemanticConsistencyError on Physics Gate violations.
Source: OBDLab_KG_Wiki.md §4, §4.1, §4.2.
"""

import logging
from typing import Any

from obdlab.core.exceptions import SemanticConsistencyError
from obdlab.schemas.dna_view import ObdLabDnaView
from obdlab.schemas.vocabulary import FuelSystemStatus, RpmStateBucket

logger = logging.getLogger(__name__)

# wiki: §3.1 — trim safety rails (redundant with physical_sensor_bounds.json)
_TRIM_MIN = -127.0   # widened from OBD-nominal -100 to accommodate OBD rail values per T-W-6
_TRIM_MAX = 127.0    # widened from OBD-nominal 99.22 to accommodate OBD rail values per T-W-6

_CUTOFF_ECT_COLD = 75         # wiki: §4.1 — thermal gate cutoff (°C)
_CUTOFF_ECT_CLOSED = 80       # wiki: §4 — closed-loop expected threshold (°C)
_CUTOFF_VSS = 10              # wiki: §4 — VSS km/h for Physics_Gate_1
_CUTOFF_RPM_STALLED = 400     # wiki: §4 — stalled engine RPM for Physics_Gate_1


class SemanticConsistencyChecker:
    """Enforces 4 Physics Gates (§4), thermal gate (§4.1), and closed-loop sanity (§4.2).

    Run after PIDIngestionValidator.validate_and_convert() and before
    VEEngine / O2Normalizer / TrimVectorAggregator.
    """

    def evaluate(
        self, sanitized_pids: dict, dna_view: ObdLabDnaView | None,
    ) -> dict[str, Any]:
        """Run all consistency gates and return a result dict.

        Physics Gates 1-4 raise on violation. Thermal and closed-loop
        gates set internal state only.

        Returns:
            rpm_state_bucket_override: RpmStateBucket | None
            engine_warmed: bool
            trim_analytics_suspect: bool
            gates_passed: list[str]
        """
        rpm_override, engine_warmed = self._thermal_gate(sanitized_pids)
        gates_passed: list[str] = []

        self._physics_gate_1(sanitized_pids)
        gates_passed.append("Physics_Gate_1")

        self._physics_gate_2(sanitized_pids)
        gates_passed.append("Physics_Gate_2")

        self._physics_gate_4(sanitized_pids)
        gates_passed.append("Physics_Gate_4")


        trim_suspect = self._closed_loop_gate(sanitized_pids)

        return {
            "rpm_state_bucket_override": rpm_override,
            "engine_warmed": engine_warmed,
            "trim_analytics_suspect": trim_suspect,
            "gates_passed": gates_passed,
        }

    # ------------------------------------------------------------------
    # Physics_Gate_1 — VSS vs stalled engine
    # ------------------------------------------------------------------

    def _physics_gate_1(self, sanitized_pids: dict) -> None:
        """Gate 1: vehicle moving, engine stalled? — wiki: §4.

        VSS > 10 km/h AND engine_rpm < 400 → SemanticConsistencyError.
        Vehicle cannot roll at speed with a stalled engine.
        """
        vss: float | None = sanitized_pids.get("vss")
        engine_rpm: int | None = sanitized_pids.get("engine_rpm")

        if vss is None or engine_rpm is None:
            return

        if vss > _CUTOFF_VSS and engine_rpm < _CUTOFF_RPM_STALLED:
            raise SemanticConsistencyError(  # noqa: TRY003
                f"Physics_Gate_1: vehicle moving (VSS={vss} km/h) "
                f"but engine stalled (RPM={engine_rpm})"
            )

    # ------------------------------------------------------------------
    # Physics_Gate_2 — closed loop expected above 80 °C
    # ------------------------------------------------------------------

    def _physics_gate_2(self, sanitized_pids: dict) -> None:
        """Gate 2: closed loop should be active at engine temperature — wiki: §4.

        coolant_temp_c >= 80 AND fuel_sys_status == "Open_Loop_Cold"
        → SemanticConsistencyError.
        ECU must enter closed loop by ~70 °C.
        """
        ect: float | None = sanitized_pids.get("coolant_temp_c")
        fuel_status = self._get_fuel_status(sanitized_pids)

        if ect is None or fuel_status is None:
            return

        if ect >= _CUTOFF_ECT_CLOSED and fuel_status == FuelSystemStatus.OL:
            raise SemanticConsistencyError(  # noqa: TRY003
                f"Physics_Gate_2: ECT={ect}°C but fuel system is "
                f"still {fuel_status.value if isinstance(fuel_status, FuelSystemStatus) else fuel_status} — closed loop should be active"
            )


    # ------------------------------------------------------------------
    # Physics_Gate_4 — trim safety limits
    # ------------------------------------------------------------------

    def _physics_gate_4(self, sanitized_pids: dict) -> None:
        """Gate 4: trim out of safety range — wiki: §4.

        Redundant with §3.1 bounds check. Raises SemanticConsistencyError
        (consistent with other gates).
        """
        for field in ("shrtft1", "longft1"):
            value: float | None = sanitized_pids.get(field)
            if value is None:
                continue
            if value < _TRIM_MIN or value > _TRIM_MAX:
                raise SemanticConsistencyError(  # noqa: TRY003
                    f"Physics_Gate_4: {field}={value} out of safety "
                    f"range [{_TRIM_MIN}, {_TRIM_MAX}]"
                )

    # ------------------------------------------------------------------
    # Thermal gate (§4.1)
    # ------------------------------------------------------------------

    def _thermal_gate(self, sanitized_pids: dict) -> tuple[RpmStateBucket | None, bool]:
        """Thermal gate — wiki: §4.1.

        ECT < 75 °C → set rpm_state_bucket = COLD_OPEN_LOOP_INVALID,
        block downstream trim/lambda/VE analytics, engine_warmed = false.

        Returns (rpm_state_bucket_override, engine_warmed).
        """
        ect: float | None = sanitized_pids.get("coolant_temp_c")

        if ect is None:
            return (None, True)

        if ect < _CUTOFF_ECT_COLD:
            return (RpmStateBucket.COLD_OPEN_LOOP_INVALID, False)

        return (None, True)

    # ------------------------------------------------------------------
    # Closed-loop sanity gate (§4.2)
    # ------------------------------------------------------------------

    def _get_fuel_status(self, sanitized_pids: dict) -> FuelSystemStatus | None:
        """Helper to get and coerce fuel system status to FuelSystemStatus enum."""
        fuel_status = sanitized_pids.get("fuel_system_status")
        if fuel_status is None:
            fuel_status = sanitized_pids.get("fuel_sys_status")
        return FuelSystemStatus.from_wire(fuel_status)

    def _closed_loop_gate(self, sanitized_pids: dict) -> bool:
        """Closed-loop sanity gate — wiki: §4.2.

        Warm engine (ECT >= 75 °C) but fuel_system_status != CL
        → flag trim analytics as suspect. Does NOT block payload emission.

        Returns True when trim analytics are suspect.
        """
        ect: float | None = sanitized_pids.get("coolant_temp_c")
        fuel_status = self._get_fuel_status(sanitized_pids)

        if ect is None or fuel_status is None:
            return False

        return ect >= _CUTOFF_ECT_COLD and fuel_status != FuelSystemStatus.CL

