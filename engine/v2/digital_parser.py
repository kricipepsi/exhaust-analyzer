"""M1 — Digital parser: DTC + FF + OBD live → DigitalSymptoms.

R4 / L04: consumes ValidatedInput, never raw DiagnosticInput.
L18: fuel-status gate fires before any trim-derived symptom.

Source: v2-design-rules §4 M1 contract (digital_parser.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from engine.v2.dna_core import DNAOutput
from engine.v2.input_model import (
    FreezeFrameRecord,
    OBDRecord,
    ValidatedInput,
    extract_ect,
    extract_fuel_status,
)

# ── DTC → symptom mapping ─────────────────────────────────────────────────
# Each entry maps a DTC code (exact or family prefix) to its M1 symptom ID.
# Priority: exact match > family-prefix match.
# source: symptoms.yaml "emitted_by: M1" entries

_DTC_EXACT_MAP: dict[str, str] = {
    "P0171": "SYM_DTC_P0171",
    "P0172": "SYM_DTC_P0172",
    "P0401": "SYM_DTC_EGR",
    "P0101": "SYM_DTC_INDUCTION",
    "P0053": "SYM_DTC_HO2S_HEATER",
}

# source: symptoms.yaml "emitted_by: M1" entries
# Each entry is (frozenset of DTC codes, symptom_id).
# Adding a new DTC family requires ONE entry here — _map_dtc iterates this list.
# Prefix-based families (P06* → ECU_INTERNAL, P01* → SENSOR) are handled
# as suffix if-guards in _map_dtc because they cannot be expressed as frozensets.
_DTC_SET_MAP: list[tuple[frozenset[str], str]] = [
    (frozenset({"P0420", "P0430"}), "SYM_DTC_CATALYST"),
    (frozenset({f"P030{i}" for i in range(8)}), "SYM_DTC_MISFIRE"),
    (frozenset({"P0201", "P0202", "P0203", "P0204"}), "SYM_DTC_INJECTOR"),
    (frozenset({"P0299", "P0234", "P0235"}), "SYM_DTC_BOOST"),
    (frozenset({"P0011", "P0012"}), "SYM_DTC_CAMSHAFT_TIMING"),
    (frozenset({"P0324", "P0325"}), "SYM_DTC_KNOCK_SENSOR"),
]

# ── threshold constants ───────────────────────────────────────────────────

# source: docs/master_guides/freeze_frame/master_freeze_frame_guide.md §9
_FF_LOAD_HIGH_THRESHOLD: float = 70.0
_FF_LOAD_LOW_THRESHOLD: float = 30.0
_FF_LOAD_RPM_THRESHOLD: int = 1500

# source: docs/master_guides/freeze_frame/master_freeze_frame_guide.md §4
_FF_ECT_WARMUP_MAX: float = 70.0

# source: docs/master_guides/freeze_frame/master_freeze_frame_guide.md §9
_FF_IAT_ECT_DELTA_THRESHOLD: float = 30.0
_FF_TIMING_RETARD_THRESHOLD: float = -10.0

# source: docs/master_guides/fuel_trim/master_fuel_trim_guide.md §3.1
# Individual STFT/LTFT ±15% = strong trim deviation.
_TRIM_INDIVIDUAL_HIGH: float = 15.0

# source: docs/master_guides/fuel_trim/master_fuel_trim_guide.md §3.2
# STFT + LTFT sum ±10% = industry-standard strong signal.
_TRIM_SUM_THRESHOLD: float = 10.0

# source: docs/master_guides/fuel_trim/master_fuel_trim_guide.md §5
# Per-bank trim divergence > 10% = bank-specific fault.
_TRIM_BANK_IMBALANCE: float = 10.0

# source: docs/master_guides/o2_sensor/master_o2_sensor_guide.md §4.1
_O2_UPSTREAM_LAZY_LOW: float = 0.3
_O2_UPSTREAM_LAZY_HIGH: float = 0.7

# source: docs/master_guides/o2_sensor/master_o2_sensor_guide.md §4.2
_O2_DOWNSTREAM_ACTIVE_MIN: float = 0.3
_O2_DOWNSTREAM_ACTIVE_MAX: float = 0.7
_O2_DOWNSTREAM_STEADY_MIN: float = 0.7
_O2_DOWNSTREAM_STEADY_MAX: float = 0.8

# source: docs/master_guides/cold_start/master_cold_start_guide.md §4.1
_COLD_ECT_THRESHOLD: float = 75.0

# source: docs/master_guides/freeze_frame/master_freeze_frame_guide.md §7
_OPEN_LOOP_FUEL_STATUSES: frozenset[str] = frozenset({"OL_DRIVE", "OL_FAULT", "OL"})


# ── output dataclass ──────────────────────────────────────────────────────


@dataclass(slots=True)
class DigitalParserOutput:
    """M1 output — digital symptoms + breathing cluster + fuel-status gate.

    Consumed by M3 (arbitrator) and M4 (KG engine) as symptom evidence.
    """

    symptoms: list[str] = field(default_factory=list)
    breathing_cluster_efficiency: float | None = None
    open_loop_suppression: bool = False
    cold_engine: bool = False
    codes_cleared: bool = False


# ── public entry point ────────────────────────────────────────────────────


def parse_digital(
    validated_input: ValidatedInput,
    dna_output: DNAOutput,
) -> DigitalParserOutput:
    """Parse DTC, OBD PID, and freeze frame data into digital symptoms.

    R4 / L04: only consumes ValidatedInput — never raw DiagnosticInput.
    L18: fuel-status gate fires before any trim-derived symptom.

    Args:
        validated_input: Post-VL validated input container.
        dna_output: M0 vehicle DNA profile (era, tech mask, engine state).

    Returns:
        DigitalParserOutput with symptom list, breathing efficiency,
        and fuel-status / cold-engine gate flags.
    """
    symptoms: list[str] = []
    raw = validated_input.raw
    obd = raw.obd
    ff = raw.freeze_frame

    # ── fuel-status gate (L18) ──────────────────────────────────────────
    fuel_status = extract_fuel_status(obd, ff)
    ect = extract_ect(obd, ff)
    open_loop_suppression = _compute_open_loop_suppression(fuel_status, ect)
    cold_engine = ect is not None and ect < _COLD_ECT_THRESHOLD

    # ── DTC symptoms ────────────────────────────────────────────────────
    symptoms.extend(_parse_dtcs(raw.dtcs))

    # ── OBD PID symptoms ────────────────────────────────────────────────
    if obd is not None:
        symptoms.extend(_parse_obd_pids(obd, open_loop_suppression, raw.dtcs))

    # ── freeze frame symptoms ───────────────────────────────────────────
    if ff is not None:
        symptoms.extend(_parse_freeze_frame(ff))

    # ── context symptoms ────────────────────────────────────────────────
    if cold_engine:
        symptoms.append("SYM_CTX_COLD_ENGINE")

    # ── breathing cluster (speed-density, no MAF) ───────────────────────
    breathing_cluster_efficiency = _compute_breathing_efficiency(
        obd, ff, raw.vehicle_context.displacement_cc
    )

    # deduplicate while preserving order
    seen: set[str] = set()
    unique_symptoms: list[str] = []
    for s in symptoms:
        if s not in seen:
            seen.add(s)
            unique_symptoms.append(s)

    return DigitalParserOutput(
        symptoms=unique_symptoms,
        breathing_cluster_efficiency=breathing_cluster_efficiency,
        open_loop_suppression=open_loop_suppression,
        cold_engine=cold_engine,
        codes_cleared=False,  # set by VL/context; M1 reads it
    )


# ── fuel-status gate (L18) ───────────────────────────────────────────────


def _compute_open_loop_suppression(
    fuel_status: str | None, ect: float | None
) -> bool:
    """L18: fuel-status gate — suppress trim symptoms in open loop when warm.

    source: docs/master_guides/freeze_frame/master_freeze_frame_guide.md §7
      "If freeze frame fuel_system_status = OL or OL_FAULT for a fuel-trim
       DTC, the DTC was set before the O₂ sensor was active."
    """
    if fuel_status is None:
        return False
    fuel_upper = fuel_status.upper()
    if fuel_upper not in _OPEN_LOOP_FUEL_STATUSES:
        return False
    return ect is not None and ect >= _COLD_ECT_THRESHOLD


# ── DTC parsing ──────────────────────────────────────────────────────────


def _parse_dtcs(dtcs: list[str]) -> list[str]:
    """Map raw DTC codes to M1 symptom IDs.

    Exact match has priority over family-prefix match.
    A single DTC may map to at most one symptom.
    """
    symptoms: list[str] = []
    for dtc in dtcs:
        dtc_upper = dtc.strip().upper()
        if not dtc_upper:
            continue
        symptom = _map_dtc(dtc_upper)
        if symptom is not None:
            symptoms.append(symptom)
    return symptoms


def _map_dtc(dtc: str) -> str | None:
    """Map a single DTC code to its symptom ID. Returns None if no mapping."""
    # exact match first
    if dtc in _DTC_EXACT_MAP:
        return _DTC_EXACT_MAP[dtc]

    # set-based families — iterate _DTC_SET_MAP linearly
    for codes, symptom_id in _DTC_SET_MAP:
        if dtc in codes:
            return symptom_id

    # prefix-based families (cannot be expressed as frozensets)
    if dtc.startswith("P06"):
        return "SYM_DTC_ECU_INTERNAL"
    if dtc.startswith("P01") and dtc != "P0101":
        return "SYM_DTC_SENSOR"

    return None


# ── OBD PID parsing ──────────────────────────────────────────────────────


def _parse_obd_pids(
    obd: OBDRecord,
    open_loop_suppression: bool,
    dtcs: list[str],
) -> list[str]:
    """Derive symptoms from OBD Mode 1 live-data PIDs.

    L18: if open_loop_suppression is True, trim-derived symptoms are
    suppressed — the ECU is not using O2 feedback, so trims are frozen.
    """
    symptoms: list[str] = []

    # ── fuel trim symptoms (suppressed in open loop per L18) ──────────
    if not open_loop_suppression:
        symptoms.extend(_parse_trim_symptoms(obd))

    # ── O2 sensor symptoms ────────────────────────────────────────────
    symptoms.extend(_parse_o2_symptoms(obd, dtcs))

    # ── bank symmetry ─────────────────────────────────────────────────
    if not open_loop_suppression:
        symptoms.extend(_parse_bank_symmetry(obd))

    return symptoms


def _parse_trim_symptoms(obd: OBDRecord) -> list[str]:
    """Derive fuel trim symptoms from STFT/LTFT values.

    source: docs/master_guides/fuel_trim/master_fuel_trim_guide.md §3
    """
    symptoms: list[str] = []

    stft_b1 = obd.stft_b1
    ltft_b1 = obd.ltft_b1
    stft_b2 = obd.stft_b2
    ltft_b2 = obd.ltft_b2

    # check individual trims for high positive / negative on either bank
    for stft in (stft_b1, stft_b2):
        if stft is not None:
            if stft > _TRIM_INDIVIDUAL_HIGH:
                symptoms.append("SYM_TRIM_POSITIVE_HIGH")
                break
            if stft < -_TRIM_INDIVIDUAL_HIGH:
                symptoms.append("SYM_TRIM_NEGATIVE_HIGH")
                break

    for ltft in (ltft_b1, ltft_b2):
        if ltft is not None:
            if ltft > _TRIM_INDIVIDUAL_HIGH:
                if "SYM_TRIM_POSITIVE_HIGH" not in symptoms:
                    symptoms.append("SYM_TRIM_POSITIVE_HIGH")
                break
            if ltft < -_TRIM_INDIVIDUAL_HIGH:
                if "SYM_TRIM_NEGATIVE_HIGH" not in symptoms:
                    symptoms.append("SYM_TRIM_NEGATIVE_HIGH")
                break

    # check trim sums (STFT + LTFT per bank)
    for stft, ltft in ((stft_b1, ltft_b1), (stft_b2, ltft_b2)):
        if stft is not None and ltft is not None:
            trim_sum = stft + ltft
            if trim_sum > _TRIM_SUM_THRESHOLD:
                symptoms.append("SYM_TRIM_SUM_POSITIVE_HIGH")
            elif trim_sum < -_TRIM_SUM_THRESHOLD:
                symptoms.append("SYM_TRIM_SUM_NEGATIVE_HIGH")

    return symptoms


def _parse_o2_symptoms(obd: OBDRecord, dtcs: list[str]) -> list[str]:
    """Derive O2 sensor symptoms from voltage readings.

    source: docs/master_guides/o2_sensor/master_o2_sensor_guide.md §4
    """
    symptoms: list[str] = []

    o2_b1 = obd.o2_voltage_b1
    o2_b2 = obd.o2_voltage_b2

    # upstream lazy check (bank 1 primary)
    if o2_b1 is not None and _O2_UPSTREAM_LAZY_LOW <= o2_b1 <= _O2_UPSTREAM_LAZY_HIGH:
        symptoms.append("SYM_O2_UPSTREAM_LAZY")

    # downstream O2 (bank 2 voltage as proxy for post-cat when B2 present)
    has_catalyst_dtc = any(
        d in {"P0420", "P0430"} for d in (dtc.upper() for dtc in dtcs)
    )

    if o2_b2 is not None:
        if _O2_DOWNSTREAM_ACTIVE_MIN <= o2_b2 <= _O2_DOWNSTREAM_ACTIVE_MAX:
            if has_catalyst_dtc:
                symptoms.append("SYM_O2_DOWNSTREAM_ACTIVE")
            else:
                symptoms.append("SYM_O2_DOWNSTREAM_STEADY")
        elif _O2_DOWNSTREAM_STEADY_MIN <= o2_b2 <= _O2_DOWNSTREAM_STEADY_MAX:
            symptoms.append("SYM_O2_DOWNSTREAM_STEADY")

    return symptoms


def _parse_bank_symmetry(obd: OBDRecord) -> list[str]:
    """Derive bank-to-bank fuel trim symmetry symptoms.

    source: docs/master_guides/fuel_trim/master_fuel_trim_guide.md §4
    """
    symptoms: list[str] = []

    stft_b1 = obd.stft_b1
    ltft_b1 = obd.ltft_b1
    stft_b2 = obd.stft_b2
    ltft_b2 = obd.ltft_b2

    # need both banks to assess symmetry
    if None in (stft_b1, ltft_b1, stft_b2, ltft_b2):
        return symptoms

    trim_sum_b1 = stft_b1 + ltft_b1  # type: ignore[operator]
    trim_sum_b2 = stft_b2 + ltft_b2  # type: ignore[operator]

    b1_pos = trim_sum_b1 > _TRIM_BANK_IMBALANCE
    b1_neg = trim_sum_b1 < -_TRIM_BANK_IMBALANCE
    b2_pos = trim_sum_b2 > _TRIM_BANK_IMBALANCE
    b2_neg = trim_sum_b2 < -_TRIM_BANK_IMBALANCE

    # both banks trimming significantly in the same direction
    if (b1_pos and b2_pos) or (b1_neg and b2_neg):
        symptoms.append("SYM_TRIM_GLOBAL_BOTH_BANKS")
        return symptoms

    # one bank significantly diverges from the other
    bank_delta = abs(trim_sum_b1 - trim_sum_b2)  # type: ignore[arg-type]
    if bank_delta > _TRIM_BANK_IMBALANCE:
        symptoms.append("SYM_TRIM_LOCAL_ONE_BANK")
        # classify which bank is lean/rich
        if trim_sum_b2 > _TRIM_BANK_IMBALANCE:
            symptoms.append("SYM_BANK2_LEAN")
        elif trim_sum_b2 < -_TRIM_BANK_IMBALANCE:
            symptoms.append("SYM_BANK2_RICH")

    return symptoms


# ── freeze frame parsing ─────────────────────────────────────────────────


def _parse_freeze_frame(ff: FreezeFrameRecord) -> list[str]:
    """Derive symptoms from freeze frame data.

    All thresholds cite docs/master_guides/freeze_frame/master_freeze_frame_guide.md.
    """
    symptoms: list[str] = []

    # source: master_freeze_frame_guide.md §5.1 — open loop at fault
    if ff.fuel_status is not None and ff.fuel_status.upper() in _OPEN_LOOP_FUEL_STATUSES:
        symptoms.append("SYM_FF_OPEN_LOOP_AT_FAULT")

    # source: master_freeze_frame_guide.md §5.2 — high load at low RPM
    if (
        ff.load_pct is not None
        and ff.rpm is not None
        and ff.load_pct > _FF_LOAD_HIGH_THRESHOLD
        and ff.rpm < _FF_LOAD_RPM_THRESHOLD
    ):
        symptoms.append("SYM_FF_LOAD_HIGH_AT_LOW_RPM")

    # source: master_freeze_frame_guide.md §5.3 — ECT warmup at fault
    if ff.ect_c is not None and ff.ect_c < _FF_ECT_WARMUP_MAX:
        symptoms.append("SYM_FF_ECT_WARMUP")

    # source: master_freeze_frame_guide.md §5.4 — IAT/ECT sensor bias
    if (
        ff.iat_c is not None
        and ff.ect_c is not None
        and ff.rpm is not None
        and abs(ff.iat_c - ff.ect_c) > _FF_IAT_ECT_DELTA_THRESHOLD
        and ff.rpm == 0
    ):
        symptoms.append("SYM_FF_IAT_ECT_BIASED")

    # source: master_freeze_frame_guide.md §5.5 — severe ignition retard
    # Timing advance not available in current FreezeFrameRecord; checked
    # via OBD VVT angle as fallback.  Skipped when neither is available.
    # TODO: add ignition_timing_advance to FreezeFrameRecord (T-P3-3b).

    # source: master_freeze_frame_guide.md §5.6 — codes cleared
    # Set externally (VL or app context); M1 cannot detect this from FF alone.

    return symptoms


# ── breathing cluster (speed-density, no MAF) ────────────────────────────


def _compute_breathing_efficiency(
    obd: OBDRecord | None,
    ff: FreezeFrameRecord | None,
    displacement_cc: int,
) -> float | None:
    """Compute volumetric efficiency proxy via speed-density model.

    Uses MAP / BARO as a simplified breathing efficiency ratio.
    No MAF — this is the speed-density model for non-MAF vehicles.

    source: docs/master_guides/air_induction/master_air_induction_guide.md §2
      Speed-density: ECU estimates charge mass from MAP, IAT, RPM, and a
      stored VE table.  MAP/BARO ratio approximates cylinder filling.

    Returns:
        Breathing efficiency as a fraction (0.0–1.0+), or None if MAP or
        BARO is unavailable.  Values > 1.0 indicate boost (turbo/supercharger).
    """
    map_kpa = _extract_map(obd, ff)
    baro_kpa = _extract_baro(obd, ff)

    if map_kpa is None or baro_kpa is None or baro_kpa <= 0:
        return None

    return map_kpa / baro_kpa


def _extract_map(obd: OBDRecord | None, ff: FreezeFrameRecord | None) -> float | None:
    """Extract MAP (kPa) from OBD (priority) or freeze frame."""
    if obd is not None and obd.map_kpa is not None:
        return obd.map_kpa
    if ff is not None and ff.map_kpa is not None:
        return ff.map_kpa
    return None


def _extract_baro(
    obd: OBDRecord | None, ff: FreezeFrameRecord | None
) -> float | None:
    """Extract barometric pressure (kPa) from OBD (priority) or freeze frame."""
    if obd is not None and obd.baro_kpa is not None:
        return obd.baro_kpa
    if ff is not None and ff.baro_kpa is not None:
        return ff.baro_kpa
    return None
