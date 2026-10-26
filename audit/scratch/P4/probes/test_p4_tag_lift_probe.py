"""P4 probe: does the routing-tag lift that test_tag_discriminator.py claims ("gets +0.10 lift") apply at
all in the unit-test router? Run from labs/comlab:
  cd labs/comlab && python -m pytest -q -p no:cacheprovider ../../audit/scratch/P4/probes/test_p4_tag_lift_probe.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "labs/comlab/tests/unit"))
import pytest  # noqa: E402
from test_tag_discriminator import _make_request, _make_sanitized  # noqa: E402
from comlab.analytics.power_loss_analytics import PowerLossAnalytics  # noqa: E402
from comlab.core.fault_atlas_kg import FaultAtlasKG  # noqa: E402
from comlab.core.fault_atlas_router import FaultAtlasRouter  # noqa: E402
from comlab.schemas.vocabulary import DTCRoutingTag  # noqa: E402

_REG = Path(__file__).resolve().parents[4] / "labs/comlab/comlab/config/global_fault_registry.json"


@pytest.fixture(scope="module")
def router():  # same construction as test_tag_discriminator.router
    return FaultAtlasRouter(str(_REG), FaultAtlasKG(), PowerLossAnalytics(), use_v2_registry=False)


def test_misfire_history_tag_changes_the_winner_score(router):
    kw = dict(chemical_state="IGNITION_MISFIRE", horizon="HORIZON_MODERN", confirmed_dtcs=["P0300"],
              active_mil=False, short_term_ft1=6.0)
    no = router.execute_triage_loop(_make_sanitized(_make_request(routing_tags=[], **kw)))
    tag = router.execute_triage_loop(_make_sanitized(_make_request(
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY], **kw)))
    print("no-tag", no["winner"].fault_id, no["winner_score"], "tag", tag["winner"].fault_id,
          tag["winner_score"], "weight", router._discriminator_weight,
          "table has MISFIRE_HISTORY:", DTCRoutingTag.MISFIRE_HISTORY in router._discriminator_table)
    # the module docstring promises a lift; a lift that cannot be observed is a vacuous test
    assert tag["winner_score"] > no["winner_score"]


@pytest.mark.parametrize("stft", [6.0, 12.0, 20.0])
@pytest.mark.parametrize("mil", [False, True])
def test_discriminator_lift_never_exceeds_ceiling(router, mil, stft):
    """Kills mutant `_SCORE_CEILING -> 5.0` (fault_atlas_router.py:1135) by assertion: the docstring of
    test_discriminator_respects_score_cap says the boost "is capped at 1.0", but its own input scores 0.9
    before the +0.10 lift, so it reaches exactly 1.0 with or without the cap."""
    req = _make_request(chemical_state="IGNITION_MISFIRE", horizon="HORIZON_MODERN",
                        confirmed_dtcs=["P0300", "P0301"], active_mil=mil, short_term_ft1=stft,
                        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY, DTCRoutingTag.MISFIRE_HISTORY])
    v = router.execute_triage_loop(_make_sanitized(req))
    scores = [v["winner_score"]] + [float(r.get("score", 0.0)) if isinstance(r, dict) else
                                    float(getattr(r, "score", 0.0)) for r in v.get("runner_ups", [])]
    print("mil", mil, "stft", stft, v["winner"].fault_id, scores)
    assert max(scores) <= 1.0


_MF = dict(chemical_state="IGNITION_MISFIRE", horizon="HORIZON_MODERN", confirmed_dtcs=["P0300"],
           active_mil=False, short_term_ft1=6.0)


def test_tag_lift_goes_to_the_tagged_family(router):
    """Kills fault_atlas_router.py:1132 `kg_node.fault_family == target_family` -> `!=` (mutant
    router.execute_triage_loop#0028). tag_discriminator.yaml: MISFIRE_HISTORY -> family misfire, weight
    0.10; test_tag_discriminator.py docstring: 'The MISFIRE_HISTORY tag boosts the misfire family'."""
    no = router.execute_triage_loop(_make_sanitized(_make_request(routing_tags=[], **_MF)))
    tag = router.execute_triage_loop(_make_sanitized(_make_request(
        routing_tags=[DTCRoutingTag.MISFIRE_HISTORY], **_MF)))
    assert router._kg.resolve(tag["winner"].fault_id).fault_family == "misfire"
    assert tag["winner"].fault_id == no["winner"].fault_id
    assert abs(tag["winner_score"] - min(no["winner_score"] + router._discriminator_weight, 1.0)) < 1e-9


def test_unmapped_tag_is_neutral(router):
    """Kills fault_atlas_router.py:1124 guard deletion `if mapping is None: continue` (mutant
    router.execute_triage_loop#0026). Router comment: 'Absent/unmapped tag -> neutral'. INJECTOR_HISTORY is a
    DTCRoutingTag with no tag_discriminator.yaml mapping; test_unmapped_tag_neutral passes O2_HISTORY,
    which IS mapped."""
    assert DTCRoutingTag.INJECTOR_HISTORY not in router._discriminator_table
    no = router.execute_triage_loop(_make_sanitized(_make_request(routing_tags=[], **_MF)))
    try:
        tag = router.execute_triage_loop(_make_sanitized(_make_request(
            routing_tags=[DTCRoutingTag.INJECTOR_HISTORY], **_MF)))
    except Exception as e:  # noqa: BLE001 - an unmapped tag must be neutral, not a crash
        pytest.fail(f"unmapped routing tag crashed the triage loop: {type(e).__name__}: {e}")
    assert (tag["winner"].fault_id, tag["winner_score"]) == (no["winner"].fault_id, no["winner_score"])
