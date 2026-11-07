"""OBDLab custom exception hierarchy."""


class ObdLabError(Exception):
    """Base exception for all OBDLab errors."""


class PIDValidationError(ObdLabError):
    """Raised when a PID violates physical_sensor_bounds.json (§3.1)."""


class AirMeteringStrategyError(ObdLabError):
    """Raised when the DNA view names no known air-metering strategy (§10.2; ADR-0005, T-AUD-17)."""


class SemanticConsistencyError(ObdLabError):
    """Raised when a Physics Gate (§4) fails.

    Source: OBDLab_KG_Wiki.md §4.
    """

