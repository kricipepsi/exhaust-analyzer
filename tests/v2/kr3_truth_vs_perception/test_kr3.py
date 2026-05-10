"""KR3 Truth-vs-Perception suite — gas chemistry as ground truth over ECU perception.

Runs structured perception-gap cases through the M0→M4 pipeline and verifies
that the engine trusts Brettschneider lambda (truth) over ECU-reported lambda
(perception).  Targets ≥80% pass rate for P4 milestone gate.

Covers: L01 (no perception short-circuit), KR3 (truth-vs-perception),
        R2 (subtractive vetoes + CF combination), R4/L04 (VL mandatory).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

from engine.v2.arbitrator import (
    _SYM_PERCEPTION_LEAN_SEEN_RICH,
    _SYM_PERCEPTION_RICH_SEEN_LEAN,
    MasterEvidenceVector,
    arbitrate,
)
from engine.v2.digital_parser import parse_digital
from engine.v2.dna_core import DNAOutput, load_dna
from engine.v2.gas_lab import analyse_gas
from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    ValidatedInput,
    VehicleContext,
)
from engine.v2.kg_engine import score_faults
from engine.v2.validation import validate

# ── paths ──────────────────────────────────────────────────────────────────

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
_SCHEMA_DIR = _REPO_ROOT / "schema" / "v2"
_CORPUS_PATH = _REPO_ROOT / "cases" / "csv" / "cases_petrol_master_v6.csv"
_VREF_DB_PATH = _REPO_ROOT / "engine" / "v2" / "vref.db"

# ── schema cache ────────────────────────────────────────────────────────────

_FAULTS: dict | None = None
_EDGES: list[dict] | None = None


def _faults() -> dict:
    global _FAULTS
    if _FAULTS is None:
        with open(_SCHEMA_DIR / "faults.yaml", encoding="utf-8") as f:
            _FAULTS = yaml.safe_load(f)
    assert _FAULTS is not None
    return _FAULTS


def _edges() -> list[dict]:
    global _EDGES
    if _EDGES is None:
        with open(_SCHEMA_DIR / "edges.yaml", encoding="utf-8") as f:
            _EDGES = yaml.safe_load(f)["edges"]
    assert _EDGES is not None
    return _EDGES


# ── pipeline runner ─────────────────────────────────────────────────────────


def _run(
    di: DiagnosticInput,
) -> tuple[ValidatedInput, DNAOutput, MasterEvidenceVector, dict[str, float]]:
    vi = validate(di)
    dna = load_dna(vi, db_path=_VREF_DB_PATH)
    digital = parse_digital(vi, dna)
    gas = analyse_gas(vi, dna)
    evidence = arbitrate(vi, dna, digital, gas)
    raw_probs = score_faults(evidence, dna, _faults(), _edges())
    return vi, dna, evidence, raw_probs


# ── helpers ─────────────────────────────────────────────────────────────────


def _ctx(my: int = 2012, engine_code: str = "EA111_1.2_TSI") -> VehicleContext:
    return VehicleContext(
        brand="VOLKSWAGEN",
        model="Golf",
        engine_code=engine_code,
        displacement_cc=1390,
        my=my,
    )


def _gas(**kw: Any) -> GasRecord:
    defaults: dict[str, float] = {
        "co_pct": 0.1, "hc_ppm": 12.0, "co2_pct": 15.2,
        "o2_pct": 0.3, "nox_ppm": 25.0,
    }
    defaults.update(kw)
    return GasRecord(**defaults)


def _obd(**kw: Any) -> OBDRecord:
    defaults: dict[str, Any] = {
        "ect_c": 90.0, "rpm": 800, "fuel_status": "CL",
        "stft_b1": None, "ltft_b1": None,
        "stft_b2": None, "ltft_b2": None,
    }
    defaults.update(kw)
    return OBDRecord(**defaults)


# ═══════════════════════════════════════════════════════════════════════════════
# KR3 core: perception gap detection
# ═══════════════════════════════════════════════════════════════════════════════


class TestPerceptionGapDetection:
    """Verify perception gap fires correctly when analyser and ECU disagree.

    KR3 rule: Brettschneider lambda (analyser) is ground truth.
    ECU-reported lambda is perception — it may be wrong.
    """

    def test_gap_lean_seen_rich_typical(self) -> None:
        """Analyser λ=0.88 (rich), ECU λ=1.15 (lean) — LEAN_SEEN_RICH gap."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=0.88, co_pct=3.5, o2_pct=0.1),
            obd=_obd(obd_lambda=1.15),
            dtcs=["P0172"],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)

        assert evidence.perception_gap is not None
        assert evidence.perception_gap.gap_type == "LEAN_SEEN_RICH"
        assert _SYM_PERCEPTION_LEAN_SEEN_RICH in evidence.active_symptoms

        # Perception must NOT zero out other fault scores (L01).
        assert len(raw_probs) > 0
        for score in raw_probs.values():
            assert 0.0 <= score <= 1.0

    def test_gap_rich_seen_lean_typical(self) -> None:
        """Analyser λ=1.12 (lean), ECU λ=0.94 (rich) — RICH_SEEN_LEAN gap."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=1.12, co_pct=0.02, o2_pct=4.5),
            obd=_obd(obd_lambda=0.94),
            dtcs=["P0171"],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)

        assert evidence.perception_gap is not None
        assert evidence.perception_gap.gap_type == "RICH_SEEN_LEAN"
        assert _SYM_PERCEPTION_RICH_SEEN_LEAN in evidence.active_symptoms

        # L01: Perception gap must not short-circuit other fault scoring.
        for score in raw_probs.values():
            assert 0.0 <= score <= 1.0

    def test_delta_below_threshold_no_gap(self) -> None:
        """Delta λ ≤ 0.05 — no perception gap should fire."""
        for analyser, obd in [(1.00, 1.04), (1.02, 0.98), (0.97, 1.01)]:
            di = DiagnosticInput(
                vehicle_context=_ctx(),
                gas_idle=_gas(lambda_analyser=analyser),
                obd=_obd(obd_lambda=obd),
                dtcs=[],
                analyser_type="5-gas",
            )
            vi, dna, evidence, raw_probs = _run(di)
            assert evidence.perception_gap is None, (
                f"Unexpected gap for analyser={analyser}, obd={obd}"
            )

    def test_same_side_no_gap_even_with_large_delta(self) -> None:
        """Both lean or both rich — no perception gap regardless of delta."""
        # Both lean: analyser=1.25, obd=1.15 — delta 0.10 but same side.
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=1.25, co_pct=0.01, o2_pct=5.0),
            obd=_obd(obd_lambda=1.15),
            dtcs=[],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)
        assert evidence.perception_gap is None, (
            "Both lean should not trigger perception gap"
        )

        # Both rich: analyser=0.90, obd=0.93 — delta 0.03 but same side.
        di2 = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=0.90, co_pct=4.0, o2_pct=0.1),
            obd=_obd(obd_lambda=0.93),
            dtcs=[],
            analyser_type="5-gas",
        )
        vi2, dna2, evidence2, raw_probs2 = _run(di2)
        assert evidence2.perception_gap is None, (
            "Both rich should not trigger perception gap"
        )

    def test_perception_gap_cf_bounded(self) -> None:
        """Perception gap CF must stay ≤ 0.70 regardless of delta."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=0.80, co_pct=6.0, o2_pct=0.05),
            obd=_obd(obd_lambda=1.20),
            dtcs=[],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)
        assert evidence.perception_gap is not None
        assert evidence.perception_gap.cf <= 0.70


