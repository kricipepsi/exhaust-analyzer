"""C3 auditor probes — OBDLab and DTCLab emitters.

Each test asserts a claim the repo makes; a FAILING test is the evidence of a defect. The
assertion message carries the observed output. Run from the repo root:

    python -m pytest -q -p no:cacheprovider audit/scratch/C3/test_c3_probes.py -rA

Composition-level probes put apps/ui, labs/comlab and apps/wired on sys.path (the same
F-C4-1 / F-C1-5 work-around the C5 harness uses) so that COMLab's verdict path runs.
"""

from __future__ import annotations

import ast
import logging
import math
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
for p in ("apps/ui", "labs/comlab", "apps/wired"):
    if str(ROOT / p) not in sys.path:
        sys.path.insert(0, str(ROOT / p))
logging.disable(logging.WARNING)

from dtclab.core.data_fusion_sanitizer import DataFusionSanitizer  # noqa: E402
from dtclab.ranking import classify_top3, rank_candidates  # noqa: E402
from dtclab.schemas.dna_view import (  # noqa: E402
    AirMeteringStrategy as DAir,
    DtcEmissionsView,
    DtcLabDnaView,
    EuroEmissionCategory,
    ResolvedHorizon,
    VinConfidence as DConf,
)
from obdlab.core.analytics_preconditions import AnalyticsPreconditions  # noqa: E402
from obdlab.core.sensor_signal_translator import SensorSignalTranslator  # noqa: E402
from obdlab.schemas.dna_view import (  # noqa: E402
    AirMeteringStrategy,
    InductionType,
    O2SensorType,
    ObdLabDnaView,
    VinConfidence,
)
from obdlab.schemas.vocabulary import TrimAnalyticsGate  # noqa: E402

# A HIGH-confidence, narrowband, EGR-less VIN (vinlab.decode -> CITROEN 2010, HIGH,
# has_catalyst=True, egr_equipped=False). Found by decoding every VIN in labs/vinlab/tests
# and apps/wired.
VIN_HIGH = "VF7SA5FR8AW511081"
TRIAGE = {"tier_1": "lack_of_power_hesitation", "tier_2": "flat_sluggish_always",
          "occurs_during": "always", "engine_state": "running", "load_state": "idle"}
GAS_RICH = {"hc": 400, "nox": 20, "co": 3.0, "co2": 12.5, "o2": 0.3}
GAS_STOICH = {"hc": 80, "nox": 50, "co": 0.3, "co2": 14.8, "o2": 0.3}
FF12 = dict(calculated_load_pct=20.0, engine_rpm=800, coolant_temp_c=90.0, short_term_ft1=1.0,
            long_term_ft1=2.0, manifold_pressure_kpa=35.0, vehicle_speed_kmh=0,
            ignition_advance_deg=10.0, intake_air_temp_c=25.0, maf_gps=3.0,
            throttle_pos_pct=0.0, fuel_system_status="CL")

# The OBD dict shape apps/ui/ui_payload.py:923-976 builds (basic fields + bank contract + O2
# + fuel status). It never contains drive_cycles_since_clear / active_dtcs / throttle_pos /
# dfco_active (see test_f3 census).
UI_OBD_WARM = {"coolant_temp_c": 90.0, "calculated_engine_load_pct": 20.0, "shrtft1": 1.0,
               "longft1": 2.0, "engine_rpm": 800, "number_of_banks": 1, "shrtft2": None,
               "longft2": None, "pid_oxygen_sensor_volts": 0.45, "fuel_sys_status": "CL"}

T = SensorSignalTranslator()


def dna(**over) -> ObdLabDnaView:
    d = dict(engine_displacement_liters=2.0, rated_rpm=6500, stress_idle_rpm_target=3500,
             air_metering_strategy=AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK,
             upstream_o2_type=O2SensorType.NARROWBAND_0_TO_1V,
             induction_type=InductionType.NATURALLY_ASPIRATED, confidence=VinConfidence.HIGH)
    d.update(over)
    return ObdLabDnaView(**d)


