"""C1 probes: verdict/severity/confidence shape on the default REG-V2 path."""
from __future__ import annotations

import logging

from c1_builders import aggregator, dtc, ff, request, run

logging.disable(logging.CRITICAL)

PRISTINE = dict(gas_hc=30, gas_co=0.1, gas_co2=15.0, gas_o2=0.3, gas_nox=40)


# --- F3: the no_fault rule wins but the verdict says "fault detected" ---------------

def test_no_fault_winner_is_not_reported_as_fault():
    out = run(request(chem="NORMAL_OPERATION", gas_kw=PRISTINE))
    v = out.diagnostic_verdict
    sev = out.performance_analytics.severity_level
    print("verdict:", v.fault_code, v.fault_family, v.is_fault_detected, sev)
    assert v.fault_family == "no_fault"            # precondition: NF-001 won
    # Claim: SeverityLevel.OPTIMAL_HEALTH = "no fault detected"; FaultFamily.NO_FAULT =
    # "all diagnostics pass; no anomaly detected".
    assert v.is_fault_detected is False
    assert sev == "OPTIMAL_HEALTH"


# --- F4: catalyst-damage override never applied on the default path -----------------

def test_flashing_mil_with_p0301_forces_critical_stop():
    req = request(chem="IGNITION_MISFIRE",
                  dtc_kw=dict(confirmed=["P0301"], mil=True, flashing=True,
                              tags=["MISFIRE_HISTORY"]))
    out = run(req)
    v = out.diagnostic_verdict
    sev = out.performance_analytics.severity_level
    print("verdict:", v.fault_code, v.fault_family, "severity:", sev)
    # Claim: wiki 07 §RULE_CAT_OVERRIDE / ADR-0010 / BDD — forced CRITICAL_IMMEDIATE_STOP.
    assert sev == "CRITICAL_IMMEDIATE_STOP"


def test_v1_override_regex_matches_wiki_p030_0_to_9():
    """Wiki 07 §RULE_CAT_OVERRIDE and HLD §4.2 cite ^P030[0-9]$; code uses ^P030[0-8]$."""
    from comlab.core.fault_atlas_router import _P030X_RE
    print("pattern:", _P030X_RE.pattern, "P0309 matches:", bool(_P030X_RE.match("P0309")))
    assert _P030X_RE.match("P0309")


# --- F6: symptom prior / discriminator re-sort writes another rule's score ----------

def test_reported_confidence_belongs_to_reported_fault():
    from registry.integration_shim import route_case_with_diagnostics
    from comlab.core.symptom_router import route_symptom
    from comlab.schemas.vocabulary import Horizon

    req = request(chem="LEAN_MISFIRE", symptom={
        "environmental_conditions": {"engine_state": "running", "occurs_during": "always"},
        "_csv_primary_symptom": "non_starter"})
    agg = aggregator()
    out = agg.process(req)
    v = out.diagnostic_verdict
    san = agg._build_sanitized_payload(req, route_symptom(req.symptom_dna),
                                       Horizon(req.metadata.resolved_horizon), "FULL_FUSION")
    _, diag = route_case_with_diagnostics(san)
    ranked = [(r["rule_id"], r["fault_family"], round(r["score"], 3)) for r in diag["scored_rules"][:4]]
    own = [r for r in diag["scored_rules"] if r["rule_id"] == v.fault_code][0]
    print("verdict:", v.fault_code, v.fault_family, "reported:", v.confidence_score,
          "own raw score:", own["score"], "abstain:", v.abstain_reason, "pre-prior ranking:", ranked)
    # own family (misfire) is not the prior's target (non_starter) -> score must be unchanged
    assert abs(v.confidence_score - own["score"]) < 1e-9


# --- F7: execution_meta.vin_confidence is hard-coded --------------------------------

def test_vin_confidence_is_passed_through():
    out = run(request(chem="RICH_MIXTURE", vin_conf="PARTIAL"))
    print("in: PARTIAL  out:", out.execution_meta.vin_confidence,
          "degradation:", out.execution_meta.degradation_mode)
    assert out.execution_meta.vin_confidence == "PARTIAL"


# --- F8: processing_confidence_rating depends on horizon only -----------------------

def test_clean_full_fusion_high_vin_is_high_assurance():
    """BDD 'All four labs reporting cleanly is full fusion' -> HIGH_ASSURANCE."""
    out = run(request(chem="NORMAL_OPERATION", gas_kw=PRISTINE, horizon="HORIZON_ADAPTIVE"))
    m = out.execution_meta
    print("degradation:", m.degradation_mode, "rating:", m.processing_confidence_rating,
          "verdict conf:", out.diagnostic_verdict.confidence_score)
    assert m.degradation_mode == "FULL_FUSION"
    assert m.processing_confidence_rating == "HIGH_ASSURANCE"


def test_rating_tracks_verdict_confidence_not_era():
    """Same evidence, different era -> rating flips although verdict+score are identical."""
    a = run(request(chem="RICH_MIXTURE", horizon="HORIZON_LEGACY"))
    b = run(request(chem="RICH_MIXTURE", horizon="HORIZON_MODERN"))
    print("LEGACY:", a.diagnostic_verdict.fault_code, a.diagnostic_verdict.confidence_score,
          a.execution_meta.processing_confidence_rating)
    print("MODERN:", b.diagnostic_verdict.fault_code, b.diagnostic_verdict.confidence_score,
          b.execution_meta.processing_confidence_rating)
    # wiki 09 §CONCEPT_CONF_TIER: tier = band of the (calibrated) score; 1.0 is >= 0.80.
    assert a.execution_meta.processing_confidence_rating != "LOW_CERTAINTY"
