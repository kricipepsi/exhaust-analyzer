"""C5 auditor probes — public UI payload (apps/ui/ui_payload.py) and app (apps/ui/app.py).

Each test asserts a claim the repo makes; a FAILING test is the evidence of a defect. The
assertion message carries the observed output. Run from the repo root:

    python -m pytest -q -p no:cacheprovider audit/scratch/C5/test_c5_probes.py -rA

Widget dicts come from c5_lib.base_widgets(), a copy of what app.py:789-918 hands to
build_diagnose_payload() at click time. AppTest probes drive the real app.py headless.
labs/comlab is put on sys.path (F-C4-1 work-around) except where a test says otherwise.
"""

from __future__ import annotations

import copy
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import c5_lib as L  # noqa: E402
from c5_lib import GOOD_GAS, base_widgets, decoded_widgets, run, verdict_str  # noqa: E402

ROOT = L.ROOT
SYM = dict(triage_tier_1="⬇️ Lack of Power / Hesitation", triage_tier_2="Flat / sluggish always")
OBD5 = dict(obd_upstream_o2_val=0.45, obd_shrtft1=1.0, obd_longft1=2.0, obd_engine_rpm=800,
            obd_coolant_temp_c=90.0)
FF12 = dict(ff_calculated_load_pct=20.0, ff_engine_rpm=800, ff_coolant_temp_c=90.0,
            ff_short_term_ft1=1.0, ff_long_term_ft1=2.0, ff_manifold_pressure_kpa=35,
            ff_vehicle_speed_kmh=0, ff_ignition_advance_deg=10.0, ff_intake_air_temp_c=25.0,
            ff_maf_gps=3.0, ff_throttle_pos_pct=0.0, ff_fuel_system_status="CL")


def _corpus():
    sys.path.insert(0, str(ROOT / "apps/wired"))
    from v7.load_corpus import load_corpus

    return list(load_corpus())


# ---------------------------------------------------------------------------------------------
# F-C5-1  blank gas field / GASLab unticked -> KeyError (the live "'co2'")
# ---------------------------------------------------------------------------------------------
def test_f1_live_co2_message_apptest():
    """Deployed sys.path (no labs/comlab): symptom picked, HC + CO typed, CO2 left blank."""
    from c5_apptest import click_run, errors, new_app, pick_symptom, set_num

    at = new_app(with_registry=False)
    pick_symptom(at, "⬇️ Lack of Power / Hesitation", "Flat / sluggish always")
    set_num(at, "gas_hc", 120)
    set_num(at, "gas_co", 0.5)
    at.run()
    click_run(at)
    errs = errors(at)
    assert not errs, f"rendered: {errs} | payload gas={at.session_state['raw_payload'].get('gas')}"


def test_f1_blank_gas_matrix():
    """ui_payload.py:825-826 — untouched widgets are omitted 'so producers can abstain'."""
    out = []
    for blank in (None, "gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox", "ALL", "MODULE_OFF"):
        g = dict(GOOD_GAS)
        extra = {}
        if blank == "ALL":
            g = {}
        elif blank == "MODULE_OFF":
            extra = {"gas_module": False}
        elif blank:
            g[blank] = None
        _, r, e = run(base_widgets(obd_module=False, dtc_module=False, **SYM, **g, **extra))
        out.append(f"{blank}: {e or verdict_str(r)}")
    crashes = [o for o in out if "Error" in o]
    assert not crashes, "\n".join(out)


def test_f1_gaslab_untick_wipes_values():
    from c5_apptest import by_label, new_app, set_num

    at = new_app(with_registry=False)
    for k, v in dict(gas_hc=120, gas_co=0.5, gas_co2=14.5, gas_o2=0.4, gas_nox=30).items():
        set_num(at, k, v)
    at.run()
    by_label(at.checkbox, "GASLab").uncheck()
    at.run()
    by_label(at.checkbox, "GASLab").check()
    at.run()
    vals = [at.number_input(key=k).value for k in ("gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox")]
    assert vals == [120, 0.5, 14.5, 0.4, 30], f"after GASLab untick/re-tick: {vals}"


def test_f1_non_starter_needs_gas():
    """symptom_router: will_not_start -> suppress_gaslab; yet the run needs 5 gas values."""
    ns = dict(triage_tier_1="🚫 Vehicle Won't Start",
              triage_tier_2="Normal crank / zero RPM (prolonged crank)",
              triage_engine_state="Won't start")
    w = decoded_widgets("WME01MC01XH072806", gas_module=False, obd_module=False,
                        dtc_module=False, **ns)
    _, r, e = run(w)
    assert e is None, f"non-starter, GASLab unticked -> {e}"