BASE = dict(engine_rpm=800, coolant_temp_c=90.0, calculated_engine_load_pct=20.0, shrtft1=2.0,
            longft1=3.0, number_of_banks=1, shrtft2=None, longft2=None,
            pid_oxygen_sensor_volts=0.45, fuel_sys_status="CL", mass_airflow_gps=3.0,
            manifold_vacuum_kpa=35.0, intake_air_temp_c=30.0, drive_cycles_since_clear=5)


def tr(d=None, drop=(), **upd):
    x = dict(BASE)
    x.update(upd)
    for k in drop:
        x.pop(k, None)
    return T.translate(x, dna() if d is None else d)


def dtc_view(has_catalyst=True, egr=True, conf=DConf.HIGH) -> DtcLabDnaView:
    return DtcLabDnaView(make="X", model="Y", model_year=2010,
                         euro_emission_category=EuroEmissionCategory.EURO_5,
                         air_metering_strategy=DAir.MAP_SPEED_DENSITY,
                         resolved_horizon=ResolvedHorizon.HORIZON_MODERN,
                         emissions=DtcEmissionsView(has_catalyst=has_catalyst, egr_equipped=egr),
                         confidence=conf)


def sanitize(raw, view=None, mode06=None, ff=None):
    return DataFusionSanitizer(view).sanitize(raw, dict(ff or FF12), mode06 or {})


def _verdict(r) -> str:
    v = r.diagnostic_verdict
    return (f"{v.fault_code} {v.fault_family} conf={v.confidence_score:.3f} "
            f"abstained={v.abstained} pdelta={r.performance_analytics.lambda_perception_delta}")


def _composition():
    from wired import composition as C  # noqa: PLC0415
    return C


# =============================================================================================
# F-C3-1  Frozen (cold-engine) lambda sentinel 1.0 is emitted as a measured lambda and decides
#         the verdict
# =============================================================================================
def test_f1_cold_engine_lambda_sentinel_decides_verdict():
    C = _composition()
    orig = C._run_obdlab
    out = []
    obd = {"coolant_temp_c": 40.0, "shrtft1": 0.0, "longft1": 0.0, "engine_rpm": 800,
           "number_of_banks": 1, "shrtft2": None, "longft2": None, "fuel_sys_status": "OL"}
    verdicts = {}
    for volts in (0.85, 0.15):
        o = dict(obd, pid_oxygen_sensor_volts=volts)
        lab = orig(o, C._build_fallback_vin_dna(VIN_HIGH))
        r = C.diagnose({"vin": VIN_HIGH, "triage": TRIAGE,
                        "gas": dict(GAS_RICH, engine_state="STABILIZED_IDLE"), "obd": o})
        verdicts[volts] = _verdict(r)
        out.append(f"volts={volts}: OBDLab lambda={lab.normalized_obd_lambda} "
                   f"warmed={lab.engine_warmed} trims={lab.shrtft1}/{lab.longft1} -> {_verdict(r)}")
    # counterfactual: the same cold OBD payload with the frozen lambda channel left empty
    C._run_obdlab = lambda oi, vd: orig(oi, vd).model_copy(update={"normalized_obd_lambda": None})
    try:
        r_none = C.diagnose({"vin": VIN_HIGH, "triage": TRIAGE,
                             "gas": dict(GAS_RICH, engine_state="STABILIZED_IDLE"),
                             "obd": dict(obd, pid_oxygen_sensor_volts=0.85)})
    finally:
        C._run_obdlab = orig
    out.append(f"same cold payload, normalized_obd_lambda=None -> {_verdict(r_none)}")
    msg = "\n".join(out)
    assert verdicts[0.85] == _verdict(r_none), msg


