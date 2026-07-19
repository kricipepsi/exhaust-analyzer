"""Slim DNA projection consumed by GASLab.

Declared locally so GASLab has no cross-lab Python imports.
Mirrors the shape of ``COMLab/comlab/schemas/lab_dna_views.py`` but does
not import from it.  Source: ``GAS_WIKI §2.4``.
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class GasLabDnaView(BaseModel):
    """The 13-field DNA slice GASLab consumes.

    GASLab does not consume the full ``VehicleDNA``.  COMLab's projector
    hands it this typed slice.  Source: ``GAS_WIKI §1.4`` table.

    ``target_lambda_v112`` carries the certified CoC λ value.
    When present, the consumer uses a window of ``[v112 - 0.005, v112 + 0.005]``;
    absent → generic ±0.005 window (centered on 1.000).
    """

    model_config = ConfigDict(frozen=True)

    engine_displacement_liters: float = Field(..., gt=0.0)  # wiki: GAS_WIKI §1.4
    cylinder_count: int = Field(..., ge=1, le=16)  # wiki: GAS_WIKI §1.4
    number_of_banks: int = Field(..., ge=1, le=4)  # wiki: GAS_WIKI §1.4
    euro_emission_category: str  # wiki: GAS_WIKI §1.4
    fuel_delivery_type: str  # wiki: GAS_WIKI §1.4
    induction_type: str  # wiki: GAS_WIKI §1.4
    upstream_o2_type: str  # wiki: GAS_WIKI §1.4
    has_catalyst: bool  # wiki: GAS_WIKI §1.4
    egr_equipped: bool  # wiki: GAS_WIKI §1.4
    target_lambda_v112: Optional[float] = Field(default=None, ge=0.5, le=2.5)  # vocab: GAS_VOCABULARY §6
    co_low_idle: Optional[float] = Field(default=None, ge=0.0, le=15.0)  # vocab: GAS_VOCABULARY §2
    co_high_idle: Optional[float] = Field(default=None, ge=0.0, le=15.0)  # vocab: GAS_VOCABULARY §2
    confidence: str = "NONE"  # wiki: GAS_WIKI §1.4
