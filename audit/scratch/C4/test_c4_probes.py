"""C4 auditor probes — cross-lab contracts and the wired composition.

Each test asserts a claim the repo makes; a FAILING test is the evidence of a defect.
Run from the repo root:
    python -m pytest -q audit/scratch/C4/test_c4_probes.py -p no:cacheprovider
"""

from __future__ import annotations

import copy
import csv
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
# Same sys.path the apps/wired pytest config uses (apps/wired/pyproject.toml pythonpath),
# so the semantic probes run; F1 below checks the *installed* environment without it.
for p in ("labs/comlab", "apps/wired"):
    if str(ROOT / p) not in sys.path:
        sys.path.insert(0, str(ROOT / p))

import wired.composition as wc  # noqa: E402
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator  # noqa: E402
from comlab.schemas.vocabulary import TrimAnalyticsGate  # noqa: E402

CSV = ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
MW002 = ROOT / "apps/wired/tests/fixtures/oil_cases/MW-002.json"


def _rows() -> dict[str, dict[str, str]]:
    with open(CSV, newline="", encoding="utf-8") as f:
        return {r["case_id"]: r for r in csv.DictReader(f)}


def _raw(case_id: str) -> dict:
    from v7.load_corpus import row_to_raw_inputs

    return row_to_raw_inputs(_rows()[case_id])


@pytest.fixture
def captured(monkeypatch):
    """Capture the OrchestratorInboundRequest the composition hands to COMLab."""
    cap: dict = {}
    orig = LabPipelineAggregator.process

    def spy(self, req, *a, **k):
        cap["req"] = req
        return orig(self, req, *a, **k)

    monkeypatch.setattr(LabPipelineAggregator, "process", spy)
    return cap


# --- F1 ---------------------------------------------------------------------------
def test_f1_diagnose_runs_in_requirements_install():
    """requirements.txt installs the labs editable; diagnose() must work there (render.yaml)."""
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONPATH", "USE_V2_REGISTRY")}
    code = (
        "import json,sys; sys.path[:0]=['.','apps/ui']\n"
        "from wired import diagnose\n"
        f"r=diagnose(json.load(open({str(MW002)!r})))\n"
        "print('VERDICT', r.diagnostic_verdict.fault_code)\n"
    )
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True)
    assert out.returncode == 0, out.stderr.strip().splitlines()[-1]


# --- F2 ---------------------------------------------------------------------------
def test_f2_blocked_trim_gate_suppresses_trim_findings(captured):
    """COMLab_BDD: 'Given an OBD payload whose trim_analytics_gate is not VALID ... Then
    trim-derived findings do not contribute to the verdict'."""
    agg = LabPipelineAggregator()
    ri = _raw("era1_005")
    ri["obd"]["coolant_temp_c"] = 40.0  # cold engine -> OBDLab: ENGINE_COLD, engine_warmed=False
    out = wc.diagnose(ri)
    req = captured["req"]
    assert req.obd_live_data.trim_analytics_gate == TrimAnalyticsGate.ENGINE_COLD
    zeroed = req.obd_live_data.model_copy(
        update={"total_trim_correction_delta": 0.0, "shrtft1": 0.0, "longft1": 0.0}
    )
    out0 = agg.process(req.model_copy(update={"obd_live_data": zeroed}))
    print("gate=", req.obd_live_data.trim_analytics_gate.value, "warmed=", req.obd_live_data.engine_warmed, "total_trim=", req.obd_live_data.total_trim_correction_delta, "stft/ltft=", req.obd_live_data.shrtft1, req.obd_live_data.longft1, "conf=", out.diagnostic_verdict.confidence_score, out.execution_meta.degradation_mode,
          "verdict=", out.diagnostic_verdict.fault_code, "| trims zeroed ->", out0.diagnostic_verdict.fault_code)
    assert out.diagnostic_verdict.fault_code == out0.diagnostic_verdict.fault_code


# --- F3 ---------------------------------------------------------------------------
def test_f3_upstream_o2_override_reaches_gaslab(captured, monkeypatch):
    """composition.py:122-124 applies overrides['upstream_o2_type'] with
    '# consumer: OBDLab O2SensorType -> COMLab perception_contradiction upstream-type branch'."""
    ri = _raw("era2_003")
    ri.pop("obd")
    wc.diagnose(dict(ri, overrides={"upstream_o2_type": "NARROWBAND"}))
    with_override = captured["req"].gas_lab_output.chemical_state

    orig = wc._run_gaslab

    def told_nb(gi, vd):
        vd = dict(vd)
        vd["emissions"] = dict(vd["emissions"], upstream_o2_type="NARROWBAND")
        return orig(gi, vd)

    monkeypatch.setattr(wc, "_run_gaslab", told_nb)
    wc.diagnose(ri)
    gaslab_told_nb = captured["req"].gas_lab_output.chemical_state
    print("override NARROWBAND ->", with_override, "| GASLab actually given NARROWBAND ->", gaslab_told_nb)
    assert with_override == gaslab_told_nb


def test_f3b_upstream_o2_override_reaches_obdlab():
    """Same override, OBD present: a narrowband reading under a narrowband override must translate."""
    ri = _raw("era2_003")
    ri["overrides"] = {"upstream_o2_type": "NARROWBAND"}
    ri["obd"].pop("pid_wideband_equivalence_ratio", None)
    ri["obd"]["pid_oxygen_sensor_volts"] = 0.45
    wc.diagnose(ri)