# ═══════════════════════════════════════════════════════════════════════════════
# KR3: Gas chemistry takes precedence over ECU perception
# ═══════════════════════════════════════════════════════════════════════════════


class TestGasTruthOverEcuPerception:
    """Verify that gas chemistry (truth) drives fault scoring over ECU (perception).

    When analyser and ECU disagree, the engine must trust the gas analyser.
    This means:
    - Rich analyser → rich faults should score higher than lean faults
    - Lean analyser → lean faults should score higher than rich faults
    - The perception gap symptom provides evidence to ECU-fault families,
      not a shortcut that suppresses gas-based faults.
    """

    def test_rich_truth_scores_rich_faults_higher(self) -> None:
        """Analyser says rich — rich-mixture faults must dominate."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=0.85, co_pct=5.0, hc_ppm=250,
                          o2_pct=0.1, co2_pct=12.0),
            obd=_obd(obd_lambda=1.10),  # ECU says lean — wrong
            dtcs=["P0172"],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)

        faults = _faults()
        rich_parents = {"Rich_Mixture", "misfire", "catalyst_inefficiency"}
        lean_parents = {"Lean_Mixture", "lean_condition"}

        rich_score = sum(
            s for fid, s in raw_probs.items()
            if faults.get(fid, {}).get("parent", "") in rich_parents
        )
        lean_score = sum(
            s for fid, s in raw_probs.items()
            if faults.get(fid, {}).get("parent", "") in lean_parents
        )
        # Rich faults should score higher than lean faults — truth wins.
        assert rich_score >= lean_score, (
            f"Rich score {rich_score:.3f} should be >= lean score {lean_score:.3f}"
        )

    def test_lean_truth_scores_lean_faults_higher(self) -> None:
        """Analyser says lean — lean-mixture faults must dominate."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=1.12, co_pct=0.01, hc_ppm=40,
                          o2_pct=5.0, co2_pct=11.0),
            obd=_obd(obd_lambda=0.94, stft_b1=15, ltft_b1=10),  # ECU says rich — wrong
            dtcs=["P0171"],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)

        faults = _faults()
        rich_parents = {"Rich_Mixture", "misfire", "catalyst_inefficiency"}
        lean_parents = {"Lean_Mixture", "lean_condition"}

        lean_score = sum(
            s for fid, s in raw_probs.items()
            if faults.get(fid, {}).get("parent", "") in lean_parents
        )
        rich_score = sum(
            s for fid, s in raw_probs.items()
            if faults.get(fid, {}).get("parent", "") in rich_parents
        )
        # Lean faults should score higher — truth wins.
        assert lean_score >= rich_score, (
            f"Lean score {lean_score:.3f} should be >= rich score {rich_score:.3f}"
        )

    def test_ecu_only_input_follows_digital_symptoms(self) -> None:
        """No gas data — digital symptoms from ECU are the only evidence."""
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=None,
            obd=_obd(stft_b1=20, ltft_b1=15, obd_lambda=1.18),
            dtcs=["P0171", "P0301"],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)

        # Digital symptoms should be present even without gas.
        assert len(evidence.active_symptoms) > 0
        # No perception gap without gas analyser data.
        assert evidence.perception_gap is None


