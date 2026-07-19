"""ComLab — orchestrator layer of the 4DLab diagnostic app.

ComLab is the deterministic rule-engine that fuses outputs from four upstream
labs (VINLab, GasLab, OBD Live Lab, DTC Lab) into one diagnostic verdict
plus performance analytics for the UI.
"""

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator

__version__ = "0.1.0"
__all__ = ["LabPipelineAggregator", "__version__"]
