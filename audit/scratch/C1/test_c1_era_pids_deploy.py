"""C1 probes: era gating on REG-V2, PID identity, deploy-time import of the shim,
discriminator stacking, abstain boundary, determinism."""
from __future__ import annotations

import json
import logging
import subprocess
import sys
from pathlib import Path

import pytest
from hypothesis import given, settings, strategies as st

from c1_builders import aggregator, ff, request, run

logging.disable(logging.CRITICAL)
REPO = Path(__file__).resolve().parents[3]


# --- F5: production layout cannot import registry.integration_shim ------------------

def test_default_path_imports_in_deployed_layout():
    """render.yaml: `pip install -r requirements.txt` (-e labs/comlab, -e apps/wired) then
    `streamlit run app.py` from the repo root; app.py puts apps/ui on sys.path.
    Replicate that sys.path (no pytest rootdir insertion) and call wired.diagnose()."""
    code = r"""
import sys
sys.path[:] = [p for p in sys.path if 'labs/comlab' not in p]
sys.path.insert(0, 'apps/ui'); sys.path.insert(0, '.')
import logging; logging.disable(logging.CRITICAL)
from wired.composition import diagnose
raw = {"vin": "WBA4W9C5ZLYYYYYYY",
       "triage": {"tier_1": "rough_idle_shudder", "tier_2": "constant_vibration_shudder",
                  "occurs_during": "always", "engine_state": "running", "load_state": "idle"},
       "gas": {"co": 0.1, "co2": 14.5, "o2": 0.3, "hc": 50, "nox": 10,
               "engine_state": "STABILIZED_IDLE"}}
try:
    r = diagnose(raw); print("OK", r.diagnostic_verdict.fault_code)
except Exception as e:
    print("EXC", type(e).__name__, e)
"""
    proc = subprocess.run([sys.executable, "-c", code], cwd=REPO, capture_output=True,
                          text=True, env={"PATH": "/usr/bin:/bin"})
    print(proc.stdout.strip()[-300:], proc.stderr.strip()[-300:])
    assert proc.stdout.startswith("OK")


# --- F19: REG-V2 has no horizon gate (GDI rule offered for a LEGACY car) ------------

def test_legacy_rich_case_offers_no_gdi_only_fault():
    """wiki 04: 'resolved_horizon gates which registry rules apply'; GDI faults are
    'MODERN only'. RM-004 itself carries precondition 'gdi_equipped: true'."""
    out = run(request(chem="RICH_MIXTURE", horizon="HORIZON_LEGACY", include_obd=False))
    v = out.diagnostic_verdict
    ids = [v.fault_code] + [(s.fault_id, s.confidence_score) for s in v.differential_siblings]
    print("LEGACY rich ->", ids)
    assert "RM-004" not in [v.fault_code] + [s.fault_id for s in v.differential_siblings]


def test_gdi_chemistry_on_legacy_car_does_not_yield_gdi_verdict():
    out = run(request(chem="GDI_HPFP_INTERNAL_SEAL_LEAK", horizon="HORIZON_LEGACY",
                      include_obd=False, include_dtc=False))
    v = out.diagnostic_verdict
    print("LEGACY GDI_HPFP chem ->", v.fault_code, v.fault_name[:60], v.confidence_score)
    assert v.fault_code != "RM-004"


def test_horizon_changes_v2_candidate_set():
    from comlab.schemas.vocabulary import ChemicalSignature
    agg = aggregator()
    same = 0
    for chem in ChemicalSignature:
        a = agg.process(request(chem=chem.value, horizon="HORIZON_LEGACY")).diagnostic_verdict
        b = agg.process(request(chem=chem.value, horizon="HORIZON_MODERN")).diagnostic_verdict
        sa = [a.fault_code] + [s.fault_id for s in a.differential_siblings]
        sb = [b.fault_code] + [s.fault_id for s in b.differential_siblings]
        same += sa == sb
    print(f"identical verdict+siblings LEGACY vs MODERN: {same}/{len(ChemicalSignature)}")
    assert same < len(ChemicalSignature)


# --- F15: o2_downstream PID resolves to the UPSTREAM sensor --------------------------

def test_o2_downstream_pid_is_not_upstream_voltage():
    from registry.integration_shim import _PID_DISPATCH, _resolve_pid_from_payload
    payload = {"dtc_lab_output": {"freeze_frame": ff(o2_voltage_b1s1=0.82)}}
    up = _resolve_pid_from_payload(payload, "o2_voltage")
    down = _resolve_pid_from_payload(payload, "o2_downstream")
    print("dispatch:", _PID_DISPATCH["o2_downstream"], "upstream b1s1=0.82 -> o2_downstream =", down)
    assert down is None  # no downstream reading supplied


def test_sf006_downstream_rule_scored_from_upstream_voltage():
    """SF-006 evidence row: o2_downstream ge 0.6 V (SUGGESTIVE). Only the UPSTREAM b1s1
    voltage is supplied; it must not move a downstream-sensor rule."""
    from registry.integration_shim import RegistryV2Router, _build_observation, _score_rule
    rules = {r.rule_id: r for r in RegistryV2Router().rules}
    base = {"gas_lab_output": {"chemical_state": "TIMING_RETARDED", "sample_validity": "VALID"},
            "obd_live_data": None}
    lo = _score_rule(rules["SF-006"], _build_observation(
        {**base, "dtc_lab_output": {"confirmed_dtcs": [], "freeze_frame": ff(o2_voltage_b1s1=0.10)}}))
    hi = _score_rule(rules["SF-006"], _build_observation(
        {**base, "dtc_lab_output": {"confirmed_dtcs": [], "freeze_frame": ff(o2_voltage_b1s1=0.80)}}))
    print("SF-006 score with upstream b1s1 0.10 V:", lo, " with upstream b1s1 0.80 V:", hi)
    assert lo == hi


