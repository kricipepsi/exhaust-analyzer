"""M3 — Cross-channel arbitrator: perception gap, trim-trend, evidence vector assembly.

R4 / L04: consumes ValidatedInput, never raw DiagnosticInput.
L01: perception fires CF-weighted symptoms only, never global overrides.
R7: resolve_conflicts() lives in M5 only — M3 does not call it.
R8: flood control skeleton — cascading_consequences[] and bank_asym
     fields exist for T-P4-2 to populate.

Source: v2-arbitrator §1–§3.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.v2.digital_parser import DigitalParserOutput
from engine.v2.dna_core import DNAOutput
from engine.v2.gas_lab import GasLabOutput
from engine.v2.input_model import OBDRecord, ValidatedInput

# ── perception gap thresholds ─────────────────────────────────────────────────
# source: v2-arbitrator §2.1 perception gap detection

_PERCEPTION_DELTA_THRESHOLD: float = 0.05
_PERCEPTION_LAMBDA_RICH: float = 0.97
_PERCEPTION_LAMBDA_LEAN: float = 1.05
_PERCEPTION_OBD_RICH: float = 0.97
_PERCEPTION_OBD_LEAN: float = 1.03
_PERCEPTION_CF_MAX: float = 0.70
_PERCEPTION_CF_MULTIPLIER: float = 6.0

# ── trim-trend thresholds ─────────────────────────────────────────────────────
# source: v2-arbitrator §2.2 trim-trend 4-pattern matrix

_TRIM_STRONG_PCT: float = 8.0
_TRIM_NO_L2_CF_REDUCTION: float = 0.70

# ── bank symmetry thresholds ───────────────────────────────────────────────────
# source: v2-arbitrator §2.3 bank symmetry (V-engine only)

_BANK_ASYM_DIFF_PCT: float = 10.0
_BANK_SWAP_CF: float = 0.65
_BANK_ASYM_CF: float = 0.55

# ── flood control thresholds ───────────────────────────────────────────────────
# source: v2-arbitrator §2.4 flood control
# source: R8 — single root cause firing > 3 sibling symptoms triggers cascade

_FLOOD_SIBLING_THRESHOLD: int = 3
_FLOOD_REDUCTION_FACTOR: float = 0.70

# ── carry-forward CF defaults ─────────────────────────────────────────────────
# source: v2-arbitrator §3 output contract — M3 assembles M1/M2 symptoms
# into the evidence vector with appropriate CF weights.
# M2 (gas chemistry) gets higher base CF than M1 (digital/ECU) because
# Brettschneider lambda is ground truth (Truth-vs-Perception architecture).

_CF_DEFAULT_DIGITAL: float = 0.70
_CF_DEFAULT_GAS: float = 0.85

# ── symptom ID constants ──────────────────────────────────────────────────────
# source: v2-arbitrator §2.1–§2.2

_SYM_PERCEPTION_LEAN_SEEN_RICH = "SYM_PERCEPTION_LEAN_SEEN_RICH"
_SYM_PERCEPTION_RICH_SEEN_LEAN = "SYM_PERCEPTION_RICH_SEEN_LEAN"

_SYM_TRIM_LEAN_IDLE_ONLY = "SYM_TRIM_LEAN_IDLE_ONLY"
_SYM_TRIM_LEAN_LOAD_BIAS = "SYM_TRIM_LEAN_LOAD_BIAS"
_SYM_TRIM_RICH_STATIC = "SYM_TRIM_RICH_STATIC"
_SYM_TRIM_RICH_IDLE_ONLY = "SYM_TRIM_RICH_IDLE_ONLY"

_SYM_O2_HARNESS_SWAP = "SYM_O2_HARNESS_SWAP"
_SYM_BANK_ASYM_FAULT = "SYM_BANK_ASYM_FAULT"


# ── symptom family groups for flood control ────────────────────────────────────
# source: v2-arbitrator §2.4 — symptoms sharing a common fault ancestry
# are grouped by prefix; when > _FLOOD_SIBLING_THRESHOLD in one group,
# the highest-CF symptom is kept at full weight and the rest reduced 30%.
# This is a proxy for full KG ancestry lookup (M4's domain); when M3 and
# M4 are integrated, replace with faults.yaml lineage.
#
# Grouping key: extracted by stripping trailing type/condition qualifiers
# from the symptom ID (e.g. SYM_TRIM_LEAN_IDLE_ONLY → SYM_TRIM_LEAN).

_FLOOD_GROUP_KEYS: dict[str, str] = {
    "SYM_TRIM_LEAN_IDLE_ONLY": "TRIM_LEAN",
    "SYM_TRIM_LEAN_LOAD_BIAS": "TRIM_LEAN",
    "SYM_TRIM_RICH_STATIC": "TRIM_RICH",
    "SYM_TRIM_RICH_IDLE_ONLY": "TRIM_RICH",
    "SYM_PERCEPTION_LEAN_SEEN_RICH": "PERCEPTION_GAP",
    "SYM_PERCEPTION_RICH_SEEN_LEAN": "PERCEPTION_GAP",
}


# ── output dataclasses ────────────────────────────────────────────────────────


@dataclass(slots=True)
class PerceptionGap:
    """Truth-vs-perception gap detected by M3.

    When gas chemistry (Brettschneider lambda) disagrees with ECU-reported
    lambda by more than 0.05, a perception gap symptom fires into the
    evidence vector as a normal weighted input — never as a global override
    (L01).
    """
    gap_type: str
    cf: float
    analyser_lambda: float
    obd_lambda: float


@dataclass
class MasterEvidenceVector:
    """M3 output — master evidence vector consumed by M4 (KG engine).

    R9: symptom IDs match schema/v2/symptoms.yaml emitted_by M3.
    L01: perception_gap is informational; M4 uses the active_symptoms
         entries, not this field, for scoring — preventing the V1
         perception short-circuit.
    """
    active_symptoms: dict[str, float] = field(default_factory=dict)
    perception_gap: PerceptionGap | None = None
    cascading_consequences: list[str] = field(default_factory=list)
    bank_asym: bool = False


# ── public entry point ────────────────────────────────────────────────────────


def arbitrate(
    validated_input: ValidatedInput,
    dna_output: DNAOutput,
    digital_output: DigitalParserOutput,
    gas_output: GasLabOutput,
) -> MasterEvidenceVector:
    """Run M3 cross-channel arbitration.

    Combines M1 (digital) and M2 (gas) evidence with cross-channel
    analysis: perception gap detection and trim-trend classification.
    Bank symmetry and flood control follow in T-P4-2.

    Args:
        validated_input: Post-VL input (R4/L04 — never raw DiagnosticInput).
        dna_output: M0 vehicle DNA profile (tech_mask, engine_state).
        digital_output: M1 digital symptoms and fuel-status gate.
        gas_output: M2 gas analysis (lambdas, gas symptoms, dual-state tag).

    Returns:
        MasterEvidenceVector with active_symptoms (CF-weighted),
        perception_gap (or None), cascading_consequences (empty until
        T-P4-2), and bank_asym (False until T-P4-2).
    """
    evidence = MasterEvidenceVector()

    _collect_digital_symptoms(digital_output, evidence)
    _collect_gas_symptoms(gas_output, evidence)
    _detect_perception_gap(validated_input, gas_output, evidence)
    _analyse_trim_trend(validated_input, gas_output, evidence)
    _analyse_bank_symmetry(dna_output, validated_input, evidence)
    _apply_flood_control(evidence)

    return evidence


# ── evidence collection (M1 / M2 carry-forward) ───────────────────────────────


def _collect_digital_symptoms(
    digital_output: DigitalParserOutput,
    evidence: MasterEvidenceVector,
) -> None:
    """Carry M1 digital symptoms into the evidence vector.

    Digital symptoms (DTCs, freeze-frame, OBD live) enter at base CF 0.70.
    The fuel-status gate and cold-engine flag are informational — they affect
    CF weighting but do not suppress symptoms (L18).
    """
    for sym in digital_output.symptoms:
        evidence.active_symptoms[sym] = _CF_DEFAULT_DIGITAL


def _collect_gas_symptoms(
    gas_output: GasLabOutput,
    evidence: MasterEvidenceVector,
) -> None:
    """Carry M2 gas symptoms into the evidence vector.

    Gas symptoms enter at base CF 0.85 — Brettschneider lambda is ground
    truth in the Truth-vs-Perception architecture.
    """
    for sym in gas_output.symptoms_idle:
        evidence.active_symptoms[sym] = _CF_DEFAULT_GAS
    for sym in gas_output.symptoms_high:
        evidence.active_symptoms[sym] = _CF_DEFAULT_GAS


# ── perception gap detection ──────────────────────────────────────────────────


def _detect_perception_gap(
    validated_input: ValidatedInput,
    gas_output: GasLabOutput,
    evidence: MasterEvidenceVector,
) -> None:
    """Detect truth-vs-perception lambda disagreement (L01).

    Compares Brettschneider analyser_lambda (ground truth) against
    ECU-reported obd_lambda.  When the delta exceeds 0.05, emits a
    CF-weighted symptom into the evidence vector — never a global override.

    source: v2-arbitrator §2.1
    """
    obd = validated_input.raw.obd
    if obd is None or obd.obd_lambda is None:
        return

    analyser_lambda = _best_analyser_lambda(gas_output)
    if analyser_lambda is None:
        return

    delta = abs(analyser_lambda - obd.obd_lambda)
    if delta <= _PERCEPTION_DELTA_THRESHOLD:
        return

    cf = min(_PERCEPTION_CF_MAX, delta * _PERCEPTION_CF_MULTIPLIER)

    if analyser_lambda < _PERCEPTION_LAMBDA_RICH and obd.obd_lambda > _PERCEPTION_OBD_LEAN:
        gap_type = "LEAN_SEEN_RICH"
        sym = _SYM_PERCEPTION_LEAN_SEEN_RICH
    elif analyser_lambda > _PERCEPTION_LAMBDA_LEAN and obd.obd_lambda < _PERCEPTION_OBD_RICH:
        gap_type = "RICH_SEEN_LEAN"
        sym = _SYM_PERCEPTION_RICH_SEEN_LEAN
    else:
        return

    evidence.active_symptoms[sym] = cf
    evidence.perception_gap = PerceptionGap(
        gap_type=gap_type,
        cf=cf,
        analyser_lambda=analyser_lambda,
        obd_lambda=obd.obd_lambda,
    )


def _best_analyser_lambda(gas_output: GasLabOutput) -> float | None:
    """Return the best available analyser lambda (prefer idle, fallback high)."""
    if gas_output.analyser_lambda_idle is not None:
        return gas_output.analyser_lambda_idle
    return gas_output.analyser_lambda_high


# ── trim-trend analysis ───────────────────────────────────────────────────────


def _analyse_trim_trend(
    validated_input: ValidatedInput,
    gas_output: GasLabOutput,
    evidence: MasterEvidenceVector,
) -> None:
    """Classify fuel-trim pattern from idle vs. cruise comparison.

    Uses the 4-pattern matrix from v2-arbitrator §2.2:
      idle >= +8%, cruise returns → LEAN_IDLE_ONLY
      idle >= +8%, cruise stays   → LEAN_LOAD_BIAS
      idle <= -8%, cruise stays   → RICH_STATIC
      idle <= -8%, cruise returns → RICH_IDLE_ONLY

    When only idle data is available (no high-idle gas sample), degrades to
    idle-only mode: only IDLE_ONLY tags emitted, CF reduced by 30%.
    """
    obd = validated_input.raw.obd
    if obd is None:
        return

    idle_total = _compute_trim_total_b1(obd)
    if idle_total is None:
        return

    has_l2 = gas_output.analyser_lambda_high is not None
    _classify_trim_trend(idle_total, has_l2, evidence)


def _compute_trim_total_b1(obd: OBDRecord) -> float | None:
    """Compute STFT + LTFT for bank 1. Returns None if both are missing."""
    stft = obd.stft_b1
    ltft = obd.ltft_b1
    if stft is None and ltft is None:
        return None
    return (stft if stft is not None else 0.0) + (ltft if ltft is not None else 0.0)


def _classify_trim_trend(
    idle_total: float,
    has_l2: bool,
    evidence: MasterEvidenceVector,
) -> None:
    """Classify fuel-trim pattern from idle trim data (Option A).

    When L2 high-idle gas data is present, the idle trim reading is at a
    confirmed operating point — no CF penalty.  When L2 is absent, a 30%
    CF reduction applies because the idle-only reading is less reliable.

    The full 4-pattern matrix (LEAN_LOAD_BIAS / RICH_STATIC) remains
    deferred to v2.1 when a high-idle OBD snapshot is added to the data
    model.

    source: v2-arbitrator §2.2 — Option A idle-only classification
    """
    cf = 0.65 if has_l2 else 0.65 * _TRIM_NO_L2_CF_REDUCTION  # 30% penalty when idle-only
    if idle_total >= _TRIM_STRONG_PCT:
        evidence.active_symptoms[_SYM_TRIM_LEAN_IDLE_ONLY] = cf
    elif idle_total <= -_TRIM_STRONG_PCT:
        evidence.active_symptoms[_SYM_TRIM_RICH_IDLE_ONLY] = cf


# ── bank symmetry analysis ─────────────────────────────────────────────────────


def _analyse_bank_symmetry(
    dna_output: DNAOutput,
    validated_input: ValidatedInput,
    evidence: MasterEvidenceVector,
) -> None:
    """Detect bank-to-bank trim asymmetry on V-engines (R8).

    Fires only when tech_mask.is_v_engine is True.  Compares Bank 1 vs
    Bank 2 total trims (STFT + LTFT):
      - Opposite signs, |diff| > 10 pp → SYM_O2_HARNESS_SWAP  (CF = 0.65)
      - Same sign,     |diff| > 10 pp → SYM_BANK_ASYM_FAULT   (CF = 0.55)

    SYM_BANK_ASYM_FAULT implies hard-veto edges to common-mode faults
    (Maf_Fault, Fuel_Pump_Weak, Plenum_Leak) — bank-asymmetric trim
    cannot come from a single-point fault affecting both banks equally.

    source: v2-arbitrator §2.3
    """
    if not dna_output.tech_mask.get("is_v_engine"):
        return

    obd = validated_input.raw.obd
    if obd is None:
        return

    trim_b1 = _compute_trim_total_b1(obd)
    if trim_b1 is None:
        return

    trim_b2 = _compute_trim_total_b2(obd)
    if trim_b2 is None:
        return

    diff = abs(trim_b1 - trim_b2)
    if diff <= _BANK_ASYM_DIFF_PCT:
        return

    b1_sign = 1 if trim_b1 > 0 else -1 if trim_b1 < 0 else 0
    b2_sign = 1 if trim_b2 > 0 else -1 if trim_b2 < 0 else 0

    if b1_sign != 0 and b2_sign != 0 and b1_sign != b2_sign:
        evidence.active_symptoms[_SYM_O2_HARNESS_SWAP] = _BANK_SWAP_CF
        evidence.bank_asym = True
    elif b1_sign != 0 or b2_sign != 0:
        evidence.active_symptoms[_SYM_BANK_ASYM_FAULT] = _BANK_ASYM_CF
        evidence.bank_asym = True


def _compute_trim_total_b2(obd: OBDRecord) -> float | None:
    """Compute STFT + LTFT for bank 2. Returns None if both are missing."""
    stft = obd.stft_b2
    ltft = obd.ltft_b2
    if stft is None and ltft is None:
        return None
    return (stft if stft is not None else 0.0) + (ltft if ltft is not None else 0.0)


# ── flood control ──────────────────────────────────────────────────────────────


def _apply_flood_control(evidence: MasterEvidenceVector) -> None:
    """Prevent a single root cause from dominating the score distribution (R8).

    Groups active symptoms by fault-family key.  When more than
    _FLOOD_SIBLING_THRESHOLD symptoms share the same group, the
    highest-CF symptom is kept at full weight and the remaining
    symptoms in that group are reduced by _FLOOD_REDUCTION_FACTOR
    (default 30% reduction).  Reduced symptoms are recorded in
    cascading_consequences[].

    Symptom grouping uses _FLOOD_GROUP_KEYS as a proxy for full KG
    ancestry lookup.  When M3/M4 integration adds faults.yaml lineage,
    replace the group-key lookup with ancestry-walk from the KG.

    source: v2-arbitrator §2.4
    source: R8 — > 3 sibling symptoms triggers cascade grouping
    """
    # Bucket symptoms by flood group key.
    groups: dict[str, list[tuple[str, float]]] = {}
    ungrouped: list[tuple[str, float]] = []

    for sym_id, cf in evidence.active_symptoms.items():
        group_key = _FLOOD_GROUP_KEYS.get(sym_id)
        if group_key is not None:
            groups.setdefault(group_key, []).append((sym_id, cf))
        else:
            ungrouped.append((sym_id, cf))

    cascading: list[str] = []

    for _group_key, entries in groups.items():
        if len(entries) <= _FLOOD_SIBLING_THRESHOLD:
            continue
        # Sort descending by CF; top symptom kept at full weight.
        entries.sort(key=lambda x: x[1], reverse=True)
        for sym_id, cf in entries[1:]:
            reduced_cf = cf * _FLOOD_REDUCTION_FACTOR
            evidence.active_symptoms[sym_id] = reduced_cf
            cascading.append(sym_id)

    evidence.cascading_consequences.extend(cascading)
