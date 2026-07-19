"""VehicleDNA — the combined Part A + Part B payload.

Schema governed by SEMANTIC_CONTRACT.md §4.3 (binding).
Top-level keys: session_id, timestamp, schema_version, vin_dna, symptom_dna.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from symptomlab.models import SymptomDNA
from vinlab.models import VinDNA

SCHEMA_VERSION = "1.2"  # WHY: SEMANTIC_CONTRACT.md §4.3; bump on wire-shape change


@dataclass(frozen=True)
class VehicleDNA:
    """Combined Part A (VinDNA) + Part B (SymptomDNA) + session metadata.

    The JSON form is the contract surface consumed by COMLab via
    OrchestratorInboundRequest.vehicle_dna.
    """

    session_id: str
    timestamp: str
    schema_version: str
    vin_dna: VinDNA
    symptom_dna: SymptomDNA

    @classmethod
    def new(
        cls,
        vin_dna: VinDNA,
        symptom_dna: SymptomDNA,
        *,
        session_id: str | None = None,
        timestamp: datetime | None = None,
        schema_version: str = SCHEMA_VERSION,
    ) -> VehicleDNA:
        """Create a VehicleDNA with auto-generated session metadata.

        Args:
            vin_dna: decoded Part A payload from vinlab.
            symptom_dna: resolved Part B payload from symptomlab.
            session_id: DNA_TX_<random> if omitted.
            timestamp: current UTC time (ISO 8601) if omitted.
            schema_version: defaults to the module-level SCHEMA_VERSION.
        """
        sid = session_id or f"DNA_TX_{uuid.uuid4().hex[:10].upper()}"
        ts = (timestamp or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
        return cls(
            session_id=sid,
            timestamp=ts,
            schema_version=schema_version,
            vin_dna=vin_dna,
            symptom_dna=symptom_dna,
        )

    def to_json_payload(self) -> dict[str, Any]:
        """Serialize to the dict layout from SEMANTIC_CONTRACT.md §4.3.

        Top-level keys are snake_case: session_id, timestamp, schema_version,
        vin_dna, symptom_dna.
        """
        return {
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "schema_version": self.schema_version,
            "vin_dna": self.vin_dna.to_json_payload(),
            "symptom_dna": self.symptom_dna.to_json_payload(),
        }

    def to_json(self, **dumps_kwargs: Any) -> str:
        """Serialize to a JSON string via to_json_payload().

        Forwards **dumps_kwargs to json.dumps (e.g. indent=2).
        """
        return json.dumps(self.to_json_payload(), **dumps_kwargs)

    @classmethod
    def from_json_payload(cls, payload: dict[str, Any]) -> VehicleDNA:
        """Inverse of to_json_payload(). Delegates to each model's from_json.

        Raises:
            ValueError: if payload["schema_version"] does not match SCHEMA_VERSION.
            KeyError: if any required top-level key is absent.
        """
        incoming = payload.get("schema_version")
        # WHY: strict-match gate — mismatched schema_version means the payload
        # was produced by a different VehicleDNA shape; deserializing would
        # silently drop or misplace fields.
        if incoming != SCHEMA_VERSION:
            raise ValueError(
                f"VehicleDNA schema_version mismatch: expected {SCHEMA_VERSION!r},"
                f" got {incoming!r}"
            )
        return cls(
            session_id=payload["session_id"],
            timestamp=payload["timestamp"],
            schema_version=payload["schema_version"],
            vin_dna=VinDNA.from_json(payload["vin_dna"]),
            symptom_dna=SymptomDNA.from_json(payload["symptom_dna"]),
        )
