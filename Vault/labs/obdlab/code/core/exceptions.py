"""OBDLab custom exception hierarchy."""


class ObdLabError(Exception):
    """Base exception for all OBDLab errors."""


class PIDValidationError(ObdLabError):
    """Raised when a PID violates physical_sensor_bounds.json (§3.1)."""


class SemanticConsistencyError(ObdLabError):
    """Raised when a Physics Gate (§4) fails.

    Source: OBDLab_KG_Wiki.md §4.
    """