# =============================================================================================
# F-C3-2  The composition never hands DTCLab its DNA view: HIGH-confidence DNA gates never apply
# =============================================================================================
def test_f2_dtclab_never_receives_dna_view():
    C = _composition()
    import vinlab  # noqa: PLC0415

    d = vinlab.decode(VIN_HIGH)
    orig = C.DataFusionSanitizer
    out = [f"vinlab.decode({VIN_HIGH}): confidence={d.confidence.value} "
           f"has_catalyst={d.emissions.has_catalyst} egr_equipped={d.emissions.egr_equipped}"]
    bad = []
    cases = ((["P0401"], None, dtc_view(has_catalyst=True, egr=False)),
             (["P0420"], {"de_cat": True}, dtc_view(has_catalyst=False, egr=False)))
    for codes, ov, view in cases:
        p = {"vin": VIN_HIGH, "triage": TRIAGE, "gas": dict(GAS_STOICH, engine_state="STABILIZED_IDLE"),
             "obd": dict(UI_OBD_WARM),
             "dtc": {"codes_cleared": False, "raw_dtcs": {"$03": codes}, "raw_freeze_frame": dict(FF12)}}
        if ov:
            p["overrides"] = ov
        C.DataFusionSanitizer = orig
        tags_prod = C._run_dtclab(p["dtc"]).routing_tags
        v_prod = _verdict(C.diagnose(p))
        C.DataFusionSanitizer = lambda *a, _v=view, **k: orig(dna_view=_v)
        try:
            tags_gated = C._run_dtclab(p["dtc"]).routing_tags
            v_gated = _verdict(C.diagnose(p))
        finally:
            C.DataFusionSanitizer = orig
        out.append(f"{codes} overrides={ov}: production tags={[t.value for t in tags_prod]} -> {v_prod}")
        out.append(f"{'':>8}with the DNA view (HIGH)  tags={[t.value for t in tags_gated]} -> {v_gated}")
        if tags_prod != tags_gated:
            bad.append(codes)
    src = (ROOT / "apps/wired/wired/composition.py").read_text(encoding="utf-8")
    out.append("composition call: " + re.search(r"DataFusionSanitizer\([^)]*\)", src).group(0))
    assert not bad, "\n".join(out)


# =============================================================================================
# F-C3-3  trim_analytics_gate: absent drive-cycle count reads as "recently cleared"; every
#         UI-shaped OBD payload emits CODES_RECENTLY_CLEARED
# =============================================================================================
def test_f3_trim_gate_constant_for_ui_payloads():
    C = _composition()
    keys = ("drive_cycles_since_clear", "active_dtcs", "throttle_pos", "dfco_active")
    census = {}
    for k in keys:
        r = subprocess.run(["grep", "-rln", "--include=*.py", f"[\"']{k}[\"']", "apps"],
                           cwd=ROOT, capture_output=True, text=True)
        census[k] = [f for f in r.stdout.split() if "/tests/" not in f]
    gates = []
    for ect in (80.0, 90.0, 100.0):
        for fss in ("CL",):
            o = dict(UI_OBD_WARM, coolant_temp_c=ect, fuel_sys_status=fss)
            gates.append(C._run_obdlab(o, C._build_fallback_vin_dna(VIN_HIGH)).trim_analytics_gate.value)
    with_count = C._run_obdlab(dict(UI_OBD_WARM, drive_cycles_since_clear=5),
                               C._build_fallback_vin_dna(VIN_HIGH)).trim_analytics_gate.value
    msg = (f"producers of gate inputs under apps/ (non-test): {census}\n"
           f"UI-shaped warm closed-loop payloads -> {gates}\n"
           f"same payload + drive_cycles_since_clear=5 -> {with_count}")
    assert "VALID" in gates, msg


# =============================================================================================
# F-C3-4  WOT gate and wideband-offset guard read `throttle_pos`; the validated, emitted field
#         is `throttle_pos_pct`
# =============================================================================================
def test_f4_wot_gate_reads_unvalidated_key():
    p_pct = tr(throttle_pos_pct=100.0)
    p_raw = tr(throttle_pos=250.0)
    wb = dna(upstream_o2_type=O2SensorType.WIDEBAND_LINEAR)
    p_wb = tr(d=wb, pid_wideband_equivalence_ratio=1.2, throttle_pos_pct=100.0)
    msg = (f"throttle_pos_pct=100 -> gate={p_pct.trim_analytics_gate.value} "
           f"emitted throttle_pos_pct={p_pct.throttle_pos_pct}\n"
           f"throttle_pos=250 (no bounds row) -> gate={p_raw.trim_analytics_gate.value} "
           f"emitted throttle_pos_pct={p_raw.throttle_pos_pct}\n"
           f"wideband lambda 1.2 at throttle_pos_pct=100 -> o2_failure_mode={p_wb.o2_failure_mode.value}")
    assert p_pct.trim_analytics_gate == TrimAnalyticsGate.WOT_ACTIVE, msg


