"""D1 probes: each test asserts what the CITED wiki section says.

A FAILING test reproduces a finding (code value != wiki value).
Run from the repo root:
    python -m pytest -q audit/scratch/D1/test_d1_probes.py -p no:cacheprovider
"""
from pathlib import Path

import pytest

from obdlab.core.ve_engine import VEEngine
from obdlab.core.o2_normalizer import O2Normalizer
from obdlab.core.pid_ingestion_validator import PIDIngestionValidator
from obdlab.core.exceptions import PIDValidationError, SemanticConsistencyError
from obdlab.core.semantic_consistency_checker import SemanticConsistencyChecker
from obdlab.schemas.vocabulary import VEValidity, O2FailureMode

ROOT = Path(__file__).resolve().parents[3]
BOUNDS = ROOT / "labs/obdlab/obdlab/config/physical_sensor_bounds.json"


# F-D1-1 — OBDLab_KG_Wiki.md §6.4 "FAULT_VE_SENSOR_SKEW # VE > 85% at idle on NA engine"
#          and §10.3 STABILIZED_IDLE high trigger "> 85% on NA engine -> FAULT_VE_SENSOR_SKEW".
@pytest.mark.parametrize("ve", [86.0, 88.0, 90.0])
def test_f1_ve_skew_threshold_is_85(ve):
    pids = {"rpm_state_bucket": "STABILIZED_IDLE", "induction_type": "NATURALLY_ASPIRATED",
            "manifold_vacuum_kpa": 35.0}
    assert VEEngine()._classify_validity(ve, pids) == VEValidity.FAULT_VE_SENSOR_SKEW


# F-D1-2 — OBDLab_KG_Wiki.md §11.1 "Voltage 0.51 – 0.59 V -> STOICH_RICH_SIDE -> normalized_obd_lambda = 1.00"
@pytest.mark.parametrize("volts", [0.51, 0.55, 0.59])
def test_f2_narrowband_stoich_rich_side_is_lambda_1(volts):
    lam, _mode, _fm = O2Normalizer().normalize({"pid_oxygen_sensor_volts": volts}, None)
    assert lam == pytest.approx(1.00)


# F-D1-3 — OBDLab_KG_Wiki.md §10.3: FAULT_MAF_CONTAMINATION is a STRESS_IDLE trigger only;
#          REGULATORY_HIGH_IDLE has no low-VE trigger in the table.
def test_f3_maf_contamination_only_at_stress_idle():
    pids = {"rpm_state_bucket": "REGULATORY_HIGH_IDLE", "total_trim_correction_delta": 20.0,
            "induction_type": "NATURALLY_ASPIRATED"}
    assert VEEngine()._classify_validity(60.0, pids) == VEValidity.VALID


# F-D1-4 — OBDLab_KG_Wiki.md §6.7 "STUCK_LEAN # pinned < 0.2 V", "STUCK_RICH # pinned > 0.85 V"
#          (code comment at o2_normalizer.py:127/134 cites §6.7 for the STUCK_* branch).
@pytest.mark.parametrize("volts,expected", [(0.15, O2FailureMode.STUCK_LEAN), (0.88, O2FailureMode.STUCK_RICH)])
def test_f4_stuck_thresholds(volts, expected):
    _lam, _mode, fm = O2Normalizer().normalize({"pid_oxygen_sensor_volts": volts}, None)
    assert fm == expected


# F-D1-5 — OBDLab_KG_Wiki.md §3.1 row `intake_air_temp_c` | −40 | 80 | °C, and
#          "Values outside these bounds raise ValueError and block all downstream processing."
def test_f5_iat_above_80_rejected():
    v = PIDIngestionValidator(BOUNDS)
    with pytest.raises((PIDValidationError, ValueError)):
        v.validate_and_convert({"engine_rpm": 800, "coolant_temp_c": 90, "intake_air_temp_c": 110.0})


# F-D1-6 — OBDLab_KG_Wiki.md §3.1 shrtft1 −100.0 .. +99.22, and §4 Physics_Gate_4
#          "shrtft1 < −100 OR shrtft1 > 99.22 -> ValueError: input breaks safety limits".
def test_f6_trim_rail_rejected_per_wiki():
    with pytest.raises((SemanticConsistencyError, ValueError)):
        SemanticConsistencyChecker()._physics_gate_4({"shrtft1": 110.0, "longft1": 0.0})
