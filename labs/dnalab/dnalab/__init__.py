"""DNALab — the umbrella lab that composes VinDNA + SymptomDNA into VehicleDNA.

Public API:
    build_vehicle_dna(vin, triage) -> VehicleDNA
    VehicleDNA — the combined dataclass
"""

from __future__ import annotations

from dnalab.assembly import build_vehicle_dna
from dnalab.models import VehicleDNA

__all__ = ["build_vehicle_dna", "VehicleDNA"]