# ═══════════════════════════════════════════════════════════════════════════════
# KR3: Corpus-based perception gap cases (≥80% pass rate)
# ═══════════════════════════════════════════════════════════════════════════════


# Hand-curated KR3 cases from the corpus where truth-vs-perception is the
# distinguishing factor.  Each case is scored pass/fail based on whether the
# pipeline correctly orients around gas chemistry (truth) vs ECU (perception).
#
# Pass criteria (for P4, without M5):
#   1. Perception gap fires when analyser/ECU are on opposite sides of stoich
#      AND delta > 0.05 (structural KR3 test).
#   2. Gas-chemistry symptoms (LAMBDA_HIGH/LOW, CO_HIGH, O2_HIGH) appear in
#      the evidence vector when the gas data supports them.
#   3. The pipeline does not crash and produces bounded raw_probs.


# Cases where analyser and ECU are on opposite sides — gap MUST fire.
_GAP_MUST_FIRE: list[dict[str, Any]] = [
    {"case_id": "KR3-001", "analyser_lambda": 0.88, "obd_lambda": 1.15,
     "co_pct": 4.0, "o2_pct": 0.1, "gap_type": "LEAN_SEEN_RICH"},
    {"case_id": "KR3-002", "analyser_lambda": 0.85, "obd_lambda": 1.10,
     "co_pct": 5.0, "o2_pct": 0.1, "gap_type": "LEAN_SEEN_RICH"},
    {"case_id": "KR3-003", "analyser_lambda": 1.12, "obd_lambda": 0.94,
     "co_pct": 0.01, "o2_pct": 4.5, "gap_type": "RICH_SEEN_LEAN"},
    {"case_id": "KR3-004", "analyser_lambda": 1.15, "obd_lambda": 0.92,
     "co_pct": 0.01, "o2_pct": 5.0, "gap_type": "RICH_SEEN_LEAN"},
    {"case_id": "KR3-005", "analyser_lambda": 0.82, "obd_lambda": 1.10,
     "co_pct": 6.0, "o2_pct": 0.05, "gap_type": "LEAN_SEEN_RICH"},
    {"case_id": "KR3-006", "analyser_lambda": 1.08, "obd_lambda": 0.95,
     "co_pct": 0.02, "o2_pct": 4.0, "gap_type": "RICH_SEEN_LEAN"},
    {"case_id": "KR3-007", "analyser_lambda": 0.86, "obd_lambda": 1.12,
     "co_pct": 3.5, "o2_pct": 0.2, "gap_type": "LEAN_SEEN_RICH"},
    {"case_id": "KR3-008", "analyser_lambda": 1.20, "obd_lambda": 0.90,
     "co_pct": 0.01, "o2_pct": 5.5, "gap_type": "RICH_SEEN_LEAN"},
    {"case_id": "KR3-009", "analyser_lambda": 0.80, "obd_lambda": 1.20,
     "co_pct": 7.0, "o2_pct": 0.03, "gap_type": "LEAN_SEEN_RICH"},
    {"case_id": "KR3-010", "analyser_lambda": 1.25, "obd_lambda": 0.88,
     "co_pct": 0.01, "o2_pct": 6.0, "gap_type": "RICH_SEEN_LEAN"},
]

