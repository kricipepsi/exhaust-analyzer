"""T-COMA-12: F-C1-18 one discriminator lift per family; F-C1-19 the abstain margin absorbs float noise; F-C1-20 the
catalyst-override pattern covers P0309. Tags: NEW fails on the base; PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

TABLE = {"LEAN_HISTORY": {"family": "lean_condition"}, "EVAP_HISTORY": {"family": "lean_condition"},
         "RICH_HISTORY": {"family": "rich_mixture"}}


@pytest.mark.parametrize(("tags", "families"), [
    (["LEAN_HISTORY", "LEAN_HISTORY"], {"lean_condition"}),
    (["LEAN_HISTORY", "EVAP_HISTORY"], {"lean_condition"}),
    (["LEAN_HISTORY", "RICH_HISTORY", "UNKNOWN_TAG"], {"lean_condition", "rich_mixture"}),
    ([], set()),
])
def test_each_family_is_lifted_once(tags, families):
    """NEW: a repeated tag, or two tags of one family, lift that family once; an unknown tag lifts nothing."""
    from comlab.core.fault_atlas_router import _discriminator_families

    assert _discriminator_families(tags, TABLE) == families


def test_margin_absorbs_float_noise():
    """NEW: the shim's SF-004 arithmetic (0.72 + 0.05 + 0.05) against 0.80 is a 0.02 gap: within the margin."""
    from comlab.core.fault_atlas_router import _within_abstain_margin

    top = 0.72
    top += 0.05
    top += 0.05
    assert _within_abstain_margin(top, 0.80)


@pytest.mark.parametrize(("winner", "runner", "within"), [(0.83, 0.80, False), (0.81, 0.80, True), (0.80, 0.80, True)])
def test_margin_boundaries(winner, runner, within):
    """PIN: a 0.03 gap is outside the margin; 0.01 and 0 are inside."""
    from comlab.core.fault_atlas_router import _within_abstain_margin

    assert _within_abstain_margin(winner, runner) is within


@pytest.mark.parametrize(("code", "match"), [("P0309", True), ("P0300", True), ("P0308", True), ("P0310", False),
                                             ("P0420", False)])
def test_p030x_pattern_matches_the_wiki(code, match):
    """NEW (P0309) and PIN: wiki 07 §RULE_CAT_OVERRIDE: ^P030[0-9]$."""
    from comlab.core.fault_atlas_router import _P030X_RE

    assert bool(_P030X_RE.match(code)) is match
