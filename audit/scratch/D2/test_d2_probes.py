"""D2 probes — each test asserts what a DESIGN-CHAIN document states.

A FAILING test reproduces a finding (code/data != document).
Run from the repo root:
    python -m pytest -q audit/scratch/D2/test_d2_probes.py -p no:cacheprovider -rA
Evidence only; changes nothing.
"""
from __future__ import annotations

import collections
import glob
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator
from comlab.core.symptom_router import route_symptom
from comlab.projection import project
from comlab.schemas.ingestion import OrchestratorInboundRequest
from comlab.schemas.response import OrchestratorFinalUIOutput
from comlab.schemas.vocabulary import FaultFamily

ROOT = Path(__file__).resolve().parents[3]
COM = ROOT / "labs/comlab"
SID = "6f1c8a3e-2b4d-4c1e-9f0a-1b2c3d4e5f60"


def _ff(**kw):
    d = {"calculated_load_pct": 25.0, "engine_rpm": 800, "coolant_temp_c": 90.0,
         "short_term_ft1": 0.0, "long_term_ft1": 0.0, "manifold_pressure_kpa": 35.0,
         "vehicle_speed_kmh": 0, "ignition_advance_deg": 10.0, "intake_air_temp_c": 30.0,
         "maf_gps": 3.0, "throttle_pos_pct": 12.0, "fuel_system_status": "CL"}
    d.update(kw)
    return d


def _req(chem="NORMAL_OPERATION", gas_kw=None, obd_kw=None, dtc_kw=None,
         horizon="HORIZON_ADAPTIVE", symptom=None, **top):
    gas = {"chemical_state": chem, "gas_co": 0.3, "gas_hc": 80, "gas_co2": 14.8,
           "gas_o2": 0.4, "gas_nox": 50, "lambda_chem": 1.0, "sample_validity": "VALID"}
    gas.update(gas_kw or {})
    obd = {"engine_warmed": True, "total_trim_correction_delta": 0.0,
           "normalized_obd_lambda": 1.0, "ve_pct": 72.0, "ve_validity": "VALID",
           "rpm_state_bucket": "STABILIZED_IDLE", "trim_analytics_gate": "VALID",
           "o2_failure_mode": "NO_FAULT", "maf_status": "REAL_SENSOR_FEED",
           "map_status": "REAL_SENSOR_FEED"}
    obd.update(obd_kw or {})
    dtc = {"active_mil": False, "mil_flashing": False, "confirmed_dtcs": [],
           "routing_tags": [], "historical_fault_context": "UNKNOWN", "freeze_frame": _ff()}
    dtc.update(dtc_kw or {})
    body = {"metadata": {"session_id": SID, "vin_dna_string": "WVWZZZ1JZXW000001",
                         "resolved_horizon": horizon, "cylinder_count": 4},
            "gas_lab_output": gas, "obd_live_data": obd, "dtc_lab_output": dtc,
            "symptom_dna": symptom or {}}
    body.update(top)
    return OrchestratorInboundRequest.model_validate(body)


# --- D2-1: BDD "A biased-lean sensor ... O2_SENSOR_BIASED_LOW"; gaslab wiki 05/06b:
#     BIASED_LOW = "λ(chem) rich/normal, ECU perceives lean". Production default path.
def test_d2_bias_direction_obd_lean_is_biased_low():
    out = LabPipelineAggregator().process(_req(obd_kw={"normalized_obd_lambda": 1.12}))
    print("default path verdict:", out.diagnostic_verdict.fault_code,
          "bias:", out.performance_analytics.o2_sensor_bias_verdict,
          "delta:", out.performance_analytics.lambda_perception_delta)
    assert out.performance_analytics.o2_sensor_bias_verdict == "O2_SENSOR_BIASED_LOW"


# --- D2-2: HLD §7.1 / LLD §3.2 / SEMANTIC_CONTRACT §4.5 — inbound top-level `vehicle_dna`.
def test_d2_inbound_contract_shape_per_hld():
    vin_dna = {
        "vin": "WVWZZZ1JZXW000001", "make": "VW", "model": "Golf", "model_year": 1999,
        "engine_displacement_liters": 1.6, "cylinder_count": 4, "number_of_banks": 1,
        "induction_type": "NATURALLY_ASPIRATED", "fuel_delivery_type": "PORT_INJECTION",
        "air_metering_architecture": {"has_maf_sensor": True, "has_map_sensor": False,
                                      "primary_load_calculation": "MAF_ONLY"},
        "air_metering_strategy": "MAF_ONLY",
        "emissions": {"upstream_o2_type": "NARROWBAND", "downstream_o2_present": True,
                      "egr_equipped": True},
        "euro_emission_category": "EURO_3", "stress_idle_rpm_target": 3000,
        "confidence": "HIGH", "resolved_horizon": "HORIZON_ADAPTIVE"}
    base = _req().model_dump(mode="json")
    hld_shape = {"vehicle_dna": {"session_id": SID, "timestamp": "2026-10-17T10:00:00Z",
                                 "schema_version": "1.0", "vin_dna": vin_dna},
                 "gas_lab_output": base["gas_lab_output"],
                 "obd_live_data": base["obd_live_data"],
                 "dtc_lab_output": base["dtc_lab_output"],
                 "symptom_dna": {}}
    try:
        OrchestratorInboundRequest.model_validate(hld_shape)
        ok, err = True, ""
    except ValidationError as exc:
        ok, err = False, str(exc).splitlines()[0:3]
    print("HLD §7.1 shape accepted:", ok, err)
    assert ok


