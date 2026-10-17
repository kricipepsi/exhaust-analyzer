"""Shared helpers for the C2 (GASLab) audit probes. Audit scratch only."""

from __future__ import annotations

from gaslab.brettschneider import lambda_chem
from gaslab.contracts import EngineStateBucket, GasReading
from gaslab.dna_view import GasLabDnaView
from gaslab.ontology_loader import load_ontology
from gaslab.process import GasLabContext, process
from gaslab.rule_engine import classify

ONT = load_ontology()
IDLE = EngineStateBucket.STABILIZED_IDLE


def dna(**kw) -> GasLabDnaView:
    base = dict(
        engine_displacement_liters=1.6,
        cylinder_count=4,
        number_of_banks=1,
        euro_emission_category="EURO_4",
        fuel_delivery_type="PORT_INJECTION",
        induction_type="NATURALLY_ASPIRATED",
        upstream_o2_type="NARROWBAND",
        has_catalyst=True,
        egr_equipped=False,
    )
    base.update(kw)
    return GasLabDnaView(**base)


def R(hc, co, co2, o2, nox) -> GasReading:
    return GasReading(hc=hc, co=co, co2=co2, o2=o2, nox=nox)


def run(reading, d=None, state=IDLE, ontology=None, **kw):
    sig, val = classify(reading, d or dna(), state, ontology or ONT, **kw)
    return sig.value, val.value


def lam(reading) -> float:
    return round(lambda_chem(reading), 4)


__all__ = ["ONT", "IDLE", "dna", "R", "run", "lam", "process", "GasLabContext", "EngineStateBucket"]