# ---------------------------------------------------------------------------------------------
# F-C5-2  OBDLab / DTCLab ticked (the default) make 5 OBD + 12 FF fields mandatory
# ---------------------------------------------------------------------------------------------
def test_f2_default_modules_minimum_form():
    steps = [
        ("symptom + 5 gas (defaults: OBD+DTC ticked)", base_widgets(**SYM, **GOOD_GAS)),
        ("+ 5 OBD", base_widgets(**SYM, **GOOD_GAS, **OBD5)),
        ("+ DTC P0171 typed, no FF", base_widgets(**SYM, **GOOD_GAS, **OBD5, dtc_confirmed="P0171")),
        ("no code, no MIL, DTCLab ticked", base_widgets(obd_module=False, **SYM, **GOOD_GAS)),
        ("+ 12 FF", base_widgets(**SYM, **GOOD_GAS, **OBD5, **FF12)),
    ]
    out = []
    for name, w in steps:
        p, r, e = run(w)
        out.append(f"{name}: obd={p.get('obd')} dtc_keys={sorted(p.get('dtc', {}))} -> "
                   f"{(e or verdict_str(r))[:150]}")
    for k in OBD5:
        o = dict(OBD5)
        o[k] = None
        _, r, e = run(base_widgets(dtc_module=False, **SYM, **GOOD_GAS, **o))
        out.append(f"OBD minus {k}: {(e or verdict_str(r))[:110]}")
    crashes = [o for o in out if "Error" in o]
    assert not crashes, "\n".join(out)


# ---------------------------------------------------------------------------------------------
# F-C5-3  WIDEBAND_AFR: the AFR number is sent as pid_wideband_equivalence_ratio
# ---------------------------------------------------------------------------------------------
def test_f3_afr_sent_as_equivalence_ratio():
    out = []
    for afr in (10.0, 14.7, 20.0):
        w = decoded_widgets("WDD1690321J749046", dtc_module=False, obd_upstream_o2_val=afr,
                            obd_shrtft1=1.0, obd_longft1=2.0, obd_engine_rpm=800,
                            obd_coolant_temp_c=90.0, obd_fuel_sys_status="CL", **SYM, **GOOD_GAS)
        p, r, e = run(w)
        out.append((afr, p["obd"].get("pid_wideband_equivalence_ratio"), e or verdict_str(r),
                    None if r is None else r.performance_analytics.lambda_perception_delta))
        if afr == 14.7:
            p2 = copy.deepcopy(p)
            p2["obd"]["pid_wideband_equivalence_ratio"] = 14.7 / 14.7  # the same reading as lambda
            r2 = L.diagnose(p2)
            out.append(("lambda 1.0", 1.0, verdict_str(r2), r2.performance_analytics.lambda_perception_delta))
    msg = "\n".join(map(str, out))
    assert all(0.7 <= o[1] <= 1.3 for o in out), msg


# ---------------------------------------------------------------------------------------------
# F-C5-4  Rough idle / constant shudder is tagged with an oil-consumption key
# ---------------------------------------------------------------------------------------------
def test_f4_symptom_tag_vs_corpus():
    import yaml

    prior_keys = set(yaml.safe_load(open(ROOT / "labs/comlab/comlab/config/symptom_prior.yaml"))["mappings"])
    p = L.build_diagnose_payload(base_widgets(triage_tier_1="🔧 Rough Idle / Shudder",
                                              triage_tier_2="Constant shudder / vibration"))
    ui_tag = p["triage"].get("csv_primary_symptom")
    changed, n = [], 0
    for cid, raw, *_ in _corpus():
        t = raw.get("triage") or {}
        if not t.get("csv_primary_symptom"):
            continue
        ui = copy.deepcopy(raw)
        ui["triage"].pop("csv_primary_symptom", None)
        if (t.get("tier_1"), t.get("tier_2")) == ("rough_idle_shudder", "constant_vibration_shudder"):
            ui["triage"]["csv_primary_symptom"] = ui_tag  # ui_payload.py:864-865
        try:
            a, b = L.diagnose(raw), L.diagnose(ui)
        except Exception:
            continue
        n += 1
        ka = (a.diagnostic_verdict.fault_code, round(a.diagnostic_verdict.confidence_score, 3), a.diagnostic_verdict.abstained)
        kb = (b.diagnostic_verdict.fault_code, round(b.diagnostic_verdict.confidence_score, 3), b.diagnostic_verdict.abstained)
        if ka != kb:
            changed.append(f"{cid} corpus[{t['csv_primary_symptom']}]={ka} ui[{ui_tag}]={kb}")
    assert ui_tag in prior_keys and not changed, (
        f"UI tag={ui_tag!r} in prior table={ui_tag in prior_keys} (keys={sorted(prior_keys)}); "
        f"{len(changed)}/{n} corpus cases change:\n" + "\n".join(changed))