# --- D2-3: HLD §7.4/§9.7, LLD §3.3, DLD §9.1 — outbound carries schema_version echo.
def test_d2_outbound_has_schema_version():
    print("OrchestratorFinalUIOutput fields:", list(OrchestratorFinalUIOutput.model_fields))
    assert "schema_version" in OrchestratorFinalUIOutput.model_fields


# --- D2-4: HLD §7.5 / LLD §3.3 OrchestratorErrorOutput / PRD §5.8 — abort shape has
#     `error.error_code`, no verdict; PRD §5.1 maps OPTIMAL_HEALTH to "no fault detected".
def test_d2_abort_shape_per_hld():
    agg = LabPipelineAggregator(enable_fatal_gates=True)
    out = agg.process(_req(gas_kw={"sample_validity": "INVALID"}))
    d = out.model_dump()
    print("abort output: fault_code=", d["diagnostic_verdict"]["fault_code"],
          "family=", d["diagnostic_verdict"]["fault_family"],
          "severity=", d["performance_analytics"]["severity_level"],
          "degradation=", d["execution_meta"]["degradation_mode"], "has error key:", "error" in d)
    assert "error" in d and d["performance_analytics"]["severity_level"] != "OPTIMAL_HEALTH"


# --- D2-5: BDD "An air-metering strategy inconsistent with its sensors is rejected ...
#     When the payload is validated Then ERR-CONTRACT-002" (and LLD §10 ERR-CONTRACT-003).
def test_d2_contract_002_reachable_from_request():
    body = _req().model_dump(mode="json")
    body["metadata"].update({"air_metering_strategy": "DUAL_MAF_MAP_CROSSCHECK",
                             "has_map_sensor": False, "has_maf_sensor": True})
    try:
        OrchestratorInboundRequest.model_validate(body)
        raised = ""
    except ValidationError as exc:
        raised = str(exc)
    print("ERR-CONTRACT-002 raised:", "ERR-CONTRACT-002" in raised)
    assert "ERR-CONTRACT-002" in raised


def test_d2_contract_003_reachable_from_request():
    body = _req().model_dump(mode="json")
    body["downstream_trim_role"] = "SECONDARY_FUEL_TRIM"   # no downstream sensor anywhere
    try:
        OrchestratorInboundRequest.model_validate(body)
        raised = ""
    except ValidationError as exc:
        raised = str(exc)
    print("ERR-CONTRACT-003 raised:", "ERR-CONTRACT-003" in raised)
    assert "ERR-CONTRACT-003" in raised


# --- D2-6: HLD §5.5 / ADR-0006 / LLD §8.2 rules 1,2,5 — registry⇆KG 1:1, no duplicates.
def _kg_ids():
    ids = {}
    for f in glob.glob(str(COM / "comlab/config/kg/*.json")):
        if Path(f).name.startswith("_"):
            continue
        for k in json.load(open(f))["nodes"]:
            ids[k] = Path(f).name
    return ids


def test_d2_registry_kg_consistency_v1():
    kg = _kg_ids()
    v1 = [r["fault_id"] for r in json.load(open(COM / "comlab/config/global_fault_registry.json"))["registry"]]
    from comlab.core.fault_atlas_kg import FaultAtlasKG
    alias = FaultAtlasKG._ALIAS_MAP          # undocumented legacy-id alias map (code only)
    dup = sorted(k for k, c in collections.Counter(v1).items() if c > 1)
    v1 = [alias.get(x, x) for x in v1]
    no_node = sorted(set(v1) - set(kg))
    no_row = sorted(set(kg) - set(v1) - {"OPTIMAL_HEALTH"})
    print(f"v1 rows={len(v1)} unique={len(set(v1))} dup={dup} no_kg_node={no_node} kg_without_row={no_row}")
    assert not dup and not no_node and not no_row


def test_d2_registry_kg_consistency_v2_default_path():
    kg = _kg_ids()
    v2 = [(r["rule_id"], r["fault_family"]) for f in glob.glob(str(COM / "registry/rules/*.json"))
          for r in json.load(open(f))["rules"]]
    missing = sorted(rid for rid, _ in v2 if f"ERR-{rid}" not in kg)
    print(f"v2 rules={len(v2)} without KG node ERR-<rule_id>: {missing}")
    assert not missing


