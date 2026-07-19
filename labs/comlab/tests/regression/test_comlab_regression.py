"""Pinned golden-master regression tests for COMLab."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.schemas.ingestion import OrchestratorInboundRequest

_FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
_FATAL_FIXTURES_DIR = _FIXTURES_DIR / "fatal"


def _fixture_paths() -> list[Path]:
    """Return all committed COMLab golden fixtures in stable order."""
    return sorted(_FIXTURES_DIR.glob("case_*.json"))


def _fatal_fixture_paths() -> list[Path]:
    """Return all fatal-gate (flag-on) golden fixtures in stable order."""
    return sorted(_FATAL_FIXTURES_DIR.glob("case_*.json"))


def _load_fixture(path: Path) -> dict[str, Any]:
    """Load one golden fixture from disk."""
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


@pytest.mark.parametrize(
    "fixture_path",
    _fixture_paths(),
    ids=lambda path: path.stem,
)
def test_comlab_regression(fixture_path: Path) -> None:
    """Pin either the current verdict or current ingestion rejection."""
    fixture = _load_fixture(fixture_path)

    if "expected_validation_error" in fixture:
        with pytest.raises(ValidationError) as exc_info:
            OrchestratorInboundRequest.model_validate(fixture["request"])
        assert fixture["expected_validation_error"] in str(exc_info.value)
        return

    request = OrchestratorInboundRequest.model_validate(fixture["request"])
    result = LabPipelineAggregator().process(request)
    observed = {
        "top_fault": result.diagnostic_verdict.fault_code,
        "fault_family": result.diagnostic_verdict.fault_family,
        "degradation_mode": result.execution_meta.degradation_mode,
        "confidence": result.execution_meta.processing_confidence_rating,
    }
    assert observed == fixture["expected"]


@pytest.mark.parametrize(
    "fixture_path",
    _fatal_fixture_paths(),
    ids=lambda path: path.stem,
)
def test_comlab_regression_fatal_gates(fixture_path: Path) -> None:
    """Pin FATAL_INCOMPLETE verdicts when ``enable_fatal_gates=True``."""
    fixture = _load_fixture(fixture_path)

    # Fatal-gate fixtures are always valid requests (no validation-error cases).
    request = OrchestratorInboundRequest.model_validate(fixture["request"])
    result = LabPipelineAggregator(enable_fatal_gates=True).process(request)
    observed = {
        "top_fault": result.diagnostic_verdict.fault_code,
        "fault_family": result.diagnostic_verdict.fault_family,
        "degradation_mode": result.execution_meta.degradation_mode,
        "confidence": result.execution_meta.processing_confidence_rating,
    }
    assert observed == fixture["expected"]


def test_regression_fixture_manifest() -> None:
    """Require the task's bounded fixture count and scenario coverage."""
    paths = _fixture_paths()
    assert 5 <= len(paths) <= 8

    fixtures = [_load_fixture(path) for path in paths]
    verdict_fixtures = [
        fixture for fixture in fixtures if "expected" in fixture
    ]
    families = {
        fixture["expected"]["fault_family"] for fixture in verdict_fixtures
    }
    degradation_modes = {
        fixture["expected"]["degradation_mode"] for fixture in verdict_fixtures
    }

    assert "no_fault" in families
    assert len(families - {"no_fault"}) >= 3
    assert "FULL_FUSION" in degradation_modes
    assert "GAS_DOMINANT" in degradation_modes
    assert any("expected_validation_error" in fixture for fixture in fixtures)
