"""D2 probes (GASLab) — each test asserts what a GASLab design-chain document states.

A FAILING test reproduces a finding. Run from the repo root:
    python -m pytest -q audit/scratch/D2/test_d2_gaslab_probes.py -p no:cacheprovider -rA
Evidence only.
"""
from __future__ import annotations

import yaml
from pathlib import Path

from gaslab.contracts import ChemicalSignature, EngineStateBucket, GasLabPayload, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.process import GasLabContext, process
from gaslab.rule_engine import classify

ROOT = Path(__file__).resolve().parents[3]
ONTO = ROOT / "labs/gaslab/gaslab/data/gas_lab_ontology.yaml"


def _dna(**kw):
    d = dict(engine_displacement_liters=2.0, cylinder_count=4, number_of_banks=1,
             euro_emission_category="Euro 4", fuel_delivery_type="PORT", induction_type="NA",
             upstream_o2_type="NARROWBAND", has_catalyst=True, egr_equipped=False, confidence="HIGH")
    d.update(kw)
    return GasLabDnaView(**d)


# GAS_VOCABULARY.md §3.1 — "`HIGH_COMBUSTION_TEMP` | none"; HLD §5 "6 DNA-gated faults" (HCT not listed).
def test_d2g_hct_not_dna_gated():
    r = GasReading(hc=50, co=0.3, co2=14.5, o2=0.3, nox=1500)
    no_egr = classify(r, _dna(egr_equipped=False), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    egr = classify(r, _dna(egr_equipped=True), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    print("egr_equipped=False ->", no_egr, "| egr_equipped=True ->", egr)
    assert no_egr[0] == egr[0] == ChemicalSignature.HIGH_COMBUSTION_TEMP


# PRD KR3 / §8 success criterion 2, HLD §3 [1] + §4, ADR-0006: exactly 3 catch-alls
# (VVT_FAILURE, EVAP_CANISTER_SATURATED, POA_SIGNATURE); HLD §4 files INCOMPLETE_OXIDATION
# under "Catalyst (DNA-gated)".
def test_d2g_catch_all_set():
    f = yaml.safe_load(ONTO.read_text())["faults"]
    ca = sorted(k for k, v in f.items() if v.get("signature_type") == "catch_all")
    gated = sorted(k for k, v in f.items() if v.get("dna_gate"))
    print("catch_all:", ca, "| dna_gate:", gated)
    assert ca == sorted(["VVT_FAILURE", "EVAP_CANISTER_SATURATED", "POA_SIGNATURE"])
    assert "INCOMPLETE_OXIDATION" in gated


# PRD §7 "GasLabPayload Pydantic output model (9 fields ...)"; HLD §3 "GasLabPayload (9 fields)";
# DLD §2 "GasLabPayload (Pydantic BaseModel, 9 fields)".
def test_d2g_payload_field_count():
    print("GasLabPayload fields:", len(GasLabPayload.model_fields), list(GasLabPayload.model_fields))
    assert len(GasLabPayload.model_fields) == 9


# BDD_GASLab.md:320 "A directly-measured lambda is passed through when supplied" (process boundary).
def test_d2g_lambda_measured_passthrough():
    r = GasReading(hc=15, co=0.2, co2=15.0, o2=0.2, nox=50)
    out = process(r, GasLabContext(dna=_dna(), engine_state=EngineStateBucket.STABILIZED_IDLE,
                                   lambda_measured=1.07))
    out2 = process(r, GasLabContext(dna=_dna(), engine_state=EngineStateBucket.STABILIZED_IDLE))
    print("lambda_measured passthrough:", out.lambda_measured, "| absent:", out2.lambda_measured)
    assert out.lambda_measured == 1.07 and out2.lambda_measured is None


# GAS_VOCABULARY §13 invariant 7 + wiki 10_limited_scope_confidence.md §10.2 table:
# "`GDI_INTAKE_VALVE_CARBON`, `GDI_HPFP_INTERNAL_SEAL_LEAK` | ✓ if `GDI` | ✗ | ✗" (HIGH|PARTIAL|NONE).
# ADR-0005/ADR-0011 (Accepted) decide the opposite: gates are strict and ignore confidence.
def test_d2g_confidence_shrinks_scope_per_vocab_invariant_7():
    r = GasReading(hc=2270, co=4.2, co2=11.7, o2=0.03, nox=5)  # inside GDI_HPFP box (found by grid search)
    hi = classify(r, _dna(fuel_delivery_type="GDI", confidence="HIGH"), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    part = classify(r, _dna(fuel_delivery_type="GDI", confidence="PARTIAL"), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    no = classify(r, _dna(fuel_delivery_type="GDI", confidence="NONE"), EngineStateBucket.STABILIZED_IDLE, load_ontology())
    print("GDI car  HIGH ->", hi[0].value, "| PARTIAL ->", part[0].value, "| NONE ->", no[0].value)
    assert hi[0] == ChemicalSignature.GDI_HPFP_INTERNAL_SEAL_LEAK
    assert part[0] != ChemicalSignature.GDI_HPFP_INTERNAL_SEAL_LEAK
    assert no[0] != ChemicalSignature.GDI_HPFP_INTERNAL_SEAL_LEAK