# --- F16: fuel_pressure PID maps to a field FreezeFrameRecord does not have ---------

def test_fuel_pressure_pid_resolvable():
    from comlab.schemas.ingestion import FreezeFrameRecord
    from registry.integration_shim import _PID_DISPATCH
    src = _PID_DISPATCH["fuel_pressure"]
    print("fuel_pressure ->", src, "; FreezeFrameRecord has field:",
          src[0][1] in FreezeFrameRecord.model_fields)
    assert src[0][1] in FreezeFrameRecord.model_fields


# --- F17: discriminator lift stacks per tag (duplicate / same-family tags) -----------

def test_discriminator_lift_is_bounded_per_family():
    one = run(request(chem="NORMAL_OPERATION", dtc_kw=dict(tags=["LEAN_HISTORY"])))
    three = run(request(chem="NORMAL_OPERATION",
                        dtc_kw=dict(tags=["LEAN_HISTORY", "EVAP_HISTORY", "BOOST_HISTORY"])))
    dup = run(request(chem="NORMAL_OPERATION", dtc_kw=dict(tags=["LEAN_HISTORY", "LEAN_HISTORY"])))
    for name, o in (("1 tag", one), ("3 lean-mapped tags", three), ("dup tag", dup)):
        v = o.diagnostic_verdict
        print(name, "->", v.fault_code, v.fault_family, round(v.confidence_score, 3))
    # T-FX-REG-3: 'bounded additive lift ... identical bounded-prior semantics' (weight 0.10)
    assert dup.diagnostic_verdict.confidence_score == one.diagnostic_verdict.confidence_score


# --- F18: abstain margin boundary vs float noise ------------------------------------

def test_abstain_margin_inclusive_at_0_02(monkeypatch):
    """ABSTAIN_MARGIN 0.02: 'top1 - top2 within this -> abstain' (route() uses <=).
    Feed the exact float the shim accumulates for SF-004 (base 0.72 + two SUGGESTIVE +0.05)
    against a 0.80 runner-up of another family: nominal gap 0.02."""
    import registry.integration_shim as shim
    real = shim.route_case_with_diagnostics
    top = 0.72
    top += 0.05            # shim arithmetic: score += _TIER_BONUS_SUGGESTIVE (lambda_perception_delta)
    top += 0.05            # shim arithmetic: score += _TIER_BONUS_SUGGESTIVE (maf ge 3.5)
    other = 0.80

    def fake(payload):
        out, diag = real(payload)
        out = shim.render_ranked_rule(payload, "SF-004", top)
        diag["scored_rules"] = [
            {"rule_id": "SF-004", "fault_family": "sensor_fault", "score": top},
            {"rule_id": "MW-004", "fault_family": "mechanical_wear", "score": other},
        ]
        diag["winner_rule_id"] = "SF-004"
        return out, diag

    monkeypatch.setattr(shim, "route_case_with_diagnostics", fake)
    v = run(request(chem="NORMAL_OPERATION")).diagnostic_verdict
    print("top", repr(top), "runner", other, "diff", repr(top - other), "abstained:", v.abstained,
          v.abstain_reason)
    assert v.abstained and v.abstain_reason == "margin"


# --- determinism (expected to hold) --------------------------------------------------

CHEMS = ["NORMAL_OPERATION", "RICH_MIXTURE", "LEAN_MIXTURE", "IGNITION_MISFIRE",
         "EXHAUST_AIR_LEAK", "POA_SIGNATURE", "EGR_STUCK_OPEN"]


@settings(max_examples=60, deadline=None)
@given(chem=st.sampled_from(CHEMS),
       trim=st.floats(-60, 60, allow_nan=False),
       lam=st.floats(0.7, 1.3, allow_nan=False),
       hc=st.integers(0, 3000),
       tags=st.lists(st.sampled_from(["LEAN_HISTORY", "RICH_HISTORY", "MISFIRE_HISTORY",
                                      "POA_HISTORY", "O2_HISTORY"]), max_size=3),
       dtcs=st.lists(st.sampled_from(["P0171", "P0172", "P0301", "P0420"]), max_size=3),
       horizon=st.sampled_from(["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"]))
def test_same_input_same_verdict(chem, trim, lam, hc, tags, dtcs, horizon):
    def once(tag_order, dtc_order):
        req = request(chem=chem, horizon=horizon, gas_kw={"gas_hc": hc},
                      obd_kw={"total_trim_correction_delta": trim, "normalized_obd_lambda": lam,
                              "shrtft1": max(-127, min(127, trim / 2)),
                              "longft1": max(-127, min(127, trim / 2))},
                      dtc_kw=dict(confirmed=dtc_order, tags=tag_order))
        o = aggregator().process(req)
        d = o.model_dump(mode="json")
        d.pop("user_input_echo_audit")  # sentinel carries now()
        return json.dumps(d, sort_keys=True)
    a = once(tags, dtcs)
    b = once(tags, dtcs)
    c = once(list(reversed(tags)), list(reversed(dtcs)))
    assert a == b
    assert a == c
