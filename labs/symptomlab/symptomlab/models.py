from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class SymptomValidationError(ValueError):
    """Raised when (tier_1, tier_2) is not one of the 18 allowed combinations,
    or environmental_conditions values are not from the contract enums."""


class OccursDuring(StrEnum):
    ALWAYS = "always"
    COLD_ONLY = "cold_only"
    HOT_ONLY = "hot_only"
    INTERMITTENT = "intermittent"


class EngineState(StrEnum):
    RUNNING = "running"
    CRANKING = "cranking"
    WONT_START = "will_not_start"


class LoadState(StrEnum):
    IDLE = "idle"
    STEADY_CRUISE = "steady_cruise"
    TRANSIENT_ACCELERATION = "transient_acceleration"
    COASTING_DECELERATION = "coasting_deceleration"


@dataclass(frozen=True)
class EnvironmentalConditions:
    occurs_during: OccursDuring
    engine_state: EngineState
    load_state: LoadState

    def to_json_payload(self) -> dict[str, Any]:
        return {"occurs_during": self.occurs_during.value,
                "engine_state": self.engine_state.value,
                "load_state": self.load_state.value}

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_json_payload())


@dataclass(frozen=True)
class SymptomDNA:
    """The 4-field Part B payload, per SEMANTIC_CONTRACT.md §4.2.

    No routing fields. Routing lives in COMLab.

    tier_1_primary_symptom and tier_2_subfield_filter are typed ``str``, not
    StrEnum, because they represent open vocabularies validated by the YAML
    symptom catalog rather than a fixed enum. Adding a symptom to the catalog
    must not require a code change.
    """
    tier_1_primary_symptom: str
    tier_2_subfield_filter: str
    environmental_conditions: EnvironmentalConditions
    free_text_notes: str | None = None

    def to_json_payload(self) -> dict[str, Any]:
        """Serialize to the JSON shape from contract §4.2."""
        return {
            "tier_1_primary_symptom": self.tier_1_primary_symptom,
            "tier_2_subfield_filter": self.tier_2_subfield_filter,
            "environmental_conditions": self.environmental_conditions.to_json_payload(),
            "free_text_notes": self.free_text_notes,
        }

    def to_json(self) -> str:
        import json
        return json.dumps(self.to_json_payload())

    @classmethod
    def from_json(cls, payload: dict[str, Any]) -> SymptomDNA:
        """Deserialize from the dict shape in SEMANTIC_CONTRACT.md §4.2.

        Raises SymptomValidationError for any structural problem:
        missing required fields, or enum strings not in the contract vocabulary.

        Note: this method validates enum membership and field presence only.
        It does NOT check whether (tier_1, tier_2) is one of the 18 allowed
        catalog pairs — that invariant is enforced by SymptomValidator.validate()
        and the resolve() entry point. DNALab must use resolve() (or equivalent)
        when constructing SymptomDNA from user input; from_json() is for
        deserializing an already-validated payload at the JSON boundary.
        """
        try:
            env = payload["environmental_conditions"]
            return cls(
                tier_1_primary_symptom=payload["tier_1_primary_symptom"],
                tier_2_subfield_filter=payload["tier_2_subfield_filter"],
                environmental_conditions=EnvironmentalConditions(
                    occurs_during=OccursDuring(env["occurs_during"]),
                    engine_state=EngineState(env["engine_state"]),
                    # WHY: Pre-load_state payloads deserialize deterministically as
                    # idle until T-DNA-7 bumps the umbrella schema version.
                    load_state=LoadState(env.get("load_state", LoadState.IDLE)),
                ),
                free_text_notes=payload.get("free_text_notes"),
            )
        except KeyError as exc:
            raise SymptomValidationError(f"Missing required field: {exc}") from exc
        except ValueError as exc:
            raise SymptomValidationError(str(exc)) from exc