# =============================================================================================
# F-C3-5  IAT 0 °C is treated as missing and replaced by 25 °C in the VE formula
# =============================================================================================
def test_f5_iat_zero_replaced_by_25c():
    rows = []
    # MAF chosen so that true VE (IAT 0 °C) sits just below a fault threshold / just above
    flips = []
    for label, maf, mapk in (("collapse side", 4.17, 50.0), ("skew side", 7.48, 50.0)):
        p0 = tr(intake_air_temp_c=0.0, mass_airflow_gps=maf, manifold_vacuum_kpa=mapk)
        p001 = tr(intake_air_temp_c=0.01, mass_airflow_gps=maf, manifold_vacuum_kpa=mapk)
        p25 = tr(intake_air_temp_c=25.0, mass_airflow_gps=maf, manifold_vacuum_kpa=mapk)
        rows.append(f"{label}: IAT 0.00 -> ve={p0.ve_pct:.2f} {p0.ve_validity.value} | "
                    f"IAT 0.01 -> ve={p001.ve_pct:.2f} {p001.ve_validity.value} | "
                    f"IAT 25 -> ve={p25.ve_pct:.2f} {p25.ve_validity.value}; emitted IAT={p0.intake_air_temp_c}")
        flips.append(p0.ve_validity != p001.ve_validity)
    assert not any(flips), "\n".join(rows)


# =============================================================================================
# F-C3-6  Any operating point outside the bucket bands is labelled STABILIZED_IDLE and gets
#         idle VE fault triggers
# =============================================================================================
def test_f6_unmatched_rpm_falls_back_to_stabilized_idle():
    rows, bad = [], []
    for rpm, load, maf, mapk in ((0, 0.0, 0.0, 100.0), (1500, 20.0, 6.0, 40.0),
                                 (3000, 70.0, 47.0, 90.0), (6000, 90.0, 120.0, 98.0),
                                 (800, 80.0, 6.0, 90.0)):
        p = tr(engine_rpm=rpm, calculated_engine_load_pct=load, mass_airflow_gps=maf,
               manifold_vacuum_kpa=mapk)
        rows.append(f"rpm={rpm} load={load}% -> bucket={p.rpm_state_bucket.value} "
                    f"ve={p.ve_pct:.1f} ve_validity={p.ve_validity.value}")
        in_band = 650 <= rpm <= 900 and load < 30
        if p.rpm_state_bucket.value == "STABILIZED_IDLE" and not in_band:
            bad.append(rpm)
    assert not bad, "\n".join(rows)


# =============================================================================================
# F-C3-7  ECT 70–74.9 °C: trim_analytics_gate VALID while engine_warmed=False and trims frozen
# =============================================================================================
def test_f7_ect_70_to_75_contradictory_channels():
    rows, bad = [], []
    for ect in (69.9, 70.0, 72.0, 74.9, 75.0):
        p = tr(coolant_temp_c=ect, shrtft1=12.0, longft1=10.0)
        rows.append(f"ECT={ect}: gate={p.trim_analytics_gate.value} engine_warmed={p.engine_warmed} "
                    f"bucket={p.rpm_state_bucket.value} total_trim={p.total_trim_correction_delta} "
                    f"raw stft/ltft={p.shrtft1}/{p.longft1}")
        if p.trim_analytics_gate == TrimAnalyticsGate.VALID and not p.engine_warmed:
            bad.append(ect)
    assert not bad, "\n".join(rows)


