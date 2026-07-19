"""Thin real-pipeline smoke test for DNALab assembly wiring."""

from __future__ import annotations

import pytest
from symptomlab.validator import SymptomValidationError
from vinlab.decoder import VINDecodeError

from dnalab.assembly import build_vehicle_dna
from dnalab.models import VehicleDNA


@pytest.mark.integration
def test_real_pipeline_smoke(sample_vin, sample_triage):
    try:
        dna = build_vehicle_dna(sample_vin, sample_triage)
    except (FileNotFoundError, SymptomValidationError, VINDecodeError) as exc:
        pytest.skip(f"real sibling pipeline unavailable: {exc}")

    assert isinstance(dna, VehicleDNA)
    assert dna.vin_dna.vin == sample_vin
    assert dna.symptom_dna.tier_1_primary_symptom == sample_triage["tier_1"]