# --- D2-7: PRD §5.2/§5.4, HLD §4.3/§4.4, LLD §6.4 route() steps 2-3: winner enriched from
#     its KG node; power loss computed. Production default (REG-V2) path.
def test_d2_default_path_runs_stage_c_and_d():
    out = LabPipelineAggregator().process(_req(chem="LEAN_MIXTURE", gas_kw={"lambda_chem": 1.08},
                                               dtc_kw={"freeze_frame": _ff(long_term_ft1=15.0, short_term_ft1=8.0)},
                                               obd_kw={"total_trim_correction_delta": 23.0}))
    v, fe, pa = out.diagnostic_verdict, out.fault_enrichment, out.performance_analytics
    kg = _kg_ids()
    print("winner:", v.fault_code, v.fault_family, "KG node ERR-id present:", f"ERR-{v.fault_code}" in kg)
    print("enrichment:", fe.component_group, fe.impacted_subsystems, fe.ui_remediation_steps)
    print("power_loss:", pa.kinetic_power_loss_pct, "catalyst_idx:", pa.catalyst_efficiency_index_pct)
    assert fe.component_group != "engine" and fe.impacted_subsystems


# --- D2-8: ADR-0010 (Accepted) "A rule must clear MIN_CONFIDENCE_THRESHOLD = 0.70 to win"
#     + BDD "every candidate scores below 0.70 -> no_fault OPTIMAL_HEALTH". Default path.
def test_d2_confidence_floor_on_default_path():
    out = LabPipelineAggregator().process(_req(chem="TIMING_RETARDED", gas_kw={"gas_hc": 120}))
    v = out.diagnostic_verdict
    print("winner:", v.fault_code, v.fault_family, "score:", v.confidence_score,
          "is_fault:", v.is_fault_detected, "abstained:", v.abstained, v.abstain_reason)
    assert not (v.is_fault_detected and v.confidence_score < 0.70)


# --- D2-9: PRD §3 / LLD §6.2 / DLD §11.2 spell the non-start state `won_not_start`.
def test_d2_won_not_start_routes_as_documented():
    d = route_symptom({"environmental_conditions": {"engine_state": "won_not_start",
                                                    "occurs_during": "always"}})
    print("won_not_start ->", d)
    assert d.suppress_gaslab and d.suppress_obd_live_pids and d.suppress_mode06_ui


# --- D2-10: DTC_VOCABULARY §14 / §14.3: DtcLabDnaView "produced by COMLab.project(..., target='dtc')"
#     and consumed by DTCLab(raw_dtc_inputs, dna_view).
def _vehicle_dna(horizon="HORIZON_ADAPTIVE"):
    return {"vin_dna": {
        "engine_displacement_liters": 1.6, "cylinder_count": 4, "number_of_banks": 1,
        "euro_emission_category": "EURO_3", "fuel_delivery_type": "PORT_INJECTION",
        "induction_type": "NATURALLY_ASPIRATED", "upstream_o2_type": "NARROWBAND",
        "has_catalyst": True, "egr_equipped": True, "confidence": "HIGH",
        "resolved_horizon": horizon, "make": "VW", "model": "Golf", "model_year": 2002,
        "rated_rpm": 6200, "stress_idle_rpm_target": 3000,
        "air_metering_strategy": "MAF_ONLY",
        "emissions": {"upstream_o2_type": "NARROWBAND", "downstream_o2_present": True,
                      "has_catalyst": True, "egr_equipped": True}}}


def test_d2_dtc_view_projection_accepted_by_dtclab():
    from dtclab.schemas.dna_view import DtcLabDnaView as DtcSide
    view = project(_vehicle_dna(), target="dtc").model_dump(mode="json")
    try:
        DtcSide.model_validate(view)
        err = ""
    except ValidationError as exc:
        err = "; ".join(f"{e['loc']}:{e['type']}" for e in exc.errors())
    print("COMLab dtc view:", view)
    print("DTCLab rejects:", err)
    assert not err


# --- D2-11: LLD §3.2 VinDNA nests upstream_o2_type/has_catalyst/egr_equipped under `emissions`;
#     LLD §5.2 project(): "Precondition: vehicle_dna_json conforms to the VehicleDNA schema (§3.2)".
def test_d2_projection_of_lld_conformant_dna():
    dna = _vehicle_dna()
    for k in ("upstream_o2_type", "has_catalyst", "egr_equipped"):
        dna["vin_dna"].pop(k)
    try:
        project(dna, target="gas")
        err = ""
    except ValidationError as exc:
        err = "; ".join(f"{e['loc']}:{e['type']}" for e in exc.errors())
    print("projection of §3.2-conformant VinDNA:", err or "OK")
    assert not err


# --- D2-12: LLD §8.2 "Twelve files match the twelve values of FaultFamily"; DLD §2.2 lists 12.
def test_d2_kg_family_files_match_fault_family_enum():
    files = sorted(Path(f).stem for f in glob.glob(str(COM / "comlab/config/kg/*.json"))
                   if not Path(f).name.startswith("_"))
    enum = sorted(m.value for m in FaultFamily)
    print("kg files:", len(files), sorted(set(files) - set(enum)), "enum:", len(enum))
    assert files == enum