# =============================================================================================
# F-C3-8  Out-of-range wideband lambda is clamped silently: NO_FAULT, mode discarded; the
#         in-range offset is flagged but a larger one is not
# =============================================================================================
def test_f8_wideband_clamp_unflagged():
    wb = dna(upstream_o2_type=O2SensorType.WIDEBAND_LINEAR)
    rows = []
    res = {}
    for r in (0.5, 0.69, 0.70, 1.30, 1.31, 1.6, math.inf):
        p = tr(d=wb, pid_wideband_equivalence_ratio=r)
        res[r] = p.o2_failure_mode.value
        rows.append(f"wideband ratio {r} -> normalized_obd_lambda={p.normalized_obd_lambda} "
                    f"o2_failure_mode={p.o2_failure_mode.value}")
    emitted = sorted(T.translate.__annotations__.keys())  # noqa: F841 (documentation only)
    payload_fields = set(type(tr()).model_fields)
    rows.append(f"'o2_normalization_mode' in OBDLivePayload fields: {'o2_normalization_mode' in payload_fields}")
    assert res[1.31] != "NO_FAULT" and res[0.5] != "NO_FAULT", "\n".join(rows)


# =============================================================================================
# F-C3-9  NaN / bool O2 inputs pass the type guard and become a definite lambda
# =============================================================================================
def test_f9_nan_and_bool_o2_inputs():
    rows, bad = [], []
    for v in (float("nan"), True, False):
        try:
            p = tr(pid_oxygen_sensor_volts=v)
            rows.append(f"pid_oxygen_sensor_volts={v!r} -> lambda={p.normalized_obd_lambda} "
                        f"o2_failure_mode={p.o2_failure_mode.value}")
            bad.append(v)
        except Exception as e:  # noqa: BLE001
            rows.append(f"pid_oxygen_sensor_volts={v!r} -> {type(e).__name__}")
    for v in (float("nan"), 72.0):
        try:
            tr(coolant_temp_c=v)
            rows.append(f"coolant_temp_c={v!r} -> accepted")
        except Exception as e:  # noqa: BLE001
            rows.append(f"coolant_temp_c={v!r} -> {type(e).__module__}.{type(e).__name__}")
    assert not bad, "\n".join(rows)


# =============================================================================================
# F-C3-10  rank_candidates ignores the DNA gate the mapper enforces, and spreads one Mode $06
#          monitor over every family
# =============================================================================================
def test_f10_rank_candidates_bypasses_dna_gate():
    v = dtc_view(has_catalyst=False, egr=False)
    p = sanitize({"$03": ["P0420"]}, v)
    ranked = rank_candidates(p, dna_view=v)
    top = classify_top3(p, dna_view=v)
    p2 = sanitize({"$07": ["P0171"]}, mode06={"MID_21_TID_01": -50.0})
    r2 = rank_candidates(p2)
    msg = (f"HIGH DNA, has_catalyst=False, confirmed P0420: routing_tags={[t.value for t in p.routing_tags]} "
           f"rank={ranked} top3={top}\n"
           f"pending P0171 + catalyst monitor MID_21 CRITICAL_FAIL: rank={r2}")
    assert not ranked, msg


# =============================================================================================
# F-C3-11  Ranking ties are broken alphabetically, against the wiki §12 hierarchy
# =============================================================================================
def test_f11_rank_tie_break_vs_wiki_hierarchy():
    rows, bad = [], []
    # wiki 12_ranking_discriminator.md: misfire > lean_condition > catalyst_failure;
    # confirmed $03 > pending $07
    cases = (({"$03": ["P0171", "P0420"]}, dtc_view(), "lean_condition"),
             ({"$03": ["P0300", "P0171"]}, None, "misfire"),
             ({"$03": ["P0420"], "$07": ["P0171"]}, None, "lean_condition"))
    for raw, view, expected_first in cases:
        r = rank_candidates(sanitize(raw, view), dna_view=view)
        got = [(c.family, c.raw_confidence, c.match_type.value) for c in r]
        rows.append(f"{raw} dna={'HIGH' if view else None}: {got} (wiki first: {expected_first})")
        if r[0].family != expected_first:
            bad.append(raw)
    assert not bad, "\n".join(rows)


