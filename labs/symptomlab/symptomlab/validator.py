from __future__ import annotations

from pathlib import Path
import yaml

from symptomlab.models import (
    EngineState,
    EnvironmentalConditions,
    LoadState,
    OccursDuring,
    SymptomDNA,
    SymptomValidationError,
)


class SymptomValidator:
    """Validator for symptom selection against allowed combinations catalog."""

    def __init__(self, allowed_path: Path) -> None:
        """Load and parse the allowed combinations catalog from allowed_path.

        Args:
            allowed_path: Path to allowed_combinations.yaml file.

        Raises:
            ValueError: If the catalog does not contain exactly 21 pairs.
        """
        with open(allowed_path, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh)
        self._allowed: set[tuple[str, str]] = {
            (tier_1, tier_2)
            for tier_1, tier_2_list in doc["combinations"].items()
            for tier_2 in tier_2_list
        }
        # WHY: allowed_combinations.yaml must define exactly 21 pairs (7 tier_1 × 3 tier_2)
        if len(self._allowed) != 21:
            raise ValueError(
                f"allowed_combinations.yaml must define exactly 21 pairs, "
                f"got {len(self._allowed)}"
            )

    def validate(
        self,
        tier_1: str,
        tier_2: str,
        occurs_during: str,
        engine_state: str,
        load_state: str,
        free_text_notes: str | None = None,
    ) -> SymptomDNA:
        """Validate a symptom selection against the catalog of 21 combinations.

        Args:
            tier_1: The primary symptom category (e.g., rough_idle_shudder).
            tier_2: The subfield filter detail (e.g., surging_hunting_idle).
            occurs_during: Environmental condition string from OccursDuring enum.
            engine_state: Environmental condition string from EngineState enum.
            load_state: Environmental condition string from LoadState enum.
            free_text_notes: Optional technician free text comments.

        Returns:
            A validated, frozen SymptomDNA instance.

        Raises:
            SymptomValidationError: If pair is not in catalog or enums are invalid.
        """
        # WHY: reject any (tier_1, tier_2) pair not explicitly allowed in the catalog
        if (tier_1, tier_2) not in self._allowed:
            valid_tier_2s = sorted(t2 for (t1, t2) in self._allowed if t1 == tier_1)
            if valid_tier_2s:
                msg = (
                    f"Unknown (tier_1={tier_1!r}, tier_2={tier_2!r}). "
                    f"Valid tier_2 for {tier_1!r}: {valid_tier_2s}"
                )
            else:
                tier_1s = sorted({t1 for (t1, _) in self._allowed})
                msg = (
                    f"Unknown tier_1={tier_1!r}. "
                    f"Valid tier_1 values: {tier_1s}"
                )
            raise SymptomValidationError(msg)

        try:
            occ = OccursDuring(occurs_during)
            eng = EngineState(engine_state)
            load = LoadState(load_state)
        except ValueError as exc:
            raise SymptomValidationError(str(exc)) from exc

        return SymptomDNA(
            tier_1_primary_symptom=tier_1,
            tier_2_subfield_filter=tier_2,
            environmental_conditions=EnvironmentalConditions(
                occurs_during=occ,
                engine_state=eng,
                load_state=load,
            ),
            free_text_notes=free_text_notes,
        )