# ---------------------------------------------------------------------------------------------
# F-C5-5  symptom silently dropped when the VIN does not decode
# ---------------------------------------------------------------------------------------------
def test_f5_symptom_dropped_without_vin():
    import wired.composition as wc

    seen = {}
    orig = wc.LabPipelineAggregator.process

    def spy(self, request):
        seen["symptom_dna"] = request.symptom_dna
        return orig(self, request)

    ns = dict(triage_tier_1="🚫 Vehicle Won't Start",
              triage_tier_2="Normal crank / zero RPM (prolonged crank)",
              triage_engine_state="Won't start", triage_occurs_during="Cold only")
    out = []
    wc.LabPipelineAggregator.process = spy
    try:
        for vin in ("", "WME01MC01XH072806"):
            w = decoded_widgets(vin, **ns) if vin else base_widgets(**ns)
            w.update(obd_module=False, dtc_module=False, **GOOD_GAS)
            p, r, e = run(w)
            d = r.execution_meta.lab_routing_directive
            out.append(f"vin={vin!r}: triage sent={p['triage']} | symptom_dna reaching COMLab="
                       f"{sorted(seen['symptom_dna'])} | suppress_gaslab={d.suppress_gaslab} "
                       f"cold_start={d.cold_start_mode} | {verdict_str(r)}")
    finally:
        wc.LabPipelineAggregator.process = orig
    assert "suppress_gaslab=True" in out[0], "\n".join(out)


def test_f5_symptom_dna_routing_weight():
    """Corpus: same VIN, symptom_dna reduced to what a no-VIN run keeps (only _csv_primary_symptom,
    composition.py:111-113). Counts routing / degradation_mode / verdict changes."""
    import wired.composition as wc

    orig = wc.LabPipelineAggregator.process

    def keep_csv_only(self, request):
        sd = {k: v for k, v in request.symptom_dna.items() if k == "_csv_primary_symptom"}
        return orig(self, request.model_copy(update={"symptom_dna": sd}))

    ch = {"routing": [], "degradation_mode": [], "verdict": []}
    n = 0
    for cid, raw, *_ in _corpus():
        try:
            a = L.diagnose(raw)
            wc.LabPipelineAggregator.process = keep_csv_only
            b = L.diagnose(raw)
        except Exception:
            continue
        finally:
            wc.LabPipelineAggregator.process = orig
        n += 1
        ma, mb = a.execution_meta, b.execution_meta
        if ma.lab_routing_directive != mb.lab_routing_directive:
            ch["routing"].append(cid)
        if ma.degradation_mode != mb.degradation_mode:
            ch["degradation_mode"].append(f"{cid}:{ma.degradation_mode}->{mb.degradation_mode}")
        va, vb = a.diagnostic_verdict, b.diagnostic_verdict
        if (va.fault_code, va.abstained) != (vb.fault_code, vb.abstained):
            ch["verdict"].append(cid)
    summary = {k: len(v) for k, v in ch.items()}
    assert not ch["routing"], f"of {n}: {summary}; degradation e.g. {ch['degradation_mode'][:3]}"


# ---------------------------------------------------------------------------------------------
# F-C5-6  'Confidence Rating' band is the era-derived processing rating, not the score band
# ---------------------------------------------------------------------------------------------
def test_f6_confidence_band_vs_score():
    def prd_band(s):  # COMLab_PRD.md §5.1
        return "HIGH" if s >= 0.85 else ("MEDIUM" if s >= 0.60 else "LOW")

    bad = {}
    n = 0
    for cid, raw, *_ in _corpus():
        try:
            r = L.diagnose(raw)
        except Exception:
            continue
        n += 1
        v = r.diagnostic_verdict
        shown = str(r.execution_meta.processing_confidence_rating).replace("_", " ").title()  # app.py:949
        key = (shown, prd_band(v.confidence_score), v.abstained)
        if (shown.startswith("Low") and prd_band(v.confidence_score) == "HIGH") or (shown.startswith("High") and v.abstained):
            bad.setdefault(key, []).append(f"{cid}:{v.fault_code}:{v.confidence_score:.2f}")
    msg = "; ".join(f"{k} x{len(v)} e.g. {v[0]}" for k, v in bad.items())
    assert not bad, f"of {n}: {msg}"


