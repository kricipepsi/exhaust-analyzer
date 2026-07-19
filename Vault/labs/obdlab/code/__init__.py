"""OBDLab — electronic-perception sub-graph of the 4D Lab system.

Public surface: SensorSignalTranslator (orchestrator), OBDLivePayload (output contract).
"""

__version__ = "0.1.0"

from obdlab.core.sensor_signal_translator import (
    LinearityAccumulator,
    SensorSignalTranslator,
)
from obdlab.schemas.payload import OBDLivePayload

__all__ = ["OBDLivePayload", "SensorSignalTranslator", "LinearityAccumulator"]
