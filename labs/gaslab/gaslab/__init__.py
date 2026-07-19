"""GASLab — 5-gas exhaust diagnostic module of 4DLab.

Public entry point: ``process``. See ``GAS_WIKI §2.1`` for the contract.
"""

from gaslab.contracts import (
    AFR_STOICH,
    HC_FACTOR,
    Hcv,
    CatalystStatus,
    ChemicalSignature,
    EngineStateBucket,
    GasBehavior,
    GasLabPayload,
    GasReading,
    LambdaBand,
    SampleValidity,
)
from gaslab.dna_view import GasLabDnaView
from gaslab.process import GasLabContext, process

__all__ = [
    "AFR_STOICH",
    "HC_FACTOR",
    "Hcv",
    "CatalystStatus",
    "ChemicalSignature",
    "EngineStateBucket",
    "GasBehavior",
    "GasLabContext",
    "GasLabDnaView",
    "GasLabPayload",
    "GasReading",
    "LambdaBand",
    "SampleValidity",
    "process",
]