def test_f6_render_low_certainty_score_one():
    from c5_apptest import new_app

    raw = next(r for c, r, *_ in _corpus() if c == "era1_001")
    res = L.diagnose(raw)
    at = new_app()
    at.session_state["diagnose_result"] = res
    at.run()
    line = [str(m.value) for m in at.markdown if "Confidence Rating" in str(m.value)]
    assert not ("Low Certainty" in line[0] and "1.00" in line[0]), line


# ---------------------------------------------------------------------------------------------
# F-C5-7  results pane omits horizon, routing directive, echo audit, severity ribbon
# ---------------------------------------------------------------------------------------------
def test_f7_results_pane_fields():
    src = (ROOT / "apps/ui/app.py").read_text(encoding="utf-8")
    needed = ["resolved_horizon", "lab_routing_directive", "user_input_echo_audit",
              "impacted_subsystems", "is_fault_detected"]
    missing = [f for f in needed if f not in src]
    from c5_apptest import new_app

    w = decoded_widgets("WME01MC01XH072806", triage_tier_1="🚫 Vehicle Won't Start",
                        triage_tier_2="Normal crank / zero RPM (prolonged crank)",
                        triage_engine_state="Won't start", obd_module=False, dtc_module=False,
                        **GOOD_GAS)
    _, res, _ = run(w)
    at = new_app()
    at.session_state["diagnose_result"] = res
    at.run()
    text = "\n".join(str(x.value) for x in list(at.markdown) + list(at.caption) + list(at.info))
    d = res.execution_meta.lab_routing_directive
    shown = {
        "horizon": res.execution_meta.resolved_horizon in text or "HORIZON" in text,
        "gas skipped disclosure": "skipped" in text.lower(),
    }
    assert not missing and all(shown.values()), (
        f"fields never referenced in app.py: {missing}; result had suppress_gaslab={d.suppress_gaslab} "
        f"horizon={res.execution_meta.resolved_horizon} verdict={verdict_str(res)}; rendered: {shown}")


# ---------------------------------------------------------------------------------------------
# F-C5-8  sibling cards are not 'first 2 distinct families'
# ---------------------------------------------------------------------------------------------
def test_f8_sibling_families():
    rep_winner, rep_pair, n, ex = 0, 0, 0, []
    for cid, raw, *_ in _corpus():
        try:
            r = L.diagnose(raw)
        except Exception:
            continue
        n += 1
        v = r.diagnostic_verdict
        sibs = v.differential_siblings[:2]  # app.py:978 / :1017
        fams = [s.fault_family for s in sibs]
        if v.fault_family in fams:
            rep_winner += 1
            if len(ex) < 3:
                ex.append(f"{cid}: {v.fault_code}/{v.fault_family} + {[(s.fault_id, s.fault_family) for s in sibs]}")
        if len(set(fams)) < len(fams):
            rep_pair += 1
    assert rep_winner == 0 and rep_pair == 0, (
        f"of {n}: winner family repeated in rendered siblings {rep_winner}, sibling pair same family {rep_pair}; e.g. {ex}")


# ---------------------------------------------------------------------------------------------
# F-C5-9  UI DNA gating vs the DNA the labs get
# ---------------------------------------------------------------------------------------------
def test_f9_partial_decode_gates_and_untick_crashes():
    from c5_apptest import new_app

    at = new_app(with_registry=False)
    at.text_input(key="vin_input").input("WDD1690321J749046")
    at.run()
    import vinlab

    conf = vinlab.decode("WDD1690321J749046").confidence.value
    up = [(n.label, n.min, n.max) for n in at.number_input if n.key == "obd_o2_up"]
    w = base_widgets(vin="WDD1690321J749046", use_decoded_dna=False, dtc_module=False,
                     obd_fuel_sys_status="CL", **SYM, **GOOD_GAS, **OBD5)
    p, r, e = run(w)
    assert conf == "HIGH" or up[0][0] == "Upstream O₂ (V)", (
        f"decode confidence={conf}; upstream widget rendered={up}; 'Use this decoded DNA' unticked "
        f"-> vin sent={p['vin']} obd O2 key={[k for k in p['obd'] if 'pid_' in k]} -> {e or verdict_str(r)}")