# --- F4 ---------------------------------------------------------------------------
def test_f4_o2_downstream_pid_reads_downstream_sensor(monkeypatch):
    """registry rules SF-006 / EL-002 test pid 'o2_downstream' (downstream O2, V)."""
    import registry.integration_shim as shim

    cap: dict = {}
    orig = shim.route_case_with_diagnostics

    def spy(payload):
        cap["payload"] = payload
        out, diag = orig(payload)
        cap["diag"] = diag
        return out, diag

    monkeypatch.setattr(shim, "route_case_with_diagnostics", spy)
    ri = json.loads(MW002.read_text())
    ri["obd"] = {"engine_rpm": 800, "coolant_temp_c": 90.0, "shrtft1": 2.0, "longft1": 3.0,
                 "fuel_sys_status": "CL", "pid_wideband_equivalence_ratio": 1.0, "downstream_o2_v": 0.10}
    ff = {"coolant_temp_c": 90.0, "engine_rpm": 800, "calculated_load_pct": 20.0, "manifold_pressure_kpa": 30.0,
          "short_term_ft1": 1.0, "long_term_ft1": 2.0, "vehicle_speed_kmh": 0, "ignition_advance_deg": 12.0,
          "intake_air_temp_c": 25.0, "maf_gps": 3.0, "throttle_pos_pct": 3.0, "fuel_system_status": "CL",
          "o2_voltage_b1s1": 0.85}
    for b1s1 in (0.10, 0.85):  # upstream B1S1 varies; measured downstream held at 0.10 V
        r = copy.deepcopy(ri)
        r["dtc"] = {"raw_dtcs": {"$03": ["P0420"]}, "raw_freeze_frame": dict(ff, o2_voltage_b1s1=b1s1),
                    "active_mil": True}
        out = wc.diagnose(r)
        sc = {d["rule_id"]: round(d["score"], 2) for d in cap["diag"]["scored_rules"] if d["rule_id"] in ("SF-006", "EL-002")}
        print(f"b1s1={b1s1}: SF-006/EL-002 scores={sc} verdict={out.diagnostic_verdict.fault_code}")
    resolved = shim._resolve_pid_from_payload(cap["payload"], "o2_downstream")
    print("measured downstream_o2_v=0.10, upstream FF o2_voltage_b1s1=0.85 -> o2_downstream resolved =", resolved)
    assert resolved != 0.85


# --- F5 ---------------------------------------------------------------------------
def test_f5_high_idle_measured_lambda_is_consumed(captured):
    """UI FIELD_HELP['gas_lambda_2500']: 'High-idle measured lambda ... used to verify fuel control under load'."""
    ri = json.loads(MW002.read_text())
    seen = []
    for lam in (None, 0.80, 1.30):
        r = copy.deepcopy(ri)
        if lam is not None:
            r["gas"]["lambda_2500"] = lam
        wc.diagnose(r)
        seen.append(captured["req"].model_dump(mode="json", exclude={"metadata": {"session_id"}}))
    print("requests identical for lambda_2500 in {absent, 0.80, 1.30}:", seen[0] == seen[1] == seen[2])
    assert not (seen[0] == seen[1] == seen[2])


# --- F6 ---------------------------------------------------------------------------
@pytest.mark.parametrize("field,value", [("induction_type", "SUPERCHARGED"), ("emissions.upstream_o2_type", "NONE")])
def test_f6_every_vinlab_value_projects_into_obdlab(field, value):
    """VINLab vocabulary (vinlab/models.py InductionType, UpstreamO2Type) -> wired -> ObdLabDnaView."""
    vd = wc._build_fallback_vin_dna("")
    if field.startswith("emissions."):
        vd["emissions"][field.split(".", 1)[1]] = value
    else:
        vd[field] = value
    wc._build_obd_dna_view(vd)


# --- F7 ---------------------------------------------------------------------------
@pytest.mark.parametrize("field,value", [("downstream_o2_v", 5.0), ("downstream_o2_v", "nan"), ("co2_idle_pct", -40.0)])
def test_f7_composition_owned_obd_channels_are_range_checked(field, value):
    """OBD channels COMLab receives should be physically bounded like OBDLab's own (shrtft1 -> PIDValidationError)."""
    vd = wc._build_fallback_vin_dna("")
    obd = {"engine_rpm": 800, "coolant_temp_c": 90.0, "shrtft1": 2.0, "longft1": 3.0,
           "fuel_sys_status": "CL", "pid_oxygen_sensor_volts": 0.45, field: value}
    with pytest.raises(Exception):
        out = wc._run_obdlab(obd, vd)
        v = getattr(out, field)
        print(field, "accepted ->", v, "(nan)" if isinstance(v, float) and math.isnan(v) else "")


# --- F8 ---------------------------------------------------------------------------
def test_f8_ui_payload_without_dna_module_is_accepted():
    """apps/ui/ui_payload.build_diagnose_payload omits 'triage' when the DNA module is off;
    composition.py:_build_fallback_vin_dna is documented for 'undecodable or absent VIN input'."""
    sys.path.insert(0, str(ROOT / "apps/ui"))
    from ui_payload import build_diagnose_payload

    raw = build_diagnose_payload({"dna_module": False, "gas_module": True, "gas_hc": 120, "gas_co": 0.5,
                                  "gas_co2": 14.5, "gas_o2": 0.6, "gas_nox": 300})
    print("raw_inputs keys:", sorted(raw))
    wc.diagnose(raw)