# Cases where analyser and ECU agree (same side) — gap must NOT fire.
_GAP_MUST_NOT_FIRE: list[dict[str, Any]] = [
    {"case_id": "KR3-011", "analyser_lambda": 0.95, "obd_lambda": 0.98,
     "co_pct": 2.5, "o2_pct": 0.2, "reason": "Both slightly rich"},
    {"case_id": "KR3-012", "analyser_lambda": 1.05, "obd_lambda": 1.03,
     "co_pct": 0.05, "o2_pct": 2.5, "reason": "Both slightly lean"},
    {"case_id": "KR3-013", "analyser_lambda": 1.00, "obd_lambda": 1.00,
     "co_pct": 0.1, "o2_pct": 0.3, "reason": "Both stoich"},
    {"case_id": "KR3-014", "analyser_lambda": 1.10, "obd_lambda": 1.08,
     "co_pct": 0.02, "o2_pct": 3.5, "reason": "Both lean, close"},
    {"case_id": "KR3-015", "analyser_lambda": 0.92, "obd_lambda": 0.94,
     "co_pct": 3.0, "o2_pct": 0.1, "reason": "Both rich, close"},
]


@pytest.mark.parametrize("case", _GAP_MUST_FIRE)
def test_kr3_gap_must_fire(case: dict[str, Any]) -> None:
    """KR3 cases where analyser/ECU are on opposite sides — gap must fire."""
    di = DiagnosticInput(
        vehicle_context=_ctx(),
        gas_idle=_gas(lambda_analyser=case["analyser_lambda"],
                      co_pct=case["co_pct"], o2_pct=case["o2_pct"]),
        obd=_obd(obd_lambda=case["obd_lambda"]),
        dtcs=[],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    assert evidence.perception_gap is not None, (
        f"{case['case_id']}: gap should fire "
        f"(analyser={case['analyser_lambda']}, obd={case['obd_lambda']})"
    )
    assert evidence.perception_gap.gap_type == case["gap_type"], (
        f"{case['case_id']}: expected {case['gap_type']}, "
        f"got {evidence.perception_gap.gap_type}"
    )
    # L01: Perception gap must not zero all fault scores.
    for fid, score in raw_probs.items():
        assert 0.0 <= score <= 1.0, f"{case['case_id']}: {fid} = {score}"


@pytest.mark.parametrize("case", _GAP_MUST_NOT_FIRE)
def test_kr3_gap_must_not_fire(case: dict[str, Any]) -> None:
    """KR3 cases where analyser/ECU agree — gap must not fire."""
    di = DiagnosticInput(
        vehicle_context=_ctx(),
        gas_idle=_gas(lambda_analyser=case["analyser_lambda"],
                      co_pct=case["co_pct"], o2_pct=case["o2_pct"]),
        obd=_obd(obd_lambda=case["obd_lambda"]),
        dtcs=[],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    assert evidence.perception_gap is None, (
        f"{case['case_id']}: gap should NOT fire ({case['reason']}) "
        f"(analyser={case['analyser_lambda']}, obd={case['obd_lambda']})"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# KR3 composite score (≥80% for P4 milestone gate)
# ═══════════════════════════════════════════════════════════════════════════════


def test_kr3_pass_rate_meets_p4_gate() -> None:
    """Aggregate KR3 pass rate across all parametrized cases must be ≥80%.

    This test summarises the overall KR3 score for the P4 milestone gate.
    The parametrized cases above test individual scenarios; this test
    verifies the aggregate passes the 80% threshold.
    """
    # Run all GAP_MUST_FIRE and GAP_MUST_NOT_FIRE cases.
    total = len(_GAP_MUST_FIRE) + len(_GAP_MUST_NOT_FIRE)
    passed = 0
    failures: list[str] = []

    for case in _GAP_MUST_FIRE:
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=case["analyser_lambda"],
                          co_pct=case["co_pct"], o2_pct=case["o2_pct"]),
            obd=_obd(obd_lambda=case["obd_lambda"]),
            dtcs=[],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)
        if (evidence.perception_gap is not None
                and evidence.perception_gap.gap_type == case["gap_type"]):
            passed += 1
        else:
            got = evidence.perception_gap.gap_type if evidence.perception_gap else "None"
            failures.append(
                f"{case['case_id']}: gap {got} != expected {case['gap_type']}"
            )

    for case in _GAP_MUST_NOT_FIRE:
        di = DiagnosticInput(
            vehicle_context=_ctx(),
            gas_idle=_gas(lambda_analyser=case["analyser_lambda"],
                          co_pct=case["co_pct"], o2_pct=case["o2_pct"]),
            obd=_obd(obd_lambda=case["obd_lambda"]),
            dtcs=[],
            analyser_type="5-gas",
        )
        vi, dna, evidence, raw_probs = _run(di)
        if evidence.perception_gap is None:
            passed += 1
        else:
            failures.append(f"{case['case_id']}: gap fired but should not "
                            f"({case['reason']})")

    pass_rate = (passed / total) * 100 if total > 0 else 0.0

    # P4 milestone gate: ≥80% KR3 pass rate.
    assert pass_rate >= 80.0, (
        f"KR3 pass rate {pass_rate:.1f}% ({passed}/{total}) below 80% gate.\n"
        f"Failures:\n" + "\n".join(f"  - {f}" for f in failures)
    )


# ═══════════════════════════════════════════════════════════════════════════════
# KR3: Structural invariants (L01 — no perception short-circuit)
# ═══════════════════════════════════════════════════════════════════════════════


def test_kr3_perception_gap_never_zeros_fault_scores() -> None:
    """L01: Even at max CF, perception gap must never zero out any fault score.

    V1 regression: perception gap at 0.70 confidence overrode L1-L4 layers.
    V2 fix: perception gap is a normal KG symptom, not an authority signal.
    """
    # Extreme perception gap case.
    di = DiagnosticInput(
        vehicle_context=_ctx(),
        gas_idle=_gas(lambda_analyser=0.80, co_pct=7.0, o2_pct=0.02),
        obd=_obd(obd_lambda=1.20, stft_b1=2, ltft_b1=1),
        dtcs=["P0172", "P0301"],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    # Every fault must have a score in [0.0, 1.0] — no short-circuit zeros.
    assert len(raw_probs) > 0
    for fid, score in raw_probs.items():
        assert 0.0 <= score <= 1.0, f"Fault {fid} score {score} out of [0, 1]"

    # At least one non-ECU fault must have a positive score.
    non_ecu_scoring = {
        fid: s for fid, s in raw_probs.items()
        if s > 0 and "ECU" not in fid and "Perception" not in fid
    }
    assert len(non_ecu_scoring) > 0, (
        "L01 violation: perception gap zeroed all non-ECU fault scores"
    )


def test_kr3_gas_symptoms_present_when_gap_fires() -> None:
    """When perception gap fires, gas chemistry symptoms must be in evidence.

    The gap is between analyser and ECU — analyser symptoms represent truth.
    These must not be suppressed when a gap is detected.
    """
    di = DiagnosticInput(
        vehicle_context=_ctx(),
        gas_idle=_gas(lambda_analyser=0.88, co_pct=4.0, hc_ppm=200,
                      o2_pct=0.1, co2_pct=12.0),
        obd=_obd(obd_lambda=1.15),
        dtcs=["P0172"],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    assert evidence.perception_gap is not None

    # Gas-chemistry symptoms from M2 must be present alongside the gap.
    gas_symptoms = [s for s in evidence.active_symptoms
                    if s.startswith("SYM_") and "PERCEPTION" not in s
                    and "TRIM" not in s and "DTC" not in s]
    assert len(gas_symptoms) >= 1, (
        f"Expected gas chemistry symptoms in evidence, got {gas_symptoms}"
    )


def test_kr3_confidence_ceiling_respected() -> None:
    """L16: Confidence ceiling must key on evidence layers used."""
    ctx = _ctx(my=2001, engine_code="UNKNOWN_CODE_XYZ")
    di = DiagnosticInput(
        vehicle_context=ctx,
        gas_idle=_gas(lambda_analyser=0.88),
        obd=_obd(obd_lambda=1.15),
        dtcs=[],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    # vref.db miss → confidence ceiling should be capped.
    assert dna.confidence_ceiling <= 0.60 + 0.01  # small tolerance
    assert dna.vref_missing is True


def test_kr3_perception_not_authority() -> None:
    """L01: Perception gap is a normal symptom, not an authority layer.

    Even when SYM_PERCEPTION_* is in evidence, other fault families must
    score independently — the perception symptom should add evidence to
    ECU-related faults without suppressing gas-based faults.
    """
    di = DiagnosticInput(
        vehicle_context=_ctx(),
        gas_idle=_gas(lambda_analyser=0.88, co_pct=4.5, o2_pct=0.1,
                      co2_pct=12.0, hc_ppm=250),
        obd=_obd(obd_lambda=1.15, stft_b1=-12, ltft_b1=-8),
        dtcs=["P0172"],
        analyser_type="5-gas",
    )
    vi, dna, evidence, raw_probs = _run(di)

    assert evidence.perception_gap is not None

    # Check that the top fault is NOT solely determined by perception gap.
    # Rich-mixture faults (gas truth) should still be among top scorers.
    faults = _faults()
    rich_fault_ids = {fid for fid, fdef in faults.items()
                      if fdef.get("parent") == "Rich_Mixture"}
    rich_scores = {fid: raw_probs.get(fid, 0.0) for fid in rich_fault_ids}
    if rich_scores:
        top_rich = max(rich_scores, key=lambda k: rich_scores[k])
        assert rich_scores[top_rich] > 0.0, (
            "L01 violation: rich-mixture faults zeroed by perception gap"
        )