# ---------------------------------------------------------------------------------------------
# F-C5-10  inputs collected and never sent
# ---------------------------------------------------------------------------------------------
def test_f10_inputs_never_sent():
    from c5_apptest import by_label, click_run, new_app, pick_symptom, set_num

    def base():
        at = new_app(with_registry=False)
        pick_symptom(at, "⬇️ Lack of Power / Hesitation", "Flat / sluggish always")
        return at

    at = base()
    click_run(at)
    p0 = copy.deepcopy(at.session_state["raw_payload"])
    at = base()
    at.checkbox(key="fuel_blend__E0").check()
    at.run()
    at.checkbox(key="mileage__High").check()
    at.run()
    by_label(at.text_area, "Free-text notes").input("misfire only above 3000 rpm")
    at.run()
    for k, v in dict(obd_rpm_high=2500, obd_ect_high=92.0, obd_stft1_high=15.0,
                     obd_ltft1_high=12.0, obd_load_high=40.0, obd_o2_up_high=0.2).items():
        set_num(at, k, v)
    at.selectbox(key="obd_fss_high").set_value("OL")
    at.run()
    by_label(at.button, "➕ Add monitor").click()
    at.run()
    at.text_input(key="mon_id_0").input("MID_21_TID_01")
    at.run()
    set_num(at, "mon_margin_0", -12.0)
    at.selectbox(key="mon_state_0").set_value("Critical fail")
    at.run()
    click_run(at)
    p1 = at.session_state["raw_payload"]
    p1_wo_m06 = copy.deepcopy(p1)
    p1_wo_m06.get("dtc", {}).pop("raw_mode06", None)
    assert p0 != p1_wo_m06, (
        f"payload unchanged by E0 + Mileage High + notes + 7 OBD high-idle fields: {p1_wo_m06}; "
        f"Mode $06 row 'Critical fail' sent as {p1['dtc'].get('raw_mode06')}")


def test_f10_no_lab_consumer():
    hits = []
    for pat in ("fuel_blend", "ethanol_blend", "mileage"):
        for f in list(ROOT.glob("labs/*/*/**/*.py")) + list(ROOT.glob("apps/wired/wired/*.py")):
            if "/tests/" in str(f):
                continue
            if re.search(pat, f.read_text(encoding="utf-8", errors="ignore"), re.I):
                hits.append(f"{pat}:{f.relative_to(ROOT)}")
    assert hits, "no reader of fuel_blend / mileage in any lab package or wired"


# ---------------------------------------------------------------------------------------------
# F-C5-11  misfire slider default writes 40 misfires on cylinder 1
# ---------------------------------------------------------------------------------------------
def test_f11_misfire_default_fill():
    from c5_apptest import click_run, new_app, pick_symptom

    at = new_app(with_registry=False)
    pick_symptom(at, "🔧 Rough Idle / Shudder", "Surging / hunting idle")
    slider = [(s.label, s.value) for s in at.slider]
    click_run(at)
    obd = at.session_state["raw_payload"].get("obd", {})
    assert "per_cylinder_misfire_counts" not in obd, (
        f"slider untouched {slider}; payload obd={obd}")


# ---------------------------------------------------------------------------------------------
# F-C5-12  app.py imports a lab directly
# ---------------------------------------------------------------------------------------------
def test_f12_ui_lab_import():
    src = (ROOT / "apps/ui/app.py").read_text(encoding="utf-8")
    labs = re.findall(r"^\s*(?:import|from)\s+(vinlab|gaslab|obdlab|dtclab|comlab|dnalab|symptomlab)\b.*$",
                      src, re.M)
    assert not labs, f"lab imports in apps/ui/app.py: {labs}"


# ---------------------------------------------------------------------------------------------
# F-C5-13  one malformed DTC / Monitor-ID token aborts the whole diagnosis
# ---------------------------------------------------------------------------------------------
def test_f13_free_text_tokens():
    out = []
    for s in ("P0171, P0420", "P0171;P0420", "P0171/P0420", "P0300 (pending)"):
        _, r, e = run(base_widgets(obd_module=False, dtc_confirmed=s, **FF12, **SYM, **GOOD_GAS))
        out.append(f"{s!r}: {(e or verdict_str(r))[:100]}")
    _, r, e = run(base_widgets(obd_module=False, mode06_monitors=[{"monitor_id": "21-01", "margin_pct": 5.0}],
                               **FF12, **SYM, **GOOD_GAS))
    out.append(f"monitor '21-01': {(e or verdict_str(r))[:100]}")
    assert not [o for o in out if "Error" in o], "\n".join(out)