# =============================================================================================
# F-C3-12  The Phase-2 scorer has no production caller, and its family relation disagrees
#          with both COMLab tag->family tables
# =============================================================================================
def test_f12_ranking_unconsumed_and_family_maps_disagree():
    import yaml  # noqa: PLC0415

    from dtclab.family_map import ROUTING_TAG_TO_FAMILY  # noqa: PLC0415
    from registry import integration_shim as S  # noqa: PLC0415

    r = subprocess.run(["grep", "-rln", "--include=*.py", r"classify_top3\|rank_candidates",
                        "apps", "labs/comlab", "harness"], cwd=ROOT, capture_output=True, text=True)
    callers = [f for f in r.stdout.split() if "/tests/" not in f]
    disc = yaml.safe_load((ROOT / "labs/comlab/comlab/config/tag_discriminator.yaml")
                          .read_text(encoding="utf-8"))["mappings"]
    hints = {k.value: sorted(f.value for f in v) for k, v in S._DTC_ROUTING_TAG_FAMILY_HINTS.items()}
    diffs = []
    for tag, fam in ROUTING_TAG_TO_FAMILY.items():
        h = hints.get(tag.value)
        dfam = disc.get(tag.value, {}).get("family")
        if (h and fam not in h) or (dfam and dfam != fam):
            diffs.append(f"{tag.value}: dtclab={fam} shim={h} discriminator={dfam}")
    msg = f"non-test callers of rank_candidates/classify_top3 outside dtclab: {callers}\n" + "\n".join(diffs)
    assert callers and not diffs, msg


# =============================================================================================
# F-C3-13  CYLINDER_FLUID_MISFIRE (coolant intrusion) is emitted for every closed-loop P030x
# =============================================================================================
def test_f13_fluid_misfire_tag_from_dtc_plus_cl_only():
    rows, hits = [], 0
    for code in ("P0300", "P0301", "P0304", "P0310", "P0312"):
        p = sanitize({"$03": [code]})
        tags = [t.value for t in p.routing_tags]
        hits += "CYLINDER_FLUID_MISFIRE" in tags
        rows.append(f"{code} + FF fuel_system_status=CL (no coolant data at all) -> {tags}")
    src = (ROOT / "labs/dtclab/dtclab/core/freeze_frame_extractor.py").read_text(encoding="utf-8")
    sig = ast.get_source_segment(src, next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)
                                           and n.name == "evaluate_coolant_dtc_context"))
    rows.append("inputs of evaluate_coolant_dtc_context: " + re.search(r"\(([^)]*)\)", sig).group(1).replace("\n", " "))
    cited = list(ROOT.rglob("CoolantLeakSig.md"))
    rows.append(f"CoolantLeakSig.md files in repo: {cited}")
    assert hits == 0, "\n".join(rows)


# =============================================================================================
# F-C3-15  SEMANTIC_ERROR can never be emitted
# =============================================================================================
def test_f15_semantic_error_unreachable():
    src = (ROOT / "labs/obdlab/obdlab/core/semantic_consistency_checker.py").read_text(encoding="utf-8")
    appended = re.findall(r'gates_passed\.append\("([^"]+)"\)', src)
    raising = re.findall(r"def (_physics_gate_\d)", src)
    tsrc = (ROOT / "labs/obdlab/obdlab/core/sensor_signal_translator.py").read_text(encoding="utf-8")
    call = re.search(r"semantic_gates_passed=\(([^)]*)\)", tsrc).group(1)
    # Every gate either raises or appends, so the count is always len(appended) when a payload exists
    outcomes = set()
    for upd in ({}, {"coolant_temp_c": 76.0, "fuel_sys_status": "OL"}, {"vss": 50.0, "engine_rpm": 500},
                {"fuel_sys_status": "OL_DRIVE"}, {"shrtft1": 127.0}):
        outcomes.add(tr(**upd).trim_analytics_gate.value)
    msg = (f"gates appended: {appended}; gate methods: {raising}; translator passes ({call}); "
           f"gate outcomes over probes: {sorted(outcomes)}")
    assert "SEMANTIC_ERROR" in outcomes, msg


