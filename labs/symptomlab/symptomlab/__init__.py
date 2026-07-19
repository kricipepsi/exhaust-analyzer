"""SymptomLab — Part B symptom-triage module for the 4DLab DNA system."""

from functools import lru_cache
from pathlib import Path

from symptomlab.models import EnvironmentalConditions, LoadState, SymptomDNA
from symptomlab.validator import SymptomValidationError, SymptomValidator

_DEFAULT_ALLOWED_PATH = Path(__file__).parent / "data" / "allowed_combinations.yaml"


@lru_cache(maxsize=None)
def _get_validator(allowed_path: Path) -> SymptomValidator:
    """Return a SymptomValidator for `allowed_path`. Cached per distinct path."""
    return SymptomValidator(allowed_path)


def resolve(
    tier_1: str,
    tier_2: str,
    *,
    occurs_during: str,
    engine_state: str,
    load_state: str,
    free_text_notes: str | None = None,
    allowed_path: Path | None = None,
) -> SymptomDNA:
    """Validate a triage selection and package it as a SymptomDNA.

    Per SEMANTIC_CONTRACT.md §4.2, the output has exactly 4 fields.
    Routing (suppress_modes, target_equation, etc.) is not this lab's job.

    Args:
        tier_1: Primary symptom category.
        tier_2: Subfield filter detail.
        occurs_during: OccursDuring enum value.
        engine_state: EngineState enum value.
        load_state: LoadState enum value.
        free_text_notes: Optional free-text technician notes.
        allowed_path: Optional custom path to allowed combinations YAML.
    """
    if allowed_path is None:
        allowed_path = _DEFAULT_ALLOWED_PATH
    return _get_validator(allowed_path).validate(
        tier_1,
        tier_2,
        occurs_during,
        engine_state,
        load_state,
        free_text_notes=free_text_notes,
    )


__all__ = [
    "resolve",
    "SymptomDNA",
    "EnvironmentalConditions",
    "LoadState",
    "SymptomValidationError",
]