# =============================================================================================
# F-C3-16  §3.2 alternate-unit path is unguarded
# =============================================================================================
def test_f16_unit_conversion_unguarded():
    from obdlab.core.exceptions import PIDValidationError  # noqa: PLC0415

    rows, bad = [], []
    for upd, drop in (({"coolant_temp_f": None}, ("coolant_temp_c",)),
                      ({"coolant_temp_f": "194"}, ("coolant_temp_c",)),
                      ({"mass_airflow_lbmin": None}, ("mass_airflow_gps",))):
        try:
            tr(drop=drop, **upd)
            rows.append(f"{upd} -> accepted")
        except PIDValidationError as e:
            rows.append(f"{upd} -> PIDValidationError {e}")
        except Exception as e:  # noqa: BLE001
            rows.append(f"{upd} -> {type(e).__name__}: {e}")
            bad.append(upd)
    p = tr(drop=("manifold_vacuum_kpa",), manifold_vacuum_inhg=18.0)
    rows.append(f"manifold_vacuum_inhg=18 (a typical idle vacuum-gauge reading) -> manifold_vacuum_kpa="
                f"{p.manifold_vacuum_kpa:.1f} ve={p.ve_pct:.1f} {p.ve_validity.value}")
    assert not bad, "\n".join(rows)


# =============================================================================================
# F-C3-17  A DTC with a trailing newline passes the canonical regex and the payload validator
# =============================================================================================
def test_f17_dtc_trailing_newline_passes():
    p = sanitize({"$03": ["P0171\n"]})
    msg = f"confirmed_dtcs={p.confirmed_dtcs!r} routing_tags={[t.value for t in p.routing_tags]}"
    assert all(re.fullmatch(r"[BCPU][0-3][0-9A-F]{3}", c) for c in p.confirmed_dtcs), msg


# =============================================================================================
# F-C3-18  The O2-fault DTC range differs between OBDLab's gate and DTCLab's O2_HISTORY
# =============================================================================================
def test_f18_o2_dtc_range_mismatch():
    from obdlab.core.analytics_preconditions import O2_FAULT_DTCS  # noqa: PLC0415

    rows = []
    for code in ("P0148", "P0149", "P0160", "P0161", "P0162", "P0167"):
        gate = AnalyticsPreconditions.evaluate({"coolant_temp_c": 90.0, "fuel_system_status": "CL",
                                                "active_dtcs": [code], "drive_cycles_since_clear": 5})
        tags = [t.value for t in sanitize({"$03": [code]}).routing_tags]
        rows.append(f"{code}: OBDLab gate={gate.value} DTCLab tags={tags}")
    mism = [r for r in rows if ("O2_FAULT_ACTIVE" in r) != ("O2_HISTORY" in r)]
    assert not mism, "\n".join(rows) + f"\nOBDLab set size={len(O2_FAULT_DTCS)}"


# =============================================================================================
# F-C3-19  Zero MAP or zero MAF on a running engine gives VE 0.0 with ve_validity VALID
# =============================================================================================
def test_f19_zero_map_or_maf_is_valid_ve():
    rows, bad = [], []
    for upd in ({"manifold_vacuum_kpa": 0.0}, {"mass_airflow_gps": 0.0}):
        p = tr(**upd)
        rows.append(f"rpm 800, {upd} -> ve_pct={p.ve_pct} ve_validity={p.ve_validity.value}")
        if p.ve_validity.value == "VALID":
            bad.append(upd)
    assert not bad, "\n".join(rows)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(pytest.main([__file__, "-q", "-rA", "-p", "no:cacheprovider"]))


# =============================================================================================
# F-C3-14  In-bounds inputs whose computed VE exceeds 200 % abort translate() with a raw
#          pydantic ValidationError
# =============================================================================================
def test_f14_ve_over_200_aborts_translate():
    from obdlab.core.exceptions import PIDValidationError, SemanticConsistencyError  # noqa: PLC0415

    rows, bad = [], []
    for upd in ({"mass_airflow_gps": 20.0}, {"manifold_vacuum_kpa": 5.0},
                {"mass_airflow_gps": 655.35}, {"coolant_temp_c": float("nan")}):
        try:
            p = tr(**upd)
            rows.append(f"idle 800 rpm, {upd} -> ve={p.ve_pct}")
        except (PIDValidationError, SemanticConsistencyError) as e:
            rows.append(f"{upd} -> documented {type(e).__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            first = str(e).splitlines()[1:3]
            rows.append(f"{upd} -> {type(e).__module__}.{type(e).__name__}: {first}")
            bad.append(upd)
    assert not bad, "\n".join(rows)
